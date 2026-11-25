"""Retain the source-faithful existing spirit-beast sentence after scoped term review."""
from copy import deepcopy
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B231_B250_contextual_v1 import OUT as PRIOR
from scripts.review_hodram_B231_B250_names_terms_v1 import TERMS

OUT=PRIOR.with_name('hodram_B231_B250_contextual_review_v2.json')

def main():
    assert not OUT.exists();doc=deepcopy(load(PRIOR));terms=load(TERMS)
    assert next(r for r in terms['equipment_terms'] if r['index']==110)['current_term']=='Gupta Spirit Beast'
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B239_R0033')
    assert row['decision']=='revision' and row['english'].startswith("It's about a statue of a sacred beast")
    row.update(english=row['current_comparison_paragraph'],logical_English=row['current_comparison_paragraph'],decision='retention',
        finding='The existing sentence preserves the Gupta origin and reputed power. Spirit beast is the established readable fantasy term in this magical-statue exchange; retain this working wording.',
        retention_reason='The source-faithful reported power, Gupta origin and established spirit-beast term already work in the complete exchange.')
    row['localization_note']=row['finding']
    old={r['id']:r for r in load(PRIOR)['records']}
    assert all(r==old[r['id']] for r in doc['records'] if r['id']!=row['id'])
    counts=dict(Counter(r['decision'] for r in doc['records']));assert counts=={'retention':110,'revision':115}
    doc.update(counts=counts,parent_contextual_review=str(PRIOR),parent_contextual_review_sha256=digest(PRIOR),
        scoped_term_refinement_only=True,all_other224_decisions_exactly_preserved=True)
    doc['evidence'].update({str(PRIOR):digest(PRIOR),str(TERMS):digest(TERMS),__file__:digest(__file__)})
    save(OUT,doc);print('Retained the existing spirit-beast sentence: 115 revisions, 110 justified retentions; other 224 decisions unchanged.')

if __name__=='__main__':main()
