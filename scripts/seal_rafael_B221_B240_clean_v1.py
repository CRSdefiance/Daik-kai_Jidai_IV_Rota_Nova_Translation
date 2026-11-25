"""Seal all B221–B240 source-first drafts before consulting Rafael2952 English."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B226_B240_clean_parts_v1 import ROOT, PACKET, STYLES, CHOICES


DRAFTS=[ROOT/f'{label}_clean_drafts_v1.json' for label in
    ('B221_B222','B223_B225','B226_B230','B231_B235','B236_B240')]
OUT=ROOT/'sealed_all_clean_first_v1'
LEDGER=Path('translations/editorial_review_current_v1.json')


def digest(p):
    return sha(Path(p).read_bytes())


def main():
    assert not OUT.exists()
    packet,style,choice=map(load,(PACKET,STYLES,CHOICES))
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert style['source_packet_sha256']==choice['source_packet_sha256']==digest(PACKET)
    blocks=list(range(221,241))
    assert [g['block'] for g in packet['groups']]==blocks
    assert [g['block'] for g in packet['groups'] if not g['records']]==[231]
    drafts=list(map(load,DRAFTS))
    assert [d['records_count'] for d in drafts]==[30,44,60,66,70]
    assert [b for d in drafts for b in d['complete_blocks']]==blocks
    assert all(d['no_current_English_extracted_for_this_intake_before_drafts'] and d['all_five_gates_pending'] for d in drafts)
    assert all(digest(p)==h for d in drafts for p,h in d['evidence'].items())
    records=[r for d in drafts for r in d['records']]
    byid={r['id']:r for r in records}
    speech=[r for g in packet['groups'] for r in g['records']]
    assert (len(speech),len(style['records']),len(choice['records']))==(234,29,7)
    assert (style['object_count'],style['style_alias_slots'],choice['object_count'])==(4,32,3)
    assert not choice['label_free2000_controls']
    original=speech+style['records']+choice['records']
    assert len(records)==len(byid)==len(original)==270 and byid.keys()=={r['id'] for r in original}
    for source in original:
        row=byid[source['id']]
        assert all(row[k]==v for k,v in source.items()) and not any(row['review'].values())
        assert row['earlier_English_unconsulted']
    credited={(r['file_path'],r['id']) for r in load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    assert not credited & {(r['file_path'],r['id']) for r in records}
    ordered=sorted(records,key=lambda r:(r['block'],r['source_reference']['offset']))
    OUT.mkdir()
    sealed=OUT/'sealed_drafts.json'
    save(sealed,dict(records=ordered,records_count=270,ordinary_speeches=234,physical_style_alternatives=29,
        style_objects=4,style_alias_slots=32,typed_captions=7,typed_choice_objects=3,control_only_blocks=[231],
        complete_blocks=blocks,source_contexts={k:v for d in drafts for k,v in d['source_contexts'].items()},
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True,no_already_credited_record_keys=True,new_credit=0,
        evidence={str(p):digest(p) for p in (PACKET,STYLES,CHOICES,*DRAFTS,Path(__file__))}))
    shared=dict(all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),no_blanket_prior_English_exposure_claim=True,new_credit=0)
    save(OUT/'current_binding_meanings.json',dict(source_packet=str(PACKET),source_packet_sha256=digest(PACKET),
        records=[{**byid[r['id']],'current_ROM_English_unconsulted':True} for r in speech],meanings=234,**shared))
    for name,object_doc in (('style_meanings',style),('choice_meanings',choice)):
        save(OUT/f'{name}.json',{**object_doc,'records':[byid[r['id']] for r in object_doc['records']],**shared})
    print('Sealed 270 source-first drafts, including all 29 style alternatives and all seven captions.')


if __name__=='__main__':
    main()

