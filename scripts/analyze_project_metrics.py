"""Calculate Cycle Time, Velocity, and Burndown from exported Project data."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


METRICS_DIR = Path("metrics")
EVENTS = METRICS_DIR / "project_events.csv"
ITEMS = METRICS_DIR / "sprint_items.csv"


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_cycle_time(events: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for event in events:
        grouped[event["issue_number"]].append(event)

    results = []
    for issue_number, issue_events in grouped.items():
        in_progress = [event for event in issue_events if event["status"] == "In Progress"]
        done = [event for event in issue_events if event["status"] == "Done"]
        if not in_progress or not done:
            continue
        start = min(parse_time(event["timestamp"]) for event in in_progress)
        finish = min(parse_time(event["timestamp"]) for event in done)
        if finish < start:
            continue
        hours = round((finish - start).total_seconds() / 3600, 2)
        results.append({"issue_number": issue_number, "cycle_time_hours": hours})
    return sorted(results, key=lambda result: result["issue_number"])


def calculate_velocity(items: list[dict[str, str]]) -> list[dict[str, object]]:
    totals: dict[str, int] = defaultdict(int)
    for item in items:
        if item["status"] == "Done":
            totals[item["sprint"]] += int(item["story_points"])
    return [{"sprint": sprint, "completed_story_points": points} for sprint, points in sorted(totals.items())]


def calculate_burndown(items: list[dict[str, str]], events: list[dict[str, str]]) -> list[dict[str, object]]:
    points_by_issue = {item["issue_number"]: int(item["story_points"]) for item in items}
    dates = sorted({event["timestamp"][:10] for event in events})
    if not dates:
        return []
    total = sum(points_by_issue.values())
    result = []
    for date in dates:
        completed = 0
        for issue_number, points in points_by_issue.items():
            done_events = [
                event for event in events
                if event["issue_number"] == issue_number
                and event["status"] == "Done"
                and event["timestamp"][:10] <= date
            ]
            if done_events:
                completed += points
        result.append({"date": date, "total_points": total, "done_points": completed, "remaining_points": total - completed})
    return result


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    events = read_rows(EVENTS)
    items = read_rows(ITEMS)
    cycle_time = calculate_cycle_time(events)
    velocity = calculate_velocity(items)
    burndown = calculate_burndown(items, events)
    write_csv(METRICS_DIR / "cycle-time.csv", cycle_time)
    write_csv(METRICS_DIR / "velocity.csv", velocity)
    write_csv(METRICS_DIR / "burndown.csv", burndown)
    (METRICS_DIR / "project-metrics.json").write_text(
        json.dumps(
            {"cycle_time": cycle_time, "velocity": velocity, "burndown": burndown},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"cycle_time={len(cycle_time)} velocity={len(velocity)} burndown={len(burndown)}")


if __name__ == "__main__":
    main()
