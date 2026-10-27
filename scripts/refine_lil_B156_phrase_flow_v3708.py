"""Resolve two viewed phrase splits without changing a reviewed word."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B156_phrase_flow_v3708');assert not root.exists()
    pairs=[derive('dk4tool/dialogue/lil_B156_layout_v1.py','dk4tool/dialogue/lil_B156_layout_v2.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({(\"why's\",'he'),('hire','you')})\n\ndef _word(value):"})]
    pairs.append(derive('scripts/plan_lil_B156_layout_v3706.py','scripts/plan_lil_B156_layout_v3709.py',{'lil_B156_layout_v1':'lil_B156_layout_v2','lil_B156_layout_v3706':'lil_B156_layout_v3709','lil_B156_editorial_manuscript_v1':'lil_B156_editorial_manuscript_v2','lil_B156_editorial_manuscript_v2':'lil_B156_editorial_manuscript_v3'}))
    root.mkdir(parents=True);save(root/'two_viewed_phrase_splits_and_automatic_successor.json',dict(viewed_sheets=list(range(1,11)),findings=[dict(id='DK4_MES_B156_R0157',finding="Why's separated from he",resolution='Protect the two-word question opening.'),dict(id='DK4_MES_B156_R0288',finding='hire separated from you',resolution='Protect hire you in the bodyguard offer.')],tools=pairs,reviewed_wording_and_all_native_metrics_guards_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
