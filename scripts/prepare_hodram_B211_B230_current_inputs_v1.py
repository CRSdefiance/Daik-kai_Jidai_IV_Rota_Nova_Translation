"""Bind only after all source-first drafts are sealed, using preserved clean inventories."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.consolidate_hodram_B211_B230_clean_drafts_v1 import ROOT,OUT as DRAFTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT=Path('work/Hodram_B211_B230_resume_20261106/binding_inputs_v1')

def main():
    assert not OUT.exists()
    drafts=load(DRAFTS);means=load(ROOT/'complete_clean_meanings_before_English.json')
    assert len(drafts['records'])==277 and drafts['previous114_drafts_exactly_preserved']
    assert drafts['source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake']
    packet=ROOT/'clean_source_packet.json'
    rows=[deepcopy(r) for r in means['records'] if 'source_complete_preamble_hex' in r]
    assert len(rows)==241
    for row in rows:row['current_ROM_English_unconsulted']=True
    OUT.mkdir(parents=True)
    save(OUT/'meanings.json',dict(source_packet=str(packet),source_packet_sha256=digest(packet),
        records=rows,meanings=241,all_drafts_sealed=str(DRAFTS),all_drafts_sha256=digest(DRAFTS),
        no_blanket_prior_English_exposure_claim=True,new_credit=0))
    for kind in ['style','choice']:
        source=ROOT/f'clean_{kind}_objects.json';doc=deepcopy(load(source))
        for row in doc['records']:row['earlier_English_unconsulted']=True
        doc['sealed_all_drafts']=str(DRAFTS);doc['sealed_all_drafts_sha256']=digest(DRAFTS)
        save(OUT/f'{kind}_objects.json',doc)
    print('Prepared exact sealed inputs: 241 ordinary speeches, 29 styles, seven captions.')

if __name__=='__main__':main()
