"""Append a tribute-table-scoped portrait hook to the research ARM9."""

import json
import struct
from pathlib import Path

import ndspy.code
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R9,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_common_display_name_autoload import execute as autoload
from scripts.probe_common_display_name_hook import ARENA_LO_LITERAL, OVERLAY, branch_link
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_common_itcm_arena_reservation import verify as arena_verify
from scripts.probe_common_monthly_tribute_preparation import execute
from scripts.probe_common_scoped_word_wrap_hook import prepare as town_hook
from scripts.probe_common_scoped_word_wrap_hook import wrapper_bytes
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded
from scripts.probe_common_tribute_loaded_copy import research_dataset
from scripts.probe_common_tribute_modal_pixels import verify as pixels

CALL = 0x54160


def caller_frame(source, common, actor_index):
    machine = machine_for(source)
    resident = ndspy.code.MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    owner = struct.unpack_from('<I', source, 0x552A0)[0]
    block = bytes(IlnkContainer.parse(common).blocks[0])
    machine.mem_write(owner + 0x2C, bytes((0, 255, 0, 1)))
    machine.mem_write(owner + 0x30, block)
    actor, digits = 0x02428000, 0x02429000
    machine.mem_write(actor + 0x1C, bytes((actor_index,)))
    machine.mem_write(digits, '９９９９９９'.encode('cp932') + b'\0')
    for register, value in ((UC_ARM_REG_R0, 1), (UC_ARM_REG_R1, BASE + 0x1189C0), (UC_ARM_REG_R2, digits)):
        machine.reg_write(register, value)
    contracts = []

    def code(uc, address, size, _):
        if address == BASE + 0x7EB24:
            contracts.append(address)
            uc.reg_write(UC_ARM_REG_R0, actor)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    machine.hook_add(UC_HOOK_CODE, code)
    machine.emu_start(BASE + 0x53F0C, BASE + 0x5408C, count=100000)
    sp = machine.reg_read(UC_ARM_REG_SP)
    parent = struct.unpack('<I', machine.mem_read(sp + 0x264, 4))[0]
    table = struct.unpack('<I', machine.mem_read(sp + 0x274, 4))[0]
    argument = struct.unpack('<I', machine.mem_read(sp + 0x278, 4))[0]
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5408C or sp != STACK - 24 - 616
            or parent != BASE + 0x53F40 or table != BASE + 0x1189C0 or argument != digits
            or len(contracts) != 1):
        raise ValueError('Actual native caller does not establish the monthly scope frame')
    pointer = machine.reg_read(UC_ARM_REG_R9)
    text = bytes(machine.mem_read(pointer, 256)).split(b'\0', 1)[0].decode('cp932')
    formatted = struct.unpack_from('<I', source, 0x5444C)[0]
    expanded = struct.unpack_from('<I', source, 0x54450)[0]
    for buffer in (formatted, expanded):
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    # The widget/portrait setup between these segments remains a contract;
    # retain the actual caller frame, selected text and varargs state unchanged.
    machine.emu_start(BASE + 0x54144, BASE + 0x54164, count=100000)
    paragraph = text.replace('%s', '９９９９９９').encode('cp932')
    wrapped = wrap_expanded(paragraph.decode('cp932')).encode('cp932')
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x54164 or machine.reg_read(UC_ARM_REG_SP) != sp:
        raise ValueError('Connected monthly preparation loses the actual caller frame')
    for buffer, expected in ((formatted, paragraph), (expanded, wrapped)):
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + expected + b'\0' + b'\xa5' * (287 - len(expected)):
            raise ValueError('Connected actual caller loses full paragraph or output guards')
    return {'actor_index': actor_index, 'parent_return': parent, 'selector_table': table,
            'amount_argument_preserved': True, 'selected_text': text,
            'complete_prepared_text': wrapped.decode('cp932'),
            'caller_lookup_formatter_and_hook_share_one_machine': True,
            'initial_widget_construction_is_contract': True,
            'native_selector_and_common_lookup_executed': True,
            'actor_object_resolution_is_contract': True}


def prepare(source):
    town, placement = town_hook(source)
    code = ndspy.code.MainCodeFile(town, BASE)
    previous = [bytes(section.data) for section in code.sections]
    resident = code.sections[1]
    address = resident.ramAddress + len(resident.data)
    payload = wrapper_bytes(address, placement['helper_address'], monthly=True)
    if address + len(payload) > OVERLAY:
        raise ValueError('Monthly resident hook overlaps overlay')
    if struct.unpack_from('<I', previous[0], CALL)[0] != branch_link(BASE + CALL, BASE + 0x53914):
        raise ValueError('Original monthly macro call differs')
    resident.data.extend(payload)
    low = (resident.ramAddress + len(resident.data) + 31) & ~31
    expected = bytearray(previous[0])
    for at, value in ((CALL, branch_link(BASE + CALL, address)), (ARENA_LO_LITERAL, low)):
        struct.pack_into('<I', code.sections[0].data, at, value)
        struct.pack_into('<I', expected, at, value)
    for at in (code.codeSettingsOffs, code.codeSettingsOffs + 4):
        struct.pack_into('<I', expected, at, struct.unpack_from('<I', previous[0], at)[0] + len(payload))
    saved = bytes(code.save())
    loaded = ndspy.code.MainCodeFile(saved, BASE)
    if (bytes(loaded.sections[0].data) != expected or bytes(loaded.sections[1].data) != previous[1] + payload
            or bytes(loaded.sections[2].data) != previous[2]):
        raise ValueError('Monthly serialization changes unrelated code/data')
    return saved, {'wrapper_address': address, 'monthly_payload_bytes': len(payload),
                   'total_payload_bytes': len(resident.data) - 6944, 'reserved_arena_low': low}


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    saved, placement = prepare(source)
    dataset = research_dataset(saved)
    frames = [caller_frame(dataset.arm9, dataset.common, index) for index in range(8)]
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    english = {row['message_id']: row['english'].removesuffix('{PAD}') for row in manuscript['records']}
    for frame, message in zip(frames, (76, 77, 78, 79, 80, 81, 76, 82)):
        if frame['selected_text'] != english[message]:
            raise ValueError('Actual monthly selector/lookup does not preserve complete approved draft')
        frame['message_id'] = message
    cases = [{'message_id': row['message_id'], **execute(saved, row['english'].removesuffix('{PAD}'), amount,
                                                      actor, word_wrapped=True)}
             for row in manuscript['records'] if 76 <= row['message_id'] <= 82
             for amount in (0, 9, 10, 999999, 42949672) for actor in (1, 19)]
    unrelated = [execute(saved, "This unrelated message contains several complete words and %s gold coins.",
                         999999, 1, parent_return=parent, selector_table=table)
                 for parent, table in ((BASE + 0x53F40, BASE + 0x1189E0),
                                       (BASE + 0x54014, BASE + 0x1189C0),
                                       (BASE + 0x53FD0, BASE + 0x1189C0))]
    texts = list(dict.fromkeys(case['complete_prepared_text'] for case in cases if case['amount'] in (999999, 42949672)))
    rendered = [{'text': text, 'mode': mode,
                 'pixels_sha256': sha(pixels(source, font, text, mode, portrait=True, guarded=True)['pixels'])}
                for text in texts for mode in (4, 16)]
    runtime = initialize(saved)
    if runtime['low'][3] != placement['reserved_arena_low']:
        raise ValueError('Monthly hook is not reserved in initialized arena bounds')
    report = {'status': 'pass-research-monthly-caller-table-scoped-preparation-and-pixels',
              'source_sha256': sha(source), 'research_sha256': sha(saved), 'placement': placement,
              'arena': arena_verify(saved, placement['reserved_arena_low']), 'arena_initialization': runtime,
              'autoload': autoload(saved), 'cases': cases, 'unrelated_cases': unrelated, 'pixels': rendered,
              'native_caller_frames': frames,
              'limitations': 'Actual caller, selector, warm COMMON lookup, formatter, macros and wrapping share one machine; intervening initial widget construction is skipped explicitly and actor-object resolution is a contract. Full widget/portrait construction and caller-through-render execution, physical composition/input and gameplay remain pending. Raster is a separate unchanged-renderer invocation. Native ink sheets have a separately recorded visual review; no playable ROM is built.'}
    Path('work/analysis/common_monthly_word_wrap_arm9.bin').write_bytes(saved)
    Path('work/analysis/common_monthly_word_wrap_hook_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} monthly hooked preparations, {len(unrelated)} bypass cases and {len(rendered)} native pixel cases pass.')


if __name__ == '__main__':
    main()
