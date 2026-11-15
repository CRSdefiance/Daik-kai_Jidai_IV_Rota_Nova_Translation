"""Verify corrected source ownership, both marker copies and controlled native crops."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.frame_buttons_v165 import atlas_indices
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT = Path('work/analysis/marker_materials_v568')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v569_candidate.nds')
PARENT = Path('out/all_routes_combined_v566_candidate.nds')
FILE, ARCHIVE = '/_pxl/__marker.pxl', '/GRP/CMMNIMG.DK4'
PATCHES = {0x020852BC: 0xE3A00028, 0x020852C0: 0xE3A01040,
           0x020852C4: 0xE3A02000, 0x020852C8: 0xE3A03000,
           0x020852CC: 0xE88D000F, 0x020852D0: 0xE28D004C,
           0x020852D8: 0xE3A02070, 0x020852DC: 0xE3A03030,
           0x020852E0: 0xE1A00000, 0x020854DC: 0x02313F74}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepare(*, root=ROOT, parent_rom=PARENT, candidate_rom=ROM,
            rectangle=(112,48,152,112), filename_prefix='marker', resource_owner=0x02313F74):
    root.mkdir(parents=True,exist_ok=True)
    left,top,right,bottom=rectangle
    assert 0<=left<right<=256 and right-left<=255 and 0<=top<bottom<=256 and bottom-top<=104
    patches=dict(PATCHES)
    patches.update({0x020852BC:0xE3A00000|(right-left),0x020852C0:0xE3A01000|(bottom-top),
                    0x020852D8:0xE3A02000|left,0x020852DC:0xE3A03000|top,
                    0x020854DC:resource_owner})
    previous = root/'native_crop_fixtures.json'
    rejected = root/'rejected_crop_fixtures.json'
    if previous.exists() and not rejected.exists():
        previous_records=read(previous)
        if any(len(f['changes'])==5 for f in previous_records):
            rejected.write_bytes(previous.read_bytes())
    fixtures = []
    for kind, parent in (('control', parent_rom), ('actual', candidate_rom)):
        image = NdsImage.open(parent)
        files = rom_files(image)
        arm = image.read_file('/__arm9__.bin')
        u = machine(arm)
        assert int.from_bytes(u.mem_read(0x020854DC,4),'little') == 0x02313C7C
        modified, changes = bytearray(arm), []
        for address, word in patches.items():
            pattern = bytes(u.mem_read(address-16,32))
            assert arm.count(pattern) == 1
            offset = arm.find(pattern)+16
            modified[offset:offset+4] = struct.pack('<I',word)
            changes.append({'RAM':address,'file_offset':offset,'before':arm[offset:offset+4].hex(),
                            'after':struct.pack('<I',word).hex()})
        image.replace_file('/__arm9__.bin',bytes(modified))
        target = root/f'{filename_prefix}_{kind}_ZERO_BANK_FIXTURE.nds'
        image.save(target)
        saved = rom_files(NdsImage.open(target))
        assert [p for p in files if files[p] != saved[p]] == ['/__arm9__.bin']
        fixtures.append({'kind':kind,'parent':str(parent),'parent_sha256':sha(parent.read_bytes()),
                         'ROM':str(target),'ROM_sha256':sha(target.read_bytes()),'changes':changes,
                         'source_rectangle':list(rectangle), 'manual_crop_fixture':True,
                         'original_price_parent_context_verified':False})
    (root/'native_crop_fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n',encoding='utf-8')
    print('Two explicit crop fixtures: ten setup/literal words; source X/Y separate from zero palette and flags; no artwork substitution.')


def main():
    old,new,clean = (NdsImage.open(p) for p in (PARENT,ROM,Path('work/clean.nds')))
    before,after = rom_files(old),rom_files(new)
    assert sorted(p for p in before if before[p]!=after[p]) == [ARCHIVE,FILE]
    a,b,source = (PxlImage.from_bytes(r.read_file(FILE)) for r in (old,new,clean))
    assert b.source[:b.pixels_offset] == source.source[:source.pixels_offset]
    assert b.source == (ROOT/'marker_price_ownership_RESEARCH_ONLY.pxl').read_bytes()
    owned = {y*256+x for y in range(48,96) for x in range(112,145)}
    assert all(a.indices[n]==b.indices[n] for n in range(65536) if n not in owned)
    assert sum(x!=y for x,y in zip(a.indices,b.indices,strict=True)) == 703
    assert all(b.indices[y*256+x]==source.indices[y*256+x] for y in range(72,112) for x in range(112,152))
    embedded = atlas_indices(new.read_file(ARCHIVE))
    assert all(embedded[y*512:y*512+256]==b.indices[y*256:(y+1)*256] for y in range(256))
    old_embedded = atlas_indices(old.read_file(ARCHIVE))
    assert all(embedded[y*512+256:(y+1)*512]==old_embedded[y*512+256:(y+1)*512] for y in range(256))
    archive_before,archive_after = (IlnkContainer.parse(r.read_file(ARCHIVE)) for r in (old,new))
    assert archive_before.blocks[5][:20]==archive_after.blocks[5][:20]
    assert all(x==y for n,(x,y) in enumerate(zip(archive_before.blocks,archive_after.blocks,strict=True)) if n!=5)
    manifest,prior = read(ROM.with_suffix('.manifest.json')),read(PARENT.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v569' and manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['batches']==prior['batches'] and len(manifest['batches'])==470
    assert manifest['required_batches']==prior['required_batches']
    assert len(read('translations/release_stack.json')['accepted_layers'])==114
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256']==prior['base_sha256']
    stage=manifest['relocations'][FILE]['marker_price_ownership']
    assert sum(r['complete_original_font_ink'] for r in stage['price_cells'])==90
    fixtures=read(ROOT/'native_crop_fixtures.json')
    reports=[]
    for fixture in fixtures:
        parent=NdsImage.open(fixture['parent'])
        f=NdsImage.open(fixture['ROM'])
        aa,bb=rom_files(parent),rom_files(f)
        assert [p for p in aa if aa[p]!=bb[p]]==['/__arm9__.bin']
        changed_bytes={n for c in fixture['changes'] for n in range(c['file_offset'],c['file_offset']+4)}
        assert all(x==y for n,(x,y) in enumerate(zip(aa['/__arm9__.bin'],bb['/__arm9__.bin'],strict=True)) if n not in changed_bytes)
        assert sha(Path(fixture['ROM']).read_bytes())==fixture['ROM_sha256']
        reports.append(capture_report(CAPTURE/f"marker_ownership_v569_zero_{fixture['kind']}",fixture['ROM_sha256']))
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    assert reports[0]['core_options']==reports[1]['core_options']
    tables=[{s['frame']:s for s in r['frames_captured']} for r in reports]
    cases=[]
    for kind,fixture,report,table,atlas in zip(('control','actual'),fixtures,reports,tables,(a,b),strict=True):
        source_save=Path(report['battery_save_preloaded']['source'])
        assert sha(source_save.read_bytes())==report['battery_save_preloaded']['source_sha256']
        image=NdsImage.open(fixture['ROM'])
        for frame in (4300,4600):
            raw=(CAPTURE/f'marker_ownership_v569_zero_{kind}'/f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
            found=[]
            for pos in range(0,len(raw)-48,4):
                w=struct.unpack_from('<12I',raw,pos)
                if w[3]==0x02313F74 and w[7:9]==(112,48) and w[10:12]==(40,64):
                    assert w[6]==0 and w[9]&255==0
                    found.append(pos+0x02000000)
            assert len(found)==1
            u=machine(image.read_file('/__arm9__.bin'));u.mem_write(0x02000000,raw)
            call(u,0xD4170,(found[0],));ptr=u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(ptr,len(atlas.source)))==atlas.source
            shot=Image.open(table[frame]['path']).convert('RGB')
            assert all(native5(shot.getpixel((x,y+261)))==native5(atlas.palette[atlas.indices[(y+48)*256+x+112]])
                       for y in range(64) for x in range(40))
            cases.append({'kind':kind,'frame':frame,'actual_marker_owner':0x02313F74,'view':found[0],
                          'resident_PXL_pointer':ptr,'full_40x64_native_crop_exact':True,
                          'manual_crop_not_original_price_parent':True})
    for frame in (4300,4600):
        shots=[Image.open(t[frame]['path']).convert('RGB') for t in tables]
        for y in range(384):
            for x in range(256):
                expected=native5(shots[0].getpixel((x,y)))
                if x<40 and 261<=y<325:expected=native5(b.palette[b.indices[(y-261+48)*256+x+112]])
                assert native5(shots[1].getpixel((x,y)))==expected
    fresh=capture_report(CAPTURE/'marker_ownership_v569_fresh',sha(ROM.read_bytes()))
    old_fresh=capture_report(CAPTURE/'header_wood_v566_fresh',sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule']==old_fresh['scripted_input_schedule']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']]==[s['PNG_sha256'] for s in old_fresh['frames_captured']]
    assert len({s['frame'] for s in fresh['frames_captured']})==56
    patch=ROM.with_suffix('.xdelta');make_xdelta(Path('work/clean.nds'),ROM,patch)
    reconstructed=ROOT/'v569_reconstructed.nds';apply_xdelta(Path('work/clean.nds'),patch,reconstructed)
    assert reconstructed.read_bytes()==ROM.read_bytes()
    for name in ('graphics_completion_campaign_v1.json','graphics_visual_audit_v150.json'):
        plaques=read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques)==18 and all(r['fully_completed'] is False for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained'])==22
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'profile':manifest['profile'],
           'base':manifest['base_rom'],'base_sha256':manifest['base_sha256'],'patch_sha256':sha(patch.read_bytes()),
           'exact_clean_patch_reconstruction':True,'only_changed_files_from_V566':[ARCHIVE,FILE],
           'changed_marker_pixels':703,'complete_price_font_ink':90,'original_bag_1600_pixels_exact':True,
           'all65536_embedded_marker_indices_match_loose':True,'embedded_frame_and_all_other_blocks_exact':True,
           'all_code_and_other_translations_exact_V566':True,'all470_batches114_layers_retained':True,
           'native_cases':cases,'native_fixture_crop_pixels_exact':10240,'full_pair_screen_pixels_exact':196608,
           'unchanged_unique_startup_frames':56,'original_price_parent_still_unverified':True,
           'experimental':True,'canonical_promoted':False,'all18_plaques_remain_incomplete':True,'full_goal_complete':False}
    (ROOT/'v569_release_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('V569:Sell/Buy full90 ink;original1600-pixel bag;both storage copies;4 native crop cases;56 unchanged startup frames;exact patch pass.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-fixtures',action='store_true')
    if parser.parse_args().prepare_fixtures:prepare()
    else:main()
