"""Read complete clean/current/independent exchanges after the sealed source-first intake."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load

ROOT=Path('work/Maria_B58_B70_clean_20261109')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('blocks',type=int,nargs='+');args=parser.parse_args()
    doc=load(ROOT/'all303_clean_meanings_andindependent_drafts_v3.json')
    current=load(ROOT/'current_v1/current_effective.json');objects=load(ROOT/'current_objects_v1/current_objects.json')
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['choice_records']})
    assert len(bound)==len(doc['records'])==303
    for block in args.blocks:
        print('\nCOMPLETE EXCHANGE',block)
        for row in [r for r in doc['records'] if r['block']==block]:
            old=bound[row['id']];assert row['source_hex']==old['source_hex']
            print(row['id'],row['speaker'],'JP:',row['source_Japanese'].replace('\n',' / '))
            print(' CURRENT:',old['current_comparison_paragraph'])
            print(' DRAFT:  ',row['english'])
if __name__=='__main__':main()
