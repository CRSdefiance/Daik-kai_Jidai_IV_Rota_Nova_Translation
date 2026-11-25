"""Seal the reviewed storage and representative gameplay evidence for registration."""
from collections import Counter
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts.check_rafael_B261_B280_retained_name_planes_v1 import NAMES, RETAINED
from scripts.checkpoint_rafael_B261_B280_display_v1 import NATIVE, PLAN
from scripts.prepare_rafael_B261_B280_actual_v1 import NAME_PROOF, PROPOSAL
from scripts.rebuild_rafael_B261_B280_reviewed_v1 import COMPOUNDS, MENU, VISUAL
from scripts.write_rafael_B261_B280_contextual_v1 import ROOT, load, save, sha
from scripts.finish_rafael_B261_B280_native_pages_v1 import MANUSCRIPT, digest


REBUILT = ROOT/'rebuilt_v1/reconstruction.json'
STORED = ROOT/'stored_v2/stored_native_verification.json'
LOOKUP = ROOT/'stored_catalogue_all_v1/all130_stored_effective_body_bindings.json'
LOADERS = ROOT/'loaders_v1/verification.json'
FIXTURE = ROOT/'fixtures_v1/rafael_puzzles_town_and_bounties_fixture.json'
TERMINAL = ROOT/'actual_run_v1/terminal.json'
LIVE = ROOT/'actual_body_v1/focused_actual_pixels.json'
LIVE_MENUS = ROOT/'actual_menus_v1/menu_actual_pixels.json'
RESEARCH = ROOT/'research_final_v1'
READY = RESEARCH/'research_completion.json'
FINAL = Path('translations/rafael_B261_B280_final_review_v1.json')
FINAL_NAMES = Path('translations/rafael_B261_B280_scoped_names_final_v1.json')


def main():
    assert not any(path.exists() for path in (RESEARCH, FINAL, FINAL_NAMES))
    paths = (REBUILT, STORED, LOOKUP, LOADERS, FIXTURE, TERMINAL, LIVE, LIVE_MENUS,
             MANUSCRIPT, PLAN, NATIVE, MENU, COMPOUNDS, VISUAL, NAMES, RETAINED, NAME_PROOF, PROPOSAL)
    rebuilt, stored, lookup, loaders, fixture, terminal, live, live_menus, doc, plan, native, menu, styles, visual, names, retained, corrected, proposal = map(load, paths)
    assert stored['reconstruction_sha256'] == loaders['reconstruction_sha256'] == digest(REBUILT)
    assert stored['native_sha256'] == rebuilt['native_sha256'] == digest(NATIVE)
    assert lookup['stored_sha256'] == digest(STORED)
    assert stored['runtime'] == lookup['runtime'] == native['runtime'] == proposal['runtime']
    assert lookup['all130_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'],
            stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (131, 47, 84, 390)
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'],
            loaders['exact_reused_parent_cases']) == (343, 40, 646)
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert rebuilt['changed_blocks'] == list(range(261, 281)) and rebuilt['relative_sites'] == 78
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    assert digest(rebuilt['target_archive']) == rebuilt['target_archive_sha256']
    blocks = IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    speech = {row['id']: row for row in stored['records'] + stored['style_records']}
    layouts = {row['id']: row for row in plan['records']}
    assert len(speech) == len(layouts) == 130 and speech.keys() == layouts.keys() == {row['id'] for row in lookup['records']}
    captions = {row['id']: (item, row) for item in stored['typed_objects'] for row in item['label_references']}
    assert len(captions) == 5 and len(menu['menus']) == len(live_menus['menus']) == 2
    assert styles['native_target_slot_cases'] == 16 and len(styles['objects']) == 2
    assert live['evidence'][str(FIXTURE)] == digest(FIXTURE) and live['evidence'][str(TERMINAL)] == digest(TERMINAL)
    assert live_menus['body_proof_sha256'] == digest(LIVE)
    assert live['all_selected_pages_observed_in_exact_fixture_order']
    assert live['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert live_menus['ordinary_A_return_to_next_fixture_speech_observed']
    assert live_menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert [row['observed_selected_options'] for row in live_menus['menus']] == [[0], [0]]
    assert not live['complete_scene_commands_retained'] and not live['natural_activation']
    assert (live['frames'], live['selected_utterances'], live['selected_pages']) == (15761, 42, 43)
    assert {row['text'] for row in live['headers'] if row['expected_actor_ID'] == 68} == {'Jacob Portunto'}
    assert fixture['proposed_surname_fields_applied'] and fixture['surname_proof_sha256'] == digest(NAME_PROOF)
    assert corrected['proposal_sha256'] == digest(PROPOSAL) and corrected['original_progressive_andfull_name_getters_pass']
    assert {(row['actor_ID'], row['text']) for row in corrected['versions'][1]['names']['rows']} == {
        (65, 'Plett Perrault'), (68, 'Jacob Portunto')}
    capture = Path(terminal['report'])
    assert digest(capture) == terminal['report_sha256']
    report = load(capture)
    snapshot = report['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert snapshot['read_only_export'] and sha(ram) == snapshot['sha256']
    arm = Path(corrected['proposed_ARM9']).read_bytes()
    assert sha(arm) == corrected['versions'][1]['ARM9_sha256']
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and ram[POOL-BASE:POOL-BASE+len(payload)] == payload
    assert ram[1184676:1184680] == arm[1184676:1184680]
    assert ram[1424360:1424376] == arm[1424360:1424376]
    assert ram[1432020:1432033] == arm[1432020:1432033]
    sheets = visual['sheets'] + live['review_sheets'] + [live_menus['review_sheet'], corrected['review_sheet']] + retained['review_sheets']
    assert len(sheets) == 16 and all(digest(row['path']) == row['sha256'] for row in sheets)
    seen = {row['id'] for row in live['body_pages']}
    actors = {row['expected_actor_ID'] for row in live['headers']}
    assert len(seen) == 42 and len(actors) == 10 and seen <= speech.keys()
    assert {'SC0_B261_STYLE_342_176', 'SC0_B261_STYLE_852_176', 'DK4_MES_B276_R0047',
            'DK4_MES_B262_R0007', 'DK4_MES_B263_R0006', 'DK4_MES_B264_R0006'} <= seen
    assert {row['page'] for row in live['body_pages'] if row['id'] == 'DK4_MES_B277_R0009'} == {1, 2}

    for row in doc['records']:
        ident = row['id']
        if ident in speech:
            saved = speech[ident]
            offset = saved['new_offset']
            ref = dict(offset=offset, record_index=saved['new_record_index'])
            if saved.get('virtual_prefix_not_stored'):
                assert row['source_style_indices'] == saved['source_style_indices']
                ref.update(command_offset=saved['final_command_offset'], source_style_indices=saved['source_style_indices'],
                           virtual_prefix_not_stored=True)
            else:
                assert blocks[row['block']][offset-5:offset+1].hex() == row['source_complete_preamble_hex']
                ref['header_offset'] = offset - 5
            if row['kind'] == 'system-FE':
                row['native_FE_presentation_binding_pending'] = False
            row['actual_utterance_observed_in_disclosed_fixture'] = ident in seen
            row['planned_English_markup'] = layouts[ident]['formatted_markup']
        else:
            item, saved = captions[ident]
            offset = saved['offset']
            assert item['block'] == row['block'] and item['word'] == row['source_word']
            assert bytes.fromhex(saved['stored_hex']).decode('ascii') == row['english']
            ref = dict(offset=offset, command_offset=item['offset'], source_index=saved['source_index'],
                       record_index=saved['record_index'])
            row['actual_caption_visible_with_default_cursor'] = True
        raw = bytes.fromhex(saved['stored_hex'])
        assert blocks[row['block']][offset:offset+len(raw)+1] == raw+b'\0'
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row.update(planned_integrated_reference=dict(**ref, file_path=row['file_path'], block=row['block'],
            exact_stored_hex=raw.hex(), target_archive_sha256=rebuilt['target_archive_sha256']),
            fresh_formatting_binding_pending=False, registered_release_and_completion_credit_pending=True)
    assert Counter(row['decision'] for row in doc['records']) == {'revision': 118, 'retention': 17}
    for row in names['records']:
        row['review']['formatting'] = True
        japanese = ' '.join(part['text'] for part in row['source_reference'] if part['text'])
        row.update(speaker='Speaker name or role', context='Source-qualified actor in the Rafael B261–B280 exchanges.',
                   source_meaning=japanese, localization_note=row['finding'],
                   actual_header_observed_in_disclosed_fixture=row['actor_ID'] in actors)

    RESEARCH.mkdir()
    actual_path, visual_path, release_plan = [RESEARCH/name for name in (
        'actual_review.json', 'complete_visual_approval.json', 'release_plans.json')]
    evidence = {str(path): digest(path) for path in (*paths, capture, Path(__file__))}
    save(actual_path, dict(total_frames=15761, initialized_fixture_runs=1, source_speech_variants_observed=42,
        native_body_pages_observed=43, actual_choice_labels=5, offline_only_speech_variants=88,
        source_IDs_observed=sorted(seen), offline_only_source_IDs=sorted(set(speech)-seen),
        observed_public_name_actor_IDs=sorted(actors), actual_header_Jacob_Portunto=True,
        proposed_Plett_slot_and_pointer_read_back_from_actual_fixture_RAM=True, actual_Plett_header_unvisited=True,
        both_complete_style_commands_observed_under_unmodified_default_roles=True,
        all_two_menu_instances_default_cursor_and_following_fixture_speech_observed=True,
        menus=live_menus['menus'], other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        observed_FE_source_IDs=sorted(seen & {row['id'] for row in doc['records'] if row['kind']=='system-FE'}),
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        evidence=evidence, new_credit=0, guide_photos=False))
    save(visual_path, dict(all_body_caption_andname_planes_approved=True, all_actual_pages_and_menus_directly_viewed=True,
        body_pages=131, observed_pages=43, scoped_public_names=18, typed_labels=5, reviewed_sheets=sheets,
        evidence=evidence, new_credit=0, guide_photos=False))
    names.update(all_name_formatting_gates_pending=False, all_individual_five_gates_pass_for_public_nameplanes=True,
                 actual_review=str(actual_path), actual_review_sha256=digest(actual_path))
    validate_natural_dialogue_batch(names)
    save(FINAL_NAMES, names)
    doc.update(all_fifth_formatting_gates_pending=False, all_individual_five_gates_pass=True,
        native_macro_tokens_still_require_formatter_marking=False, only_disclosed_fixture_gameplay_observed=True,
        native_body_pages=131, actual_source_speech_variants=42, actual_body_pages=43, offline_only_source_speech_variants=88,
        scoped_name_review=str(FINAL_NAMES), scoped_name_review_sha256=digest(FINAL_NAMES), parent_manuscript=str(MANUSCRIPT),
        parent_manuscript_sha256=digest(MANUSCRIPT), registered_release_and_completion_credit_pending=True,
        formatting_evidence=dict(native=str(NATIVE), stored=str(STORED), catalogue=str(LOOKUP),
                                 loaders=str(LOADERS), visual=str(visual_path), actual=str(actual_path)))
    validate_natural_dialogue_batch(doc)
    save(FINAL, doc)
    save(release_plan, {**plan, 'manuscript': str(FINAL), 'manuscript_sha256': digest(FINAL),
                       'exact_all_prose_and_compiled_bytes_unchanged': True})
    save(READY, dict(manuscript=str(FINAL), manuscript_sha256=digest(FINAL),
        plan=str(release_plan), plan_sha256=digest(release_plan), all_individual_five_gates_pass=True,
        records=135, revisions=118, retentions=17, body_pages=131, typed_labels=5, scoped_public_names=18,
        actual_source_variants=42, actual_pages=43, actual_choice_labels=5, actual_menus=2, actual_name_headers=10,
        offline_only_source_variants=88, registered_integration_pending=True, new_credit=0, full_goal_complete=False,
        evidence={**evidence, **{str(p):digest(p) for p in (FINAL, FINAL_NAMES, release_plan, visual_path, actual_path)}}))
    print('Sealed 135 reviews, 131 stored pages, both surnames and 43 focused emulator pages.')


if __name__ == '__main__':
    main()
