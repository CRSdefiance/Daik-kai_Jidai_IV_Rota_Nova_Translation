"""Preserve the failed draft producer; repair a Python variable-shadowing error only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_draft_repair_v7873b');assert not root.exists()
    result=derive('scripts/draft_Rafael_B45_v7873.py','scripts/draft_Rafael_B45_v7873b.py',{
        'work/analysis/Rafael_B45_prose_v7873':'work/analysis/Rafael_B45_prose_v7873b',
        "source_speech_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows if r['source_selector']==r['actor_ID']]":
        "source_speech_keys=[dict(file_path=speech['file_path'],id=speech['id']) for speech in rows if speech['source_selector']==r['actor_ID']]",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        preserved_failed_producer='scripts/draft_Rafael_B45_v7873.py',
        failure="KeyError: actor_ID in scoped-name list comprehension before manuscript or name outputs",
        only_loop_variable_shadowing_repaired=True,no_prose_source_orchecks_changed=True,
        no_failed_ROM_ornegative_control_claim=True,new_credit=0,full_goal_complete=False))
