"""Revalidate inherited B44 layout constraints and prepare a complete-block probe."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue, encode_relocatable_dialogue
from dk4tool.dialogue.profiles import DialogueProfile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_character_names import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH = "/data/SC0.DK4"
ROOT = Path("work/analysis/confirmed_names_v199")


def logical(block):
    assert block[:4] == b"CS\0\x01"
    end = 8 + struct.unpack_from("<H", block, 4)[0]
    assert end <= len(block) and not any(block[end:])
    return block[:end].split(b"\0")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    map_path = Path("translations/sc0_b44_lisbon_parity_relocation_map.json")
    original_map = json.loads(map_path.read_text(encoding="utf-8"))
    historical = NdsImage.open("out/raphael_natural_v2_pre_lisbon_accepted_rollback.nds")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    current = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    old_file, source_file = historical.read_file(PATH), canonical.read_file(PATH)
    assert sha(old_file) == original_map["source_file_sha256"]
    old_block, source_block = [IlnkContainer.parse(data).blocks[44] for data in (old_file, source_file)]
    assert sha(old_block) == original_map["source_block_sha256"]
    old, source = logical(old_block), logical(source_block)
    assert len(old) == len(source) == 500
    movable = set(original_map["movable_segments"])
    assert original_map["external_references_complete"] and original_map["preserve_record_parity"]
    changed_fixed = []
    for index, (before, after) in enumerate(zip(old, source, strict=True)):
        assert len(before) % 2 == len(after) % 2
        if index == 1 or index in movable or before == after:
            continue
        assert index in (454, 456) and len(before) == len(after)
        changed_fixed.append(index)
    assert changed_fixed == [454, 456]
    preparation = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    targets = [r for r in preparation["records"] if r["file_path"] == PATH and r["id"].startswith("DK4_MES_B44_")]
    result, changes, resized = list(source), [], []
    for record in targets:
        index = int(record["id"].split("_R")[1])
        assert source[index] == bytes.fromhex(record["source_hex"])
        payload = dict(preparation["proposed_profiles_not_registered"][record["proposed_profile"]])
        payload["leading_speaker_bytes"] = frozenset(payload["leading_speaker_bytes"])
        profile = DialogueProfile(**payload)
        if index in (210, 327):
            assert index in movable
            encoded = encode_relocatable_dialogue(source[index], record["english"].removesuffix("{PAD}"), profile).encoded
            if len(encoded) % 2 != len(source[index]) % 2:
                encoded += b" "
            assert len(encoded) % 2 == len(source[index]) % 2
            resized.append(index)
        else:
            encoded = encode_fixed_dialogue(source[index], record["english"], profile).encoded
            assert len(encoded) == len(source[index])
        result[index] = encoded
        changes.append({"id": record["id"], "index": index,
                        "before_length": len(source[index]), "after_length": len(encoded),
                        "before_hex": source[index].hex(), "after_hex": encoded.hex()})
    assert resized == [210, 327]
    body = b"\0".join(result)[8:]
    assert len(body) <= 65535
    block = b"CS\0\x01" + struct.pack("<H", len(body)) + b"\0\0" + body
    block += bytes((-len(block)) % 4)
    after_segments = logical(block)
    assert len(after_segments) == len(source)
    allowed = {r["index"] for r in changes} | {1}
    assert all(a == b for index, (a, b) in enumerate(zip(source, after_segments, strict=True)) if index not in allowed)
    assert all(len(a) % 2 == len(b) % 2 for a, b in zip(source, after_segments, strict=True))
    assert source[454] == after_segments[454] and source[456] == after_segments[456]
    inherited = {**original_map, "source_file_sha256": sha(source_file), "source_block_sha256": sha(source_block),
                 "source_block_size": len(source_block), "source_cs_body_size": struct.unpack_from("<H", source_block, 4)[0],
                 "status": "research-inherited-layout-cold-boot-pending", "not_registered_release_map": True,
                 "inherited_map": map_path.as_posix(), "inherited_map_sha256": sha(map_path.read_bytes())}
    (ROOT / "b44_current_source_inherited_map.json").write_text(json.dumps(inherited, indent=2) + "\n", encoding="utf-8")
    blocks = IlnkContainer.parse(current.read_file(PATH))
    assert blocks.blocks[44] == source_block
    before_other_blocks = list(blocks.blocks)
    blocks.blocks[44] = block
    new_file = blocks.to_bytes()
    roundtrip = IlnkContainer.parse(new_file)
    assert all(before_other_blocks[i] == roundtrip.blocks[i] for i in range(len(roundtrip.blocks)) if i != 44)
    original_files = {p: data for _, p, data in current.iter_files()}
    original_components = dict(current.iter_components())
    names_arm9, _ = transform(current.read_file("/__arm9__.bin"), NdsImage.open("work/clean.nds").read_file("/__arm9__.bin"))
    current.replace_file("/__arm9__.bin", names_arm9)
    current.replace_file(PATH, new_file)
    research = ROOT / "b44_name_relocation_research_only.nds"
    current.save(research)
    saved = NdsImage.open(research)
    assert {p: data for _, p, data in saved.iter_files() if p != PATH} == {p: data for p, data in original_files.items() if p != PATH}
    assert bytes(saved.rom.arm7) == original_components["/__arm7__.bin"]
    report = {"format": "dk4-confirmed-name-b44-revalidation-v1",
              "historical_source_SC0_sha256": sha(old_file), "canonical_SC0_sha256": sha(source_file),
              "logical_segments": 500, "historical_movable_records": len(movable),
              "changed_nonmovable_records_only_same_size_choices": changed_fixed,
              "all_source_record_parities_preserved": True,
              "changed_name_records": changes, "resized_indices": resized,
              "block_size_delta": len(block) - len(source_block), "all_other_SC0_blocks_exact": True,
              "other_files_and_ARM7_exact": True,
              "research_ROM": research.as_posix(), "research_ROM_sha256": sha(research.read_bytes()),
              "research_only": True, "not_for_normal_gameplay_or_handoff": True,
              "full_macro_migration_outside_B44_incomplete": True,
              "cold_boot_verification_pending": True,
              "scope": "Inherited static layout/phase proof and complete selected-name B44 preparation; dynamic branches/continuations still require cold boot."}
    (ROOT / "b44_revalidation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"logical_segments": 500, "changed_name_records": len(changes),
                      "resized_records": len(resized), "block_size_delta": report["block_size_delta"], "research_only": True}))


if __name__ == "__main__":
    main()
