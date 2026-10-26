# Changelog

## v3.1 — 26 October 2026

- **Moved into selfdriven-build** as `lab/field-deck/`, beside the original guide's source (`docs/pages/`).
- **Octo r2** (22 October): wakes to "hey octo", "hello octo" or just "octo"; a livelier Piper voice (pitch and
  timing variation up, a touch quicker: `TALK_EXPRESS`, `TALK_RHYTHM`, `TALK_PACE`); chattier answers; a few different
  "Yes?" replies. Tests in `software/voice/tests/`. Confirmed working on the deck.
- **New: [JOURNEY.md](JOURNEY.md)**, the dated story of the build, with pictures of the earlier cases.
- **New: [concepts/dock-and-camera/](concepts/dock-and-camera/README.md)**: a base dock (keyboard, radio, knob,
  speaker), camera-pod looks and how the chosen film lens fixes on. Concepts only; nothing built.
- **Public copy:** the two first names cut into the body's back are filled in (body STL, STEP, scripts); the HUD
  service's user name is `YOURUSER`; local paths in the Fusion scripts read `/path/to/Field Deck/`.

## v3 — 20 October 2026

The guide rewritten as one complete document, [BUILD_GUIDE.md](BUILD_GUIDE.md), after the deck was rebuilt into the
printed MK-I case.

- **New: the MK-I case.** Print settings for each of the six parts, the power lever and the retainer ring, the
  after-print clean-up, and the assembly sequence with every screw (18 + 8 × M3 × 8) and the foam.
- **New: microphone and an offline voice assistant.** INMP441 on I2S (`dtoverlay=adau7002-simple`), whisper.cpp,
  Ollama with llama3.2:3b, Piper, a Bluetooth speaker; `octo.py` (wake phrase "hello octo") and `talk.py`.
- **New: `POWER_OFF_ON_HALT=1`**, so `sudo poweroff` really turns the deck off (E26).
- **New: diagrams** of the stack and of the 40-pin header as wired, and how to open a finished stack safely (E27).
- **New for Raspberry Pi OS trixie:** Control Centre paths for rotation and screen blanking; Wi-Fi sign-in pages;
  keyring prompts with auto-login.
- **New: the heat check** — idle temperatures and a 30-minute closed-case soak test (E29).
- **Updated:** the BOM with the prices actually paid and the parts added since September; a tools list.
- **Updated:** case-design lessons — design from the maker's drawing, not the caliper sheet (E36); check screws with
  the real screw (E37).
- **HUD software:** the one-page HUD that runs on the deck (`software/hud/`); the earlier four-page package is archived.
- **Errata:** E25–E37 added; E1–E24 brought up to date ([docs/ERRATA.md](docs/ERRATA.md)).
- **This repository:** print files, CAD, software and config collected as a build kit.

## v2 change list — 28 September 2026

E15–E24 plus the structural changes — an assembly-order diagram, lessons for printed cases, a troubleshooting table —
after two months with a working unit (`Field-Deck-Guide-v2-Changes.md`).

## Errata E1–E14 — June to August 2026

The June desk audit and the August field findings (`Field-Deck-Guide-Errata.docx`).

## v1 — June 2026

The original public guide at `selfdriven.you/cyberdeck-build-guide`, now `selfdriven.build/cyberdeck-build-guide`.
