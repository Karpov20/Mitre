#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional


SUPPORTED_DOMAINS = ("enterprise", "mobile", "ics")
MAX_CHARS = 4500

# Silence macOS LibreSSL warning from urllib3 (doesn't affect our use-case).
warnings.filterwarnings("ignore", message=r"urllib3 v2 only supports OpenSSL.*")


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _autosave(domain: str, out_path: Path, patch: Dict[str, Any], translated_objects: int) -> None:
    _write_json(out_path, patch)
    print(f"[{domain}] autosave {out_path} (+{translated_objects})")


def _domains_from_arg(arg: str) -> List[str]:
    if arg == "all":
        return list(SUPPORTED_DOMAINS)
    if arg not in SUPPORTED_DOMAINS:
        raise ValueError(f"Unknown domain: {arg}")
    return [arg]


def _build_translator() -> Any:
    try:
        from deep_translator import GoogleTranslator  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Не найден пакет deep-translator. Установите: python3 -m pip install deep-translator"
        ) from e
    return GoogleTranslator(source="en", target="ru")


def _sleep(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


def _translate_chunk(tr: Any, text: str, sleep_sec: float) -> str:
    for attempt in range(3):
        try:
            out = tr.translate(text)
            _sleep(sleep_sec)
            return out
        except Exception:
            if attempt == 2:
                raise
            _sleep(1.5 + attempt)


def _split_long_line(line: str) -> List[str]:
    if len(line) <= MAX_CHARS:
        return [line]
    sentences = re.split(r"(?<=[.!?])\\s+", line)
    chunks: List[str] = []
    current = ""
    for s in sentences:
        if not s:
            continue
        if len(s) > MAX_CHARS:
            if current:
                chunks.append(current)
                current = ""
            for i in range(0, len(s), MAX_CHARS):
                chunks.append(s[i : i + MAX_CHARS])
            continue
        if len(current) + len(s) + 1 > MAX_CHARS:
            if current:
                chunks.append(current)
            current = s
        else:
            current = f"{current} {s}".strip()
    if current:
        chunks.append(current)
    return chunks


def _translate_text(tr: Any, text: str, sleep_sec: float) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    paragraphs = text.split("\n\n")
    out_paragraphs: List[str] = []
    for para in paragraphs:
        if not para.strip():
            out_paragraphs.append("")
            continue
        if len(para) <= MAX_CHARS:
            out_paragraphs.append(_translate_chunk(tr, para, sleep_sec))
            continue
        if "\n" in para:
            lines = para.split("\n")
            translated_lines = []
            for line in lines:
                if not line.strip():
                    translated_lines.append("")
                    continue
                line_chunks = _split_long_line(line)
                translated_line = " ".join(_translate_chunk(tr, c, sleep_sec) for c in line_chunks)
                translated_lines.append(translated_line)
            out_paragraphs.append("\n".join(translated_lines))
        else:
            line_chunks = _split_long_line(para)
            out_paragraphs.append(" ".join(_translate_chunk(tr, c, sleep_sec) for c in line_chunks))
    return "\n\n".join(out_paragraphs)


def _maybe_translate(tr: Any, text: str, sleep_sec: float) -> Optional[str]:
    txt = (text or "").strip()
    if not txt:
        return None
    return _translate_text(tr, txt, sleep_sec)


def _init_or_resume_patch(existing: Optional[Dict[str, Any]], domain: str) -> Dict[str, Any]:
    patch: Dict[str, Any] = existing if isinstance(existing, dict) else {}
    patch.setdefault("tactics", {})
    patch.setdefault("techniques", {})
    patch.setdefault("groups", {})
    patch.setdefault("software", {})
    patch.setdefault("mitigations", {})
    patch["meta"] = {
        "language": "ru",
        "domain": domain,
        "generated_at": _utc_now_iso(),
        "generator": "google translate (deep-translator)",
        "note": "Это неофициальный машинный перевод. Возможны неточности.",
    }
    return patch


def _build_ru_patch(
    *,
    base: Dict[str, Any],
    domain: str,
    tr: Any,
    existing: Optional[Dict[str, Any]] = None,
    max_items: Optional[int],
    save_every: int,
    out_path: Path,
    sleep_sec: float,
) -> Dict[str, Any]:
    tactics = base.get("tactics") or []
    techniques = base.get("techniques") or []
    groups = base.get("groups") or []
    software = base.get("software") or []
    mitigations = base.get("mitigations") or []

    patch = _init_or_resume_patch(existing=existing, domain=domain)
    translated_objects = 0

    for t in tactics:
        tid = t.get("id")
        if not tid:
            continue
        existing_t = patch["tactics"].get(tid)
        if isinstance(existing_t, dict) and isinstance(existing_t.get("name"), str) and isinstance(
            existing_t.get("description"), str
        ):
            continue

        patch["tactics"][tid] = {
            "name": _translate_text(tr, t.get("name") or "", sleep_sec),
            "description": _translate_text(tr, t.get("description") or "", sleep_sec),
        }

        translated_objects += 1
        if save_every and translated_objects % save_every == 0:
            _autosave(domain, out_path, patch, translated_objects)
        if max_items and translated_objects >= max_items:
            return patch

    for tech in techniques:
        tech_id = tech.get("id")
        if not tech_id:
            continue

        existing_tech = patch["techniques"].get(tech_id)
        if not isinstance(existing_tech, dict):
            existing_tech = {}

        changed = False
        if not isinstance(existing_tech.get("name"), str) or not existing_tech.get("name"):
            existing_tech["name"] = _translate_text(tr, tech.get("name") or "", sleep_sec)
            changed = True
        if not isinstance(existing_tech.get("description"), str) or not existing_tech.get("description"):
            existing_tech["description"] = _translate_text(tr, tech.get("description") or "", sleep_sec)
            changed = True
        if "detection" not in existing_tech:
            det = _maybe_translate(tr, tech.get("detection") or "", sleep_sec)
            if det:
                existing_tech["detection"] = det
                changed = True

        if changed:
            patch["techniques"][tech_id] = existing_tech
            translated_objects += 1
            if save_every and translated_objects % save_every == 0:
                _autosave(domain, out_path, patch, translated_objects)
            if max_items and translated_objects >= max_items:
                return patch

    for g in groups:
        gid = g.get("id")
        if not gid:
            continue
        existing_g = patch["groups"].get(gid)
        if isinstance(existing_g, dict) and isinstance(existing_g.get("name"), str) and isinstance(
            existing_g.get("description"), str
        ):
            continue
        patch["groups"][gid] = {
            "name": _translate_text(tr, g.get("name") or "", sleep_sec),
            "description": _translate_text(tr, g.get("description") or "", sleep_sec),
        }
        translated_objects += 1
        if save_every and translated_objects % save_every == 0:
            _autosave(domain, out_path, patch, translated_objects)
        if max_items and translated_objects >= max_items:
            return patch

    for sw in software:
        sid = sw.get("id")
        if not sid:
            continue
        existing_sw = patch["software"].get(sid)
        if isinstance(existing_sw, dict) and isinstance(existing_sw.get("name"), str) and isinstance(
            existing_sw.get("description"), str
        ):
            continue
        patch["software"][sid] = {
            "name": _translate_text(tr, sw.get("name") or "", sleep_sec),
            "description": _translate_text(tr, sw.get("description") or "", sleep_sec),
        }
        translated_objects += 1
        if save_every and translated_objects % save_every == 0:
            _autosave(domain, out_path, patch, translated_objects)
        if max_items and translated_objects >= max_items:
            return patch

    for m in mitigations:
        mid = m.get("id")
        if not mid:
            continue
        existing_m = patch["mitigations"].get(mid)
        if isinstance(existing_m, dict) and isinstance(existing_m.get("name"), str) and isinstance(
            existing_m.get("description"), str
        ):
            continue
        patch["mitigations"][mid] = {
            "name": _translate_text(tr, m.get("name") or "", sleep_sec),
            "description": _translate_text(tr, m.get("description") or "", sleep_sec),
        }
        translated_objects += 1
        if save_every and translated_objects % save_every == 0:
            _autosave(domain, out_path, patch, translated_objects)
        if max_items and translated_objects >= max_items:
            return patch

    return patch


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate Russian translation patch files for the static ATT&CK site.")
    parser.add_argument("--domain", default="enterprise", help="enterprise|mobile|ics|all")
    parser.add_argument("--in-dir", default="site/data", help="Directory with <domain>.json files")
    parser.add_argument("--out-dir", default="site/data", help="Directory to write <domain>.ru.json files")
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Resume existing <domain>.ru.json file if present (default: true)",
    )
    parser.add_argument(
        "--save-every",
        type=int,
        default=25,
        help="Write output patch file every N translated objects (default: 25)",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Delay between translation requests in seconds (default: 0)",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Limit number of translated objects (useful for quick test runs)",
    )
    args = parser.parse_args(argv)

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)

    tr = _build_translator()

    for domain in _domains_from_arg(args.domain):
        base_path = in_dir / f"{domain}.json"
        if not base_path.exists():
            raise RuntimeError(f"Не найден файл {base_path}. Сначала запустите scripts/fetch_attack.py")
        base = _read_json(base_path)
        out_path = out_dir / f"{domain}.ru.json"
        existing = _read_json(out_path) if args.resume and out_path.exists() else None
        patch = _build_ru_patch(
            base=base,
            domain=domain,
            tr=tr,
            existing=existing,
            max_items=args.max_items,
            save_every=args.save_every,
            out_path=out_path,
            sleep_sec=args.sleep,
        )
        _write_json(out_path, patch)
        print(f"[{domain}] wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
