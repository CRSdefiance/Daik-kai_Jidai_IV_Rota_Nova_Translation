"""Actual complete Square glyphs, preserved borders, cold boot and exact patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_caption_cells import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROOT=Path('work/analysis/square_caption_cells_v484')
ROM=Path('out/all_routes_combined_v484_candidate.nds')
PARENT=Path('out/all_routes_combined_v474_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def report(folder,digest):
    path=Path('work/emulation_v193')/folder/'capture_report.json'
    r=read(path)
    assert r['ROM_sha256']==digest and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not r.get('synthetic_inventory_fixtures')
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    if r.get('battery_save_preloaded'):
        donor=r['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']
    return path,r


def main():
    digest=sha(ROM.read_bytes())
    manifest,old_manifest=read(ROM.with_suffix('.manifest.json')),read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256']==digest and manifest['profile']=='all-routes-unified-v484'
    assert manifest['base_sha256']==old_manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches']==old_manifest['batches'] and len(manifest['batches'])==470
    assert manifest['required_batches']==old_manifest['required_batches'] and all(manifest['checks'].values())
    registry=read(Path('translations/release_stack.json'))
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114
    assert all(registry['profiles']['all-routes-unified-v484'][k]==v for k,v in registry['profiles']['all-routes-unified-v474'].items()if k not in('note','description'))
    before,after=files(NdsImage.open(PARENT)),files(NdsImage.open(ROM))
    assert before.keys()==after.keys() and [p for p in before if before[p]!=after[p]]==['/__arm9__.bin']
    arm,change=apply_release(before['/__arm9__.bin'],'translations/square_caption_cells_v2.json')
    assert arm==after['/__arm9__.bin'] and change['all_section_extents_startup_heap_and_cache_wrapper_exact']
    native=read(ROOT/'native_proof.json')
    assert native['target_arm9_sha256']==sha(arm)
    font=GameAsciiFont.from_arm9(arm)
    _,old=report('istanbul_square_v482',sha(PARENT.read_bytes()))
    new_path,new=report('square_cells_v484',digest)
    assert old['scripted_input_schedule']==new['scripted_input_schedule'] and new['frames']==old['frames']==5900
    assert old['battery_save_preloaded']['source_sha256']==new['battery_save_preloaded']['source_sha256']
    a={r['frame']:r for r in old['frames_captured']};b={r['frame']:r for r in new['frames_captured']}
    assert a.keys()<=b.keys()
    for frame in a:
        before_image=Image.open(a[frame]['path']).convert('RGB');after_image=Image.open(b[frame]['path']).convert('RGB')
        differences=[(i%256,i//256)for i,(x,y)in enumerate(zip(before_image.get_flattened_data(),after_image.get_flattened_data()))if x!=y]
        assert all(120<=x<184 and 214<=y<226 for x,y in differences),frame
        if frame<=3500:
            assert not differences,frame
    cases=[]
    labels=[('Delicacy Shop',214),('Liquor Shop',246),('Gems Shop',278),('Fiber Shop',310)]
    for frame,selected in ((4500,0),(4600,1),(4700,2),(4800,3)):
        im=Image.open(b[frame]['path']).convert('RGB')
        rows=[]
        for i,(text,y)in enumerate(labels):
            expected={(120+n*5+x,y+gy)for n,c in enumerate(text)for gy in range(11)for x in range(6)if font.decode(c).getpixel((x,gy))}
            actual={(x,yy)for yy in range(y,y+12)for x in range(120,184)if im.getpixel((x,yy))==(230,230,230)}
            assert actual==expected,(frame,text)
            top=208+i*32
            if i==selected:
                for yy in range(top-2,top+26):
                    for x in range(170,186):
                        assert im.getpixel((x,yy))==((230,230,230)if(x,yy)in expected else(0,165,172))
                assert im.getpixel((186,top+4))==(123,121,98)
            else:
                assert im.getpixel((180,top+4))==(57,56,57)
            rows.append({'text':text,'ink_pixels':len(expected),'first_and_final_letters_and_blank_cells_exact':True})
        cases.append({'frame':frame,'selected':selected,'capture':b[frame],'complete_captions':rows,'border_and_focus_padding_exact':True})
    for frame in(5200,5600,5900):
        im=Image.open(b[frame]['path']).convert('RGB')
        for text,y in(('Business? Fair. I wish a good',296),('opportunity would arise.',312)):
            complete_mask(font,text,im,22,y,(0,8,0))
    _,old_fresh=report('repair_regression_newgame_v474',sha(PARENT.read_bytes()))
    fresh_path,fresh=report('square_cells_fresh_v484',digest)
    assert old_fresh['scripted_input_schedule']==fresh['scripted_input_schedule'] and old_fresh['frames']==fresh['frames']==21200
    x={r['frame']:r for r in old_fresh['frames_captured']};y={r['frame']:r for r in fresh['frames_captured']}
    # V474 reference was captured every100 frames; this regression captures
    # every400 frames. Compare all56 new frames, not an invented equal density.
    assert len(y)==56 and y.keys()<=x.keys() and all(x[f]['PNG_sha256']==y[f]['PNG_sha256']for f in y)
    clean=Path('work/clean.nds');patch=ROM.with_suffix('.xdelta');rebuilt=ROOT/'reconstructed.nds'
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,rebuilt)
    assert rebuilt.read_bytes()==ROM.read_bytes()
    proof={'candidate':str(ROM),'candidate_sha256':digest,'patch_sha256':sha(patch.read_bytes()),
           'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),'base':manifest['base_rom'],'base_sha256':manifest['base_sha256'],
           'profile':'all-routes-unified-v484','change':change,'all470_inherited_batches_and_stages_preserved':True,
           'all114_accepted_layers_retained':True,'all_non_ARM9_files_and_components_exact_to_V474':True,
           'native_proof':str(ROOT/'native_proof.json'),'native_proof_sha256':sha((ROOT/'native_proof.json').read_bytes()),
           'actual_complete_four_shop_selection_states':cases,'all_matched_Square_frame_changes_confined_to_Delicacy_caption':sorted(a),
           'three_complete_dialogues_unchanged_and_aligned':True,'fresh_NewGame_title_story_town_help_whole_frames_exact':sorted(y),
           'reports':[str(new_path),str(fresh_path)],'exact_clean_patch_reconstruction':True,
           'release_status':'experimental-actual-cold-boot-verified-awaiting-user-acceptance',
           'V483_revoked_actual_black_screen':True,'all22_historical_requirements_retained':True,'all18_plaques_incomplete':True,
           'hardware_verification':False,'full_goal_complete':False}
    (ROOT/'release_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'candidate_sha256':digest,'fresh_unchanged_frames':len(y),'patch_exact':True}))


if __name__=='__main__':
    main()
