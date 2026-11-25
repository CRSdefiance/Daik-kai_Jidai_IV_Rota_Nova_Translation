"""Preserve the rejected preparer; remove one absent derivation key before any target was generated."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_relocation_key_fix_v6716b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/research_lil_B214_relocation_v6716.py').exists()
    proof=derive('scripts/prepare_lil_B214_relocation_v6716.py','scripts/prepare_lil_B214_relocation_v6716b.py',{"'blocks[209]':'blocks[214]',":''})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_absent_key_correction.json',dict(derivation=proof,first_attempt_stopped_before_target_generation_or_shared_mutation=True,no_source_prose_native_address_or_ROM_change=True,full_goal_complete=False))
