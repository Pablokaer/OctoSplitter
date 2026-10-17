"""CHANGELOG.md: parsing, the release step and the repository's own file (standard library only)."""

import unittest

from stemsplitter import __version__, changelog
from stemsplitter.release import DOWNLOAD, write_notes

SAMPLE = """# Changelog

Intro text, with **Unreleased** in it.

## Unreleased

- Added a thing.

## 1.0.1 (2026-01-02)

- Fixed a bug.

### Details

- A subheading stays inside its version.

## 1.0.0 (2026-01-01)

- First version.
"""


class Sections(unittest.TestCase):
    def test_sections_in_order(self):
        found = changelog.sections(SAMPLE)
        self.assertEqual(list(found), ["Unreleased", "1.0.1", "1.0.0"])
        self.assertEqual(found["Unreleased"], "- Added a thing.")
        self.assertIn("### Details", found["1.0.1"])
        self.assertEqual(found["1.0.0"], "- First version.")

    def test_notes_for(self):
        self.assertEqual(changelog.notes_for(SAMPLE, "v1.0.0"), "- First version.")
        with self.assertRaises(ValueError):
            changelog.notes_for(SAMPLE, "1.0.2")
        with self.assertRaises(ValueError):
            changelog.notes_for(SAMPLE.replace("- First version.", ""), "1.0.0")


class Release(unittest.TestCase):
    def test_unreleased_becomes_the_version(self):
        text = changelog.release_unreleased(SAMPLE, "1.1.0", "2026-02-03")
        found = changelog.sections(text)
        self.assertEqual(list(found), ["Unreleased", "1.1.0", "1.0.1", "1.0.0"])
        self.assertEqual(found["Unreleased"], "")
        self.assertEqual(found["1.1.0"], "- Added a thing.")
        self.assertIn("## 1.1.0 (2026-02-03)\n", text)
        self.assertEqual(found["1.0.1"], changelog.sections(SAMPLE)["1.0.1"])

    def test_refuses_without_notes(self):
        empty = SAMPLE.replace("- Added a thing.\n", "")
        with self.assertRaises(ValueError):
            changelog.release_unreleased(empty, "1.1.0", "2026-02-03")
        with self.assertRaises(ValueError):
            changelog.release_unreleased(SAMPLE.replace("## Unreleased", "## Next"), "1.1.0", "2026-02-03")
        with self.assertRaises(ValueError):
            changelog.release_unreleased(SAMPLE, "1.0.1", "2026-02-03")


class RepositoryChangelog(unittest.TestCase):
    """The real CHANGELOG.md: a version bump without notes fails here, before any release is built."""

    def test_current_version_has_notes(self):
        text = changelog.PATH.read_text(encoding="utf-8")
        self.assertTrue(changelog.notes_for(text, __version__))
        self.assertIn(changelog.UNRELEASED, changelog.sections(text))

    def test_release_notes_file(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "notes.md"
            self.assertEqual(write_notes(f"v{__version__}", out), 0)
            notes = out.read_text(encoding="utf-8")
        self.assertTrue(notes.startswith(DOWNLOAD))
        self.assertIn(changelog.notes_for(changelog.PATH.read_text(encoding="utf-8"), __version__), notes)


if __name__ == "__main__":
    unittest.main()
