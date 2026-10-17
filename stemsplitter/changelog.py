"""CHANGELOG.md: what each version adds or changes for the people who use the app (standard library only).

Every user-visible change adds a line under `## Unreleased` in the same PR. `tools/release.py` refuses to
release while that section is empty and turns it into the new version's `## X.Y.Z (date)` section. CI
publishes that section as the version's release notes, which is what the app's update dialog shows, and
fails the release if the version has no section.
"""

from __future__ import annotations

import re
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
UNRELEASED = "Unreleased"
_HEADING = re.compile(r"^## +(\S+)[^\n]*$", re.M)  # "## 1.2.3 (2026-10-17)" -> "1.2.3"; "###" doesn't match


def sections(text: str) -> dict[str, str]:
    """{"Unreleased" or "X.Y.Z": the section's text without its heading}, in file order."""
    found = list(_HEADING.finditer(text))
    out = {}
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(text)
        out[m.group(1)] = text[m.end():end].strip()
    return out


def notes_for(text: str, version: str) -> str:
    """The notes of `version` (a leading "v" is ignored); ValueError when it has no section or an empty one."""
    version = version.lstrip("vV")
    body = sections(text).get(version, "")
    if not body:
        raise ValueError(f"CHANGELOG.md has no notes for {version}: add a '## {version}' section that says "
                         "exactly what this version adds or changes")
    return body


def release_unreleased(text: str, version: str, date: str) -> str:
    """Move the Unreleased notes under a new `## version (date)` heading, leaving an empty Unreleased on top.

    ValueError when there is no Unreleased section, when it is empty or when `version` already has a section.
    """
    found = sections(text)
    if UNRELEASED not in found:
        raise ValueError(f"CHANGELOG.md has no '## {UNRELEASED}' section")
    if not found[UNRELEASED]:
        raise ValueError(f"nothing under '## {UNRELEASED}' in CHANGELOG.md: write exactly what this version adds "
                         "or changes first")
    if version in found:
        raise ValueError(f"CHANGELOG.md already has a section for {version}")
    m = re.search(rf"^## +{UNRELEASED}[^\n]*$", text, re.M)
    return f"{text[:m.end()]}\n\n## {version} ({date}){text[m.end():]}"
