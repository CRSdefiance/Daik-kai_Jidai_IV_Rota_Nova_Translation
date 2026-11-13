"""Read sealed source/current/draft triples in complete exchange order."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load

ROOT = Path('work/Maria_B37_B50_clean_20261109')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('first', type=int)
    ap.add_argument('last', type=int)
    args = ap.parse_args()
    drafts = load(ROOT/'all286_clean_meanings_andindependent_drafts_v2.json')
    current = load(ROOT/'current_v1/current_effective.json')
    objects = load(ROOT/'current_objects_v1/current_objects.json')
    byid = {r['id']: r for g in current['groups'] for r in g['records']}
    byid.update({r['id']: r for r in objects['choice_records']})
    assert len(byid) == 286
    for block in range(args.first, args.last+1):
        rows = [r for r in drafts['records'] if r['block'] == block]
        print('\nBLOCK', block, 'CONTEXT:', rows[0]['whole_exchange_context'])
        for row in rows:
            c = byid[row['id']]
            assert c['source_reference'] == row['source_reference'] and c['source_hex'] == row['source_hex']
            print(row['source_record_index'], 'selector', row.get('source_selector'), 'J:', row['source_Japanese'].replace('\n', ' / '))
            print(' C:', c['current_comparison_paragraph'])
            print(' D:', row['independent_English_draft'])

if __name__ == '__main__':
    main()
