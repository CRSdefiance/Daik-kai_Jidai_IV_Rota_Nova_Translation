"""Verify current Hangzhou display in the authorized Maria selection fixture."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_fleet_release_v375 import files
from scripts.verify_movie_gpu_fixtures_v336 import quantized


def main():
    out=Path('work/analysis/maria_asia_v515')
    folder=Path('work/emulation_v193/maria_asia_v515')
    manifest=json.loads((out/'selection_fixture_manifest.json').read_text(encoding='utf-8'))
    report_path=folder/'capture_report.json'
    report=json.loads(report_path.read_text(encoding='utf-8'))
    assert report['ROM_sha256']==manifest['research_ROM_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('synthetic_inventory_fixtures')
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    production=NdsImage.open(manifest['production_ROM'])
    research=NdsImage.open(manifest['research_ROM'])
    a,b=files(production),files(research)
    assert [p for p in a if a[p]!=b[p]]==['/__arm9__.bin']
    assert [i for i,(x,y) in enumerate(zip(a['/__arm9__.bin'],b['/__arm9__.bin'])) if x!=y]==[0x9F068]
    image=Image.open(folder/'frame_018400_navigation.png').convert('RGB')
    font=GameAsciiFont.from_arm9(a['/__arm9__.bin'])
    labels=[mask(image,font,text,88+i*16) for i,text in enumerate(('China','Silk Cloth','Jade'))]
    background=PxlImage.from_bytes(a['/towngrp/towngrp33.pxl']).render()
    # The Inn nameplate/frame occludes source columns84-85 at rows80-95.
    source_box=(86,0,256,96)
    assert quantized(background.crop(source_box)).tobytes()==quantized(image.crop((86,192,256,288))).tobytes()
    latest=NdsImage.open('out/all_routes_combined_v514_candidate.nds')
    paths=['/towngrp/towngrp33.pxl','/towngrp/towngrp32.pxl']
    assert all(production.read_file(p)==latest.read_file(p)for p in paths)
    proof={'format':'dk4-maria-hangzhou-v515','production_candidate':manifest['production_ROM'],
           'production_candidate_sha256':manifest['production_ROM_sha256'],
           'selection_fixture_manifest':str(out/'selection_fixture_manifest.json'),
           'capture_report':str(report_path),'capture_report_sha256':sha(report_path.read_bytes()),
           'only_selection_limit_instruction_changed':True,'all_other_files_and_progress_flags_untouched':True,
           'user_authorized_Maria_selection_bypass_not_earned_unlock':True,
           'normal_New_Game_and_town_facility_navigation_inside_fixture':True,
           'actual_current_stock_labels':labels,'source_background33_box':list(source_box),
           'exact_visible_retained_background_pixels':170*96,
           'Inn_nameplate_occlusion_columns84_85_excluded':True,
           'unchanged_backgrounds32_33_also_present_in_V514':True,
           'manual_sailing_attempt_not_a_Seoul_or_Nagasaki_docking':True,
           'manual_attempt_ended_at_Kurushima_warning_low_supplies':True,
           'Auto_Move_research_run_pending':True,'other_Asian_visits_still_open':True,
           'all18_plaques_incomplete':True,'full_goal_complete':False}
    (out/'hangzhou_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Hangzhou: three complete current labels and16320 retained background pixels match.')


if __name__=='__main__':main()
