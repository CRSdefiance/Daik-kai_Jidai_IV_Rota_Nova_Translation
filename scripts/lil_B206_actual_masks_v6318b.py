"""Exact native text/name and source-derived menu masks in actual framebuffer holds."""
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_B206_menu_backing_v6285 import paint
from scripts.verify_village_wrap_v608 import read
NAMES={2:'Lil Argot',7:'Cristina Erneco',173:'Shady Man'}
def match_English(version,font):
    byid={r['id']:r for r in font['cases']};glyphs=GameAsciiFont.from_arm9(version['image'].read_file('/__arm9__.bin'));observations=[];failures=[]
    for interval in version['speech_intervals']:
        case=byid[interval['id']];assert sha(Path(case['preview']).read_bytes())==case['preview_sha256'];preview=Image.open(case['preview']).convert('RGB');assert preview.size==(216,64)
        masks=[{(i%216,i//216) for i,c in enumerate(preview.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]];name=NAMES[interval['prefix']];namewidth=len(name)*6;nameink={(i*6+x,y) for i,c in enumerate(name) for y in range(11) for x in range(6) if glyphs.decode(c).getpixel((x,y))};holds=[]
        for frame,(photo,pic) in version['photos'].items():
            if not interval['interval']['start']<frame<interval['interval']['returned']:continue
            crop=pic.crop((16,296,232,360));actual=[{(i%216,i//216) for i,c in enumerate(crop.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]]
            if actual!=masks:continue
            actualname={(x-4,y-1) for y in range(13) for x in range(namewidth+8) if pic.getpixel((12+x,276+y))==(98,97,98)}
            if actualname!=nameink:continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],all216x64_ink_gray_pixels_equal_complete_native_plane=True,complete_current_nameplate_glyphs_and_blank_guards_equal=True))
        if not holds:failures.append(dict(id=interval['id'],path=version['path'],finding='No actual hold matches complete text and source-supported nameplate.'))
        observations.append(dict(id=interval['id'],path=version['path'],prefix=interval['prefix'],name=name,interval=interval['interval'],holds=holds,native_plane_sha256=case['whole_native_plane_sha256'],actual_complete_dialogue_and_nameplate_observed=bool(holds)))
    menu_cases=[]
    for interval in version['menu_intervals']:
        offset=interval['source_offset'];proofpath=Path(f'work/analysis/lil_B206_choices_v6286/B206_C{offset}/original_choice_decoder_VM_geometry_and_native_pixels.json');proof=read(proofpath);native=proof['current_and_reviewed_VM_and_font_cases'][1];vm=native['native_VM_getters_geometry_and_selection'];width=native['source_derived_text_canvas_width'];rect=vm['native_menu_rectangle'];origin=(rect[0]+16,192+rect[1]+16);arm=version['image'].read_file('/__arm9__.bin');masks=[]
        for index,label in enumerate(vm['labels']):
            pixels,p=paint(arm,label.encode('ascii'),8,width,(0,index*12));assert p['independent_complete_native_pixels_match'];masks.append({(i%width,i//width) for i,b in enumerate(pixels) if b})
        selected=interval['native_result'][1];earliest=interval['start']+30
        if selected==1:earliest=max(earliest,6305 if offset==852 else 7305)
        holds=[]
        for frame,(photo,pic) in version['photos'].items():
            if not earliest<frame<interval['returned']-3:continue
            actual=[{(x,y) for y in range(12) for x in range(width) if pic.getpixel((origin[0]+x,origin[1]+index*20+y))==(8,8,8)} for index in range(2)]
            backgrounds=[pic.getpixel((origin[0],origin[1]+index*20)) for index in range(2)];expected_bg=[(0,165,172) if index==selected else (205,198,180) for index in range(2)]
            if actual==masks and backgrounds==expected_bg:holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],both_full_labels_and_actual_selected_background_equal=True))
        if not holds:failures.append(dict(path=version['path'],menu_source_offset=offset,selected=selected,finding='No actual full-menu hold matches original native geometry,glyphs and selected option.'))
        menu_cases.append(dict(path=version['path'],source_command_offset=offset,interval=interval,labels=vm['labels'],native_rectangle=rect,caption_origin=list(origin),logical_caption_width=width,observed_selected_option=selected,holds=holds,source_native_proof=str(proofpath),source_native_proof_sha256=sha(proofpath.read_bytes()),actual_choice_label_order_selection_and_VM_return_bound=bool(holds)))
    return dict(speech_observations=observations,actual_menu_cases=menu_cases,failures=failures)
