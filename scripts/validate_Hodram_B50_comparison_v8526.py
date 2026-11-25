"""Recompute all B49 saved comparison state/RGB fields without emulator replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B50_comparison_v1 import check_comparisons
from scripts.validate_Hodram_B50_native_v8520 import require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_independent_compare_v8526')
PROOFS={
 'comparison':'work/analysis/Hodram_B50_comparison_v8509/paired_selected_path_comparison.json',
 'actual':'work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B50_editorial_manuscript_v5.json')
    data={k:read(p) for k,p in PROOFS.items()};parent=NdsImage.open(doc['current_ROM'])
    result=check_comparisons(data,parent,read,require);ROOT.mkdir(parents=True)
    save(ROOT/'independent_comparison.json',dict(result=result,no_capture_producer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B50_comparison_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B50 comparison:89laterRGBpairs,all fourRGB differences,two speech-duration differences,allPRNG/native-state/raw-calendar/item/layout0/hide scope recomputed;no emulator replay orcredit.')
