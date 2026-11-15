"""Prepare immutable B50 production pins and one-commit whole-reference positive test."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_production_prepare_v8168')
if __name__=='__main__':
    assert not ROOT.exists()
    config=derive('scripts/pin_Rafael_B49_production_v8118.py','scripts/pin_Rafael_B50_production_v8168.py',{
        'scripts.Rafael_B49_release_paths_v8114':'scripts.Rafael_B50_release_paths_v8164',
        'Rafael_B49_production_tools_v8118':'Rafael_B50_production_tools_v8168',
        'scripts/Rafael_B49_release_paths_v8114.py':'scripts/Rafael_B50_release_paths_v8164.py',
        'scripts/seal_Rafael_B49_references_v8114.py':'scripts/seal_Rafael_B50_references_v8164.py',
        "Path('dk4tool/patch/rafael_B49_editorial_v1.py')":"Path('dk4tool/patch/rafael_B50_editorial_v1.py'),Path('dk4tool/patch/rafael_B50_risk_v1.py'),Path('scripts/focus_Rafael_B50_picture_risk_v8160.py')",
        'Rafael61':'Rafael28','V8066':'V8122','61 speech':'28 speech','B49':'B50',
    })
    positive=derive('scripts/validate_Rafael_B49_atomic_positive_v8119.py','scripts/validate_Rafael_B50_atomic_positive_v8169.py',{
        'scripts.Rafael_B49_release_paths_v8114':'scripts.Rafael_B50_release_paths_v8164',
        'Rafael_B49_atomic_positive_v8119':'Rafael_B50_atomic_positive_v8169',
        "len(proof['changed_records'])==61":"len(proof['changed_records'])==28",
        'positive_records=61':'positive_records=28',
        'all154_commands56_relatives_13predicates_onequery_source00_02_09_twoFI_sevenA000_C281_full_end_inverse_exact':'all37_commands_zero_relative_predicate_query_sites_source00_02_09_FA2_FI1_4821_A000_4720_4681_full_end_inverse_exact',
        'all61_single_pages_three_narrow_warnings22_infos_eleven_native_only_speeches_preserved':'all28_single_pages_two_narrow_warnings18_infos_all28_actual_speeches_preserved',
        '61-record atomic positive':'28-record atomic positive','B49':'B50',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[config,positive])
    print('Prepared B50 production pinning and28-record whole-reference atomic positive.')
