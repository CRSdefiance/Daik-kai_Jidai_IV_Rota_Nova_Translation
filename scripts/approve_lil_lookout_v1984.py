"""Approve the one changed B23 record within its full64-entry contextual review."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Lookout_approval_v1984')
DOC = Path('translations/lil_lookout_affiliation_editorial_manuscript_v1.json')
MAP = Path('translations/lil_lookout_affiliation_relocation_map_v1.json')
ACTUAL = Path('work/analysis/lil_Lookout_actual_v1983/focused_Lookout_neighbors_original_B23_results_and_return.json')
DRAFT = Path('translations/lil_lessons_editorial_manuscript_v6.json')
CHOICES = Path('translations/lil_lesson_choices_editorial_draft_v3.json')
FONT = Path('work/analysis/lil_Lookout_affiliation_fonts_v1978/one_changed_native_macros_and_complete_font_plane.json')
PLAN = Path('work/analysis/lil_Lookout_relocation_v1980/current_B23_typed_relocation_research.json')
LOADER = Path('work/analysis/lil_Lookout_loader_v1981/whole_SC2_and_B23_initial_entry_proof.json')
INHERITANCE = Path('work/analysis/lil_lessons_native_checkpoint_v1979b/all60_source_bound_native_font_inheritance.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not MAP.exists()
    draft, actual, font, plan, loader, inheritance = map(read,(DRAFT,ACTUAL,FONT,PLAN,LOADER,INHERITANCE))
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    assert plan['all55_current_and_target_native_commands_and_opaque_bytes_preserved']
    assert plan['all12_relative_sites_120_cases_preserve_targets']
    assert plan['inverse_restores_every_original_logical_byte']
    assert plan['all_other335_SC2_blocks_and_all_other_files_components_exact']
    for flag in ('changed_Lookout_two_holds_complete_native_actual_ink',
        'preceding_and_following_Camille_four_holds_complete_native_actual_ink',
        'all46_original_B23_command_results_and_mapped_targets_equal',
        'all_unowned_B120_command_results_and_source_offsets_unchanged',
        'original_choice0_full_crew_lesson_and_normal_type0_return',
        'one16_coordinate_byte_fixture_replay_exact',
        'all_inputs_schedule_PNGs4MiB_snapshots_and_readonly_observers_host_restoration_pass'):
        assert actual[flag]
    assert actual['normal_Bruges_town_ID'] == 3 and actual['whole_terminal_RGB_equal_original']
    assert actual['candidate_sha256'] == plan['research_ROM_sha256']
    assert inheritance['new_native_planes'] == 1 and inheritance['inherited_unchanged_progressive_planes'] == 50
    assert inheritance['inherited_unchanged_separate_FE_mode1_planes'] == 9 and inheritance['inherited_typed_choice_labels'] == 4
    files = {str(p) for p in (DRAFT,CHOICES,FONT,PLAN,LOADER,INHERITANCE,ACTUAL,Path(__file__),
        Path('work/analysis/lil_Lookout_relocation_v1980/research_image_receipt.json'),
        Path('translations/lil_lessons_final_review_v1.json'),
        Path('translations/lil_lessons_editorial_relocation_map_v1.json'))}
    pending, checked = list(files), set()
    while pending:
        name = pending.pop()
        if name in checked: continue
        checked.add(name)
        path = Path(name)
        assert path.exists(),name
        if path.suffix != '.json': continue
        data = read(path)
        if not isinstance(data,dict): continue
        for dep,expected in data.get('evidence',{}).items():
            assert sha(Path(dep).read_bytes()) == expected,dep
            files.add(dep)
            pending.append(dep)
    for case in font['cases']:
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        files.add(case['preview'])
    for group in actual['focused_glyph_groups']:
        for hold in group['holds']:
            assert sha(Path(hold['capture']).read_bytes()) == hold['capture_sha256']
            files.add(hold['capture'])
    ROOT.mkdir(parents=True)
    visual = ROOT/'representative_actual_visual_approval.json'
    save(visual,dict(changed_Lookout_and_two_neighboring_Camille_panels_actually_viewed=True,
        full_Camille_portrait_nameplate_body_bounds_and_normal_Bruges_return_viewed=True,
        changed_native_preview_and_actual_full_glyph_planes_viewed=True,
        automated_six_full_pixel_holds_distinct_from_three_visual_panels=True,
        original_choice0_only_new_sample_other_paths_inherited=True,other27_B23_speeches_execute_without_fresh_pixel_claim=True,
        old_full64_review_keeps_five_original_conditional_equivalent_objects_without_individual_visit_claim=True,
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),full_goal_complete=False))
    files.add(str(visual))
    mapping = deepcopy(plan)
    mapping.update(format='dk4-lil-lookout-source-relocation-map-v1',file_path='/data/SC2.DK4',entry_point_offset=8,
        external_references_complete=True,preserve_record_parity=True,required_runtime_ARM9_sha256=plan['ARM9_sha256'],
        target_SC2_sha256=plan['target_SC2_sha256'],target_block_sha256=plan['research_block_sha256'],
        all55_nested_commands12_relative_sites_verified=True,all120_current_relocated_native_cases_verified=True,
        current_EV2_block_index_loader_and_two_parent_modes_verified=True,
        immutable_runtime_overlay_reference_census_inherited_from_registered_parent=True,
        one_changed_progressive_record_actual_and_neighbor_transition_approved=True,
        not_a_release_relocation_map=False,
        evidence={p:sha(Path(p).read_bytes()) for p in sorted(files)},
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(MAP,mapping)
    row = deepcopy(next(r for r in draft['records'] if r['id'] == 'DK4_MES_B23_R0142'))
    row['english'] = row['english'].removesuffix('{PAD}')
    row['review']['formatting'] = True
    compiled = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],get_dialogue_profile('lil-opening-editorial-native-v1'))
    assert compiled.encoded.hex() == font['cases'][0]['encoded_hex'] and not compiled.diagnostics
    row.update(compiled_hex=compiled.encoded.hex(),native_display_consumer='original_progressive_54020',
        native_font_proof=str(FONT),actual_proof=str(ACTUAL),actual_holds=actual['focused_glyph_groups'][1]['holds'],
        complete_current_source_reference_map=str(MAP),context=row['context'].split('New native/')[0]+(
            'Full native,typed source reference,final parity,focused revised glyphs andnormal Brugesreturn pass;registered integration pending. The other63 entries retain source-reviewed wording andexact inherited display evidence.'))
    batch = dict(format='dk4-natural-dialogue-reviewed-batch-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',dialogue_profile='lil-opening-editorial-native-v1',file_path='/data/SC2.DK4',block=23,
        review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=False,
        source_context=draft['source_context'],source_context_sha256=draft['source_context_sha256'],current_ROM=draft['current_ROM'],
        current_ROM_sha256=draft['current_ROM_sha256'],source_clean_ROM_sha256=draft['source_clean_ROM_sha256'],
        required_runtime_ARM9_sha256=plan['ARM9_sha256'],approved_names=draft['approved_names'],records=[row],
        full64_contextual_review_manuscript=str(DRAFT),unchanged_four_choices_review=str(CHOICES),
        full60_native_inheritance=str(INHERITANCE),native_font_proof=str(FONT),approved_reference_map=str(MAP),
        approved_reference_map_sha256=sha(MAP.read_bytes()),actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),
        status='one-source-native-reference-revised-approved;registered-integration-pending',full_goal_complete=False)
    validate_natural_dialogue_batch(batch)
    save(DOC,batch)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        map=str(MAP),map_sha256=sha(MAP.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        full64_source_prose_entries=64,revisions=1,justified_retentions=63,new_native_planes=1,new_macro_calls=8,
        inherited_unchanged_speech_targets=59,inherited_unchanged_labels=4,native_commands=55,relative_sites=12,
        current_relocated_native_cases=120,actual_changed_holds=2,actual_neighbor_holds=4,original_B23_results=46,
        no_new_ROM_registry_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(release_records=1,contextual_entries=64,justified_retentions=63,typed_commands=55,relative_sites=12,registered_integration_pending=True))
