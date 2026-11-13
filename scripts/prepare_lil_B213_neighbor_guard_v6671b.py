"""Correct the inherited neighbor exclusion to the actual B213 target; preserve the rejected output."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B213_neighbor_guard_tools_v6671b')
if __name__=='__main__':
    assert not ROOT.exists();old=Path('work/analysis/lil_B213_relocation_v6671/SC2_block213_RESEARCH_ONLY.bin');assert old.is_file();proof=derive('scripts/research_lil_B213_relocation_v6671.py','scripts/research_lil_B213_relocation_v6671b.py',{'relocation_v6671':'relocation_v6671b','if n!=212':'if n!=213'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_actual_block_neighbor_guard.json',dict(proof=proof,rejected_first_target_block=str(old),rejected_first_target_block_sha256=sha(old.read_bytes()),first_failure_was_wrong_neighbor_ID_not_inverse_or_target_bytes=True,no_archive_ROM_registry_ledger_or_credit_mutation=True,full_goal_complete=False))
