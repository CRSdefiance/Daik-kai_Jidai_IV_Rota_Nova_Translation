"""Pure cumulative SC0 integration of249 individually reviewed speech/choice records."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_scene_batch_v5 import compound_objects
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from scripts.audit_story_glyph_consistency import load
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def require(value, message):
    if not value:
        raise ValueError('Rafael B51-B60 release: ' + message)


def qualify_evidence(conf, doc, stored):
    native, visual, names, actual, pixels, menu_pixels, menu, lookup, loaders = [load(conf[k]) for k in
        ['compiled_native','visual_review','scoped_names','actual','focused_pixels','menu_pixels','typed_menu','stored_lookup','loaders']]
    validate_natural_dialogue_batch(names)
    require(len(names['records']) == 18 and names['no_new_dialogue_credit'], 'all18 scoped identities without dialogue credit')
    require({r['actor_ID'] for r in names['records']} == {0,1,4,5,6,7,8,11,14,20,24,35,37,39,84,114,116,151}, 'exact scoped actors')
    require(native['runtime'] == stored['runtime'] and stored['runtime']['captain'] == 0, 'own Rafael context')
    require(visual['final_253_pages_have_exact_native_glyphs_bounds_controls_substitutions_consumption_pagination_andvisual_approval']
            and visual['body_pages'] == stored['complete_stored_pages'] == 253, 'complete native/stored/visual pages')
    require(stored['fresh_relocated_native_relative_cases'] == 380 and stored['all_stored_planes_equal_directly_viewed_compiled_planes']
            and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'], 'native branches and complete glyphs')
    observed = {r['id']:r for r in stored['records']}
    compiled = {r['id']:r for r in native['records']}
    speech = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    require(set(observed) == set(compiled) == {r['id'] for r in speech} and len(speech) == 245, 'complete individual speech membership')
    for row in speech:
        entry, plane, ref = observed[row['id']], compiled[row['id']], row['planned_integrated_reference']
        require(ref['offset'] == entry['new_offset'] and ref['record_index'] == entry['new_record_index']
                and ref['exact_stored_hex'] == entry['stored_hex'], 'individual tested stored reference')
        require(plane['source_reference'] == row['source_reference'] and plane['current_reference'] == row['current_reference']
                and plane['logical_English'] == row['english'], 'individual source/current/prose binding')
        if row['kind'] == 'system-FE':
            require(row['source_selector'] == 254 and plane['complete_native_English_display']['planned_native_row_comparison']['complete_glyph_row_membership_exact'], 'FE consumer andcomplete row membership')
    require(sum(r['kind'] == 'system-FE' for r in speech) == 3, 'exact three FE notices')
    require(len(lookup['records']) == 245 and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'no old catalogue alias restoration')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) == (343,20,666)
            and loaders['prior_executed_parent_instructions_match_current_runtime'], 'all native archive and parent modes')
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and len(menu['menus']) == 2, 'both native menus visually approved')
    for item in menu['menus']:
        proof_path = Path(item['source_native_receipt'])
        require(sha(proof_path.read_bytes()) == item['source_native_receipt_sha256'], 'exact menu native receipt')
        proof = load(proof_path)
        require(proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
                and proof['source_index_andcount_preserved'] and len(proof['compiler_negatives_rejected']) == 7, 'complete captions/indices andnegative cases')
        require((proof['native_provider_alignments'],proof['bridged_modal_returns'],proof['complete_English_caption_style_planes']) == (6,18,8), 'all tested menu alignments/returns/styles')
    require((actual['total_frames'],actual['initialized_fixture_runs'],actual['actual_utterances'],actual['actual_body_pages'],actual['actual_choice_captions'],actual['offline_only_utterances'])
            == (18662,2,32,35,4,213), 'honest actual versus offline scope')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']), 'no unobserved route/hardware claim')
    require(actual['all_six_QA_sheets_directly_viewed'] and actual['all_required_distinct_wrap_glyph_macro_pagination_andmenu_cases_pass'], 'all six QA sheets anddistinct risks')
    require(pixels['all_selected_pages_observed_in_exact_fixture_order'] and pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
            and (pixels['complete_body_planes'],pixels['complete_header_planes']) == (64,58), 'complete ordered live body/header planes')
    require(len(pixels['body_pages']) == 64 and len(pixels['headers']) == 58
            and len({(r['id'],r['page']) for r in pixels['body_pages']}) == 30, 'individual actual page/header membership')
    require({r['actor_ID'] for r in pixels['headers']} == {r['actor_ID'] for r in names['records']}, 'all18 live scoped headers')
    require(menu_pixels['both_two_option_menu_caption_planes_centering_first_internal_final_glyphs_andblank_guards_match']
            and menu_pixels['first_menu_cursor_down_up_andsecond_menu_cursor_down_observed']
            and menu_pixels['A_acceptance_followed_by_original_next_fixture_speech_observed'], 'controller captions/cursors andmodal continuations')
    require(menu_pixels['original_story_response_branches_conditions_andcancellation_unvisited']
            and actual['live_numeric_return_register_original_menu_response_branches_andcancellation_unvisited'], 'accurate unvisited branch scope')
    require(len(menu_pixels['menu_samples']) == 8
            and len({r['id'] for r in pixels['body_pages']} | {r['id'] for r in menu_pixels['body_pages']}) == 32, 'individual menu andunique sampled speech membership')


def plan_release(image, baseline, config_path):
    conf = load(config_path)
    require(conf['format'] == 'dk4-rafael-B51-B60-release-v1', 'schema')
    for path, digest in conf['dependencies'].items():
        require(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before, base_before = bytes(image.rom.save()), bytes(baseline.rom.save())
    require(sha(before) == conf['parent_ROM_sha256'], 'complete ordered predecessor')
    require(sha(baseline.source.read_bytes()) == conf['canonical_ROM_sha256'], 'canonical baseline')
    arm = image.read_file('/__arm9__.bin')
    require(sha(arm) == conf['pre_runtime_ARM9_sha256'], 'pre-runtime ARM9')
    clean_path = Path(conf['clean_ROM'])
    require(sha(clean_path.read_bytes()) == conf['clean_ROM_sha256'], 'clean Japanese input')
    clean = NdsImage.open(clean_path)
    doc, layout, reconstruction, stored, menu, styles = [load(conf[k]) for k in
        ['manuscript','plan','reconstruction','stored_native','typed_menu','native_styles']]
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US', 'individual American English review')
    require(len(doc['records']) == len({r['id'] for r in doc['records']}) == conf['record_count'] == 249, 'complete unique membership')
    require(all(all(r['review'][g] is True for g in REQUIRED_REVIEW_GATES) for r in doc['records']), 'all five individual gates')
    require(all(not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD}','\n']) for r in doc['records']), 'logical prose only')
    speech = [r for r in doc['records'] if r['kind'] in ('progressive','system-FE')]
    choices = [r for r in doc['records'] if r['kind'] == 'typed-choice-label']
    require(len(speech) == 245 and len(choices) == 4 and not styles['objects']
            and not any(r.get('native_object_kind') == '4100-style-alternative' for r in speech), 'exact qualified consumers')
    plans = {r['id']:r for r in layout['records']}
    approved = {r['id']:r for r in doc['records']}
    require(len(plans) == len(layout['records']) == 245 and not layout['failures'], 'complete unique fresh plans')
    for row in speech:
        plan = plans[row['id']]
        require(row['english'] == plan['logical_English'] and row['planned_English_markup'] == plan['formatted_markup'], 'logical andformatted plan binding')
        require(bytes.fromhex(plan['encoded_hex'])[0] == row['source_selector'], 'complete source speaker selector')
        require(not any(i['severity'] in ('warning','error') for i in plan['base_QA']['issues']), 'resolved fresh formatting diagnostics')
    require(doc['blocks'] == conf['blocks'] == reconstruction['changed_blocks'] == list(range(51,61)), 'all ten complete scenes')
    qualify_evidence(conf, doc, stored)
    path = doc['file_path']
    require(path == '/data/SC0.DK4', 'owned route archive')
    archive = image.read_file(path)
    require(sha(archive) == reconstruction['source_archive_sha256'], 'complete current archive')
    container = IlnkContainer.parse(archive)
    clean_blocks = IlnkContainer.parse(clean.read_file(path)).blocks
    require(len(container.blocks) == len(clean_blocks) == 343, 'whole route membership')
    inventory, _, _ = scoped_inventory()
    blocks, changes = list(container.blocks), []
    require([g['block'] for g in reconstruction['groups']] == conf['blocks'], 'complete ordered reconstruction')
    for group in reconstruction['groups']:
        number = group['block']
        require(sha(blocks[number]) == group['current_sha256'] and sha(clean_blocks[number]) == group['clean_sha256'], 'source/current complete block identities')
        objects = compound_objects(group, approved, plans, menu, styles)
        rows = [r for r in speech if r['block'] == number]
        target, proof = rebuild_block(arm, clean_blocks[number], blocks[number], rows, plans, inventory, objects)
        require(sha(target) == group['target_sha256'] and target == Path(group['target_block']).read_bytes(), 'fresh complete source-bound reconstruction')
        require(all(value == group[key] for key,value in proof.items()), 'complete commands/relative maps andinverses')
        blocks[number] = target
        for row in (r for r in doc['records'] if r['block'] == number):
            ref = row['planned_integrated_reference']
            at, raw = ref['offset'], bytes.fromhex(ref['exact_stored_hex'])
            require(target[at:at+len(raw)+1] == raw+b'\0' and ref['target_archive_sha256'] == reconstruction['target_archive_sha256'], 'individual stored target reference')
            changes.append(dict(id=row['id'],file_path=path,block=number,new_offset=at,kind=row['kind'],stored_sha256=sha(raw)))
    result = IlnkContainer(blocks).to_bytes()
    require(sha(result) == reconstruction['target_archive_sha256'] and result == Path(reconstruction['target_archive']).read_bytes(), 'whole tested archive')
    require({i for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if a != b} == set(conf['blocks']), 'only reviewed blocks change')
    inverse = list(blocks)
    for number in conf['blocks']:
        inverse[number] = container.blocks[number]
    require(IlnkContainer(inverse).to_bytes() == archive, 'complete archive inverse')
    planned = deepcopy(image)
    planned.replace_file(path,result)
    require(sha(bytes(planned.rom.save())) == conf['target_ROM_sha256'], 'complete ordered target')
    require([p for _,p,v in image.iter_files() if planned.read_file(p) != v] == [path]
            and all(planned.read_file(p) == v for p,v in image.iter_components()), 'all other files/components unchanged')
    restored = deepcopy(planned)
    restored.replace_file(path,archive)
    require(bytes(restored.rom.save()) == before, 'complete serialized parent inverse')
    require(bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == base_before, 'pure caller preservation')
    return planned.rom, dict(manuscripts=[conf['manuscript']],changed_records=changes,
        files=[dict(file_path=path,source_sha256=sha(archive),target_sha256=sha(result),changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,all_source_controls_commands_relatives_andunowned_bytes_preserved=True,
        native_pages=253,fresh_relative_cases=380,native_loads=343,typed_labels=4,actual_frames=18662,
        representative_initialized_gameplay_not_natural_event_activation=True,
        canonical_stage_requires_registered_right_bound_runtime_layer=conf['right_bound_configuration'],
        no_completion_credit_orpromotion_granted=True,full_goal_complete=False)
