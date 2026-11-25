"""Restore one contextually sound current line found better during direct page review."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')
OLD=Path('translations/maria_B216_B252_contextual_review_v1.json')
NEW=Path('translations/maria_B216_B252_contextual_review_v2.json')


def main():
    out=ROOT/'viewed_prose_amendment_v1.json';newcomp=ROOT/'contextual_comparisons_v2.json';newinput=ROOT/'formatting_v1/formatting_input_v2.json'
    assert not any(p.exists() for p in [out,NEW,newcomp,newinput])
    doc=load(OLD);comparison_path=ROOT/'contextual_comparisons_v1.json';comparison=load(comparison_path)
    inputpath=ROOT/'formatting_v1/formatting_input.json';formatted=load(inputpath)
    key='DK4_MES_B242_R0011';row=next(r for r in doc['records'] if r['id']==key)
    assert row['english']=="We need to find that wanted man Jacob's fleet."
    assert row['current_comparison_paragraph']=="We must find Jacob's fleet."
    assert row['source_Japanese'].replace('\r','').replace('\n','')=='賞金首のジャコブ艦隊を捜さないと'
    quest=next(r for r in doc['records'] if r['id']=='DK4_MES_B240_R0011')
    assert '賞金首' in quest['source_Japanese'] and 'Jacob Portunto' in quest['english']
    text=row['current_comparison_paragraph']
    reason=('Retain the natural current self-reminder We must find Jacob\'s fleet. The complete quest already explicitly establishes Jacob as the wanted Dutch smuggler; '
        'repeating that wanted man here produced awkward English without adding useful context. The fleet-search objective, identity and urgency remain faithful. '
        'Direct page review reverses the earlier over-literal revision, preserving both original findings and drafts as historical evidence.')
    before=row['english']
    for target in [row,next(r for r in comparison['records'] if r['id']==key),next(r for r in formatted['records'] if r['id']==key)]:
        target.update(english=text,logical_English=text,proposed_English=text,decision='retention',finding=reason,
            localization_note=reason,retention_reason=reason,viewed_page_contextual_amendment=str(out),
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True)
    row['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    comp=next(r for r in comparison['records'] if r['id']==key);assert not any(comp['review'].values())
    frow=next(r for r in formatted['records'] if r['id']==key)
    frow.update(editorial_logical_English=text,planned_English_markup='{SPEAKER:03}'+text,prior_macro_normalized_comparison=text)
    assert not any(row['source_macros'].values())
    doc.update(proposed_revisions=202,justified_retentions=161,previous_manuscript=str(OLD),previous_manuscript_sha256=digest(OLD),
        viewed_page_prose_amendment=str(out),all_fifth_formatting_gates_pending=True)
    comparison.update(revised=202,retained=161,previous_comparison=str(comparison_path),previous_comparison_sha256=digest(comparison_path),
        viewed_page_prose_amendment=str(out))
    save(newcomp,comparison);doc['evidence'][str(newcomp)]=digest(newcomp);save(NEW,doc)
    formatted.update(proposed_revisions=202,justified_retentions=161,source_full_manuscript=str(NEW),source_full_manuscript_sha256=digest(NEW),
        previous_formatting_input=str(inputpath),previous_formatting_input_sha256=digest(inputpath),
        viewed_page_prose_amendment=str(out),all_fifth_formatting_gates_pending=True)
    save(newinput,formatted)
    original=load(OLD)
    assert len(doc['records'])==363 and sum(r['decision']=='revision' for r in doc['records'])==202
    assert [a['id'] for a,b in zip(original['records'],doc['records'],strict=True) if a['english']!=b['english']]==[key]
    save(out,dict(id=key,source_reference=row['source_reference'],current_reference=row['current_reference'],
        source_Japanese=row['source_Japanese'],source_quest_context_reference=quest['source_reference'],
        before=before,after=text,reason=reason,source_context_localization_andnaturalness_rechecked=True,
        new_manuscript=str(NEW),new_manuscript_sha256=digest(NEW),new_formatting_input=str(newinput),new_formatting_input_sha256=digest(newinput),
        all_other363_source_bindings_and362_paragraphs_unchanged=True,prior_drafts_andproposals_preserved=True,
        fresh_changed_text_formatting_andnative_display_pending=True,no_new_credit_orROM=True,
        evidence={str(p):digest(p) for p in [OLD,inputpath,comparison_path,newcomp,Path(__file__)]}))
    print('Restored one justified retention;202 revisions/161 retentions; onlyB242R11 requires fresh native text checks.')


if __name__=='__main__':main()
