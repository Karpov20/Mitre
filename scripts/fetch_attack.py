#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


CTI_URLS: Dict[str, str] = {
    "enterprise": "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
    "mobile": "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json",
    "ics": "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json",
}

KILL_CHAIN_BY_DOMAIN: Dict[str, List[str]] = {
    "enterprise": ["mitre-attack"],
    "mobile": ["mitre-mobile-attack"],
    "ics": ["mitre-ics-attack"],
}


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _download_json(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "attack-ru-site/1.0"})
    with urllib.request.urlopen(req) as resp:
        payload = resp.read()
    return json.loads(payload.decode("utf-8"))


def _write_json(path: Path, data: Any) -> None:
    _mkdir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _external_id_and_url(stix_obj: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    refs = stix_obj.get("external_references") or []
    for ref in refs:
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id"), ref.get("url")
    return None, None


def _is_active(stix_obj: Dict[str, Any]) -> bool:
    if stix_obj.get("revoked") is True:
        return False
    if stix_obj.get("x_mitre_deprecated") is True:
        return False
    return True


@dataclass(frozen=True)
class Tactic:
    id: str
    stix_id: str
    name: str
    description: str
    shortname: str
    order: int
    url: Optional[str]


@dataclass(frozen=True)
class Technique:
    id: str
    stix_id: str
    name: str
    description: str
    url: Optional[str]
    is_subtechnique: bool
    parent_id: Optional[str]
    tactics: List[str]
    platforms: List[str]
    detection: str


@dataclass(frozen=True)
class Group:
    id: str
    stix_id: str
    name: str
    description: str
    url: Optional[str]
    aliases: List[str]


@dataclass(frozen=True)
class Software:
    id: str
    stix_id: str
    name: str
    description: str
    url: Optional[str]
    software_type: str
    aliases: List[str]
    platforms: List[str]


@dataclass(frozen=True)
class Mitigation:
    id: str
    stix_id: str
    name: str
    description: str
    url: Optional[str]


def _string_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return []


def _unique_list(values: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for v in values:
        if v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def _parse_tactics(objects: Iterable[Dict[str, Any]]) -> List[Tactic]:
    tactics: List[Tactic] = []
    for obj in objects:
        if obj.get("type") != "x-mitre-tactic":
            continue
        if not _is_active(obj):
            continue
        external_id, url = _external_id_and_url(obj)
        if not external_id:
            continue
        tactics.append(
            Tactic(
                id=external_id,
                stix_id=obj.get("id", ""),
                name=(obj.get("name") or "").strip(),
                description=(obj.get("description") or "").strip(),
                shortname=(obj.get("x_mitre_shortname") or "").strip(),
                order=int(obj.get("x_mitre_order") or 0),
                url=url,
            )
        )
    tactics.sort(key=lambda t: (t.order, t.id))
    return tactics


def _parse_groups(objects: Iterable[Dict[str, Any]]) -> List[Group]:
    groups: List[Group] = []
    for obj in objects:
        if obj.get("type") != "intrusion-set":
            continue
        if not _is_active(obj):
            continue
        external_id, url = _external_id_and_url(obj)
        if not external_id:
            continue
        groups.append(
            Group(
                id=external_id,
                stix_id=obj.get("id", ""),
                name=(obj.get("name") or "").strip(),
                description=(obj.get("description") or "").strip(),
                url=url,
                aliases=_unique_list(_string_list(obj.get("aliases"))),
            )
        )
    groups.sort(key=lambda g: (g.id, g.name))
    return groups


def _parse_software(objects: Iterable[Dict[str, Any]]) -> List[Software]:
    software: List[Software] = []
    for obj in objects:
        stix_type = obj.get("type")
        if stix_type not in ("malware", "tool"):
            continue
        if not _is_active(obj):
            continue
        external_id, url = _external_id_and_url(obj)
        if not external_id:
            continue
        aliases = _unique_list(_string_list(obj.get("x_mitre_aliases")) + _string_list(obj.get("aliases")))
        software.append(
            Software(
                id=external_id,
                stix_id=obj.get("id", ""),
                name=(obj.get("name") or "").strip(),
                description=(obj.get("description") or "").strip(),
                url=url,
                software_type=str(stix_type),
                aliases=aliases,
                platforms=_string_list(obj.get("x_mitre_platforms")),
            )
        )
    software.sort(key=lambda s: (s.id, s.name))
    return software


def _parse_mitigations(objects: Iterable[Dict[str, Any]]) -> List[Mitigation]:
    mitigations: List[Mitigation] = []
    for obj in objects:
        if obj.get("type") != "course-of-action":
            continue
        if not _is_active(obj):
            continue
        external_id, url = _external_id_and_url(obj)
        if not external_id:
            continue
        mitigations.append(
            Mitigation(
                id=external_id,
                stix_id=obj.get("id", ""),
                name=(obj.get("name") or "").strip(),
                description=(obj.get("description") or "").strip(),
                url=url,
            )
        )
    mitigations.sort(key=lambda m: (m.id, m.name))
    return mitigations


def _parse_subtechnique_rels(objects: Iterable[Dict[str, Any]]) -> Dict[str, str]:
    sub_to_parent: Dict[str, str] = {}
    for obj in objects:
        if obj.get("type") != "relationship":
            continue
        if not _is_active(obj):
            continue
        if obj.get("relationship_type") != "subtechnique-of":
            continue
        source_ref = obj.get("source_ref")
        target_ref = obj.get("target_ref")
        if isinstance(source_ref, str) and isinstance(target_ref, str):
            sub_to_parent[source_ref] = target_ref
    return sub_to_parent


def _kill_chain_phases(obj: Dict[str, Any], kill_chain_names: Iterable[str]) -> List[str]:
    allowed = set(kill_chain_names)
    phases = obj.get("kill_chain_phases") or []
    out: List[str] = []
    for ph in phases:
        if ph.get("kill_chain_name") not in allowed:
            continue
        phase_name = (ph.get("phase_name") or "").strip()
        if phase_name:
            out.append(phase_name)
    return out


def _parse_techniques(
    objects: Iterable[Dict[str, Any]],
    tactic_shortname_to_id: Dict[str, str],
    stix_id_to_external_id: Dict[str, str],
    sub_to_parent_stix: Dict[str, str],
    kill_chain_names: Iterable[str],
) -> List[Technique]:
    techniques: List[Technique] = []
    for obj in objects:
        if obj.get("type") != "attack-pattern":
            continue
        if not _is_active(obj):
            continue

        external_id, url = _external_id_and_url(obj)
        if not external_id:
            continue

        stix_id = obj.get("id", "")
        is_sub = bool(obj.get("x_mitre_is_subtechnique") is True)

        parent_id: Optional[str] = None
        if is_sub:
            parent_stix = sub_to_parent_stix.get(stix_id)
            if parent_stix:
                parent_id = stix_id_to_external_id.get(parent_stix)

        phase_shortnames = _kill_chain_phases(obj, kill_chain_names)
        tactic_ids = []
        for sn in phase_shortnames:
            tid = tactic_shortname_to_id.get(sn)
            if tid and tid not in tactic_ids:
                tactic_ids.append(tid)

        techniques.append(
            Technique(
                id=external_id,
                stix_id=stix_id,
                name=(obj.get("name") or "").strip(),
                description=(obj.get("description") or "").strip(),
                url=url,
                is_subtechnique=is_sub,
                parent_id=parent_id,
                tactics=tactic_ids,
                platforms=list(obj.get("x_mitre_platforms") or []),
                detection=(obj.get("x_mitre_detection") or "").strip(),
            )
        )
    techniques.sort(key=lambda t: (t.id, t.name))
    return techniques


def _build_matrix(
    tactics: List[Tactic], techniques: List[Technique]
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    matrix: Dict[str, List[str]] = {t.id: [] for t in tactics}
    subtechniques: Dict[str, List[str]] = {}

    for tech in techniques:
        if tech.is_subtechnique and tech.parent_id:
            subtechniques.setdefault(tech.parent_id, []).append(tech.id)
            continue
        for tactic_id in tech.tactics:
            matrix.setdefault(tactic_id, []).append(tech.id)

    for tactic_id, ids in matrix.items():
        ids.sort()
        matrix[tactic_id] = ids

    for parent_id, ids in subtechniques.items():
        ids.sort()
        subtechniques[parent_id] = ids

    return matrix, subtechniques


def _extract_stix_external_ids(objects: Iterable[Dict[str, Any]]) -> Dict[str, str]:
    stix_to_external: Dict[str, str] = {}
    for obj in objects:
        if obj.get("type") in (
            "attack-pattern",
            "x-mitre-tactic",
            "intrusion-set",
            "malware",
            "tool",
            "course-of-action",
        ):
            external_id, _ = _external_id_and_url(obj)
            if external_id and isinstance(obj.get("id"), str):
                stix_to_external[obj["id"]] = external_id
    return stix_to_external


def _add_link(links: Dict[str, Dict[str, set]], key: str, src: str, dst: str) -> None:
    links.setdefault(key, {}).setdefault(src, set()).add(dst)


def _links_to_lists(links: Dict[str, Dict[str, set]]) -> Dict[str, Dict[str, List[str]]]:
    out: Dict[str, Dict[str, List[str]]] = {}
    for rel_name, mapping in links.items():
        out[rel_name] = {k: sorted(v) for k, v in mapping.items()}
    return out


def _parse_links(objects: Iterable[Dict[str, Any]], stix_id_to_external_id: Dict[str, str]) -> Dict[str, Any]:
    links: Dict[str, Dict[str, set]] = {}

    for obj in objects:
        if obj.get("type") != "relationship":
            continue
        if not _is_active(obj):
            continue
        rel_type = obj.get("relationship_type")
        if rel_type not in ("uses", "mitigates"):
            continue
        source_ref = obj.get("source_ref")
        target_ref = obj.get("target_ref")
        if not isinstance(source_ref, str) or not isinstance(target_ref, str):
            continue
        src = stix_id_to_external_id.get(source_ref)
        dst = stix_id_to_external_id.get(target_ref)
        if not src or not dst:
            continue

        if rel_type == "uses":
            if src.startswith("G") and dst.startswith("T"):
                _add_link(links, "group_techniques", src, dst)
            elif src.startswith("G") and dst.startswith("S"):
                _add_link(links, "group_software", src, dst)
            elif src.startswith("S") and dst.startswith("T"):
                _add_link(links, "software_techniques", src, dst)
        elif rel_type == "mitigates":
            if src.startswith("M") and dst.startswith("T"):
                _add_link(links, "mitigation_techniques", src, dst)

    # Reverse indexes for detail pages.
    for group_id, technique_ids in links.get("group_techniques", {}).items():
        for technique_id in technique_ids:
            _add_link(links, "technique_groups", technique_id, group_id)

    for group_id, software_ids in links.get("group_software", {}).items():
        for software_id in software_ids:
            _add_link(links, "software_groups", software_id, group_id)

    for software_id, technique_ids in links.get("software_techniques", {}).items():
        for technique_id in technique_ids:
            _add_link(links, "technique_software", technique_id, software_id)

    for mitigation_id, technique_ids in links.get("mitigation_techniques", {}).items():
        for technique_id in technique_ids:
            _add_link(links, "technique_mitigations", technique_id, mitigation_id)

    return _links_to_lists(links)


def _build_output(domain: str, stix: Dict[str, Any], source_url: str) -> Dict[str, Any]:
    objects = stix.get("objects") or []
    stix_id_to_external_id = _extract_stix_external_ids(objects)
    tactics = _parse_tactics(objects)
    tactic_shortname_to_id = {t.shortname: t.id for t in tactics if t.shortname}
    sub_to_parent_stix = _parse_subtechnique_rels(objects)
    groups = _parse_groups(objects)
    software = _parse_software(objects)
    mitigations = _parse_mitigations(objects)
    kill_chain_names = KILL_CHAIN_BY_DOMAIN.get(domain, ["mitre-attack"])
    techniques = _parse_techniques(
        objects=objects,
        tactic_shortname_to_id=tactic_shortname_to_id,
        stix_id_to_external_id=stix_id_to_external_id,
        sub_to_parent_stix=sub_to_parent_stix,
        kill_chain_names=kill_chain_names,
    )
    matrix, subtechniques = _build_matrix(tactics, techniques)
    links = _parse_links(objects, stix_id_to_external_id)

    return {
        "meta": {
            "domain": domain,
            "generated_at": _utc_now_iso(),
            "source_url": source_url,
            "stix_spec_version": stix.get("spec_version"),
        },
        "tactics": [
            {
                "id": t.id,
                "stix_id": t.stix_id,
                "name": t.name,
                "description": t.description,
                "shortname": t.shortname,
                "order": t.order,
                "url": t.url,
            }
            for t in tactics
        ],
        "techniques": [
            {
                "id": tech.id,
                "stix_id": tech.stix_id,
                "name": tech.name,
                "description": tech.description,
                "url": tech.url,
                "is_subtechnique": tech.is_subtechnique,
                "parent_id": tech.parent_id,
                "tactics": tech.tactics,
                "platforms": tech.platforms,
                "detection": tech.detection,
            }
            for tech in techniques
        ],
        "matrix": matrix,
        "subtechniques": subtechniques,
        "groups": [
            {
                "id": g.id,
                "stix_id": g.stix_id,
                "name": g.name,
                "description": g.description,
                "url": g.url,
                "aliases": g.aliases,
            }
            for g in groups
        ],
        "software": [
            {
                "id": s.id,
                "stix_id": s.stix_id,
                "name": s.name,
                "description": s.description,
                "url": s.url,
                "type": s.software_type,
                "aliases": s.aliases,
                "platforms": s.platforms,
            }
            for s in software
        ],
        "mitigations": [
            {
                "id": m.id,
                "stix_id": m.stix_id,
                "name": m.name,
                "description": m.description,
                "url": m.url,
            }
            for m in mitigations
        ],
        "links": links,
    }


def _domains_from_arg(arg: str) -> List[str]:
    if arg == "all":
        return list(CTI_URLS.keys())
    if arg not in CTI_URLS:
        raise ValueError(f"Unknown domain: {arg}")
    return [arg]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch and simplify MITRE ATT&CK STIX JSON for the static site.")
    parser.add_argument("--domain", default="enterprise", help="enterprise|mobile|ics|all")
    parser.add_argument("--raw-dir", default="data/raw", help="Where to store downloaded raw STIX JSON")
    parser.add_argument("--out-dir", default="site/data", help="Where to write simplified JSON for the site")
    args = parser.parse_args(argv)

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)

    for domain in _domains_from_arg(args.domain):
        url = CTI_URLS[domain]
        print(f"[{domain}] download {url}")
        stix = _download_json(url)
        raw_path = raw_dir / f"{domain}.stix.json"
        _write_json(raw_path, stix)

        out_path = out_dir / f"{domain}.json"
        simplified = _build_output(domain=domain, stix=stix, source_url=url)
        _write_json(out_path, simplified)
        print(f"[{domain}] wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
