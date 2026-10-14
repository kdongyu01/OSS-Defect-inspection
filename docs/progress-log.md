# OSS-Defect inspection 진행 기록

작성일: 2026-10-15

이 문서는 현재 대화에서 사용자가 요청한 작업과 실제 저장소 진행 상황을 정리한 기록이다. 개인 토큰, SSH 개인키, 비밀번호 등 인증 비밀값은 기록하지 않는다.

## 1. 사용자 요청 흐름

### 요청 1: 강의 자료 학습

사용자는 첨부된 강의 자료 PDF를 세부적으로 학습하고, 내용을 요약한 뒤 문제를 제시하기 전에 학습 여부를 확인하고 싶다고 요청했다.

확인한 강의 자료:

- Week 0: Orientation
- Week 1: Metrics That Matter
- Week 2: Plan, Track, and Visualize
- Week 3: Teamwork and Collaborative Development
- Week 4: Asynchronous Work
- Week 5: Open and Inner Source Software Delivery

학습한 핵심 내용:

- GitHub 기반 협업, Pull Request, 코드 리뷰, CI/CD
- DORA 4대 지표와 Flow Metrics
- Agile, GitHub Projects, User Story, INVEST
- GitHub Flow, Conventional Commits, Protected Branch
- 비동기 협업, ADR, RFC, 공개 문서화
- Open Source와 Inner Source, 라이선스, 기여 절차

### 요청 2: 공모전용 PRD 작성

사용자는 부산 지역문제를 해결하는 공모전 MVP의 PRD를 요청했다.

입력 조건:

- 선택 주제: 수산가공품 포장 불량 검사
- 서비스명: OSS-Defect inspection
- 개발 기간: 1개월
- 개발 인원: 1명
- 역량: 코딩 초보, LLM 활용
- 시범 지역: 부산광역시 서구 원양로 1
- 운영비: 월 0원 목표
- 결과물: 웹 접속 가능한 시제품

PRD 결정:

- 한 제품, 한 촬영 구도, 사진 1장 검사로 범위 제한
- Python + Gradio + OpenCV + SSIM 기준선 검사 선택
- Render Free Web Service 배포 계획
- 로그인·DB·실시간 카메라·GPU·유료 AI API 제외
- 실제 데이터·공개 데이터·협력 데이터·합성 데이터 구분
- 오탐·미탐·재현율·처리시간을 별도로 평가

작성 파일:

- `OSS-Defect-inspection_PRD.md`

### 요청 3: 1~3단계 실행 계획

사용자는 다음 세 단계와 선택 과제를 순서대로 해결하는 계획을 요청했다.

1. Git/GitHub 환경, SSH, 테스트 저장소, 프로젝트 제안서, Profile README
2. GitHub Actions 기반 DORA 4대 지표와 JSON 리포트·대시보드
3. GitHub Project, 칸반 상태, Issue, 템플릿, 라벨, 마일스톤, Cycle Time·Velocity·Burndown

계획 기준:

- 계정 생성·SSH 키 등록 등 사용자의 인증이 필요한 작업은 사용자가 직접 수행
- 나머지 파일·스크립트·문서·로컬 Git 작업은 프로젝트 폴더에서 자동 진행

### 요청 4: 프로젝트 폴더 이동

사용자가 PRD 파일을 `OSS-Defect inspection` 폴더로 이동했고, 이후 모든 작업을 해당 폴더 내부에서 진행하도록 요청했다.

이후 작업 기준 폴더:

```text
C:\Users\kdong\Desktop\(4-2)\OSS기반SW프로그래밍\OSS-Defect inspection
```

### 요청 5: GitHub 원격 저장소 연결

사용자가 GitHub 저장소 주소를 제공했다.

```text
https://github.com/kdongyu01/OSS-Defect-inspection
```

SSH 원격 연결과 첫 Push를 수행했다. 원격 저장소의 초기 README·LICENSE와 로컬 프로젝트 이력을 병합한 뒤 Push했다.

### 요청 6: 인증 없이 가능한 작업 계속 진행

사용자는 직접 해결해야 하는 인증 작업을 제외하고 질문 없이 계속 진행하도록 요청했다.

이에 따라 다음을 로컬에서 추가했다.

- DORA 주간 리포트 Workflow
- DORA JSON·Markdown 생성 스크립트
- Chart.js 대시보드
- GitHub Project 자동 설정 스크립트
- Cycle Time·Velocity·Burndown 분석 스크립트
- Project 구성 문서와 CSV 입력 템플릿

### 요청 7: GitHub Project 권한 오류 해결

초기 토큰은 `repo` 권한만 있어 Project v2 생성에 실패했다. 이후 사용자가 Project 권한을 가진 토큰으로 다시 실행하여 Project 생성에 성공했다.

### 요청 8: 현재 진행 결과 작성

사용자는 지금까지의 프롬프트와 진행 상황을 하나의 기록으로 작성해 달라고 요청했다. 이 문서가 해당 요청의 결과다.

## 2. 현재 저장소 구성

```text
OSS-Defect inspection/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ bug.md
│  │  └─ feature.md
│  ├─ pull_request_template.md
│  └─ workflows/
│     └─ dora-weekly-report.yml
├─ docs/
│  ├─ dora-dashboard.html
│  ├─ github-bootstrap.md
│  ├─ github-project-setup.md
│  └─ progress-log.md
├─ metrics/
│  ├─ project_events.example.csv
│  └─ sprint_items.example.csv
├─ scripts/
│  ├─ analyze_project_metrics.py
│  ├─ bootstrap_github_project.py
│  └─ generate_dora_report.py
├─ .gitignore
├─ OSS-Defect-inspection_PRD.md
├─ README.md
└─ github-profile-readme-draft.md
```

## 3. 완료된 작업

### Git/GitHub

- Git 2.49.0 설치 확인
- Git 사용자 이름·이메일 설정 확인
- `id_ed25519.pub` 공개키 존재 확인
- 첨부 프로젝트 폴더에서 `main` 브랜치 초기화
- SSH 원격 접근 확인
- GitHub 원격 저장소 연결
- 첫 커밋 및 Push 완료
- 현재 로컬·원격 브랜치 동기화

### 프로젝트 문서

- PRD 작성 및 GitHub 업로드
- 프로젝트 README 작성
- 16주 마일스톤 작성
- GitHub Profile README 초안 작성
- PR 템플릿 작성
- Feature/Bug Issue 템플릿 작성

### DORA 자동화

- Lead Time, Deployment Frequency, MTTR, Change Failure Rate 기준 정의
- 주간 실행 GitHub Actions 작성
- `dora.json` Artifact 생성 구조 작성
- 주간 Markdown 리포트 생성 구조 작성
- Chart.js 대시보드 시안 작성
- Python 스크립트 문법 검사 완료

### GitHub Project

- 라벨 생성 완료
- 마일스톤 2개 생성 완료
- Issue 12개 생성 완료
- Project v2 생성 완료
- Issue 12개를 Project에 연결 완료
- Project URL: [OSS-Defect inspection Sprint Board](https://github.com/users/kdongyu01/projects/2)

### 선택 과제

- Profile README 초안 작성
- DORA JSON·주간 리포트 자동 생성 구조 작성
- Cycle Time·Velocity·Burndown 분석 스크립트 작성
- 예시 CSV를 이용한 분석 실행 검증 완료

## 4. 실제 생성된 Issue

1. Git/GitHub 개발 환경 구성
2. 프로젝트 README 작성
3. 포장 결함 라벨 기준 정의
4. 샘플 데이터 수집 및 메타데이터 작성
5. 이미지 업로드와 파일 검증 구현
6. 제품 ROI 전처리 구현
7. SSIM 기준선 검사 구현
8. 결함 의심 영역 시각화 구현
9. Gradio 결과 화면 구현
10. DORA Lead Time Workflow 구현
11. 주간 DORA JSON 리포트 생성
12. Render 배포 및 모바일 점검

## 5. 주요 커밋

| 커밋 | 내용 |
|---|---|
| `7285838` | 프로젝트 기본 문서와 템플릿 초기화 |
| `0415721` | DORA 리포트·대시보드·Project 구성안 추가 |
| `a78931a` | 첫 GitHub Push 완료 상태 기록 |
| `21af219` | GitHub Project 자동 설정 스크립트 추가 |
| `693abb5` | Cycle Time·Velocity·Burndown 분석 추가 |
| `fa104dc` | Project 권한 오류 안내 개선 |
| `5d2a531` | Project scope 부족 오류 안내 개선 |
| `aaed8eb` | 실제 Project URL과 완료 상태 문서화 |
| `현재` | 진행 기록 추가 |

## 6. 현재 남은 작업

자동화와 문서 작업은 완료되었고, 다음 항목은 실제 데이터 또는 GitHub 화면 확인이 필요하다.

- Project 보드 상태를 `Backlog / To Do / In Progress / Review / Done`으로 최종 설정
- `Priority / Story Points / Sprint / Type` Custom Field 설정
- 실제 Project 이벤트를 CSV로 추출해 Cycle Time·Velocity·Burndown 계산
- GitHub Actions를 수동 실행해 DORA JSON Artifact 생성 확인
- 실제 이미지 데이터 확보 및 모델 구현
- Gradio 앱 작성 및 Render 배포
- Profile README 초안을 사용자명과 실제 학습 내용에 맞게 조정

## 7. 인증 보안 기록

대화 과정에서 GitHub 토큰이 여러 차례 노출되었다. 노출된 토큰은 재사용하지 말고 모두 폐기해야 한다. 토큰, 비밀번호, SSH 개인키는 저장소·README·진행 기록에 기록하지 않는다.

## 8. 최신 요청 및 최종 확인

기준 시각: 2026-10-15 07:31 (KST)

사용자는 현재까지의 프롬프트와 진행 상황을 빠짐없이 하나의 문서로 정리해 달라고 다시 요청했다. 같은 요청이 연속으로 전달되었으며, 이 문서는 두 요청을 모두 반영한 최종 진행 기록이다.

최신 확인 결과:

- 작업 폴더: `OSS-Defect inspection`
- Git 브랜치: `main`
- 원격 저장소: `https://github.com/kdongyu01/OSS-Defect-inspection`
- Project v2: [OSS-Defect inspection Sprint Board](https://github.com/users/kdongyu01/projects/2)
- Project에 연결된 Issue: 12개
- 라벨과 마일스톤: 생성 완료
- 최신 로컬 상태 확인 시 `docs/progress-log.md`만 아직 커밋 전이었으며, 이 문서 작성 후 커밋할 예정이다.

## 9. 프롬프트별 결과 요약

| 순서 | 사용자 요청 | 결과 |
|---:|---|---|
| 1 | 강의 PDF를 세부 학습하고 요약 | Week 0~5의 GitHub 협업, DORA, Agile, 비동기 협업, OSS/Inner Source 학습 및 요약 |
| 2 | 부산 수산가공품 포장 불량 검사 PRD 작성 | 1인·1개월 MVP 기준 PRD 작성 및 저장 |
| 3 | 1~3단계와 선택 과제의 해결 계획 수립 | Git/GitHub, DORA 자동화, Project 운영 계획 수립 |
| 4 | 첨부 폴더 내부에서 계속 진행 | 작업 기준 폴더를 `OSS-Defect inspection`으로 변경 |
| 5 | GitHub 저장소 URL 제공 | SSH 원격 연결, 병합, 첫 Push 완료 |
| 6 | 사용자 인증 외 작업을 질문 없이 진행 | 자동화 스크립트, 대시보드, 분석 코드, 템플릿 추가 |
| 7 | 토큰으로 bootstrap 스크립트 실행 | Issue·라벨·마일스톤 생성 성공, Project 권한 오류 확인 |
| 8 | Project 권한 오류 수정 후 재실행 | Project v2 생성 및 12개 Issue 연결 성공 |
| 9 | 현재까지의 프롬프트·진행 상황 기록 | 본 `docs/progress-log.md`에 전체 기록 작성 및 최신 상태 반영 |

## 10. 주의할 점

- `docs/progress-log.md`는 작업 기록이며, 앞으로의 기능 구현 완료를 의미하지 않는다.
- DORA 결과는 실제 GitHub 이벤트가 수집된 뒤에만 성과로 제시한다.
- Cycle Time·Velocity·Burndown 결과는 실제 Project 상태 변경 이력이 필요하다.
- Profile README 초안은 사용자 GitHub 프로필 저장소에 별도로 Push해야 공개된다.
- GitHub Project의 상태 컬럼과 Custom Field는 GitHub 화면에서 최종 확인해야 한다.
- 토큰이 노출된 경우 즉시 Revoke하고 새 토큰을 발급해야 한다.

## 11. 2026-10-15 후속 실행

계획을 이어서 실행하는 과정에서 DORA 수집 스크립트를 점검했다. 기존
인증 헤더가 API 토큰을 실제로 전달하지 않는 상태였으므로, 다음을 수정했다.

- `GH_TOKEN`과 `GITHUB_REPOSITORY`가 없을 때 명시적인 오류를 출력
- GitHub REST API 요청에 환경변수 토큰을 Bearer 인증으로 전달
- DORA Workflow 수동 실행 방법과 데이터가 없는 경우의 `0`·`null` 의미를 문서화

검증 결과:

- Python 파일 문법 오류 없음
- Git diff 공백 오류 없음
- GitHub Actions Workflow가 `active` 상태로 등록됨
- 현재 Workflow 실행 이력은 0건
- 실제 Artifact 검증을 위해 GitHub Actions 화면에서 수동 실행 필요

추가 커밋:

| 커밋 | 내용 |
|---|---|
| `e5bd911` | DORA API 인증과 수동 실행 안내 보완 |

## 12. 2026-10-15 Actions 실패 분석 및 수정

사용자가 공유한 GitHub Actions 화면에서 최신 재실행이 실패했지만, Job 단계
확인 결과 `Generate DORA report`와 `Upload DORA artifacts`는 성공하고
`Commit report files`만 실패했다. 첫 번째 시도가 이미 리포트 커밋을 원격
`main`에 생성한 뒤, 재실행이 이전 커밋 기준으로 다시 Push하여
non-fast-forward 충돌이 발생한 것이 원인이었다.

수정 내용:

- 변경사항이 없으면 커밋·Push를 정상 종료
- 변경사항이 있으면 리포트 커밋 생성
- `origin/main`을 fetch한 뒤 rebase
- `git push origin HEAD:main`으로 최신 원격 브랜치에 Push
- 동시 실행을 막는 Workflow concurrency 그룹 추가

검증 결과:

- 수정 Workflow를 원격 `main`에 Push 완료
- 원격에 `metrics/dora.json`과 `metrics/weekly-report.md`가 실제 생성됨
- 로컬 브랜치와 원격 브랜치가 동기화됨
- 수정 후 새 실행 이력은 아직 없으며, 다음 `Run workflow`에서 재검증 가능

추가 커밋:

| 커밋 | 내용 |
|---|---|
| `1c505af` | DORA 리포트 재실행 시 원격 충돌 방지 |

## 13. 주차별 완료 현황 재점검

2026-10-15 07:46 기준으로 1~3주차를 다시 점검했다.

| 주차 | 진행 상태 | 근거 |
|---|---|---|
| 1주차 | 핵심 과제 완료 | Git 초기화, SSH Push, 프로젝트 제안서, 16주 마일스톤, Profile README 초안 |
| 2주차 | 구현 완료, 수정 Workflow 재실행 대기 | DORA Workflow active, 첫 실행의 수집·Artifact 성공, Chart.js 대시보드 구현 |
| 3주차 | 핵심 구성 완료, 화면 Custom Field 최종 확인 대기 | Project v2, Issue 12개, 템플릿, 라벨, 마일스톤 생성 |

이번 점검에서 다음을 추가했다.

- 대시보드가 `null` 지표를 실제 값 `0`으로 오해하지 않고 `측정 데이터 없음`으로 표시
- README에 주차별 진행 현황, 선택 과제, 남은 확인 작업 추가
- 두 Python 분석 스크립트 문법 재검증
- Git diff 공백 오류 없음 확인

이번 변경 커밋:

| 커밋 | 내용 |
|---|---|
| 최신 | 주차별 현황과 DORA 대시보드 표시 개선 |

## 14. 선택 과제 3개 검토 및 보완

2026-10-15 07:49 기준 선택 과제를 다시 확인했다.

### 선택 과제 1: GitHub Profile README

- 학습 목표와 관심 분야를 `github-profile-readme-draft.md`에 작성 완료
- 사용자명과 같은 Profile 전용 저장소는 아직 생성되지 않아 공개 완료로
  표시하지 않음
- 공개 절차와 현재 상태를 `docs/optional-assignments.md`에 기록

### 선택 과제 2: DORA JSON·주간 보고서

- `metrics/dora.json`과 `metrics/weekly-report.md`가 실제 첫 Workflow
  실행으로 생성됨
- Artifact 업로드 성공 확인
- 현재 Pull Request·production 배포·incident 표본이 없어 `null` 또는 `0`
  인 상태이며, 이를 성과로 해석하지 않음
- Workflow 재실행 충돌 수정본은 원격에 Push했지만 수정 후 새 실행은 아직 없음

### 선택 과제 3: Cycle Time·Velocity·Burndown

- 분석 함수가 예시 CSV 입력으로 실제 실행됨
- 결과: Cycle Time 6.0시간, Sprint 1 Velocity 2점, Burndown 잔여 3점
- 결과를 `metrics/project-metrics.example-output.json`에 저장
- 예시 결과임을 명시했으며, 실제 Project 상태 변경 이력으로 계산한 결과는
  아직 아님

선택 과제의 구현·검증 상태와 남은 항목은
`docs/optional-assignments.md`에 정리했다.
