"""Recompute all B49 saved comparison state/RGB fields without emulator replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_comparison_v1 import check_comparisons
from scripts.validate_Hodram_B49_native_v8433 import require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_compare_v8439')
PROOFS={
 'comparison':'work/analysis/Hodram_B49_comparison_v8410/paired_selected_path_comparison.json',
 'tail_comparison':'work/analysis/Hodram_B49_tail_comparison_v8421/both_bounded_tail_comparisons.json',
 'actual':'work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json')
    data={k:read(p) for k,p in PROOFS.items()};parent=NdsImage.open(doc['current_ROM'])
    result=check_comparisons(data,parent,read,require);ROOT.mkdir(parents=True)
    save(ROOT/'independent_comparison.json',dict(result=result,no_capture_producer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_comparison_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 comparison:231laterRGBpairs,all fiveRGB differences,all timings/PRNG/native-state/raw-calendar/item/hide-wait scope recomputed;no emulator replay orcredit.')
