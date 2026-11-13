"""Compile current short-slot translations and census every route match."""

import json
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.revalidate_name_migration_v276 import DIGEST, ROM

ROOT = Path("work/analysis/name_catalog_v277")
PREPARATION = Path("work/analysis/confirmed_names_v276")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == DIGEST
    current = NdsImage.open(ROM)
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    packet = json.loads((PREPARATION / "current_route_migration_packet.json").read_text(encoding="utf-8"))
    proof = json.loads((PREPARATION / "current_migration_proof.json").read_text(encoding="utf-8"))
    selected = {(r["file_path"], r["id"]) for r in proof["allocation_backlog"]}
    drafts = {(r["file_path"], r["id"]): r for r in packet["records"]}
    records, requests, errors = [], {}, []
    blocks = {p: IlnkContainer.parse(current.read_file(p)).blocks for p in {k[0] for k in selected}}
    original = {p: IlnkContainer.parse(canonical.read_file(p)).blocks for p in blocks}
    for owner in sorted(selected):
        row = drafts[owner]
        block = int(row["id"].split("_B")[1].split("_")[0])
        index = int(row["id"].split("_R")[1])
        source = bytes.fromhex(row["source_hex"])
        assert original[owner[0]][block].split(b"\0")[index] == source
        profile_data = dict(packet["proposed_profiles_not_registered"][row["proposed_profile"]])
        profile_data["leading_speaker_bytes"] = frozenset(profile_data["leading_speaker_bytes"])
        profile = DialogueProfile(**profile_data)
        formatter_recovery = None
        try:
            encoded = encode_relocatable_dialogue(source, row["compiler_safe_markup"].removesuffix("{PAD}"), profile)
        except ValueError as error:
            if "pair-phase-auto-wrap" not in str(error):
                errors.append({"file_path": owner[0], "id": owner[1], "error": str(error)})
                continue
            profile = replace(profile, balanced_wrapping=True)
            try:
                encoded = encode_relocatable_dialogue(source, row["compiler_safe_markup"].removesuffix("{PAD}"), profile)
            except ValueError as retry_error:
                errors.append({"file_path": owner[0], "id": owner[1], "error": str(retry_error)})
                continue
            formatter_recovery = "Existing balanced formatter; wording, controls, width, line limit and macro lengths unchanged."
        key = blocks[owner[0]][block].split(b"\0")[index]
        target = encoded.encoded
        forms = [("whole", key, target)]
        tokens = parse_markup(row["compiler_safe_markup"])
        if tokens and tokens[0].kind == "speaker":
            assert key[0] == target[0] == source[0], owner
            forms.append(("body", key[1:], target[1:]))
        for form, key_form, target_form in forms:
            assert key_form and target_form and b"\0" not in key_form + target_form
            requests.setdefault(key_form, []).append({"owner": list(owner), "form": form, "target_hex": target_form.hex()})
        records.append({"file_path": owner[0], "id": owner[1], "source_hex": source.hex(),
                        "current_key_hex": key.hex(), "target_hex": target.hex(),
                        "English": row["english"], "formatted_markup": encoded.formatted_markup,
                        "current_slot_bytes": len(key), "complete_target_bytes": len(target),
                        "diagnostics": [r.__dict__ for r in encoded.diagnostics],
                        "balanced_formatter_recovery": formatter_recovery,
                        "proposed_profile": row["proposed_profile"], "editorial_override": row.get("editorial_override"),
                        "review": row["review"]})
    conflicts = [{"key_hex": key.hex(), "requests": rows} for key, rows in requests.items()
                 if len({r["target_hex"] for r in rows}) != 1]
    targets = {key: bytes.fromhex(rows[0]["target_hex"]) for key, rows in requests.items()
               if len({r["target_hex"] for r in rows}) == 1}
    matches, unintended, scanned = [], [], 0
    compiled = {(r["file_path"], r["id"]): r for r in records}
    covered = set()
    for path in [f"/data/SC{i}.DK4" for i in range(4)]:
        for block, raw_block in enumerate(IlnkContainer.parse(current.read_file(path)).blocks):
            for index, raw in enumerate(raw_block.split(b"\0")):
                scanned += 1
                owner = (path, f"DK4_MES_B{block:02d}_R{index:04d}")
                for form, key in [("whole", raw), ("body", raw[1:])] if raw else [("whole", raw)]:
                    if key not in targets:
                        continue
                    row = {"file_path": path, "id": owner[1], "form": form, "key_hex": key.hex()}
                    if owner not in compiled:
                        unintended.append(row)
                    else:
                        expected = bytes.fromhex(compiled[owner]["target_hex"])
                        if form == "body":
                            expected = expected[1:]
                        if expected != targets[key]:
                            unintended.append({**row, "reason": "matched target differs from own compiled translation"})
                        else:
                            covered.add(owner)
                    matches.append(row)
    result = {"format": "dk4-current-name-catalog-preparation-v277", "source_ROM_sha256": DIGEST,
              "selected_allocation_records": len(selected), "compiled_records": len(records),
              "compile_errors": errors, "records": records,
              "keys": [{"key_hex": key.hex(), "target_hex": targets[key].hex(), "requests": requests[key]} for key in sorted(targets)],
              "conflicting_keys": conflicts, "all_route_NUL_segments_scanned": scanned,
              "route_matches": matches, "unintended_or_conflicting_matches": unintended,
              "covered_source_records": len(covered),
              "all_four_route_strings_have_only_intended_matches": not errors and not conflicts and not unintended and covered == selected,
              "native_lookup_startup_pixels_and_registered_integration_pending": True,
              "playable_ROM_modified": False, "full_goal_complete": False}
    arm9 = current.read_file("/__arm9__.bin")
    common_matches = []
    native_entries = common_message_entries(current.read_file("/COMMON/MESFILE.DK4"), arm9, clean=False)
    for row in native_entries:
        for form, key in [("whole", row.text), ("body", row.text[1:])]:
            if key in targets:
                common_matches.append({"global_message_id": row.message_id, "form": form, "key_hex": key.hex()})
    result["COMMON_native_selections_checked_as_other_consumer_inputs"] = len(native_entries)
    result["COMMON_matching_keys_requiring_further_scope_review"] = common_matches
    result["required_native_caller_scope"] = ["020242C8", "02024310", "02024330"]
    (ROOT / "preparation_and_scope.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["selected_allocation_records", "compiled_records", "all_route_NUL_segments_scanned", "covered_source_records", "all_four_route_strings_have_only_intended_matches"]}
                     | {"compile_errors": len(errors), "conflicting_keys": len(conflicts), "unintended_matches": len(unintended)}))


if __name__ == "__main__":
    main()
