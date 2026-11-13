"""Preserve the failed phrase plan and keep the offer's possessive phrase intact."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B156_hire_flow_v3711');assert not root.exists()
    pairs=[derive('dk4tool/dialogue/lil_B156_layout_v2.py','dk4tool/dialogue/lil_B156_layout_v3.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('your','skills')})\n\ndef _word(value):"})]
    pairs.append(derive('scripts/plan_lil_B156_layout_v3709.py','scripts/plan_lil_B156_layout_v3712.py',{'lil_B156_layout_v2':'lil_B156_layout_v3','lil_B156_layout_v3709':'lil_B156_layout_v3712','lil_B156_editorial_manuscript_v3':'lil_B156_editorial_manuscript_v4'}))
    pairs.append(derive('scripts/verify_lil_B156_fonts_v3710.py','scripts/verify_lil_B156_fonts_v3713.py',{'lil_B156_fonts_v3710':'lil_B156_fonts_v3713','lil_B156_editorial_manuscript_v3':'lil_B156_editorial_manuscript_v4',"('lil_B156_layout_v1','lil_B156_layout_v2')":"('lil_B156_layout_v1','lil_B156_layout_v3')"}))
    failed=Path('work/analysis/lil_B156_layout_v3709/all76_paragraph_layout_QA.json');root.mkdir(parents=True);save(root/'failed_plan_and_possessive_phrase_refinement.json',dict(failed_plan=str(failed),failed_plan_sha256=sha(failed.read_bytes()),finding='Protecting hire you exposed a weak your line ending. Keep your skills together;no warning waiver or prose change.',tools=pairs,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
