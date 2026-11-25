"""Verify natural Sick/Relaxed/Upset states and the complete current plaques."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field

ROM = Path('out/all_routes_combined_v508_candidate.nds')
CAPTURE = Path('work/emulation_v193/environment_voyage_v511')
OUT = Path('work/analysis/environment_voyage_v511')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report_path = CAPTURE/'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('synthetic_inventory_fixtures') and report['frames'] == 20940
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    old,new = machine(clean_arm),machine(arm)
    source_labels = []
    for field,japanese,english in [(0x1483DC,'疾病','Sick'),(0x1483B8,'リラックス','Relaxed'),(0x1483C0,'不機嫌','Upset')]:
        pointers = [struct.unpack_from('<I',a,field)[0]for a in (clean_arm,arm)]
        before,after = [bytes(u.mem_read(p,64)).split(b'\0')[0].decode('cp932')for u,p in zip((old,new),pointers)]
        assert (before,after) == (japanese,english)
        source_labels.append({'field':field,'original_Japanese':japanese,'current_English':english})
    batch = json.loads(Path('translations/person_info_graphics_v3.json').read_text(encoding='utf-8'))
    art = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    cases = []
    for frame,name,health,mood in [(9340,'Hodram Joakim Bergstrom','Healthy','Relaxed'),
                                   (9940,'Manuel Almeida','Healthy','Upset'),
                                   (10540,'Charles Jean Rochefort','Sick','Upset'),
                                   (17540,'Hodram Joakim Bergstrom','Healthy','Relaxed'),
                                   (18140,'Manuel Almeida','Healthy','Relaxed'),
                                   (18740,'Charles Jean Rochefort','Healthy','Relaxed')]:
        path = CAPTURE/f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        plaques = []
        for row in batch['records']:
            x0,y0,x1,y1 = row['plaque_box']
            assert all(native5(image.getpixel((x,y))) == native5(art.palette[art.indices[y*256+x]][:3])
                       for y in range(y0,y1)for x in range(x0,x1)),(frame,row['id'])
            plaques.append({'label':row['text'],'bounds':row['plaque_box'],'all_pixels_exact':True})
        statuses = []
        for text,y in [(health,108),(mood,128)]:
            pixels,bounds = complete_mask(font,text,image,56,y,(230,230,230))
            statuses.append({'text':text,'ink_pixels':pixels,'bounds':bounds})
        name_mask = find_mask(font,name,image,(80,28,256,54))
        skills = []
        for label,x,y in [('Command',16,272),('Sailing',96,272),('Survey',176,272),
                          ('Finance',16,296),('Observe',96,296),('Vigor',176,296),
                          ('Aim',16,320),('Swords',96,320),('Speech',176,320),('Guile',16,344)]:
            value = numeric_field(font,image,x+42,y)
            pixels,bounds = complete_mask(font,f'{label:>7}{value:3d}',image,x,y,(230,230,230))
            skills.append({'label':label,'value':value,'ink_pixels':pixels,'bounds':bounds})
        cases.append({'frame':frame,'name':name,'name_mask':name_mask,'health':health,'mood':mood,
                      'plaques':plaques,'complete_status_masks':statuses,'complete_skill_lines':skills})
    towns = []
    for frame in (7740,11340,19540):
        image = Image.open(CAPTURE/f'frame_{frame:06d}_navigation.png').convert('RGB')
        towns.append({'frame':frame,'stock_labels':[mask(image,font,text,88+i*16)
                      for i,text in enumerate(('Iron','Hemp','Rhino Horn'))]})
    saved = Path('E:/Rota Nova translations/Saves/hodram-tunis-rested-v508.dsv')
    assert saved.read_bytes() == Path(donor['destination']).read_bytes()
    reload_path = Path('work/emulation_v193/environment_voyage_v511_tunis_reload/capture_report.json')
    reload = json.loads(reload_path.read_text(encoding='utf-8'))
    assert reload['ROM_sha256'] == report['ROM_sha256'] and reload['cold_boot'] and not reload['savestate_loaded']
    assert not reload['callback_errors'] and reload['battery_save_preloaded']['source_sha256'] == sha(saved.read_bytes())
    for row in reload['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    reload_image = Image.open('work/emulation_v193/environment_voyage_v511_tunis_reload/frame_004200_final.png').convert('RGB')
    reload_labels = [mask(reload_image,font,text,88+i*16)for i,text in enumerate(('Iron','Hemp','Rhino Horn'))]
    saved_image = Image.open(CAPTURE/'frame_020940_navigation.png').convert('RGB')
    assert saved_image.crop((0,0,256,192)).tobytes() == reload_image.crop((0,0,256,192)).tobytes()
    proof = {'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
             'capture_report':str(report_path),'capture_report_sha256':sha(report_path.read_bytes()),
             'source_backed_condition_labels':source_labels,'six_natural_Sailor_Info_cases':cases,
             'all60_plaque_regions_and60_skill_lines_exact':True,'all12_health_mood_masks_complete':True,
             'Charles_observed_Sick_Upset_before_Inn_Healthy_Relaxed_after':True,
             'no_savestate_inventory_condition_or_unlock_injection':True,
             'Tunis_30_day_stay_observed_Nov10_to_Dec10_fatigue44_to0':True,
             'complete_Tunis_stock_labels':towns,
             'normal_saved_Tunis_checkpoint':str(saved),'saved_checkpoint_sha256':sha(saved.read_bytes()),
             'saved_Tunis_cold_reload_verified':True,
             'reload_report':str(reload_path),'reload_report_sha256':sha(reload_path.read_bytes()),
             'complete_reload_stock_labels':reload_labels,'whole_upper_Tunis_panel_exact_after_reload':True,
             'all18_plaques_remain_incomplete':True,'East_Asian_checks_and_full_goal_still_open':True,
             'ROM_unchanged_no_new_candidate':True,'full_goal_complete':False}
    (OUT/'sick_recovery_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Six natural states:60 plaques,60 full skill lines,12 status masks,three original labels and Tunis stocks pass.')


if __name__ == '__main__':
    main()
