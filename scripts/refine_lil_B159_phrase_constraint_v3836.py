"""Preserve the failed plan and remove only a new redundant overlapping put/up constraint."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B159_phrase_constraint_v3836');assert not root.exists();failed=Path('work/analysis/lil_B159_layout_v3834/all41_paragraph_layout_QA.json');proof=read(failed);assert [r['id'] for r in proof['failures']]==['DK4_MES_B159_R0112'];pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B159_layout_v1.py','dk4tool/dialogue/lil_B159_layout_v2.py',{"('put','up'),":''}))
    pairs.append(derive('scripts/plan_lil_B159_layout_v3834.py','scripts/plan_lil_B159_layout_v3837.py',{'lil_B159_layout_v1':'lil_B159_layout_v2','lil_B159_layout_v3834':'lil_B159_layout_v3837'}))
    pairs.append(derive('scripts/verify_lil_B159_fonts_v3835.py','scripts/verify_lil_B159_fonts_v3838.py',{'lil_B159_layout_v1':'lil_B159_layout_v2','lil_B159_fonts_v3835':'lil_B159_fonts_v3838'}))
    root.mkdir(parents=True);save(root/'failed_plan_and_redundant_phrase_constraint_resolution.json',dict(failed_plan=str(failed),failed_plan_sha256=sha(failed.read_bytes()),finding='R112 retains natural source-faithful wording but the added put/up pair conflicts with the existing up/with protection during native pair-phase wrapping.',resolution='Remove only the newly added nonterm put/up constraint. Retain the existing up/with protection and all glyph, row, bounds, weak-ending, orphan, macro and control guards. Replan without any wording change or waiver.',tools=pairs,source_prose_and_all_retention_decisions_unchanged=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
