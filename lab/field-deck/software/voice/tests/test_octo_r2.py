"""Tests for octo.py r2 (22 Oct 2026): the wake phrases, the talk loop with fakes, Piper's settings against the
real piper-tts 1.8.0, environment overrides, and the file itself. Run with a Python that has piper-tts installed:
    <venv>/bin/python test_octo_r2.py
"""
import io, os, queue, random, subprocess, sys, types
HERE = os.path.dirname(os.path.abspath(__file__))
OCTO_DIR = HERE if os.path.exists(os.path.join(HERE, "octo.py")) else os.path.dirname(HERE)   # beside it, or one up
sys.path.insert(0, OCTO_DIR)
import octo

PASS, FAIL = [], []
def ok(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("  ok    " if cond else "  FAIL  ") + name + (("   " + extra) if extra else ""))

# ------------------------------------------------------------------ A: wake phrases
print("A. wake phrases (default: %s)" % octo.WAKE)
CASES = [
    ("Hello Octo, what's the time?", "what's the time?"),
    ("Hey Octo, what's the time?", "what's the time?"),
    ("Octo, what's the time?", "what's the time?"),
    ("Octo.", ""), ("Octo?", ""), ("Hey Octo.", ""), ("Hello, Octo.", ""), ("Hey, Octo...", ""),
    ("Hey, Octo\x21 Tell me a joke.", "Tell me a joke."),
    ("Um, hey Octo, how far is the moon?", "how far is the moon?"),
    ("Okay Octo what's up", "what's up"),
    ("Hey Otto, what's the weather?", "what's the weather?"),
    ("Hello Otto.", ""),
    ("Octa, set a timer.", "set a timer."),
    ("Hey Octa.", ""),
    ("Okto, how are you?", "how are you?"),
    ("Hellocto, hi.", "hi."),
    ("Oc to, what time is it?", "what time is it?"),
    ("Octo's here?", "here?"),
    ("So, Octo, play some music.", "play some music."),
    # not for Octo
    ("Hello everyone.", None), ("Hey, how are you?", None), ("Hello there.", None), ("Hey Siri.", None),
    ("October is nice.", None), ("I like octopus.", None), ("Auto mode on.", None), ("What's the time?", None),
    ("Doctor Who is on tonight.", None), ("A doctor said so.", None), ("Okay.", None), ("Oh, to be honest.", None),
    ("Actually, I think so.", None), ("Hector called.", None), ("", None),
]
for text, want in CASES:
    got = octo.after_wake(text)
    ok("%-42r -> %r" % (text, want), got == want, "" if got == want else "got %r" % (got,))

# ------------------------------------------------------------------ B: the talk loop with fakes
print("\nB. the talk loop (fake mic, whisper and Ollama)")
class Heard:
    """Hands talk() one scripted stretch per get(); nothing arrives while Octo is busy."""
    def __init__(self, texts, clock):
        self.items, self.clock = list(texts), clock
    def get(self, timeout=None):
        if not self.items:
            return None                          # the mic 'stops': talk() exits
        item = self.items.pop(0)
        if item == "WAIT":                       # a quiet poll: time passes, nothing heard
            self.clock[0] += 9.0
            raise queue.Empty
        octo._next_text = item
        return [0.0] * 4800
    def get_nowait(self):
        raise queue.Empty
    def put(self, x):
        pass
    def empty(self):
        return True

class Ears:
    def __init__(self, texts, clock):
        import threading
        self.heard, self.mute, self.talking, self.problem = Heard(texts, clock), threading.Event(), False, "the recording ended"

class Mouth:
    def __init__(self):
        self.said = []
    def speak(self, text):
        self.said.append(text)
    def start(self): pass
    def say(self, text): self.said.append(text)
    def finish(self): pass

def run(texts, mouth=None):
    clock = [1000.0]
    asked, out = [], io.StringIO()
    octo.save = lambda s: None
    octo.transcribe = lambda: octo._next_text
    octo.answer = lambda q, h, m: asked.append(q)
    octo.time.time = lambda: clock[0]
    octo.time.sleep = lambda s: None
    real = sys.stdout
    sys.stdout = out
    try:
        octo.talk(Ears(texts, clock), mouth)
    except SystemExit:
        pass
    finally:
        sys.stdout = real
    return asked, out.getvalue()

random.seed(1)
asked, log = run(["Hey Octo, what's the time?"])
ok("one breath: 'Hey Octo, what's the time?' is asked", asked == ["what's the time?"], repr(asked))
ok("start-up line names all three phrases", 'Say "Hey Octo" or "Hello Octo" or "Octo", and your question.' in log,
   log.splitlines()[0] if log else "")
asked, log = run(["Octo.", "What's the weather like?"])
ok("'Octo.' then the question in the next breath is asked", asked == ["What's the weather like?"], repr(asked))
ok("  ... and Octo acknowledged with one of the replies", any(("Octo: " + a) in log for a in octo.ACKS))
m = Mouth()
asked, log = run(["Hello Octo.", "Tell me a joke."], m)
ok("spoken greeting, then a spoken acknowledgement", m.said[:1] == ["G'day, Octo here."] and m.said[1] in octo.ACKS, repr(m.said))
asked, log = run(["Hello everyone.", "What's the time?"])
ok("not for Octo: nothing asked", asked == [] and log.count("(not for me") == 2, repr(asked))
asked, log = run(["Octo.", "WAIT", "What's the time?"])
ok("after 'Octo.' and 9 s of quiet it stops waiting", asked == [] and '(stopped waiting - say "Octo" again)' in log, repr(asked))
seen = set()
for s in range(40):
    random.seed(s)
    _, log = run(["Octo."])
    seen |= {a for a in octo.ACKS if ("Octo: " + a) in log}
ok("acknowledgements vary (seen over 40 runs)", seen == set(octo.ACKS), repr(sorted(seen)))

# ------------------------------------------------------------------ C: Piper settings, real piper-tts
print("\nC. the voice settings against the real piper-tts")
import piper
captured = {}
class FakeVoice:
    config = types.SimpleNamespace(sample_rate=22050)
    def synthesize(self, text, syn_config=None):
        captured.setdefault("cfg", syn_config); captured.setdefault("texts", []).append(text)
        yield types.SimpleNamespace(audio_int16_bytes=b"\x00\x00" * 100)
class FakeAplay:
    def __init__(self, *a, **k):
        self.stdin = io.BytesIO(); self.stdin.close = lambda: None
    def wait(self): return 0
    def kill(self): pass
piper.PiperVoice.load = staticmethod(lambda path: FakeVoice())
real_popen = octo.subprocess.Popen
octo.subprocess.Popen = FakeAplay
try:
    mo = octo.Mouth()
    mo.speak("G'day, Octo here.")
finally:
    octo.subprocess.Popen = real_popen
cfg = captured.get("cfg")
ok("SynthesisConfig is piper's own class", isinstance(cfg, piper.SynthesisConfig), type(cfg).__name__)
ok("speaker 71, noise_scale 0.85, noise_w_scale 1.0, length_scale 0.92",
   cfg is not None and (cfg.speaker_id, cfg.noise_scale, cfg.noise_w_scale, cfg.length_scale) == (71, 0.85, 1.0, 0.92),
   repr(cfg))
ok("the text reached synthesize()", captured.get("texts") == ["G'day, Octo here."], repr(captured.get("texts")))
import inspect
src = inspect.getsource(piper.voice.PiperVoice)
ok("piper 1.8.0 reads noise_scale / noise_w_scale / length_scale from syn_config",
   all(("syn_config.%s" % f) in src for f in ("noise_scale", "noise_w_scale", "length_scale")))

# ------------------------------------------------------------------ D: environment overrides
print("\nD. environment overrides")
code = "import octo; print(octo.WAKE); print(octo.EXPRESS, octo.RHYTHM, octo.PACE)"
env = dict(os.environ, TALK_WAKE="Hello Octo", TALK_EXPRESS="0.7", TALK_RHYTHM="0.9", TALK_PACE="1.0")
r = subprocess.run([sys.executable, "-c", code], cwd=OCTO_DIR, env=env, capture_output=True, text=True)
ok("TALK_WAKE='Hello Octo' -> just that phrase", "['hello octo']" in r.stdout, r.stdout.strip().replace("\n", " | ") + r.stderr[-200:])
ok("TALK_EXPRESS / TALK_RHYTHM / TALK_PACE are read", "0.7 0.9 1.0" in r.stdout)
env = dict(os.environ, TALK_WAKE="computer, hey deck")
r = subprocess.run([sys.executable, "-c", "import octo; print(octo.WAKE); print(octo.after_wake('Hey deck, hi'))"],
                   cwd=OCTO_DIR, env=env, capture_output=True, text=True)
ok("any list works ('computer, hey deck')", "['hey deck', 'computer']" in r.stdout and "hi" in r.stdout, r.stdout.strip().replace("\n", " | "))

# ------------------------------------------------------------------ E: the file
print("\nE. the file")
path = os.path.join(OCTO_DIR, "octo.py")
text = open(path).read()
ok("no exclamation mark anywhere (safe to paste)", "\x21" not in text)
ok("compiles", subprocess.run([sys.executable, "-m", "py_compile", path]).returncode == 0)
ok("only the standard library at the top (piper/onnxruntime only inside Mouth)",
   "import array, collections, difflib, json, math, os, queue, random, re, subprocess, sys, threading, time, urllib.request, wave" in text)

print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
sys.exit(1 if FAIL else 0)
