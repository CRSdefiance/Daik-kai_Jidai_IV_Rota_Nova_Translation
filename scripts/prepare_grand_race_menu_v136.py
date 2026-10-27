"""Create reviewed native menu labels and exact consumer gates for V136."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import (
    LOCKS,
    SLOTS,
    compile_records,
    sha,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    manuscript = json.loads(path.read_text(encoding='utf-8'))
    preview = json.loads(Path('work/qa/grand_race_menu_label_layout/report.json').read_text())
    if preview['manuscript_sha256'] != sha(path.read_bytes()) or not all(r['preview_reviewed'] for r in preview['selections']):
        raise ValueError('Reviewed label preview is stale')
    if preview['preview_sha256'] != sha(Path('work/qa/grand_race_menu_label_layout/sheet.png').read_bytes()):
        raise ValueError('Reviewed preview pixels changed')
    rows = [copy.deepcopy(r) for r in manuscript['records'] if r['id'] in SLOTS]
    for row in rows:
        row['review'] = dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)
        row['localization_note'] = 'Faithful complete menu label. Native 48-byte copier preserves every ASCII character; centered 84-by-20 label area reviewed. Full-screen runtime pending.'
    document = {'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US', 'records': rows,
                'status': 'reviewed-experimental-runtime-pending'}
    output = Path('translations/grand_race_menu_manuscript_v2.json')
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    batch = {'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
             'editorial_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
             'source_file_sha256': sha(source), 'records': compile_records(document, source),
             'native_menu_labels': {'manuscript': output.as_posix(), 'manuscript_sha256': sha(output.read_bytes()),
                                    'consumer_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])} for lo, hi in LOCKS]}}
    validate_release_batch(batch, source)
    Path('translations/grand_race_menu_arm9_v2.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Six complete native menu labels prepared; no code or pointer changes.')


if __name__ == '__main__':
    main()
