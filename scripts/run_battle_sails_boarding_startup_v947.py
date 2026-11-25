"""Ordinary no-save cold-boot/New Game control;earlier harness stays exact."""



import sys

from pathlib import Path



from dk4tool.patch.grand_race_menu_release import sha

from scripts import headless_desmume_v193 as harness

from scripts.verify_village_wrap_v608 import read,save



ROOT=Path('work/analysis/battle_sails_boarding_v947')

ROM=Path('out/all_routes_combined_v947_candidate.nds')

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_sails_boarding_v947_newgame')





def main():

    assert not CAP.exists()

    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']

    inputs=Path('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')

    frames=[1,60,180,1600,2000,3200,4000]

    save(ROOT/'newgame_run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),

        'folder':str(CAP),'frames_budget':4000,'capture_at':frames,'inputs':str(inputs),

        'input_sha256':sha(inputs.read_bytes()),'no_battery_save_savestate_or_fixtures':True})

    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','4000',

        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at',*map(str,frames),

        '--dump-capture-ram','--dump-ram']

    harness.main()





if __name__=='__main__':main()

