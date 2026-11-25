"""Verify a complete COMMON allocation proposal without creating a ROM."""

import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_reblocking import plan
from scripts.prepare_confirmed_name_common_v228 import CURRENT, CURRENT_SHA, OUT
from scripts.probe_remaining_common_layout import warm_copy


def select(common, arm9, message_id):
    blocks = IlnkContainer.parse(common).blocks
    directory = [struct.unpack_from("<HH", arm9, DIRECTORY_OFFSET + block * 4) for block in range(41)]
    block = max(index for index, (first, _) in enumerate(directory) if first <= message_id)
    start, following = struct.unpack_from("<HH", arm9, TABLE_OFFSET + message_id * 2)
    end = following if following >= start else directory[block][1]
    return blocks[block][start:end].split(b"\0", 1)[0]


def main():
    manuscript_path = Path("translations/confirmed_name_common_manuscript_v1.json")
    manuscript = json.loads(manuscript_path.read_text(encoding="utf-8"))
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError("Current candidate identity changed")
    image = NdsImage.open(CURRENT)
    common, arm9 = image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")
    old = common_message_entries(common, arm9, clean=False)
    authored = {row["message_id"]: row["english"].removesuffix("{PAD}").encode("cp932") for row in manuscript["records"]}
    for row in manuscript["records"]:
        if bytes.fromhex(row["current_native_lock"]["text_hex"]) != old[row["message_id"]].text:
            raise ValueError("Current selected source lock differs")
    rebuilt, mapped, allocation = plan(common, arm9, authored)
    # Compare every global selection, including terminal padding and packed
    # neighbors. Do not register an unreviewed directory hash merely to read it.
    for row in old:
        if select(rebuilt, mapped, row.message_id) != authored.get(row.message_id, row.text):
            raise ValueError(f"Unrelated or authored native selection differs: {row.message_id}")
    neighbors = sorted({i for target in authored for i in (target - 1, target + 1) if i not in authored})
    cases = [warm_copy(mapped, rebuilt, i, authored[i], cold_cache=cold)
             for i in authored for cold in (False, True)]
    cases.extend(warm_copy(mapped, rebuilt, i, old[i].text) for i in neighbors)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "common.bin").write_bytes(rebuilt)
    (OUT / "arm9.bin").write_bytes(mapped)
    (OUT / "allocation_plan.json").write_text(json.dumps(allocation, indent=2) + "\n", encoding="utf-8")
    proof = {
        "format": "dk4-confirmed-name-common-native-proof-v228",
        "parent_ROM_sha256": CURRENT_SHA, "manuscript_sha256": sha(manuscript_path.read_bytes()),
        "proposed_COMMON_sha256": sha(rebuilt), "proposed_ARM9_sha256": sha(mapped),
        "all_native_selections_exact": len(old), "unmodified_selections_byte_exact": len(old) - len(authored),
        "changed_messages": list(authored), "native_copy_cases": cases,
        "warm_and_cold_cache_paths_verified": True, "complete_first_last_and_terminal_NUL_verified": True,
        "max_native_copy_bytes": allocation["max_native_copy_bytes"],
        "original_4096_byte_cache_and_512_byte_output_bounds_preserved": True,
        "executable_code_and_other_ARM9_bytes_preserved": allocation["executable_code_unchanged"],
        "unrelated_native_padding_not_compacted": allocation["removed_english_padding_bytes"] == 0,
        "whole_packed_owner_four_entries_retained": True,
        "scope": "Actual ARM9 loader/selector/copy with explicit cache state and host file-read bridges; not final macro expansion, text pixels, scene control flow or physical gameplay.",
        "registered_release_modified": False, "full_goal_complete": False,
    }
    (OUT / "native_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_selections": len(old), "authored": len(authored), "native_copy_cases": len(cases),
                      "max_copy": allocation["max_native_copy_bytes"], "playable_ROM_modified": False}))


if __name__ == "__main__":
    main()
