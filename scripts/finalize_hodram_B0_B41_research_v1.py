"""Seal394 exact individual reviews and three owned fields after display/storage/gameplay checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107');OUT=ROOT/'research_final_v1'
PROSE=Path('translations/hodram_B0_B41_contextual_review_v3.json')
FINAL=Path('translations/hodram_B0_B41_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B0_B41_scoped_names_final_v1.json')
FINAL_FIELDS=Path('translations/hodram_B0_B41_owned_surnames_final_v1.json')
READY=OUT/'research_completion.json'
GATES=['source','context','localization','naturalness','formatting']

def main():
    assert not any(p.exists() for p in [OUT,FINAL,FINAL_NAMES,FINAL_FIELDS])
    paths=dict(rebuilt=ROOT/'stored_reconstruction_v3/reconstruction.json',stored=ROOT/'stored_v2/stored_native_verification.json',
        catalogue=ROOT/'stored_catalogue_all_v2/all388_stored_effective_body_bindings.json',loaders=ROOT/'loaders_v2/verification.json',
        visual=ROOT/'offline_visual_approval_v2.json',actual=ROOT/'gameplay_review_v1.json',
        names=ROOT/'scoped_names_formatting_review_v1.json',name_native=ROOT/'name_field_checks_v1/native_name_fields_verification.json',
        name_visual=ROOT/'name_field_visual_approval_v1.json',name_proposal=ROOT/'name_field_inputs_v1/owned_fields_proposal.json',
        mixed=ROOT/'mixed_research_v2/research_reference.json',roles=ROOT/'role_bindings_v1.json',terms=ROOT/'scoped_terms_v1.json')
    data={k:load(p) for k,p in paths.items()};rebuilt=data['rebuilt'];actual=data['actual'];stored=data['stored']
    doc,plan,native,styles,menus=map(load,[rebuilt[k] for k in ['manuscript','plan','native','styles','menu']])
    prose=load(PROSE);byprose={r['id']:r for r in prose['records']}
    assert len(doc['records'])==394 and prose['counts']==dict(revision=221,retention=173)
    assert all(r['english']==byprose[r['id']]['english'] and r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert native['manuscript_sha256']==styles['manuscript_sha256']==menus['manuscript_sha256']==digest(rebuilt['manuscript'])
    assert native['plan_sha256']==styles['plan_sha256']==digest(rebuilt['plan'])
    assert native['runtime']==stored['runtime']==styles['runtime']==menus['runtime']==data['roles']['runtime']==data['terms']['runtime']
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert not plan['failures'] and not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert data['visual']['final_all389_pages_directly_viewed_or_exact_reused'] and data['visual']['additional_final_native_page_directly_viewed']
    assert data['visual']['visual_wrap_corrections']==5 and data['visual']['all42_scoped_planned_names_native_andvisually_checked']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(389,1,388,685)
    assert len(stored['exact_stored_speech_records_reused'])==340
    assert stored['reconstruction_sha256']==data['loaders']['reconstruction_sha256']==digest(paths['rebuilt'])
    assert data['catalogue']['stored_sha256']==digest(paths['stored']) and data['catalogue']['all388_ordinary_and_style_bodies_checked']
    assert (data['loaders']['fresh_whole_archive_loads_andcache_hits'],data['loaders']['fresh_parent_cases'],data['loaders']['exact_reused_parent_cases'])==(325,2,648)
    assert (actual['frames'],actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])==(57363,169,170,219)
    assert actual['all170_broad_pages_three_corrected_headers_andfinal_wrap_directly_viewed'] and actual['all_three_final_resupply_returns_directly_viewed']
    assert actual['all_three_native_menus_default_selection_andordinary_A_returns_observed'] and actual['all_three_changed_progressive_names_observed_complete']
    for p,h in actual['evidence'].items():assert digest(p)==h
    assert data['mixed']['complete_registered_parent_inverse_exact'] and digest(data['mixed']['research_ROM'])==data['mixed']['research_ROM_sha256']
    assert data['name_visual']['all12_current_andproposed_planes_directly_viewed'] and data['name_native']['proposal_sha256']==digest(paths['name_proposal'])
    assert len(data['name_native']['negative_cases_rejected'])==8 and data['name_native']['name_data_plan']['changed_bytes']==28
    archive=Path(rebuilt['target_archive']).read_bytes();assert digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    blocks=IlnkContainer.parse(archive).blocks
    bodies={r['id']:r for r in stored['records']+stored['style_records']};captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans={r['id']:r for r in plan['records']};seen={r['id'] for r in actual['final_observed_samples']}
    assert len(bodies)==388 and len(captions)==6 and len(seen)==169
    OUT.mkdir()
    for row in doc['records']:
        ident=row['id'];block=blocks[row['block']]
        if ident in bodies:
            item=bodies[ident];at=item['new_offset'];raw=bytes.fromhex(item['stored_hex'])
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=item['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            if row.get('native_object_kind')=='4100-style-alternative':
                header=bytes.fromhex(item['final_header_hex']);assert block[item['final_command_offset']:item['final_command_offset']+len(header)]==header
                ref.update(command_offset=item['final_command_offset'],source_style_indices=item['source_style_indices'],exact_command_header_hex=item['final_header_hex'],virtual_prefix_not_stored=True)
            else:
                assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];ref['header_offset']=at-5
            row['planned_English_markup']=plans[ident]['formatted_markup']
            row['actual_utterance_observed_in_disclosed_fixture']=ident in seen
        else:
            obj,item=captions[ident];at=item['offset'];raw=bytes.fromhex(item['stored_hex']);assert raw.decode('ascii')==row['english']
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],source_index=item['source_index'],record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            row['actual_caption_display_observed_in_disclosed_fixture']=True
        assert block[at:at+len(raw)+1]==raw+b'\0'
        row.update(planned_integrated_reference=ref,registered_release_andcompletion_credit_pending=True,
            fresh_formatting_binding_pending=False,fresh_display_stored_gameplay_andregistered_integration_pending=False,new_credit=0)
        row['review']['formatting']=True
        row['review_evidence']=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(paths['actual']),
            coverage='observed-disclosed-QA' if ident in seen or ident in captions else 'offline-native-andstored-only')
    doc.update(encoder='dialogue-relocatable-v1',review_gates=GATES,all_individual_five_gates_pass=True,all394_individual_five_gates_pass=True,
        formatting_gate_pending=False,all_fifth_formatting_gates_pending=False,
        actual_source_speech_variants=169,actual_body_pages=170,offline_only_source_speech_variants=219,
        native_body_pages=389,registered_release_andcompletion_credit_pending=True,
        parent_manuscript=rebuilt['manuscript'],parent_manuscript_sha256=digest(rebuilt['manuscript']),new_credit=0,full_goal_complete=False)
    validate_natural_dialogue_batch(doc);save(FINAL,doc)
    names=deepcopy(data['names']);observed={h['expected_actor_ID'] for h in actual['name_headers']}
    for row in names['records']:
        assert all(row['review'][g] for g in GATES[:-1]);row['review']['formatting']=True
        row['actual_changed_header_observed']=row['actor_ID'] in observed
        row['full_catalogue_UI_unvisited']=True
    names.update(encoder='dialogue-relocatable-v1',review_gates=GATES,all42_individual_five_gates_pass=True,actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names);save(FINAL_NAMES,names)
    versions={v['version']:v['names']['rows'] for v in data['name_native']['versions']};byactor={r['actor_ID']:r for r in names['records']}
    fields=[]
    for field in data['name_proposal']['fields']:
        row=deepcopy(byactor[field['actor']]);full=next(r['text'] for r in versions['proposed'] if r['actor_ID']==field['actor'] and r['consumer']=='full-catalogue')
        row.update(id='ACTOR'+str(field['actor'])+'_OWNED_SURNAME',english=full,owned_field=field,full_catalogue_UI_unvisited=True)
        fields.append(row)
    fielddoc=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=GATES,
        records=fields,all3_owned_fields_five_gates_pass=True,new_credit=0)
    validate_natural_dialogue_batch(fielddoc);save(FINAL_FIELDS,fielddoc)
    native_names=deepcopy(data['name_native']);native_names.update(offline_visual_approved=True,direct_view_pending=False,
        direct_visual_approval=str(paths['name_visual']),direct_visual_approval_sha256=digest(paths['name_visual']),actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    save(OUT/'owned_surnames_native_approved.json',native_names)
    plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL));save(OUT/'release_plans.json',plan)
    save(READY,dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),all_individual_five_gates_pass=True,
        records=394,revisions=221,retentions=173,body_pages=389,typed_labels=6,scoped_names=42,
        owned_surname_fields=3,owned_name_bytes=28,actual_source_variants=169,actual_pages=170,offline_only_source_variants=219,
        actual_runs=3,actual_frames=57363,actual_menus=3,registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),PROSE,FINAL,FINAL_NAMES,FINAL_FIELDS,OUT/'owned_surnames_native_approved.json',Path(__file__)]}))
    print('Sealed394 five-gate story reviews,42 names andthree owned surnames;169 observed variants/219 offline-only. Registered integration remains;zero credit.')

if __name__=='__main__':main()
