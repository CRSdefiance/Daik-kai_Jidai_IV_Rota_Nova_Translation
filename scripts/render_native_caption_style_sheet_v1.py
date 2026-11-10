"""Render every checked native caption style,including state15,without rerunning its painter."""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--proofs',nargs='+',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();pictures=[];records=[]
    colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
    for path in args.proofs:
        proof=load(path);assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        for row in proof['records']:
            binary=Path(row['path']);raw=binary.read_bytes();assert sha(raw)==row['sha256'] and set(raw)<=set(colors)
            width,height=row['logical_width_px'],row['logical_height_px'];assert len(raw)==width*height and height==12
            pic=Image.new('RGB',(width,height));pic.putdata([colors[v] for v in raw]);pictures.append((row,pic))
            records.append(dict(proof=str(path),proof_sha256=sha(path.read_bytes()),plane=str(binary),plane_sha256=sha(raw),
                version=row['version'],option=row['option'],style=row['style'],text=row['text'],complete_native_pixels_reused=True))
    args.out.mkdir();sheet=Image.new('RGB',(1100,((len(pictures)+1)//2)*66),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(row,pic) in enumerate(pictures):
        x,y=i%2*550,i//2*66
        draw.text((x+4,y+2),row['version']+f" option{row['option']} style{row['style']}",fill='white')
        sheet.paste(pic.resize((pic.width*3,36),Image.Resampling.NEAREST),(x+4,y+22))
    png=args.out/'all_caption_styles.png';sheet.save(png)
    save(args.out/'receipt.json',dict(records=records,planes=len(records),sheet=str(png),sheet_sha256=sha(png.read_bytes()),
        actual_display_palette_not_reinferred_from_this_offline_sheet=True,direct_visual_review_pending=True,new_credit=0))
    print('Rendered',len(records),'already native-checked caption planes,all styles;direct visual review pending.')
