"""Unmodified V893,no-save RIGHT selection using the retained Joakim schedule."""

import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_name_v896')
ROM=Path('out/all_routes_combined_v893_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_name_v896_fresh_Joakim')


def main():
    assert not CAP.exists();ROOT.mkdir(parents=True,exist_ok=True)
    source=Path('work/analysis/reviewed_name_release_v299/hodram_inputs.json')
    events=[r for r in read(source) if r['start']<=4000]
    assert events[2]=={'start':1450,'duration':12,'buttons':['RIGHT']}
    inputs=ROOT/'fresh_Joakim_inputs.json';save(inputs,events)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    save(ROOT/'fresh_control_run_plan.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'folder':str(CAP),
        'source_inputs':str(source),'source_inputs_sha256':sha(source.read_bytes()),'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),
        'only_original_controller_events_through4000':True,'no_battery_save_savestate_ROM_RAM_or_unlock_fixture':True,
        'runner_sha256':sha(Path(__file__).read_bytes())})
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','4000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','1600','2400','3200','4000',
        '--dump-capture-ram','--dump-ram']
    harness.main()


if __name__=='__main__':main()
