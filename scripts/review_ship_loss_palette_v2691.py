"""Color the already-verified full palette planes;binary sheets hide gray detail."""
from pathlib import Path
from collections import Counter
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.verify_village_wrap_v608 import read,save
import struct

ROOT=Path('work/analysis/ship_loss_palette_v2691')
PROOF=Path('work/analysis/ship_loss_fonts_v2690b/native_font_and_pipeline_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(PROOF);image=NdsImage.open(proof['candidate']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    palette=struct.unpack('<16H',resident(arm,PALETTE,32));colors={0:(255,255,255),1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
    assert colors[1]==(0,8,0) and colors[15]==(197,198,197)
    selections=[(2078,('長崎丸'*3).encode('cp932').hex()),(2076,('F'+'A'*17).encode().hex()),(2078,b'Santa Maria'.hex()),(2078,b"F's Hope".hex()),(2099,'ＦＡＬＣＯＮ'.encode('cp932').hex()),(2099,b'%s%o%09d'.hex())]
    ROOT.mkdir(parents=True);samples=[]
    for n,hx in selections:
        case=next(c for c in proof['cases'] if c['message_ID']==n and c['name_case']['hex']==hx)
        pixels=bytes(independent_font(arm,font,case['lines']));assert sha(pixels)==case['full_palette_font_plane_sha256'] and set(pixels)<=colors.keys()
        plane=Image.new('RGB',(228,64));plane.putdata([colors[p] for p in pixels]);path=ROOT/f'ID{n}_name{hx}_source_palette.png';plane.save(path)
        samples.append(dict(message_ID=n,name_hex=hx,lines=case['lines'],pixel_index_counts=dict(Counter(pixels)),
            whole_palette_plane_equals_previously_executed_native_SHA=True,preview=str(path),preview_sha256=sha(path.read_bytes())))
    sheet=Image.new('RGB',(936,456),'#263238');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(samples):
        x,y=i%2*468,i//2*152;draw.text((x+5,y+3),f'ID{s["message_ID"]}: native ink + gray; controlled preview',fill='white')
        sheet.paste(Image.open(s['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
    out=ROOT/'source_palette_CJK_fullwidth_and_data.png';sheet.save(out)
    save(ROOT/'palette_review.json',dict(candidate=proof['candidate'],candidate_sha256=proof['candidate_sha256'],native_proof=str(PROOF),native_proof_sha256=sha(PROOF.read_bytes()),
        colors={str(k):v for k,v in colors.items()},samples=samples,review_sheet=str(out),review_sheet_sha256=sha(out.read_bytes()),
        binary_previews_are_coverage_masks_not_actual_ink_color=True,
        dense_CJK_in_binary_mask_is_not_a_new_font_or_overlap_finding=True,
        all_colors_map_verified_current_full_native_planes_no_ROM_or_prose_change=True,
        controlled_white_paper_preview_not_an_actual_gameplay_capture=True,
        visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('6source-palette previews bind exact full native plane hashes;gray detail is distinct frombinary coverage masks. No ROM/font/prose change.')
