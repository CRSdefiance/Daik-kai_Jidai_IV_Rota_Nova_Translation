"""Keep the viewed rear-mast noun phrase together;preserve all reviewed prose."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_rear_mast_flow_v4134b')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B167_layout_v4.py','dk4tool/dialogue/lil_B167_layout_v5.py',{
        'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('rear','mast')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B167_layout_v4134.py','scripts/plan_lil_B167_layout_v4134b.py',{
        'lil_B167_layout_v4':'lil_B167_layout_v5','lil_B167_layout_v4134':'lil_B167_layout_v4134b',
        'lil_B167_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v6',
        'lil_B167_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v7'}))
    tools.append(derive('scripts/verify_lil_B167_fonts_v4134.py','scripts/verify_lil_B167_fonts_v4134b.py',{
        'lil_B167_layout_v4':'lil_B167_layout_v5','lil_B167_fonts_v4134':'lil_B167_fonts_v4134b',
        'lil_B167_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v7',
        'lil_B167_fonts_v4132d/current_macro_QA_and_progressive_font_proof':'lil_B167_fonts_v4134/current_macro_QA_and_progressive_font_proof'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,viewed_finding='R112 rear / mast split after right-behind-you was preserved; keep rear mast whole.',
        no_prose_meaning_macro_control_or_decision_change=True,no_ROM_registry_ledger_credit_change=True))
    print('Viewed rear-mast phrase protected;reviewed wording unchanged.')
