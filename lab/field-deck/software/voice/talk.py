"""Field Deck - talk to the local model.
Press Enter, speak, press Enter. The deck writes down what you said (whisper.cpp, offline)
and your Ollama model answers on screen. Ctrl+C quits.

Needs: the INMP441 mic on I2S (dtoverlay=adau7002-simple), whisper.cpp built in ~/whisper.cpp
with models/ggml-base.en.bin, and Ollama serving on this deck (localhost:11434)."""
import array, json, math, os, re, signal, subprocess, sys, threading, time, urllib.request, wave

MODEL = os.environ.get("TALK_MODEL", "llama3.2:3b")
OLLAMA = "http://localhost:11434"
WHISPER = os.path.expanduser("~/whisper.cpp/build/bin/whisper-cli")
WMODEL = os.path.expanduser(os.environ.get("TALK_WMODEL", "~/whisper.cpp/models/ggml-base.en.bin"))
MIC = ["arecord", "-q", "-D", "hw:CARD=adau7002,DEV=0", "-f", "S32_LE", "-r", "48000", "-c", "2"]
RAW, CLEAN, ERR = "/tmp/talk_raw.wav", "/tmp/talk_16k.wav", "/tmp/talk_mic.err"
QUIET_DB = -75.0          # below this the mic heard only its own hiss
KEEP = 12                 # remember the last 6 questions and answers
SYSTEM = ("You are Field Deck, the assistant inside a small handheld computer. "
          "The user is speaking to you, so answer in two or three short sentences.")


def post(path, body, timeout):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout)


def check_ollama():
    """Says at the start if Ollama or the model is missing, then loads the model while you speak."""
    try:
        with urllib.request.urlopen(OLLAMA + "/api/tags", timeout=5) as r:
            names = [m.get("name") for m in json.load(r).get("models", [])]
    except Exception as e:
        print("Warning: Ollama isn't answering (%s). Check that 'ollama run %s' works." % (e, MODEL))
        return
    if (MODEL if ":" in MODEL else MODEL + ":latest") not in names:
        print("Warning: %s isn't on this deck. 'ollama list' shows the ones that are." % MODEL)
        return

    def warm():
        try:
            with post("/api/generate", {"model": MODEL, "keep_alive": "30m"}, 300) as r:
                r.read()
        except Exception:
            pass                              # chat() will say what is wrong
    threading.Thread(target=warm, daemon=True).start()


def record():
    """Records until Enter. Returns None if it went well, else what went wrong."""
    for f in (RAW, CLEAN):
        if os.path.exists(f):
            os.remove(f)                      # never send an old take by mistake
    input("\nPress Enter, then speak... ")
    with open(ERR, "w") as err:
        p = subprocess.Popen(MIC + [RAW], stderr=err)
    try:
        time.sleep(0.3)                       # the mic settles; arecord stops at once if it can't open it
        if p.poll() is None:
            input("  listening - press Enter when you're done. ")
    finally:
        if p.poll() is None:
            p.send_signal(signal.SIGINT)      # arecord finishes the file properly on Ctrl+C
        p.wait()
    if os.path.exists(RAW) and os.path.getsize(RAW) > 44:
        return None
    with open(ERR) as f:
        msg = f.read().strip()
    if "busy" in msg:
        return "the mic is busy - another recording is still running. Stop it with: pkill arecord"
    return "the mic didn't record: " + (msg.splitlines()[-1] if msg else "no sound file")


def to_16k():
    """The mic's left channel (L/R is on ground), 48 kHz 32-bit -> 16 kHz 16-bit mono, the first 0.3 s
    and the DC and rumble removed, levelled. Returns the level in dBFS, or None if the take is too short."""
    try:
        with wave.open(RAW) as w:
            if (w.getsampwidth(), w.getnchannels()) not in ((4, 2),):
                return None
            raw = w.readframes(min(w.getnframes(), (os.path.getsize(RAW) - 44) // 8))
    except (wave.Error, EOFError, OSError):
        return None
    left = array.array("i", raw[:len(raw) // 8 * 8])[0::2][int(0.3 * 48000):]
    n = len(left) // 3 * 3
    if n < 48000 // 2:                        # under half a second of speech
        return None
    avg = [(a + b + c) / 3.0 for a, b, c in zip(left[0:n:3], left[1:n:3], left[2:n:3])]
    x, y, prev = [], 0.0, avg[0]
    for v in avg:                             # high-pass at about 50 Hz: drops DC and rumble
        y = v - prev + 0.98 * y
        prev = v
        x.append(y)
    rms = math.sqrt(sum(v * v for v in x) / len(x))
    if rms == 0:
        return -999.0                         # a flat line: the mic sent no sound at all
    g = 0.6 * 32767 / max(abs(v) for v in x)
    pcm = array.array("h", (int(v * g) for v in x))
    with wave.open(CLEAN, "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(16000); o.writeframes(pcm.tobytes())
    return 20 * math.log10(rms / 2 ** 31)


def transcribe():
    """Returns the words, "" if there were none, or None if whisper failed."""
    r = subprocess.run([WHISPER, "-m", WMODEL, "-f", CLEAN, "-nt", "-np", "-t", "4"],
                       capture_output=True, text=True)
    if r.returncode:
        lines = r.stderr.strip().splitlines()
        print("  (whisper stopped: %s)" % (lines[-1] if lines else "exit code %d" % r.returncode))
        return None
    text = re.sub(r"\[[^\]]*\]|\([^)]*\)|\*[^*]*\*", " ", r.stdout)   # [BLANK_AUDIO], (wind), *music*
    return " ".join(text.split())


def chat(history):
    reply = ""
    body = {"model": MODEL, "messages": history, "stream": True, "keep_alive": "30m"}
    with post("/api/chat", body, 300) as r:
        for line in r:
            if not line.strip():
                continue
            m = json.loads(line)
            if "error" in m:
                raise RuntimeError(m["error"])
            piece = m.get("message", {}).get("content", "")
            print(piece, end="", flush=True)
            reply += piece
            if m.get("done"):
                break
    print()
    return reply


def main():
    for f, what in ((WHISPER, "whisper.cpp (build it in ~/whisper.cpp)"), (WMODEL, "the speech model")):
        if not os.path.exists(f):
            sys.exit("Missing %s: %s" % (what, f))
    print("Talking to %s. Ctrl+C quits." % MODEL)
    check_ollama()
    history = [{"role": "system", "content": SYSTEM}]
    while True:
        problem = record()
        if problem:
            print("  (%s)" % problem)
            continue
        level = to_16k()
        if level is None:
            print("  (too short - speak for at least a second)")
            continue
        if level < -120:
            print("  (the mic sent a flat line - check its leads)")
            continue
        if level < QUIET_DB:
            print("  (too quiet: %.0f dB - speak closer to the mic)" % level)
            continue
        print("  level %.0f dB, writing it down..." % level)
        text = transcribe()
        if text is None:
            continue
        if not text:
            print("  (couldn't make out any words)")
            continue
        print("You:  " + text)
        history.append({"role": "user", "content": text})
        print("Deck: ", end="", flush=True)
        try:
            history.append({"role": "assistant", "content": chat(history)})
        except Exception as e:
            history.pop()
            print("\n  (no answer from Ollama: %s. Check that 'ollama run %s' works.)" % (e, MODEL))
        del history[1:-KEEP]                  # keep the instructions and the last 6 exchanges


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")
