"""Source-pinned title capture after START with retained V928 comparison."""
import argparse,sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.finish_refit_display_v712 import load
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_survey_lookout_v939')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',choices=('938',));parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    if args.verify:
        reports={}
        for version,folder in [('928',CAP/'battle_bridge_v929_title_928'),('938',CAP/'battle_survey_lookout_v939_title_938')]:
            rom=Path(f'out/all_routes_combined_v{version}_candidate.nds');report,images,receipt=load(folder,sha(rom.read_bytes()),1150)
            assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and 'battery_save_preloaded' not in report
            reports[version]=(images,receipt)
        assert reports['928'][0][1100].tobytes()==reports['938'][0][1100].tobytes()
        save(ROOT/'paired_actual_title_menu.json',{'whole256x384_title_menu_at1100_exact_to_V928':True,'receipts':{v:r[1] for v,r in reports.items()},'visual_review_pending':True,'no_savestate_save_or_fixtures':True,'baseline_reuses_prior_hash_checked_V928_cold_boot_title_capture':True,'producer_sha256':sha(Path(__file__).read_bytes())})
        print('Whole title-menu frame after START matches V928;visual review pending.');return
    assert args.run=='938'
    rom=Path('out/all_routes_combined_v938_candidate.nds');folder=CAP/'battle_survey_lookout_v939_title_938';assert not folder.exists()
    assert sha(rom.read_bytes())==read(rom.with_suffix('.manifest.json'))['candidate_sha256']
    inputs=Path('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
    save(ROOT/'title_938_run_plan.json',{'ROM':str(rom),'sha256':sha(rom.read_bytes()),'folder':str(folder),'frames':1150,'capture_at':[1100],'input':str(inputs),'input_sha256':sha(inputs.read_bytes()),'no_save_or_fixtures':True})
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(folder),'--frames','1150','--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','1100']
    harness.main()
if __name__=='__main__':main()
