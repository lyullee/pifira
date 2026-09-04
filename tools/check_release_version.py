"""Check that every release surface declares one identical version."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def _match(path: Path, pattern: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text, flags=re.MULTILINE)
    if match is None:
        raise RuntimeError(f"Version not found in {path.relative_to(ROOT)}")
    return match.group(1)


def declared_versions() -> dict[str, str]:
    """Return versions declared by package and archive metadata."""
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    return {
        "pyproject.toml": _match(
            ROOT / "pyproject.toml", r'^version\s*=\s*"([^"]+)"\s*$'
        ),
        "src/pifira/__init__.py": _match(
            ROOT / "src" / "pifira" / "__init__.py",
            r'^__version__\s*=\s*"([^"]+)"\s*$',
        ),
        "CITATION.cff": _match(
            ROOT / "CITATION.cff", r'^version:\s*"([^"]+)"\s*$'
        ),
        ".zenodo.json": str(zenodo["version"]).removeprefix("v"),
    }


def check_release_version(release_tag: str | None = None) -> str:
    """Return the common version or raise when metadata/tag values differ."""
    versions = declared_versions()
    unique = set(versions.values())
    if len(unique) != 1:
        detail = ", ".join(f"{name}={value}" for name, value in versions.items())
        raise RuntimeError(f"Release version mismatch: {detail}")
    version = unique.pop()
    if release_tag is not None and release_tag != f"v{version}":
        raise RuntimeError(
            f"Release tag {release_tag!r} does not match package version v{version}"
        )
    return version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "release_tag",
        nargs="?",
        help="Optional Git tag, for example v0.3.0",
    )
    arguments = parser.parse_args()
    version = check_release_version(arguments.release_tag)
    print(f"Release version check PASS: {version}")


if __name__ == "__main__":
    main()
