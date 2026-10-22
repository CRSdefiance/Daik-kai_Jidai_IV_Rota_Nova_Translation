"""Verify actual Asian map previews and route denials; do not claim town visits."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


def main():
    out=Path('work/analysis/maria_asia_v515')
    folder=Path('work/emulation_v193/maria_asia_v515_auto_seoul')
    report_path=folder/'capture_report.json'
    report=json.loads(report_path.read_text(encoding='utf-8'))
    fixture=json.loads((out/'selection_fixture_manifest.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256']==fixture['research_ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames']==27800
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    arm=NdsImage.open(fixture['research_ROM']).read_file('/__arm9__.bin')
    font=GameAsciiFont.from_arm9(arm)
    cases=[]
    for frame,city,labels in [(22600,'Seoul',['Hazelnuts','China','Silk','Silk Cloth','Ginseng']),
                               (22400,'Nagasaki',['Silver','CotClth','T-Shell'])]:
        image=Image.open(folder/f'frame_{frame:06d}_navigation.png').convert('RGB')
        masks=[]
        # This is the map provider's original 20-pixel row spacing and six-pixel
        # glyph advance, distinct from the town portrait panel's 16/5 layout.
        for index,text in enumerate(labels):
            pixels,bounds=complete_mask(font,text,image,136,84+index*20,(230,230,230))
            masks.append({'text':text,'ink_pixels':pixels,'bounds':bounds})
        cases.append({'city':city,'frame':frame,'actual_map_preview_not_docked_town':True,'complete_masks':masks})
    denials=[]
    for frame,city in [(25000,'Seoul'),(27800,'Nagasaki')]:
        image=Image.open(folder/f'frame_{frame:06d}_navigation.png').convert('RGB')
        rows=[]
        for index,text in enumerate(['There is no route','to that city.']):
            pixels,bounds=complete_mask(font,text,image,22,296+16*index,(0,8,0))
            rows.append({'text':text,'ink_pixels':pixels,'bounds':bounds})
        denials.append({'city':city,'frame':frame,'complete_text_rows':rows})
    route_path=out/'seoul_route/water_route_proof.json'
    route=json.loads(route_path.read_text(encoding='utf-8'))
    assert route['candidate_sha256']==fixture['research_ROM_sha256']
    proof={'capture_report':str(report_path),'capture_report_sha256':sha(report_path.read_bytes()),
           'selection_fixture_manifest':str(out/'selection_fixture_manifest.json'),
           'normal_Auto_Move_menu_and_city_selections_with_authorized_Maria_bypass':True,
           'map_preview_complete_specialty_labels':cases,'actual_Auto_Move_route_denials':denials,
           'no_normal_city_docking_claimed':True,'no_savestate_or_inventory_supply_movement_injection':True,
           'read_only_Seoul_water_route_proof':str(route_path),'water_route_proof_sha256':sha(route_path.read_bytes()),
           'next_safe_waypoints':route['waypoint_world_points'],
           'route_cell_centres_not_live_boat_footprint_or_successful_docking_proof':True,
           'Seoul_Osaka_environment_and_alternate_Japan_facility_scenes_still_open':True,
           'all18_plaques_incomplete':True,'full_goal_complete':False}
    (out/'map_and_route_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Asian map previews:8 complete labels;two complete route denials;native shoreline waypoints recorded.')


if __name__=='__main__':main()
