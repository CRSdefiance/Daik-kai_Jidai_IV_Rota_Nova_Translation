"""Prepare complete B49 predecessor pin and one-commit exact-reference positive test."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_production_preparation_v8118')
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/pin_Rafael_B48_production_v8062.py','scripts/pin_Rafael_B49_production_v8118.py',{
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'seal_Rafael_B48_references_v8060':'seal_Rafael_B49_references_v8114',
        'Rafael_B48_production_tools_v8062':'Rafael_B49_production_tools_v8118',
        'B48':'B49','V8013':'V8066','Rafael91':'Rafael61','91 speech manifest':'61 speech manifest',
    })
    b=derive('scripts/validate_Rafael_B48_atomic_positive_v8063.py','scripts/validate_Rafael_B49_atomic_positive_v8119.py',{
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'Rafael_B48_atomic_positive_v8063':'Rafael_B49_atomic_positive_v8119',
        'B48':'B49',"len(proof['changed_records'])==91":"len(proof['changed_records'])==61",'positive_records=91':'positive_records=61',
        'all163_commands28_relatives_five_predicates_two_queries_source00_4B71_oneFI_fourFE_full_end_inverse_exact':'all154_commands56_relatives_13predicates_onequery_source00_02_09_twoFI_sevenA000_C281_full_end_inverse_exact',
        'R347_two_pages_two_narrow_warning_exceptions_thirteen_native_only_speeches_preserved':'all61_single_pages_three_narrow_warnings22_infos_eleven_native_only_speeches_preserved',
        '91-record atomic positive':'61-record atomic positive',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b])
    print('Prepared B49 pin and atomic positive tools; no ROM/registry/credit mutation.')
