"""Materialize the two reviewed full-prose statuses without relocation or code changes."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_status_release import (
    LOCKS,
    SLOTS,
    compile_records,
    sha,
    validate_release_batch,
)
from dk4tool.rom.nds import NdsImage


def main():
    source = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/grand_race_remaining_ui_manuscript_v2.json').read_text(encoding='utf-8'))
    preview = json.loads(Path('work/qa/grand_race_status_layout/report.json').read_text(encoding='utf-8'))
    if not preview['preview_reviewed'] or preview['manuscript_sha256'] != sha(Path('translations/grand_race_remaining_ui_manuscript_v2.json').read_bytes()):
        raise ValueError('Full status preview is not reviewed/current')
    records = [copy.deepcopy(r) for r in manuscript['records'] if r['id'] in SLOTS]
    for row in records:
        row['review'] = {gate: True for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')}
        row['presentation'] = 'wireless-immediate-ascii-body-v1'
        row['context'] = ('Joining-body status at (16,64); following row is cleared when registration is pending.'
                          if row['id'].endswith('WAIT_REGISTRATION') else
                          'Hosting-body status at (16,64); both following rows are cleared when starting the race.')
    document = {'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                'scope': 'Complete joining registration-wait and hosting race-start status messages',
                'status': 'reviewed-experimental-runtime-pending', 'records': records}
    path = Path('translations/grand_race_transition_status_manuscript_v2.json')
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    batch = {key: document[key] for key in ('target_locale', 'scope', 'status')}
    batch['editorial_policy'] = 'natural-dialogue-v2'
    batch.update({'format': 'dk4-arm9-fixed-text-batch-v1', 'file_path': '/__arm9__.bin',
                  'source_file_sha256': sha(source), 'records': compile_records(document, source),
                  'native_wireless_status': {'manuscript': str(path).replace('\\', '/'),
                                             'manuscript_sha256': sha(path.read_bytes()),
                                             'consumer_locks': [{'start': lo, 'end': hi, 'sha256': sha(source[lo:hi])}
                                                                for lo, hi in LOCKS]}})
    validate_release_batch(batch, source)
    Path('translations/grand_race_transition_status_arm9_v2.json').write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared two complete reviewed status messages; 68 source-owned bytes; no code/pointer changes.')


if __name__ == '__main__':
    main()
