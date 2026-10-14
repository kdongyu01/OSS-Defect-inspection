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
