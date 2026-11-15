"""Bound original specialty response fragments and two shop reply call sites."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_responses_v751')
ITEM, GOODS, VTABLE, GETTER, ITEM_NAME, GOODS_NAME, ACTOR, TOWN = (
    0x02450000, 0x02450100, 0x02450200, 0x02450300, 0x02450400, 0x02450500, 0x02450600, 0x02450700)


def specialty(arm):
    rows = []
    for answer in (0, 1):
        cpu = machine(arm)
        cpu.mem_write(ITEM, struct.pack('<I', VTABLE))
        cpu.mem_write(GOODS, struct.pack('<I', VTABLE))
        cpu.mem_write(VTABLE + 8, struct.pack('<I', GETTER))
        cpu.mem_write(ITEM_NAME, b'Tomato Seeds\0')
        cpu.mem_write(GOODS_NAME, b'Tomatoes\0')
        cpu.mem_write(GOODS + 14, bytes((0x20,)))
        cpu.mem_write(STACK, struct.pack('<I', ACTOR))
        for register, value in ((UC_ARM_REG_R4, 0), (UC_ARM_REG_R5, GOODS), (UC_ARM_REG_R6, ITEM),
                (UC_ARM_REG_R7, TOWN), (UC_ARM_REG_R8, 0), (UC_ARM_REG_SP, STACK)):
            cpu.reg_write(register, value)
        events = []

        def bridge(u, address, size, unused, events=events, answer=answer):
            if address == GETTER:
                result = ITEM_NAME if u.reg_read(UC_ARM_REG_R0) == ITEM else GOODS_NAME
            elif address == BASE + 0x53F9C:
                assert u.reg_read(UC_ARM_REG_R1) == 742
                assert u.reg_read(UC_ARM_REG_R2) == ITEM_NAME and u.reg_read(UC_ARM_REG_R3) == GOODS_NAME
                events.append({'message': 742, 'question': True, 'item_pointer': ITEM_NAME, 'product_pointer': GOODS_NAME})
                result = answer
            elif address == BASE + 0x53FE4:
                events.append({'message': u.reg_read(UC_ARM_REG_R1), 'question': False})
                result = 0
            elif address in (BASE + 0xB3A6C, BASE + 0x4A610, BASE + 0x49F30, BASE + 0x4A5AC):
                result = 0
            elif address in (BASE + 0xBAD98, BASE + 0xBADB4):
                u.emu_stop()
                return
            else:
                return
            u.reg_write(UC_ARM_REG_R0, result)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, bridge)
        try:
            cpu.emu_start(BASE + 0xBAD0C, BASE + 0xBADC8, count=1000)
        finally:
            cpu.hook_del(hook)
        assert [e['message'] for e in events] == [742, 743 if answer else 744]
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE + (0xBAD98 if answer else 0xBADB4)
        assert cpu.mem_read(GOODS + 14, 1)[0] == (0x21 if answer else 0x20)
        rows.append({'supplied_question_answer': answer, 'original_messages': events,
            'original_local_specialty_flag_result': cpu.mem_read(GOODS + 14, 1)[0],
            'fragment': [0xBAD0C, 0xBADB4], 'eligibility_inventory_transfer_and_recursive_propagation_not_executed': True})
    return rows


def literal_calls(arm):
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    rows = []
    for fn_start, fn_end in ((0xBBF00, 0xBC260), (0xBC894, 0xBCA30)):
        for x in cs.disasm(arm[fn_start:fn_end], BASE + fn_start):
            if x.mnemonic.startswith('ldr') and x.op_str.startswith('r1, [pc,'):
                literal = x.address + 8 + x.operands[1].mem.disp - BASE
                if struct.unpack_from('<I', arm, literal)[0] != 746:
                    continue
                following = list(cs.disasm(arm[x.address - BASE:x.address - BASE + 12], x.address))
                call_site = next(y.address for y in following if y.mnemonic == 'bl' and y.op_str == '#0x2053fe4')
                rows.append({'message': 746, 'literal': literal, 'instruction': x.address,
                    'mnemonic': x.mnemonic, 'operand': x.op_str, 'ordinary_portrait_call': call_site})
    assert len(rows) == 2
    assert struct.unpack_from('<I', arm, 0xBA48C)[0] == 745
    # Original loop explicitly loads745 into fp, then forwards it to the
    # ordinary portrait consumer when the selected menu action needs a reply.
    code = list(cs.disasm(arm[0xBA3D4:0xBA430], BASE + 0xBA3D4))
    assert (code[0].mnemonic, code[0].op_str) == ('ldr', 'fp, [pc, #0xb4]')
    assert any(x.address == BASE + 0xBA420 and x.mnemonic == 'mov' and x.op_str == 'r1, fp' for x in code)
    assert any(x.address == BASE + 0xBA428 and x.op_str == '#0x2053fe4' for x in code)
    rows.append({'message': 745, 'literal': 0xBA48C, 'source_loop_span': [0xBA3D4, 0xBA430],
        'ordinary_portrait_call': 0x020BA428})
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v750_candidate.nds').read_file('/__arm9__.bin')
    spans = ((0xBAB64, 0xBADC8), (0xBA3D4, 0xBA490), (0xBBF00, 0xBC2B4), (0xBC894, 0xBCA48))
    assert all(clean[a:b] == current[a:b] for a, b in spans)
    a, b = specialty(clean), specialty(current)
    assert a == b
    calls = literal_calls(clean)
    assert literal_calls(current) == calls
    trend = read('work/analysis/town_events_v750/native_context.json')
    assert all(clean[r['start']:r['end']] == current[r['start']:r['end']] for r in trend['original_code_spans'])
    save(ROOT / 'native_context.json', {'source_spans': [{'start': a, 'end': b, 'sha256': sha(clean[a:b])} for a, b in spans],
        'two_source_specialty_response_fragments_each_clean_and_current': a,
        'shop_literal_and_caller_evidence': calls,
        'trend288_original_cases_carried_forward_from': 'work/analysis/town_events_v750/native_context.json',
        'trend_report_sha256': sha(Path('work/analysis/town_events_v750/native_context.json').read_bytes()),
        'not_whole_specialty_eligibility_or_inventory_transfer_verification': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Specialty743/744 fragments and shop745/746 caller evidence pass clean/current; eligibility remains separate.', flush=True)


if __name__ == '__main__':
    main()
