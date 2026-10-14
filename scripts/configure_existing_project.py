"""Configure the existing OSS-Defect inspection Project v2 fields.

The script is intentionally idempotent. It never creates another Project.
Set GH_TOKEN with classic ``project`` or fine-grained Projects write access.
"""

from __future__ import annotations

import json
import os
import sys
from urllib.request import Request, urlopen


API = "https://api.github.com/graphql"
PROJECT_NUMBER = 2
OWNER = "kdongyu01"


def graphql(query: str, variables: dict) -> dict:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN 또는 GITHUB_TOKEN 환경변수를 설정하세요.")
    request = Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise SystemExit(json.dumps(result["errors"], ensure_ascii=False))
    return result["data"]


def get_project() -> tuple[str, list[dict]]:
    query = """
    query($login: String!, $number: Int!) {
      user(login: $login) {
        projectV2(number: $number) {
          id
          title
          fields(first: 100) {
            nodes {
              __typename
              ... on ProjectV2Field { id name dataType }
              ... on ProjectV2SingleSelectField { id name options { id name } }
            }
          }
        }
      }
    }
    """
    project = graphql(query, {"login": OWNER, "number": PROJECT_NUMBER})["user"]["projectV2"]
    if not project:
        raise SystemExit(f"Project #{PROJECT_NUMBER}를 찾을 수 없습니다.")
    return project["id"], project["fields"]["nodes"]


def create_field(project_id: str, name: str, data_type: str, options: list[str] | None = None) -> None:
    mutation = """
    mutation($input: CreateProjectV2FieldInput!) {
      createProjectV2Field(input: $input) {
        projectV2Field { __typename ... on ProjectV2Field { name } ... on ProjectV2SingleSelectField { name } }
      }
    }
    """
    input_data = {"projectId": project_id, "name": name, "dataType": data_type}
    if options:
        input_data["singleSelectOptions"] = options
    result = graphql(mutation, {"input": input_data})
    field = result["createProjectV2Field"]["projectV2Field"]
    print(f"created field: {field['name']}")


def main() -> None:
    if "--dry-run" in sys.argv:
        print(json.dumps({
            "project": f"https://github.com/users/{OWNER}/projects/{PROJECT_NUMBER}",
            "fields": {
                "Priority": ["High", "Medium", "Low"],
                "Story Points": "number",
                "Type": ["Feature", "Bug", "Docs", "Chore"],
            },
            "note": "Status 기본 필드는 GitHub Project 화면에서 옵션명을 확인하세요.",
        }, ensure_ascii=False, indent=2))
        return

    project_id, fields = get_project()
    existing = {field.get("name") for field in fields}
    print(f"project: {OWNER} #{PROJECT_NUMBER}")
    if "Priority" not in existing:
        create_field(project_id, "Priority", "SINGLE_SELECT", ["High", "Medium", "Low"])
    if "Story Points" not in existing:
        create_field(project_id, "Story Points", "NUMBER")
    if "Type" not in existing:
        create_field(project_id, "Type", "SINGLE_SELECT", ["Feature", "Bug", "Docs", "Chore"])
    print("Project field configuration complete")


if __name__ == "__main__":
    main()
