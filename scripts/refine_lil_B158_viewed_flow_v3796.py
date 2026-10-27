"""Preserve three viewed sheets and keep the complete affection-for-the-song clause together."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B158_viewed_flow_v3796');assert not root.exists();pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B158_layout_v1.py','dk4tool/dialogue/lil_B158_layout_v2.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('love','this'),('this','song')})\n\ndef _word(value):"}))
    pairs.append(derive('scripts/plan_lil_B158_layout_v3794.py','scripts/plan_lil_B158_layout_v3797.py',{'lil_B158_layout_v1':'lil_B158_layout_v2','lil_B158_layout_v3794':'lil_B158_layout_v3797','lil_B158_editorial_manuscript_v1':'lil_B158_editorial_manuscript_v2','lil_B158_editorial_manuscript_v2':'lil_B158_editorial_manuscript_v3'}))
    root.mkdir(parents=True);save(root/'three_viewed_sheets_and_one_phrase_refinement.json',dict(all3_original_native_sheets_viewed=True,findings=[dict(id='DK4_MES_B158_R0118',resolution='Keep I love this song together rather than breaking after love. Unchanged source-faithful words; automatic phrase boundary only.')],tools=pairs,source_meaning_all_words_and_retention_decisions_unchanged=True,no_manual_layout_or_guard_waiver=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
