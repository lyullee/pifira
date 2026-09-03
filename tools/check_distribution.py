"""Reject third-party validation material from built distribution archives."""

from __future__ import annotations

import argparse
import glob
import tarfile
import zipfile
from pathlib import Path, PurePosixPath


FORBIDDEN_SUFFIXES = {
    ".bmp",
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".jpeg",
    ".jpg",
    ".mts",
    ".npy",
    ".npz",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".tif",
    ".tiff",
    ".tsv",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".zip",
}

FORBIDDEN_PARTS = {
    "data",
    "literature_sources",
    "validation-data",
    "validation_data",
}


def archive_members(path: Path) -> list[str]:
    """Return normalized member names from a wheel, zip, or tar archive."""
    if path.suffix == ".whl" or path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            return archive.namelist()
    if path.name.endswith((".tar.gz", ".tar.bz2", ".tar.xz")):
        with tarfile.open(path, "r:*") as archive:
            return [member.name for member in archive.getmembers() if member.isfile()]
    raise ValueError(f"Unsupported distribution archive: {path}")


def forbidden_reason(member_name: str) -> str | None:
    """Return the policy violation for one archive member, if any."""
    normalized = member_name.replace("\\", "/")
    path = PurePosixPath(normalized)
    lower_parts = {part.lower() for part in path.parts}
    if lower_parts & FORBIDDEN_PARTS:
        return "forbidden validation-data directory"
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return f"forbidden file type {path.suffix.lower()}"
    return None


def check_archive(path: Path) -> list[tuple[str, str]]:
    """Return all policy violations in one distribution archive."""
    return [
        (member, reason)
        for member in archive_members(path)
        if (reason := forbidden_reason(member)) is not None
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="+")
    args = parser.parse_args()

    archives: list[Path] = []
    for pattern in args.archives:
        matches = [Path(match) for match in glob.glob(pattern)]
        archives.extend(matches or [Path(pattern)])

    failures: list[tuple[Path, str, str]] = []
    for archive in archives:
        if not archive.is_file():
            parser.error(f"archive not found: {archive}")
        for member, reason in check_archive(archive):
            failures.append((archive, member, reason))

    if failures:
        for archive, member, reason in failures:
            print(f"FAIL {archive}: {member} ({reason})")
        return 1

    for archive in archives:
        print(f"PASS {archive}: no third-party validation material detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
