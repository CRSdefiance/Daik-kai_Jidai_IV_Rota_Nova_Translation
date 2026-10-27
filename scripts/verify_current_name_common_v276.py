"""Current whole-COMMON allocation proposal with stable source message IDs."""

import json

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_reblocking import plan
from scripts.probe_remaining_common_layout import warm_copy
from scripts.revalidate_name_migration_v276 import DIGEST, ROM, ROOT
from scripts.verify_confirmed_name_common_v228 import select


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    image = NdsImage.open(ROM)
    common, arm9 = image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")
    entries = common_message_entries(common, arm9, clean=False)
    manuscript = json.loads((ROOT / "current_common_manuscript.json").read_text(encoding="utf-8"))
    authored = {}
    for row in manuscript["records"]:
        selected = entries[row["message_id"]]
        assert selected.text.hex().upper() == row["current_native_lock"]["text_hex"]
        authored[row["message_id"]] = row["english"].removesuffix("{PAD}").encode("cp932")
    rebuilt, mapped, allocation = plan(common, arm9, authored)
    for row in entries:
        assert select(rebuilt, mapped, row.message_id) == authored.get(row.message_id, row.text), row.message_id
    neighbors = sorted({n for i in authored for n in (i - 1, i + 1) if n not in authored})
    cases = [warm_copy(mapped, rebuilt, i, text, cold_cache=cold)
             for i, text in authored.items() for cold in (False, True)]
    cases.extend(warm_copy(mapped, rebuilt, i, entries[i].text) for i in neighbors)
    assert allocation["removed_english_padding_bytes"] == 0
    assert allocation["executable_code_unchanged"]
    (ROOT / "common_research_only.bin").write_bytes(rebuilt)
    (ROOT / "common_research_only_arm9.bin").write_bytes(mapped)
    proof = {"format": "dk4-current-name-common-allocation-v276", "source_ROM_sha256": DIGEST,
             "source_COMMON_sha256": sha(common), "source_ARM9_sha256": sha(arm9),
             "target_COMMON_sha256": sha(rebuilt), "target_ARM9_sha256": sha(mapped),
             "changed_global_message_IDs": list(authored), "all3668_message_selections_exact": True,
             "all3662_other_messages_including_padding_byte_exact": True,
             "native_warm_cold_and_neighbor_copy_cases": cases,
             "allocation_plan": allocation, "complete_packed_four_response_owner_preserved": True,
             "source_article_allocation_and_name_macro_route_migration_still_pending": True,
             "actual_final_expansion_glyphs_and_gameplay_unproved": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "current_common_allocation_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_selections": len(entries), "changed": len(authored),
                      "unchanged": len(entries) - len(authored), "native_copy_cases": len(cases),
                      "max_native_copy_bytes": allocation["max_native_copy_bytes"]}))


if __name__ == "__main__":
    main()
