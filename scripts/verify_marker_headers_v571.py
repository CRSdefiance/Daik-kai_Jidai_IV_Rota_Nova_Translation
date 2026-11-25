"""Verify complete marker header bounds, source material, native crops and release."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.frame_buttons_v165 import atlas_indices
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_marker_ownership_v569 import prepare
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT=Path('work/analysis/marker_headers_v570')
ROM=Path('out/all_routes_combined_v571_candidate.nds')
PARENT=Path('out/all_routes_combined_v569_candidate.nds')
CAPTURE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FILE,ARCHIVE='/_pxl/__marker.pxl','/GRP/CMMNIMG.DK4'
ROWS=((184,0,64,'Temp Storage'),(168,64,48,'Issued'),(168,80,48,'Spoils'))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    old,new,clean=(NdsImage.open(p) for p in (PARENT,ROM,Path('work/clean.nds')))
    before,after=rom_files(old),rom_files(new)
    assert before.keys()==after.keys() and sorted(p for p in before if before[p]!=after[p])==[ARCHIVE,FILE]
    inherited,image,original=(PxlImage.from_bytes(r.read_file(FILE)) for r in (old,new,clean))
    assert image.source[:image.pixels_offset]==original.source[:original.pixels_offset]
    assert image.source==(ROOT/'marker_headers_RESEARCH_ONLY.pxl').read_bytes()
    owned={y*256+x for l,t,w,text in ROWS for y in range(t,t+16) for x in range(l,l+w)}
    assert all(a==b for n,(a,b) in enumerate(zip(inherited.indices,image.indices,strict=True)) if n not in owned)
    assert sum(a!=b for a,b in zip(inherited.indices,image.indices,strict=True))==993
    font=GameAsciiFont.from_arm9(new.read_file('/__arm9__.bin'))
    font_cases=[]
    for left,top,width,text in ROWS:
        cursor=left+(width-sum(3 if ch==' ' else 5 for ch in text))//2
        expected=set()
        for ch in text:
            glyph=font.decode(ch)
            assert not any(glyph.getpixel((x,y)) for y in range(2) for x in range(6))
            assert not any(glyph.getpixel((5,y)) for y in range(11))
            expected|={(cursor+x,top+3+y-2) for y in range(2,11) for x in range(5) if glyph.getpixel((x,y))}
            cursor+=3 if ch==' ' else 5
        assert expected=={(x,y) for y in range(top,top+16) for x in range(left,left+width) if image.indices[y*256+x]==15}
        font_cases.append({'English':text,'source_box':[left,top,left+width,top+16],'complete_font_ink':len(expected)})
    assert sum(c['complete_font_ink'] for c in font_cases)==282
    embedded,old_embedded=(atlas_indices(r.read_file(ARCHIVE)) for r in (new,old))
    assert all(embedded[y*512:y*512+256]==image.indices[y*256:(y+1)*256] for y in range(256))
    assert all(embedded[y*512+256:(y+1)*512]==old_embedded[y*512+256:(y+1)*512] for y in range(256))
    aa,bb=(IlnkContainer.parse(r.read_file(ARCHIVE)) for r in (old,new))
    assert aa.blocks[5][:20]==bb.blocks[5][:20]
    assert all(a==b for n,(a,b) in enumerate(zip(aa.blocks,bb.blocks,strict=True)) if n!=5)
    manifest,prior=read(ROM.with_suffix('.manifest.json')),read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256']==sha(ROM.read_bytes()) and manifest['profile']=='all-routes-unified-v571'
    assert manifest['base_sha256']==prior['base_sha256']
    assert manifest['batches']==prior['batches'] and len(manifest['batches'])==470
    assert manifest['required_batches']==prior['required_batches']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(read('translations/release_stack.json')['accepted_layers'])==114
    stage=manifest['relocations'][FILE]['marker_header_materials']
    assert sum(c['legacy_outside_box_Japanese_points_removed'] for c in stage['cases'])==27
    assert sum(c['original_visible_material_points_exact'] for c in stage['cases'])==1528
    fixtures=read(ROOT/'native_crop_fixtures.json');reports=[]
    for fixture in fixtures:
        parent,altered=(NdsImage.open(fixture[k]) for k in ('parent','ROM'))
        a,b=rom_files(parent),rom_files(altered)
        assert [p for p in a if a[p]!=b[p]]==['/__arm9__.bin']
        offsets={n for c in fixture['changes'] for n in range(c['file_offset'],c['file_offset']+4)}
        assert all(x==y for n,(x,y) in enumerate(zip(a['/__arm9__.bin'],b['/__arm9__.bin'],strict=True)) if n not in offsets)
        assert sha(Path(fixture['ROM']).read_bytes())==fixture['ROM_sha256']
        reports.append(capture_report(CAPTURE/f"marker_headers_v571_{fixture['kind']}",fixture['ROM_sha256']))
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    assert reports[0]['core_options']==reports[1]['core_options']
    tables=[{s['frame']:s for s in r['frames_captured']} for r in reports]
    cases=[]
    for fixture,report,table,atlas in zip(fixtures,reports,tables,(inherited,image),strict=True):
        kind=fixture['kind'];source_save=Path(report['battery_save_preloaded']['source'])
        assert sha(source_save.read_bytes())==report['battery_save_preloaded']['source_sha256']
        for frame in (4300,4600):
            raw=(CAPTURE/f'marker_headers_v571_{kind}'/f'frame_{frame:06d}_arm9_ram.bin').read_bytes();found=[]
            for pos in range(0,len(raw)-48,4):
                words=struct.unpack_from('<12I',raw,pos)
                if words[3]==0x02313F74 and words[7:9]==(168,0) and words[10:12]==(80,96):
                    assert words[6]==0 and words[9]&255==0
                    found.append(pos+0x02000000)
            assert len(found)==1
            u=machine(NdsImage.open(fixture['ROM']).read_file('/__arm9__.bin'));u.mem_write(0x02000000,raw)
            call(u,0xD4170,(found[0],));pointer=u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer,len(atlas.source)))==atlas.source
            shot=Image.open(table[frame]['path']).convert('RGB')
            assert all(native5(shot.getpixel((x,y+261)))==native5(atlas.palette[atlas.indices[y*256+x+168]])
                       for y in range(96) for x in range(80))
            cases.append({'kind':kind,'frame':frame,'view':found[0],'owner':0x02313F74,'resident_pointer':pointer,
                          'complete_80x96_original_resource_crop_exact':True,'palette0_flags0_verified':True,
                          'manual_crop_not_original_context':True})
    for frame in (4300,4600):
        control,actual=(Image.open(t[frame]['path']).convert('RGB') for t in tables)
        for y in range(384):
            for x in range(256):
                expected=native5(control.getpixel((x,y)))
                if x<80 and 261<=y<357:expected=native5(image.palette[image.indices[(y-261)*256+x+168]])
                assert native5(actual.getpixel((x,y)))==expected,(frame,x,y)
    fresh=capture_report(CAPTURE/'marker_headers_v571_fresh',sha(ROM.read_bytes()))
    prior_fresh=capture_report(CAPTURE/'marker_ownership_v569_fresh',sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule']==prior_fresh['scripted_input_schedule']
    assert fresh['core_options']==prior_fresh['core_options']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']]==[s['PNG_sha256'] for s in prior_fresh['frames_captured']]
    assert len({s['frame'] for s in fresh['frames_captured']})==56
    patch=ROM.with_suffix('.xdelta');make_xdelta(Path('work/clean.nds'),ROM,patch)
    reconstructed=ROOT/'v571_reconstructed.nds';apply_xdelta(Path('work/clean.nds'),patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes()
    for name in ('graphics_completion_campaign_v1.json','graphics_visual_audit_v150.json'):
        entries=read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(entries)==18 and all(e['fully_completed'] is False for e in entries)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained'])==22
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],
           'base':manifest['base_rom'],'base_sha256':manifest['base_sha256'],'patch_sha256':sha(patch.read_bytes()),
           'exact_clean_patch_reconstruction':True,'only_changed_files_from_V569':[ARCHIVE,FILE],
           'all_code_other_art_and_translations_exact_V569':True,'all470_batches114_layers_retained':True,
           'source_material_and_bounds_cases':stage['cases'],'font_cases':font_cases,'changed_marker_pixels':993,
           'all65536_embedded_marker_indices_match_loose':True,'embedded_frame_headers_other_blocks_exact':True,
           'native_cases':cases,'native_crop_pixels_exact':30720,'full_pair_screen_pixels_exact':196608,
           'unchanged_unique_startup_frames':56,'original_header_contexts_still_unverified':True,
           'all18_plaques_remain_incomplete':True,'experimental':True,'canonical_promoted':False,'full_goal_complete':False}
    (ROOT/'v571_release_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('V571:3 complete282-ink headers,27 missed Japanese edges removed,1528 source material points,4 full native crops,56 unchanged startup frames and exact patch pass.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-fixtures',action='store_true')
    if parser.parse_args().prepare_fixtures:
        prepare(root=ROOT,parent_rom=PARENT,candidate_rom=ROM,rectangle=(168,0,248,96),filename_prefix='marker_headers')
    else:main()
