# Octo — the voice assistant

Talk to the deck's local model, offline:

INMP441 mic → whisper.cpp (speech to text) → Ollama, llama3.2:3b (the answer) → Piper (text to speech) → Bluetooth speaker

| File | What it is |
|---|---|
| `octo.py` | Hands-free (r2, 22 October 2026). Say **"Hey Octo"**, **"Hello Octo"** or just **"Octo"** and your question in one go ("Hey Octo, what's the time?"), or say the name, wait for its reply ("Yes?", "Yep?", "What's up?" or "Go on.") and finish your question within about 7 seconds. The answer shows on screen and Piper reads it out. Ctrl+C quits |
| `talk.py` | Push to talk: press Enter, speak, press Enter. Text only |
| `tests/test_octo_r2.py` | Checks for `octo.py` that need no deck: the wake phrases (20 that should wake it, 15 that shouldn't), the listening loop with a fake mic, whisper and Ollama, and Piper's settings. Needs `piper-tts`: `python tests/test_octo_r2.py` |

## Setup

Everything they need — the microphone overlay, whisper.cpp with the `base.en` model, Ollama with `llama3.2:3b`, Piper
with the `en_GB-vctk-medium` voice, `pipewire-alsa` and a paired Bluetooth speaker — is in Step 7 of the
[build guide](../../BUILD_GUIDE.md). Then copy the two files to the deck, for example from your computer:

```bash
scp octo.py talk.py <user>@<deck-ip>:~/
```

## Run

```bash
~/voice/bin/python ~/octo.py     # with speech (python3 ~/octo.py gives text only)
python3 ~/talk.py
```

## Settings

Change them with environment variables, e.g. `TALK_EXPRESS=0.75 ~/voice/bin/python ~/octo.py`:

| Variable | Default | |
|---|---|---|
| `TALK_MODEL` | `llama3.2:3b` | the Ollama model (Ollama at `http://localhost:11434`) |
| `TALK_WMODEL` | `~/whisper.cpp/models/ggml-base.en.bin` | the whisper model; a `tiny.en` model is faster |
| `TALK_VOICE` | `~/piper-voices/en_GB-vctk-medium.onnx` | the Piper voice |
| `TALK_SPEAKER` | `71` | the speaker within that voice (71 and 25 are the closest to Australian) |
| `TALK_WAKE` | `hey octo,hello octo,octo` | the wake phrases, comma-separated |
| `TALK_EXPRESS` | `0.85` | how much the pitch moves (Piper's `noise_scale`; this voice's own value is 0.667) |
| `TALK_RHYTHM` | `1.0` | how uneven the timing is (`noise_w_scale`; the voice's own 0.8) |
| `TALK_PACE` | `0.92` | speed (`length_scale`; under 1 is quicker, the voice's own 1.0) |

Much past 1.0 on `TALK_EXPRESS` or `TALK_RHYTHM` and the voice starts to wobble; 0.667 / 0.8 / 1.0 gives the flatter r1
voice back.

The microphone is read with `arecord -D hw:CARD=adau7002,DEV=0 -f S32_LE -r 48000 -c 2` (left channel). Octo remembers
the last six questions and answers.

## How it hears its name

Octo listens all the time, cuts what it hears into stretches of speech, and has whisper write each one down. It answers
when a stretch **starts** with a wake phrase (an "um" or "okay" in front is fine). The match is loose, because whisper
mishears short names: "Hey Otto", "Octa", "Okto" and "Oc to" all count, while "Hello everyone", "October", "octopus" and
"Doctor…" don't. Known slips: "Hey doctor" would wake it, and so would a stretch starting with the name Otto.

## Limits

- No echo cancelling: the mic is muted while Octo speaks, so you can't interrupt it.
- English only (the `base.en` model).
- Piper has no Australian English voice; speaker 71 of the British multi-speaker voice is the stand-in.
- It runs in a terminal, not as a service.
- "Mic busy" means another recording is running: `pkill arecord`.
