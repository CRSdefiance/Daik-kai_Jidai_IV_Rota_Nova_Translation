"""Scope the Japanese zodiac names to the verified native stat-table path."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.probe_button_prompt_native import call, machine
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, OUT, digest, read, reference


RELEASE = Path("releases/all_routes_editorial_20261123_pirate_affiliation_candidate/verification/registered_release_verification.json")
RESULT = OUT.with_name("zodiac_stat_table_scope_20261123.json")
TABLE, ENTRY_SIZE, COUNT = 0x15F578, 0x1C, 12
SELECT, STAT, ACTOR = 0xCDDF8, 0xCDDD8, 0x7E960


def address_sites(rom, targets):
    positions = {target: [] for target in targets}
    for name, base, raw in loaded_components(rom):
        for i, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) // 4 * 4])):
            if word in positions:
                positions[word].append({"component": name, "address": base + i * 4})
    return positions


def main():
    import json

    assert not RESULT.exists()
    receipt = read(RELEASE)
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"]
    assert digest("work/clean.nds") == receipt["clean_input_sha256"]
    clean, current = map(NdsImage.open, ("work/clean.nds", receipt["candidate"]))
    source, arm = (rom.read_file(ARM) for rom in (clean, current))
    spans = [(0x15F4E8, TABLE + COUNT * ENTRY_SIZE), (STAT, 0xCDE20), (ACTOR, 0x7E980), (0x7E45C, 0x7E4A8)]
    assert all(source[lo:hi] == arm[lo:hi] for lo, hi in spans)
    for caller, callee in ((0x7E460, ACTOR), (0x7E4A0, STAT), (0x7E974, SELECT)):
        assert direct_bl_target(unpack_from("<I", arm, caller)[0], BASE + caller) == BASE + callee

    pointers = [unpack_from("<I", arm, TABLE + i * ENTRY_SIZE)[0] for i in range(COUNT)]
    assert set(pointers) == {BASE + 0x15F4E8 + 8 * i for i in range(COUNT)}
    addresses = address_sites(current, {BASE + TABLE, *pointers})
    assert addresses[BASE + TABLE] == [{"component": "arm9_section_0", "address": BASE + 0xCDE1C}]
    cpu = machine(arm)
    rows = []
    for index, pointer in enumerate(pointers):
        offset = TABLE + index * ENTRY_SIZE
        assert addresses[pointer] == [{"component": "arm9_section_0", "address": BASE + offset}]
        call(cpu, SELECT, (index,))
        assert cpu.reg_read(UC_ARM_REG_R0) == BASE + offset
        numbers = unpack_from("<6I", arm, offset + 4)
        for field, expected in enumerate(numbers):
            call(cpu, STAT, (BASE + offset, field))
            assert cpu.reg_read(UC_ARM_REG_R0) == expected
        name = arm[pointer - BASE:pointer - BASE + 8]
        rows.append(dict(index=index, table_address=BASE + offset, name_address=pointer,
            clean_and_current_slot_hex=name.hex(), japanese=name.split(b"\0", 1)[0].decode("cp932"),
            verified_numeric_fields=list(numbers), name_pointer_use_in_tested_stat_path=False))
    for invalid in (-1, 12):
        call(cpu, SELECT, (invalid & 0xFFFFFFFF,))
        assert cpu.reg_read(UC_ARM_REG_R0) == 0
    icon_research = Path("docs/all_routes_unified_v173_checkpoint.md")
    result = dict(candidate_sha256=receipt["candidate_sha256"], source_clean_sha256=receipt["clean_input_sha256"],
        verified_source_current_spans=spans, native_call_path=[0x0207E460, BASE + ACTOR, BASE + SELECT, 0x0207E4A0, BASE + STAT],
        twelve_exact_storage_refs=rows, original_stat_cases=COUNT * 6, invalid_sign_cases=2,
        earlier_visual_icon_scope=reference(icon_research), current_gameplay=False,
        finding="The mapped actor stat path reads the six numeric coefficients. It does not fetch the sign-name field.",
        disposition="Preserve the original table bytes in the proven numeric consumer scope. Keep the references for other callers.",
        other_possible_indirect_consumers_unverified=True, new_review_credit=0)
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("Verified all 72 native zodiac coefficients and two invalid inputs without consuming the stored names.")


if __name__ == "__main__":
    main()
