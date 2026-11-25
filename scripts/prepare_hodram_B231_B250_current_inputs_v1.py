"""Bridge sealed clean-first drafts to the existing original-consumer current binders."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.draft_hodram_B231_B250_clean_v1 import OUT as DRAFTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B231_B250_scope_v1 import ROOT,ELIGIBLE

OUT=ROOT/'binding_inputs_v1'

def main():
    assert not OUT.exists();drafts=load(DRAFTS)
    assert drafts['records_count']==225 and drafts['all225_logical_drafts_written_before_current_story_English_intake_in_this_batch']
    source={r['id']:r for r in load(ROOT/'all225_clean_meanings_before_English.json')['records']}
    for row in drafts['records']:
        assert all(row[k]==source[row['id']][k] for k in ('source_reference','source_hex','source_Japanese'))
    OUT.mkdir();sealed=OUT/'sealed_drafts.json'
    save(sealed,{**drafts,'source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake':True,
        'original_drafts':str(DRAFTS),'original_drafts_sha256':digest(DRAFTS),'metadata_only_schema_bridge_all225_drafts_unchanged':True})
    ordinary=[deepcopy(r) for r in drafts['records'] if 'source_complete_preamble_hex' in r]
    assert len(ordinary)==209
    for row in ordinary:row['current_ROM_English_unconsulted']=True
    save(OUT/'meanings.json',dict(source_packet=str(ELIGIBLE),source_packet_sha256=digest(ELIGIBLE),records=ordinary,meanings=209,
        all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),no_blanket_prior_English_exposure_claim=True,new_credit=0))
    for kind in ('style','choice'):
        path=ROOT/f'clean_{kind}_objects.json';doc=deepcopy(load(path))
        doc.update(sealed_all_drafts=str(sealed),sealed_all_drafts_sha256=digest(sealed))
        save(OUT/f'{kind}_objects.json',doc)
    print('Bound sealed 225 drafts to exact 209 ordinary, 14 style and two caption inputs. No current dialogue read yet.')

if __name__=='__main__':main()
