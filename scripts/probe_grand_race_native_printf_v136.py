"""Verify every complete result combination using the ROM's actual formatter."""

import json
import struct
from pathlib import Path

import unicorn

from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_grand_race_native_printf import execute
from scripts.probe_grand_race_result_rows import assemble_row


def main():
    proposal = Path('work/analysis/grand_race_complete_ui_proposal_v136')
    source = (proposal / 'proposed_arm9.bin').read_bytes()
    report = json.loads((proposal / 'report.json').read_text())
    if sha(source) != report['proposed_arm9_sha256']:
        raise ValueError('Complete proposed ARM9 differs')
    allocation_path = Path('work/analysis/grand_race_ui_allocation_v136/report.json')
    allocation = json.loads(allocation_path.read_text())
    labels = {}
    for selection in allocation['selections']:
        if selection['message'].startswith(('PLACE_', 'NUMBER_')):
            offset = struct.unpack_from('<I', source, selection['pointer_fields'][0])[0] - 0x02000000
            text = source[offset:source.index(0, offset)].decode('ascii')
            if text != selection['line']:
                raise ValueError('Native selector lost the complete result label')
            labels[selection['message']] = text
    if len(labels) != 8:
        raise ValueError('Complete eight result labels required')
    cases, executed = [], set()
    names = [b'A' * size for size in range(1, 17)] + ['ア'.encode('cp932') * size for size in (1, 4, 7, 8)]
    for place in range(1, 5):
        for player in range(1, 5):
            for name in names:
                label, number = labels[f'PLACE_{place}'], labels[f'NUMBER_{player}']
                proof = execute(source, label, number, name)
                expected, width = assemble_row(label, number, name)
                if bytes.fromhex(proof['full_row_hex']) != expected or width > 180:
                    raise ValueError('Native formatting or full row width differs')
                executed.update(proof.pop('executed_offsets'))
                cases.append({'place': place, 'player': player, 'name_hex': name.hex(), 'width_pixels': width, **proof})
    result = {'status': 'pass-actual-native-sprintf-all-reached-helpers',
              'proposed_arm9_sha256': sha(source), 'emulator': f'Unicorn {unicorn.__version__}',
              'allocation_sha256': sha(allocation_path.read_bytes()),
              'rom_written': False, 'runtime_verified': False, 'case_count': len(cases),
              'max_output_bytes_with_nul': max(case['bytes_with_nul'] for case in cases),
              'max_width_pixels': max(case['width_pixels'] for case in cases),
              'executed_offsets': sorted(executed), 'cases': cases,
              'limitations': ['Actual ARM formatter/core/parser/string/copy bodies executed without replacement helpers.',
                              'Native caller stack, preserved registers, exact bytes/NUL and all output neighbors verified.',
                              'Valid names initialized; this does not validate damaged incoming save/network fields.',
                              'Pixel width uses previously mapped native advances; frame artwork and gameplay remain unverified.',
                              'No registered batch/ROM, runtime acceptance or final formatting-gate promotion.']}
    Path('work/analysis/grand_race_native_printf_v136_proof.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'{len(cases)} actual native sprintf cases pass; all reached helper bodies execute, max 30 bytes including NUL.')


if __name__ == '__main__':
    main()
