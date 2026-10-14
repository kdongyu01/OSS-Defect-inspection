# 선택 과제 검증 결과

기준일: 2026-10-15

선택 과제는 “파일·코드가 작성된 상태”와 “실제 공개 또는 실제 프로젝트
데이터로 검증된 상태”를 구분한다. 표본이 없는 결과를 성과로 해석하지 않는다.

| 선택 과제 | 현재 상태 | 근거 |
|---|---|---|
| GitHub Profile README | 공개용 파일 완료, Profile 저장소 생성 대기 | `profile/README.md` |
| DORA JSON·주간 보고서 | 구현 및 수정 Workflow 재실행 성공 | `metrics/dora.json`, `metrics/weekly-report.md`, Actions Artifact |
| Cycle Time·Velocity·Burndown | 수집·계산 자동화 완료, 실제 이력 축적 대기 | `scripts/export_project_metrics.py`, `scripts/analyze_project_metrics.py`, Project metrics Workflow |

## 1. GitHub Profile README

공개용 내용은 [profile/README.md](../profile/README.md)에 작성되어 있다.
GitHub 사용자명과 동일한 공개 저장소가 현재 존재하지 않아, 계정 외부 공개
단계만 남아 있다.

## 2. DORA JSON 및 주간 보고서

Workflow는 최근 7일의 Pull Request, production 배포, `incident` Issue를
GitHub REST API로 수집한다.

- JSON: `metrics/dora.json`
- 보고서: `metrics/weekly-report.md`
- Workflow: `.github/workflows/dora-weekly-report.yml`
- 대시보드: `docs/dora-dashboard.html`

첫 실행에서 수집과 Artifact 업로드가 성공했다. 현재 저장된 결과는
Pull Request·production 배포·incident 표본이 없어 다음과 같이 표시된다.

- Lead Time: `null`
- Deployment Frequency: `0`
- MTTR: `null`
- Change Failure Rate: `null`

이는 실패나 0점이 아니라 측정 표본이 없는 상태다.

## 3. Cycle Time·Velocity·Burndown

예시 입력으로 실제 함수를 실행한 결과는 다음과 같다.

```text
Cycle Time: Issue #1 = 6.0 hours
Velocity: Sprint 1 = 2 story points
Burndown: total 5, done 2, remaining 3
```

재현 명령:

```powershell
python scripts/analyze_project_metrics.py
```

`scripts/export_project_metrics.py`가 Project v2의 현재 이슈·Status·Sprint·
Story Points를 주기적으로 스냅샷하고, `scripts/analyze_project_metrics.py`가
세 지표를 계산한다. 실제 수집을 활성화하려면 저장소 Secret
`PROJECTS_TOKEN`에 Project 읽기 권한과 저장소 Contents 쓰기 권한이 있는
토큰을 등록한 뒤 `Collect GitHub Project metrics` Workflow를 수동 실행한다.
첫 실행 전의 과거 상태 변경 이력은 GitHub API가 소급해 주지 않으므로, 실행
이후 축적되는 데이터만 실측 결과로 사용한다. 저장소에 포함된
`metrics/project-metrics.example-output.json`은 여전히 예시 결과다.

## 1~3주차 최종 확인 항목

- [x] Profile README 콘텐츠 작성
- [x] Profile README 공개용 파일 완성
- [x] DORA JSON·Markdown 생성 및 Artifact 업로드
- [x] Chart.js 대시보드 구현
- [x] 분석 스크립트와 예시 실행 결과 작성
- [ ] Profile 전용 저장소에 README 공개
- [x] 수정된 DORA Workflow 재실행 성공 확인
- [x] 실제 Project 이벤트 수집·계산 Workflow 구현
- [ ] 실제 Project 이벤트가 축적된 뒤 실측 결과 확인
- [ ] Project 화면에서 5개 상태와 Custom Field 최종 확인

## Project 최종 설정 자동화

기존 Project #2를 중복 생성하지 않고 Priority, Story Points, Type 필드를
보정하는 스크립트를 추가했다.

```powershell
python scripts/configure_existing_project.py --dry-run
python scripts/configure_existing_project.py
Remove-Item Env:GH_TOKEN
```

GitHub 기본 Status 필드의 옵션명과 순서는 Project 화면에서 확인한다.
