# 배포 가이드 (GitHub → Zenodo DOI → PyPI)

이 문서는 `pifira` 패키지를 공개 배포하는 실제 절차입니다.
코드·설정은 모두 준비돼 있으니, 아래 계정 작업만 순서대로 하면 됩니다.

배포 전 확인:
- 실측 데이터(CSV)·논문 원문(PDF)은 패키지에 **포함돼 있지 않음** (확인 완료)
- `.gitignore`가 `*.csv`, `*.pdf`를 무시하므로 실수로도 커밋 안 됨
- `pyproject.toml`·`README.md`의 `USERNAME`을 실제 GitHub 아이디로 교체 필요

---

## 0. 사전 준비 (한 번만)

- GitHub 계정
- PyPI 계정 (https://pypi.org/account/register/)
- Zenodo 계정 (https://zenodo.org — GitHub으로 로그인 가능)

---

## 1. GitHub 저장소 생성 및 push

```bash
# 저장소 폴더에서
cd pifira

# USERNAME을 실제 아이디로 바꾼 뒤:
#   pyproject.toml 의 project.urls
#   README.md 의 링크
#   CITATION.cff 의 repository-code
# (에디터로 일괄 치환 권장)

git init
git add .
git commit -m "Initial release: pifira 0.1.0"
git branch -M main
git remote add origin https://github.com/USERNAME/pifira.git
git push -u origin main
```

push 후 GitHub Actions의 `tests` 워크플로가 자동 실행되어 4개 파이썬
버전에서 테스트가 도는지 확인하세요 (Actions 탭).

---

## 2. Zenodo DOI 연동 (GitHub Release 시 자동 발급)

1. https://zenodo.org 에 GitHub 계정으로 로그인
2. 우측 상단 → **GitHub** 메뉴
3. 저장소 목록에서 `pifira`의 스위치를 **ON**
4. GitHub에서 **Release**를 만들면 Zenodo가 자동으로 아카이빙 + DOI 발급

Release 만들기 (GitHub 웹 또는 CLI):
```bash
git tag v0.1.0
git push origin v0.1.0
```
그 뒤 GitHub 저장소 → **Releases** → **Draft a new release** →
태그 `v0.1.0` 선택 → **Publish release**.

- 발급된 DOI는 Zenodo 배지로 README에 추가할 수 있습니다.
- `.zenodo.json`의 메타데이터(제목·저자·ORCID·키워드)가 자동 반영됩니다.
- 이후 버전마다 새 DOI + 항상 최신을 가리키는 "concept DOI"가 생깁니다.

---

## 3. PyPI 배포

### 방법 A — Trusted Publishing (권장, 토큰 불필요)

1. https://pypi.org → 로그인 → **Your projects** → **Publishing**
2. **Add a new pending publisher** 등록:
   - PyPI Project Name: `pifira`
   - Owner: `USERNAME` (GitHub)
   - Repository name: `pifira`
   - Workflow name: `publish.yml`
3. 이후 GitHub에서 **Release를 Publish하면** `publish.yml`이 자동으로
   빌드·업로드합니다 (`.github/workflows/publish.yml`이 이미 OIDC 설정됨).

### 방법 B — API 토큰 수동 업로드

```bash
pip install build twine
python -m build
python -m twine upload dist/*
# 사용자명: __token__
# 비밀번호: pypi-... (PyPI에서 발급한 API 토큰)
```

배포 후 확인:
```bash
pip install pifira
python -c "import pifira; print(pifira.__version__)"
```

---

## 4. 배포 후 마무리

- README 상단에 배지 추가 (선택):
  ```markdown
  [![PyPI](https://img.shields.io/pypi/v/pifira)](https://pypi.org/project/pifira/)
  [![DOI](https://zenodo.org/badge/DOI/<your-doi>.svg)](https://doi.org/<your-doi>)
  [![tests](https://github.com/USERNAME/pifira/actions/workflows/tests.yml/badge.svg)](https://github.com/USERNAME/pifira/actions)
  ```
- 논문에서 인용 시: Zenodo DOI(소프트웨어) + 논문(방법론)을 함께 인용.

---

## 버전 올릴 때 (다음 릴리스)

1. `pyproject.toml`, `src/pifira/__init__.py`, `CITATION.cff`의 버전 갱신
2. commit → push
3. 새 태그 + GitHub Release → Zenodo 새 DOI + PyPI 자동 배포

---

## 이름 관련 참고

PyPI에서 `pifira`가 이미 사용 중이면 등록이 거부됩니다. 업로드 직전
https://pypi.org/project/pifira/ 를 확인하세요. 충돌 시 대안:
`pifira-lpg`, `pyfira`, `firecvp` 등 (pyproject.toml의 name과
`src/pifira/` 폴더명을 함께 바꿔야 함).
