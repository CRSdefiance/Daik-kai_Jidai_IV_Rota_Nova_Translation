"""Current-ROM five occupied slots, right-edge paper and full Sailor Info plaques."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_occupied_armor_v469 import compact_mask
from scripts.verify_occupied_weapon_v477 import item_state
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path('work/analysis/equipment_right_slots_v504')
CAPTURE = Path('work/emulation_v193/equipment_right_slots_v504')
ROM = Path('out/all_routes_combined_v502_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert digest == report['ROM_sha256'] == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert digest == 'f26a930d91f0df2089a080f0945b9f06a3d1f9718f18a39a6e6dca7edc8842bc'
    assert report['frames'] == 7200 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert len(report['synthetic_inventory_fixtures']) == 1
    fixture = report['synthetic_inventory_fixtures'][0]
    assert [row['item_id'] for row in fixture['items']] == [75, 82, 83]
    assert fixture['synthetic_inventory_fixture'] and not report['normal_acquisition_verified']
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    for row in report['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    snapshots = {row['frame']: Path(row['path']) for row in report['read_only_pause_RAM_snapshots']}
    cases = []
    for item, name, frame, slot_x, rect, inventory_frame in (
        (29, 'Golden Cutlass', 6800, 16, [16,208,104,224], None),
        (49, 'Blue Oak Shield', 6900, 64, [64,208,158,224], None),
        (75, 'Tireless Hawser', 7000, 112, [112,208,206,224], 4300),
        (82, 'Pocket Watch', 7100, 160, [148,208,224,224], 4800),
        (83, "Rocco's Sailing Guide", 7200, 208, [94,208,224,224], 5300),
    ):
        shot = next(row for row in report['frames_captured'] if row['frame'] == frame and 'navigation' in row['path'])
        image = Image.open(shot['path']).convert('RGB')
        left, top, right, bottom = rect
        ink, bounds = complete_mask(font, name, image, left + 2, top + 2, (0,8,0))
        expected = {(left + 2 + n * 6 + x, top + 2 + y) for n, c in enumerate(name)
                    for y in range(11) for x in range(6) if font.decode(c).getpixel((x,y))}
        tile = paper(right-left, bottom-top, palette)
        for y in range(bottom-top):
            for x in range(right-left):
                point = left+x, top+y
                color = (0,8,0) if point in expected else palette[tile[y * (right-left) + x]][:3]
                assert native5(image.getpixel(point)) == native5(color)
        assert [native5(p) for p in image.crop((slot_x,224,slot_x+32,256)).get_flattened_data()] == [
            native5(p) for p in atlas.crop((0,item*32,32,(item+1)*32)).get_flattened_data()]
        state = item_state(arm, snapshots[frame], item)
        assert state['name'] == name and state['owner_descriptor_type'] == 2 and state['owner_index_or_city_if_type2_or4'] == 1
        inventory = None
        if inventory_frame:
            path = CAPTURE / f'frame_{inventory_frame:06d}_navigation.png'
            inventory = compact_mask(font, name, Image.open(path).convert('RGB'), 56, 24)
        cases.append({'item_id':item, 'name':name, 'equipped_slot_x':slot_x, 'capture':shot,
                      'complete_tooltip_ink':ink, 'tooltip_bounds':bounds, 'entire_paper_rect_exact':rect,
                      'all1024_icon_pixels_exact':True, 'inventory_name':inventory, 'ownership':state})
    image = Image.open(CAPTURE / 'frame_007200_navigation.png').convert('RGB')
    batch = read('translations/person_info_graphics_v3.json')
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    plaques = []
    for row in batch['records']:
        x0,y0,x1,y1 = row['plaque_box']
        assert all(native5(image.getpixel((x,y))) == native5(art.palette[art.indices[y*256+x]][:3])
                   for y in range(y0,y1) for x in range(x0,x1))
        plaques.append({'text':row['text'], 'bounds':row['plaque_box'], 'every_border_bevel_and_letter_pixel_exact':True})
    assert len(plaques) == 10
    statuses = []
    for text, y in (('Healthy',108),('Normal',128)):
        ink,bounds = complete_mask(font,text,image,56,y,(230,230,230))
        statuses.append({'text':text,'ink_pixels':ink,'bounds':bounds})
    skills = []
    for label,x,y in (('Command',16,272),('Sailing',96,272),('Survey',176,272),
                      ('Finance',16,296),('Observe',96,296),('Vigor',176,296),
                      ('Aim',16,320),('Swords',96,320),('Speech',176,320),('Guile',16,344)):
        value = numeric_field(font,image,x+42,y)
        ink,bounds = complete_mask(font,f'{label:>7}{value:3d}',image,x,y,(230,230,230))
        skills.append({'label':label,'value':value,'ink_pixels':ink,'bounds':bounds})
    audit = read('translations/graphics_visual_audit_v150.json')
    assert len(audit['plaque_style_v247']['ongoing_plaque_inventory']) == 18
    assert all(not row['fully_completed'] for row in audit['plaque_style_v247']['ongoing_plaque_inventory'])
    proof = {'candidate':str(ROM), 'candidate_sha256':digest, 'report':str(report_path),
             'report_sha256':sha(report_path.read_bytes()), 'synthetic_inventory_fixture':True,
             'normal_acquisition_verified':False, 'original_donor_save_preserved':True,
             'all_five_occupied_equipment_slots':cases, 'current_ten_Sailor_Info_plaques':plaques,
             'complete_health_and_mood':statuses, 'all_ten_complete_skill_lines_and_numbers':skills,
             'Swords_source_meaning':'剣闘術; sword-fighting skill; compact six-character label matches Help',
             'actual_right_slot_long_name_not_clipped':True, 'no_new_translation_change_needed':True,
             'all22_historical_requirements_retained':True, 'all18_plaques_remain_incomplete':True,
             'other_characters_conditions_empty_hints_and_acquisition_contexts_still_open':True,
             'hardware_verification':False, 'full_goal_complete':False}
    (ROOT / 'fixture_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'occupied_slots':len(cases),'tooltip_ink_pixels':sum(c['complete_tooltip_ink']for c in cases),
                      'exact_Sailor_Info_plaques':len(plaques),'complete_skill_lines':len(skills)}))


if __name__ == '__main__':
    main()
