"""Retain the native coordinate pairs as readable units in faithful prose."""

import re
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_conversations_v765')
SOURCE = Path('translations/tavern_conversations_editorial_manuscript_v2.json')
MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v3.json')


def coordinate_splits(result, values):
    if result['id'] != 842: return []
    coordinates = ' '.join(values[0].decode('ascii').split())
    return [m.group() for m in re.finditer(r'\b[NSEW] \d+\b', coordinates)
            if not any(m.group() in line for line in result['lines'])]


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True, exist_ok=True)
    old = read('work/analysis/tavern_storage_v764/full_mapped/native_layout_matrix.json')
    failures = []
    for row in old['cases']:
        split = coordinate_splits(row, [bytes.fromhex(v) for v in row['values_hex']])
        if split: failures.append({**row, 'split_coordinate_pairs': split})
    assert failures
    doc = deepcopy(read(SOURCE))
    row = next(r for r in doc['records'] if r['message_id'] == 842)
    assert row['japanese'] == '詳しい位置は…そうねえ\n%sのあたりかしら'
    assert row['english'] == 'The exact location? Hmm... Somewhere around %s, I think.{PAD}'
    row['english'] = 'Where exactly? Hmm... Around %s, I think.{PAD}'
    row['localization_note'] += ' V3 uses the idiomatic rhetorical Where exactly and tentative Around/I think for the source detailed-position hesitation. This preserves all meaning while avoiding redundant Somewhere around. The visual review found compass-letter/number separation in the older draft;each original coordinate pair must now remain on one rendered line.'
    doc['unpublished_visual_refinement'] = {'prior_manuscript': str(SOURCE), 'sha256': sha(SOURCE.read_bytes()),
        'only_English_change': 842, 'late_visual_finding': 'Compass letter and number split across rows despite complete bytes and no basic width/weak-ending failures.',
        'prior_provider_role_correction_applies_to_V1_to_V2_only': True,
        'source_meaning_and_every_coordinate_letter_digit_preserved': True}
    assert all(not r['review']['formatting'] for r in doc['records'])
    save(MANUSCRIPT, doc)
    save(ROOT / 'coordinate_visual_finding.json', {'previous38957_matrix_basic_findings': old['findings_count'],
        'new_semantic_coordinate_pair_split_count': len(failures), 'cases': failures,
        'previous_draft_unpublished_not_a_shipped_ROM_regression': True,
        'new_English': row['english'], 'producer_sha256': sha(Path(__file__).read_bytes())})
    print(f'{len(failures)} previously split coordinate pairs recorded;842 prose refined;full recheck required.', flush=True)


if __name__ == '__main__': main()
