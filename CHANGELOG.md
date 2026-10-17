# Changelog

What each version of OctoSplitter adds or changes for the people who use it. A version's section is published as its release notes, which is what the app shows when it offers the update.

How it is kept (see [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md#74-publishing-a-release)):

- Every change people can notice adds a line under **Unreleased** in the same pull request. Say exactly what was added, changed or fixed, in plain words. A version that changes nothing in the app says so.
- `tools/release.py` refuses to release while Unreleased is empty and turns it into the new version's section.
- CI refuses to publish a version that has no section here.

The technical history (commits, measurements) is in [section 9 of the documentation](docs/DOCUMENTATION.md#9-change-history).

## Unreleased

## 1.2.2 (2026-10-17)

- The project moved to https://github.com/Pablokaer/OctoSplitter. The old address still leads there.
- The app now checks for updates at the new address.
- Nothing else in the app changed.

## 1.2.1 (2026-10-17)

- No change to the app: this version only updated the README screenshots and the build checks. Updating from 1.2.0 is optional.

## 1.2.0 (2026-10-08)

- New name and logo: StemSplitter is now **OctoSplitter**, with a red octopus logo and new app icons. The download files, the program, the install folder and your settings keep the name StemSplitter, so this version installs over the old one and keeps your settings and models.
- New look: a near-black theme with a red accent, a sidebar that shrinks to icons when the window is narrow, a bigger drop area that you can click or drop files on, and an animation in the processing card while a song is split.
- New **Extracted Stems** card: after a split, play the original song and each stem on its own channel, with its waveform, play, mute, solo, volume and a menu to show the file in its folder or copy its path. All the tracks share one playhead: click or drag any waveform to move it.
- The window opens at 1180×760 and can be made as small as 900×640 (it was 1100×700).
- Unchanged: the separation, the files it writes and your settings.
