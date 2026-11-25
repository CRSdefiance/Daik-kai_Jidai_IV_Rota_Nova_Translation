"""Bind one provisional speaker attribution to clean actor7; retain the original seal."""
from copy import deepcopy
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT, OUT as PRIOR

OUT = ROOT/'all394_clean_meanings_before_English_v2.json'
REFERENCE = ROOT/'draft_names_andterms_reference_v1.json'


def main():
    assert not OUT.exists()
    prior, reference = map(load,(PRIOR,REFERENCE))
    assert reference['source_meanings_sha256'] == digest(PRIOR)
    actor7 = next(r for r in reference['records'] if r['actor_ID']==7)
    assert actor7['source_andcurrent_fields'][0]['source']['text']=='クリスティナ'
    assert actor7['source_andcurrent_fields'][0]['current']['text']=='Cristina'
    result = deepcopy(prior)
    row = next(r for r in result['records'] if r['id']=='DK4_MES_B17_R0103')
    assert row['source_selector']==7 and 'Lil says' in row['source_meaning']
    before = row['source_meaning']
    row['source_meaning'] = row['source_meaning'].replace('Lil says','Cristina says',1)
    result.update(previous_meaning_seal=str(PRIOR),previous_meaning_seal_sha256=digest(PRIOR),
        source_identity_amendments=[dict(id=row['id'],source_selector=7,previous_meaning=before,
            corrected_meaning=row['source_meaning'],reason='Exact clean actor7 given-name field identifies Cristina; actor2 is Lil. No eligible existing dialogue was consulted.')],
        current_eligible_story_English_not_extracted=True,
        evidence={**prior['evidence'],str(PRIOR):digest(PRIOR),str(REFERENCE):digest(REFERENCE),str(Path(__file__)):digest(__file__)})
    assert len(result['records'])==394
    save(OUT,result)
    print('Preserved original seal; corrected actor7 attribution in one source gloss. All394 meanings remain source-first.')


if __name__=='__main__':
    main()
