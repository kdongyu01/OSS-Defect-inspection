"""Create the repository labels, milestones, issues, and a Project v2."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


API = "https://api.github.com"
OWNER = "kdongyu01"
REPOSITORY = "OSS-Defect-inspection"

LABELS = [
    ("type:feature", "7057ff", "기능 개발"),
    ("type:bug", "d73a4a", "버그 수정"),
    ("type:docs", "0075ca", "문서 작업"),
    ("type:chore", "6f42c1", "설정·유지보수"),
    ("priority:high", "b60205", "높은 우선순위"),
    ("priority:medium", "fbca04", "중간 우선순위"),
    ("priority:low", "0e8a16", "낮은 우선순위"),
    ("area:data", "1d76db", "데이터"),
    ("area:model", "5319e7", "모델"),
    ("area:ui", "c2e0c6", "화면"),
    ("area:deployment", "bfdadc", "배포"),
    ("area:metrics", "f9d0c4", "메트릭"),
    ("status:blocked", "b60205", "차단됨"),
    ("status:needs-review", "fbca04", "리뷰 필요"),
]

MILESTONES = [
    ("MVP Foundation", "GitHub 환경·데이터·기준선 검사·DORA 기반"),
    ("Demo Release", "결과 시각화·배포·평가·발표 준비"),
]

ISSUES = [
    ("Git/GitHub 개발 환경 구성", "type:chore,priority:high", 2, "MVP Foundation"),
    ("프로젝트 README 작성", "type:docs,priority:medium", 2, "MVP Foundation"),
    ("포장 결함 라벨 기준 정의", "type:feature,priority:high", 3, "MVP Foundation"),
    ("샘플 데이터 수집 및 메타데이터 작성", "type:feature,priority:high,area:data", 5, "MVP Foundation"),
    ("이미지 업로드와 파일 검증 구현", "type:feature,priority:high,area:ui", 3, "MVP Foundation"),
    ("제품 ROI 전처리 구현", "type:feature,priority:high,area:model", 5, "MVP Foundation"),
    ("SSIM 기준선 검사 구현", "type:feature,priority:high,area:model", 5, "MVP Foundation"),
    ("결함 의심 영역 시각화 구현", "type:feature,priority:medium,area:model", 3, "Demo Release"),
    ("Gradio 결과 화면 구현", "type:feature,priority:high,area:ui", 3, "Demo Release"),
    ("DORA Lead Time Workflow 구현", "type:feature,priority:medium,area:metrics", 5, "MVP Foundation"),
    ("주간 DORA JSON 리포트 생성", "type:feature,priority:medium,area:metrics", 5, "Demo Release"),
    ("Render 배포 및 모바일 점검", "type:chore,priority:high,area:deployment", 3, "Demo Release"),
]


def request(path: str, method: str = "GET", payload: dict | None = None) -> dict | list:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN 또는 GITHUB_TOKEN 환경변수를 설정한 뒤 실행하세요.")
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    with urlopen(Request(f"{API}{path}", data=body, headers=headers, method=method), timeout=30) as response:
        return json.load(response)


def create_label(name: str, color: str, description: str) -> None:
    path = f"/repos/{OWNER}/{REPOSITORY}/labels"
    try:
        request(path, "POST", {"name": name, "color": color, "description": description})
        print(f"created label: {name}")
    except HTTPError as error:
        if error.code == 422:
            print(f"exists label: {name}")
        else:
            raise


def create_milestone(title: str, description: str) -> int:
    path = f"/repos/{OWNER}/{REPOSITORY}/milestones"
    existing = request(path + "?state=all&per_page=100")
    for milestone in existing:
        if milestone["title"] == title:
            print(f"exists milestone: {title}")
            return milestone["number"]
    created = request(path, "POST", {"title": title, "description": description})
    print(f"created milestone: {title}")
    return created["number"]


def create_issue(title: str, labels: str, points: int, milestone: int) -> str:
    path = f"/repos/{OWNER}/{REPOSITORY}/issues"
    existing = request(path + "?state=all&per_page=100")
    for issue in existing:
        if issue["title"] == title:
            print(f"exists issue: {title}")
            return issue["node_id"]
    body = f"## 완료 조건\n\n- [ ] 기능 구현\n- [ ] 테스트 또는 수동 검증\n\nStory Points: {points}"
    created = request(
        path,
        "POST",
        {"title": title, "body": body, "labels": labels.split(","), "milestone": milestone},
    )
    print(f"created issue #{created['number']}: {title}")
    return created["node_id"]


def graphql(query: str, variables: dict) -> dict:
    result = request("/graphql", "POST", {"query": query, "variables": variables})
    if result.get("errors"):
        errors = json.dumps(result["errors"], ensure_ascii=False)
        error_types = {error.get("type") for error in result["errors"]}
        if "INSUFFICIENT_SCOPES" in error_types:
            raise SystemExit(
                "현재 토큰에 Project API 권한이 없습니다. "
                "classic PAT를 사용하는 경우 Settings > Developer settings > "
                "Personal access tokens에서 project와 read:project scope를 추가하거나 "
                "해당 scope로 새 토큰을 발급한 뒤 다시 실행하세요. "
                f"GitHub 응답: {errors}"
            )
        if "FORBIDDEN" in error_types:
            raise SystemExit(
                "Project 생성 권한이 없습니다. "
                "토큰의 사용자 Projects 권한을 Read and write로 설정하거나 "
                "classic PAT의 project scope를 추가한 뒤 다시 실행하세요. "
                f"GitHub 응답: {errors}"
            )
        raise RuntimeError(errors)
    return result["data"]


def create_project() -> str:
    owner_data = graphql("query { viewer { id login } }", {})
    owner_id = owner_data["viewer"]["id"]
    mutation = """
    mutation($ownerId: ID!, $title: String!) {
      createProjectV2(input: {ownerId: $ownerId, title: $title}) {
        projectV2 { id number url }
      }
    }
    """
    project = graphql(mutation, {"ownerId": owner_id, "title": "OSS-Defect inspection Sprint Board"})
    result = project["createProjectV2"]["projectV2"]
    print(f"created project: {result['url']}")
    return result["id"]


def add_issue_to_project(project_id: str, issue_id: str) -> None:
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                item { id }
            }
        }
        """
        graphql(mutation, {"projectId": project_id, "contentId": issue_id})


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print(json.dumps({"labels": LABELS, "milestones": MILESTONES, "issues": ISSUES}, ensure_ascii=False, indent=2))
        return

    for label in LABELS:
        create_label(*label)
    milestone_ids = {title: create_milestone(title, description) for title, description in MILESTONES}
    issue_ids = [
        create_issue(title, labels, points, milestone_ids[milestone])
        for title, labels, points, milestone in ISSUES
    ]
    project_id = create_project()
    for issue_id in issue_ids:
        add_issue_to_project(project_id, issue_id)
    print(f"added {len(issue_ids)} issues to Project v2")


if __name__ == "__main__":
    main()
