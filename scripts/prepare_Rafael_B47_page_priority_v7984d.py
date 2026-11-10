"""Prefer a complete sentence at a required native page turn without changing prose orgeometry."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_page_priority_tools_v7984d')
PAGE_ADAPTER="""ADAPTER=checked_text(ADAPTER,{
    'return (0,0,0,0),()':'return (0,0,0,0,0),()',
    'cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+':
        'cost[0]+tiny,cost[1]+int(not final and (line+1)%4==0 and not terminal),cost[2]+1,cost[3]+weak,cost[4]+',
})
"""
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/plan_Rafael_B47_layout_v7984c.py','scripts/plan_Rafael_B47_layout_v7984d.py',{
        'Rafael_B47_layout_v7984c':'Rafael_B47_layout_v7984d',
        'PAIRS=previous.PAIRS|{':PAGE_ADAPTER+'PAIRS=previous.PAIRS|{',
        'orphan_avoidance_then_rows_then_soft_weak_preferences':
            'orphan_avoidance_then_sentence_page_boundaries_then_rows_then_soft_weak_preferences',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        finding='R53 cannot fit the complete paragraph in four native rows;the initial five-row solution turns the page inside its conditional clause.',
        correction='After orphan avoidance,prefer a sentence orstrong punctuation boundary at every original four-row page turn,then minimize rows andsoft weak boundaries.',
        unchanged_words_punctuation_width_four_physical_rows_pair_phase_source00_andall_QA_checks=True,
        automatic_page_boundary_not_translator_authored_break_ornew_runtime_control=True,
        requires_complete_native_pages_andfocused_actual_page_transition_before_approval=True,
        no_global_profile_font_native_guard_orhistorical_compiler_change=True,new_credit=0,full_goal_complete=False))
    print('Prepared automatic sentence-aware native page-turn successor;R53 prose preserved,full native/actual transition checks required.')
