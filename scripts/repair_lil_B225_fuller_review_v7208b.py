"""Preserve the failed preflight and correct only its metadata quotation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_fuller_review_repair_v7208b')
if __name__=='__main__':
    assert not ROOT.exists();target='scripts/prepare_lil_B225_fuller_review_v7208b.py';assert not Path(target).exists()
    row=derive('scripts/prepare_lil_B225_fuller_review_v7208.py',target,{r"only this record\'s first-row balancing preference changes":"only the first-row balancing preference for this record changes",'fuller_review_tools_v7208':'fuller_review_tools_v7208b'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_quotation_correction.json',dict(tool=row,failed_preflight_preserved_no_target_review_files_or_ROM_mutated=True,only_metadata_quotation_and_proof_root_changed=True,all_prose_source_native_andactual_evidence_unchanged=True,new_credit=0))
