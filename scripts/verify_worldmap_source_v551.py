"""Ordinary World Map resource residency and actual bitmap-plane evidence."""
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v546_candidate.nds')
ROOT = Path('work/analysis/worldmap_source_v551')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/worldmap_source_v551')
BASE = 0x02000000


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    digest = sha(ROM.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    report = read(CAPTURE/'capture_report.json')
    assert report['ROM_sha256'] == digest and report['frames'] == 36000 and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['scripted_input_schedule'] == read('work/analysis/town_force_texture_v544/map_inputs.json')
    state = read(CAPTURE/'native_state/native_state.json')
    assert state['read_only_export'] and not state['state_loaded']
    assert state['serialized_RAM_matches_same_frame_direct_export'] and state['main_RAM_unchanged_by_export']
    for region in state['regions'].values():
        assert sha(Path(region['path']).read_bytes()) == region['sha256']
    snapshot = CAPTURE/'frame_036000_arm9_ram.bin'
    raw = snapshot.read_bytes()
    final = (CAPTURE/'final_arm9_ram.bin').read_bytes()
    assert len(raw) == 0x400000 and raw == final
    seaarea,seamap = [rom.read_file(p) for p in ('/_pxl/seaarea.pxl','/_pxl/seamap.pxl')]
    assert seaarea == clean.read_file('/_pxl/seaarea.pxl') and seamap == clean.read_file('/_pxl/seamap.pxl')
    at = raw.find(seaarea)
    assert at >= 0 and raw.find(seaarea,at+1)<0
    assert raw.find(seamap) == -1
    fields = struct.unpack_from('<5I',raw,0x0231336C-BASE)
    unused = struct.unpack_from('<5I',raw,0x02313B8C-BASE)
    assert fields[0] == unused[0] == 0x02160538
    assert fields[4] != 0xFFFFFFFF and unused[4] == 0xFFFFFFFF
    name = b'_pxl/seaarea.pxl\0'
    assert raw[fields[3]-BASE:fields[3]-BASE+len(name)] == name
    before = (Path('E:/Rota Nova translations/Generated/work/emulation_v193/legacy_descriptor_v547')/'frame_002400_arm9_ram.bin').read_bytes()
    assert before.find(seaarea) == -1 and struct.unpack_from('<I',before,0x31336C+16)[0] == 0xFFFFFFFF
    # Complete original page-copy routine with actual current native cache state.
    arm = rom.read_file('/__arm9__.bin')
    ranges = [(0x474DC,0x47608),(0xD6524,0xD6C90)]
    assert all(arm[a:b] == clean.read_file('/__arm9__.bin')[a:b] for a,b in ranges)
    u = machine(arm)
    u.mem_write(BASE,raw)
    destination = 0x02470020
    copies = []
    for page in range(8):
        u.mem_write(destination-16,b'\xA5'*(19520+32))
        executed = call(u,0x474DC,(0,page,destination),instruction_limit=200000)
        expected = seaarea[276+page*19520:276+(page+1)*19520]
        assert bytes(u.mem_read(destination,19520)) == expected
        assert bytes(u.mem_read(destination-16,16)) == b'\xA5'*16
        assert bytes(u.mem_read(destination+19520,16)) == b'\xA5'*16
        assert 0x020DED50 not in executed and 0x020DEBDC not in executed
        copies.append({'page':page,'complete_packed_pixel_bytes':19520,'sha256':sha(expected),
                       'full_native_return_stack_saved_registers_and_guards_exact':True,
                       'actual_resident_cache_used_without_file_bridge':True,
                       'page_selection_supplied_not_live_current_page':True})
    header = 0x02279B38
    assert struct.unpack_from('<5I',raw,header-BASE) == (4,61,160,20,52)
    palette = raw[header-BASE+20:header-BASE+52]
    assert palette == seaarea[20:52]
    # All eight stored banks duplicate the same16 colours. RGB equality cannot
    # identify a unique selected bank or a particular native source page.
    assert all(seaarea[20+bank*32:52+bank*32] == palette for bank in range(8))
    packed = raw[header-BASE+52:header-BASE+52+19520]
    indices = [n for byte in packed for n in (byte&15,byte>>4)]
    source_page = [n for byte in seaarea[276+7*19520:276+8*19520] for n in (byte&15,byte>>4)]
    assert sum(bool(n) for n in indices) == 9674
    assert all(n == original or n == 0 for n,original in zip(indices,source_page))
    direct_view = struct.unpack_from('<12I',raw,0x02190E3C-BASE)
    assert direct_view[4] == header and direct_view[10:12] == (244,160)
    io = Path(state['regions']['9REG']['path']).read_bytes()
    vram = Path(state['regions']['LCDM']['path']).read_bytes()
    assert struct.unpack_from('<I',io,0)[0] == 0x1191B
    assert struct.unpack_from('<I',io,0x1000)[0] == 0x11813
    assert struct.unpack_from('<H',io,0x100E)[0] == struct.unpack_from('<H',io,0xE)[0] == 0x4084
    assert io[0x243] == 0x81 and io[0x242] == 0x84
    shot = next(s for s in report['frames_captured'] if s['frame']==36000)
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    picture = Image.open(shot['path']).convert('RGB')
    pixels = picture.load()
    colours = [(v&31,(v>>5)&31,(v>>10)&31) for v, in struct.iter_unpack('<H',palette)]
    bitmap_overlay_points = [(x,y) for y in range(160) for x in range(244)
                             if colours[indices[y*244+x]] != native5(pixels[x+6,y+208])]
    assert len(bitmap_overlay_points) == 281
    comparisons = []
    for offset,screen in ((0x40000,0),(0x60000,192)):
        words = struct.unpack_from('<65536H',vram,offset)
        matched = 0
        for y in range(160):
            for x in range(244):
                value = words[(y+16)*256+x+6]
                color = (value&31,(value>>5)&31,(value>>10)&31)
                assert native5(pixels[x+6,y+16+screen]) == color
                matched += 1
        comparisons.append({'physical_VRAM_offset':offset,'screen_offset':screen,
                            'crop_origin':[6,16+screen],'complete244x160_pixels_exact':matched})
    assert comparisons[1]['complete244x160_pixels_exact'] == 39040
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'production_ROM_changed':False,
             'ordinary_cold_boot_no_fixture_cheat_or_preloaded_save':True,
             'capture_report':str(CAPTURE/'capture_report.json'),'snapshot':str(snapshot),'snapshot_sha256':sha(raw),
             'actual_complete_seaarea_atlas_in_RAM':{'pointer':BASE+at,'bytes':len(seaarea),'sha256':sha(seaarea),
                  'owner':0x0231336C,'owner_fields':list(fields)},
             'seamap_owner_uncached_and_exact_file_absent_in_this_snapshot':{'owner':0x02313B8C,'fields':list(unused)},
             'earlier_chooser_state_seaarea_uncached':True,'all8_original_blue_page_copy_calls':copies,
             'direct244x160_descriptor_copies_first_palette_bank':{'header':header,'palette_bytes':32},
             'all8_seaarea_palette_banks_identical_unique_selection_not_inferred':True,
             'actual_direct_map_view':{'address':0x02190E3C,'words':list(direct_view)},
             'actual_dynamic_bitmap_is_page7_with_background_colour_mask':{'nonzero_source_exact_pixels':9674,
                  'background_index0_pixels':29366,'packed_pixels_sha256':sha(packed)},
             'direct_bitmap_to_live_crop_source_colour_matches':38759,
             'remaining_281_overlay_points_not_silently_excluded':bitmap_overlay_points,
             'VRAM_bitmap_comparisons':comparisons,
             'raw_IO_POWCNT_value_not_assumed_to_be_engine_screen_assignment':True,
             'pinned_emulator_source_receipt':str(ROOT/'core_source/source_receipt.json'),
             'source_page7_dynamic_mask_and_observed_origin_verified':True,
             'actual_mask_creation_and281_overlay_producers_not_yet_traced':True,
             'legacy_CMMN_or_sepia_source_usage_not_proven':True,
             'all22_requirements_and18_incomplete_plaques_retained':True,'full_goal_complete':False}
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'residency_and_bitmap_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Ordinary World Map:complete blue atlas residency,8 original guarded page copies and39040-pixel actual lower VRAM bitmap verified; sepia/legacy consumers remain open.')


if __name__ == '__main__':
    main()
