"""Seal the301 individual reviews after exact offline, stored andrepresentative checks."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'research_final_v1'
FINAL = Path('translations/maria_B0_B32_final_review_v1.json')
FINAL_NAMES = Path('translations/maria_B0_B32_scoped_names_final_v1.json')
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']


def main():
    assert not any(p.exists() for p in [OUT, FINAL, FINAL_NAMES])
    paths = dict(rebuilt=ROOT/'stored_reconstruction_v1/reconstruction.json',
        stored=ROOT/'stored_v1/stored_native_verification.json',
        catalogue=ROOT/'stored_catalogue_all_v1/all299_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json', visual=ROOT/'offline_display_approval_v1.json',
        actual=ROOT/'gameplay_review_v1.json', names=ROOT/'scoped36_name_editorial_review_v2.json',
        name_planes=ROOT/'name_planes_v1/native_name_planes.json',
        roles=ROOT/'formatting_v1/role_bindings.json', terms=ROOT/'scoped_terms_v1.json',
        prose=Path('translations/maria_B0_B32_contextual_review_v1.json'))
    data = {k:load(p) for k,p in paths.items()}
    rebuilt, stored, actual = [data[k] for k in ['rebuilt','stored','actual']]
    doc, plan, native, menus, styles = map(load, [rebuilt[k] for k in ['manuscript','plan','native','menu','styles']])
    original_doc = deepcopy(doc)
    byprose = {r['id']:r for r in data['prose']['records']}
    assert len(doc['records']) == len(byprose) == 301
    assert (data['prose']['proposed_revisions'],data['prose']['justified_retentions']) == (178,123)
    for row in doc['records']:
        prose = byprose[row['id']]
        unmarked = re.sub(r'\{MACRO:([A-Z]{2})\}',lambda m:m[1],row['english'])
        assert unmarked == prose['english']
        assert row['source_hex'] == prose['source_hex'] and row['current_hex'] == prose['current_hex']
        assert row['decision'] == prose['decision'] and row['finding'] == prose['finding']
        assert row['review'] == dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == menus['manuscript_sha256'] == digest(rebuilt['manuscript'])
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(rebuilt['plan'])
    assert native['runtime'] == stored['runtime'] == styles['runtime'] == menus['runtime'] == data['name_planes']['runtime'] == data['roles']['runtime'] == data['terms']['runtime']
    pending = [native]; checked_receipts = set()
    while pending:
        receipt = pending.pop()
        assert receipt['runtime'] == native['runtime'] and receipt['font_sha256'] == native['font_sha256']
        if 'all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass' in receipt:
            assert receipt['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and receipt['complete_consumption_andpagination_exact']
        else:
            assert receipt['all_records_native_checked_once_or_exact_compiled_dependency_reuse']
            for key in ['previous_native','fresh_native']:
                p = receipt[key]
                assert digest(p) == receipt[key+'_sha256']
                if p not in checked_receipts:
                    checked_receipts.add(p); pending.append(load(p))
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert data['visual']['every_final_page_directly_viewed_in_readable_sheets']
    assert data['visual']['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']
    assert (native['pages'],stored['complete_stored_pages'],stored['fresh_relocated_native_relative_cases']) == (303,303,635)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['reconstruction_sha256'] == data['loaders']['reconstruction_sha256'] == digest(paths['rebuilt'])
    assert data['catalogue']['stored_sha256'] == digest(paths['stored']) and data['catalogue']['all299_ordinary_and_style_bodies_checked']
    assert (data['loaders']['fresh_whole_archive_loads_andcache_hits'],data['loaders']['fresh_parent_cases']) == (303,606)
    assert (actual['frames'],actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances']) == (42683,92,96,207)
    assert actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed'] and actual['all_four_two_page_transitions_observed']
    assert actual['ordinary_default_menu_return_to_next_fixture_speech_observed']
    assert actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']
    assert actual['reclaimed_one_page_Havana_paragraph_observed'] and actual['corrected_B14_I_glyph_observed']
    assert styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8
    assert sum(len(x['rejected']) for x in styles['compiler_negatives']) == 9
    assert len(menus['menus']) == 1 and stored['typed_labels_checked'] == 2
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    for collection in [data['visual']['evidence'],actual['evidence']]:
        for p,h in collection.items():assert digest(p) == h
    archive = Path(rebuilt['target_archive']).read_bytes()
    assert digest(rebuilt['target_archive']) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(archive).blocks
    bodies = {r['id']:r for r in stored['records']+stored['style_records']}
    captions = {r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans = {r['id']:r for r in plan['records']}
    seen = set(bodies)-set(actual['unvisited_source_IDs'])
    assert (len(bodies),len(captions),len(seen)) == (299,2,92)
    for row in doc['records']:
        ident = row['id']; block = blocks[row['block']]
        if ident in bodies:
            item = bodies[ident]; at = item['new_offset']; raw = bytes.fromhex(item['stored_hex'])
            ref = dict(file_path=row['file_path'],block=row['block'],offset=at,
                record_index=item['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            if row.get('native_object_kind') == '4100-style-alternative':
                header = bytes.fromhex(item['final_header_hex'])
                assert block[item['final_command_offset']:item['final_command_offset']+len(header)] == header
                ref.update(command_offset=item['final_command_offset'],source_style_indices=item['source_style_indices'],
                    exact_command_header_hex=item['final_header_hex'],virtual_prefix_not_stored=True)
            else:
                assert block[at-5:at+1].hex() == row['source_complete_preamble_hex']
                ref['header_offset'] = at-5
            row['planned_English_markup'] = plans[ident]['formatted_markup']
            row['actual_utterance_observed_in_disclosed_fixture'] = ident in seen
        else:
            obj,item = captions[ident]; at = item['offset']; raw = bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii') == row['english']
            ref = dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],
                source_index=item['source_index'],record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            row['actual_caption_display_observed_in_disclosed_fixture'] = True
        assert block[at:at+len(raw)+1] == raw+b'\0'
        row['review']['formatting'] = True
        row.update(planned_integrated_reference=ref, fresh_formatting_binding_pending=False,
            registered_release_andcompletion_credit_pending=True, new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(paths['actual']),
                coverage='observed-disclosed-QA' if ident in seen or ident in captions else 'offline-native-andstored-only'))
    doc.update(encoder='dialogue-relocatable-v1',review_gates=GATES,
        all_individual_five_gates_pass=True,all301_individual_five_gates_pass=True,
        all_fifth_formatting_gates_pending=False,all_fifth_gates_still_false=False,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=False,
        actual_source_speech_variants=92,actual_body_pages=96,offline_only_source_speech_variants=207,
        native_body_pages=303,registered_release_andcompletion_credit_pending=True,
        parent_manuscript=rebuilt['manuscript'],parent_manuscript_sha256=digest(rebuilt['manuscript']),
        new_credit=0,full_goal_complete=False)
    assert all(before['english']==after['english'] and before['finding']==after['finding'] for before,after in zip(original_doc['records'],doc['records'],strict=True))
    validate_natural_dialogue_batch(doc)
    names = deepcopy(data['names']); observed = {h['expected_actor_ID'] for h in actual['name_headers']}
    plane_texts = {p['text'] for p in data['name_planes']['planes']}
    for row in names['records']:
        assert all(row['review'][g] for g in GATES[:-1]) and not row['review']['formatting']
        public = next(c['text'] for c in row['current_consumers'] if c['consumer']=='progressive-nameplate')
        assert all(c['text'] in plane_texts for c in row['current_consumers'])
        row.update(id='ACTOR'+str(row['actor_ID'])+'_MARIA_SCOPED_NAME',english=public,
            speaker='Source actor '+str(row['actor_ID']),
            context='Source-bound name/role in the reviewed SC3 references: '+', '.join(row['context_record_ids']),
            source_meaning='The recorded clean Japanese name components identify this source actor. '+row['finding'],
            actual_progressive_header_observed_in_disclosed_fixture=row['actor_ID'] in observed,
            full_catalogue_UI_layout_unvisited=True,full_catalogue_string_font_only_not_UI_layout_approval=True,
            final_font_complete_glyph_bounds_andrepresentative_display_checks_pending=False,
            name_localization_andfresh_display_approval_pending=False)
        row['review']['formatting'] = True
    names.update(encoder='dialogue-relocatable-v1',review_gates=GATES,
        all36_individual_five_gates_pass_in_scoped_context=True,
        all_name_formatting_gates_pending=False,full_catalogue_UI_andfuture_role_assignments_unvisited=True,
        actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names)
    OUT.mkdir(); save(FINAL,doc); save(FINAL_NAMES,names)
    plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL))
    release_plan = OUT/'release_plans.json'; save(release_plan,plan)
    save(OUT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),
        all_individual_five_gates_pass=True,records=301,revisions=178,retentions=123,
        body_pages=303,typed_labels=2,scoped_names=36,wrap_improvements=35,layout_retentions=2,
        actual_source_variants=92,actual_pages=96,offline_only_source_variants=207,
        actual_runs=3,actual_frames=42683,actual_menus=1,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),FINAL,FINAL_NAMES,release_plan,Path(__file__)]}))
    print('Sealed301 five-gate reviews and36 scoped names;178 revisions/123 retentions. Registered integration andonce-only credit remain.')


if __name__ == '__main__':
    main()
