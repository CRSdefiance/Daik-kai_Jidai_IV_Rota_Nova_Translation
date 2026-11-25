"""Seal 292 source-first drafts and scope out the previously integrated B246 block."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.draft_rafael_B249_B260_clean_v1 import ROOT, OUT
from scripts.write_rafael_B221_B240_contextual_v1 import digest

CENSUS = ROOT/'clean_source_census_v2.json'
PACKET = ROOT/'clean_source_packet.json'
OUT = OUT/'sealed_clean_first_v1'
DRAFTS = (ROOT/'B241_B244_clean_drafts_v1.json', ROOT/'B245_B248_clean_drafts_v1.json', *[
    OUT.parent/f'rafael_{part}_clean_drafts_v1.json' for part in ('B249_B252','B253_B256','B257_B260')
])
BLOCKS = [block for block in range(241,261) if block != 246]


def main():
    assert not OUT.exists()
    packet, census, style, choice = map(load, (PACKET,CENSUS,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json'))
    assert census['new_eligible_objects'] == 292 and census['prior_reviewed_records'] == 18
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert style['source_packet_sha256'] == choice['source_packet_sha256'] == digest(PACKET)
    drafts = list(map(load, DRAFTS))
    assert [doc['records_count'] for doc in drafts] == [50,44,98,62,38]
    assert [block for doc in drafts for block in doc['complete_blocks']] == BLOCKS
    assert all(doc['no_current_English_extracted_for_this_intake_before_drafts'] and doc['all_five_gates_pending'] for doc in drafts)
    assert all(digest(Path(path)) == checksum for doc in drafts for path,checksum in doc['evidence'].items())
    groups = [group for group in packet['groups'] if group['block'] in BLOCKS]
    speech = [row for group in groups for row in group['records']]
    original = speech + style['records'] + choice['records']
    assert (len(speech),len(style['records']),len(choice['records'])) == (272,14,6)
    records = [row for doc in drafts for row in doc['records']]
    by_id = {row['id']:row for row in records}
    assert len(records) == len(by_id) == len(original) == 292
    for source in original:
        row = by_id[source['id']]
        assert all(row[key] == value for key,value in source.items()) and not any(row['review'].values())
        assert row['earlier_English_unconsulted']
    ledger = load('translations/editorial_review_current_v1.json')['contextual_story_natural_dialogue_pass_v1871']
    credited = {(row['file_path'],row['id']) for row in ledger['integrated_record_keys']}
    assert not credited & {(row['file_path'],row['id']) for row in records}
    OUT.mkdir()
    scoped = OUT/'scoped_clean_packet.json'
    save(scoped,{**packet,'groups':groups,'records':272,'prior_reviewed_context_only_blocks':[246],
        'original_clean_packet':str(PACKET),'original_clean_packet_sha256':digest(PACKET)})
    sealed = OUT/'sealed_drafts.json'
    save(sealed,dict(records=sorted(records,key=lambda row:(row['block'],row['source_reference']['offset'])),
        records_count=292,ordinary_speeches=272,physical_style_alternatives=14,style_objects=2,style_alias_slots=16,
        typed_captions=6,typed_choice_objects=3,control_only_blocks=[244],complete_blocks=BLOCKS,
        source_contexts={k:v for doc in drafts for k,v in doc['source_contexts'].items()},
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True,no_already_credited_record_keys=True,new_credit=0,
        evidence={str(path):digest(path) for path in (PACKET,CENSUS,*DRAFTS,scoped,Path(__file__))}))
    common = dict(source_packet=str(scoped),source_packet_sha256=digest(scoped),all_drafts_sealed=str(sealed),
                  all_drafts_sha256=digest(sealed),no_blanket_prior_English_exposure_claim=True,new_credit=0)
    save(OUT/'current_binding_meanings.json',dict(records=[
        {**by_id[row['id']],'current_ROM_English_unconsulted':True} for row in speech],meanings=272,**common))
    for key, doc in (('style_meanings',style),('choice_meanings',choice)):
        save(OUT/f'{key}.json',{**doc,**common,'records':[by_id[row['id']] for row in doc['records']]})
    print('Sealed 292 source-first drafts before consulting Rafael3222 English. The 18 B246 records remain context only.')


if __name__ == '__main__':
    main()

