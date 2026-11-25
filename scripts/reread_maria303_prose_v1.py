"""Save three naturalness refinements after reading all303 final paragraphs as exchanges."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

BEFORE=Path('translations/maria_B58_B70_contextual_review_v1.json')
AFTER=Path('translations/maria_B58_B70_contextual_review_v2.json')
CHANGES={
    'DK4_MES_B61_R0053':(
        "Showing you there would be easy enough, miss... But I still think you'd be better off staying away...",
        "Taking you there would be easy enough, miss... But I still think you'd be better off staying away...",
        'Read-aloud refinement: taking someone there is natural American speech for 案内する; showing you there is an awkward collocation. Preserve the offer, ordinary miss address and warning.'),
    'DK4_MES_B62_R0021':(
        'Has that man still not arrived?',
        'Is that man still not here?',
        'Use a natural spoken arrival question while retaining Maria\'s surprise that the expected man has not appeared.'),
    'DK4_MES_B70_R0041':(
        'Oh. Actually, what I heard about was the clothing.',
        'Oh. Actually, I heard something about what they wear.',
        'Give Angelo a natural casual correction about ninja clothing, setting up the reported black outfit without adding a named source or eyewitness claim.'),
}

def main():
    proof=Path('work/Maria_B58_B70_clean_20261109/final_exchange_reread_v1.json')
    assert not AFTER.exists() and not proof.exists()
    doc=deepcopy(load(BEFORE));seen=set();amendments=[]
    for r in doc['records']:
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if r['id'] in CHANGES:
            before,after,note=CHANGES[r['id']];assert r['english']==before and r['decision']=='revision'
            r.update(english=after,logical_English=after,proposed_English=after)
            r['finding']+=' '+note;r['localization_note']=r['finding']
            amendments.append(dict(id=r['id'],before=before,after=after,reason=note));seen.add(r['id'])
        assert r['english'].isascii() and '\n' not in r['english']
        assert all(r['english'].count(t)==r['source_macros'].get(t,0) for t in ['FI','FA','FO','FU'])
        assert (r['english']==r['current_comparison_paragraph'])==(r['decision']=='retention')
        r['final_whole_exchange_readaloud_review_complete']=True
    assert seen==set(CHANGES) and len(doc['records'])==303
    assert Counter(r['decision'] for r in doc['records'])=={'revision':181,'retention':122}
    doc.update(previous_prose_manuscript=str(BEFORE),previous_prose_manuscript_sha256=digest(BEFORE),
        final_readaloud_amendments=amendments,all303_paragraphs_read_in_ten_complete_exchanges=True)
    doc['evidence'].update({str(BEFORE):digest(BEFORE),str(Path(__file__)):digest(__file__)})
    save(AFTER,doc)
    save(proof,dict(manuscript=str(AFTER),manuscript_sha256=digest(AFTER),read_paragraphs=303,complete_exchanges=10,
        naturalness_refinements=amendments,revision_retention_counts_unchanged=True,
        all_fifth_gates_still_false=True,no_new_pages_gameplay_orintegration=True,new_credit=0))
    print('Read303 final paragraphs as ten complete exchanges;three naturalness refinements saved.181 revisions/122 retentions;formatting pending.')

if __name__=='__main__':main()
