"""Keep the complete following-wind phrase together with no further prose change."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_flow_tools_v4131c')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B167_layout_v2.py','dk4tool/dialogue/lil_B167_layout_v3.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('with','a'),('a','following')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B167_layout_v4131b.py','scripts/plan_lil_B167_layout_v4131c.py',{
        'lil_B167_layout_v2':'lil_B167_layout_v3','lil_B167_layout_v4131b':'lil_B167_layout_v4131c'}))
    tools.append(derive('scripts/verify_lil_B167_fonts_v4132b.py','scripts/verify_lil_B167_fonts_v4132c.py',{
        'lil_B167_layout_v2':'lil_B167_layout_v3','lil_B167_fonts_v4132b':'lil_B167_fonts_v4132c'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,no_prose_meaning_control_or_decision_change=True,
        preserve_both_failed_layout_plans=True,no_guard_change_waiver_or_ROM_registry_ledger_credit=True))
    print('B167 following-wind phrase protected;reviewed wording unchanged.')
