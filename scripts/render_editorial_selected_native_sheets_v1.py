"""Assemble exact selected native pages into readable sheets; never claim they have been viewed."""
import argparse
from collections import defaultdict
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['selection','out']:ap.add_argument('--'+arg,type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();selection=load(args.selection)
    assert selection['native_selection_complete'] and selection['remaining_records']==0
    rows=[];groups=defaultdict(list);runs={};case_count=0
    for binding in selection['reused_native_records']:
        path=Path(binding['receipt']);assert digest(path)==binding['receipt_sha256'];proof=load(path);row=proof['record']
        assert row['id']==binding['id'] and row['compiled_hex']==binding['compiled_hex']
        runpath=Path(proof['native_run_inputs']);assert digest(runpath)==proof['native_run_inputs_sha256']
        runs[str(runpath)]=load(runpath);rows.append(row);case_count+=len(row['native_alignment']['cases'])
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
        for n,page in enumerate(pages,1):
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            label=row['id']+(f' p{n}' if row['kind']=='progressive' else ' FE')
            groups[row['block']].append((label,page))
    assert len(rows)==selection['complete_body_candidates'] and case_count==4*len(rows)
    runtime=next(iter(runs.values()))['runtime'];font=next(iter(runs.values()))['font_sha256']
    assert all(r['runtime']==runtime and r['font_sha256']==font for r in runs.values())
    args.out.mkdir(parents=True);sheets=[]
    for block,pages in sorted(groups.items()):
        for start in range(0,len(pages),12):
            part=pages[start:start+12];sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
            for i,(label,page) in enumerate(part):
                picture=Image.open(page['preview']).convert('RGB');x,y=i%2*456,i//2*160
                draw.text((x+3,y+3),label+' offline QA',fill='white')
                sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
            output=args.out/f'B{block}_part{start//12+1}.png';sheet.save(output)
            sheets.append(dict(block=block,path=str(output),sha256=digest(output),pages=len(part),
                exact_selected_pages=[dict(label=label,preview=page['preview'],preview_sha256=page['preview_sha256']) for label,page in part]))
    save(args.out/'selected_native_pages.json',dict(records=rows,records_count=len(rows),pages=sum(map(len,groups.values())),runtime=runtime,font_sha256=font,
        selected_completed_alignment_cases=case_count,source_receipt_selection=str(args.selection),source_receipt_selection_sha256=digest(args.selection),
        review_sheets=sheets,all_selected_runtime_font_macro_source_current_compiled_glyph_andbounds_receipts_exact=True,
        existing_completed_native_cases_reused_not_reexecuted=True,direct_visual_review_pending=True,formatting_gates_still_false=True,
        actual_gameplay=False,new_credit=0,producer_sha256=digest(__file__)))
    print(dict(records=len(rows),pages=sum(map(len,groups.values())),alignments=case_count,sheets=len(sheets),direct_visual_review_pending=True))

if __name__=='__main__':main()
