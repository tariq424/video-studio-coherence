"""Time one short vs one long TTS call through WanGP (no polling delay measured separately)."""
import time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from studio import config, media
from studio.wangp import WanGP
cfg = config.load(); wg = WanGP(cfg["wangp_mcp"])
short = "Dave Blundin says nothing will ever police AI except other AI. He argues the real bottleneck is transparency of the activations, seeing what the AI is thinking."
long_ = " ".join([short, "On longevity, Peter Diamandis says evidence changes minds. He cites Dario predicting lifespans could double in five to ten years, and Demis Hassabis talking about curing all disease.",
                  "Dave's career advice for computer scientists: move toward manufacturing. Software is cooked, he says, but hardware has many years to run."])
for name, text in (("short", short), ("long", long_)):
    t0 = time.time()
    r = wg.gen({"model_type": cfg["tts_model"], "prompt": text, "audio_prompt_type": "A", "audio_guide": cfg["voice_ref_wav"],
                "alt_prompt": cfg["voice_ref_text"], "model_mode": "english", "duration_seconds": 60, "temperature": 0.7, "top_k": 50, "seed": 4242},
               print, name)
    dt = time.time() - t0
    print(f"BENCH {name}: {len(text.split())} words, wall {dt:.1f}s, audio {media.dur(r['file']):.1f}s, ok={r['ok']}", flush=True)
print("BENCH_DONE")
