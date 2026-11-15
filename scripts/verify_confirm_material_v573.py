"""Verify original Confirm shading, full native letters and controlled rendering."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_marker_ownership_v569 import prepare
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT=Path('work/analysis/confirm_material_v572')
ROM=Path('out/all_routes_combined_v573_candidate.nds')
PARENT=Path('out/all_routes_combined_v571_candidate.nds')
CAPTURE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FILE='/_pxl/kakutei.pxl'
OWNER=0x023139C0


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    old,new,clean=(NdsImage.open(p) for p in (PARENT,ROM,Path('work/clean.nds')))
    before,after=rom_files(old),rom_files(new)
    assert before.keys()==after.keys() and sorted(p for p in before if before[p]!=after[p])==[FILE]
    inherited,image,original=(PxlImage.from_bytes(r.read_file(FILE)) for r in (old,new,clean))
    assert (image.width,image.height)==(48,20)
    assert image.source[:image.pixels_offset]==original.source[:original.pixels_offset]
    packed_palette=struct.unpack_from('<16H',image.source,20)
    assert [n for n,v in enumerate(packed_palette) if not v&0x8000]==[14]
    transparent={(x,y) for y in range(20) for x in range(48) if image.indices[y*48+x]==14}
    assert len(transparent)==79
    assert transparent=={(x,y) for y in range(20) for x in range(48) if original.indices[y*48+x]==14}
    assert image.source==(ROOT/'confirm_RESEARCH_ONLY.pxl').read_bytes()
    proof=read(ROOT/'prototype_proof.json')
    hidden={tuple(c['point']) for c in proof['reconstruction_controls']}
    white={(x,y) for y in range(20) for x in range(48) if original.indices[y*48+x]==13}
    assert len(white)==109 and len(hidden)==190 and white<=hidden
    assert all(c['source_controls'] and len(c['source_controls'])==2 for c in proof['reconstruction_controls'])
    for c in proof['reconstruction_controls']:
        x,y=c['point']
        for a,b in c['source_controls']:
            assert (a,b) not in hidden and x+y==a+b and original.indices[b*48+a]<=6
        assert c['index'] in range(1,7)
    font=GameAsciiFont.from_arm9(new.read_file('/__arm9__.bin'));ink=set()
    for n,ch in enumerate('Confirm'):
        glyph=font.decode(ch)
        assert not any(glyph.getpixel((x,y)) for y in range(2) for x in range(6))
        assert not any(glyph.getpixel((5,y)) for y in range(11))
        ink|={(6+n*5+x,3+y) for y in range(2,11) for x in range(5) if glyph.getpixel((x,y))}
    shadow={(x+1,y+1) for x,y in ink}-ink
    assert len(ink)==86 and len(shadow)==76
    assert {(x,y) for y in range(20) for x in range(48) if image.indices[y*48+x]==13}==ink
    assert all(image.indices[y*48+x]==0 for x,y in shadow)
    preserved={(x,y) for y in range(20) for x in range(48) if (x,y) not in hidden|ink|shadow}
    assert len(preserved)==674
    assert all(image.indices[y*48+x]==original.indices[y*48+x] for x,y in preserved)
    assert all(image.indices[y*48+x]==original.indices[y*48+x] for y in range(20) for x in range(48)
               if x<4 or x>=43 or y<3 or y>=17 or original.indices[y*48+x] in range(7,13))
    assert sum(a!=b for a,b in zip(inherited.indices,image.indices,strict=True))==217
    manifest,prior=read(ROM.with_suffix('.manifest.json')),read(PARENT.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v573' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['base_sha256']==prior['base_sha256']
    assert manifest['batches']==prior['batches'] and len(manifest['batches'])==470
    assert manifest['required_batches']==prior['required_batches']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(read('translations/release_stack.json')['accepted_layers'])==114
    stage=manifest['relocations'][FILE]['confirm_button_material']
    assert stage['complete_native_font_ink']==86 and stage['all_visible_original_material_points_exact']==674
    fixtures=read(ROOT/'native_crop_fixtures.json');reports=[]
    for fixture in fixtures:
        parent,altered=(NdsImage.open(fixture[k]) for k in ('parent','ROM'))
        a,b=rom_files(parent),rom_files(altered)
        assert [p for p in a if a[p]!=b[p]]==['/__arm9__.bin']
        offsets={n for c in fixture['changes'] for n in range(c['file_offset'],c['file_offset']+4)}
        assert len(fixture['changes'])==10
        assert all(x==y for n,(x,y) in enumerate(zip(a['/__arm9__.bin'],b['/__arm9__.bin'],strict=True)) if n not in offsets)
        assert sha(Path(fixture['ROM']).read_bytes())==fixture['ROM_sha256']
        reports.append(capture_report(CAPTURE/f"confirm_material_v573_{fixture['kind']}",fixture['ROM_sha256']))
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    assert reports[0]['core_options']==reports[1]['core_options']
    tables=[{s['frame']:s for s in r['frames_captured']} for r in reports];cases=[]
    for fixture,report,table,atlas in zip(fixtures,reports,tables,(inherited,image),strict=True):
        kind=fixture['kind'];source_save=Path(report['battery_save_preloaded']['source'])
        assert sha(source_save.read_bytes())==report['battery_save_preloaded']['source_sha256']
        for frame in (4300,4600):
            raw=(CAPTURE/f'confirm_material_v573_{kind}'/f'frame_{frame:06d}_arm9_ram.bin').read_bytes();found=[]
            for pos in range(0,len(raw)-48,4):
                w=struct.unpack_from('<12I',raw,pos)
                if w[3]==OWNER and w[7:9]==(0,0) and w[10:12]==(48,20):
                    assert w[6]==0 and w[9]&255==0
                    found.append(pos+0x02000000)
            assert len(found)==1
            u=machine(NdsImage.open(fixture['ROM']).read_file('/__arm9__.bin'));u.mem_write(0x02000000,raw)
            call(u,0xD4170,(found[0],));pointer=u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer,len(atlas.source)))==atlas.source
            shot=Image.open(table[frame]['path']).convert('RGB')
            assert all(native5(shot.getpixel((x,y+261)))==native5(atlas.palette[atlas.indices[y*48+x]])
                       for y in range(20) for x in range(48) if (x,y) not in transparent)
            cases.append({'kind':kind,'frame':frame,'view':found[0],'owner':OWNER,'resident_pointer':pointer,
                          'all881_opaque_original_resource_pixels_exact':True,'original79_transparent_points_retained':True,
                          'palette0_flags0_verified':True,
                          'manual_crop_not_original_button_context':True})
    for frame in (4300,4600):
        control,actual=(Image.open(t[frame]['path']).convert('RGB') for t in tables)
        for y in range(384):
            for x in range(256):
                expected=native5(control.getpixel((x,y)))
                if x<48 and 261<=y<281 and (x,y-261) not in transparent:
                    expected=native5(image.palette[image.indices[(y-261)*48+x]])
                assert native5(actual.getpixel((x,y)))==expected,(frame,x,y)
    fresh=capture_report(CAPTURE/'confirm_material_v573_fresh',sha(ROM.read_bytes()))
    prior_fresh=capture_report(CAPTURE/'marker_headers_v571_fresh',sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule']==prior_fresh['scripted_input_schedule']
    assert fresh['core_options']==prior_fresh['core_options']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']]==[s['PNG_sha256'] for s in prior_fresh['frames_captured']]
    assert len({s['frame'] for s in fresh['frames_captured']})==56
    patch=ROM.with_suffix('.xdelta');make_xdelta(Path('work/clean.nds'),ROM,patch)
    reconstructed=ROOT/'v573_reconstructed.nds';apply_xdelta(Path('work/clean.nds'),patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes()
    for name in ('graphics_completion_campaign_v1.json','graphics_visual_audit_v150.json'):
        entries=read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(entries)==18 and all(e['fully_completed'] is False for e in entries)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained'])==22
    result={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],
            'base':manifest['base_rom'],'base_sha256':manifest['base_sha256'],'patch_sha256':sha(patch.read_bytes()),
            'exact_clean_patch_reconstruction':True,'only_changed_files_from_V571':[FILE],
            'all_code_other_art_and_translations_exact_V571':True,'all470_batches114_layers_retained':True,
            'source_material_proof':stage,'complete_font_ink':86,'new_English_shadow_points':76,
            'original_visible_material_points_exact':674,'source_frame_and_all_metadata_exact':True,
            'changed_pixels':217,'native_cases':cases,'native_opaque_pixels_exact':3524,
            'original_transparent_points_per_crop':79,'transparent_framebuffer_points_match_control':158,
            'full_pair_screen_pixels_exact':196608,'unchanged_unique_startup_frames':56,
            'concealed_gradient_is_inferred_not_exact_recovery':True,'original_button_context_still_unverified':True,
            'all18_plaques_remain_incomplete':True,'experimental':True,'canonical_promoted':False,'full_goal_complete':False}
    (ROOT/'v573_release_proof.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('V573: Confirm full86 ink,190 old face/shadow points reconstructed,674 source material points exact,4 native crops,56 unchanged startup frames and exact patch pass.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-fixtures',action='store_true')
    if parser.parse_args().prepare_fixtures:
        prepare(root=ROOT,parent_rom=PARENT,candidate_rom=ROM,rectangle=(0,0,48,20),
                filename_prefix='confirm',resource_owner=OWNER)
    else:main()
