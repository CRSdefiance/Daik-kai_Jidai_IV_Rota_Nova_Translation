"""Paired actual title menu capture after START, before selecting New Game."""

import argparse
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.finish_refit_display_v712 import load
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/planning_finance_v864')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',choices=('855','863'));parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    if args.verify:
        reports={}
        for version in ('855','863'):
            rom=Path(f'out/all_routes_combined_v{version}_candidate.nds')
            report,images,receipt=load(CAP/f'planning_finance_v864_title_{version}',sha(rom.read_bytes()),1150)
            assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and 'battery_save_preloaded' not in report
            reports[version]=(images,receipt)
        assert reports['855'][0][1100].tobytes()==reports['863'][0][1100].tobytes()
        save(ROOT/'paired_actual_title_menu.json',{'whole256x384_title_menu_at1100_exact_to_V855':True,
            'receipts':{v:r[1] for v,r in reports.items()},'visual_review_pending':True,'no_savestate_save_or_fixtures':True,
            'producer_sha256':sha(Path(__file__).read_bytes())})
        print('Whole title-menu frame after START matches V855;visual review pending.');return
    assert args.run
    rom=Path(f'out/all_routes_combined_v{args.run}_candidate.nds');folder=CAP/f'planning_finance_v864_title_{args.run}'
    assert not folder.exists()
    assert sha(rom.read_bytes())==read(rom.with_suffix('.manifest.json'))['candidate_sha256']
    inputs=Path('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
    save(ROOT/f'title_{args.run}_run_plan.json',{'ROM':str(rom),'sha256':sha(rom.read_bytes()),'folder':str(folder),
        'frames':1150,'capture_at':[1100],'input':str(inputs),'input_sha256':sha(inputs.read_bytes()),'no_save_or_fixtures':True})
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(folder),'--frames','1150',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','1100']
    harness.main()


if __name__=='__main__':main()
