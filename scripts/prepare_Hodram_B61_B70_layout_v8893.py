"""Retain passing first plans; qualify readable sentence/tag/auxiliary boundaries."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_layout_preparation_v8893')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('work/analysis/Hodram_B61_B70_layout_v8892/automatic_plans.json');doc=read(old)
    assert len(doc['records'])==224 and not doc['failures']
    assert not any(i['severity'] in ['error','warning'] for r in doc['records'] for i in r['base_QA']['issues'])
    additional="""PAIRS=(PAIRS-{('king','of')})|{('what','is'),('is','your'),('your','homeland'),('homeland','like'),("don't",'you'),('truly','are'),('never','mind'),('one','will'),('will','object'),('iron','ship'),("world's",'finest'),('finest','navy'),('after','all'),('make','our'),('our','lives'),("i'll",'have'),("couldn't",'ask'),("won't",'be'),('get','along'),('someone','would'),("i'm",'not')}
"""
    receipt=derive('scripts/plan_Hodram_B61_B70_v8892.py','scripts/plan_Hodram_B61_B70_v8893.py',{
        'work/analysis/Hodram_B61_B70_layout_v8892':'work/analysis/Hodram_B61_B70_layout_v8893',
        "    'Hodram B31/B53 plan:':'Hodram B61-B70 plan:',":
            "    '(line==0 and not final and length<=12)':'(line==0 and not final and length<=12 and not terminal)',\n    'Hodram B31/B53 plan:':'Hodram B61-B70 plan:',",
        'ENV={**previous.ENV':additional+'ENV={**previous.ENV'
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_readability_successor.json',dict(derivation=receipt,prior_passing_plans=str(old),
        findings=[
            'B64R11 had first row You truly because a newly added king/of preference overconstrained the longer Indian Ocean complement. Remove only that new batch pair, retaining all earlier frozen/global planners.',
            'B63R22 split the short tag don\'t/you? Add its coherent pair rather than alter prose or narrow the viewport.',
            'B62R39 benefits from keeping what-is-your-homeland-like as a question. A complete opening clause ending in sentence/pause punctuation may be short; the tiny-opening preference should still penalize an incomplete You truly.',
            'B67R238 split He won\'t/be easy across a page. Keep the contracted auxiliary with be. Additional compound/auxiliary pairs reflect the reviewed prose.'],
        no_prose_orfont_viewport_native_geometry_page_height_encoder_guard_macro_orbase_QA_change=True,
        terminal_first_clause_only_exempt_from_soft_tiny_preference_not_safety_orQA=True,
        prior_plans_preserved_for_before_after_comparison=True,new_credit=0,full_goal_complete=False))
