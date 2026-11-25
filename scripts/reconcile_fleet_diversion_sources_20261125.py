"""Characterize original scheduled fleet-diversion inputs on the current ROM."""

from collections import Counter
from struct import pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_REG_PC, ARM_REG_R1, ARM_REG_SP
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from scripts import reconcile_fleet_destination_writers_20261123 as earlier
from scripts import register_seoul_reika_20261125 as current
from scripts.checkpoint_pending_shared_native_20261115 import branch_hits, find
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = earlier.OUT.with_name("fleet_diversion_sources_current_20261125.json")
BASE, CONSTRUCTOR = earlier.BASE, earlier.CONSTRUCTOR
STORY, MENU = earlier.STORY_TYPE6, earlier.MENU_TYPE6
FLEET_TARGET, PICKER_BUILD, PICKER, PICKER_CAP = 0x02057068, 0x0209B144, 0x02057104, 20
TABLE, TOWNS, CLASS, VIEW, EVENT = 0x023F1400, 0x023FA000, 0x023F2000, 0x023F2400, 0x023F3000
CALENDAR, CALENDAR_DAY = 0x022CFD54, 0x1234
TEST_ACTIVITY = 0x0202C000
GATEWAY = {0x020CB178, 0x020B6618, 0x020B2B48, TEST_ACTIVITY, 0x020B50D8, 0x020B4AA8}
STACK_TYPES = {
    0x0203B2C8: (0x0203B178, 0x0203B188, 0x3C, 4),
    0x0203B32C: (0x0203B160, 0x0203B164, 0x44, 2),
    0x0203BB5C: (0x0203BA44, 0x0203BA48, 0x50, 8),
}


def bound_span(clean, installed, lo, hi):
    a, b = (earlier.code_at(raw, lo, hi) for raw in (clean, installed))
    assert len(a) == hi - lo and a == b, (hex(lo), hex(hi))
    return dict(start=lo, end=hi, sha256=sha256(a).hexdigest())


def constructor_sites(clean_rom, current_rom, clean, arm):
    def sites(rom):
        result = []
        for area, base, data in earlier.loaded_components(rom):
            result.extend((area, pc, kind) for pc, _, kind in branch_hits(data, base, {CONSTRUCTOR}))
            result.extend((area, base + offset, "state-bit pointer word")
                          for offset in find(data, pack("<I", CONSTRUCTOR | 1)))
        return result

    inventory = read(earlier.OUT)["native_reference_census"][str(CONSTRUCTOR)]
    references = sites(clean_rom)
    assert references == sites(current_rom)
    assert references == [(*pair, "arm_bl") for pair in inventory["aligned_ARM_BL"]]
    assert len(references) == 31 and not inventory["aligned_exact_pointer"]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    cpu = machine(arm)
    result = []
    for area, pc, kind in references:
        setup = list(decoder.disasm(earlier.code_at(arm, pc - 24, pc), pc - 24))
        setter = next(ins for ins in reversed(setup) if ARM_REG_R1 in ins.regs_access()[1])
        if pc in STACK_TYPES:
            start, store, offset, event_type = STACK_TYPES[pc]
            source = list(decoder.disasm(earlier.code_at(arm, start, setter.address + 4), start))
            by_address = {ins.address: ins for ins in source}
            assert (source[0].mnemonic, source[0].op_str) == ("mov", f"r0, #{event_type}")
            assert (by_address[store].mnemonic, by_address[store].op_str) == ("str", f"r0, [sp, #{offset:#x}]")
            assert (setter.mnemonic, setter.op_str) == ("ldr", f"r1, [sp, #{offset:#x}]")
            assert not [ins for ins in source if store < ins.address < setter.address
                        and ins.mnemonic.startswith("str") and f"[sp, #{offset:#x}]" in ins.op_str]
            assert not [ins for ins in source if store < ins.address < setter.address and ARM_REG_SP in ins.regs_access()[1]]
            earlier.run_fragment(cpu, start, store + 4, ((UC_ARM_REG_SP, STACK),))
            assert bytes(cpu.mem_read(STACK + offset, 4)) == pack("<I", event_type)
            source_scope = bound_span(clean, arm, start, pc + 4)
        else:
            assert setter.mnemonic == "mov" and setter.operands[1].type == ARM_OP_IMM
            event_type = setter.operands[1].imm
            assert 0 <= event_type <= 9
            source_scope = bound_span(clean, arm, setter.address, pc + 4)
        assert not [ins for ins in setup if setter.address <= ins.address and ARM_REG_PC in ins.regs_access()[1]]
        earlier.run_fragment(cpu, setter.address, pc, ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_R1, 0xFFFFFFFF)))
        assert cpu.reg_read(UC_ARM_REG_R1) == event_type
        result.append(dict(component=area, call=pc, branch_kind=kind, type_load=setter.address,
                           event_type=event_type, stack_source=pc in STACK_TYPES, binding=source_scope))
    assert [row["call"] for row in result if row["event_type"] == 6] == [STORY, MENU]
    return result


def constructor_behavior(arm):
    cpu = machine(arm)
    assert unpack_from("<I", arm, 0x020CB1BC - BASE) == (CALENDAR,)
    cpu.mem_write(CALENDAR + 8, pack("<I", CALENDAR_DAY))
    assert earlier.code_at(arm, CONSTRUCTOR, CONSTRUCTOR + 4) == bytes.fromhex("10402de9")
    results = []
    for event_type in range(12):
        for town in (0, 89, 114, 115, 255):
            guard = b"\xa5" * 20
            cpu.mem_write(EVENT - 2, guard)
            cpu.mem_write(STACK, pack("<4I", 3, 2, town, 21))
            call(cpu, CONSTRUCTOR - BASE, (EVENT, event_type, 5, 1))
            expected = guard[:6] + bytes((event_type, 5, 1, 3, town, 21)) + guard[12:14] + pack("<I", CALENDAR_DAY + 96) + guard[18:]
            assert bytes(cpu.mem_read(EVENT - 2, len(guard))) == expected
            accepted = cpu.reg_read(UC_ARM_REG_R0)
            assert accepted == int(event_type < 10)
            results.append(dict(type=event_type, supplied_town=town, stored_town=town, accepted=bool(accepted)))
    return results


def menu_behavior(arm):
    cpu = machine(arm)
    cpu.mem_write(CLASS + 0x10, pack("<I", TEST_ACTIVITY))
    for index in range(115):
        cpu.mem_write(TOWNS + 4 + index * earlier.TOWN_STRIDE, pack("<I", CLASS))
    active = set()
    supplied_index, cap_observations, forwarded = -1, [], []

    def reply(uc, address, _size, _data):
        r0, r1 = (uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1))
        if address in GATEWAY:
            if address == 0x020CB178:
                answer = TOWNS
            elif address == 0x020B6618:
                answer = TOWNS + 4
            elif address == TEST_ACTIVITY:
                slot, rem = divmod(r0 - TOWNS - 4, earlier.TOWN_STRIDE)
                assert rem == 0 and 0 <= slot < 90
                answer = int(slot in active)
            else:
                answer = 1
        elif address == 0x02021478:
            assert r0 == 5
            cap_observations.append(r1)
            answer = TOWNS + 4 + r1 * earlier.TOWN_STRIDE
        elif address == 0x0209B36C:
            assert r0 == VIEW
            answer = 1
        elif address == 0x02053D44:
            assert r0 == 2 and r1 == 0x02118300
            answer = 0
        else:
            assert address == 0x0209B0D8 and r0 == TABLE and r1 == 90
            answer = supplied_index
        uc.reg_write(UC_ARM_REG_R0, answer & 0xFFFFFFFF)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hooked = GATEWAY | {0x02021478, 0x0209B36C, 0x02053D44, 0x0209B0D8}
    handles = [cpu.hook_add(UC_HOOK_CODE, reply, begin=pc, end=pc) for pc in hooked]
    try:
        for supplied in [set(), *({i} for i in range(115)), set(range(115))]:
            active = supplied
            expected = sorted(supplied.intersection(range(90)))
            cpu.mem_write(TABLE, b"\xa5" * (116 * 4))
            call(cpu, FLEET_TARGET - BASE, (0, TABLE), instruction_limit=5000)
            assert cpu.reg_read(UC_ARM_REG_R0) == len(expected)
            raw = bytes(cpu.mem_read(TABLE, 116 * 4))
            assert raw == pack(f"<{len(expected)}I", *expected) + b"\xa5" * ((116 - len(expected)) * 4)
        for count in (0, 1, 19, 20, 21, 90):
            cap_observations.clear()
            call(cpu, PICKER_BUILD - BASE, (VIEW, TABLE, count, 0x191))
            shown = min(count, PICKER_CAP)
            assert cap_observations == list(range(shown))
            assert unpack_from("<I", cpu.mem_read(VIEW + 0x26C, 4)) == (shown,)
        for supplied_index in (-1, *range(PICKER_CAP)):
            call(cpu, PICKER - BASE, (6, TABLE, 90))
            value = cpu.reg_read(UC_ARM_REG_R0)
            assert value == (115 if supplied_index < 0 else supplied_index)
            forwarded.append(dict(supplied_visible_index=supplied_index, target_slot=value))
    finally:
        for handle in handles:
            cpu.hook_del(handle)
    return dict(eligibility_cases=117, native_index_range=[0, 89], cap_rows=PICKER_CAP, menu_size_cases=6,
                displayed_row_and_cancel_cases=forwarded, cancel_slot=115,
                supplied_boundaries="Town predicates, list renderer and picker inputs were supplied offline.")


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean_rom, rom = (NdsImage.open(p) for p in (CLEAN, current.ROM))
    clean, arm = (image.read_file(current.ARM) for image in (clean_rom, rom))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    spans = [bound_span(clean, arm, lo, hi) for lo, hi in
             ((CONSTRUCTOR, 0x02093C04), (0x020CB1B4, 0x020CB1C0), (0x02056D48, 0x02056D70),
              (0x02056FA0, 0x02057010), (FLEET_TARGET, 0x02057194), (PICKER_BUILD, 0x0209B1B0))]
    data = constructor_sites(clean_rom, rom, clean, arm)
    story = []
    for side in (clean_rom, rom):
        archives = earlier.story_operands(side)
        assert all(row["type6_raw_candidates"] == 0 for row in archives)
        story.append([dict(path=row["path"], sha256=row["sha256"], blocks=row["sections"]) for row in archives])
    assert all(sum(row["blocks"] for row in side) == 2617 for side in story)
    menu = menu_behavior(arm)
    constructor = constructor_behavior(arm)
    sources = read(earlier.OUT)["menu_path"]
    assert sources["cancel_skips_constructor"] and sources["cancel_value"] == 115
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], verified_source_and_installed_spans=spans,
                    constructor_inputs=data, constructor_counts_by_type=Counter(row["event_type"] for row in data),
                    source_story_archive_scan=story[0], installed_story_archive_scan=story[1],
                    packed_type6_candidates_in_either_ROM=0, supplied_constructor_cases=constructor,
                    supplied_native_menu_cases=menu, earlier_fleet_writer_evidence=reference(earlier.OUT),
                    scope="The two mapped type-6 producers are the shipped story effect and the ordinary town menu. "
                          "No authored type-6 operand and no menu choice for slot 114 were found in these scopes. "
                          "Other computed references, external save data, and other ways of assigning a destination remain open.",
                    new_gameplay_runs=0, new_editorial_credit=0, ROM_changed=False))
    print("Classified all 31 inventoried calls and verified the native 20-row diversion picker and destination byte.")


if __name__ == "__main__":
    main()
