"""Prepare every canonical-source component of the remaining full race UI."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_complete_release import (
    ALLOCATION,
    CODE,
    DATA,
    DEPENDENCIES,
    MANUSCRIPT,
    compile_components,
    sha,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batches


def main():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    compiled, proposed = compile_components(source)
    batches = {}
    for kind, path in (('data', DATA), ('code', CODE)):
        batch = {'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
                 'source_file_sha256': sha(source), 'target_locale': 'en-US',
                 'status': 'prepared-experimental-unregistered-runtime-pending',
                 'scope': 'Complete 43-message remainder; eight inherited messages preserved',
                 'native_complete_race_ui': {
                     'component': kind, 'manuscript': MANUSCRIPT.as_posix(),
                     'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                     'allocation': ALLOCATION.as_posix(), 'allocation_sha256': sha(ALLOCATION.read_bytes()),
                     'dependencies': {p: sha(Path(p).read_bytes()) for p in DEPENDENCIES if p not in (DATA, CODE)}},
                 'records': compiled[kind]}
        if kind == 'code':
            batch['content_type'] = 'arm9-inline-code-v1'
        batches[path] = batch
    paths = [Path(path) for path in DEPENDENCIES]
    for path, batch in batches.items():
        validate_release_batch(batch, source, paths)
        Path(path).write_text(json.dumps(batch, indent=2) + '\n', encoding='utf-8')
    rebuilt, ids = apply_arm9_fixed_batches(paths, source)
    for batch in batches.values():
        for row in batch['records']:
            lo, size = row['offset'], len(bytes.fromhex(row['source_hex']))
            if rebuilt[lo:lo + size] != proposed[lo:lo + size]:
                raise ValueError('Integrated builder did not preserve complete UI component')
    report = {'status': 'prepared-complete-release-components-unregistered-runtime-pending',
              'message_count': 51, 'remaining_message_count': 43, 'saved_string_count': 60,
              'data_records': len(compiled['data']), 'code_records': len(compiled['code']),
              'builder_record_count': len(ids), 'rom_written': False, 'runtime_verified': False,
              'components': {path: sha(Path(path).read_bytes()) for path in DEPENDENCIES},
              'next': 'Register full combined profile, replace original help variant, build and verify saved ROM.'}
    Path('work/analysis/grand_race_complete_release_preparation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"Full race UI components prepared: {len(compiled['data'])} data / {len(compiled['code'])} instruction records; all six dependencies pass integrated builder.")


if __name__ == '__main__':
    main()
