"""Approve complete B74 source map after revised progressive/FE/choice gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_hamburg_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_approval_v1968')
OLD = Path('translations/lil_hamburg_recruitment_editorial_manuscript_v3.json')
DOC = Path('translations/lil_hamburg_recruitment_editorial_manuscript_v4.json')
OLD_CHOICES = Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v2.json')
CHOICES = Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v3.json')
MAP = Path('translations/lil_hamburg_editorial_relocation_map_v1.json')
RELOC = Path('work/analysis/lil_Hamburg_relocation_v1960/nested_source_relocation_research.json')
CENSUS = Path('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')
ACTUAL = Path('work/analysis/lil_Hamburg_revised_audit_v1967b/revised_Hamburg79_choice_join_and_three_access_fixture_audit.json')
SOURCE = Path('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not CHOICES.exists() and not MAP.exists()
    doc, menu, reloc, census, actual, source = map(read,(OLD,OLD_CHOICES,RELOC,CENSUS,ACTUAL,SOURCE))
    assert len(doc['records']) == 79 and len(menu['records']) == 2
    assert census['all123_clean_current_target_commands_and20_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert census['only_original24070_interpreter_call_no_literal_alias']
    assert reloc['all100_relocated_native_skip_cases_match_original_target_mapping']
    for flag in ('all79_activated_revised_speeches158_holds_complete_native_independent_actual_glyphs',
        'both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds',
        'all3_FE_panels_six_actual_holds_match_separate_paper_planes',
        'original_join_command_and_complete_bottom_screen_ink_preserved',
        'same116_original_B74_commands_results_and_event_transitions',
        'normal_docking_B74_entry_and_Hamburg_return_not_overridden',
        'all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified',
        'all_readonly_observer_boundaries_and_host_restoration_pass'):
        assert actual[flag]
    observed = {r['id'] for r in actual['revised_speech_observations']}
    assert observed == {r['id'] for r in doc['records']} and len(observed) == 79
    parent, target, clean = map(NdsImage.open,(reloc['candidate'],census['research_ROM'],'work/clean.nds'))
    arm = parent.read_file('/__arm9__.bin')
    source_block = IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks[74]
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[74]
    fonts = {r['id']:r for r in read(doc['native_font_proof'])['cases']}
    ROOT.mkdir(parents=True)
    visual = ROOT/'representative_actual_visual_approval.json'
    save(visual,dict(all5_representative_revised_sheets19_panels_actually_viewed=True,
        Gerhard_full_portrait_nameplate_mistaken_wife_question_manners_clash_and_limited_apology_viewed=True,
        strongest_private_fleet_history_reluctant_recruitment_and_name_joke_viewed=True,
        all3_revised_FE_panels_six_matching_actual_holds=True,
        original_complete_Gerhard_join_panel_revised_two_label_menu_and_normal_town_return_viewed=True,
        automated158_complete_speech_holds_separate_from19_visual_samples=True,choice1_not_individually_selected=True,
        evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),**{p:sha(Path(p).read_bytes()) for p in actual['representative_contact_sheets']}},
        full_goal_complete=False))
    files = {str(p) for p in (OLD,OLD_CHOICES,RELOC,CENSUS,ACTUAL,SOURCE,visual,Path(__file__),
        Path('dk4tool/dialogue/lil_hamburg_profile.py'),
        Path('work/analysis/lil_Hamburg_controls_v1953b/source_bound_B74_presenter_and_control_contract.json'),
        Path('work/analysis/lil_Hamburg_font_approval_v1959/approval_receipt.json'),
        Path('work/analysis/lil_Hamburg_choice_v1958/original_choice_decoder_VM_geometry_and_native_pixels.json'),
        Path('work/analysis/lil_Hamburg_choice_calibration_v1964/original_current_menu_fixed_margin_calibration.json'),
        Path('work/analysis/lil_Hamburg_research_v1961/research_image_receipt.json'),
        Path('work/analysis/lil_Hamburg_loader_v1962/whole_SC2_and_B74_initial_entry_proof.json'))}
    files.add(doc['native_font_proof'])
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
        for dep,digest in data.get('evidence',{}).items():
            assert sha(Path(dep).read_bytes()) == digest,dep
            files.add(dep)
            pending.append(dep)
    for case in fonts.values():
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        files.add(case['preview'])
    assert len(reloc['blocks']) == len(census['blocks']) == 1
    proposed, spec = reloc['blocks'][0], census['blocks'][0]
    assert proposed['block'] == spec['block'] == 74 and len(spec['mapped_commands']) == 123
    assert len(proposed['relative_skip_fixups']) == 20 and len(proposed['target_native_skip_cases']) == 100
    assert proposed['inverse_restoration_recovers_every_original_logical_byte']
    block = dict(block=74,source_block_sha256=proposed['source_block_sha256'],clean_block_sha256=sha(jp),
        target_block_sha256=proposed['research_block_sha256'],entry_point_offset=8,external_references_complete=True,
        text_records=proposed['text_records'],choice_commands=proposed['choice_commands'],
        relative_skip_fixups=proposed['relative_skip_fixups'],mapped_native_commands=spec['mapped_commands'],
        inverse_restores_every_original_logical_byte=True,target_native_skip_cases=proposed['target_native_skip_cases'])
    mapping = dict(format='dk4-lil-hamburg-source-relocation-map-v1',file_path='/data/SC2.DK4',
        required_runtime_ARM9_sha256=sha(arm),source_SC2_sha256=sha(parent.read_file('/data/SC2.DK4')),
        target_SC2_sha256=sha(target.read_file('/data/SC2.DK4')),clean_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),
        entry_point_offset=8,external_references_complete=True,preserve_record_parity=True,
        all123_nested_command_boundaries_and20_relative_sites_verified=True,
        all100_relocated_relative_skip_cases_preserve_original_targets=True,
        representative79_speech158_holds_and_two_choice_labels_approved=True,
        actual_speech_record_IDs=sorted(observed),offline_only_speech_record_IDs=[],blocks=[block],
        actual_scope='79 revised speeches/158 complete holds,three FE panels/six holds,both visible tutorial labels,the original default choice0 lesson,Gerhard join panel andnormal Hamburg return. Choice1 is native-VM/source only.',
        conditional_risk_assessment='Both stored choice indices andnative selection/cancel returns preserve original semantics;all20 relative operands and123 command mappings pass. Choice1 only skips the battle lesson;no extra display consumer or unresolved alternate-path risk requires a second live selection.',
        evidence={p:sha(Path(p).read_bytes()) for p in sorted(files)},
        not_registered_ROM_or_full_route_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(MAP,mapping)
    successor = deepcopy(doc)
    for row in successor['records']:
        consumer = 'FE-paper' if row['source_presentation_prefix_hex'] == 'fe' else 'progressive'
        compiled = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source_block,consumer))
        assert compiled.encoded.hex() == fonts[row['id']]['encoded_hex']
        row.update(compiled_hex=compiled.encoded.hex(),individually_activated_in_revised_sample=True,representative_actual_proof=str(ACTUAL))
        row['context'] = row['context'].split('NewB74 native')[0]+('Source-bound original controls,native progressive andFE layouts,typed choice dispatch andrepresentative revised gameplay pass;registered integration remains pending. All79speeches were individually captured;choice1 has source/native-VM coverage only.')
    successor.update(status='source-native-and-revised-approved;registered-integration-pending',
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        approved_reference_map=str(MAP),approved_reference_map_sha256=sha(MAP.read_bytes()),
        actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),
        scoped_control_proof='work/analysis/lil_Hamburg_controls_v1953b/source_bound_B74_presenter_and_control_contract.json',
        native_font_source_manuscript_sha256=sha(OLD.read_bytes()),
        actual_revised_gameplay_and_registered_release_pending=False,registered_release_pending=True)
    menu_successor = deepcopy(menu)
    menu_successor.update(status='source-native-and-revised-menu-approved;registered-integration-pending',
        predecessor_manuscript=str(OLD_CHOICES),predecessor_manuscript_sha256=sha(OLD_CHOICES.read_bytes()),
        approved_reference_map=str(MAP),approved_reference_map_sha256=sha(MAP.read_bytes()),
        actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),registered_release_pending=True)
    for row in menu_successor['records']:
        row['context'] += ' Both labels are visible in the revised menu;default option0 was selected with native result0 andthe complete lesson. Option1 has source/native-VM coverage without individual selection.'
    validate_natural_dialogue_batch(successor)
    validate_natural_dialogue_batch(menu_successor)
    save(DOC,successor)
    save(CHOICES,menu_successor)
    save(ROOT/'final_source_reference_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        native_speeches=79,typed_choice_labels=2,complete_commands=123,relative_sites=20,target_native_skip_cases=100,
        actual_revised_speeches=79,actual_complete_speech_holds=158,actual_FE_holds=6,actual_complete_choice_holds=2,
        actual_join_holds=2,all_required_source_native_and_representative_gameplay_gates_passed=True,
        no_new_ROM_registry_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_native_revised_speeches=79,typed_labels=2,approved_commands=123,approved_spans=20,registered_release_pending=True))
