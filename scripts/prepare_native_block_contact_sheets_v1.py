"""Make legible review sheets from only complete native block receipts."""
import argparse
from pathlib import Path
import subprocess
import sys
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-root',type=Path,required=True)
    parser.add_argument('--blocks',type=int,nargs='+',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists() and len(set(args.blocks))==len(args.blocks)
    parts=[args.native_root/f'B{n}_checked.json' for n in args.blocks]
    assert all(p.is_file() for p in parts)
    rows=[r for p in parts for r in load(p)['records']]
    args.out.mkdir();inputs=args.out/'staged_previews';inputs.mkdir()
    pages=[]
    for row in rows:
        rendered=row['complete_native_English_display']
        items=[dict(page=1,preview=rendered['preview'],preview_sha256=rendered['preview_sha256'])] if row['kind']=='system-FE' else rendered['pages']
        for item in items:
            source=Path(item['preview']);assert sha(source.read_bytes())==item['preview_sha256']
            picture=Image.open(source).convert('RGB');assert picture.size in [(216,64),(228,64)]
            canvas=Image.new('RGB',(456,128),(239,232,201))
            canvas.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(0,0))
            staged=inputs/f'{len(pages)+1:04d}_{row["id"]}_p{item["page"]}.png';canvas.save(staged)
            pages.append(dict(id=row['id'],page=item['page'],source=str(source),source_sha256=sha(source.read_bytes()),
                staged=str(staged),staged_sha256=sha(staged.read_bytes())))
    helper=Path('scripts/build_preview_contact_sheets.py')
    subprocess.run([sys.executable,str(helper),str(inputs),str(args.out/'sheets'),'--columns','3','--rows','6'],check=True,stdout=subprocess.DEVNULL)
    sheets=sorted((args.out/'sheets').glob('*.png'),key=lambda p:int(p.stem.split('_')[-1]))
    assert len(sheets)==(len(pages)+17)//18
    save(args.out/'contact_manifest.json',dict(blocks=args.blocks,records=len(rows),pages=pages,
        readable_2x_nearest_native_pixels_no_content_changed=True,
        sheets=[dict(path=str(p),sha256=sha(p.read_bytes()),page_indices=list(range(i*18,min((i+1)*18,len(pages))))) for i,p in enumerate(sheets)],
        complete_block_receipts={str(p):sha(p.read_bytes()) for p in parts},
        helper_sha256=sha(helper.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),direct_visual_review_pending=True,new_credit=0))
    print(len(rows),'complete native records /',len(pages),'pages /',len(sheets),'readable sheets. Direct review pending.',flush=True)
