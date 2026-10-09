"""Prepare all nine reviewed native help pages and eight untranslated headings."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_help_release import (
    PRESENTATION,
    compile_records,
    sha,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage


def main():
    path = Path('translations/grand_race_rules_manuscript_v2.json')
    manuscript = json.loads(path.read_text(encoding='utf-8'))
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    japanese = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    proof = json.loads(Path('work/analysis/grand_race_help_consumer_proof.json').read_text())
    records, selections, used = compile_records(manuscript, source, japanese)
    batch = {'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
             'source_file_sha256': sha(source), 'target_locale': 'en-US',
             'scope': 'All nine complete Grand Race help bodies and eight untranslated native headings',
             'status': 'reviewed-experimental-runtime-pending',
             'native_text_repack': {'presentation': PRESENTATION, 'manuscript': str(path).replace('\\', '/'),
                                   'manuscript_sha256': sha(path.read_bytes()),
                                   'consumer_locks': proof['code_locks']},
             'records': records}
    validate_release_batch(batch, source)
    out = Path('translations/grand_race_help_arm9_v2.json')
    out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    Path('work/analysis/grand_race_help_release_plan.json').write_text(
        json.dumps({'batch': str(out), 'batch_sha256': sha(out.read_bytes()),
                    'formatted_region_bytes_used': used, 'region_bytes': 1796,
                    'free_bytes': 1796 - used, 'source_locked_patch_spans': len(records),
                    'selections': selections}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'pages': len(selections), 'new_headings': 8, 'patch_spans': len(records),
                      'formatted_region_used': used, 'free_bytes': 1796 - used}))


if __name__ == '__main__':
    main()
