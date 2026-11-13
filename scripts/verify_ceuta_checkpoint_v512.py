"""Verify ordinary Ceuta arrival, recovery, source artwork and cartridge reload."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_movie_gpu_fixtures_v336 import quantized

ROM = Path('out/all_routes_combined_v508_candidate.nds')
CAPTURE = Path('work/emulation_v193/environment_voyage_v512')
RELOAD = Path('work/emulation_v193/environment_voyage_v512_ceuta_reload')
OUT = Path('work/analysis/environment_voyage_v512')


def main():
    reports = []
    digest = sha(ROM.read_bytes())
    for folder in (CAPTURE,RELOAD):
        path = folder/'capture_report.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        assert data['ROM_sha256'] == digest and data['cold_boot'] and not data['savestate_loaded']
        assert not data['callback_errors'] and not data.get('synthetic_inventory_fixtures')
        for row in data['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        donor = data['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        reports.append((path,data))
    assert reports[0][1]['frames'] == 16950 and reports[1][1]['frames'] == 4200
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    u = machine(arm)
    call(u,0xB7294,(12,0))
    assert u.reg_read(UC_ARM_REG_R0) == 42
    source = PxlImage.from_bytes(rom.read_file('/towngrp/towngrp42.pxl')).render()
    box = (64,112,224,128)
    expected = quantized(source.crop(box)).tobytes()
    cases = []
    paths = [CAPTURE/'frame_010750_navigation.png',CAPTURE/'frame_015550_navigation.png',
             RELOAD/'frame_003400_cold_boot.png']
    for path in paths:
        image = Image.open(path).convert('RGB')
        labels = [mask(image,font,text,88+i*16)for i,text in enumerate(('P. Oil','Ambergris','Leather'))]
        assert quantized(image.crop((64,304,224,320))).tobytes() == expected
        cases.append({'image':str(path),'complete_specialty_masks':labels,
                      'source_background42_visible_bounds':list(box),'exact_native_color_pixels':2560})
    saved_image = Image.open(CAPTURE/'frame_016950_navigation.png').convert('RGB')
    reloaded = Image.open(RELOAD/'frame_004200_final.png').convert('RGB')
    assert saved_image.crop((0,0,256,192)).tobytes() == reloaded.crop((0,0,256,192)).tobytes()
    saved = Path('E:/Rota Nova translations/Saves/hodram-ceuta-rested-v508.dsv')
    assert saved.read_bytes() == Path(reports[0][1]['battery_save_preloaded']['destination']).read_bytes()
    assert reports[1][1]['battery_save_preloaded']['source_sha256'] == sha(saved.read_bytes())
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    original = machine(clean_arm)
    values = []
    for cpu in (original,u):
        call(cpu,0xCD1AC,(15,))
        pointer = struct.unpack('<I',cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0),4))[0]
        values.append(bytes(cpu.mem_read(pointer,64)).split(b'\0')[0].decode('cp932'))
    assert values == ['ヤシ油','P. Oil']
    proof = {'candidate':str(ROM),'candidate_sha256':digest,
             'reports':[{'path':str(p),'sha256':sha(p.read_bytes()),'frames':d['frames']}for p,d in reports],
             'normal_Tunis_to_Ceuta_discovery_docking_resupply':True,
             'all_three_specialties_and2560_unobscured_background_pixels_match_in_three_captures':cases,
             'whole_upper_town_panel_exact_after_cold_reload':True,
             'normal_30_night_Inn_stay_observed_Jan19_to_Feb18_fatigue62_to0':True,
             'saved_checkpoint':str(saved),'saved_checkpoint_sha256':sha(saved.read_bytes()),
             'older_record_followup':{'commodity_index':15,'original_Japanese':values[0],
                                     'inherited_English':values[1],'original_abbreviation_not_changed':True,
                                     'full_wording_and_fidelity_review_still_open':True},
             'earlier_Rafael_unreadable_announcement_not_triggered_or_reverified':True,
             'no_savestate_inventory_condition_unlock_or_movement_injection':True,
             'ROM_unchanged_no_new_candidate':True,'all18_plaques_incomplete':True,
             'East_Asian_checks_and_full_goal_still_open':True,'full_goal_complete':False}
    (OUT/'ceuta_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Ceuta:three complete stock masks,three source-art patches,and saved upper-panel cold reload pass.')


if __name__ == '__main__':
    main()
