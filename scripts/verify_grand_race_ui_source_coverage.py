"""Reconcile race manuscript parts and all referenced wireless-pool candidates."""

import hashlib
import json
from pathlib import Path

from scripts.prepare_grand_race_remaining_ui_manuscript import CANDIDATE_SHA


def main():
    manuscript_path = Path('translations/grand_race_remaining_ui_manuscript_v2.json')
    inventory_path = Path('work/analysis/arm9_text_inventory_v134_expanded.json')
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    if inventory['candidate_sha256'] != CANDIDATE_SHA:
        raise ValueError('Expanded inventory is for a different candidate')
    rows = inventory['records']
    covered = []
    for row in manuscript['records']:
        for part in row['source_parts_in_reading_order']:
            matches = [item for item in rows if item['component'] == 'arm9'
                       and item['offset'] == part['offset'] and item['text'] == part['japanese']
                       and item['nul_terminated'] and item['current_hex'] == part['source_hex'][:-2]]
            if len(matches) != 1:
                raise ValueError(f"Inventory misses exact source {part['offset']:#x}")
            fields = [ref['word_offset'] for ref in matches[0]['aligned_pointer_candidates']
                      if ref['component'] == 'arm9' and ref['interior_byte_offset'] == 0]
            if fields != part['aligned_pointer_fields']:
                raise ValueError('Native source reference coverage differs')
            covered.append({'id': row['id'], 'offset': part['offset'], 'pointer_fields': fields})
    if len(covered) != 59 or len({part['offset'] for part in covered}) != 59:
        raise ValueError('Expected the complete 59-part reviewed source set')
    owned = {part['offset'] for part in covered}
    exceptions = []
    for row in rows:
        if row['component'] != 'arm9' or not (0x16AFD0 <= row['offset'] < 0x16BAB0):
            continue
        refs = [ref for ref in row['aligned_pointer_candidates']
                if ref['component'] == 'arm9' and ref['interior_byte_offset'] == 0]
        if refs and row['nul_terminated'] and row['offset'] not in owned:
            exceptions.append({'offset': row['offset'], 'text': row['text'],
                               'pointer_fields': [ref['word_offset'] for ref in refs],
                               'classification': 'remaining-consumer-classification-required'})
    if {row['offset'] for row in exceptions} != {0x16AFD0, 0x16B482, 0x16B688}:
        raise ValueError('Wireless pool has a newly uncovered referenced candidate')
    report = {'status': 'all-59-reviewed-race-source-parts-covered-with-three-explicit-other-leads',
              'candidate_changed': False, 'candidate_sha256': CANDIDATE_SHA,
              'manuscript_sha256': hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
              'inventory_sha256': hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
              'source_parts': covered, 'other_referenced_pool_leads': exceptions,
              'limitations': ['Scoped coverage does not prove exhaustive UI completion.',
                             'The three other leads are retained for consumer classification, not declared unused.',
                             'Unreferenced strings and other address grammars require separate coverage.']}
    output = Path('work/analysis/grand_race_ui_v134_expanded_coverage.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'source_parts': len(covered),
                      'logical_messages': len(manuscript['records']), 'other_pool_leads': len(exceptions)}))


if __name__ == '__main__':
    main()
