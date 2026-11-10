# 마크다운(.md) 문서 및 작업 노트 작성/저장 규칙

이 프로젝트 및 작업 중 생성하는 모든 마크다운(.md) 문서와 작업 노트에 대해 아래 규칙을 항상 자동으로 적용한다:

## 1. 저장 경로
- 마크다운(.md) 파일은 현재 작업 디렉토리와 아래 지정된 절대 경로에 저장한다.
- **저장 위치**: `C:\Users\slee122\OneDrive - NASA\Documents\MDfiles\IDE_Notes\`
- (해당 폴더가 없으면 자동 생성 후 저장)

## 2. 파일명 규칙
- **형식**: `[PROJECT]_[YYYYMMDD]_[주제].md`
- **예시**: `CIMI_20261104_run_setup.md`, `MATE_20261104_analysis.md`

## 3. 상단 메타데이터(Frontmatter) 필수 포함
- 모든 .md 파일의 최상단에는 옵시디언 Dataview 연동을 위해 아래 YAML 속성을 반드시 작성한다:
```yaml
---
project: [CIMI / MATE / WACCM-X / OpenGGCM / Tsyganenko / General 중 선택]
type: [run_log / bugfix / setup / analysis / theory 중 선택]
date: YYYY-MM-DD
---
```

