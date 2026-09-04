# pifira 0.3.0 배포 가이드

이 문서는 이미 공개된 `lyullee/pifira`의 세 번째 릴리스를 만드는
절차다. 신규 저장소 생성 절차가 아니다.

현재 공개 상태:

- GitHub tag/source commit: `v0.2.0` / `5d184902fec2fb40ed45435eb2cbddbf16db70c7`
- PyPI: `pifira 0.2.0` (Trusted Publishing 확인됨)
- Zenodo version DOI: `10.5281/zenodo.22270499`
- Zenodo concept DOI: `10.5281/zenodo.22162092`
- 이번 후보 버전: `0.3.0`

원자료는 어디에도 올리지 않는다. GitHub, GitHub release 자동 소스
압축본, Zenodo, PyPI wheel/sdist에는 DOI와 공식 출처 목록만 들어간다.

## 1. 한 번만 확인할 계정 설정

### PyPI Trusted Publisher

PyPI의 `pifira` 프로젝트에서 **Manage > Publishing**으로 들어가 GitHub
publisher가 다음과 정확히 일치하는지 확인한다.

| 항목 | 값 |
|---|---|
| PyPI project | `pifira` |
| GitHub owner | `lyullee` |
| Repository | `pifira` |
| Workflow | `publish.yml` |
| Environment | `pypi` |

GitHub 저장소의 **Settings > Environments**에도 `pypi` 환경을 만든다.
가능하면 본인 승인을 required reviewer로 설정한다. 장기 API token은
필요하지 않다.

### Zenodo GitHub 연결

`v0.1.0`이 이미 Zenodo에 등록됐으므로 연결 이력은 있다. 그래도 Zenodo
프로필의 **GitHub** 화면에서 저장소 목록을 동기화하고 `pifira` 스위치가
켜져 있는지 확인한다. 이 상태에서 새 GitHub release를 공개하면 Zenodo가
새 버전을 수집한다.

## 2. 로컬 후보 검사

저장소 루트에서 PowerShell로 실행한다.

```powershell
python -m venv .venv-release
.\.venv-release\Scripts\python.exe -m pip install --upgrade pip
.\.venv-release\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv-release\Scripts\python.exe tools/check_release_version.py v0.3.0
.\.venv-release\Scripts\python.exe -m pytest -q
.\.venv-release\Scripts\python.exe -m build
.\.venv-release\Scripts\python.exe -m twine check dist/*
.\.venv-release\Scripts\python.exe tools/check_distribution.py dist/*
```

마지막 두 명령이 모두 PASS여야 한다. `dist`에는 다음 두 파일만 생기는
것이 정상이다.

```text
pifira-0.3.0-py3-none-any.whl
pifira-0.3.0.tar.gz
```

압축본 내부에 PDF, Word, PowerPoint, Excel, CSV, 그림 또는
`literature_sources`/`validation-data` 폴더가 있으면 배포하지 않는다.

## 3. 변경 검토와 GitHub 반영

```powershell
git status --short
git diff --check
git diff --stat
git diff
```

의도한 변경만 확인한 뒤 커밋하고 main에 올린다.

```powershell
git add .
git commit -m "Prepare pifira 0.3.0"
git push origin main
```

GitHub **Actions**에서 `tests`가 Python 3.10-3.13 및 distribution 검사까지
모두 통과하는지 확인한다. 실패 상태에서 release를 만들지 않는다.

## 4. GitHub release 공개

저장소의 **Releases > Draft a new release**에서 다음처럼 설정한다.

- 새 태그: `v0.3.0`
- Target: 검사에 통과한 `main` 커밋
- 제목: `pifira 0.3.0`
- 본문: `RELEASE_NOTES_v0.3.0.md` 내용
- Pre-release: 선택하지 않음
- Latest release: 선택

먼저 draft 상태로 내용과 태그 대상을 재확인한 뒤 **Publish release**를
누른다. release 공개가 PyPI workflow와 Zenodo 수집을 동시에 시작한다.

CLI로 할 경우에도 같은 태그와 노트를 사용한다.

```powershell
gh release create v0.3.0 --target main --title "pifira 0.3.0" --notes-file RELEASE_NOTES_v0.3.0.md
```

## 5. PyPI 확인

GitHub **Actions > publish**가 성공했는지 확인한다. 그 다음 깨끗한 임시
환경에서 실제 PyPI 파일을 설치한다.

```powershell
python -m venv .venv-pypi-check
.\.venv-pypi-check\Scripts\python.exe -m pip install --upgrade pip
.\.venv-pypi-check\Scripts\python.exe -m pip install --no-cache-dir pifira==0.3.0
.\.venv-pypi-check\Scripts\python.exe -c "import pifira; print(pifira.__version__)"
.\.venv-pypi-check\Scripts\python.exe -c "from pifira.lh2 import RigidRotorSpinThermo; print(RigidRotorSpinThermo().equilibrium_ortho(20.3))"
```

버전은 `0.3.0`이어야 한다. PyPI 파일은 같은 버전으로 덮어쓸 수 없으므로
업로드 후 코드 오류가 발견되면 `0.3.0`을 재사용하지 말고 `0.3.1`로
수정한다.

## 6. Zenodo DOI 확인

Zenodo의 GitHub 화면에서 `v0.3.0` 처리 완료를 기다린다. 새 record에서
다음을 확인한다.

- 제목과 설명이 `.zenodo.json`과 일치함
- version이 `v0.3.0`임
- creator와 ORCID가 맞음
- license가 MIT임
- 새 **version DOI**가 발급됨
- concept DOI가 계속 `10.5281/zenodo.22162092`임
- release archive에 검증 원자료가 없음

README의 DOI 배지는 concept DOI를 사용하므로 매 릴리스마다 바꿀 필요가
없다. 논문에서 특정 소프트웨어 판을 인용하려면 Zenodo가 새로 발급한
`v0.3.0` version DOI를 쓴다.

## 7. 최종 공개 확인

아래 세 페이지에서 버전과 링크가 서로 맞는지 확인한다.

- GitHub: <https://github.com/lyullee/pifira/releases/tag/v0.3.0>
- PyPI: <https://pypi.org/project/pifira/0.3.0/>
- Zenodo concept record: <https://doi.org/10.5281/zenodo.22162092>

새 Zenodo version DOI는 발급 후 release 메모와 논문 Data and code
availability 문장에 기록한다. concept DOI와 version DOI를 혼동하지 않는다.

## 8. 논문에 넣을 권장 문장

릴리스가 실제로 완료된 뒤 `<VERSION_DOI>`만 새 DOI로 바꾼다.

> Reusable software components are available as pifira v0.3.0 on GitHub and
> PyPI and are archived at Zenodo (version DOI: <VERSION_DOI>; concept DOI:
> 10.5281/zenodo.22162092). Third-party validation files, source publications,
> digitized traces and derived validation tables are not redistributed.
> Persistent identifiers and official acquisition locations are listed in
> VALIDATION_SOURCES.md. Study-specific analysis scripts and the complete audit
> record are available from the corresponding author on reasonable request.

이 문장은 공개 패키지가 실제 원고 전체 재현 코드를 모두 포함한다고
과장하지 않으면서, 공개한 재사용 모듈과 제3자 자료의 경계를 명확히 한다.

## 9. 실패 시 처리

- `tests` 실패: release를 만들지 않고 main에서 수정한다.
- `publish` 실패 전 PyPI 업로드 없음: 같은 `v0.3.0` release workflow를
  원인 수정 후 재실행할 수 있다.
- PyPI에 일부 파일이라도 `0.3.0`이 등록됨: 버전을 `0.3.1`로 올린다.
- Zenodo 수집 실패: release나 태그를 성급히 삭제하지 말고 Zenodo
  GitHub 화면의 오류를 확인한다. 메타데이터를 수정한 뒤 새 patch release를
  만드는 것이 가장 추적하기 쉽다.
- 원자료가 실수로 커밋됨: release를 중단하고 git history와 이미 생성된
  archive의 노출 여부를 별도로 처리한다. 단순 `.gitignore` 추가만으로는
  이미 커밋된 파일이 제거되지 않는다.
