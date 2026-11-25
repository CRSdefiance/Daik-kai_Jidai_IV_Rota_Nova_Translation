"""Verify the original fleet destination formatter and regional picker bounds."""

from pathlib import Path
from struct import iter_unpack, pack

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
from unicorn.arm_const import UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP

from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.native_call_abi_v764 import STACK, STOP
from scripts.observe_seoul_tavern_decline_20261123 import RELEASE
from scripts.reconcile_class_names_20261123 import type_name, word
from scripts.reconcile_town_trend_catalogue_20261123 import OUT as CATALOGUE
from scripts.stage_azores_wording_20261123 import ARM, BASE, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = CATALOGUE.with_name("fleet_destination_name_caller_20261123.json")
LEGACY = OUT.with_name("legacy_fleet_text_current_20261123.json")
PICKER, PICKER_END = 0x0208BD84, 0x0208BDC0
DISPLAY, CALL, NO_TARGET = 0x02037624, 0x02037668, 0x0203766C
FORMAT, TEMPLATE = 0x020D5200, 0x021370F8
MISSIONARY_GETTER = 0x0202BFEC
PICKER_SCRATCH, PICKER_TABLE = 0x02443000, 0x02443200
MENU_ENTRY, LEGACY_FACTORY = 0x0208C308, 0x02036DB8
FACTORY_BRANCHES = {0: 0x0208C33C, 1: 0x0208C368, 2: 0x0208C36C}


def code_at(arm, start, stop):
    return arm[start - BASE:stop - BASE]


def regional_picker(cpu):
    values = {}
    cpu.mem_write(PICKER_SCRATCH, pack("<I", PICKER_TABLE) + bytes(60))
    cpu.mem_write(PICKER_TABLE - 0x10, bytes(4))
    for raw_choice in (*range(256), -1, -2147483648, 2147483647):
        original_mode = 0xAB
        cpu.mem_write(PICKER_SCRATCH + 4, pack("<I", 1))
        cpu.mem_write(PICKER_SCRATCH + 0x20, bytes(4))
        cpu.mem_write(STACK - 12, pack("<3I", original_mode, PICKER_SCRATCH, STOP))
        for reg, value in ((UC_ARM_REG_R0, raw_choice & 0xFFFFFFFF),
                           (UC_ARM_REG_R4, original_mode), (UC_ARM_REG_R5, PICKER_SCRATCH),
                           (UC_ARM_REG_SP, STACK - 16)):
            cpu.reg_write(reg, value)
        cpu.emu_start(PICKER, STOP, count=32)
        assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
        actual = cpu.reg_read(UC_ARM_REG_R0)
        assert actual == (raw_choice - 29 if 29 <= raw_choice < 119 else 115)
        assert bytes(cpu.mem_read(PICKER_SCRATCH + 4, 4)) == pack("<I", original_mode)
        assert bytes(cpu.mem_read(PICKER_SCRATCH + 0x20, 4)) == pack("<I", 1)
        values[raw_choice] = actual
    assert set(values.values()) == set(range(90)) | {115}
    return dict(tail_address=PICKER, tested_widget_result_values=len(values), valid_widget_commands=[29, 118],
                ordinary_returned_destination_slots=list(range(90)), cancel_or_other_result=115,
                boundaries={n: values[n] for n in (-1, 28, 29, 118, 119, 143, 255)})


def read_string(cpu, pointer):
    assert BASE <= pointer < BASE + 0x400000 - 64
    raw, terminator, _ = bytes(cpu.mem_read(pointer, 64)).partition(b"\0")
    assert raw and terminator
    return raw + terminator


def fleet_menu_modes(cpu):
    cpu.mem_write(PICKER_TABLE - 0x0C, bytes(4))
    cpu.mem_write(PICKER_SCRATCH + 0x0C, pack("<I", 0x30))
    report, trace = [], []

    def stop_at_branch(core, address, _size, _data):
        trace.append(address)
        core.emu_stop()

    hooks = [cpu.hook_add(UC_HOOK_CODE, stop_at_branch, begin=pc, end=pc) for pc in FACTORY_BRANCHES.values()]
    try:
        for mode in FACTORY_BRANCHES:
            cpu.mem_write(PICKER_SCRATCH + 4, pack("<I", mode))
            for reg, value in ((UC_ARM_REG_R0, PICKER_SCRATCH), (UC_ARM_REG_R1, 27), (UC_ARM_REG_SP, STACK)):
                cpu.reg_write(reg, value)
            trace.clear()
            cpu.emu_start(MENU_ENTRY, STOP, count=100)
            caller = FACTORY_BRANCHES[mode]
            assert trace == [caller] and cpu.reg_read(UC_ARM_REG_PC) == caller
            args = None
            if mode < 2:
                args = [cpu.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
                if mode == 0:
                    assert args == [27, 1, PICKER_SCRATCH, 0]
                else:
                    assert args == [27, 0, 0, PICKER_SCRATCH]
                    assert bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 4)) == pack("<I", 0x3A)
            report.append(dict(supplied_widget_mode=mode, original_branch=caller, args=args))
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    return report


def test_destination(arm, snapshot, names):
    raw = read_ram(snapshot)
    assert raw[DISPLAY - BASE:NO_TARGET - BASE] == code_at(arm, DISPLAY, NO_TARGET)
    assert raw[PICKER - BASE:PICKER_END - BASE] == code_at(arm, PICKER, PICKER_END)
    cpu, get = get_machine(arm, raw)
    root = get(0xCB178)
    fleet = get(0xCB1A8) + 4 + 132
    assert type_name(raw, word(raw, root + 4 + 114 * 108)) == "6CAdman"
    slot = fleet + 0x3F
    existing_byte = bytes(cpu.mem_read(slot, 1))
    probe = []

    def stop_before_draw(core, address, _size, _user):
        probe.append((address, core.reg_read(UC_ARM_REG_R0)))
        if address != MISSIONARY_GETTER:
            core.emu_stop()

    hooks = [cpu.hook_add(UC_HOOK_CODE, stop_before_draw, begin=address, end=address)
             for address in (CALL, NO_TARGET, MISSIONARY_GETTER)]
    destinations = []
    try:
        for destination in range(116):
            cpu.mem_write(slot, bytes([destination]))
            cpu.reg_write(UC_ARM_REG_R4, fleet)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            probe.clear()
            cpu.emu_start(DISPLAY, STOP, count=1000)
            if destination == 115:
                assert [pc for pc, _ in probe] == [NO_TARGET] and cpu.reg_read(UC_ARM_REG_PC) == NO_TARGET
                destinations.append(dict(destination=destination, reaches_formatter=False))
                continue
            receiver = root + 4 + destination * 108
            vtable = word(raw, receiver)
            getter = word(raw, vtable + 8)
            if destination == 114:
                assert probe[0] == (MISSIONARY_GETTER, receiver) and getter == MISSIONARY_GETTER
                assert len(probe) == 2
            else:
                assert len(probe) == 1
            assert probe[-1][0] == CALL and cpu.reg_read(UC_ARM_REG_PC) == CALL
            assert cpu.reg_read(UC_ARM_REG_R0) == STACK and cpu.reg_read(UC_ARM_REG_R1) == TEMPLATE
            pointer = cpu.reg_read(UC_ARM_REG_R2)
            text = read_string(cpu, pointer)
            if destination < 114:
                name = names[destination]
                assert name["town"] == destination and getter == name["original_name_getter"]
                assert pointer == name["string_address"] and text.hex() == name["exact_hex"]
            else:
                assert text == "伝道師".encode("cp932") + b"\0"
            destinations.append(dict(destination=destination, reached_formatter=FORMAT, name_getter=getter,
                    name_address=pointer, exact_hex=text.hex(), name=text[:-1].decode("cp932")))
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
        cpu.mem_write(slot, existing_byte)
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    picker = regional_picker(cpu)
    modes = fleet_menu_modes(cpu)
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return dict(snapshot=snapshot, original_fleet_destination_byte=existing_byte.hex(),
                original_town_root=root, fleet_record=fleet, picker=picker, menu_mode_test=modes,
                destinations=destinations)


def factory_references(image):
    found = dict(direct_calls=[], aligned_pointer_references=[])
    for area, origin, data in loaded_components(image):
        for index, (value,) in enumerate(iter_unpack("<I", data[:len(data) // 4 * 4])):
            address = origin + index * 4
            if direct_bl_target(value, address) == LEGACY_FACTORY:
                found["direct_calls"].append((area, address))
            if value == LEGACY_FACTORY:
                found["aligned_pointer_references"].append((area, address))
    assert found["direct_calls"] == [("arm9_section_0", 0x020407E0), ("arm9_section_0", 0x0208C368)]
    assert not found["aligned_pointer_references"]
    return found


def main():
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    catalogue = read(CATALOGUE)
    assert catalogue["exact_candidate_sha256"] == release["candidate_sha256"]
    images = [NdsImage.open(p) for p in (CLEAN, release["candidate"])]
    clean, current = [image.read_file(ARM) for image in images]
    assert digest_bytes(current) == release["target_ARM9_sha256"]
    spans = [(DISPLAY, 0x02037680), (PICKER, PICKER_END), (0x0208ACC0, 0x0208AD14),
             (0x0208AE5C, 0x0208B010), (0x02035A24, 0x02035A30),
             (MISSIONARY_GETTER, MISSIONARY_GETTER + 12), (TEMPLATE, TEMPLATE + 12),
             (MENU_ENTRY, 0x0208C388), (0x020407A0, 0x020407F0),
             (0x0203FE40, 0x0203FEA4), (0x0203FEE8, 0x0203FEEC)]
    code = {}
    for start, stop in spans:
        actual = code_at(current, start, stop)
        assert actual == code_at(clean, start, stop)
        code[f"0x{start:08X}"] = dict(end=stop, exact_hex=actual.hex(), sha256=digest_bytes(actual))
    for caller, target in ((0x0208ACC8, 0x0208BD5C), (0x0208ACFC, 0x0208AE5C),
                           (0x0208B000, 0x02035A24), (CALL, FORMAT), (0x0203FE98, 0x020406E4)):
        assert direct_bl_target(word(current, caller), caller) == target
    assert code_at(current, TEMPLATE, TEMPLATE + 12).split(b"\0", 1)[0] == "目標街：%s".encode("cp932")
    table = word(current, 0x0203FEE8)
    label = word(current, table + 3 * 16)
    assert table == 0x02115568 and word(clean, table + 3 * 16) == label == 0x02138608
    clean_text, installed_text = [code_at(arm, label, label + 64).split(b"\0", 1)[0]
                                  for arm in (clean, current)]
    assert clean_text == "艦隊情報".encode("cp932") and installed_text == b"Fleet Info"
    names = catalogue["town_table"]
    results = dict(
        clean=test_destination(clean, names["original_snapshot"]["read_only_frame"], names["clean"]),
        installed=test_destination(current, names["installed_snapshot"]["read_only_frame"], names["installed"]),
    )
    assert results["clean"]["picker"] == results["installed"]["picker"]
    assert results["clean"]["menu_mode_test"] == results["installed"]["menu_mode_test"]
    factories = [factory_references(image) for image in images]
    assert factories[0] == factories[1]
    legacy = read(LEGACY)
    calls = legacy["regional_order_selector_calls"]
    assert len(calls) == 6 and all(v["PC"] == 0x0208AE5C and v["LR"] == 0x0208AD00 for v in calls)
    write(OUT, dict(registered_release=reference(RELEASE), exact_native_code=code, town_name_catalogue=reference(CATALOGUE),
        original_destination_formatter=dict(template_address=TEMPLATE, template="目標街：%s", caller=CALL, callee=FORMAT),
        legacy_factory=dict(address=LEGACY_FACTORY, references=factories[0], menu_entry=MENU_ENTRY,
                            stock_mode_zero_call=0x0208AB88, stock_mode_one_call=LEGACY_FACTORY),
        fleet_info_menu=dict(actual_menu_activation_unverified_by_offline_test=True,
            label_address=label, clean_hex=clean_text.hex(), installed_hex=installed_text.hex(),
            source_Japanese=clean_text.decode("cp932"), installed=installed_text.decode("ascii"),
            widget_index=3, dispatcher_call=0x0203FE98, fleet_list=0x020406E4, selected_detail=0x020407E0,
            reason="Fleet Info conveys that the player is opening information about a fleet."),
        offline=results, earlier_ordinary_regional_orders=dict(receipt=reference(LEGACY), observed_path=calls,
            destination_formatter_calls=0),
        scope=dict(known_indirect_Missionary_path_resolved=True, original_regional_picker_can_supply_114=False,
            whole_legacy_widget_and_other_fleet_destination_writers_open=True, actual_text_draw_or_new_gameplay_proven=False,
            new_editorial_credit=0, ROM_changed=False, full_goal_complete=False)))
    print("116 original destination cases and 259 picker results per ROM. Only supplied slot 114 selects Missionary.")


if __name__ == "__main__":
    main()
