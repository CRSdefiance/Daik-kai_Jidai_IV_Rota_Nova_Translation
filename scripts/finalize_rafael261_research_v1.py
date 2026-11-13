"""Seal261 five-gate reviews with exact storage and honest representative gameplay scope."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael261_checked_20261105')
REBUILD = Path('work/analysis/Rafael261_rebased678_20261105/reconstruction.json')
STORED = Path('work/analysis/Rafael261_stored_native_20261105/stored_native_verification.json')
LOOKUP = Path('work/analysis/Rafael261_stored_catalogue_20261105/all_stored_effective_body_bindings.json')
LOADERS = Path('work/analysis/Rafael261_loaders_20261105/verification.json')
NAMES = Path('work/analysis/Rafael261_scoped_name_planes_v2_20261105/native_name_planes.json')
NAME_VISUAL = NAMES.with_name('direct_visual_approval.json')
BODY = Path('work/analysis/Rafael261_names_pages_actual_pixels_v1_20261105/focused_actual_pixels.json')
MENU_BODY = Path('work/analysis/Rafael261_menus_body_actual_pixels_v1_20261105/focused_actual_pixels.json')
MENU_PIXELS = Path('work/analysis/Rafael261_menus_actual_pixels_v1_20261105/menu_actual_pixels.json')
CONTACTS = Path('work/analysis/Rafael261_actual_compact_sheets_20261105/receipt.json')
FINAL = Path('translations/rafael_B85_B100_contextual_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B85_B100_scoped_names_final_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not FINAL_NAMES.exists()
    rebuilt, stored, lookup, loaders, names, name_visual, body, menu_body, menu_pixels, contacts = map(load,
        [REBUILD, STORED, LOOKUP, LOADERS, NAMES, NAME_VISUAL, BODY, MENU_BODY, MENU_PIXELS, CONTACTS])
    doc, plan, native, menu = map(load, [rebuilt['manuscript'], rebuilt['plan'], rebuilt['native'], rebuilt['menu']])
    assert len(doc['records']) == 261 and doc['four_gate_passes'] == 261 and not doc['pending_name_term_IDs']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert (len(stored['records']), stored['complete_stored_pages'], stored['fresh_relocated_native_relative_cases']) == (255, 256, 300)
    assert stored['reconstruction_sha256'] == sha(REBUILD.read_bytes()) and stored['native_sha256'] == sha(Path(rebuilt['native']).read_bytes())
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert len(lookup['records']) == 255 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'], loaders['exact_reused_parent_cases']) == (343, 22, 664)
    assert name_visual['all18_complete_public_name_planes_approved'] and name_visual['scoped_actors'] == 20
    assert names['runtime'] == stored['runtime'] == menu['runtime']
    for actual in [body, menu_body]:
        assert actual['all_selected_pages_observed_in_exact_fixture_order'] and actual['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert (body['selected_utterances'], body['selected_pages'], menu_body['selected_utterances'], menu_body['selected_pages']) == (38,39,6,6)
    assert menu_pixels['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert {(m['source_command_offset'], tuple(m['observed_selected_options'])) for m in menu_pixels['menus']} == {(80,(0,1)),(814,(0,1)),(110,(0,1))}
    sourceids = {r['id'] for a in [body,menu_body] for r in a['body_pages']}
    pageids = {(r['id'],r['page']) for a in [body,menu_body] for r in a['body_pages']}
    actors = {r['actor_ID'] for a in [body,menu_body] for r in a['headers']}
    assert (len(sourceids),len(pageids),len(actors)) == (43,44,16)
    assert {12,13,18,20,26,41,108,109,114,151,152,158} <= actors
    assert {('DK4_MES_B86_R0075',1),('DK4_MES_B86_R0075',2)} <= pageids
    assert all(f'DK4_MES_B90_R{n:04d}' in sourceids for n in [5,9,14,18,23,27,32,35,40,43])
    for receipt in [contacts]:
        for sheet in receipt['bottom_screen_sheets']+receipt['full_scene_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert len(contacts['bottom_screen_sheets']) == 4 and len(contacts['full_scene_sheets']) == 1
    for sheet in [*menu_body['review_sheets'], menu_pixels['review_sheet']]:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    ROOT.mkdir()
    visual_path = ROOT/'complete_visual_approval.json'
    save(visual_path, dict(body_pages=256, all256_final_pages_directly_viewed_or_exact_native_plane_reuse=True,
        all6_labels_and24_current_reviewed_caption_style_planes_checked=True, all18_scoped_nameplanes_viewed=True,
        actual_four_compact_body_sheets_one_full_context_sheet_one_menu_body_sheet_andone_cursor_sheet_directly_viewed=True,
        body_native_proof=rebuilt['native'], body_native_proof_sha256=sha(Path(rebuilt['native']).read_bytes()),
        native_body_visual='work/analysis/Rafael261_native_final_v4_20261105/direct_visual_approval.json',
        native_menu_visual=rebuilt['menu'], native_menu_visual_sha256=sha(Path(rebuilt['menu']).read_bytes()),
        name_visual=str(NAME_VISUAL), name_visual_sha256=sha(NAME_VISUAL.read_bytes()),
        actual_contacts=str(CONTACTS), actual_contacts_sha256=sha(CONTACTS.read_bytes()), all_prose_retained=True,
        actual_review_retention_note='The ten-speech Janus exchange and the payer correction read naturally in sequence. The former sailor deliberately questions belief before his later shipwreck contrast and apology; preserve that source-defined shift rather than smoothing away his characterization.',
        new_credit=0, guide_photos=False))
    actual_path = ROOT/'actual_review.json'
    save(actual_path, dict(total_frames=20722, initialized_fixture_runs=2, source_speeches_observed=43,
        native_body_pages_observed=44, actual_choice_labels=6, source_editorial_objects_observed=49,
        offline_only_source_speeches=212, source_IDs_observed=sorted(sourceids), actual_actor_IDs=sorted(actors),
        complete_body_holds=103, complete_header_holds=97,
        all12_newly_scoped_identities_andthree_distinct_Sailor_portraits_observed=True,
        all_three_native_menus_both_cursor_states_andA_to_following_dialogue_observed=True,
        full_Janus_ten_speech_conversation_payer_exchange_andtwo_page_sentence_transition_observed=True,
        FE_FI_notices_animal_cry_andnormal_ASCII_I_questionmarks_observed=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        original_story_branches_numeric_return_registers_stat_effects_andcancellation_unvisited=True,
        initialized_copy_of_native_commands_not_original_event_activation=True,
        body_proofs=[str(BODY),str(MENU_BODY)], menu_proofs=[str(MENU_PIXELS)], new_credit=0, guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [BODY,MENU_BODY,MENU_PIXELS,CONTACTS,visual_path]}))
    name_doc = deepcopy(load('translations/rafael_B85_B100_scoped_names_androles_v1.json'))
    for row in name_doc['records']:
        row['review']['formatting'] = True
        row.update(actual_header_observed_in_current_fixture=row['actor_ID'] in actors,
            public_style11_native_plane_andrepresentative_actual_header_checks_pass=True)
    name_doc.update(all20_name_planes_andrepresentative_actual_headers_pending=False, all_five_gates_pass_in_scoped_context=True,
        actual_actor_IDs_observed=sorted(actors), actual_actor_IDs_unvisited_in_current_batch=sorted(set(names['actors'][i]['actor_ID'] for i in range(len(names['actors'])))-actors),
        actual_headers_observed=True, actual_header_scope='16 current actors including all12 newly scoped identities;four other public names retain exact qualified earlier proofs. Full catalogue UI andglobal207 review remain open.',
        native_name_planes=str(NAMES), native_name_planes_sha256=sha(NAMES.read_bytes()), native_visual=str(NAME_VISUAL), native_visual_sha256=sha(NAME_VISUAL.read_bytes()),
        actual_review=str(actual_path), actual_review_sha256=sha(actual_path.read_bytes()))
    validate_natural_dialogue_batch(name_doc)
    save(FINAL_NAMES, name_doc)
    groups = {g['block']:g for g in rebuilt['groups']}
    text_records = {t['id']:t for g in rebuilt['groups'] for t in g['text_records']}
    planned = {r['id']:r for r in plan['records']}
    target = NdsImage.open(rebuilt['research_ROM']).read_file(doc['file_path'])
    assert sha(target) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(target).blocks
    for row in doc['records']:
        if row['kind'] in ['progressive','system-FE']:
            text = text_records[row['id']]
            at = text['new_offset']
            raw = bytes.fromhex(text['stored_hex'])
            ref = dict(file_path=row['file_path'],block=row['block'],offset=at,header_offset=at-5,
                record_index=text['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(target))
            assert blocks[row['block']][at-5:at+1].hex() == row['source_complete_preamble_hex']
            row['planned_English_markup'] = planned[row['id']]['formatted_markup']
            row['actual_utterance_observed_in_disclosed_fixture'] = row['id'] in sourceids
        else:
            obj = next(o for o in groups[row['block']]['native_objects'] if any(r['id']==row['id'] for r in o['records']))
            complete = bytes.fromhex(obj['compiled_hex'])
            count, base = count_and_base(complete)
            assert count == 2 and row['source_index'] < count
            relative = struct.unpack_from('<H',complete,2+2*row['source_index'])[0]
            at = obj['new_offset']+base+relative
            raw = complete[base+relative:].split(b'\0')[0]
            assert raw.decode('ascii') == row['english']
            ref = dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['new_offset'],
                source_index=row['source_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(target))
            row['actual_caption_andboth_cursor_states_observed'] = True
        assert blocks[row['block']][at:at+len(raw)+1] == raw+b'\0'
        row.update(planned_integrated_reference=ref, current_English_comparison_pending=False,
            source_context_localization_formatting_gates_pending=False, native_name_controls_andfresh_formatting_pending=False,
            native_name_controls_andfresh_display_pending=False, all_fresh_display_andregistered_integration_pending=False,
            registered_release_andcompletion_credit_pending=True, new_credit=0)
        row['review']['formatting'] = True
    doc.update(all_fifth_formatting_gates_pending=False, all_native_visual_stored_gameplay_andregistered_integration_pending=False,
        all261_individual_five_gates_pass=True, source_editorial_objects=261, source_speeches=255, typed_choice_labels=6,
        native_body_pages=256, actual_source_speeches=43, actual_body_pages=44, offline_only_source_speeches=212,
        scoped_name_review=str(FINAL_NAMES), scoped_name_review_sha256=sha(FINAL_NAMES.read_bytes()),
        parent_manuscript=rebuilt['manuscript'], parent_manuscript_sha256=rebuilt['manuscript_sha256'],
        formatting_evidence=dict(native=rebuilt['native'],stored=str(STORED),lookup=str(LOOKUP),loaders=str(LOADERS),
            visual=str(visual_path),actual=str(actual_path)), registered_release_andcompletion_credit_pending=True)
    validate_natural_dialogue_batch(doc)
    assert (sum(r['decision']=='revision' for r in doc['records']),sum(r['decision']=='retention' for r in doc['records'])) == (111,150)
    save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()), exact_all_prose_andcompiled_bytes_unchanged=True)
    save(ROOT/'release_plans.json',plan)
    save(ROOT/'research_completion.json',dict(manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),all261_individual_five_gates_pass=True,
        revisions=111,retentions=150,body_pages=256,typed_labels=6,scoped_names=20,new_credit=0,registered_integration_pending=True,main_unchanged=True,
        evidence={str(p):sha(p.read_bytes()) for p in [FINAL,FINAL_NAMES,REBUILD,STORED,LOOKUP,LOADERS,NAMES,NAME_VISUAL,BODY,MENU_BODY,MENU_PIXELS,CONTACTS,visual_path,actual_path,Path(__file__)]}))
    print('261 five-gate research reviews sealed:111 revisions/150 retentions,256 body pages/six captions/20 names;43 speeches+six choices observed,212 speeches offline-only. Registered integration pending;no credit.')
