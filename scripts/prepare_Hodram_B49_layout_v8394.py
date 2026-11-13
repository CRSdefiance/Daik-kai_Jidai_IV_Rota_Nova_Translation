"""Source-lock the reviewed complete-word paragraph boundary and coherent auxiliary/request phrases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_layout_tools_v8394');assert not root.exists()
    helper='''ORDINARY_BINDINGS={r['id']:dict(source_hex=r['source_hex'],logical_English=r['english'],pairs=[('new','world')]) for r in document['records'] if r['id']=='DK4_MES_B49_R0033'}
assert len(ORDINARY_BINDINGS)==1

def ordinary_boundaries(row,body):
    if row['id'] not in ORDINARY_BINDINGS:return frozenset()
    binding=ORDINARY_BINDINGS[row['id']]
    if row['source_hex']!=binding['source_hex'] or body!=binding['logical_English']:
        raise ValueError('Exact source-qualified B49 directions paragraph required for ordinary word boundary')
    return set(binding['pairs'])

def get_profile(row):'''
    d=derive('scripts/plan_Hodram_B49_layout_v8393.py','scripts/plan_Hodram_B49_layout_v8394.py',{
        'Hodram_B49_layout_v8393':'Hodram_B49_layout_v8394',
        'def get_profile(row):':helper,
        "    'Hodram B47/B48 plan:':'Hodram B49 plan:'":"    'ordinary=pair in set()':'ordinary=pair in ordinary_boundaries(row,body)',\n    'Hodram B47/B48 plan:':'Hodram B49 plan:'",
        "('new','world')}\nENV=":"('new','world'),(\"i'd\",'trade'),('give','me'),('now','give'),('find','it'),('give','you')}\nENV=",
        "'source_bound_ellipsis':source_bound_ellipsis}":"'source_bound_ellipsis':source_bound_ellipsis,'ordinary_boundaries':ordinary_boundaries}",
        'source_bound_ellipsis_bindings=ELLIPSIS_BINDINGS,':'source_bound_ellipsis_bindings=ELLIPSIS_BINDINGS,source_owned_ordinary_boundary_predicate=inspect.getsource(ordinary_boundaries),ordinary_boundary_bindings=ORDINARY_BINDINGS,prior_layout_preserved="work/analysis/Hodram_B49_layout_v8393/automatic_plans.json",read_only_comparison="work/analysis/Hodram_B49_wrap_compare_v8393b/read_only_wrap_comparison.json",all_QA_recomputed_for_changed_compiler_breaks_without_filtering=True,',
    })
    root.mkdir(parents=True);save(root/'reviewed_automatic_wrap_derivation.json',dict(derivation=d,all_native_high_constants_andmultiplicity_preserved=True,only_exact_source_andapproved_R33_New_World_complete_word_boundary_allowed=True,all_prose_words_and216usable_width_preserved=True,source_qualifications_names_controls_NUL_guard_andglobal_profiles_unchanged=True,no_formatting_gate_approval_before_native_display_review=True,new_credit=0,full_goal_complete=False))
