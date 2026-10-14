"""Generate a small, explainable DORA report from GitHub REST API data."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
REPORT_PATH = Path("metrics/dora.json")
MARKDOWN_PATH = Path("metrics/weekly-report.md")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def request_json(path: str) -> list | dict:
    token = os.environ.get("GH_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token:
        raise RuntimeError("GH_TOKEN is required to collect DORA metrics")
    if not repository:
        raise RuntimeError("GITHUB_REPOSITORY is required to collect DORA metrics")

    request = Request(
        f"{API_ROOT}/repos/{repository}/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def hours_between(start: datetime | None, end: datetime | None) -> float | None:
    if not start or not end:
        return None
    return round((end - start).total_seconds() / 3600, 2)


def average(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 2) if values else None


def collect_report() -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    pulls = request_json("pulls?state=closed&sort=updated&direction=desc&per_page=100")
    deployments = request_json("deployments?environment=production&per_page=100")
    issues = request_json("issues?state=all&labels=incident&per_page=100")

    lead_times = []
    for pull in pulls:
        merged_at = parse_time(pull.get("merged_at"))
        created_at = parse_time(pull.get("created_at"))
        if merged_at and start <= merged_at <= end:
            lead_time = hours_between(created_at, merged_at)
            if lead_time is not None:
                lead_times.append(lead_time)

    successful_deployments = 0
    failed_deployments = 0
    for deployment in deployments:
        created_at = parse_time(deployment.get("created_at"))
        if not created_at or not start <= created_at <= end:
            continue
        statuses = request_json(
            f"deployments/{deployment['id']}/statuses?per_page=10"
        )
        latest = statuses[0].get("state") if statuses else "unknown"
        if latest == "success":
            successful_deployments += 1
        elif latest in {"failure", "error"}:
            failed_deployments += 1

    recovery_times = []
    for issue in issues:
        created_at = parse_time(issue.get("created_at"))
        closed_at = parse_time(issue.get("closed_at"))
        if created_at and start <= created_at <= end and closed_at:
            recovery_time = hours_between(created_at, closed_at)
            if recovery_time is not None:
                recovery_times.append(recovery_time)

    total_deployments = successful_deployments + failed_deployments
    return {
        "period": {"start": start.date().isoformat(), "end": end.date().isoformat()},
        "lead_time_hours": {
            "average": average(lead_times),
            "sample_count": len(lead_times),
            "definition": "Pull Request created_at to merged_at proxy",
        },
        "deployment_frequency": {
            "successful_deployments": successful_deployments,
            "period_days": 7,
        },
        "mttr_hours": {
            "average": average(recovery_times),
            "incident_count": len(recovery_times),
            "definition": "incident Issue created_at to closed_at",
        },
        "change_failure_rate": {
            "failed_changes": failed_deployments,
            "total_changes": total_deployments,
            "percentage": round(failed_deployments / total_deployments * 100, 2)
            if total_deployments
            else None,
            "definition": "failed production deployment statuses / all production deployment statuses",
        },
    }


def render_markdown(report: dict) -> str:
    period = report["period"]
    lead = report["lead_time_hours"]
    frequency = report["deployment_frequency"]
    mttr = report["mttr_hours"]
    failure = report["change_failure_rate"]
    return f"""# DORA Weekly Report

기간: {period['start']} ~ {period['end']}

| 지표 | 결과 |
|---|---:|
| Lead Time | {lead['average']} hours |
| Deployment Frequency | {frequency['successful_deployments']} successful deployments |
| MTTR | {mttr['average']} hours |
| Change Failure Rate | {failure['percentage']}% |

## 측정 기준

- Lead Time은 현재 구현에서 PR 생성부터 Merge까지를 대리 지표로 사용합니다.
- MTTR은 `incident` 라벨이 붙은 Issue의 생성부터 종료까지를 계산합니다.
- Change Failure Rate는 production 배포 상태의 failure/error 비율입니다.
- 표본이 작을 때는 제품 성과나 비용 절감으로 해석하지 않습니다.
"""


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = collect_report()
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    MARKDOWN_PATH.write_text(render_markdown(report), encoding="utf-8")


if __name__ == "__main__":
    main()
