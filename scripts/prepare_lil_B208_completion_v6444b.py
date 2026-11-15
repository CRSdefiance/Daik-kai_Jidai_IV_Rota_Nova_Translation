"""Correct inherited documentary paths before executing the completion producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_completion_tools_v6444b')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/complete_lil_B208_v6444.py','scripts/complete_lil_B208_v6444b.py',{
        'lil_B208_regressions_v6380':'lil_B208_regressions_v6439',
        'all13-source-native-reference':'all24-source-native-reference',
        'Lil_B208_completed_v6385':'Lil_B208_completed_v6444',
        'complete_native_text_nameplate_holds=51':'complete_native_text_nameplate_holds=95',
        "paths=[DOC,RELEASE":"paths=[Path('scripts/lil_B208_completion_gates_v6444.py'),Path('work/analysis/lil_B209_clean_inventory_v6446/all_clean_B209_speeches_before_predecessor_comparison.json'),DOC,RELEASE",
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',receipt)
