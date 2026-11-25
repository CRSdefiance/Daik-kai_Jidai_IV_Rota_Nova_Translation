"""Keep the viewed right-behind-you phrase whole without changing reviewed words."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_viewed_flow_v4134')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B167_layout_v3.py','dk4tool/dialogue/lil_B167_layout_v4.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('right','behind'),('behind','you')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B167_layout_v4131d.py','scripts/plan_lil_B167_layout_v4134.py',{
        'lil_B167_layout_v3':'lil_B167_layout_v4','lil_B167_layout_v4131d':'lil_B167_layout_v4134',
        'lil_B167_editorial_manuscript_v4':'lil_B167_editorial_manuscript_v5',
        'lil_B167_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v6'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,finding='Viewed R112 split wind right / behind you; keep the complete directional phrase together.',
        all_four_native_sheets_and_typed_menu_sheet_viewed=True,no_reviewed_prose_meaning_or_decision_change=True,
        no_ROM_registry_ledger_credit_change=True))
    print('Viewed R112 right-behind-you phrase protected;all reviewed words unchanged.')
