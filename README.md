# OSS-Defect inspection

부산 수산가공품 포장 사진의 가시적 결함을 1차 선별하는 공모전 MVP입니다.

## 문제 정의

수산가공품 포장 검사는 반복적인 육안 확인에 의존할 수 있으며, 검사자별 판단 차이와 작은 포장 이상 누락이 발생할 수 있습니다. 이 프로젝트는 고정된 촬영 조건에서 정상 기준 이미지와 업로드 이미지를 비교해 사람이 재확인할 대상을 선별합니다.

> 이 서비스는 식품 안전 판정이나 출하 승인을 대신하지 않는 품질검사 보조 시제품입니다.

## 핵심 기능

1. JPG/PNG 포장 이미지 업로드 및 촬영 조건 검증
2. OpenCV·SSIM 기반 정상 기준 이미지 비교
3. 결함 점수, 의심 영역, 판정 근거 표시

## 기술 스택

- Python, Gradio
- OpenCV, NumPy, Pillow, scikit-image
- GitHub Actions
- Render Free Web Service

## 개발 마일스톤

| 기간 | 목표 |
|---|---|
| 1~4주 | GitHub 환경, 데이터 기준, 기준선 검사, Gradio 시제품, DORA 자동화 |
| 5~8주 | GitHub Project 운영, 협업 문서, 공개 데이터 검토, 화면 개선 |
| 9~12주 | 제품별 전처리, 검증 데이터 확대, 평가 대시보드 |
| 13~16주 | 현장 검토, 배포 안정화, 발표 자료와 회고 |

## 문서

- [제품 요구사항 문서](OSS-Defect-inspection_PRD.md)
- [GitHub Profile README 초안](github-profile-readme-draft.md)
- [GitHub Project 보드](https://github.com/users/kdongyu01/projects/2)
- [GitHub Project 구성안](docs/github-project-setup.md)

## 현재 상태

- [x] 로컬 Git 저장소 초기화
- [x] 프로젝트 제안서 작성
- [x] 협업용 템플릿 초안 추가
- [x] GitHub 원격 저장소 연결 및 첫 Push
- [x] DORA Actions 작성
- [x] GitHub Project 생성 및 Issue 12개 연결
- [ ] Project 보드 상태·Custom Field 최종 설정

## 선택 과제 검증

선택 과제의 구현·검증 수준은 [선택 과제 검증 결과](docs/optional-assignments.md)에
정리했습니다. 예시 데이터 결과는 실제 성과로 해석하지 않으며, 실제 Project
이력이 입력된 뒤 다시 계산합니다.

## 주차별 진행 현황

| 주차 | 핵심 과제 | 상태 | 확인 근거 |
|---|---|---|---|
| 1주차 | Git/GitHub, 제안서, Profile README | 완료 | SSH Push, PRD, 16주 마일스톤, Profile README 초안 |
| 2주차 | DORA 수집, 대시보드, JSON·주간 보고서 | 구현 완료·재실행 검증 대기 | Workflow 등록, 첫 실행의 수집·Artifact 성공 |
| 3주차 | Project, 칸반, Issue, 템플릿, 라벨, 마일스톤 | 핵심 구성 완료 | Project v2, Issue 12개, 템플릿, 라벨, 마일스톤 |

### 선택 과제

- DORA JSON Artifact 및 주간 Markdown 보고서: 구현 완료
- Cycle Time·Velocity·Burndown: 실제 Project 이벤트 CSV 입력 후 계산 가능한 스크립트 완료
- Chart.js 대시보드: `docs/dora-dashboard.html` 구현

### 남은 확인

- GitHub Project 화면에서 상태를 `Backlog / To Do / In Progress / Review / Done`으로 확인
- `Priority / Story Points / Sprint / Type` Custom Field 확인
- 수정된 DORA Workflow를 `Actions → Run workflow`로 한 번 재실행
- Profile README 초안을 사용자 프로필 저장소에 공개
