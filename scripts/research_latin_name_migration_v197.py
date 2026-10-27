"""Verify source owners and evaluate Latin-name dialogue migration before release."""

import copy
import json
import re
import struct
from collections import Counter
from dataclasses import replace
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.verify_ordinary_name_fidelity_research import initialized

NAMES = {"Raphael": "Rafael", "Hodram": "Hoodlum", "Kamil": "Camille"}
OWNERS = [(0, 0x15CA40, 12, "ラファエル", "Raphael", "Rafael"),
          (1, 0x15C134, 12, "ホドラム", "Hodram", "Hoodlum"),
          (9, 0x15BF08, 8, "カミル", "Kamil", "Camille")]


def revised_profile(profile, file_path):
    lengths, widths = dict(profile.macro_ascii_lengths), dict(profile.macro_widths)
    if file_path == "/data/SC0.DK4":
        assert lengths["FI"] == 7
        lengths["FI"], widths["FI"] = 6, 36
        if "FU" in lengths:
            assert lengths["FU"] == 14
            lengths["FU"], widths["FU"] = 13, 78
    elif file_path == "/data/SC1.DK4":
        assert lengths["FI"] == 6
        lengths["FI"], widths["FI"] = 7, 42
    return replace(profile, macro_ascii_lengths=lengths, macro_widths=widths)


def rename(text):
    return re.sub(r"\b(?:Raphael|Hodram|Kamil)\b", lambda match: NAMES[match[0]], text)


def main():
    root = Path("work/analysis/latin_name_migration_v197")
    root.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    japanese = NdsImage.open("work/clean.nds")
    raw = current.read_file("/__arm9__.bin")
    clean = japanese.read_file("/__arm9__.bin")
    assert sha(raw) == "9c03e253a6e91231a7e6d7ee112c07c632a3cfe16b2a33d2d349cc1e45857958"
    result, owners = bytearray(raw), []
    for index, offset, capacity, jp, before, after in OWNERS:
        field = 0x120B80 + index * 32
        pointer = 0x02000000 + offset
        assert struct.unpack_from("<I", raw, field)[0] == pointer
        assert struct.unpack_from("<I", clean, field)[0] == pointer
        assert raw[offset:offset + capacity] == (before.encode() + b"\0").ljust(capacity, b"\0")
        assert clean[offset:offset + capacity] == (jp.encode("cp932") + b"\0").ljust(capacity, b"\0")
        assert len(after) + 1 <= capacity
        references = [at for at in range(len(raw) - 3)
                      if raw[at:at + 4] == struct.pack("<I", pointer)]
        assert references == [field]
        result[offset:offset + capacity] = (after.encode() + b"\0").ljust(capacity, b"\0")
        owners.append({"index": index, "offset": offset, "capacity": capacity,
                       "pointer": pointer, "references": references, "japanese": jp,
                       "before": before, "after": after})
    saved = bytes(result)
    old_sections, new_sections = MainCodeFile(raw, 0x02000000), MainCodeFile(saved, 0x02000000)
    assert len(old_sections.sections) == len(new_sections.sections)
    assert all(bytes(a.data) == bytes(b.data) for a, b in
               zip(old_sections.sections[1:], new_sections.sections[1:], strict=True))
    allowed = {at for _, start, capacity, *_ in OWNERS for at in range(start, start + capacity)}
    assert {at for at, (a, b) in enumerate(zip(raw, saved, strict=True)) if a != b} <= allowed
    (root / "three_given_names_research_only_arm9.bin").write_bytes(saved)
    before_machine, after_machine = initialized(raw), initialized(saved)
    expected, getters = {r[0]: r[-1] for r in OWNERS}, []
    for index in range(207):
        before_pointer = ordinary_getter(raw, index, before_machine)
        after_pointer = ordinary_getter(saved, index, after_machine)
        before = bytes(before_machine.mem_read(before_pointer, 128)).split(b"\0", 1)[0].decode("cp932")
        after = bytes(after_machine.mem_read(after_pointer, 128)).split(b"\0", 1)[0].decode("cp932")
        assert before_pointer == after_pointer
        assert after == expected.get(index, before)
        getters.append({"index": index, "pointer": after_pointer, "before": before, "after": after})
    registry = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    profile = registry["profiles"]["all-routes-unified-v190"]
    batches, effective = {}, {}
    for path in profile["batches"]:
        batch = json.loads(Path(path).read_text(encoding="utf-8"))
        batches[path] = batch
        for record in batch.get("records", []):
            if isinstance(record.get("english"), str):
                effective[batch.get("file_path"), record["id"]] = (path, record)
    sources, clean_rows = {}, {}
    checks, proposals = [], []
    for (file_path, record_id), (batch_path, original) in sorted(effective.items()):
        batch = batches[batch_path]
        old = original["english"]
        new = rename(old)
        macro_affected = (file_path == "/data/SC0.DK4" and any(m in old for m in ("{MACRO:FI}", "{MACRO:FU}"))) or (
            file_path == "/data/SC1.DK4" and "{MACRO:FI}" in old)
        if old == new and not macro_affected:
            continue
        if file_path not in sources:
            source = canonical.read_file(file_path)
            sources[file_path] = {row["id"]: row for row in export_mesfile_rows(source, file_path, include_non_japanese=True)}
            clean_rows[file_path] = {row["id"]: row for row in export_mesfile_rows(japanese.read_file(file_path), file_path, include_non_japanese=True)}
        assert sha(canonical.read_file(file_path)) == batch["source_file_sha256"]
        source_row = sources[file_path][record_id]
        record = copy.deepcopy(original)
        record["english"] = new
        record["original_batch"] = batch_path
        record["original_english"] = old
        record["source_hex"] = source_row["source_hex"]
        record["japanese_source"] = clean_rows[file_path].get(record_id, {}).get("japanese")
        record["file_path"] = file_path
        record["status"] = "research-draft-not-registered"
        for field in ("speaker", "context", "source_meaning", "localization_note"):
            if isinstance(record.get(field), str):
                record[field] = rename(record[field])
        check = {"file_path": file_path, "id": record_id, "batch": batch_path,
                 "literal_name_changed": old != new, "default_macro_changed": bool(macro_affected)}
        if batch.get("encoder") == "dialogue-fixed-v1":
            old_profile = get_dialogue_profile(batch["dialogue_profile"])
            new_profile = revised_profile(old_profile, file_path)
            raw_source = bytes.fromhex(source_row["source_hex"])
            before_qa = audit_fixed_dialogue_record(raw_source, old, old_profile)
            after_qa = audit_fixed_dialogue_record(raw_source, new, new_profile)
            check.update({"profile": old_profile.name, "proposed_macro_ascii_lengths": new_profile.macro_ascii_lengths,
                          "before": before_qa, "after": after_qa,
                          "new_encoding_errors": [i for i in after_qa["issues"] if i["severity"] == "error"],
                          "encoded_layout_changes": before_qa["formatted_markup"] != after_qa["formatted_markup"]})
        else:
            check["requires_native_common_or_relocation_review"] = True
        record["review"] = {"source": False, "context": False, "localization": False,
                            "naturalness": False, "formatting": False}
        # A generated draft is not an inherited editorial approval or a build batch.
        proposals.append(record)
        checks.append(check)
    (root / "source_locked_record_drafts.json").write_text(json.dumps({
        "format": "dk4-original-latin-name-migration-research-drafts-v1",
        "not_a_release_batch": True, "records": proposals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"format": "dk4-original-latin-name-migration-research-v1",
              "source_arm9_sha256": sha(raw), "research_arm9_sha256": sha(saved),
              "owners": owners, "native_getters": getters,
              "native_ordinary_name_selections": 207, "other_given_names_preserved": 204,
              "instructions_sections_staged_payload_and_pointers_preserved": True,
              "record_checks": checks,
              "literal_name_records": sum(r["literal_name_changed"] for r in checks),
              "default_macro_records": sum(r["default_macro_changed"] for r in checks),
              "new_encoding_error_records": [{"file_path": r["file_path"], "id": r["id"],
                                              "issues": r["new_encoding_errors"]}
                                             for r in checks if r.get("new_encoding_errors")],
              "macro_length_changes_are_default_name_assumptions_not_live_expansion_proof": True,
              "remaining_scope": "Terminal scene-caption/Gallery owners, baked canonical records, native macro expansion proof, manuscript review, complete previews and integrated build/cold boot still required.",
              "playable_ROM_modified": False, "migration_complete": False}
    (root / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"owners": len(owners), "native_getters": 207,
                      "literal_records": report["literal_name_records"],
                      "macro_records": report["default_macro_records"],
                      "evaluated_records": len(checks), "encoding_error_records": len(report["new_encoding_error_records"]),
                      "formats": dict(Counter(batches[r["batch"]].get("encoder", "native") for r in checks)),
                      "playable_ROM_modified": False}))


if __name__ == "__main__":
    main()
