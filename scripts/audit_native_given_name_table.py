"""Audit source/current table selections through actual ordinary character getter.

The 207-entry inspection range follows the native ordinary-object initialization
loop. This does not establish which indices are valid fleet captains.
"""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for


def string(raw, pointer):
    at = pointer - BASE
    if not 0 <= at < len(raw):
        return {'pointer': pointer, 'status': 'outside-arm9-static-text'}
    end = raw.find(b'\0', at)
    if end < 0:
        return {'pointer': pointer, 'status': 'no-static-nul'}
    encoded = raw[at:end]
    try:
        text = encoded.decode('cp932')
    except UnicodeDecodeError:
        return {'pointer': pointer, 'offset': at, 'hex': encoded.hex(), 'status': 'invalid-cp932'}
    printable = all(c.isprintable() or c in '\r\n\t\u3000' for c in text)
    return {'pointer': pointer, 'offset': at, 'hex': encoded.hex(), 'text': text,
            'byte_length': len(encoded), 'status': 'printable-static-string' if printable else 'nonprintable-static-payload'}


def ordinary_getter(raw, index, machine=None):
    machine = machine_for(raw) if machine is None else machine
    root = struct.unpack_from('<I', raw, 0xCB18C)[0]
    actor = root + 4 + index * 32
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_R0, actor)
    machine.emu_start(BASE + 0x7EB3C, STOP, count=10)
    machine.reg_write(UC_ARM_REG_R0, actor)
    machine.emu_start(BASE + 0x7EB0C, STOP, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Actual ordinary given-name getter fails to return')
    return machine.reg_read(UC_ARM_REG_R0)


def main():
    parent = Path('out/all_routes_combined_v147_candidate.nds')
    current = NdsImage.open(parent).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if sha(current) != '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75':
        raise ValueError('Exact V147 required')
    spans = [(0x7EB0C, 0x7EB4C), (0x7EE08, 0x7EE20), (0x7F1F4, 0x7F254),
             (0x7F254, 0x7F2AC), (0xCDAB4, 0xCDAC4), (0xCB184, 0xCB190)]
    if any(current[a:b] != clean[a:b] for a, b in spans):
        raise ValueError('Native ordinary given-name consumer/initialization differs')
    base = struct.unpack_from('<I', current, 0xCDAC0)[0] - BASE
    rows = []
    for index in range(207):
        field = base + index * 32
        source_pointer, current_pointer = [struct.unpack_from('<I', raw, field)[0] for raw in (clean, current)]
        if ordinary_getter(current, index) != current_pointer:
            raise ValueError('Actual getter differs from static table selection')
        original, translated = string(clean, source_pointer), string(current, current_pointer)
        rows.append({'index': index, 'table_field': field, 'source': original, 'current': translated,
                     'source_pointer_preserved': source_pointer == current_pointer,
                     'actual_ordinary_constructor_index_and_getter_verified': True,
                     'source_bytes_unchanged': original.get('hex') == translated.get('hex')})
    suspicious = [r['index'] for r in rows if r['current']['status'] != 'printable-static-string']
    japanese = [r['index'] for r in rows if any('\u3040' <= c <= '\u30ff' or '\u3400' <= c <= '\u9fff'
                                              for c in r['current'].get('text', ''))]
    result = {'status': 'pass-native-table-audit-followup-required', 'candidate_sha256': sha(parent.read_bytes()),
              'arm9_sha256': sha(current), 'ordinary_inspection_count': 207, 'table_base': base,
              'rows': rows, 'nonprintable_or_invalid_current_indices': suspicious,
              'japanese_current_indices': japanese,
              'consumer_locks': [{'start': a, 'end': b, 'sha256': sha(current[a:b])} for a, b in spans],
              'limits': ['Ordinary zero-type character objects are constructed as fixtures; all 207 selections execute the actual getter chain.',
                         'Initialization-loop range does not establish valid captain IDs or virtual class ownership for every index.',
                         'Player interface, mutable names, runtime text/rendering and visible use of flagged records remain unverified.',
                         'Printable suffixes or unrelated strings may also be wrong; this audit is not a complete fidelity verdict.']}
    Path('work/analysis/native_given_name_table_v147_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'207 actual ordinary getter selections audited; {len(suspicious)} nonprintable/invalid current results and {len(japanese)} Japanese results require classification.')


if __name__ == '__main__':
    main()
