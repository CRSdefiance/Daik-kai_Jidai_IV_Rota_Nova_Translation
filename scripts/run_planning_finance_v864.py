"""Fresh-copy cold boots with recorded Planning19/Finance20 navigation;no savestates."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_planning_finance_adapter_v864 as adapter
from scripts.native_planning_finance_fixture_v864 import CASES
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/planning_finance_v864')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM=Path('out/all_routes_combined_v863_candidate.nds')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=tuple(CASES),required=True);args=parser.parse_args()
    ROOT.mkdir(parents=True,exist_ok=True)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    folder=CAP/f'planning_finance_v864_863_{args.case}'
    provenance=read('work/analysis/refit_editorial_v831/donor_copy.json');source=Path(provenance['disposable_source'])
    donor=ROOT/f'disposable_{args.case}.dsv';assert not donor.exists() and not folder.exists()
    digest=sha(source.read_bytes());assert digest==provenance['disposable_source_sha256']
    copy2(source,donor);assert sha(donor.read_bytes())==digest
    inputs=Path('work/analysis/ceremony_heroes_v825/load_save_inputs.json')
    navigation=ROOT/f'{args.case}_navigation.jsonl';assert navigation.exists()
    save(ROOT/f'{args.case}_run_plan.json',{'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),'folder':str(folder),
        'source_donor':str(source),'source_donor_sha256':digest,'disposable_source':str(donor),
        'existing_isolated_five_ship_Copenhagen_save_no_earned_fleet_or_progression_claim':True,
        'existing_donor_provenance':provenance,'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),
        'recorded_navigation':str(navigation),'recorded_navigation_sha256':sha(navigation.read_bytes()),
        'frames_budget':30000,'initial_pause':3200,'no_savestate_or_text_selector_code_RNG_substitutions':True,
        'only_declared_Planning19/Finance20_room_type_and_occupant_fixture_enabled':True})
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(folder),'--battery-save',str(donor),
        '--inputs-json',str(inputs),'--touchscreen','--frames','30000','--capture-every','999999',
        '--capture-at','1','60','180','3200','--dump-capture-ram','--dump-pause-ram','--dump-ram','--pause-at','3200','--allow-planning-finance-fixtures']
    adapter.main()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==digest


if __name__=='__main__':main()
