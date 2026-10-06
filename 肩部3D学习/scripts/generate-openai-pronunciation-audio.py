#!/usr/bin/env python3
"""Complete a Marin pronunciation batch, reusing verified existing downloads.

Default is a local plan only. --generate reads OPENAI_API_KEY from the process
environment and calls the official speech endpoint for missing English terms.
It saves a resumable mapping after each successful clip; it does not publish
audio to the application. Then use import-openai-pronunciation-audio.py.

API schema: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


PROJECT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.openai.com/v1/audio/speech"
MODEL = "gpt-4o-mini-tts"
VOICE = "marin"
INSTRUCTIONS = (
    "Read the supplied anatomical term once, clearly and naturally in American English, "
    "as a pronunciation example for a student. Use accurate anatomical pronunciation "
    "and stress, a neutral conversational tone, and a comfortable pace. Say only the "
    "supplied term. No introduction, explanation, spelling, or added words."
)

# Share the same complete-set, text and non-silence checks used by the importer.
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("pronunciation_import", Path(__file__).with_name("import-openai-pronunciation-audio.py"))
audio_import = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_import)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("Speech endpoint redirected; no credentials were forwarded")


def save_mapping(path: Path, batch: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_entries(path: Path) -> dict:
    audio_import.prepare(path, allow_partial=True)
    batch = json.loads(path.read_text(encoding="utf-8"))
    if batch["voice"] != VOICE:
        raise ValueError("Existing clips must use Marin to join this batch")
    entries = {}
    for key, entry in batch["clips"].items():
        local = Path(entry["path"]).expanduser()
        if not local.is_absolute():
            local = path.parent / local
        parameters = dict(batch.get("generationParameters") or {})
        parameters.update(entry.get("generationParameters") or {})
        entries[key] = {
            **entry, "path": str(local.resolve(strict=True)),
            "model": entry.get("model", batch["model"]),
            "source": entry.get("source", batch["source"]),
            "generationParameters": parameters,
        }
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse", type=Path, required=True, help="Mapping of existing verified OpenAI clips")
    parser.add_argument("--output", type=Path, default=PROJECT / ".voice-staging" / "marin-complete.json")
    parser.add_argument("--generate", action="store_true", help="Generate missing clips using OPENAI_API_KEY")
    args = parser.parse_args()

    # Fail before reading or writing audio when an actual generation lacks a key.
    api_key = os.environ.get("OPENAI_API_KEY", "").strip() if args.generate else ""
    if args.generate and not api_key:
        print("未设置 OPENAI_API_KEY，未发起任何请求。请在本机运行环境中配置密钥后重试；不要把密钥放进网页、映射文件或聊天。", file=sys.stderr)
        return 2

    reuse_path = args.reuse.resolve(strict=True)
    output_path = args.output.resolve()
    if output_path == reuse_path:
        raise ValueError("--output must differ from --reuse so original UI provenance remains available")
    entries = load_entries(reuse_path)
    if output_path.exists():
        for key, entry in load_entries(output_path).items():
            if key in entries and audio_import.digest(Path(entries[key]["path"])) != audio_import.digest(Path(entry["path"])):
                raise ValueError(f"Resume mapping conflicts with an existing download: {key}")
            entries.setdefault(key, entry)
    manifest = json.loads(audio_import.MANIFEST.read_text(encoding="utf-8"))
    terms = {key: clip["text"] for key, clip in manifest["clips"].items() if clip["lang"].startswith("en")}
    if len(terms) != 22 or not set(entries) <= set(terms):
        raise ValueError("The batch must refer only to the 22 current English vocabulary IDs")
    missing = [key for key in terms if key not in entries]
    print(json.dumps({"mode": "generate" if args.generate else "plan", "reuse": len(entries), "missing": len(missing), "terms": {key: terms[key] for key in missing}, "model": MODEL, "voice": VOICE}, ensure_ascii=False), flush=True)
    if not args.generate:
        return 0

    parameters = {"instructions": INSTRUCTIONS, "response_format": "wav", "speed": 1.0}
    batch = {
        "provider": "OpenAI", "voice": VOICE, "model": MODEL,
        "source": {"url": ENDPOINT, "method": "OpenAI speech API"},
        "generationParameters": parameters, "clips": entries,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    opener = build_opener(NoRedirect())
    for key in missing:
        payload = {"model": MODEL, "voice": VOICE, "input": terms[key], **parameters}
        request = Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}, method="POST")
        try:
            with opener.open(request, timeout=60) as response:
                content = response.read(5 * 1024 * 1024 + 1)
        except HTTPError as error:
            # Do not print response bodies or request headers: an auth error may
            # echo credentials. No automatic retry, avoiding duplicate charges.
            raise RuntimeError(f"OpenAI speech API returned HTTP {error.code} for {key}; completed clips remain saved") from None
        except URLError:
            raise RuntimeError(f"Could not reach the OpenAI speech API for {key}; completed clips remain saved") from None
        if not content.startswith((b"RIFF", b"RF64")) or len(content) > 5 * 1024 * 1024:
            raise ValueError(f"Unexpected WAV response for {key}; no application files were changed")
        filename = f"{key}-{hashlib.sha256(content).hexdigest()[:10]}.wav"
        destination = output_path.parent / filename
        destination.write_bytes(content)
        inspection = audio_import.inspect_audio(destination)
        batch["clips"][key] = {
            "path": str(destination), "input": terms[key], "model": MODEL,
            "source": {"url": ENDPOINT, "method": "OpenAI speech API", "generated_at": datetime.now(timezone.utc).isoformat()},
            "generationParameters": parameters, "sha256": inspection["sha256"],
        }
        save_mapping(output_path, batch)
        print(json.dumps({"generated": key, "duration": inspection["duration"], "complete": len(batch["clips"]), "total": 22}, ensure_ascii=False), flush=True)
    if not missing:
        save_mapping(output_path, batch)
    audio_import.prepare(output_path)
    print(json.dumps({"readyToImport": str(output_path), "clips": len(batch["clips"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
