"""Derive B157's eight source-relative sites with unchanged full-memory guards."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    row=derive('scripts/prove_lil_B156_branches_v3701.py','scripts/prove_lil_B157_branches_v3747.py',{'lil_B156_branches_v3701':'lil_B157_branches_v3747','lil_B156_source_v3700/all76_clean_current_complete_context.json':'lil_B157_source_v3746/all75_clean_current_complete_context.json','B156-all12-relative-sites':'B157-all8-relative-sites','Run all12 original':'Run all8 original'});root=Path('work/analysis/lil_B157_branch_tools_v3747');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(tool=row,expected_source_current_cases=80,expected_target_cases_when_relocated=40,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
