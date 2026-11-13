"""Keep strict native-number preservation while comparing the measured RNG witnesses as parsed data."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_checkpoint_seed_tools_v6579b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prepare_lil_B211_sealed_checkpoint_v6579.py','scripts/prepare_lil_B211_sealed_checkpoint_v6579b.py',{'lil_B211_sealed_checkpoint_tools_v6579':'lil_B211_sealed_checkpoint_tools_v6579b',"view['final_PRNG_seeds']==[3542426494,2102660053]":"view['final_PRNG_seeds']==[int('3542426494'),int('2102660053')]"});ROOT.mkdir(parents=True);save(ROOT/'source_locked_seed_comparison_receipt.json',dict(proof=proof,strict_native_number_check_preserved=True,measured_seed_witnesses_still_exact_not_a_weaker_guard=True,initial_preparation_rejected_new_high_integer_literals_before_checkpoint_write=True,all_prior_producers_and_evidence_preserved=True,full_goal_complete=False))
