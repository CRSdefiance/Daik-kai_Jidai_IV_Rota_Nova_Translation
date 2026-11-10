"""Keep the stored FI template distinct from its proven original runtime name expansion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_consumer_tools_v6551b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B211_current_consumers_v6551.py','scripts/prove_lil_B211_current_consumers_v6551b.py',{
        'lil_B211_current_consumers_v6551':'lil_B211_current_consumers_v6551b',
        "assert body==value[1:] and result['registered_catalog_match'] is None;text=body.decode('cp932')":"expected,match=namespace['expanded_current_body'](value[1:]);assert body==expected and result['registered_catalog_match']==match is None;text=body.decode('cp932')",
        'current_effective_runtime_template_hex=body.hex()':'current_effective_runtime_template_hex=value[1:].hex(),current_expanded_runtime_hex=body.hex()',
        "effective_predecessor_paragraph=' '.join(text.split())":"effective_predecessor_paragraph=' '.join(value[1:].decode('cp932').split()),expanded_predecessor_paragraph=' '.join(text.split())",
        'all12_effective_bodies_equal_raw_storage_without_catalogue_override=True':'all12_templates_equal_raw_storage_without_catalogue_override=True,original_FI_expands_to_Lil_at_source_owned_native_macro_path=True',
        'FI expansion,source/native display,name decisions,controls andrelease remain pending':'FI native expansion bound;complete source/native display,name decisions,controls andrelease remain pending'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_successor_receipt.json',dict(proof=proof,initial_no_macro_body_equality_assertion_rejected_FI_before_final_proof=True,original_macro_behavior_and_all_memory_guards_preserved=True,stored_template_expanded_body_and_actual_UI_coverage_distinguished=True,full_goal_complete=False))
