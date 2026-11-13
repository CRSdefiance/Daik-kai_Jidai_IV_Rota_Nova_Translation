"""Balance complete final rows as well as earlier rows;retain sentence-aware pagination."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_final_balance_tools_v7984e')
if __name__=='__main__':
    assert not ROOT.exists()
    adapter="""ADAPTER=checked_text(ADAPTER,{
    '(0 if final else (cells-length)**2*(2 if line==0 else 1))':'((cells-length)**2*(2 if line==0 else 1))',
})
"""
    result=derive('scripts/plan_Rafael_B47_layout_v7984d.py','scripts/plan_Rafael_B47_layout_v7984e.py',{
        'Rafael_B47_layout_v7984d':'Rafael_B47_layout_v7984e',
        'PAIRS=previous.PAIRS|{':adapter+'PAIRS=previous.PAIRS|{',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        finding='Ignoring final-row raggedness packs the new second page tostand/achance rather than a complete conditional-clause boundary.',
        correction='Use the same automatic raggedness score for the final row;retain orphan,page-sentence,row-count andsoft-boundary priorities.',
        no_prose_orfont_width_page_capacity_pair_phase_orQA_guard_change=True,
        native_pages_andactual_page_turn_still_required=True,new_credit=0,full_goal_complete=False))
    print('Prepared automatic final-row balance successor;no prose ornative safety changes.')
