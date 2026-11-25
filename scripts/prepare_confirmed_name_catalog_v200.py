"""Prepare full text for short name slots without changing script byte boundaries."""

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/confirmed_names_v200")


def prepare(image, *, smoke=False):
    preparation = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    backlog = json.loads(Path("work/analysis/confirmed_names_v198/allocation_backlog.json").read_text(encoding="utf-8"))
    drafts = {(r["file_path"], r["id"]): r for r in preparation["records"]}
    overrides = json.loads(Path("translations/confirmed_name_editorial_overrides_v1.json").read_text(encoding="utf-8"))
    for override in overrides["records"]:
        key = override["file_path"], override["id"]
        if key not in drafts:
            raise ValueError("Editorial override has no canonical source dossier")
        draft = drafts[key]
        if draft["source_hex"] != override["expected_source_hex"]:
            raise ValueError("Editorial override source lock changed")
        for field in ("english", "speaker", "context", "source_meaning", "localization_note", "review"):
            draft[field] = override[field]
    files, entries, records = {}, [], []
    for case in backlog["records"]:
        if case.get("research_allocation_solution_verified"):
            continue
        path, record_id = case["file_path"], case["id"]
        draft = drafts[path, record_id]
        if path not in files:
            files[path] = IlnkContainer.parse(image.read_file(path))
        block = int(record_id.split("_B")[1].split("_")[0])
        segment = int(record_id.split("_R")[1])
        current = files[path].blocks[block].split(b"\0")[segment]
        payload = dict(preparation["proposed_profiles_not_registered"][draft["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        encoded = encode_relocatable_dialogue(bytes.fromhex(draft["source_hex"]), draft["english"].removesuffix("{PAD}"), DialogueProfile(**payload)).encoded
        if not draft["english"].startswith("{SPEAKER:") or current[0] != encoded[0]:
            raise ValueError("Short-name catalog requires the exact already-mapped one-byte speaker state")
        record = {"file_path": path, "id": record_id, "speaker_byte": current[0],
                  "current_record_hex": current.hex(), "encoded_translation_hex": encoded.hex(),
                  "source_slot_bytes": len(current), "full_translation_bytes": len(encoded),
                  "english": draft["english"], "canonical_source_hex": draft["source_hex"],
                  "speaker": draft["speaker"], "context": draft["context"],
                  "source_meaning": draft["source_meaning"], "localization_note": draft["localization_note"],
                  "review": draft["review"], "proposed_profile": draft["proposed_profile"],
                  "translation_source": "Immutable canonical/clean Japanese and previously prepared source-reviewed name decisions; V190 bytes used only as exact runtime lookup keys."}
        records.append(record)
        # Both forms are guarded; the dispatcher normally receives text separately
        # from its actor selector. Whole-record matching preserves the selector too.
        for key, target, form in ((current, encoded, "whole"), (current[1:], encoded[1:], "body")):
            entries.append({"key_hex": key.hex(), "target_hex": target.hex(), "form": form, "owner": record_id})
    assert len(records) == 25
    if smoke:
        source = IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks[44].split(b"\0")[53]
        chosen = next(r for r in records if r["id"] == "DK4_MES_B76_R0012")
        target = bytes.fromhex(chosen["encoded_translation_hex"])[1:]
        for key, replacement in ((source, source[:1] + target), (source[1:], target)):
            entries.append({"key_hex": key.hex(), "target_hex": replacement.hex(), "form": "explicit-research-smoke-alias", "owner": "B44_R0053-smoke-only"})
    return entries, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    root = parser.parse_args().out
    root.mkdir(parents=True, exist_ok=True)
    source_path = Path("out/all_routes_combined_v190_candidate.nds")
    image = NdsImage.open(source_path)
    clean = NdsImage.open("work/clean.nds")
    for smoke in (False, True):
        entries, records = prepare(image, smoke=smoke)
        saved, plan = transform(image.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin"), entries)
        suffix = "smoke" if smoke else "catalog"
        (root / f"{suffix}_research_arm9.bin").write_bytes(saved)
        plan.update({"prepared_records": records, "entry_keys": entries,
                     "explicit_smoke_alias": smoke, "source_ROM_sha256": sha(source_path.read_bytes())})
        (root / f"{suffix}_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if smoke:
            probe = NdsImage.open(source_path)
            original = {p: bytes(data) for _, p, data in probe.iter_files()}
            arm7 = bytes(probe.rom.arm7)
            probe.replace_file("/__arm9__.bin", saved)
            output = root / "catalog_smoke_research_only.nds"
            probe.save(output)
            parsed = NdsImage.open(output)
            assert {p: bytes(data) for _, p, data in parsed.iter_files()} == original
            assert bytes(parsed.rom.arm7) == arm7
            plan.update({"research_ROM": output.as_posix(), "research_ROM_sha256": sha(output.read_bytes()),
                         "all_script_files_instruction_addresses_and_other_resources_exact": True,
                         "not_for_normal_gameplay_or_handoff": True})
            (root / "smoke_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"kind": suffix, "full_records": len(records), "unique_keys": len(plan["records"]),
                          "pool_bytes": plan["pool_payload_bytes"], "helper_bytes": plan["helper_bytes"], "research_only": True}))


if __name__ == "__main__":
    main()
