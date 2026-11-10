"""Preserve failed reuse preflight; read the actual path/hash review-sheet object."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_name_reuse_repair_v7386b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B229_name_planes_v7386').exists()
    r=derive('scripts/reuse_lil_B229_name_planes_v7386.py','scripts/reuse_lil_B229_name_planes_v7386b.py',{"Path(old['review_sheet'])":"Path(old['review_sheet']['path'])","old['review_sheet_sha256']":"old['review_sheet']['sha256']"});ROOT.mkdir(parents=True);save(ROOT/'source_locked_review_sheet_schema.json',dict(tool=r,failed_preflight_preserved_before_output_orROM_mutation=True,actual_review_sheet_path_hash_object_bound=True,no_repeat_font_execution=True,new_credit=0,full_goal_complete=False))
