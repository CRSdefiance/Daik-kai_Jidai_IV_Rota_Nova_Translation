"""Bind the measured donor captain1 rather than inheriting Lil opening captain2."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/recommendation_audit_tools_v4985b');assert not root.exists()
    tool=derive('scripts/verify_recommendation_actual_v4985.py','scripts/verify_recommendation_actual_v4985b.py',{
        'assert captain==2':'assert captain==1',
        'whole_actor_and_captain2_equal':'whole_actor_and_actual_captain_equal',
        "PRNG_seeds=[v['seed'] for v in final],PRNG_equal=":"actual_donor_captain_IDs=[v['captain'] for v in final],PRNG_seeds=[v['seed'] for v in final],PRNG_equal=",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,measured_original_donor_captain_IDs=[1,1],both_source_sequences_and_timings_exact=True,
        prior_hardcoded_Lil_captain_assumption_stopped_and_preserved=True,no_repeat_emulator_run=True))
