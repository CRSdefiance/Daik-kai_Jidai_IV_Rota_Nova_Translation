"""Audit complete current control lettering and source material without native-use claims."""
import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.compact_font import layout
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.frame_buttons_v165 import atlas_indices
from scripts.review_action_materials_v561 import GROUPS

ROOT = Path('work/analysis/action_materials_v561')
ROM = Path('out/all_routes_combined_v558_candidate.nds')


def main():
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    data = current.read_file('/_pxl/__frame.pxl')
    original_data = clean.read_file('/_pxl/__frame.pxl')
    image, original = PxlImage.from_bytes(data), PxlImage.from_bytes(original_data)
    assert data[:image.pixels_offset] == original_data[:original.pixels_offset]
    batch = json.loads(Path('translations/frame_action_buttons_graphics_v7.json').read_text(encoding='utf-8'))
    prototype = json.loads((ROOT/'local_texture_prototype_proof.json').read_text(encoding='utf-8'))
    assert all(r['source_visible_points_restored'] == 0 for r in prototype['records'])
    proposed = PxlImage.from_bytes((ROOT/'action_RESEARCH_ONLY.pxl').read_bytes())
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    cases = []
    for index, row in enumerate(batch['records']):
        box = row.get('draw_box', row['box'])
        l,t,r,b = box
        colour = row.get('color_index', batch['color_index'])
        text = row['text']
        expected = set()
        if row.get('font_face', 'native-ascii') != 'native-ascii':
            mask, _, _ = layout(text, tuple(box), word_space_width=row.get('compact_word_space_width',2), font_face=row['font_face'])
            expected = {(l+x,t+y) for y in range(b-t) for x in range(r-l) if mask.getpixel((x,y))}
        else:
            offsets, width = [], 0
            for ch in text:
                glyph = font.decode(ch)
                assert not glyph.crop((0,0,6,2)).getbbox()
                bounds = glyph.getbbox()
                if row.get('glyph_spacing') == 'native-ink-v1':
                    offsets.append(width-bounds[0] if bounds else width)
                    width += bounds[2]-bounds[0]+1 if bounds else 3
                else:
                    offsets.append(width)
                    width += batch['advance']
            tx,ty = l+(r-l-width)//2,t+(b-t-9)//2
            expected = {(tx+offset+x,ty+y-2) for offset,ch in zip(offsets,text,strict=True)
                        for y in range(2,11) for x in range(6) if font.decode(ch).getpixel((x,y))}
        actual = {(x,y) for y in range(t,b) for x in range(l,r) if image.indices[y*256+x] == colour}
        assert actual == expected, (text, sorted(actual-expected)[:4], sorted(expected-actual)[:4])
        assert all(l<=x<r and t<=y<b for x,y in expected)
        assert all(proposed.indices[y*256+x] == image.indices[y*256+x] for y in range(t,b) for x in range(l,r)
                   if index >= 12 or (x,y) in expected)
        case = {'id':row['id'],'English':text,'source_Japanese':row['source_japanese'],
                'box':row['box'],'complete_font_ink_pixels':len(expected),
                'complete_first_final_letters_and_spaces_exact':True,
                'actual_consumer_and_native_crop_not_claimed':True,'fully_completed':False}
        if index >= 15:
            assert {image.indices[y*256+x] for y in range(t,b) for x in range(l,r)} <= {0,colour}
            case['all_background_points_are_exact_index_zero'] = True
        if index < 12:
            sx,sy = GROUPS[index//6][index%6]
            width = 40 if index < 6 else 48
            white = {(x,y) for y in range(2,13) for x in range(3,width-3)
                     if original.indices[(sy+y)*256+sx+x] == 15}
            shadow = {(x,y) for y in range(2,13) for x in range(3,width-3)
                      if original.indices[(sy+y)*256+sx+x] == 0 and
                      any(abs(x-xx)<=2 and abs(y-yy)<=2 for xx,yy in white)}
            material = {(sx+x,sy+y) for y in range(2,13) for x in range(3,width-3)
                        if (x,y) not in white|shadow and (sx+x,sy+y) not in expected}
            assert all(image.indices[y*256+x] == original.indices[y*256+x] for x,y in material)
            case['source_material_points_exact_outside_conservative_Japanese_mask'] = len(material)
        cases.append(case)
    embedded = atlas_indices(current.read_file('/GRP/CMMNIMG.DK4'))
    assert all(embedded[y*512+256:(y+1)*512] == image.indices[y*256:(y+1)*256] for y in range(256))
    origins = {tuple(row['box'][:2]) for row in batch['records'][15:]}
    snapshots = []
    for path in (
            Path('E:/Rota Nova translations/Generated/work/emulation_v193/radial_obj_v560/frame_012700_arm9_ram.bin'),
            Path('E:/Rota Nova translations/Generated/work/emulation_v193/fleet_wallpaper_v559_navigation/frame_006700_arm9_ram.bin')):
        raw = path.read_bytes()
        matches = []
        for pos in range(0,len(raw)-48,4):
            words = struct.unpack_from('<12I',raw,pos)
            if words[3] == 0x02313F60 and tuple(words[7:9]) in origins and 0<words[10]<=256 and 0<words[11]<=256:
                matches.append({'address':0x02000000+pos,'fields':list(words)})
        snapshots.append({'path':str(path),'sha256':sha(raw),'exact_caption_origin_view_matches':matches})
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'cases':cases,
           'all22_complete_stored_font_masks_and_bounds_exact':True,
           'all65536_embedded_frame_indices_exact_to_loose':True,
           'all83_palette_banks_header_and_extent_exact_clean':True,
           'current_visible_material_not_changed_by_nearest_row_reconstruction':True,
           'conservative_shadow_mask_is_a_review_assumption_not_original_shadow_mapping':True,
           'alternative_changes_only_concealed_reconstruction_and_is_not_integrated':True,
           'prototype_changed_pixels':sum(a!=b for a,b in zip(image.indices,proposed.indices,strict=True)),
           'seven_miniature_cells_have_exact_zero_background':True,
           'two_ordinary_snapshot_exact_caption_origin_census':snapshots,
           'snapshot_absence_is_not_global_nonuse':True,
           'ordinary_native_consumers_and_crops_remain_open':True,
           'production_ROM_changed':False,'full_goal_complete':False}
    (ROOT/'current_material_and_font_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('22 stored controls:full glyphs/bounds and65536 embedded pixels pass;7 miniature backgrounds exactzero. Alternative texture remains research only.')


if __name__ == '__main__':
    main()
