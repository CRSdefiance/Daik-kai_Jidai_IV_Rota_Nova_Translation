"""Prepare the canonical-source inline repair dependency for complete race UI."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.name_editor_atomic_append import END, START, apply
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batches
from scripts.execute_grand_race_name_append import execute

BASELINE = Path('out/raphael_natural_v2_accepted_base.nds')
BASELINE_SHA = '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
BATCH = Path('translations/name_editor_atomic_append_arm9_v1.json')


def main():
    if sha(BASELINE.read_bytes()) != BASELINE_SHA:
        raise ValueError('Canonical baseline differs')
    source = NdsImage.open(BASELINE).read_file('/__arm9__.bin')
    patched = apply(source)
    proof_path = Path('work/analysis/grand_race_name_append_v136_proof.json')
    proof = json.loads(proof_path.read_text())
    if len(proof['repaired_cases']) != 34 or any(
            not case['full_return'] or not case['stack_balanced'] for case in proof['repaired_cases']):
        raise ValueError('Full insertion-function boundary proof missing')
    for size in range(17):
        for inserted in (b'B', 'ア'.encode('cp932')):
            case = execute(patched, b'A' * size, inserted, 16, full_return=True)
            expected = b'A' * size + (inserted if size + len(inserted) <= 16 else b'')
            if bytes.fromhex(case['result_hex']) != expected:
                raise ValueError('Canonical native insertion boundary failed')
    batch = {
        'format': 'dk4-arm9-fixed-text-batch-v1', 'content_type': 'arm9-inline-code-v1',
        'file_path': '/__arm9__.bin', 'source_file_sha256': sha(source),
        'status': 'prepared-experimental-unregistered-runtime-pending',
        'scope': 'Whole-character end insertion; preserves configured name capacity and NUL.',
        'verification': {'proof_path': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
                         'cases': 34, 'full_native_frame_and_return': True,
                         'external_helpers': 'Cursor/drawing contracts, caller-register poisoning; not gameplay.'},
        'records': [{'id': 'NAME_EDITOR_ATOMIC_END_APPEND', 'offset': START,
                     'runtime_address': 0x02000000 + START,
                     'source_hex': source[START:END].hex(),
                     'replacement_hex': patched[START:END].hex()}]
    }
    BATCH.write_text(json.dumps(batch, indent=2) + '\n')
    actual, ids = apply_arm9_fixed_batches([BATCH], source)
    if actual != patched or ids != ['NAME_EDITOR_ATOMIC_END_APPEND']:
        raise ValueError('Integrated builder changed prepared inline repair')
    print('Canonical-source 40-byte inline repair prepared; builder and 34 full-return cases pass; unregistered.')


if __name__ == '__main__':
    main()
