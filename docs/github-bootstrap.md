# GitHub 관리 항목 자동 생성

저장소의 라벨, 마일스톤, Issue 12개, Project v2를 한 번에 생성하는 스크립트입니다.

## 안전 원칙

- 토큰은 파일에 저장하지 않습니다.
- 토큰은 `GH_TOKEN` 또는 `GITHUB_TOKEN` 환경변수로만 전달합니다.
- 먼저 `--dry-run`으로 생성 목록을 확인할 수 있습니다.
- 이미 같은 이름의 라벨·마일스톤·Issue가 있으면 중복 생성하지 않습니다.

## 실행

PowerShell에서 GitHub Fine-grained token을 직접 입력하지 않고 환경변수로 설정한 뒤 실행합니다.

```powershell
$env:GH_TOKEN = "발급한 토큰"
python scripts/bootstrap_github_project.py --dry-run
python scripts/bootstrap_github_project.py
Remove-Item Env:GH_TOKEN
```

필요한 권한은 저장소 Issues·Metadata 쓰기와 Projects 쓰기입니다. 실제 토큰 권한과 GitHub 계정 정책은 실행 전에 GitHub 설정 화면에서 확인합니다.

## DORA Workflow 수동 실행

GitHub 저장소의 `Actions` 탭에서 `Generate DORA weekly report`를 선택한 뒤
`Run workflow`를 누르면 최근 7일 데이터를 수집합니다. Workflow는
`metrics/dora.json`과 `metrics/weekly-report.md`를 Artifact로 업로드하고,
저장소에도 결과 파일을 커밋합니다.

아직 Pull Request, production 배포, `incident` Issue가 없으면 해당 지표는
표본 수 0 또는 `null`로 표시됩니다. 이 값은 성과가 아니라 측정 데이터가
아직 없는 상태를 뜻합니다.
