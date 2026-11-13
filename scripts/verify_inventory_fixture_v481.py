"""Exact native GPU captures from explicitly synthetic inventory; no acquisition credit."""

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

ROOT = Path('work/analysis/equipment_names_v481')
CAPTURE = Path('work/emulation_v193/inventory_fixture_v481_live')


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    rom_path = Path(report['ROM'])
    assert sha(rom_path.read_bytes()) == report['ROM_sha256'] == '1d513b81762499f0fd6a2edeeabb182a69c334756fc9261f70c07a0110984b9e'
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert len(report['synthetic_inventory_fixtures']) == 1 and report['normal_acquisition_verified'] is False
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    rom = NdsImage.open(rom_path)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    palette = PxlImage.from_bytes(rom.read_file('/_pxl/towninfo.pxl')).palette
    atlas = PxlImage.from_bytes(rom.read_file('/_pxl/item.pxl')).render().convert('RGB')
    cases = []
    for item, name, inventory_frame, tooltip_frame, rect in (
        (40, 'Red-Haired Pirate Sword', 3500, 6000, [16,208,158,224]),
        (71, "Saladin's Silver Armor", 4000, 6100, [64,208,200,224]),
        (83, "Rocco's Sailing Guide", 4500, 6200, [94,208,224,224]),
    ):
        def capture(frame):
            row = next(r for r in report['frames_captured'] if r['frame'] == frame)
            path = Path(row['path'])
            assert sha(path.read_bytes()) == row['PNG_sha256']
            return Image.open(path).convert('RGB'), row
        inventory, inv_row = capture(inventory_frame)
        inventory_mask = compact_mask(font, name, inventory, 56, 24)
        image, screenshot = capture(tooltip_frame)
        left, top, right, bottom = rect
        ink, bounds = complete_mask(font, name, image, left+2, top+2, (0,8,0))
        expected = {(left+2+n*6+x,top+2+y) for n,c in enumerate(name)
                    for y in range(11) for x in range(6) if font.decode(c).getpixel((x,y))}
        tile = paper(right-left,bottom-top,palette)
        for y in range(bottom-top):
            for x in range(right-left):
                point = left+x,top+y
                rgb = (0,8,0) if point in expected else palette[tile[y*(right-left)+x]][:3]
                assert native5(image.getpixel(point)) == native5(rgb)
        slot_x = {40:16,71:64,83:112}[item]
        assert [native5(v) for v in image.crop((slot_x,224,slot_x+32,256)).get_flattened_data()] == [
            native5(v) for v in atlas.crop((0,item*32,32,(item+1)*32)).get_flattened_data()]
        state = item_state(arm,CAPTURE/f'frame_{tooltip_frame:06d}_arm9_ram.bin',item)
        assert state['owner_descriptor_type'] == 2 and state['owner_index_or_city_if_type2_or4'] == 1
        cases.append({'item_id':item,'name':name,'inventory_name':inventory_mask,'inventory_screenshot':inv_row,
                      'tooltip_screenshot':screenshot,'tooltip_ink_pixels':ink,'tooltip_glyph_bounds':bounds,
                      'entire_paper_rect_exact':rect,'icon_pixels_exact':1024,'equipped_state':state})
    proof = {'candidate':str(rom_path),'candidate_sha256':report['ROM_sha256'],'report':str(report_path),
             'report_sha256':sha(report_path.read_bytes()),'synthetic_inventory_fixture':True,
             'normal_acquisition_verified':False,'original_donor_save_preserved':True,'cases':cases,
             'goal_complete':False,'limits':['Three equipment cases on Hodram; other owners, conditions and names remain open.',
                                           'No hardware or full-playthrough verification.']}
    (ROOT/'fixture_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'verified_fixture_cases':len(cases),'tooltip_ink_pixels':sum(r['tooltip_ink_pixels']for r in cases)}))


if __name__ == '__main__':
    main()
