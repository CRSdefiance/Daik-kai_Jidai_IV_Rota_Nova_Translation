"""Render all pixel-bound actual dialogue pages compactly;keep optional full-screen scene samples."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--full-scene-ids',nargs='*',default=[])
    args=parser.parse_args();assert not args.out.exists();proof=load(args.proof)
    assert proof['all_complete_native_body_andheader_planes_andblank_guards_match'] and proof['all_selected_pages_observed_in_exact_fixture_order']
    ordered=[(r['id'],r['page']) for r in proof['ordered_selected_source_calls']];assert len(set(ordered))==len(ordered)
    selected=[next(s for s in proof['body_pages'] if (s['id'],s['page'])==key) for key in ordered]
    assert len(selected)==proof['selected_pages']
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18);args.out.mkdir();sheets=[]
    for start in range(0,len(selected),12):
        part=selected[start:start+12];sheet=Image.new('RGB',(1536,((len(part)+2)//3)*410),'#eee');draw=ImageDraw.Draw(sheet)
        for i,sample in enumerate(part):
            cap=sample['capture'];path=Path(cap['path']);assert sha(path.read_bytes())==cap['PNG_sha256']
            im=Image.open(path).convert('RGB');assert im.size==(256,384)
            x,y=i%3*512,i//3*410
            draw.text((x+4,y+4),sample['id'].replace('DK4_MES_','')+f" p{sample['page']} @{sample['frame']}",font=font,fill='black')
            sheet.paste(im.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+25))
        png=args.out/f'actual_dialogue_{len(sheets)+1}.png';sheet.save(png)
        sheets.append(dict(path=str(png),sha256=sha(png.read_bytes()),pages=len(part),full_original_capture_refs=[s['capture'] for s in part]))
    whole=[]
    if args.full_scene_ids:
        samples=[next(s for s in selected if s['id']==ident) for ident in args.full_scene_ids]
        for start in range(0,len(samples),6):
            part=samples[start:start+6];sheet=Image.new('RGB',(1536,((len(part)+2)//3)*800),'#eee');draw=ImageDraw.Draw(sheet)
            for i,sample in enumerate(part):
                x,y=i%3*512,i//3*800;draw.text((x+4,y+4),sample['id'].replace('DK4_MES_','')+f" @{sample['frame']}",font=font,fill='black')
                sheet.paste(Image.open(sample['capture']['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST),(x,y+25))
            png=args.out/f'full_scene_{len(whole)+1}.png';sheet.save(png);whole.append(dict(path=str(png),sha256=sha(png.read_bytes()),pages=len(part)))
    save(args.out/'receipt.json',dict(actual_pixel_proof=str(args.proof),actual_pixel_proof_sha256=sha(args.proof.read_bytes()),
        actual_dialogue_pages=len(selected),bottom_screen_sheets=sheets,full_scene_sheets=whole,
        original_complete_captures_preserved_crop_is_QA_view_only=True,direct_visual_review_pending=True,new_credit=0,guide_photos=False))
    print(len(selected),'actual pages on',len(sheets),'compact sheets and',len(whole),'full-scene sheets;all originalcaptures preserved.')
