"""Bind the archived debt lead against the original monthly settlement."""

from struct import pack, unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R4, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_SB, UC_ARM_REG_SP,
)

from dk4tool.script.common_message_table import common_message_entries
from scripts import register_fleet_diversion_20261125 as current
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = panels.OUT.with_name("month_end_debt_scope_20261125.json")
ARCHIVED = OUT.with_name("archived_dialogue_current_drafts_20261124.json")
PLAYBACK = "releases/all_routes_editorial_20261111_fleet_reports_candidate/verification/fleet_reports_gameplay_verification.json"
ENTRY, STOP = 0x0202DCF0, 0x0202DE00
CAPTAIN_GETTER, NUMERALS = 0x0203697C, 0x020ABF50
DIRECT, QUEUED = 0x02053F0C, 0x02053D44
PROFIT, LOSS, DEBT = 0x02117FA0, 0x02117F20, 0x02118080
TABLES = {
    PROFIT: (2571, -1, -1, -1, 2572, 2573, 2574, -1),
    LOSS: (2565, -1, 2566, 2567, 2568, 2569, 2570, -1),
    DEBT: (2575, -1, 2576, -1, 2577, 2578, 2579, -1),
}
COMPANY, FINANCE, ACTOR, FORMATTED = 0x023F0400, 0x023F0500, 0x023F0600, 0x023F0700
GUARD = b"\xa5" * 8
CASES = (
    (897400, 691, 0, 0, True, True),
    (100, 691, 0, 0, True, True),
    (691, 691, 0, 0, True, True),
    (692, 691, 0, 0, True, True),
    (0, 691, 0, 0, True, True),
    (100, 691, 0, 0, False, True),
    (100, 691, 0, 0, True, False),
    (100, 0, 0, 0, True, True),
    (100, 17, 120, 4, True, True),
    (99_999_999, 0, 200, 0, True, True),
)


def source_spans(japanese, installed):
    spans = []
    for start, end in (
        (0x0202DC94, STOP), (0x0202DEE0, 0x0202DEEC), (0x0202E800, 0x0202E82C),
        (0x0203CC80, 0x0203CCD0), (0x02053F4C, 0x02053F84),
        *((table, table + 32) for table in TABLES),
    ):
        raw = installed[start - BASE:end - BASE]
        assert raw and raw == japanese[start - BASE:end - BASE]
        spans.append(dict(start=start, end=end, sha256=sha256(raw).hexdigest()))
    assert tuple(unpack_from("<I", installed, addr - BASE)[0] for addr in
                 (0x0202DEE0, 0x0202DEE4, 0x0202DEE8)) == (PROFIT, LOSS, DEBT)
    assert all(unpack_from("<8i", installed, addr - BASE) == ids for addr, ids in TABLES.items())
    return spans


def one_case(arm, funds, expenses, income, invested, reports, actor):
    cpu = machine(arm)
    cpu.mem_write(COMPANY + 4, GUARD + pack("<I", funds) + GUARD)
    cpu.mem_write(FINANCE - 8, GUARD + pack("<6I", 1, 2, 3, expenses, income, invested) + GUARD)
    cpu.mem_write(STACK, b"\xcc" * 64)
    cpu.mem_write(STACK + 0xC, pack("<I", 0))
    cpu.mem_write(STACK + 0x3C, pack("<I", 1))
    for register, value in (
        (UC_ARM_REG_SP, STACK), (UC_ARM_REG_R4, FINANCE), (UC_ARM_REG_R6, 62),
        (UC_ARM_REG_R7, COMPANY), (UC_ARM_REG_R8, int(reports)), (UC_ARM_REG_SB, ACTOR),
    ):
        cpu.reg_write(register, value)
    callbacks, numbers = [], []

    def callback(core, address, _size, _userdata):
        a, b, c = (core.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        if address == CAPTAIN_GETTER:
            assert a == ACTOR
            core.reg_write(UC_ARM_REG_R0, ACTOR if actor else 0)
        elif address == NUMERALS:
            numbers.append(a)
            core.reg_write(UC_ARM_REG_R0, FORMATTED)
        elif address == DIRECT:
            assert a == ACTOR and c == FORMATTED
            callbacks.append(("fleet report", b))
        else:
            assert address == QUEUED and a == 3
            callbacks.append(("carryover warning", b))
        core.reg_write(UC_ARM_REG_PC, core.reg_read(UC_ARM_REG_LR))

    for address in (CAPTAIN_GETTER, NUMERALS, DIRECT, QUEUED):
        cpu.hook_add(UC_HOOK_CODE, callback, begin=address, end=address)
    cpu.emu_start(ENTRY, STOP, count=20000)
    assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert cpu.reg_read(UC_ARM_REG_R6) == 63

    net = income - expenses - invested
    delta = net // 2 if net > 0 else net
    unpaid = max(0, -delta - funds)
    balance = max(0, min(99_999_999, funds + delta))
    new_finance = (expenses, income, invested, unpaid, 0, 0)
    assert bytes(cpu.mem_read(COMPANY + 4, 20)) == GUARD + pack("<I", balance) + GUARD
    assert bytes(cpu.mem_read(FINANCE - 8, 40)) == GUARD + pack("<6I", *new_finance) + GUARD
    assert unpack("<I", cpu.mem_read(STACK + 0xC, 4)) == (int(bool(unpaid)),)
    assert numbers == ([abs(delta)] if reports and actor else [])
    expected = ([("fleet report", LOSS if delta < 0 else PROFIT)] if reports and actor else [])
    if reports and unpaid:
        expected.append(("carryover warning", DEBT))
    assert callbacks == expected
    return dict(funds=funds, expenses=expenses, income=income, invested=invested, requested_reports=reports,
                fleet_captain_available=actor, settlement_amount=delta, closing_funds=balance, carried=unpaid,
                observed_native_wrappers=callbacks, formatted_amounts=numbers)


def main():
    release = read(current.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean, active = map(NdsImage.open, (CLEAN, current.ROM))
    ja, arm = (rom.read_file(current.ARM) for rom in (clean, active))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    spans = source_spans(ja, arm)
    clean_results, current_results = [[one_case(blob, *case) for case in CASES] for blob in (ja, arm)]
    assert clean_results == current_results

    old = read(PLAYBACK)
    assert old["observed_ids"] == [2565, 2575] and old["ordinary_loss_and_deduction"]
    ordinary, focused = old["observations"]
    assert ordinary["loss"]["loss"] == focused["loss"]["loss"] == 691
    assert focused["carryover"]["unpaid_amount"] == 591
    native_archive, stored_archive = (rom.read_file(current.COMMON) for rom in (clean, active))
    original = common_message_entries(native_archive, ja)
    installed = panels.common_rows(stored_archive, arm)
    draft, = [row for row in read(ARCHIVED)["records"] if row["message_ID"] == 284]
    assert draft["original_display_ownership_open"]

    def exact(table, message):
        entry = table[message]
        return panels.text_reference(entry) | {"exact_hex": entry.text.hex()}

    assert exact(original, 284) == draft["source_reference"] and exact(installed, 284) == draft["installed_reference"]
    prior_holds = (ordinary["loss"], focused["loss"], focused["carryover"])
    for row in prior_holds:
        key = row["message_ID"]
        template = installed[key].text
        displayed = bytes.fromhex(row["formatter_input_hex"])
        assert displayed == (template % ("６９１".encode("cp932"),) if key == 2565 else template)

    bound = sorted({message for ids in TABLES.values() for message in ids if message >= 0})
    assert bound == list(range(2565, 2580))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
        scope="Native one-fleet settlement and aggregate notice branch. The original calculation, wallet update and rollover run. "
              "Captain selection, number formatting and display are supplied boundaries in this offline test.",
        original_and_installed_spans=spans, clean_and_current_results_equal=True, tested_cases=current_results,
        observed_tables=TABLES, message_ids_in_tables=bound,
        exact_records=[dict(message_ID=key, source=exact(original, key), installed=exact(installed, key)) for key in bound],
        earlier_gameplay=reference(PLAYBACK), captured_templates_still_installed=[2565, 2575],
        archived_common_284=dict(source=draft["source_reference"], installed=draft["installed_reference"],
                                excluded_from_tested_month_end_branch=True, other_owners_open=True),
        ROM_changed=False, new_gameplay=False, new_editorial_credit=0))
    print("Verified ten clean and installed settlement cases. The shortfall used the active carryover table.")


if __name__ == "__main__":
    main()
