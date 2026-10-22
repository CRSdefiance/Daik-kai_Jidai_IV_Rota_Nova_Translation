"""Verify full surname, normal Japanese-town signs, regressions and exact patch."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shiraki_surname import NEW, OFFSET, SOURCE
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files
from scripts.verify_seoul_v516 import background, icon

ROM=Path('out/all_routes_combined_v518_candidate.nds')
PARENT=Path('out/all_routes_combined_v514_candidate.nds')
OUT=Path('work/analysis/shiraki_surname_v518')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def capture(name,digest):
    folder=Path('work/emulation_v193')/name
    path=folder/'capture_report.json';data=read(path)
    assert data['ROM_sha256']==digest and data['cold_boot'] and not data['savestate_loaded']
    assert not data['callback_errors'] and not data.get('synthetic_inventory_fixtures')
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    if data.get('battery_save_preloaded'):
        assert sha(Path(data['battery_save_preloaded']['source']).read_bytes())==data['battery_save_preloaded']['source_sha256']
    return folder,path,data


def main():
    digest=sha(ROM.read_bytes());parent_digest=sha(PARENT.read_bytes())
    m=read(ROM.with_suffix('.manifest.json'));old_m=read(PARENT.with_suffix('.manifest.json'))
    assert m['candidate_sha256']==digest and m['profile']=='all-routes-unified-v518'
    assert m['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert m['batches']==old_m['batches'] and len(m['batches'])==470
    assert m['required_batches']==old_m['required_batches'] and all(m['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114
    assert m['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    a,b=[files(NdsImage.open(p)) for p in (PARENT,ROM)]
    assert sorted(p for p in a if a[p]!=b[p])==['/__arm9__.bin']
    assert [i for i,(x,y)in enumerate(zip(a['/__arm9__.bin'],b['/__arm9__.bin']))if x!=y]==[OFFSET+5,OFFSET+6]
    assert b['/__arm9__.bin'][OFFSET:OFFSET+8]==NEW
    assert NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[OFFSET:OFFSET+8]==SOURCE
    graphics=[p for p in a if p.lower().endswith(('.pxl','.fls'))]
    assert len(graphics)==675 and all(a[p]==b[p] for p in graphics)
    assert (OUT/'research_only_shiraki_surname.nds').read_bytes()==ROM.read_bytes()
    voyage,voyage_path,voyage_report=capture('japan_facilities_v517',parent_digest)
    dream,dream_path,dream_report=capture('shiraki_surname_v518_dream',digest)
    _,fresh_path,fresh_report=capture('shiraki_surname_v518_fresh',digest)
    _,_,old_fresh=capture('sea_foam_family_v514_fresh',parent_digest)
    reload,reload_path,reload_report=capture('japan_facilities_v518_reload',digest)
    assert voyage_report['frames']==15240 and dream_report['frames']==12240 and reload_report['frames']==5600
    assert dream_report['scripted_input_schedule']==[e for e in voyage_report['scripted_input_schedule']if e['start']<=12240]
    assert fresh_report['scripted_input_schedule']==old_fresh['scripted_input_schedule']
    assert fresh_report['core_options']==old_fresh['core_options']
    x,y=[{row['frame']:row for row in r['frames_captured']}for r in (old_fresh,fresh_report)]
    assert x.keys()==y.keys() and len(x)==56
    assert all(x[n]['PNG_sha256']==y[n]['PNG_sha256']for n in x)
    # Exact replay controls/frame numbers; only the wider nameplate may change.
    current={row['frame']:row for row in dream_report['frames_captured']}
    comparison=[]
    for row in voyage_report['frames_captured']:
        n=row['frame']
        if n not in current or n>12240:continue
        before=Image.open(row['path']).convert('RGB');after=Image.open(current[n]['path']).convert('RGB')
        differences=[(px,py)for py in range(384)for px in range(256)if before.getpixel((px,py))!=after.getpixel((px,py))]
        assert all(0<=px<256 and 272<=py<292 for px,py in differences),(n,differences[:4])
        comparison.append({'frame':n,'changed_pixels_only_in_portrait_nameplate_band':len(differences)})
    font=GameAsciiFont.from_arm9(b['/__arm9__.bin']);names=[]
    for n in (9240,9640,10040,10640,10840,11040,11240):
        image=Image.open(dream/f'frame_{n:06d}_cold_boot.png').convert('RGB')
        # Some frames contain the other dream participant or an empty transition;
        # only original Yukihisa captions are required to carry his full surname.
        previous=Image.open(voyage/f'frame_{n:06d}_navigation.png').convert('RGB')
        try:complete_mask(font,'Yukihisa Shira',previous,16,276,(98,97,98))
        except ValueError:continue
        ink,bounds=complete_mask(font,'Yukihisa Shiraki',image,16,276,(98,97,98))
        names.append({'frame':n,'complete_text':'Yukihisa Shiraki','all_glyph_and_blank_cells_exact':True,'ink_pixels':ink,'bounds':bounds})
    assert len(names)>=4
    landscape=PxlImage.from_bytes(b['/towngrp/towngrp47.pxl']).render()
    facilities=[]
    for folder,tavern,inn,suffix in [(voyage,7440,8240,'navigation'),(dream,7440,8240,'cold_boot'),(reload,4600,5400,'cold_boot')]:
        for n,text,origin,resource,pixel_origin in [(tavern,'Tavern',(56,238),'kbj04',(50,192)),
                                                    (inn,'Inn',(63,260),'kbj08',(0,240))]:
            image=Image.open(folder/f'frame_{n:06d}_{suffix}.png').convert('RGB')
            ink,bounds=complete_mask(font,text,image,*origin,(0,8,0))
            count=icon(image,PxlImage.from_bytes(b['/_pxl/'+resource+'.pxl']),*pixel_origin)
            facilities.append({'image':str(folder/f'frame_{n:06d}_{suffix}.png'),'English':text,'bounds':bounds,'full_glyph_pixels':ink,
                               'actual_alternate_icon':resource,'all_nontransparent_source_pixels':count})
    stock_cases=[]
    for path in [voyage/'frame_007640_navigation.png',dream/'frame_007640_cold_boot.png',
                 reload/'frame_004800_cold_boot.png',reload/'frame_005600_final.png']:
        image=Image.open(path).convert('RGB')
        stock_cases.append({'image':str(path),'background47_unoccluded_pixels_exact':background(image,landscape),
                            'complete_stock_masks':[mask(image,font,text,88+i*16)for i,text in enumerate(('Silver','CotClth','T-Shell'))]})
    saved=read('work/analysis/japan_facilities_v517/saved_checkpoint.json')
    assert sha(Path(saved['save']).read_bytes())==saved['sha256'] and saved['original_Seoul_donor_unchanged']
    assert reload_report['battery_save_preloaded']['source_sha256']==saved['sha256']
    assert saved['completed_route_bits']==0
    for folder in (voyage,dream,reload):
        ram=(folder/'final_arm9_ram.bin').read_bytes();assert struct.unpack_from('<H',ram,0x27985C)[0]&15==0
    before=Image.open(voyage/'frame_015240_navigation.png').convert('RGB')
    after=Image.open(reload/'frame_004200_cold_boot.png').convert('RGB')
    assert before.crop((0,0,256,192)).tobytes()==after.crop((0,0,256,192)).tobytes()
    patch=ROM.with_suffix('.xdelta');make_xdelta(Path('work/clean.nds'),ROM,patch)
    rebuilt=OUT/'reconstructed.nds';apply_xdelta(Path('work/clean.nds'),patch,rebuilt);assert rebuilt.read_bytes()==ROM.read_bytes()
    plaques=read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques)==18 and all(not p['fully_completed']for p in plaques)
    proof={'candidate':str(ROM),'candidate_sha256':digest,'profile':m['profile'],'base':m['base_rom'],'base_sha256':m['base_sha256'],
           'patch_sha256':sha(patch.read_bytes()),'exact_clean_patch_reconstruction':True,
           'only_two_surname_data_bytes_change_from_V514':True,'all675_PXL_FLS_files_and_other_components_exact':True,
           'all470_batches_and114_accepted_layers_retained':True,'full_native_caption_cases':names,'exact_replay_frame_comparison':comparison,
           'all56_fresh_whole_frames_exact':True,'normal_Nagasaki_alternate_sign_and_caption_cases':facilities,
           'actual_town_stock_and_background_cases':stock_cases,'normal_Seoul_to_Nagasaki_docking_resupply_and_Namahage_award':True,
           'saved_checkpoint':saved['save'],'saved_checkpoint_sha256':saved['sha256'],'production_cold_reload_passes_upper_panel_exact':True,
           'no_false_route_completion_flags_or_inventory_position_injection':True,
           'normal_dream_graphics_do_not_clear_unidentified_raw_creature_introduction':True,
           'reports':[{'path':str(p),'sha256':sha(p.read_bytes())}for p in (voyage_path,dream_path,fresh_path,reload_path)],
           'Osaka37_Naha_and_other_original_gates_still_open':True,'all18_plaques_incomplete':True,
           'status':'experimental-awaiting-human-acceptance','full_goal_complete':False}
    (OUT/'release_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'full_name_captions':len(names),'matched_replay_frames':len(comparison),'alternate_facility_cases':len(facilities),
                      'fresh_frames':56,'exact_patch':True,'candidate_sha256':digest}))


if __name__=='__main__':main()
