"""Correct inherited episode labels before staging any ledger change."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_completion_tools_v6165b')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/complete_lil_B204_v6165.py','scripts/complete_lil_B204_v6165b.py',{'all22_exact_clean_predecessor_runtime_logical_and_integrated_references_bound':'all20_exact_clean_predecessor_runtime_logical_and_integrated_references_bound','all22-source-native-reference-actual-registered-release-pass':'all20-source-native-reference-actual-registered-release-pass','natural_event203_not_selected':'natural_event204_not_selected','actual_selected_source203_events':'actual_selected_source204_events','actual_source_event203_selected':'actual_source_event204_selected','B204 and full broader editorial/name-review scope remain active.':'B205 and full broader editorial/name-review scope remain active.'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_metadata_successor.json',dict(tool=tool,inherited_episode_labels_caught_before_staging_or_any_ledger_mutation=True,all_source_words_native_addresses_counts_and_inverse_checks_unchanged=True,full_goal_complete=False));print('Correct20-object/event204 completion metadata prepared before staging;original producer preserved.')
