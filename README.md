# Mornye for iOS 15

Compatibility fork of [mornyeapp/Mornye](https://github.com/mornyeapp/Mornye), based on version 5.4.0.

## Download and install

Download **Mornye-iOS15-unsigned.ipa** from this fork's [Releases](https://github.com/Michy234/Mornye-iOS-Legacy/releases). Re-sign and install it with Sideloadly, AltStore or SideStore. No Mac or Apple distribution certificate is needed to generate the unsigned IPA. The signing tool handles your own Apple ID and provisioning.

Minimum system: **iOS 15.0, arm64**. iOS 14 is not supported by the pinned Flutter 3.50 framework. A successful build checks the minimum OS load commands of every bundled native binary, in addition to bundle metadata. Real-device startup, playback and background behavior still need testing.

## Compatibility changes

- Build the app, CocoaPods plugins and Rust backend for iOS 15.
- Omit the iOS 17 home-screen widget and iOS 27 remote Now Playing extension; their channels report no widget/support. Normal in-app playback and local lock-screen audio controls remain.
- Disable the optional Discord Social SDK integration, which requires private SDK material. No SDK secret is needed.
- Restore the upstream FFmpeg iOS setup script omitted from the vendored plugin and explicitly prepare its frameworks before installing path-based pods.
- Remove the unused App Group entitlement for personal sideload signing.

## Build with GitHub Actions

Open **Actions → iOS 15 IPA → Run workflow**. The workflow uses a GitHub-hosted Mac with Xcode, the project's pinned Flutter and Rust versions, and the committed dependency lockfiles. On success it uploads an artifact and publishes a release containing the IPA and SHA-256 checksum. Pushes to `main` also build it.

The workflow rejects any bundled binary or Info.plist requiring a version above iOS 15.0. It does not rewrite a prebuilt binary's deployment target to bypass this check.

Upstream project documentation: [Contributing](CONTRIBUTING.md). Original licenses and notices are retained in [LICENSE](LICENSE), [COPYING](COPYING), and [NOTICE](NOTICE).
