# GitHub Project 구성안

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

생성 결과:

- `metrics/cycle-time.csv`: In Progress부터 Done까지의 시간
- `metrics/velocity.csv`: Sprint별 완료 Story Points
- `metrics/burndown.csv`: 날짜별 남은 Story Points
- `metrics/project-metrics.json`: 세 지표 통합 결과
