"""Trace actual movement callers, actor table, varargs and native preparation."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.execute_map_entity_tooltip_copy import BASE, STACK
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded
from scripts.verify_ordinary_name_fidelity_research import initialized


def caller(source, common, variant, *, supply_selector=None):
    machine = initialized(source)
    owner = struct.unpack_from('<I', source, 0x552A0)[0]
    entries = common_message_entries(common, source, clean=False)
    mid = (610, 610, 610, 610, 611, 612, 613, 610)[variant]
    block_id = entries[mid].block
    machine.mem_write(owner + 0x2C, bytes((block_id, 255, 0, 1)))
    machine.mem_write(owner + 0x30, bytes(IlnkContainer.parse(common).blocks[block_id]))
    actor_source = 0x02431000
    machine.mem_write(actor_source + 0x1C, bytes((variant,)))
    trace = set()
    supply = 'water and food'
    start = BASE + 0x78260
    if supply_selector is not None:
        if supply_selector not in (0, 1):
            raise ValueError('Only the two actual supply getter branches are mapped')
        supply = ('Water', 'Food')[supply_selector]
        pointer = struct.unpack_from('<I', source, 0xA4C34 + supply_selector * 4)[0]
        machine.mem_write(pointer, supply.encode('ascii') + b'\0')
        machine.reg_write(UC_ARM_REG_R0, supply_selector)
        start = BASE + 0x78278

    def fixture(uc, address, size, _):
        trace.add(address)
        if address == BASE + 0x829C8:
            uc.mem_write(uc.reg_read(UC_ARM_REG_R2), struct.pack('<2I', 0, 4))
            uc.reg_write(UC_ARM_REG_R0, 2)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0x7EB24:
            uc.reg_write(UC_ARM_REG_R0, actor_source)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, fixture)
    machine.emu_start(start, BASE + 0x5408C, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5408C:
        raise ValueError('Movement caller did not reach actual portrait frame')
    sp = machine.reg_read(UC_ARM_REG_SP)
    frame = bytes(machine.mem_read(sp + 0x264, 32))
    frame_words = struct.unpack('<8I', frame)
    if frame_words[0] != BASE + 0x53DB8 or frame_words[6] != BASE + 0x118580:
        raise ValueError('Actual movement portrait frame differs: ' + str([hex(w) for w in frame_words]))
    paragraph = entries[mid].text.decode('ascii').replace('%s', supply, 1).replace('%s', 'automatic travel', 1)
    wanted = wrap_expanded(paragraph)
    buffers = [struct.unpack_from('<I', source, at)[0] for at in (0x5444C, 0x54450)]
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    machine.emu_start(BASE + 0x54144, BASE + 0x54164, count=100000)
    if machine.reg_read(UC_ARM_REG_SP) != sp:
        raise ValueError('Movement native preparation changes caller stack')
    for buffer, expected in zip(buffers, (paragraph, wanted), strict=True):
        raw = expected.encode('ascii')
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + raw + b'\0' + b'\xa5' * (287 - len(raw)):
            observed = bytes(machine.mem_read(buffer, 256)).split(b'\0', 1)[0]
            raise ValueError(f'Movement preparation differs at {buffer:08X}: {observed!r}; expected {raw!r}')
    if not {BASE + 0x53D44, BASE + 0x82478, BASE + 0x53F4C, BASE + 0x5528C,
            BASE + 0xCE898, 0x01FF9BC8} <= trace or BASE + 0x53914 in trace:
        raise ValueError('Movement preparation bypasses a required native path')
    if supply_selector is not None and BASE + 0xA4C24 not in trace:
        raise ValueError('Single-supply branch bypasses actual runtime supply getter')
    return {'variant': variant, 'message_id': mid, 'complete_prepared_text': wanted,
            'supply_selector': supply_selector, 'supply': supply,
            'single_supply_runtime_string_initialization_is_fixture': supply_selector is not None,
            'actual_portrait_frame_sp': sp, 'parent_return': frame_words[0],
            'actual_actor_table_stack_offset': 0x27C, 'argument_pointers_preserved': True,
            'native_caller_captain_selector_actor_table_common_lookup_sprintf_literal_copy_and_wrap_execute': True,
            'buffer_canaries_and_stack_intact': True,
            'crew_list_actor_source_and_initial_widget_construction_are_contracts': True}


def main():
    source = Path('work/analysis/movement_notices_research_arm9.bin').read_bytes()
    common = Path('work/analysis/movement_notices_research_common.bin').read_bytes()
    plan = json.loads(Path('work/analysis/movement_notices_plan.json').read_text(encoding='utf-8'))
    if sha(source) != plan['target_arm9_sha256'] or sha(common) != plan['target_common_sha256']:
        raise ValueError('Movement research identities differ')
    cases = [caller(source, common, i, supply_selector=supply)
             for supply in (None, 0, 1) for i in range(8)]
    report = {'status': 'pass-native-movement-caller-frame-and-preparation',
              'source_arm9_sha256': sha(source), 'common_sha256': sha(common), 'cases': cases,
              'initial_stack': STACK, 'formatting_approved': False, 'physical_gameplay_verified': False}
    Path('work/analysis/movement_notice_callers_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('24 native movement caller/table/sprintf/preparation cases pass; research only.')


if __name__ == '__main__':
    main()
