"""Rebase bounded message-catalog research onto exact V218 with full prose.

Writes ARM9 analysis bytes only. All route files/instruction boundaries stay
unchanged; this is not a playable or registered partial name migration.
"""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_character_names import transform as historical_names
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO, helper
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path("work/analysis/name_catalog_v233")
ROM = Path("out/all_routes_combined_v218_candidate.nds")
ROM_SHA = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
ARM_SHA = "a4af5e53f570bdfe76c895fb8704ba0db461851b4935c591daa2ea23647652c1"


def named_source(source, prior, clean):
    # Reuse the old strictly pinned transform to obtain its already-proven five
    # changes; apply only those exact source intervals to a separately pinned
    # current source. Do not weaken the historical transform's source guard.
    _, report = historical_names(prior, clean)
    result = bytearray(source)
    for row in report["records"]:
        offset, capacity = row["offset"], row["capacity"]
        if source[offset:offset + capacity] != bytes.fromhex(row["source_hex"]):
            raise ValueError("Current name allocation/source differs")
        pointer = struct.pack("<I", row["pointer"])
        references = [i for i in range(len(source) - 3) if source[i:i + 4] == pointer]
        if references != [row["table_field"]]:
            raise ValueError("Current name has unreviewed static aliases")
        result[offset:offset + capacity] = bytes.fromhex(row["replacement_hex"])
    report.update({"current_source_sha256": sha(source), "current_named_sha256": sha(result),
                   "historical_transform_source_guard_retained": True})
    return bytes(result), report


def append(source, named, names, entries):
    code = MainCodeFile(named, BASE)
    before = [bytes(section.data) for section in code.sections]
    if len(before) != 4 or len(before[3]) != 52624 or not cache_plan(named):
        raise ValueError("Exact V218 inherited staging/cache source differs")
    packed = bytearray(before[3][:-48])
    pointers, seen, records = {}, {}, []

    def store(raw):
        if not raw or b"\0" in raw or len(raw) >= 512:
            raise ValueError("Bounded complete NUL-ended catalog string required")
        if raw not in pointers:
            packed.extend(bytes((-len(packed)) % 4))
            pointers[raw] = POOL + len(packed)
            packed.extend(raw + b"\0")
        return pointers[raw]

    for entry in entries:
        key, target = bytes.fromhex(entry["key_hex"]), bytes.fromhex(entry["target_hex"])
        if key in seen and seen[key] != target:
            raise ValueError("Same native source key has conflicting meanings")
        seen[key] = target
    for key, target in sorted(seen.items()):
        records.append({"key_pointer": store(key), "target_pointer": store(target),
                        "key_bytes_with_NUL": len(key) + 1, "key_hex": key.hex(), "target_hex": target.hex()})
    packed.extend(bytes((-len(packed)) % 4))
    table = POOL + len(packed)
    for row in records:
        packed.extend(struct.pack("<3I", row["key_pointer"], row["target_pointer"], row["key_bytes_with_NUL"]))
    entry = POOL + len(packed)
    implementation = helper(entry, table, len(records))
    packed.extend(implementation)
    for field in CALLS:
        if struct.unpack_from("<I", named, field)[0] != branch_link(BASE + field, MACRO):
            raise ValueError("Current source story-copy instruction changed")
        struct.pack_into("<I", code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Catalog exceeds mapped main-pool/staging ownership")
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, named))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, cache_entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for field in (*CALLS, 0x8E4, 0xE45DC):
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if (bytes(restored) != before[0] or any(bytes(parsed.sections[i].data) != before[i] for i in (1, 2))
            or bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]):
        raise ValueError("Inherited code/sections/graphics/helpers changed")
    return saved, {"source_arm9_sha256": sha(source), "named_arm9_sha256": sha(named),
                   "target_arm9_sha256": sha(saved), "name_fields": names,
                   "entry": entry, "table": table, "records": records,
                   "helper_bytes": len(implementation), "helper_sha256": sha(implementation),
                   "inherited_pool_bytes_preserved": len(before[3]) - 48,
                   "pool_payload_bytes": size, "copy_entry": copy_entry,
                   "cache": cache_plan(saved), "pool_span": [POOL, POOL + size],
                   "staging_span": [STAGE, STAGE + size + 48],
                   "scoped_call_sites": [BASE + field for field in CALLS],
                   "original_macro_expander_and_other_sections_preserved": True,
                   "research_only_not_playable": True}


def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--prior-plan", type=Path, default=Path("work/analysis/confirmed_names_v201/catalog_plan.json"))
    parser.add_argument("--expected-inherited", type=int, default=25)
    parser.add_argument("--formatting-report", type=Path, default=Path("work/analysis/name_editorial_v232/formatting_report.json"))
    parser.add_argument("--manuscript", type=Path, default=Path("translations/confirmed_name_route_editorial_v232.json"))
    parser.add_argument("--expected-additions", type=int, default=10)
    args = parser.parse_args()
    ROOT = args.out
    ROOT.mkdir(parents=True, exist_ok=True)
    if sha(ROM.read_bytes()) != ROM_SHA:
        raise ValueError("Current registered ROM identity differs")
    image = NdsImage.open(ROM)
    prior = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    source = image.read_file("/__arm9__.bin")
    if sha(source) != ARM_SHA:
        raise ValueError("Current complete ARM9 source differs")
    old_plan_path = args.prior_plan
    old_plan = json.loads(old_plan_path.read_text(encoding="utf-8"))
    entries = list(old_plan["entry_keys"])
    inherited = list(old_plan["prepared_records"])
    if len(inherited) != args.expected_inherited:
        raise ValueError("Complete prior catalog owner set differs")
    report_path = args.formatting_report
    formatting = json.loads(report_path.read_text(encoding="utf-8"))
    manuscript = json.loads(args.manuscript.read_text(encoding="utf-8"))
    reviewed = {r["id"]: r for r in manuscript["records"]}
    blocks = IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks
    added = []
    for row in formatting["checks"]:
        if not row.get("private_pool_allocation_required"):
            continue
        if not row["visual_review_complete"] or row["private_catalog_allocation_blockers"]:
            raise ValueError("Incomplete private allocation review")
        block_id = int(row["id"].split("_B")[1].split("_")[0])
        record_id = int(row["id"].split("_R")[1])
        key = blocks[block_id].split(b"\0")[record_id]
        target = bytes.fromhex(row["private_message_catalog_payload_hex"])
        one_byte_selector = reviewed[row["id"]]["english"].startswith("{SPEAKER:")
        if one_byte_selector and key[:1] != target[:1]:
            raise ValueError("Original calibrated actor selector differs")
        forms = [(key, target, "whole")]
        if one_byte_selector:
            forms.append((key[1:], target[1:], "body"))
        for original, translated, form in forms:
            entries.append({"key_hex": original.hex(), "target_hex": translated.hex(),
                            "form": form, "owner": row["id"]})
        added.append({"file_path": "/data/SC0.DK4", "id": row["id"],
                      "current_record_hex": key.hex(), "encoded_translation_hex": target.hex(),
                      "canonical_source_hex": row["source_hex"], "english": row["english"],
                      "calibrated_one_byte_selector": one_byte_selector,
                      "source_slot_bytes": len(key), "full_translation_bytes": len(target)})
    if len(added) != args.expected_additions:
        raise ValueError("Complete declared capacity case set differs")
    if {(r["file_path"], r["id"]) for r in added} & {(r["file_path"], r["id"]) for r in inherited}:
        raise ValueError("New catalog owners duplicate inherited owners")
    for index in range(4):
        path = f"/data/SC{index}.DK4"
        if image.read_file(path) != prior.read_file(path):
            raise ValueError("Inherited catalog runtime source keys need fresh mapping")
    selected = {(r["file_path"], r["id"]) for r in inherited + added}
    key_map = {bytes.fromhex(r["key_hex"]): bytes.fromhex(r["target_hex"]) for r in entries}
    matches, scanned, unexpected = [], 0, []
    for index in range(4):
        path = f"/data/SC{index}.DK4"
        for block_id, block in enumerate(IlnkContainer.parse(image.read_file(path)).blocks):
            for record_id, raw in enumerate(block.split(b"\0")):
                scanned += 1
                for form, candidate in [("whole", raw), ("body", raw[1:])]:
                    if candidate not in key_map:
                        continue
                    owner = path, f"DK4_MES_B{block_id:02d}_R{record_id:04d}"
                    item = {"file_path": path, "id": owner[1], "form": form}
                    matches.append(item)
                    if owner not in selected:
                        unexpected.append(item)
    covered = {(r["file_path"], r["id"]) for r in matches}
    if not selected <= covered:
        raise ValueError("A selected source owner is missing from the complete route audit")
    scope = {"all_route_NUL_segments_scanned": scanned, "matches": matches,
             "all_selected_owners_covered": True, "selected_source_owners": len(selected),
             "unique_matched_source_owners": len(covered),
             "unreviewed_extra_matches": unexpected, "script_resources_unchanged": True}
    (ROOT / "route_scope.json").write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    if unexpected:
        raise ValueError(f"Additional exact-key owners need source review: {unexpected}")
    named, names = named_source(source, prior.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin"))
    saved, plan = append(source, named, names, entries)
    plan.update({"source_ROM_sha256": ROM_SHA, "prepared_records": inherited + added,
                 "added_editorial_records": added, "entry_keys": entries,
                 "prior_catalog_plan_sha256": sha(old_plan_path.read_bytes()),
                 "editorial_formatting_report_sha256": sha(report_path.read_bytes()), "route_scope": scope,
                 "all_script_instruction_boundaries_and_resources_untouched": True,
                 "whole_name_migration_and_live_release_still_pending": True})
    (ROOT / "catalog_research_arm9.bin").write_bytes(saved)
    (ROOT / "catalog_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inherited_records": len(inherited), "new_records": len(added),
                      "unique_keys": len(plan["records"]), "pool_bytes": plan["pool_payload_bytes"],
                      "all_inherited_bytes_preserved": True, "route_segments_scanned": scanned,
                      "research_only_no_ROM_created": True}))


if __name__ == "__main__":
    main()
