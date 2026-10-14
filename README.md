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

## 현재 상태

- [x] 로컬 Git 저장소 초기화
- [x] 프로젝트 제안서 작성
- [x] 협업용 템플릿 초안 추가
- [x] GitHub 원격 저장소 연결 및 첫 Push
- [x] DORA Actions 작성
- [ ] GitHub Project와 Issue 구성
