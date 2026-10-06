#!/usr/bin/env python3
"""Generate local synthesized pronunciation clips with installed macOS voices.

These clips are synthesized study aids, not dictionary recordings. Acupoint
names are Chinese names written in pinyin; they use Mandarin audio rather than
pretending the names are English words. No network access is used.
"""

from array import array
import json
import math
from pathlib import Path
import subprocess
import sys
import wave


PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT / "public" / "audio"
ENGLISH_TERMS = {
    "supraspinatus": "Supraspinatus",
    "infraspinatus": "Infraspinatus",
    "teres-minor": "Teres minor",
    "subscapularis": "Subscapularis",
    "deltoid": "Deltoid",
    "acromial-part": "Acromial part",
    "clavicular-part": "Clavicular part",
    "spinal-part": "Spinal part",
    "scapula": "Scapula",
    "clavicle": "Clavicle",
    "humerus": "Humerus",
    "rotator-cuff": "Rotator cuff",
    "scapular-spine": "Scapular spine",
    "inferior-angle": "Inferior angle",
    "acromion": "Acromion",
    "greater-tubercle": "Greater tubercle",
    "infraspinous-fossa": "Infraspinous fossa",
    "supraspinous-fossa": "Supraspinous fossa",
    "posterior-shoulder": "Posterior shoulder",
    "anterolateral-acromion": "Anterolateral acromion",
    "posterolateral-acromion": "Posterolateral acromion",
    "posterior-deltoid": "Posterior deltoid",
}
ACUPOINT_NAMES = {
    "si11": "天宗",
    "si12": "秉风",
    "si9": "肩贞",
    "li15": "肩髃",
    "te14": "肩髎",
}


def inspect_audio(path: Path) -> dict:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frames = wav.getnframes()
        if sample_width != 2 or wav.getcomptype() != "NONE":
            raise ValueError("Expected uncompressed signed 16-bit PCM")
        samples = array("h", wav.readframes(frames))
    if sys.byteorder != "little":
        samples.byteswap()
    duration = frames / sample_rate
    peak = max((abs(sample) for sample in samples), default=0)
    rms = math.sqrt(sum(sample * sample for sample in samples) / max(1, len(samples)))
    if not 0.35 <= duration <= 10:
        raise ValueError(f"Unexpected duration: {duration:.3f}s")
    if peak < 100 or rms < 10:
        raise ValueError(f"Audio is silent or too quiet: peak={peak}, rms={rms:.2f}")
    return {
        "duration": round(duration, 4),
        "sampleRate": sample_rate,
        "channels": channels,
        "peak": peak,
        "rms": round(rms, 2),
        "bytes": path.stat().st_size,
    }


def main() -> int:
    current_manifest = OUTPUT / "manifest.json"
    if current_manifest.exists():
        current = json.loads(current_manifest.read_text(encoding="utf-8"))
        if any(clip.get("provider") == "OpenAI" for clip in current.get("clips", {}).values()):
            print("This manifest already includes OpenAI audio. Use the OpenAI generation/import scripts to preserve its clips and provenance.", file=sys.stderr)
            return 2
    OUTPUT.mkdir(parents=True, exist_ok=True)
    clips = {}
    failures = {}
    batches = [
        (ENGLISH_TERMS, "Samantha", "en-US", "English anatomical term"),
        (ACUPOINT_NAMES, "Tingting", "zh-CN", "Chinese acupoint name; pinyin is not English"),
    ]
    for terms, voice, language, kind in batches:
        for slug, term in terms.items():
            output = OUTPUT / f"{slug}.wav"
            try:
                subprocess.run(
                    ["/usr/bin/say", "-v", voice, "-r", "140", "-o", str(output),
                     "--file-format=WAVE", "--data-format=LEI16@22050", term],
                    check=True, capture_output=True, text=True, timeout=30,
                )
                inspection = inspect_audio(output)
                clips[slug] = {
                    "text": term,
                    "voice": voice,
                    "lang": language,
                    "file": f"audio/{slug}.wav",
                    "synthesized": True,
                    "kind": kind,
                    "rateWordsPerMinute": 140,
                    **inspection,
                }
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                failures[slug] = str(exc)
                output.unlink(missing_ok=True)
    manifest = {
        "version": 1,
        "synthesized": True,
        "generator": "macOS say",
        "description": "Synthesized pronunciation study aids, not human dictionary recordings.",
        "acupointNote": "穴位名称为汉语拼音名称，并非英语词；穴名音频使用普通话。",
        "clips": clips,
        "failures": failures,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"generated": len(clips), "failed": failures, "totalBytes": sum(item["bytes"] for item in clips.values())}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
