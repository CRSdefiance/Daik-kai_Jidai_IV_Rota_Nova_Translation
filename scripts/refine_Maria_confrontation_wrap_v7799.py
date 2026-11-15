"""Keep the short He's a great merchant sentence together using a scoped soft-wrap preference."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Maria_confrontation_layout_v7793 as layout
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_wrap_v7799')
PREVIOUS=Path('work/analysis/maria_confrontation_intro_v7796/16_complete_automatic_plans_original_macro_order_preserved.json')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,doc=map(read,[PREVIOUS,MANUSCRIPT]);assert prior['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    env=dict(layout.ENV);env['PAIRS']=layout.ENV['PAIRS']|{("he's","a")}
    exec(compile(layout.ADAPTER,__file__+'::source-bound-sentence-coherence','exec'),env)
    rows=[];changed=[]
    for row in doc['records']:
        before=next(p for p in prior['records'] if p['id']==row['id']);p=deepcopy(before)
        candidate=env['plan'](deepcopy(p['planning_record']))
        assert candidate['English']==p['English'] and ' '.join(candidate['lines'])==' '.join(p['lines'])
        if candidate['encoded_hex']!=p['encoded_hex']:
            assert row['source_record_index']==37 and ("he's","a") in {tuple(b['pair']) for b in p['automatic_boundaries']}
            p.update(candidate);p['base_QA']=layout.base_qa(p['planning_record'],p)
            assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
            assert "He's a great merchant!" in p['lines']
            changed.append(dict(id=row['id'],before_lines=before['lines'],after_lines=p['lines'],
                reason="Native preview review found the short closing sentence split after He's. A source-scoped ordinary word-pair preference keeps He's a great merchant! together. No prose, meaning, width, guard, font or global QA rule changes."))
        rows.append(p)
    assert len(changed)==1 and len(rows)==16 and all(p['expected_native_pages']==1 for p in rows)
    ROOT.mkdir(parents=True);save(ROOT/'16_plans_one_sentence_coherence_refinement_no_prose_change.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,failures=[],
        previous_plan=str(PREVIOUS),previous_plan_sha256=sha(PREVIOUS.read_bytes()),changed_records=changed,
        source_owned_plan_adapter=layout.ADAPTER,source_word_boundary_pairs=sorted(env['PAIRS']),
        one_source_bound_He_s_a_soft_wrap_preference=True,all15_other_compiled_bodies_lineplans_andQA_exact=True,
        all16_original_logical_paragraphs_andcontrols_unchanged=True,no_manual_break_padding_width_font_macro_or_global_QA_change=True,
        complete_native_pages=16,row_count_infos=sum(i['code']=='line-break-count' for p in rows for i in p['base_QA']['issues']),
        all16_formatting_gates_false=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,MANUSCRIPT,Path(layout.__file__),Path(__file__)]}))
    print(changed)
