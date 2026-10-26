"""Octo - talk to the deck's local model, hands-free.
Say "Hey Octo", "Hello Octo" or just "Octo", and your question: in one go ("Hey Octo, what's the time?")
or with a pause ("Octo." ... "Yep?" ... your question). Octo writes down what you said (whisper.cpp,
offline), your Ollama model answers on screen, and Piper reads the answer out loud. Ctrl+C quits.

Run with the voice:  ~/voice/bin/python ~/octo.py      (python3 ~/octo.py gives text only)
Needs: the INMP441 mic (dtoverlay=adau7002-simple), ~/whisper.cpp with models/ggml-base.en.bin,
Ollama on this deck, and for the voice piper-tts in ~/voice and ~/piper-voices/en_GB-vctk-medium.onnx.

r2 (22 Oct 2026): three wake phrases; a livelier voice (Piper's pitch and timing variation turned up, a
little quicker - TALK_EXPRESS, TALK_RHYTHM, TALK_PACE); chattier answers; a few different "Yes?"es."""
import array, collections, difflib, json, math, os, queue, random, re, subprocess, sys, threading, time, urllib.request, wave

MODEL = os.environ.get("TALK_MODEL", "llama3.2:3b")
OLLAMA = "http://localhost:11434"
WHISPER = os.path.expanduser("~/whisper.cpp/build/bin/whisper-cli")
WMODEL = os.path.expanduser(os.environ.get("TALK_WMODEL", "~/whisper.cpp/models/ggml-base.en.bin"))
VOICE = os.path.expanduser(os.environ.get("TALK_VOICE", "~/piper-voices/en_GB-vctk-medium.onnx"))
SPEAKER = int(os.environ.get("TALK_SPEAKER", "71"))   # 71 = a man of 26 from Sydney (VCTK p326); 25 = p374
# How the voice moves (Piper; this voice's own values in brackets). Higher EXPRESS = more pitch movement,
# higher RHYTHM = less even timing, PACE under 1 = quicker. Much past 1.0 on the first two starts to wobble.
EXPRESS = float(os.environ.get("TALK_EXPRESS", "0.85"))   # noise_scale   (0.667)
RHYTHM = float(os.environ.get("TALK_RHYTHM", "1.0"))      # noise_w_scale (0.8)
PACE = float(os.environ.get("TALK_PACE", "0.92"))         # length_scale  (1.0)
# Wake phrases, any of them at the start of what you say; TALK_WAKE takes a comma-separated list.
WAKE = sorted({" ".join(p.lower().split()) for p in os.environ.get("TALK_WAKE", "hey octo,hello octo,octo").split(",")
               if p.strip()}, key=lambda p: (-len(p.split()), -len(p)))
SOUNDS_LIKE = {"octa": "octo", "okto": "octo", "okta": "octo", "otto": "octo", "ochto": "octo"}   # how whisper mishears it
ACKS = ["Yes?", "Yep?", "What's up?", "Go on."]          # when you say only the wake phrase
MIC = ["arecord", "-q", "-D", "hw:CARD=adau7002,DEV=0", "-f", "S32_LE", "-r", "48000", "-c", "2", "-t", "raw"]
CLIP, PLAY_ERR = "/tmp/octo_16k.wav", "/tmp/octo_aplay.err"
FRAME = 1440              # 30 ms of the mic at 48 kHz (480 samples at 16 kHz)
START, HOLD = 12.0, 7.0   # dB above the room's hiss that starts / keeps a stretch of speech
FLOOR = -72.0             # and never quieter than this
HANG, LONGEST = 30, 667   # 0.9 s of quiet ends a stretch; 20 s at most (counted in 30 ms frames)
KEEP = 12                 # remember the last 6 questions and answers
SYSTEM = ("You are Octo, the voice assistant inside Field Deck, a small handheld computer. "
          "The user talks to you and hears your answer read aloud, so answer in one to three short "
          "sentences of plain text, with no lists, symbols or emoji. Sound warm and lively, like a "
          "friendly person chatting: use contractions, mix short and longer sentences, and let a question "
          "or the odd exclamation show how you feel.")


def post(path, body, timeout):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout)


def check_ollama():
    """Says at the start if Ollama or the model is missing, then loads the model in the background."""
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


class Ears(threading.Thread):
    """Listens all the time; every stretch of speech lands in self.heard (16 kHz samples)."""

    def __init__(self):
        super().__init__(daemon=True)
        self.heard = queue.Queue()
        self.mute = threading.Event()         # set while Octo answers, so it doesn't hear itself
        self.talking = False                  # True while someone is speaking
        self.problem = None
        self.proc = subprocess.Popen(MIC, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run(self):
        try:
            self.listen()
        except Exception as e:
            self.problem = repr(e)
        if self.problem is None:
            msg = self.proc.stderr.read().decode(errors="replace").strip()
            self.problem = msg.splitlines()[-1] if msg else "the recording ended"
        self.heard.put(None)

    def listen(self):
        noise, prev, y, skip, told = None, None, 0.0, 10, False   # skip: the mic settles for 0.3 s
        before = collections.deque(maxlen=10)                    # 0.3 s from just before the speech
        speech, levels, loud, quiet = None, [], 0, 0
        while True:
            raw = self.proc.stdout.read(FRAME * 8)
            if len(raw) < FRAME * 8:
                return
            if skip or self.mute.is_set():
                skip = max(0, skip - 1)
                speech, loud, quiet, prev, y = None, 0, 0, None, 0.0
                before.clear()
                self.talking = False
                continue
            left = array.array("i", raw)[0::2]
            frame = []
            for i in range(0, FRAME, 3):              # 48 -> 16 kHz, then a high-pass at about 50 Hz
                v = (left[i] + left[i + 1] + left[i + 2]) / 3.0
                if prev is None:
                    prev = v
                y = v - prev + 0.98 * y
                prev = v
                frame.append(y)
            power = sum(v * v for v in frame) / len(frame)
            db = 10 * math.log10(power / 2.0 ** 62) if power > 0 else -150.0
            if noise is None:
                noise = db
            if speech is None:
                noise += (db - noise) * (0.2 if db < noise else 0.005)
                before.append(frame)
                if not told and len(before) == before.maxlen:
                    print("  (room hiss: %.0f dB)" % noise)
                    told = True
                loud = loud + 1 if db > max(noise + START, FLOOR) else 0
                if loud >= 3:
                    speech, levels, quiet, self.talking = list(before), [], 0, True
            else:
                speech.append(frame)
                levels.append(db)
                quiet = quiet + 1 if db < max(noise + HOLD, FLOOR - 5) else 0
                if quiet >= HANG or len(speech) >= LONGEST:
                    if len(speech) >= LONGEST:        # a steady noise, not speech: raise the bar to it
                        noise = max(noise, sorted(levels)[len(levels) // 2] - 3)
                    if len(speech) - quiet >= 13:     # at least 0.4 s of sound
                        self.heard.put([v for f in speech for v in f])
                    speech, loud, self.talking = None, 0, False
                    before.clear()


def save(samples):
    """The stretch of speech as a 16 kHz 16-bit WAV for whisper, levelled."""
    g = 0.6 * 32767 / (max(abs(v) for v in samples) or 1.0)
    pcm = array.array("h", (int(v * g) for v in samples))
    with wave.open(CLIP, "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(16000); o.writeframes(pcm.tobytes())


def transcribe():
    """The words in CLIP ("" if none). Whisper's [BLANK_AUDIO], (wind) and *music* tags are dropped."""
    r = subprocess.run([WHISPER, "-m", WMODEL, "-f", CLIP, "-nt", "-np", "-t", "4"],
                       capture_output=True, text=True)
    if r.returncode:
        lines = r.stderr.strip().splitlines()
        print("  (whisper stopped: %s)" % (lines[-1] if lines else "exit code %d" % r.returncode))
        return ""
    return " ".join(re.sub(r"\[[^\]]*\]|\([^)]*\)|\*[^*]*\*", " ", r.stdout).split())


def after_wake(text):
    """What follows a wake phrase ("" if nothing), or None if the text doesn't start with one."""
    words = text.split()
    plain = [re.sub(r"[^a-z0-9]", "", w.lower()) for w in words]
    plain = [SOUNDS_LIKE.get(w, w) for w in plain]
    for start in range(3):                    # allows an "um" or "okay" before it
        for want in WAKE:                     # the longest phrase first, so "hey octo" isn't cut after "hey"
            n = len(want.split())
            need = 0.8 if n > 1 else 0.86     # one word on its own must be closer: "doctor" is 0.8 to "octo"
            best, cut = 0.0, 0
            for k in (n, n + 1, n - 1):       # "hello octo", "hello oc to", "hellocto"
                if k < 1 or start + k > len(words):
                    continue
                r = difflib.SequenceMatcher(None, " ".join(w for w in plain[start:start + k] if w), want).ratio()
                if r > best:
                    best, cut = r, start + k
            if best >= need:
                return re.sub(r"^\W+", "", " ".join(words[cut:])).strip()
    return None


class Mouth:
    """Reads text out loud with Piper through aplay, a sentence at a time."""

    def __init__(self):
        import onnxruntime
        onnxruntime.set_default_logger_severity(3)        # hides a harmless GPU warning
        from piper import PiperVoice, SynthesisConfig
        self.voice = PiperVoice.load(VOICE)
        self.style = SynthesisConfig(speaker_id=SPEAKER, noise_scale=EXPRESS, noise_w_scale=RHYTHM, length_scale=PACE)
        self.lines, self.worker, self.problem = None, None, None

    def start(self):
        self.lines = queue.Queue()
        self.worker = threading.Thread(target=self.play, daemon=True)
        self.worker.start()

    def say(self, text):
        text = " ".join(re.sub(r"[^\w\s.,;:?\x21'\"%$&()/+-]", " ", text).split())
        if re.search(r"\w", text):
            self.lines.put(text)

    def finish(self):
        """Waits until everything said so far has been played."""
        self.lines.put(None)
        self.worker.join()

    def speak(self, text):
        self.start()
        self.say(text)
        self.finish()

    def play(self):
        rate, out, done = self.voice.config.sample_rate, None, False
        try:
            with open(PLAY_ERR, "w") as err:
                out = subprocess.Popen(["aplay", "-q", "-t", "raw", "-f", "S16_LE", "-r", str(rate), "-c", "1"],
                                       stdin=subprocess.PIPE, stderr=err)
            out.stdin.write(bytes(2 * int(0.5 * rate)))   # 0.5 s of silence wakes a dozing speaker
            while True:
                text = self.lines.get()
                if text is None:
                    done = True
                    break
                for chunk in self.voice.synthesize(text, syn_config=self.style):
                    out.stdin.write(chunk.audio_int16_bytes)
            out.stdin.close()
            if out.wait() and os.path.getsize(PLAY_ERR):
                raise OSError("aplay stopped")
            self.problem = None
        except Exception as e:
            if out:
                out.kill()
            with open(PLAY_ERR) as f:
                why = f.read().strip()
            why = why.splitlines()[-1] if why else str(e)
            if not why == self.problem:                   # says it once, not after every answer
                print("\n  (no sound: %s)" % why)
                self.problem = why
            while not done:                               # lets finish() return
                done = self.lines.get() is None


def chat(history, say=None):
    """Streams the model's answer to the screen, and each finished sentence to say()."""
    reply, part = "", ""
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
            if say:
                part += piece
                *done, part = re.split(r"(?<=[.?\x21])\s+|\n+", part)
                for s in done:
                    say(s)
            if m.get("done"):
                break
    print()
    if say and part.strip():
        say(part)
    return reply


def answer(question, history, mouth):
    print("You:  " + question)
    history.append({"role": "user", "content": question})
    print("Octo: ", end="", flush=True)
    if mouth:
        mouth.start()
    try:
        history.append({"role": "assistant", "content": chat(history, mouth.say if mouth else None)})
    except Exception as e:
        history.pop()
        print("\n  (no answer from Ollama: %s. Check that 'ollama run %s' works.)" % (e, MODEL))
    if mouth:
        mouth.finish()
    del history[1:-KEEP]                      # keep the instructions and the last 6 exchanges


def busy(ears, job, *args):
    """Runs job with the mic muted, then listens afresh."""
    ears.mute.set()
    try:
        job(*args)
    finally:
        time.sleep(0.5)                       # the last word dies away (Bluetooth lags a little)
        try:
            while True:                       # drops whatever was heard before or meanwhile
                if ears.heard.get_nowait() is None:
                    ears.heard.put(None)      # but not the news that the mic stopped
                    break
        except queue.Empty:
            pass
        ears.mute.clear()


def talk(ears, mouth):
    history = [{"role": "system", "content": SYSTEM}]
    if mouth:
        busy(ears, mouth.speak, "G'day, Octo here.")
    names = [w.title() for w in sorted(WAKE, key=lambda p: (len(p.split()), p), reverse=True)]
    print('Listening. Say %s, and your question. Ctrl+C quits.' % " or ".join('"%s"' % w for w in names))
    awake = 0.0                               # until then, the next thing you say is the question
    while True:
        try:
            samples = ears.heard.get(timeout=0.5)
        except queue.Empty:
            if awake and time.time() > awake:
                awake = 0.0
                print('  (stopped waiting - say "%s" again)' % names[-1])
            continue
        if samples is None:
            hint = " - another recording is running: pkill arecord" if "busy" in ears.problem else ""
            sys.exit("The mic stopped: %s%s" % (ears.problem, hint))
        save(samples)
        text = transcribe()
        if not text:
            continue
        rest = after_wake(text)
        if rest is None and not awake:
            print('  (not for me: "%s")' % text)
            continue
        question = text if rest is None else rest
        if question:
            awake = 0.0
            busy(ears, answer, question, history, mouth)
        else:                                 # only the wake phrase
            if not ears.talking and ears.heard.empty():
                ack = random.choice(ACKS)
                print("Octo: " + ack)
                if mouth:
                    busy(ears, mouth.speak, ack)
            awake = time.time() + 8


def main():
    for f, what in ((WHISPER, "whisper.cpp (build it in ~/whisper.cpp)"), (WMODEL, "the speech model")):
        if not os.path.exists(f):
            sys.exit("Missing %s: %s" % (what, f))
    mouth = None
    try:
        if not os.path.exists(VOICE):
            raise OSError("no voice file at " + VOICE)
        print("Loading the voice...")
        mouth = Mouth()
    except ImportError:
        print("Voice off: Piper isn't here. For the voice, run me as: ~/voice/bin/python ~/octo.py")
    except Exception as e:
        print("Voice off: %s" % e)
    check_ollama()
    ears = Ears()
    ears.start()
    try:
        talk(ears, mouth)
    finally:
        ears.proc.terminate()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")
