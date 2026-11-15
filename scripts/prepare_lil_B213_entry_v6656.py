"""Bind the new source EV2 action without inheriting B212 dependencies or eligibility."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_entry_tools_v6656')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B212_entry_v6602.py','scripts/prove_lil_B213_entry_v6656.py',{'B212':'B213','entry_v6602':'entry_v6656','source_v6594b':'source_v6651','all14_clean_current_complete_exchange_with_two_three_choices':'eighteen_clean_current_full_prophecy_exchange_source_references','current_V6584_native_v6593':'current_V6641_native_v6650',"in [212]":"in [213]"});ROOT.mkdir(parents=True);save(ROOT/'source_locked_entry_getters.json',proof)
