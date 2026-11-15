"""Calibrate actual framebuffer menu highlights;retain the failed preview-RGB assumption."""
from pathlib import Path
from collections import Counter
from scripts.lil_B206_actual_source_v6318 import load
from scripts.native_B206_menu_backing_v6285 import paint
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B206_actual_menu_palette_v6318b')
if __name__=='__main__':
    assert not ROOT.exists();v=load('English','buy');arm=v['image'].read_file('/__arm9__.bin');rows=[]
    for frame,x,y,width,labels in [(6360,104,272,48,['Got it','So?']),(7380,71,272,114,["I'll take them!","That's expensive..."])]:
        photo,image=v['photos'][frame]
        for i,text in enumerate(labels):
            pixels,p=paint(arm,text.encode('ascii'),8,width,(0,i*12));expected={(j%width,j//width) for j,b in enumerate(pixels) if b};actual={(xx,yy) for yy in range(12) for xx in range(width) if image.getpixel((x+xx,y+i*20+yy))==(8,8,8)};assert actual==expected
            color=image.getpixel((x,y+i*20));assert color==((0,165,172) if i==0 else (205,198,180));counts=Counter(image.crop((x,y+i*20,x+width,y+i*20+12)).getdata());assert set(counts)=={color,(8,8,8)}
            rows.append(dict(frame=frame,option_index=i,label=text,background_RGB=list(color),complete_native_ink_pixels=len(expected),actual_ink_mask_exact=True,capture=photo['path'],capture_sha256=photo['PNG_sha256']))
    tool=derive('scripts/lil_B206_actual_masks_v6318.py','scripts/lil_B206_actual_masks_v6318b.py',{'(0,168,176) if index==selected else (204,198,180)':'(0,165,172) if index==selected else (205,198,180)'})
    ROOT.mkdir(parents=True);save(ROOT/'actual_highlight_palette_and_all_four_complete_buy_menu_labels.json',dict(rows=rows,actual_selected_background_RGB=[0,165,172],actual_unselected_background_RGB=[205,198,180],actual_ink_RGB=[8,8,8],original_preview_palette_was_not_actual_framebuffer_RGB=True,all_four_complete_glyph_masks_and_native_geometry_were_already_correct=True,derived_actual_checker=tool,no_ROM_native_font_geometry_or_capture_pixels_changed=True,no_menu_actual_approval_until_all_path_checks_pass=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())));print('Both actual buy menus/allfour labels match exact native glyphs. Checker now uses measured framebuffer highlight colors;preview-palette failure preserved.')
