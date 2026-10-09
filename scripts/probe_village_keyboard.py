"""Execute original keyboard tables and real selected-key insertion/capacity path."""

import json
import struct
from pathlib import Path

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
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_promised_words_release import PAIRS
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized

PARENT, POPUP, RESULT, KEYS = 0x02431000, 0x02436000, 0x02438000, 0x02439000


def word(machine, address):
    return struct.unpack('<I', machine.mem_read(address, 4))[0]


def write_word(machine, address, value):
    machine.mem_write(address, struct.pack('<I', value))


def read_string(machine, address, size=128):
    return bytes(machine.mem_read(address, size)).split(b'\0', 1)[0]


def scene(source, plan, *, marked=True):
    machine = initialized(source)
    # Two constructor assignments are actual native code; other widget/bitmap
    # constructors are outside this input byte-path fixture.
    machine.reg_write(UC_ARM_REG_R4, PARENT)
    machine.emu_start(BASE + 0xB07C0, BASE + 0xB07D0, count=1000)
    original_provider = word(machine, PARENT + 4)
    expected = plan['keyboard_wrapper']
    if original_provider != expected['original_provider_vtable']:
        raise ValueError('Native constructor provider differs')
    header = expected['header_pointer'] if marked else BASE + 0x156074
    for reg, value in ((UC_ARM_REG_R0, PARENT), (UC_ARM_REG_R1, RESULT),
                       (UC_ARM_REG_R2, 18), (UC_ARM_REG_R3, header)):
        machine.reg_write(reg, value)
    machine.emu_start(BASE + 0xAEBE0, BASE + 0xAFBB0, count=1000)
    selected = expected['provider_vtable'] if marked else original_provider
    if word(machine, PARENT + 4) != selected or machine.reg_read(UC_ARM_REG_R2) != 18:
        raise ValueError('Editor marker scope or input limit differs')
    if bytes(machine.mem_read(selected, 8)) != bytes(machine.mem_read(original_provider, 8)):
        raise ValueError('Marked provider methods differ from original')
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.mem_write(RESULT, b'\0')
    contracts = []

    def cursor_and_drawing(uc, address, size, data):
        if address in (BASE + 0xB0B7C, BASE + 0xB0C70):
            child = uc.reg_read(UC_ARM_REG_R0)
            if child != PARENT + 0x38:
                raise ValueError('Cursor/drawing contract selects a different child')
            if address == BASE + 0xB0B7C:
                cursor = min(uc.reg_read(UC_ARM_REG_R1), len(read_string(uc, child + 0x7C)))
                write_word(uc, child + 0x40, cursor)
            contracts.append(address)
            ret = uc.reg_read(UC_ARM_REG_LR)
            for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12):
                uc.reg_write(reg, 0xDEAD0000)
            uc.reg_write(UC_ARM_REG_PC, ret)

    machine.hook_add(UC_HOOK_CODE, cursor_and_drawing)
    # Real AFE58 writes parent+D8, aliases child+38+A0, and initializes its text.
    for reg, value in ((UC_ARM_REG_R0, PARENT), (UC_ARM_REG_R1, 18), (UC_ARM_REG_R2, RESULT)):
        machine.reg_write(reg, value)
    machine.emu_start(BASE + 0xAFE58, STOP, count=10000)
    if word(machine, PARENT + 0xD8) != 18 or word(machine, PARENT + 0x38 + 0xA0) != 18:
        raise ValueError('Actual parent setter does not configure the child capacity')
    if machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Actual editor setter fails to return with intact stack')
    # Original native resource-name lookup selects Latin and symbol pages.
    pages = {}
    for label, at, expected_index in (('英', 0x15510C, 50), ('記', 0x1550F4, 51)):
        machine.reg_write(UC_ARM_REG_R0, PARENT + 4)
        machine.reg_write(UC_ARM_REG_R1, BASE + at)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0xD1E3C, STOP, count=100000)
        index = machine.reg_read(UC_ARM_REG_R0)
        if index != expected_index:
            raise ValueError('Functional keyboard resource-name lookup fails')
        for reg, value in ((UC_ARM_REG_R0, PARENT + 4), (UC_ARM_REG_R1, index),
                           (UC_ARM_REG_R2, KEYS), (UC_ARM_REG_R3, 0)):
            machine.reg_write(reg, value)
        write_word(machine, STACK, 0xFFFFFFFF)
        machine.reg_write(UC_ARM_REG_LR, STOP)
        machine.emu_start(BASE + 0xD1BBC, STOP, count=100000)
        count = machine.reg_read(UC_ARM_REG_R0)
        raw = bytes(machine.mem_read(KEYS, count * 2))
        decoded = raw.decode('cp932')
        if len(decoded) != count:
            raise ValueError('Actual native keyboard cells are not complete CP932 pairs')
        pages[index] = {'label': label, 'native_keys': decoded, 'raw_hex': raw.hex(), 'count': count}
    return machine, pages, contracts


def selected_key(machine, pages, character, initial=b''):
    page = next(index for index, data in pages.items() if character in data['native_keys'])
    index = pages[page]['native_keys'].index(character)
    child = PARENT + 0x38
    write_word(machine, POPUP + 0x5C, PARENT)
    write_word(machine, POPUP + 0x68, page)
    write_word(machine, POPUP + 0x6C, pages[page]['count'])
    write_word(machine, POPUP + 0x50, 0)
    write_word(machine, POPUP + 0x44, 0)
    machine.mem_write(child + 0x7C, b'\xa5' * 33)
    machine.mem_write(child + 0x7C, initial + b'\0')
    write_word(machine, child + 0x40, len(initial))
    write_word(machine, child + 0xA0, 18)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.mem_write(STACK, b'\xa5' * 16)
    machine.reg_write(UC_ARM_REG_R4, index)
    machine.reg_write(UC_ARM_REG_R5, POPUP)
    entered, seen = [], set()

    def trace(uc, address, size, data):
        seen.add(address)
        if address == BASE + 0xAED2C:
            entered.append(read_string(uc, uc.reg_read(UC_ARM_REG_R1), 3))

    hook = machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(BASE + 0xAECD8, BASE + 0xAED30, count=100000)
    machine.hook_del(hook)
    result = read_string(machine, child + 0x7C, 33)
    incoming = character.encode('cp932')
    if entered != [incoming] or not {BASE + 0xD1BBC, BASE + 0xB08D8, BASE + 0xB0A14} <= seen:
        raise ValueError('Selected key bypasses native table generation/append/full return')
    if (machine.reg_read(UC_ARM_REG_SP) != STACK or len(result) > 18
            or bytes(machine.mem_read(child + 0x7C + 19, 14)) != b'\xa5' * 14
            or bytes(machine.mem_read(STACK + 7, 9)) != b'\xa5' * 9):
        raise ValueError('Real key callback damages text capacity, surrounding bytes or stack')
    return result, {'page': page, 'key_index': index, 'fullwidth_key': character,
                    'native_generated_hex': incoming.hex(), 'result_hex': result.hex(),
                    'actual_callback_reader_normalizer_append_and_return_executed': True,
                    'guards_and_stack_intact': True}


def main():
    source = Path('work/analysis/village_promised_words_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    if sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Prepared village keyboard source differs')
    machine, pages, contracts = scene(source, plan)
    if pages[50]['native_keys'] != ''.join(chr(i) for i in range(0xFF41, 0xFF5B)) + ''.join(chr(i) for i in range(0xFF21, 0xFF3B)):
        raise ValueError('Actual Latin table differs from complete lower/upper alphabet')
    keys = []
    for marked in (True, False):
        current, actual_pages, _ = scene(source, plan, marked=marked)
        for page in actual_pages.values():
            for character in page['native_keys']:
                result, case = selected_key(current, actual_pages, character)
                normalized = (chr(ord(character) - 0xFEE0) if 'Ａ' <= character <= 'Ｚ' or 'ａ' <= character <= 'ｚ' or '０' <= character <= '９' else ' ' if character == '\u3000' else character).encode('cp932')
                expected = normalized if marked else character.encode('cp932')
                if result != expected:
                    raise ValueError('Village normalization or unchanged non-village keyboard differs')
                keys.append({**case, 'marked_village': marked})
    answers = []
    for index, (answer, _) in enumerate(PAIRS):
        built, events = b'', []
        for char in answer:
            fullwidth = '\u3000' if char == ' ' else chr(ord(char) + 0xFEE0)
            built, case = selected_key(machine, pages, fullwidth, built)
            events.append(case)
        if built != answer.encode('ascii'):
            raise ValueError('Real keyboard cannot enter a complete localized answer')
        # Native completion copies the actual child text into the 19-byte caller
        # destination. Initialize only the surrounding parent state/vtable.
        machine.mem_write(RESULT - 16, b'\xa5' * 51)
        vtable = word(machine, PARENT)
        state = PARENT + struct.unpack('<i', machine.mem_read(vtable - 0x10, 4))[0]
        write_word(machine, state + 0x24, 0)
        machine.reg_write(UC_ARM_REG_R6, PARENT)
        machine.reg_write(UC_ARM_REG_R5, RESULT)
        machine.emu_start(BASE + 0xAFC44, BASE + 0xAFC6C, count=10000)
        expected = b'\xa5' * 16 + built + b'\0' + b'\xa5' * (34 - len(built))
        if bytes(machine.mem_read(RESULT - 16, 51)) != expected:
            raise ValueError('Actual input completion copy damages caller destination or neighbors')
        answers.append({'index': index, 'answer': answer, 'actual_key_events': events,
                        'native_completion_copy_and_19_byte_destination_intact': True})
    boundaries = []
    for size in (16, 17, 18):
        for character in ('Ａ', 'ｚ', '０', '\u3000', '☆'):
            result, case = selected_key(machine, pages, character, b'A' * size)
            normalized = 'A' if character == 'Ａ' else 'z' if character == 'ｚ' else '0' if character == '０' else ' ' if character == '\u3000' else character
            incoming = normalized.encode('cp932')
            expected = b'A' * size + (incoming if size + len(incoming) <= 18 else b'')
            if result != expected:
                raise ValueError('Real key boundary truncates, splits or overflows a key')
            boundaries.append({**case, 'initial_bytes': size})
    proof = {'status': 'pass-real-village-key-generation-normalization-and-input-byte-path',
             'arm9_sha256': sha(source), 'native_pages': pages, 'key_cases': keys,
             'complete_answer_cases': answers, 'boundary_cases': boundaries,
             'actual_capacity_alias': {'parent_D8': 18, 'child_38_plus_A0': 18, 'same_address': PARENT + 0xD8},
             'cursor_and_drawing_are_contracts': True, 'cursor_drawing_contract_calls': len(contracts),
             'limitations': ['Widget/bitmap construction, actual input device events and full hardware gameplay remain unproven.',
                             'Original case-sensitive comparison is preserved; choose capitals from the Latin page as spelled.']}
    Path('work/analysis/village_promised_words_keyboard_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(keys)} village/unchanged-page key cases; {len(answers)} full keyboard answers and caller copies; {len(boundaries)} boundary cases pass.')


if __name__ == '__main__':
    main()
