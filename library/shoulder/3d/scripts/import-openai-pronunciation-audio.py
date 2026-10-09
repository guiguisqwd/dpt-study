#!/usr/bin/env python3
"""Validate and import downloaded OpenAI pronunciation audio.

This does not call a speech service or search for credentials. Supply a JSON
mapping of the actual downloaded clips; unknown generation settings stay null.
By default it validates without writing and requires a complete set. Explicit
--allow-partial permits a selected subset; unprovided terms retain their audio.

Input shape:
{
  "provider": "OpenAI", "voice": "marin", "model": null,
  "source": {"url": "https://www.openai.fm/", "method": "browser UI download"},
  "generationParameters": {"instructions": "the exact instructions used"},
  "clips": {
    "supraspinatus": {"path": "/path/to/download.wav", "input": "Supraspinatus"}
  }
}
Per-clip generationParameters override common settings when necessary.
"""

from array import array
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import wave


PROJECT = Path(__file__).resolve().parent.parent
AUDIO = PROJECT / "public" / "audio"
MANIFEST = AUDIO / "manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_audio(path: Path) -> dict:
    """Decode locally to signed PCM, retaining the original download on import."""
    with tempfile.TemporaryDirectory(prefix="pronunciation-check-") as directory:
        decoded = Path(directory) / "decoded.wav"
        subprocess.run(
            ["/usr/bin/afconvert", str(path), str(decoded), "-f", "WAVE", "-d", "LEI16"],
            check=True, capture_output=True, text=True, timeout=30,
        )
        with wave.open(str(decoded), "rb") as wav:
            frames = wav.getnframes()
            sample_rate = wav.getframerate()
            channels = wav.getnchannels()
            if wav.getsampwidth() != 2 or wav.getcomptype() != "NONE":
                raise ValueError(f"Expected 16-bit PCM after decoding: {path}")
            samples = array("h", wav.readframes(frames))
    if sys.byteorder != "little":
        samples.byteswap()
    duration = frames / sample_rate
    peak = max((abs(sample) for sample in samples), default=0)
    rms = math.sqrt(sum(sample * sample for sample in samples) / max(1, len(samples)))
    if not 0.25 <= duration <= 15:
        raise ValueError(f"Unexpected single-term duration {duration:.3f}s: {path}")
    if peak < 100 or rms < 10:
        raise ValueError(f"Audio is silent or too quiet: {path}")
    return {
        "duration": round(duration, 4), "sampleRate": sample_rate,
        "channels": channels, "peak": peak, "rms": round(rms, 2),
        "bytes": path.stat().st_size, "sha256": digest(path),
        "measurement": "Locally decoded signed 16-bit PCM; source download preserved",
    }


def prepare(mapping_path: Path, allow_partial: bool = False) -> tuple[dict, list[tuple[Path, Path]], dict]:
    batch = json.loads(mapping_path.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if batch.get("provider") != "OpenAI":
        raise ValueError("Only an explicitly identified OpenAI batch is supported")
    voice = batch.get("voice", "")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", voice):
        raise ValueError("voice must be the actual lower-case OpenAI voice name")
    for key in ("model", "source", "generationParameters"):
        if key not in batch:
            raise ValueError(f"Missing {key}; use null for unknown settings")
    if not isinstance(batch["source"], dict) or not batch["source"].get("url"):
        raise ValueError("source must include the actual generation page URL")
    expected = {key for key, clip in manifest["clips"].items() if clip["lang"].startswith("en")}
    supplied = set(batch["clips"])
    if len(expected) != 22 or not supplied or not supplied <= expected or (not allow_partial and supplied != expected):
        raise ValueError(f"Expected all 22 English clips; missing={sorted(expected - set(batch['clips']))}, extra={sorted(set(batch['clips']) - expected)}")
    manifest = copy.deepcopy(manifest)
    copies = []
    used_sources = set()
    for key in sorted(supplied):
        entry = batch["clips"][key]
        path = Path(entry["path"]).expanduser()
        if not path.is_absolute():
            path = mapping_path.parent / path
        path = path.resolve(strict=True)
        extension = path.suffix.lower()
        if extension not in (".wav", ".mp3", ".m4a", ".ogg", ".flac"):
            raise ValueError(f"Unsupported audio extension: {path}")
        if path in used_sources:
            raise ValueError(f"One file was assigned to more than one term: {path}")
        used_sources.add(path)
        original = manifest["clips"][key]
        if not isinstance(entry.get("input"), str) or entry["input"].strip().casefold().rstrip(".") != original["text"].casefold():
            raise ValueError(f"Input does not match the vocabulary term for {key}")
        inspection = inspect_audio(path)
        relative = Path("audio") / voice / f"{key}-{inspection['sha256'][:10]}{extension}"
        parameters = dict(batch["generationParameters"] or {})
        parameters.update(entry.get("generationParameters") or {})
        manifest["clips"][key] = {
            "text": original["text"], "voice": voice, "provider": "OpenAI",
            "model": entry.get("model", batch["model"]), "lang": original["lang"],
            "file": str(relative), "synthesized": True, "kind": original["kind"],
            "source": entry.get("source", batch["source"]),
            "generationParameters": {"input": entry["input"], **parameters},
            **inspection,
        }
        copies.append((path, PROJECT / "public" / relative))
    retained = {}
    for key, clip in manifest["clips"].items():
        if key in supplied:
            continue
        path = PROJECT / "public" / clip["file"]
        retained[key] = {"path": path, "sha256": digest(path), "lang": clip["lang"]}
        if clip.get("voice") in ("Samantha", "Tingting"):
            clip.setdefault("provider", "Apple")
            clip.setdefault("model", None)
            clip.setdefault("source", {"method": "macOS say", "note": "Retained original local speech synthesis"})
    voice_counts = {}
    for clip in manifest["clips"].values():
        name = f"{clip.get('provider', 'Unspecified')} / {clip['voice']}"
        voice_counts[name] = voice_counts.get(name, 0) + 1
    manifest.update({
        "version": 2, "generator": "Per-clip source metadata",
        "description": "Synthesized pronunciation study aids. See each clip for its actual provider and voice.",
        "voiceCounts": voice_counts,
        "failures": {},
    })
    return manifest, copies, retained


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path, help="JSON with metadata and every English clip path")
    parser.add_argument("--apply", action="store_true", help="Copy validated audio and update manifest")
    parser.add_argument("--allow-partial", action="store_true", help="Explicitly allow a subset, retaining all other clips")
    args = parser.parse_args()
    manifest, copies, retained = prepare(args.mapping.resolve(strict=True), args.allow_partial)
    if args.apply:
        for source, destination in copies:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        for key, entry in retained.items():
            if digest(entry["path"]) != entry["sha256"]:
                raise ValueError(f"Retained audio changed: {key}")
        temporary = MANIFEST.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(MANIFEST)
    print(json.dumps({
        "applied": args.apply, "validatedEnglish": len(copies),
        "retainedChinese": sum(entry["lang"].startswith("zh") for entry in retained.values()),
        "retainedEnglish": sum(entry["lang"].startswith("en") for entry in retained.values()),
        "voiceCounts": manifest["voiceCounts"],
        "totalEnglishBytes": sum(destination.stat().st_size if args.apply else source.stat().st_size for source, destination in copies),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
