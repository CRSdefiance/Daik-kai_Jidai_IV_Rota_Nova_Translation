"""Make whole-exchange contact sheets from exact completed final-plan records."""
import argparse
from PIL import Image, ImageDraw
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def pages(row):
    value=row['complete_native_English_display']
    return value['pages'] if row['kind']=='progressive' else [value]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--blocks',nargs='+',type=int,required=True)
    args=parser.parse_args()
    doc=load(ROOT/'formatting_FE_v1/physical_manuscript.json')
    plans={r['id']:r for r in load(ROOT/'plan_visual_v4/automatic_plans.json')['records']}
    reused=load(ROOT/'native_final_selection_v1.json')['exact_reused_records']
    folder=ROOT/'selected_review_sheets_v1';folder.mkdir(exist_ok=True)
    for block in args.blocks:
        target=folder/f'B{block}_pages.json';assert not target.exists()
        selected={r['id']:dict(record=r['record'],path=r['path'],sha256=r['sha256']) for r in reused if r['record']['block']==block}
        freshpath=ROOT/f'native_final_v1/B{block}_checked.json'
        if freshpath.exists():
            for row in load(freshpath)['records']:
                assert row['id'] not in selected
                journal=ROOT/('native_final_v1/complete_'+row['id']+'.json')
                proof=load(journal)
                assert proof['record']==row and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
                inputs=load(proof['native_run_inputs'])
                assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256'] and inputs['runtime']==doc['runtime']
                selected[row['id']]=dict(record=row,path=str(journal),sha256=digest(journal))
        originals=[r for r in doc['records'] if r['block']==block and r['kind'] in ['progressive','system-FE']]
        assert selected.keys()=={r['id'] for r in originals}
        members=[];pictures=[]
        for original in originals:
            binding=selected[original['id']];row=binding['record'];plan=plans[row['id']]
            assert digest(binding['path'])==binding['sha256']
            assert row['logical_English']==original['english'] and row['compiled_hex']==plan['encoded_hex']
            assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
            assert len(row['native_alignment']['cases'])==4 and len(pages(row))==plan['expected_native_pages']
            for number,panel in enumerate(pages(row),1):
                assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
                members.append(dict(id=row['id'],page=number,preview=panel['preview'],preview_sha256=panel['preview_sha256'],
                    native_plane_sha256=panel['native_plane_sha256'],native_receipt=binding['path'],native_receipt_sha256=binding['sha256']))
                with Image.open(panel['preview']) as picture:pictures.append((row['id']+f' p{number}',picture.convert('RGB')))
        sheets=[]
        for start in range(0,len(pictures),12):
            part=pictures[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
            for index,(label,picture) in enumerate(part):
                x,y=index%2*456,index//2*160
                draw.text((x+3,y+3),label+' offline QA',fill='white')
                sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
            path=folder/f'B{block}_part{start//12+1}.png';assert not path.exists();sheet.save(path)
            sheets.append(dict(path=str(path),sha256=digest(path),pages=len(part)))
        save(target,dict(block=block,records=[selected[r['id']]['record'] for r in originals],pages=len(members),
            selected_page_receipts=members,review_sheets=sheets,direct_visual_review_pending=True,actual_gameplay=False,new_credit=0))
        print('Staged final-plan exchange',block,len(originals),'bodies',len(members),'pages',len(sheets),'sheets.')

if __name__=='__main__':main()
