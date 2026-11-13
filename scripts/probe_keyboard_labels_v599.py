"""Check display-only routing and original keyboard-provider IDs before build."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.keyboard_page_labels import BASE, DRAW, ENTRY, SOURCE_LABELS
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path("work/analysis/keyboard_labels_v599")
PARENT = 0x0218EEC8


def main():
    source = NdsImage.open("out/all_routes_combined_v593_candidate.nds").read_file("/__arm9__.bin")
    revised = (ROOT / "research_arm9.bin").read_bytes()
    u = machine(revised)
    observed = []

    def draw(uc, address, size, data):
        if address == DRAW:
            observed.append([uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)])
            uc.reg_write(UC_ARM_REG_R0, 0x12345678)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, draw)
    cases = []
    try:
        for index, pointer in enumerate(struct.unpack_from("<49I", source, 0x155408)):
            executed = call(u, ENTRY - BASE, (0x02460000, pointer))
            selected = ENTRY + 44 if pointer == SOURCE_LABELS[0] else ENTRY + 48 if pointer == SOURCE_LABELS[1] else pointer
            assert observed[-1] == [0x02460000, selected]
            assert u.reg_read(UC_ARM_REG_R0) == 0x12345678 and DRAW in executed
            cases.append({"index": index, "source_label_pointer": pointer, "display_pointer": selected,
                          "returned_original_painter_result_and_preserved_ABI": True})
        assert [c["index"] for c in cases if c["source_label_pointer"] != c["display_pointer"]] == [47, 48]
    finally:
        u.hook_del(hook)
    raw = Path("E:/Rota Nova translations/Generated/work/emulation_v193/name_editor_v582/frame_005500_arm9_ram.bin").read_bytes()
    contracts = []
    for arm in (source, revised):
        uc = machine(arm)
        uc.mem_write(BASE, raw)
        rows = []
        for japanese, expected in (("英", 50), ("記", 51)):
            label, keys = 0x02470000, 0x02470100
            uc.mem_write(label, japanese.encode("cp932") + b"\0")
            call(uc, 0xD1E3C, (PARENT + 4, label))
            assert uc.reg_read(UC_ARM_REG_R0) == expected
            uc.mem_write(STACK, struct.pack("<I", 0xFFFFFFFF))
            call(uc, 0xD1BBC, (PARENT + 4, expected, keys, 0))
            count = uc.reg_read(UC_ARM_REG_R0)
            assert 0 < count < 1024
            table = bytes(uc.mem_read(keys, count * 2))
            rows.append({"source_identifier": japanese, "original_page_index": expected,
                         "character_count": count, "complete_two_byte_table_hex": table.hex()})
        contracts.append(rows)
    assert contracts[0] == contracts[1]
    (ROOT / "display_and_provider_contract.json").write_text(json.dumps({
        "revised_ARM9_sha256": sha(revised), "all49_display_routes": cases,
        "only_two_original_label_pointers_remapped": True, "original_painter_boundary_bridged_only_in_routing_cases": True,
        "original_provider_queries_from_historical_captured_RAM": contracts[0],
        "current_and_revised_original_provider_contracts_exact": True,
        "actual_new_ROM_keyboard_pixels_and_navigation_not_yet_verified": True,
        "script_sha256": sha(Path(__file__).read_bytes())}, indent=2) + "\n", encoding="utf-8")
    counts = [row["character_count"] for row in contracts[0]]
    print(f"Keyboard contracts:49 exact display routes;original English/Symbol page IDs and complete character tables{counts} preserved.")


if __name__ == "__main__":
    main()
