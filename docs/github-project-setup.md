# GitHub Project 구성안

실제 Project: [OSS-Defect inspection Sprint Board](https://github.com/users/kdongyu01/projects/4)

현재 자동화 완료 상태:

- 라벨 생성 완료
- 마일스톤 2개 생성 완료
- Issue 12개 생성 및 Project 연결 완료
- 현재 Project(#4)의 Priority·Story Points·Type 필드는
  Project 설정 화면에서 확인·보정 가능
- GitHub 기본 Status 필드의 옵션명·순서는 Project 화면에서 최종 확인 필요

## 상태

`Backlog` → `To Do` → `In Progress` → `Review` → `Done`

## Custom Fields

| 필드 | 유형 | 값 |
|---|---|---|
| Priority | Single select | High, Medium, Low |
| Story Points | Number | 1, 2, 3, 5, 8 |
| Sprint | Iteration | Sprint 1, Sprint 2, Sprint 3, Sprint 4 |
| Type | Single select | Feature, Bug, Docs, Chore |

## Labels

`type:feature`, `type:bug`, `type:docs`, `type:chore`, `priority:high`, `priority:medium`, `priority:low`, `area:data`, `area:model`, `area:ui`, `area:deployment`, `area:metrics`, `status:blocked`, `status:needs-review`

## Milestones

### MVP Foundation

- Git/GitHub 개발 환경
- 포장 결함 라벨 기준
- 샘플 데이터
- 이미지 업로드
- 기준선 검사
- DORA Workflow

### Demo Release

- 결과 시각화
- 평가 지표
- 공개 배포
- 모바일 점검
- 발표 자료

## Issue 백로그

| 제목 | Type | Priority | Story Points | Milestone |
|---|---|---|---:|---|
| Git/GitHub 개발 환경 구성 | Chore | High | 2 | MVP Foundation |
| 프로젝트 README 작성 | Docs | Medium | 2 | MVP Foundation |
| 포장 결함 라벨 기준 정의 | Feature | High | 3 | MVP Foundation |
| 샘플 데이터 수집 및 메타데이터 작성 | Feature | High | 5 | MVP Foundation |
| 이미지 업로드와 파일 검증 구현 | Feature | High | 3 | MVP Foundation |
| 제품 ROI 전처리 구현 | Feature | High | 5 | MVP Foundation |
| SSIM 기준선 검사 구현 | Feature | High | 5 | MVP Foundation |
| 결함 의심 영역 시각화 구현 | Feature | Medium | 3 | Demo Release |
| Gradio 결과 화면 구현 | Feature | High | 3 | Demo Release |
| DORA Lead Time Workflow 구현 | Feature | Medium | 5 | MVP Foundation |
| 주간 DORA JSON 리포트 생성 | Feature | Medium | 5 | Demo Release |
| Render 배포 및 모바일 점검 | Chore | High | 3 | Demo Release |

## 선택 과제 분석 입력

Project의 상태 변경 이력을 다음 파일에 내보내면 로컬 분석 스크립트가 세 가지 지표를 계산합니다.

```text
metrics/project_events.csv
metrics/sprint_items.csv
```

예시 파일을 복사한 뒤 실제 이벤트와 Story Points로 바꿉니다.

```powershell
Copy-Item metrics/project_events.example.csv metrics/project_events.csv
Copy-Item metrics/sprint_items.example.csv metrics/sprint_items.csv
python scripts/analyze_project_metrics.py
```

자동 수집을 사용하려면 저장소 Settings → Secrets and variables → Actions에
`PROJECTS_TOKEN`을 추가한다. 토큰은 Project 읽기 권한과 저장소 Contents
쓰기 권한을 가져야 한다. `Collect GitHub Project metrics` Workflow를
수동 실행하거나 매주 월요일 스케줄 실행하면 현재 Project 상태가
`project_events.csv`와 `sprint_items.csv`에 누적되고, 계산 결과가 Artifact와
커밋으로 저장된다. Workflow 도입 이후의 스냅샷만 실측 이력으로 인정한다.
기본 대상은 `PROJECT_OWNER=kdongyu01`, `PROJECT_NUMBER=4`이며, 필요하면
Workflow 환경변수로 다른 Project로 바꿔 실행할 수 있다.

기존 Project 필드 보정:

```powershell
python scripts/configure_existing_project.py --dry-run
python scripts/configure_existing_project.py
Remove-Item Env:GH_TOKEN
```

생성 결과:

- `metrics/cycle-time.csv`: In Progress부터 Done까지의 시간
- `metrics/velocity.csv`: Sprint별 완료 Story Points
- `metrics/burndown.csv`: 날짜별 남은 Story Points
- `metrics/project-metrics.json`: 세 지표 통합 결과
