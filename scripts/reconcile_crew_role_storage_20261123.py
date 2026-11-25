"""Bind all sixteen original crew roles to the current native selector and runtime RAM."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.reconcile_editorial_acceptance_20261123 import ARM, OUT, digest, read, reference


RELEASE = Path("releases/all_routes_editorial_20261123_sound_play_stop_candidate/verification/registered_release_verification.json")
RESULT = OUT.with_name("crew_role_storage_current_20261123.json")
SELECTOR, LITERAL, SAILOR_DRAW_CALL = 0x86314, 0x86334, 0x7D8D4
CLEAN_TABLE, CURRENT_TABLE = 0x021197A0, 0x023889C8
ROLE_COUNT = 16
APPROVED = ("Captain", "First Mate", "Strategist", "Purser", "Surveyor", "Sail Handler", "Helmsman",
            "Lookout", "Boarding Leader", "Gunner", "Missionary", "Surgeon", "Chief Cook", "Shipwright",
            "Animal Keeper", "Deckhand")


def row_at(memory, field):
    pointer, = unpack_from("<I", memory, field - BASE)
    start = pointer - BASE
    window = memory[start:start + 32]
    raw, terminator, _ = window.partition(b"\0")
    assert BASE <= pointer < BASE + len(memory) - 32 and terminator and raw
    return dict(pointer_field=field, string_pointer=pointer, exact_C_string_hex=(raw + terminator).hex(),
                text=raw.decode("cp932"))


def selected(arm, memory, table):
    u = machine(arm)
    if memory is not arm:
        u.mem_write(BASE, memory)
    rows = []
    for index in range(ROLE_COUNT):
        call(u, SELECTOR, (index,))
        field = u.reg_read(UC_ARM_REG_R0)
        assert field == table + index * 4
        rows.append(row_at(memory, field))
    for bad in (-2147483648, -1, 16, 255, 2147483647):
        call(u, SELECTOR, (bad & 0xFFFFFFFF,))
        assert u.reg_read(UC_ARM_REG_R0) == 0
    return rows


def main():
    import json

    assert not RESULT.exists()
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    assert digest("work/clean.nds") == release["clean_input_sha256"]
    original, candidate = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    clean, current = (img.read_file(ARM) for img in (original, candidate))
    startup_file = Path(release["own_registered_startup"])
    boot = read(startup_file)
    assert boot["candidate_sha256"] == release["candidate_sha256"]
    assert digest(startup_file) == release["own_registered_startup_sha256"]
    snapshot = boot["read_only_snapshot"]
    active = Path(snapshot["path"]).read_bytes()
    assert len(active) == 0x400000 and digest(snapshot["path"]) == snapshot["sha256"]

    assert clean[SELECTOR:LITERAL] == current[SELECTOR:LITERAL] == active[SELECTOR:LITERAL]
    assert tuple(unpack_from("<I", blob, LITERAL)[0] for blob in (clean, current, active)) == (CLEAN_TABLE, CURRENT_TABLE, CURRENT_TABLE)
    upto = CLEAN_TABLE - BASE + ROLE_COUNT * 4
    assert clean[CLEAN_TABLE - BASE:upto] == current[CLEAN_TABLE - BASE:upto]
    assert clean[SAILOR_DRAW_CALL:SAILOR_DRAW_CALL + 4] == current[SAILOR_DRAW_CALL:SAILOR_DRAW_CALL + 4]
    assert direct_bl_target(unpack_from("<I", current, SAILOR_DRAW_CALL)[0], BASE + SAILOR_DRAW_CALL) == BASE + SELECTOR
    assert all(not any(CLEAN_TABLE <= word < CLEAN_TABLE + ROLE_COUNT * 4
                   for word, in iter_unpack("<I", data[:len(data) // 4 * 4]))
               for _, _, data in loaded_components(candidate))
    source, visible = selected(clean, clean, CLEAN_TABLE), selected(current, active, CURRENT_TABLE)
    rows = []
    for index, (jp, en, approved) in enumerate(zip(source, visible, APPROVED, strict=True)):
        displaced = row_at(current, CLEAN_TABLE + index * 4)
        assert displaced == jp and en["text"].isascii() and en["text"].rstrip(" ") == approved
        rows.append(dict(index=index, source_reference=jp, original_storage_in_candidate=displaced,
                         runtime_selected= en, approved_English=approved,
                         disposition="The original selector uses the registered English slot for this role."))
    result = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        registered_release=reference(RELEASE), initialized_snapshot=snapshot, original_selector=BASE + SELECTOR,
        selector_table_literal=BASE + LITERAL, original_sailor_draw_call=BASE + SAILOR_DRAW_CALL,
        earlier_localization=reference("docs/crew_roles_v326.md"), role_records=rows,
        clean_and_current_invalid_case_count=10, original_table_aligned_references_in_loaded_ROM=0,
        ordinary_gameplay=False, other_possible_indirect_consumers_unverified=True,
        registered_ROM_changed=False, new_editorial_credit=0)
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("Bound all sixteen crew-role strings to the verified English selector table on the registered ROM.")


if __name__ == "__main__":
    main()
