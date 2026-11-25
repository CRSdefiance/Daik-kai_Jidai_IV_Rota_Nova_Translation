"""Approve exhaustive Speyer source map after representative revised gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_speyer_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Speyer_approval_v1942')
OLD=Path('translations/lil_speyer_encounter_editorial_manuscript_v2.json')
DOC=Path('translations/lil_speyer_encounter_editorial_manuscript_v3.json')
OLD_CHOICES=Path('translations/lil_speyer_choices_editorial_draft_v2.json')
CHOICES=Path('translations/lil_speyer_choices_editorial_draft_v3.json')
MAP=Path('translations/lil_speyer_editorial_relocation_map_v1.json')
RELOC=Path('work/analysis/lil_Speyer_relocation_v1928/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Speyer_reference_census_v1931/all137_commands48_relative_sites_and_shipped_entry_census.json')
ACTUAL=Path('work/analysis/lil_Speyer_revised_audit_v1941/revised_Speyer51_choice_and_three_access_fixture_audit.json')
SOURCE=Path('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not CHOICES.exists() and not MAP.exists()
    doc,menu,reloc,census,actual,source=map(read,(OLD,OLD_CHOICES,RELOC,CENSUS,ACTUAL,SOURCE))
    assert len(doc['records'])==57 and len(menu['records'])==2
    assert census['all137_clean_current_target_commands_and48_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert census['only_original24070_interpreter_call_no_literal_alias']
    assert reloc['all240_relocated_native_skip_cases_match_original_target_mapping']
    assert actual['all51_activated_revised_speeches102_holds_complete_native_independent_actual_glyphs']
    assert actual['both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds']
    assert actual['same107_original_B128_commands_results_and_event_transitions']
    assert actual['same116_unowned_B74_command_results']
    assert actual['normal_docking_Port_action_B128_entry_and_Hamburg_return_not_overridden']
    assert actual['all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified']
    assert actual['all_readonly_observer_boundaries_and_host_restoration_pass']
    observed={r['id']for r in actual['revised_speech_observations']}
    all_ids={r['id']for r in doc['records']}
    unseen=all_ids-observed
    assert len(observed)==51 and len(unseen)==6
    parent,target,clean=map(NdsImage.open,(reloc['candidate'],census['research_ROM'],'work/clean.nds'))
    arm=parent.read_file('/__arm9__.bin')
    source_blocks=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks
    jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    ROOT.mkdir(parents=True)
    visual=ROOT/'representative_actual_visual_approval.json'
    save(visual,dict(all3_representative_revised_sheets12_panels_actually_viewed=True,
        Martin_Speyer_and_Sailor152_portraits_nameplates_and_transitions_viewed=True,
        complete_four_row_paragraphs_company_macros_First_Mate_and_negation_viewed=True,
        revised_two_label_menu_and_normal_Hamburg_return_viewed=True,
        automated102_complete_speech_holds_and_two_complete_menu_holds_separate_from12_visual_samples=True,
        six_conditional_speeches_not_individually_activated=True,choice1_not_individually_selected=True,
        unowned_B74_79_original_captures_not_editorial_completion=True,
        evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),**{p:sha(Path(p).read_bytes())for p in actual['representative_contact_sheets']}},
        full_goal_complete=False))
    files={str(p)for p in(OLD,OLD_CHOICES,RELOC,CENSUS,ACTUAL,SOURCE,visual,Path(__file__),
        Path('dk4tool/dialogue/lil_speyer_profile.py'),
        Path('work/analysis/lil_Speyer_controls_v1936/source_bound_B25_B128_progressive_control_contract.json'),
        Path('work/analysis/lil_Speyer_font_approval_v1937b/approval_receipt.json'),
        Path('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json'),
        Path('work/analysis/lil_Speyer_choice_calibration_v1939/original_current_menu_fixed_margin_calibration.json'),
        Path('work/analysis/lil_Speyer_research_v1929/research_image_receipt.json'),
        Path('work/analysis/lil_Speyer_loader_v1930/whole_SC2_and_B25_B128_initial_entry_proof.json'))}
    files.add(doc['native_font_proof'])
    pending=list(files)
    checked=set()
    while pending:
        name=pending.pop()
        if name in checked:continue
        checked.add(name)
        path=Path(name)
        assert path.exists(),name
        if path.suffix!='.json':continue
        data=read(path)
        if not isinstance(data,dict):continue
        for dep,digest in data.get('evidence',{}).items():
            assert sha(Path(dep).read_bytes())==digest,dep
            files.add(dep)
            pending.append(dep)
    for case in fonts.values():
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        files.add(case['preview'])
    blocks=[]
    for proposed in reloc['blocks']:
        number=proposed['block']
        spec=next(r for r in census['blocks']if r['block']==number)
        assert len(spec['mapped_commands'])==(15 if number==25 else 122)
        assert proposed['inverse_restoration_recovers_every_original_logical_byte']
        blocks.append(dict(block=number,source_block_sha256=proposed['source_block_sha256'],
            clean_block_sha256=sha(jp[number]),target_block_sha256=proposed['research_block_sha256'],
            entry_point_offset=8,external_references_complete=True,
            text_records=proposed['text_records'],choice_commands=proposed['choice_commands'],
            relative_skip_fixups=proposed['relative_skip_fixups'],mapped_native_commands=spec['mapped_commands'],
            inverse_restores_every_original_logical_byte=True,target_native_skip_cases=proposed['target_native_skip_cases']))
    mapping=dict(format='dk4-lil-speyer-source-relocation-map-v1',file_path='/data/SC2.DK4',
        required_runtime_ARM9_sha256=sha(arm),source_SC2_sha256=sha(parent.read_file('/data/SC2.DK4')),
        target_SC2_sha256=sha(target.read_file('/data/SC2.DK4')),clean_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),
        entry_point_offset=8,external_references_complete=True,preserve_record_parity=True,
        all137_nested_command_boundaries_and48_relative_sites_verified=True,
        all240_relocated_relative_skip_cases_preserve_original_targets=True,
        representative51_speech102_holds_and_two_choice_labels_approved=True,
        actual_speech_record_IDs=sorted(observed),offline_only_speech_record_IDs=sorted(unseen),blocks=blocks,
        actual_scope='51 revised B128 speeches,102 complete holds,both visible labels and original default choice0. B12897 fallback,two alternate-choice replies and all three B25 aftermath speeches are offline/source-native only. B74original79 captures remain unreviewed editorially.',
        conditional_risk_assessment='All six unvisited speeches use the same proven original progressive presenter; exact source preambles,native selectors,complete per-record fonts/macros and typed reference checks resolve display risks. No individual visit or forced aftermath claim.',
        evidence={p:sha(Path(p).read_bytes())for p in sorted(files)},
        not_registered_ROM_or_full_route_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(MAP,mapping)
    successor=deepcopy(doc)
    for row in successor['records']:
        compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,source_blocks[row['block']]))
        assert compiled.encoded.hex()==fonts[row['id']]['encoded_hex']
        row.update(compiled_hex=compiled.encoded.hex(),individually_activated_in_revised_sample=row['id']in observed,
            representative_actual_proof=str(ACTUAL))
        row['context']=row['context'].split('Newscene display/preamble scope,')[0]+(
            'Original controls,native layouts,typed choice dispatch and representative revised gameplay now pass; registered integration remains pending. Six speeches have source/native coverage without individual activation.')
    successor.update(status='source-native-and-representative-revised-approved;registered-integration-pending',
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        approved_reference_map=str(MAP),approved_reference_map_sha256=sha(MAP.read_bytes()),
        actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),
        scoped_profile_module='dk4tool/dialogue/lil_speyer_profile.py',
        scoped_control_proof='work/analysis/lil_Speyer_controls_v1936/source_bound_B25_B128_progressive_control_contract.json',
        native_font_source_manuscript_sha256=sha(OLD.read_bytes()),
        actual_revised_gameplay_and_registered_release_pending=False,registered_release_pending=True)
    menu_successor=deepcopy(menu)
    menu_successor.update(status='source-native-and-revised-menu-approved;registered-integration-pending',
        predecessor_manuscript=str(OLD_CHOICES),predecessor_manuscript_sha256=sha(OLD_CHOICES.read_bytes()),
        approved_reference_map=str(MAP),approved_reference_map_sha256=sha(MAP.read_bytes()),
        actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),registered_release_pending=True)
    for row in menu_successor['records']:
        row['context']+=' Both labels are visible in the revised native menu; default option0 was selected and returns native result0. Option1 retains source/native-VM coverage without individual selection.'
        row['localization_note']=row['localization_note'].replace('visible menu/result association still needs native dispatch proof.',
            'the revised visible menu and native result0/choice0 association are verified; choice1 is source/native-VM only.')
    validate_natural_dialogue_batch(successor)
    validate_natural_dialogue_batch(menu_successor)
    save(DOC,successor)
    save(CHOICES,menu_successor)
    save(ROOT/'final_source_reference_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        native_speeches=57,typed_choice_labels=2,complete_commands=137,relative_sites=48,target_native_skip_cases=240,
        actual_revised_speeches=51,actual_complete_speech_holds=102,actual_complete_choice_holds=2,
        offline_only_speeches=6,all_required_source_native_and_representative_gameplay_gates_passed=True,
        no_new_ROM_registry_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_native_revised_speeches=57,typed_labels=2,approved_commands=137,approved_spans=48,
        actual_speeches=51,offline_speeches=6,registered_release_pending=True))
