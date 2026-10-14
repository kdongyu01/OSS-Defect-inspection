"""Export a GitHub Project v2 snapshot for the project metrics calculator."""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = "https://api.github.com/graphql"
DEFAULT_OWNER = "kdongyu01"
DEFAULT_PROJECT_NUMBER = 4
METRICS_DIR = Path("metrics")
EVENTS_PATH = METRICS_DIR / "project_events.csv"
ITEMS_PATH = METRICS_DIR / "sprint_items.csv"


def graphql(query: str, variables: dict[str, object]) -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN 또는 GITHUB_TOKEN 환경변수를 설정하세요.")
    request = Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except (HTTPError, URLError) as error:
        raise SystemExit(f"GitHub Project API 요청 실패: {error}") from error
    if result.get("errors"):
        raise SystemExit(json.dumps(result["errors"], ensure_ascii=False))
    return result["data"]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_project_owner() -> str:
    return os.environ.get("PROJECT_OWNER", DEFAULT_OWNER)


def read_project_number() -> int:
    value = os.environ.get("PROJECT_NUMBER")
    if value is None:
        return DEFAULT_PROJECT_NUMBER
    try:
        number = int(value)
    except ValueError as error:
        raise SystemExit(f"PROJECT_NUMBER는 숫자여야 합니다. 현재 값: {value!r}") from error
    if number <= 0:
        raise SystemExit(f"PROJECT_NUMBER는 1 이상의 숫자여야 합니다. 현재 값: {value!r}")
    return number


def fetch_project() -> list[dict[str, str]]:
    owner = read_project_owner()
    project_number = read_project_number()
    query = """
    query($login: String!, $number: Int!) {
      user(login: $login) {
        projectV2(number: $number) {
          items(first: 100) {
            nodes {
              content {
                ... on Issue { number title }
                ... on PullRequest { number title }
              }
              fieldValues(first: 50) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    field { ... on ProjectV2SingleSelectField { name } }
                    name
                  }
                  ... on ProjectV2ItemFieldNumberValue {
                    field { ... on ProjectV2Field { name } }
                    number
                  }
                  ... on ProjectV2ItemFieldTextValue {
                    field { ... on ProjectV2Field { name } }
                    text
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    project = graphql(query, {"login": owner, "number": project_number})["user"]["projectV2"]
    if not project:
        raise SystemExit(f"{owner}의 Project #{project_number}를 찾을 수 없습니다.")
    result = []
    for node in project["items"]["nodes"]:
        content = node.get("content") or {}
        if not content.get("number"):
            continue
        values: dict[str, object] = {}
        for value in node["fieldValues"]["nodes"]:
            field = value.get("field") or {}
            if field.get("name"):
                values[field["name"]] = value.get("name", value.get("number", value.get("text")))
        result.append({
            "issue_number": str(content["number"]),
            "title": content.get("title", ""),
            "sprint": str(values.get("Sprint", "Unassigned")),
            "story_points": str(values.get("Story Points", 0) or 0),
            "status": str(values.get("Status", "Backlog")),
        })
    return result


def main() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    items = fetch_project()
    events = read_rows(EVENTS_PATH)
    for item in items:
        if not any(
            row["issue_number"] == item["issue_number"]
            and row["status"] == item["status"]
            and row["timestamp"].startswith(timestamp[:10])
            for row in events
        ):
            events.append({
                "issue_number": item["issue_number"],
                "status": item["status"],
                "timestamp": timestamp,
            })
    write_rows(EVENTS_PATH, ["issue_number", "status", "timestamp"], events)
    current = {row["issue_number"]: row for row in read_rows(ITEMS_PATH)}
    current.update({item["issue_number"]: item for item in items})
    write_rows(ITEMS_PATH, ["issue_number", "title", "sprint", "story_points", "status"], list(current.values()))
    print(f"exported_items={len(items)} event_rows={len(events)}")


if __name__ == "__main__":
    main()
