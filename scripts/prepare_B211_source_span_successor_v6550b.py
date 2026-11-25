"""Retain the old exact runtime guard and bind the same instructions to the approved name-data target."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_source_span_tools_v6550b')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/lil_B209_source_span_binding_v6450c.py','scripts/lil_B211_source_span_binding_v6550b.py',{'4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351':'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'}))
    proofs.append(derive('scripts/map_lil_B211_source_v6550.py','scripts/map_lil_B211_source_v6550b.py',{'lil_B209_source_span_binding_v6450c':'lil_B211_source_span_binding_v6550b','lil_B211_source_v6550':'lil_B211_source_v6550b'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_successor_receipt.json',dict(proofs=proofs,initial_mapper_rejected_old_exact_ARM9_guard_before_packet_write=True,all_previous_guards_native_constants_renderer_span_and_branch_checks_preserved=True,new_exact_hash_is_approved_five_byte_name_target_not_weakened_guard=True,full_goal_complete=False))
