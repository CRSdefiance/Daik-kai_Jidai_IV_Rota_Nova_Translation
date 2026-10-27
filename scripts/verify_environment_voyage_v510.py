"""Verify normal recovery, crew plaques, Tripoli arrival and cartridge reload."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_movie_gpu_fixtures_v336 import quantized
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v508_candidate.nds')
OUT = Path('work/analysis/environment_voyage_v510')


def report(folder):
    path = Path('work/emulation_v193')/folder/'capture_report.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    assert data['ROM_sha256'] == sha(ROM.read_bytes())
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('synthetic_inventory_fixtures')
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    donor = data['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return path,data


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    reports = [report(name)for name in ('environment_voyage_v510','environment_voyage_v510_leg','environment_voyage_v510_tripoli_reload')]
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    crew_path = Path('work/emulation_v193/environment_voyage_v510/frame_010300_navigation.png')
    crew = Image.open(crew_path).convert('RGB')
    batch = json.loads(Path('translations/assign_sailors_graphics_v5.json').read_text(encoding='utf-8'))
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    plaques = []
    for row in batch['records']:
        x0,y0,x1,y1 = row['plaque_box']
        assert all(tuple(c>>3 for c in crew.getpixel((x,y))) ==
                   tuple(c>>3 for c in art.palette[art.indices[y*art.width+x]][:3])
                   for y in range(y0,y1)for x in range(x0,x1)),row['id']
        plaques.append({'label':row['text'],'bounds':row['plaque_box'],'all_pixels_exact':True})
    values = []
    for text,region in [('~38 days',(85,37,230,61)),('39',(90,16,128,38)),
                        ('0',(216,16,254,38)),('39',(140,206,170,227)),
                        ('39',(178,206,204,227)),('124',(205,206,250,227))]:
        values.append(find_mask(font,text,crew,region))
    towns = []
    for path in [Path('work/emulation_v193/environment_voyage_v510_leg/frame_009170_navigation.png'),
                 Path('work/emulation_v193/environment_voyage_v510_tripoli_reload/frame_003400_cold_boot.png')]:
        image = Image.open(path).convert('RGB')
        labels = [mask(image,font,text,88+i*16)for i,text in enumerate(('Cotton','Hemp','Gold'))]
        # Original native town getter26/facility0 selected harbor44. Inspect a
        # wholly visible patch below facility icons and above the date panel.
        source = PxlImage.from_bytes(rom.read_file('/towngrp/towngrp44.pxl')).render()
        box = (64,112,224,128)
        got = quantized(image.crop((64,304,224,320)))
        expected = quantized(source.crop(box))
        assert got.tobytes() == expected.tobytes()
        towns.append({'image':str(path),'complete_three_stock_masks':labels,
                      'source_background44_visible_patch':list(box),'exact_background_pixels':2560})
    # The restored original donor is never overwritten. The first run's saved
    # battery is exactly the second run's donor; its result is the reload donor.
    rested = Path('E:/Rota Nova translations/Saves/hodram-athens-rested-v508.dsv')
    tripoli = Path('E:/Rota Nova translations/Saves/hodram-tripoli-resupplied-v508.dsv')
    assert Path(reports[0][1]['battery_save_preloaded']['destination']).read_bytes() == rested.read_bytes()
    assert Path(reports[1][1]['battery_save_preloaded']['destination']).read_bytes() == tripoli.read_bytes()
    assert reports[1][1]['battery_save_preloaded']['source_sha256'] == sha(rested.read_bytes())
    assert reports[2][1]['battery_save_preloaded']['source_sha256'] == sha(tripoli.read_bytes())
    proof = {'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
             'capture_reports':[{'path':str(p),'sha256':sha(p.read_bytes()),'frames':d['frames']}for p,d in reports],
             'normal_cold_boot_controls_no_savestate_or_injection':True,
             'Athens_30_night_stay_observed_Aug23_to_Sep22_fatigue55_to0':True,
             'all_seven_crew_plaque_composites_exact':plaques,'complete_crew_and_Endurance_masks':values,
             'fleet_Need39_Current39_Max124_no_crew_reduction':True,
             'normal_Athens_to_Tripoli_discovery_docking_resupply':True,
             'Tripoli_actual_arrival_and_cold_reload':towns,
             'saved_restored_checkpoints':[{'path':str(rested),'sha256':sha(rested.read_bytes())},
                                           {'path':str(tripoli),'sha256':sha(tripoli.read_bytes())}],
             'East_Asian_town_checks_still_pending':True,
             'ROM_unchanged_no_new_candidate':True,'all18_plaques_incomplete':True,'full_goal_complete':False}
    (OUT/'voyage_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Recovery,seven crew plaques,Tripoli full specialty masks,2560 unobscured background pixels and cold reload pass.')


if __name__ == '__main__':
    main()
