"""Compare scoped complete-word paragraph alternatives without changing approved prose or native metrics."""
from pathlib import Path
from scripts import plan_Hodram_B49_layout_v8393 as original
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_wrap_compare_v8393a')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(original.DOC);baseline=read(original.ROOT/'automatic_plans.json');selected=[r for r in doc['records'] if r['source_record_index'] in [19,33,71]];results=[]
    for label,pair in [('article-before-New-World',('the','new')),('preposition-before-the-New-World',('in','the'))]:
        def ordinary_boundaries(row,body):
            if row['id']!='DK4_MES_B49_R0033':return frozenset()
            approved=next(r for r in doc['records'] if r['id']==row['id']);assert row['source_hex']==approved['source_hex'] and body==approved['english'];return {pair}
        code=checked_text(original.ADAPTER,{'ordinary=pair in set()':'ordinary=pair in ordinary_boundaries(row,body)'})
        env={**original.ENV,'PAIRS':original.PAIRS|{("i'd",'trade'),('give','me')},'ordinary_boundaries':ordinary_boundaries};exec(compile(code,__file__+'::read-only-comparison','exec'),env)
        for row in selected:
            planning=dict(row);planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'];p=env['plan'](planning);assert ' '.join(p['lines'])==row['english']
            results.append(dict(comparison=label,id=row['id'],logical_chars=len(row['english']),logical_English=row['english'],baseline_lines=next(r for r in baseline['records'] if r['id']==row['id'])['lines'],candidate_lines=p['lines'],candidate_cell_lengths=p['line_lengths'],native_pages=p['expected_native_pages'],base_QA=original.base_qa(planning,p),no_prose_metrics_font_guard_orviewport_change=True))
    ROOT.mkdir(parents=True);save(ROOT/'read_only_wrap_comparison.json',dict(candidates=results,prose_unmodified=True,ordinary_allowance_only_exact_R33_source_andapproved_text=True,all_original_QA_issues_retained=True,no_native_font_stored_actual_orfinal_formatting_approval=True,new_credit=0,full_goal_complete=False))
    for r in results:print(r['comparison'],r['id'],r['candidate_lines'],r['candidate_cell_lengths'],[(x['severity'],x['code']) for x in r['base_QA']['issues']])
