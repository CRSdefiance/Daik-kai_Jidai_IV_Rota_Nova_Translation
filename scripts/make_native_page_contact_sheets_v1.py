"""Collect every page of a native receipt into readable nonduplicated review sheets."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    native=load(args.receipt);pictures=[];seen=set()
    for row in native['records']:
        rendered=row['complete_native_English_display']
        pages=rendered['pages'] if row['kind']=='progressive' else [rendered]
        for index,page in enumerate(pages,1):
            key=(row['id'],index);assert key not in seen;seen.add(key)
            assert digest(page['preview'])==page['preview_sha256']
            assert digest(page['native_plane'])==page['native_plane_sha256']
            pic=Image.open(page['preview']).convert('RGB');assert pic.height==64 and pic.width in [216,228]
            pictures.append((row['id']+f' p{index}',pic,dict(id=row['id'],page=index,
                preview=page['preview'],preview_sha256=page['preview_sha256'],native_plane_sha256=page['native_plane_sha256'])))
    assert len(pictures)==native['pages']
    args.out.mkdir(parents=True);sheets=[]
    for start in range(0,len(pictures),12):
        part=pictures[start:start+12]
        sheet=Image.new('RGB',(912,((len(part)+1)//2)*160),'#263238');draw=ImageDraw.Draw(sheet)
        for index,(label,pic,_) in enumerate(part):
            x,y=index%2*456,index//2*160;draw.text((x+3,y+3),label+' offline QA',fill='white')
            sheet.paste(pic.resize((pic.width*2,128),Image.Resampling.NEAREST),(x,y+24))
        path=args.out/f'part{start//12+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=digest(path),pages=len(part),members=[p[2] for p in part]))
    save(args.out/'contact_sheet_manifest.json',dict(receipt=str(args.receipt),receipt_sha256=digest(args.receipt),
        pages=len(pictures),records=len(native['records']),review_sheets=sheets,
        every_native_page_represented_exactly_once=True,nearest_neighbor_2x_no_text_orfont_changes=True,
        direct_visual_review_pending=True,actual_gameplay=False,new_credit=0))
    print('Created',len(sheets),'readable sheets covering all',len(pictures),'native pages exactly once.')


if __name__=='__main__':main()
