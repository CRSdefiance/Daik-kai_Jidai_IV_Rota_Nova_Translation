"""Preserve the failed fixture producer; bind the actual candidate_sha256 startup-plan field."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_fixture_schema_v7892b');assert not root.exists()
    result=derive('scripts/create_Rafael_B45_fixtures_v7892.py','scripts/create_Rafael_B45_fixtures_v7892b.py',{
        "start['ROM_sha256']":"start['candidate_sha256']",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        failure="KeyError ROM_sha256 before any fixture directory,ROM orpin mutation",
        original_current_ROM_hash_equality_guard_preserved_using_real_schema=True,
        no_failed_ROM_ornegative_release_control_claim=True,new_credit=0,full_goal_complete=False))
