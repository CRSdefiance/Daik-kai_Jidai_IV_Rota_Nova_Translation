"""Prepare clean-only Rafael catalogue review;block order is not narrative chronology."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_next_clean_tools_v7864');assert not root.exists()
    result=derive('scripts/inventory_Maria_next_clean_v7786.py','scripts/inventory_Rafael_next_clean_v7864.py',{
        'Inventory complete clean B34/B35 andoriginal EV3 context before exposing current English.':
        'Inventory complete clean Rafael B45 andoriginal EV0 context;numeric adjacency proves no chronology.',
        'work/analysis/maria_next_clean_v7786':'work/analysis/Rafael_next_clean_v7864',
        'editorial_handoff_verification_v7785b':'editorial_handoff_verification_v7863',
        '==6922':'==6938',
        '/data/SC3.DK4':'/data/SC0.DK4',
        '/data/EV3.DK4':'/data/EV0.DK4',
        'for number in [36]':'for number in [45]',
        'complete_clean_SC3_B36_EV3_andcoverage_before_current_English':'complete_clean_SC0_B45_EV0_andcoverage_before_current_English',
        'EV3_sha256':'EV0_sha256',
        "if g['block']==36":"if g['block']==45",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        all_original_native_high_constants_six_byte_preambles_andcomplete_exchange_walk_guards_preserved=True,
        selected_source_event45_action46_not_claimed_as_chronological_followup_to44=True,
        clean_source_only_no_current_English_ornew_credit=True,full_goal_complete=False))
