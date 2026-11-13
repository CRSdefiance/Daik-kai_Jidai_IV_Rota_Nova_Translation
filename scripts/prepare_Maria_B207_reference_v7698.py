"""Prepare a single-block reversible research reference from the full registered current."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_reference_tools_v7698')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/create_papal_trade_reference_v7642.py','scripts/create_Maria_B207_reference_v7698.py',{
        'Pin an exact reversible two-file research reference; no playable handoff or promotion.':'Pin an exact reversible Maria single-block research reference; no playable handoff or promotion.',
        'papal_trade_reference_v7642':'maria_B207_reference_v7698',
        'papal_trade_relocation_v7640/two_archives36_speeches40_commands_exact_predecessor_inverse_RESEARCH':'maria_B207_relocation_v7696/Maria18_speeches20_commands_exact_clean_andpredecessor_inverse_RESEARCH',
        'papal_trade_stored_v7641/all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages':'maria_B207_stored_v7697/Maria18_stored_targets72_alignments7_zero_ink_tails18_complete_pages',
        'all_routes_combined_v7611_candidate':'all_routes_combined_v7660_candidate',
        'all-routes-unified-v7611':'all-routes-unified-v7660',
        "len(manifest['batches'])==626":"len(manifest['batches'])==628",
        "stored['all36_final_stored_targets_equal_reviewed_complete_ink']":"stored['all18_final_stored_targets_equal_reviewed_complete_ink']",
        "['/data/SC0.DK4','/data/SC1.DK4']":"['/data/SC3.DK4']",
        'SC0B246/SC1B237 full36-speech papal-trade contextual review, exact reversible archives andstored native proofs. Only those two blocks change from complete V7611.':'Maria SC3B207 full18-speech contextual review,distinct CS0101 header,exact clean/predecessor inverse andstored native proofs. Only this block changes from complete V7660.',
        'Pinned reversible two-block research reference from complete V7611;342 SC0 and324 SC1 other blocks/all other files andcomponents exact. Current/main unchanged;no handoff package.':'Pinned reversible Maria B207 research reference from complete V7660;302 other SC3 blocks/allother files andcomponents exact. Current/main unchanged;no handoff package.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_single_Maria_reference.json',dict(derivation=result,no_high_native_constant_changes=True,new_credit=0,full_goal_complete=False))
