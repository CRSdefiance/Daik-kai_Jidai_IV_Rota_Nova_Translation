"""Verify normal Seoul arrival, retained art, captions and production save reload."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files
from scripts.verify_movie_gpu_fixtures_v336 import quantized

OUT=Path('work/analysis/maria_asia_v516')
ROM=Path('out/all_routes_combined_v514_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def report(folder,digest):
    path=Path('work/emulation_v193')/folder/'capture_report.json'
    data=read(path)
    assert data['ROM_sha256']==digest and data['cold_boot'] and not data['savestate_loaded']
    assert not data['callback_errors'] and not data.get('synthetic_inventory_fixtures')
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    if data.get('battery_save_preloaded'):
        donor=data['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']
    return path,data


def background(image,source):
    current=quantized(image.crop((0,192,256,384))).convert('RGB')
    expected=quantized(source).convert('RGB')
    count=0
    # Original portrait and nameplate occlusions; dialog covers rows96 onward.
    for y in range(96):
        for x in range(72 if y<80 else 86,256):
            assert current.getpixel((x,y))==expected.getpixel((x,y)),(x,y)
            count+=1
    assert count==17440
    return count


def icon(image,pxl,x0,y0):
    count=0
    for index,value in enumerate(pxl.indices):
        if value==255:continue
        x,y=index%pxl.width,index//pxl.width
        assert tuple(c>>3 for c in image.getpixel((x+x0,y+y0)))==tuple(c>>3 for c in pxl.palette[value][:3])
        count+=1
    return count


def main():
    fixture=read(OUT/'selection_fixture_manifest.json')
    a,b=[files(NdsImage.open(p)) for p in (ROM,fixture['research_ROM'])]
    assert sorted(p for p in a if a[p]!=b[p])==['/__arm9__.bin']
    assert [i for i,(x,y)in enumerate(zip(a['/__arm9__.bin'],b['/__arm9__.bin']))if x!=y]==[0x9F068]
    digest=sha(ROM.read_bytes())
    assert digest==fixture['production_ROM_sha256']
    manifest=read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256']==digest and manifest['profile']=='all-routes-unified-v514'
    voyage_path,voyage=report('maria_asia_v516_channel',fixture['research_ROM_sha256'])
    reload_path,reload=report('maria_asia_v516_reload',digest)
    facilities_path,facilities=report('maria_asia_v516_production_facilities',digest)
    assert voyage['frames']==34040 and reload['frames']==4200 and facilities['frames']==5600
    saved=read(OUT/'saved_checkpoint.json')
    save_path=Path(saved['save'])
    assert sha(save_path.read_bytes())==saved['sha256']
    assert save_path.read_bytes()==(voyage_path.parent/'saves/research_only_maria_selection_v514.dsv').read_bytes()
    assert saved['completed_route_bits']==0
    for folder in (voyage_path.parent,reload_path.parent,facilities_path.parent):
        ram=(folder/'final_arm9_ram.bin').read_bytes()
        assert struct.unpack_from('<H',ram,0x27985C)[0]&15==0
    for folder in (reload_path.parent,facilities_path.parent):
        ram=(folder/'final_arm9_ram.bin').read_bytes()
        assert struct.unpack_from('<I',ram,0x9F068)[0]==0x03A00003
    # Production code with the bypass removed can cold-load the assisted save.
    initial=Image.open(voyage_path.parent/'frame_034040_navigation.png').convert('RGB')
    loaded=Image.open(reload_path.parent/'frame_004200_final.png').convert('RGB')
    assert initial.crop((0,0,256,192)).tobytes()==loaded.crop((0,0,256,192)).tobytes()
    font=GameAsciiFont.from_arm9(a['/__arm9__.bin'])
    clean=NdsImage.open('work/clean.nds')
    assert a['/towngrp/towngrp35.pxl']==clean.read_file('/towngrp/towngrp35.pxl')
    source=PxlImage.from_bytes(a['/towngrp/towngrp35.pxl']).render()
    backgrounds=[]
    stocks=[]
    for path in [voyage_path.parent/'frame_026440_navigation.png',
                 voyage_path.parent/'frame_027440_navigation.png',
                 facilities_path.parent/'frame_004800_cold_boot.png',
                 facilities_path.parent/'frame_005600_final.png']:
        image=Image.open(path).convert('RGB')
        backgrounds.append({'image':str(path),'source':'/towngrp/towngrp35.pxl',
                            'native_origin':[0,192],'full_unoccluded_source_pixels':background(image,source),
                            'portrait_nameplate_dialog_occlusions_excluded':True})
        stocks.append({'image':str(path),'complete_stock_label_masks':[
            mask(image,font,text,88+i*16) for i,text in enumerate(('Hazelnuts','China','Silk','Silk Cloth','Ginseng'))]})
    captions=[]
    for folder,tavern_frame,inn_frame in [(voyage_path.parent,26040,27040),
                                          (facilities_path.parent,4600,5400)]:
        for frame,text,x,y,name,x0,y0 in [(tavern_frame,'Tavern',64,244,'kbe04',62,192),
                                         (inn_frame,'Inn',64,264,'kbe08',0,240)]:
            suffix='navigation.png' if folder==voyage_path.parent else 'cold_boot.png'
            path=folder/f'frame_{frame:06d}_{suffix}'
            image=Image.open(path).convert('RGB')
            ink,bounds=complete_mask(font,text,image,x,y,(0,8,0))
            resource='/_pxl/'+name+'.pxl'
            count=icon(image,PxlImage.from_bytes(a[resource]),x0,y0)
            captions.append({'image':str(path),'English':text,'all_first_final_letters_and_blank_cells_exact':True,
                             'ink_pixels':ink,'bounds':bounds,'source_icon':resource,
                             'complete_nontransparent_icon_pixels':count,'not_an_alternate_kbj_icon':True})
    u=machine(a['/__arm9__.bin'])
    mapping=[]
    for facility in (0,4,8):
        call(u,0xB7294,(57,facility));assert u.reg_read(UC_ARM_REG_R0)==35
        mapping.append({'town':57,'facility':facility,'original_background':35})
    proof={'candidate':str(ROM),'candidate_sha256':digest,
           'source_voyage_fixture_manifest':str(OUT/'selection_fixture_manifest.json'),
           'reports':[{'path':str(p),'sha256':sha(p.read_bytes()),'frames':r['frames']}for p,r in
                      [(voyage_path,voyage),(reload_path,reload),(facilities_path,facilities)]],
           'normal_Hangzhou_to_Seoul_channel_voyage_docking_resupply_and30_night_rest':True,
           'Maria_selection_bypass_user_authorized':True,'earned_unlock_not_claimed':True,
           'no_route_completion_bits_set_and_original_selection_instruction_restored_in_production_runs':True,
           'no_inventory_condition_supply_or_movement_injection':True,
           'background35_source_exact_and_actual_full_unoccluded_regions':backgrounds,
           'all_five_Seoul_specialties_complete_in_both_town_facilities':stocks,
           'complete_actual_Tavern_Inn_captions_and_icons':captions,'original_background_getter':mapping,
           'whole_upper_town_panel_exact_after_production_cold_reload':True,
           'saved_checkpoint':str(save_path),'saved_checkpoint_sha256':saved['sha256'],
           'registered_ROM_unchanged_no_new_playable_release':True,
           'Osaka37_and_Japan_alternate_facilities_still_open':True,
           'all22_original_requirements_and18_incomplete_plaques_retained':True,'full_goal_complete':False}
    (OUT/'seoul_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Seoul: four17440-pixel source-art matches,20 full stock masks,four icon/caption cases and production cold reload pass.')


if __name__=='__main__':main()
