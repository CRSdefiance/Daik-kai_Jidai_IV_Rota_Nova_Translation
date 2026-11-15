"""Bind the live Common wheel to exact OBJ banks, palette/OAM and visible pixels."""
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.frame_buttons_v165 import atlas_indices
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROM = Path('out/all_routes_combined_v558_candidate.nds')
ROOT = Path('work/analysis/radial_obj_v560')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/radial_obj_v560')
LABELS = ('Functions', 'Crew Setup', 'Deck View', 'Info', 'Route Map', 'Items')
LIVE = ((11200, 1, 59), (11500, 2, 61), (11800, 4, 61),
        (12100, 3, 74), (12400, 5, 71), (12700, 0, 61))


def decode(data, bank):
    return [((data[bank*1024+((y//8)*8+x//8)*32+(y%8)*4+(x%8)//2] >> ((x&1)*4)) & 15)
            for y in range(32) for x in range(64)]


def main():
    rom, clean, base = [NdsImage.open(p) for p in (ROM, Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds'))]
    digest = sha(ROM.read_bytes())
    report = capture_report(CAPTURE, digest)
    assert report['frames'] == 12700 and not report.get('battery_save_preloaded')
    data = rom.read_file('/GRP/DSOBJ.DK4')
    original_data = clean.read_file('/GRP/DSOBJ.DK4')
    assert data == base.read_file('/GRP/DSOBJ.DK4')
    sprites, original = [[decode(d, bank) for bank in range(6)] for d in (data, original_data)]
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    source_cases = []
    for bank, text in enumerate(LABELS):
        expected = {(6+y)*64+(64-len(text)*5)//2+n*5+x for n, ch in enumerate(text)
                    for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        assert {p for p, v in enumerate(sprites[bank]) if v == 15} == expected
        assert all(a == b for p, (a, b) in enumerate(zip(original[bank], sprites[bank], strict=True))
                   if a != 15 and p not in expected)
        for y in range(5, 18):
            for x in range(3, 61):
                values = {s[y*64+x] for s in original} - {15}
                if not values:
                    assert (x, y) == (23, 11)
                    values = {6}
                    for delta in range(-6, 8):
                        if delta:
                            assert {s[(11-delta)*64+23+delta] for s in original} - {15} == {6}
                assert len(values) == 1
                if y*64+x not in expected:
                    assert sprites[bank][y*64+x] == next(iter(values))
        source_cases.append({'bank': bank, 'English': text, 'complete_native_font_ink': len(expected),
                             'source_frame_padding_and_nonwhite_material_retained': True,
                             'one_concealed_pixel_index6_inferred_from13_original_diagonal_samples': True})
    shots = {s['frame']: s for s in report['frames_captured']}
    live = []
    for frame, bank, origin_x in LIVE:
        image = Image.open(shots[frame]['path']).convert('RGB')
        text = LABELS[bank]
        width = (len(text)-1)*5+6
        expected = {(n*5+x, y) for n, ch in enumerate(text) for y in range(11)
                    for x in range(6) if font.decode(ch).getpixel((x, y))}
        assert all((image.getpixel((origin_x+x, 259+y)) == (255, 255, 255)) == ((x, y) in expected)
                   for y in range(11) for x in range(width))
        live.append({'frame': frame, 'bank': bank, 'English': text,
                     'full_ink_and_blank_font_cell_pixels_exact': width*11,
                     'first_final_letters_and_all_internal_spaces_complete': True})
    state = report['read_only_native_state']
    assert state['read_only_export'] and not state['state_loaded']
    assert state['serialized_RAM_matches_same_frame_direct_export'] and state['main_RAM_unchanged_by_export']
    regions = {}
    for tag in ('LCDM', 'OAMS', 'VMEM', '9REG'):
        entry = state['regions'][tag]
        regions[tag] = Path(entry['path']).read_bytes()
        assert len(regions[tag]) == entry['bytes'] and sha(regions[tag]) == entry['sha256']
    vram, oam, palette, io = [regions[k] for k in ('LCDM', 'OAMS', 'VMEM', '9REG')]
    assert vram[0x80000:0x81800] == data[:6144]
    display = struct.unpack_from('<I', io)[0]
    assert display & 0x10 and (display >> 20) & 3 == 0 and not display & 0x80000000
    assert io[0x244] == 0x82 and struct.unpack_from('<H', io, 0x50)[0] == 0
    raw = (CAPTURE / 'frame_012700_arm9_ram.bin').read_bytes()
    assert raw == (CAPTURE / 'final_arm9_ram.bin').read_bytes()
    view_rects = {}
    for p in range(0, len(raw)-128, 4):
        words = struct.unpack_from('<12I', raw, p)
        if words[0] == 0x0214B190 and words[3] == 0x02313F74 and words[7] == 0 and words[10:] == (64, 24):
            assert words[9] & 255 == 10 and words[8] % 24 == 0
            view_rects[words[8]//24] = struct.unpack_from('<4I', raw, p+0x70)
    assert set(view_rects) == set(range(6))
    canvas, attributes = {}, []
    for slot in range(79, 73, -1):
        a, b, c, _ = struct.unpack_from('<4H', oam, slot*8)
        assert a >> 14 == 1 and b >> 14 == 3
        assert not a & 0x3F00 and not b & 0x3000 and not c & 0x0C00
        tile, pal = c & 1023, c >> 12
        assert tile % 32 == 0 and tile // 32 in range(6)
        bank = tile//32
        x0, y0 = b & 511, a & 255
        assert view_rects[bank] == (x0, y0, x0+64, y0+24)
        for y in range(32):
            for x in range(64):
                value = sprites[bank][y*64+x]
                if value:
                    word = struct.unpack_from('<H', palette, 0x200+pal*32+value*2)[0]
                    canvas[x0+x, y0+y+192] = (word & 31, (word >> 5) & 31, (word >> 10) & 31)
        attributes.append({'main_OAM_slot': slot, 'bank': bank, 'tile_index': tile, 'palette_bank': pal,
                           'native_origin': [x0, y0], 'stored_extent': [64, 32], 'source_frame_extent': [64, 24],
                           'all_coordinates_match_actual_marker_view': True})
    final = Image.open(shots[12700]['path']).convert('RGB')
    assert len(canvas) == 8150 and all(native5(final.getpixel(p)) == rgb for p, rgb in canvas.items())
    marker, earlier = [PxlImage.from_bytes(r.read_file('/_pxl/__marker.pxl')) for r in (rom, base)]
    covered = []
    for bank in range(6):
        changed = [(x, y) for y in range(24) for x in range(64)
                   if marker.indices[(bank*24+y)*256+x] != earlier.indices[(bank*24+y)*256+x]]
        assert all(sprites[bank][y*64+x] for x, y in changed)
        covered.append({'bank': bank, 'marker_caption_changed_points': len(changed),
                        'all_points_covered_by_opaque_native_OBJ_sprite': True})
    assert sum(r['marker_caption_changed_points'] for r in covered) == 1044
    embedded = atlas_indices(rom.read_file('/GRP/CMMNIMG.DK4'))
    assert all(embedded[y*512:y*512+256] == marker.indices[y*256:(y+1)*256] for y in range(256))
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'production_ROM_changed': False,
             'DSOBJ_file_sha256': sha(data), 'whole_DSOBJ_exact_accepted_baseline': True,
             'source_material_and_font_cases': source_cases, 'ordinary_selected_caption_cases': live,
             'physical_OBJ_VRAM_offset': 0x80000, 'all6144_source_tile_bytes_exact': True,
             'standard_main_OBJ_palette_base': 0x200, 'main_DISPCNT': display,
             'VRAM_E_control': io[0x244], 'BLDCNT_zero_no_blending': True,
             'actual_OAM_source_bindings': attributes, 'all8150_visible_wheel_composite_pixels_exact': True,
             'actual_marker_view_positions_match_OAM_sprites': True,
             'marker_edits_opaque_coverage': covered, 'all1044_prior_marker_edits_covered_in_observed_state': True,
             'embedded_marker_copy_indices_exact': True,
             'whole_DSOBJ_VRAM_residency_or_unobserved_animation_states_not_claimed': True,
             'other_action_buttons_and_atlas_consumers_remain_open': True,
             'hardware_or_full_route_verified': False, 'full_goal_complete': False}
    (ROOT / 'source_and_hardware_proof.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print('Common wheel:6 full live captions;6144 actual OBJ VRAM bytes;6 OAM/palette bindings;8150 composite pixels;1044 marker edits opaque-covered.')


if __name__ == '__main__':
    main()
