"""Read sealed drafts/current prose in complete-exchange order, without truncation."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['drafts','current','objects']:ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--blocks',type=int,nargs='+',required=True)
    ap.add_argument('--include-japanese',action='store_true'); args=ap.parse_args()
    drafts,current,objects=map(load,[args.drafts,args.current,args.objects])
    sealed=load(Path(current['clean_meanings']).parent/'sealed_drafts.json')
    assert digest(args.drafts)==sealed['independent_drafts_sha256']
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    assert len(bound)==len(drafts['records']) and current['runtime']==objects['runtime']
    assert set(args.blocks)<={r['block'] for r in drafts['records']}
    for block in args.blocks:
        print('\nCOMPLETE EXCHANGE',block)
        for row in (r for r in drafts['records'] if r['block']==block):
            old=bound[row['id']]
            assert row['source_hex']==old['source_hex'] and row['source_reference']==old['source_reference']
            print(row['id'],'A'+str(row.get('source_selector','choice')))
            if args.include_japanese:print(' J:',row['source_Japanese'].replace('\n',' / '))
            print(' C:',old['current_comparison_paragraph'])
            print(' D:',row['independent_English_draft'])

if __name__=='__main__':main()
