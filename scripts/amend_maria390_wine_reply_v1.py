"""Restore the clean-first draft that fits the complete problem/no-problem exchange."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')
IDENT='DK4_MES_B152_R0008'


def main():
    priorpath=Path('translations/maria_B152_B175_contextual_review_v1.json')
    output=Path('translations/maria_B152_B175_contextual_review_v2.json')
    docpath=ROOT/'formatting_v1/formatting_input.json';nextdoc=ROOT/'formatting_v2/formatting_input.json'
    findingpath=ROOT/'wine_reply_contextual_amendment_v1.json'
    assert not any(p.exists() for p in [output,nextdoc.parent,findingpath])
    prior=load(priorpath);prose=deepcopy(prior);doc=deepcopy(load(docpath))
    rows={r['id']:r for r in prose['records']};row=rows[IDENT]
    assert row['source_Japanese']=='悪いか！' and row['proposed_English']==row['english']=='So what?'
    assert row['decision']=='retention' and row['independent_English_draft']=='Got a problem with that?'
    assert rows['DK4_MES_B152_R0005']['proposed_English']=="Hey, you're still drinking that stuff?"
    assert rows['DK4_MES_B152_R0012']['proposed_English']=="Not at all. But wine's the thing now. Wine!"
    reason='Reopen the isolated So what? retention after viewing the whole wine exchange. Clean 悪いか！ asks whether there is a problem, and 悪かぁないけどよ explicitly answers no. Restore the already saved clean-first independent draft Got a problem with that? so Not at all answers the actual challenge naturally. Keep the rough defensive voice without inventing a relationship or fact.'
    def revise(r):
        assert r['english']==r['proposed_English']=='So what?' and r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        r.update(english='Got a problem with that?',logical_English='Got a problem with that?',
            proposed_English='Got a problem with that?',decision='revision',finding=reason,localization_note=reason,retention_reason='',
            reopened_retention_exact_previous_prose=str(priorpath),reopened_retention_exact_previous_prose_sha256=digest(priorpath),
            final_whole_exchange_readaloud_review_complete=True)
    revise(row)
    formatted=next(r for r in doc['records'] if r['id']==IDENT);revise(formatted)
    assert formatted['source_selector']==96 and formatted['planned_English_markup']=='{SPEAKER:60}So what?'
    formatted.update(editorial_logical_English='Got a problem with that?',planned_English_markup='{SPEAKER:60}Got a problem with that?')
    for value in [prose,doc]:
        value.update(proposed_revisions=154,justified_retentions=236,previous_contextual_prose=str(priorpath),
            previous_contextual_prose_sha256=digest(priorpath),one_whole_exchange_retention_reopened=True,new_credit=0)
        assert Counter(r['decision'] for r in value['records'])=={'revision':154,'retention':236}
    save(output,prose)
    doc.update(source_full_manuscript=str(output),source_full_manuscript_sha256=digest(output),
        previous_formatting_input=str(docpath),previous_formatting_input_sha256=digest(docpath),
        only_one_logical_paragraph_changed_all_controls_macros_names_andother389_objects_exact=True)
    nextdoc.parent.mkdir();save(nextdoc,doc)
    oldrows={r['id']:r for r in prior['records']}
    assert all(r==oldrows[r['id']] for r in prose['records'] if r['id']!=IDENT)
    save(findingpath,dict(id=IDENT,source_reference=row['source_reference'],current_reference=row['current_reference'],
        source_Japanese=row['source_Japanese'],source_hex=row['source_hex'],current_hex=row['current_hex'],
        whole_exchange_context=row['whole_exchange_context'],previous_English='So what?',revised_English=row['english'],finding=reason,
        before_andafter_neighbors=[dict(id=i,source_Japanese=rows[i]['source_Japanese'],English=rows[i]['proposed_English'])
            for i in ['DK4_MES_B152_R0005',IDENT,'DK4_MES_B152_R0012']],
        unchanged_objects=389,revisions=154,retentions=236,first_four_individual_gates_pass=True,
        changed_record_fresh_native_storage_andgameplay_checks_pending=True,registered_integration_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [priorpath,docpath,output,nextdoc,Path(__file__)]}))
    print('Revised one whole-exchange retention from its original clean-first draft;154 revisions/236 retentions,389 objects unchanged.')


if __name__=='__main__':main()
