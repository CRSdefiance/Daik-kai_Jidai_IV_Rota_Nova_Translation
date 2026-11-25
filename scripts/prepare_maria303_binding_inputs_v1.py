"""Project the sealed303 drafts into the original speech/menu native binder contracts."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B58_B70_clean_20261109')
def main():
    out=ROOT/'binding_inputs_v1';assert not out.exists()
    original=ROOT/'clean_source_packet.json';sealed=ROOT/'all303_clean_meanings_andindependent_drafts_v3.json'
    choices_path=ROOT/'binding_source_choices_v1.json';packet,doc,choices=map(load,[original,sealed,choices_path])
    assert doc['current_English_not_consulted_for_these303_objects'] and doc['all_drafts_saved_before_current_story_English_intake']
    assert len(doc['records'])==303 and (choices['object_count'],choices['caption_count'])==(2,4)
    source={r['id']:r for g in packet['groups'] for r in g['records']};groups={g['block']:g for g in packet['groups']}
    choice_byid={r['id']:r for r in choices['records']};rows=deepcopy(doc['records'])
    for row in rows:
        before=source[row['id']];group=groups[row['block']]
        assert all(row[k]==before[k] for k in ['id','file_path','block','source_hex','source_Japanese'])
        assert not any(row['review'].values()) and row['english']==row['independent_English_draft']
        row.update(earlier_English_unconsulted=True,current_ROM_English_unconsulted=True,
            source_meaning_pending=False,localized_draft_pending=False,source_first_independent_meaning_saved=True,
            source_read_with_all_previous_andfollowing_speeches_in_block=True,
            independent_draft_precedes_current_English_intake=True,current_English_comparison_pending=True,
            no_blanket_historical_English_unexposure_claim=True)
        if row['source_object_kind']=='ordinary-speech':
            command=next(c for c in group['all_source_commands'] if c['offset']==row['source_command_offset'])
            raw=bytes.fromhex(command['whole_command_hex']);body=bytes.fromhex(row['source_hex'])
            assert command['word']==0x4000 and raw[5:5+len(body)]==body and raw[5+len(body):] in [b'\0',b'\0\0']
            assert len(raw)==command['native_extent'] and raw[:6].hex()==row['source_complete_preamble_hex']
            row.update(kind='ordinary-speech',source_record_index=int(row['id'].rsplit('R',1)[1]),
                source_presentation_kind='source-FE-system-panel' if body[0]==254 else 'source-named-progressive')
        else:
            metadata=choice_byid[row['id']]
            assert row['kind']=='typed-choice-label' and row['source_hex']==metadata['source_hex']
            assert all(row['source_reference'][k]==metadata['source_reference'][k] for k in ['block','command_offset','offset','length'])
            row.update({k:deepcopy(v) for k,v in metadata.items() if k not in ['source_reference','earlier_English_unconsulted','all_five_review_gates_pending','new_credit']})
            row['source_reference']=deepcopy(metadata['source_reference'])
    speech=[r for r in rows if r['kind']=='ordinary-speech'];captions=[r for r in rows if r['kind']=='typed-choice-label']
    assert (len(speech),len(captions))==(299,4)
    for group in packet['groups']:
        group['records']=[r for r in speech if r['block']==group['block']]
        group['clean_block_sha256']=sha(bytes.fromhex(group['clean_block_hex']))
    out.mkdir();projected=out/'clean_source_packet.json';save(projected,packet)
    projection=out/'sealed_drafts.json';save(projection,dict(records=rows,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        original_sealed_drafts=str(sealed),original_sealed_drafts_sha256=digest(sealed),
        source_schema_projection_only_no_meaning_draft_orcontrol_changes=True,new_credit=0))
    save(out/'meanings_view.json',dict(records=speech,meanings=299,source_packet=str(projected),source_packet_sha256=digest(projected),
        all_drafts_sealed=str(projection),all_drafts_sha256=digest(projection),no_blanket_prior_English_exposure_claim=True,new_credit=0))
    for name,records in [('clean_style_objects.json',[]),('clean_choice_objects.json',captions)]:
        save(out/name,dict(records=records,source_packet_sha256=digest(projected),original_source_packet_sha256=digest(original),
            current_English_unconsulted=True,all_drafts_sealed=str(projection),all_drafts_sha256=digest(projection),new_credit=0))
    save(out/'projection_qualification.json',dict(source_objects=303,ordinary_speeches=299,physical_style_alternatives=0,captions=4,
        complete_blocks=10,all_source_commands_retained=True,all303_meanings_anddrafts_unchanged=True,
        no_current_English_yet_extracted=True,all_five_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [original,sealed,choices_path,projected,projection,Path(__file__)]}))
    print('Projected303 sealed drafts:299 speech/zero styles/four captions;allcontrols andprose unchanged,zero credit.')
if __name__=='__main__':main()
