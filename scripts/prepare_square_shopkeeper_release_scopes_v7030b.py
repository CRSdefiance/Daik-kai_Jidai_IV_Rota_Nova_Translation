"""Clarify that new label proofs bind the final target; inherited compilers bind their own stages."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/square_shopkeeper_release_scope_tools_v7030b')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/verify_square_shopkeeper_release_v7030.py','scripts/verify_square_shopkeeper_release_v7030b.py',{
        'all_native_payload_proofs_bound_by_exact_target_hash':'new_label_native_payload_proofs_bound_by_exact_target_hash',
        "arm=after.read_file('/__arm9__.bin');assert":"assert len(stage['data_plan']['changed_byte_offsets'])==18 and stage['data_plan']['all_unread_old_tail_bytes_preserved']\n    arm=after.read_file('/__arm9__.bin');assert"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_verification_scope.json',dict(tool=row,
        current_label_proofs_use_exact_final2b6_hash=True,all_inherited_strict_compilers_replay_their_original_order_and_hashes=True,
        no_guard_or_native_address_weakened=True,exact18_data_bytes_and_unread_tail_requirement_added=True,full_goal_complete=False))
