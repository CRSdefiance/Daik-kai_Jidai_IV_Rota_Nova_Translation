"""Compile all remaining fixed name records without prose or slot changes."""

import json
from dataclasses import asdict, replace
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.revalidate_name_migration_v276 import DIGEST, ROM

ROOT = Path("work/analysis/fixed_names_v279")
PREPARATION = Path("work/analysis/confirmed_names_v276")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == DIGEST
    packet = json.loads((PREPARATION / "current_route_migration_packet.json").read_text(encoding="utf-8"))
    backlog = json.loads((PREPARATION / "current_migration_proof.json").read_text(encoding="utf-8"))
    catalog = {(r["file_path"], r["id"]) for r in backlog["allocation_backlog"]}
    rows = [r for r in packet["records"] if (r["file_path"], r["id"]) not in catalog]
    image = NdsImage.open(ROM)
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    current = {path: IlnkContainer.parse(image.read_file(path)).blocks for path in {r["file_path"] for r in rows}}
    original = {path: IlnkContainer.parse(canonical.read_file(path)).blocks for path in current}
    records, profiles = [], {}
    for row in rows:
        row = dict(row)
        path, record_id = row["file_path"], row["id"]
        block = int(record_id.split("_B")[1].split("_")[0])
        index = int(record_id.split("_R")[1])
        source = bytes.fromhex(row["source_hex"])
        assert original[path][block].split(b"\0")[index] == source
        actual = current[path][block].split(b"\0")[index]
        assert len(source) == len(actual)
        payload = dict(packet["proposed_profiles_not_registered"][row["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        profile = DialogueProfile(**payload)
        presentation_recovery = None
        if (path == "/data/SC0.DK4" and record_id in {
                "DK4_MES_B64_R0287", "DK4_MES_B64_R0363", "DK4_MES_B66_R0005",
                "DK4_MES_B66_R0031", "DK4_MES_B67_R0023", "DK4_MES_B67_R0148", "DK4_MES_B67_R0178"}):
            assert source[0] == actual[0] == 0x50
            if row["english"].startswith("P"):
                row["english"] = "{SPEAKER:50}" + row["english"][1:]
                row["compiler_safe_markup"] = "{SPEAKER:50}" + row["compiler_safe_markup"][1:]
            assert row["english"].startswith("{SPEAKER:50}")
            profile = replace(profile, name=profile.name + "-Charlotte-50-v279",
                              leading_speaker_bytes=profile.leading_speaker_bytes | {0x50})
            presentation_recovery = "Native02029B18..02029B2C separates actor80 metadata from the body; selector0202434C and table80 identify Charlotte. Limited to these seven exact source records."
        audit = audit_fixed_dialogue_record(source, row["compiler_safe_markup"], profile)
        recovery = None
        if any(i["severity"] == "warning" or "pair-phase-auto-wrap" in i["message"] for i in audit["issues"]):
            profile = replace(profile, name=profile.name + "-fixed-review-balanced-v279", balanced_wrapping=True)
            audit = audit_fixed_dialogue_record(source, row["compiler_safe_markup"], profile)
            recovery = "Existing balanced formatter; wording, controls, panel size and slot length unchanged."
        assert not any(i["severity"] in ("warning", "error") for i in audit["issues"]), (path, record_id, audit["issues"])
        encoded = encode_fixed_dialogue(source, row["compiler_safe_markup"], profile)
        assert len(encoded.encoded) == len(actual) and b"\0" not in encoded.encoded
        profiles[profile.name] = asdict(profile)
        profiles[profile.name]["leading_speaker_bytes"] = sorted(profile.leading_speaker_bytes)
        records.append({**row, "current_key_hex": actual.hex(), "target_hex": encoded.encoded.hex(),
                        "formatted_markup": encoded.formatted_markup, "padding_bytes": encoded.padding_bytes,
                        "current_profile": profile.name, "balanced_formatter_recovery": recovery,
                        "printable_presentation_recovery": presentation_recovery,
                        "final_layout_audit": audit,
                        "source_context_editorial_review_not_inherited_from_QA": True})
    rebuilt = {p: [bytes(b) for b in blocks] for p, blocks in current.items()}
    changed = {}
    for row in records:
        path = row["file_path"]
        block = int(row["id"].split("_B")[1].split("_")[0])
        index = int(row["id"].split("_R")[1])
        parts = rebuilt[path][block].split(b"\0")
        assert parts[index].hex() == row["current_key_hex"]
        parts[index] = bytes.fromhex(row["target_hex"])
        rebuilt[path][block] = b"\0".join(parts)
        changed.setdefault((path, block), set()).add(index)
    for path, blocks in rebuilt.items():
        for block, (before, after) in enumerate(zip(current[path], blocks, strict=True)):
            assert len(before) == len(after)
            assert [i for i, c in enumerate(before) if c == 0] == [i for i, c in enumerate(after) if c == 0]
            for index, (left, right) in enumerate(zip(before.split(b"\0"), after.split(b"\0"), strict=True)):
                if index not in changed.get((path, block), set()):
                    assert left == right
    proof = {"format": "dk4-fixed-name-migration-v279", "source_ROM_sha256": DIGEST,
             "records": records, "profiles_not_registered": profiles,
             "fixed_records": len(records), "balanced_warning_recoveries": sum(bool(r["balanced_formatter_recovery"]) for r in records),
             "all_fixed_record_block_lengths_NUL_offsets_and_unmodified_segments_preserved": True,
             "no_errors_or_unwaived_warnings_in_fixed_record_layout_audits": True,
             "all_368_complete_glyph_pixels_editorial_reviews_and_scene_tests_pending": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "fixed_record_proposal.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"fixed_records": len(records), "balanced_recoveries": proof["balanced_warning_recoveries"],
                      "errors": 0, "warnings": 0, "script_boundaries_preserved": True}))


if __name__ == "__main__":
    main()
