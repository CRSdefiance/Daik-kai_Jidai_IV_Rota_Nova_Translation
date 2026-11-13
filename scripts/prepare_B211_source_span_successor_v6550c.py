"""Update both exact runtime identity bindings while retaining every instruction check."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_source_span_tools_v6550c')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/lil_B211_source_span_binding_v6550b.py','scripts/lil_B211_source_span_binding_v6550c.py',{'out/all_routes_combined_v6380_candidate.nds':'out/all_routes_combined_v6541_candidate.nds'}))
    proofs.append(derive('scripts/map_lil_B211_source_v6550b.py','scripts/map_lil_B211_source_v6550c.py',{'lil_B211_source_span_binding_v6550b':'lil_B211_source_span_binding_v6550c','lil_B211_source_v6550b':'lil_B211_source_v6550c'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_successor_receipt.json',dict(proofs=proofs,initial_guards_and_failed_producers_preserved=True,exact_approved_target_hash_and_exact_registered_ROM_both_bound=True,all_native_constants_source_spans_and_complete_branch_words_preserved=True,no_mask_or_weaker_hash_guard=True,full_goal_complete=False))
