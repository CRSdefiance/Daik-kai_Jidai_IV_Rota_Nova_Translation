"""Display all four complete verified native name masks for direct review."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_native_review_assets_v7987')
PROOF=Path('work/analysis/Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(PROOF);assert len(d['name_planes'])==4
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(896,320),'#263238');draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(d['name_planes']):
        pixels=Path(row['native_plane']).read_bytes();assert sha(pixels)==row['native_plane_sha256'] and len(pixels)==216*64
        im=Image.new('RGB',(216,64));im.putdata([(98,97,98) if p else (250,245,223) for p in pixels])
        x,y=i%2*448,i//2*160;draw.text((x+3,y+3),f"Actor{row['actor_ID']} {row['text']} original style11",fill='white')
        sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x,y+24))
    path=ROOT/'four_complete_current_names.png';sheet.save(path)
    save(ROOT/'review_sheet_receipt.json',dict(source=str(PROOF),source_sha256=sha(PROOF.read_bytes()),
        sheet=str(path),sheet_sha256=sha(path.read_bytes()),four_complete_native_masks_without_new_glyph_processing=True,
        visual_review_pending=True,not_actual_B47_nameplate_gameplay_orcatalogue_UI=True,new_credit=0,full_goal_complete=False))
    print(str(path))
