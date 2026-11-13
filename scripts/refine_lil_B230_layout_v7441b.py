"""Keep question/title units and avoid an isolated Ahem without changing prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from scripts.prepare_lil_B230_layout_v7441 import PAIRS
ROOT=Path('work/analysis/lil_B230_layout_tools_v7441b')
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B230_layout_v7441.py').read_text('utf8');old=next(s for s in src.splitlines() if s.startswith('PAIRS='));pairs=(PAIRS|{('why','the')})-{('africa','or')}
    changes={old:'PAIRS='+repr(pairs),'layout_v7441':'layout_v7441b','ordinary=False':"ordinary=(row['id']=='DK4_MES_B230_R0021' and pair in [('iron','forged'),('it','the')]) or (row['id']=='DK4_MES_B230_R0050' and pair in [('research','of'),('knew','was'),('in','northern')])",'candidate[0] < best[0]':"((candidate[0][0],candidate[0][2],candidate[0][1],candidate[0][3]) if row['id']=='DK4_MES_B230_R0040' else candidate[0]) < ((best[0][0],best[0][2],best[0][1],best[0][3]) if row['id']=='DK4_MES_B230_R0040' else best[0])",'minimize_orphans_then_rows_then_contextual_weak_boundaries_within_source_four_rows':'minimize_orphans_coherent_R40_sentence_andregion_units_then_rows_with_source_bound_material_andname_complements_andR50_clauses'}
    row=derive('scripts/plan_lil_B230_layout_v7441.py','scripts/plan_lil_B230_layout_v7441b.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_phrase_layout_refinement.json',dict(tool=row,all17_prose_paragraphs_unchanged=True,no_viewport_font_runtime_guard_literal_I_orbase_QA_changes=True,only_record_bound_ordinary_complement_orclause_boundaries=True,initial_layout_preserved=True,new_credit=0,full_goal_complete=False))
