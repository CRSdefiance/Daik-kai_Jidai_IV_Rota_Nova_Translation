"""Preserve six viewed sheets and refine four ordinary phrase boundaries without changing prose."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_B159_viewed_flow_v3839');assert not root.exists();pairs=[]
    pairs.append(derive('dk4tool/dialogue/lil_B159_layout_v2.py','dk4tool/dialogue/lil_B159_layout_v3.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('oh','right'),('great','cooking'),('hate','to'),('weird','hobby')})\n\ndef _word(value):"}))
    pairs.append(derive('scripts/plan_lil_B159_layout_v3837.py','scripts/plan_lil_B159_layout_v3840.py',{'lil_B159_layout_v2':'lil_B159_layout_v3','lil_B159_layout_v3837':'lil_B159_layout_v3840','lil_B159_editorial_manuscript_v1':'lil_B159_editorial_manuscript_v2','lil_B159_editorial_manuscript_v2':'lil_B159_editorial_manuscript_v3'}))
    root.mkdir(parents=True);save(root/'six_viewed_sheets_and_four_automatic_phrase_refinements.json',dict(all6_original_native_sheets_viewed=True,findings=[dict(id='DK4_MES_B159_R0077',resolution='Keep weird hobby together.'),dict(id='DK4_MES_B159_R0085',resolution='Keep Oh, right together.'),dict(id='DK4_MES_B159_R0088',resolution='Keep great cooking together.'),dict(id='DK4_MES_B159_R0186',resolution='Keep hate to together so I hate to admit it begins a coherent row.')],tools=pairs,all_source_meanings_English_words_and_retention_decisions_unchanged=True,no_manual_layout_or_guard_waiver=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
