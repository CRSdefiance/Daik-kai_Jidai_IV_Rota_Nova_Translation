"""Approve B26 map after full native checks and representative revised gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_approval_v1907')
OLD=Path('translations/lil_london_editorial_manuscript_v4.json')
DOC=Path('translations/lil_london_editorial_manuscript_v5.json')
MAP=Path('translations/lil_london_editorial_relocation_map_v1.json')
RELOC=Path('work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_London_reference_census_v1905/all262_commands92_relative_sites_and_shipped_entry_census.json')
ACTUAL=Path('work/analysis/lil_London_revised_audit_v1906/revised_London105_branch_and_three_fixture_audit.json')
SOURCE=Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
PARITY=Path('work/analysis/lil_London_FE_parity_v1900/all3_final_FE_parity_native_planes.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not MAP.exists()
    doc,reloc,census,actual,source,parity=map(read,(OLD,RELOC,CENSUS,ACTUAL,SOURCE,PARITY))
    assert len(doc['records'])==111 and len(reloc['mapped_commands'])==262 and len(reloc['relative_skip_fixups'])==92
    assert census['all262_commands_reexecuted_clean_current_and_target']
    assert census['all92_typed_span_sites_and460_target_native_cases_preserve_destinations']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert census['only_original24070_interpreter_call_no_literal_alias']
    assert parity['all3_complete_padded_targets_one_native_page_and_pixel_exact']
    assert actual['all105_activated_revised_speeches210_holds_complete_native_independent_actual_glyphs']
    assert actual['same228_original_commands_results_and_event_transitions']
    assert actual['normal_docking_B26_entry_and_terminal_return_not_injected']
    observed={r['id'] for r in actual['revised_speech_observations']}
    unseen=set(actual['unvisited_original_speech_IDs'])
    assert len(observed)==105 and len(unseen)==6 and observed|unseen=={r['id'] for r in doc['records']}
    assert not observed&unseen
    ROOT.mkdir(parents=True)
    # The control contact sheet was authored during a growing observation log.
    # Reconstruct that exact historical prefix rather than silently treating its
    # recorded hash as a hash of the later, longer LIVE file.
    sheet_proof=Path('work/analysis/lil_London_control_sheet_v1890b/contact_sheet_provenance.json')
    sheet=read(sheet_proof)
    original=read('work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json')
    prefix=dict(rows=original['old_text_observations'][:19],art_pauses=original['source2000_interstitials'][:1],
        next_pause_frame=56040,not_terminal_or_revised_prose_approval=True)
    historical=ROOT/'historical_first19_original_observations.json'
    save(historical,prefix)
    assert sha(historical.read_bytes())==sheet['navigation_sha256']
    old_by={r['id']:r for r in original['old_text_observations']}
    assert all(old_by[r['id']]==r for r in sheet['rows'])
    visual=ROOT/'representative_actual_visual_approval.json'
    save(visual,dict(all4_representative_revised_sheets16_panels_actually_viewed=True,
        full_Clifford_portrait_nameplate_three_anonymous_FE_panels_and_macro_substitutions_viewed=True,
        clothing_joke_dinner_long_four_row_paragraphs_andnormal_London_return_viewed=True,
        automated_all210_full_actual_native_holds_separate_from16_visual_samples=True,
        six_conditional_speeches_not_individually_activated=True,
        original_control_sheet_historical19_prefix_reconstructed_exactly=True,
        evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(historical):sha(historical.read_bytes()),
            **{p:sha(Path(p).read_bytes()) for p in actual['representative_contact_sheets']}},full_goal_complete=False))
    files={str(p) for p in (OLD,RELOC,CENSUS,ACTUAL,SOURCE,PARITY,visual,historical,sheet_proof,Path(__file__))}
    files.update((doc['source_context'],doc['native_font_proof'],doc['visual_review'],doc['scoped_profile_module'],doc['scoped_control_proof']))
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
    font=read(doc['native_font_proof'])
    for case in font['cases']:
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        files.add(case['preview'])
    mapping=dict(format='dk4-lil-london-source-relocation-map-v1',file_path='/data/SC2.DK4',block=26,
        required_runtime_ARM9_sha256=source['ARM9_sha256'],source_block_sha256=reloc['source_block_sha256'],
        clean_block_sha256=source['clean_block_sha256'],target_block_sha256=reloc['research_block_sha256'],
        entry_point_offset=8,external_references_complete=True,preserve_record_parity=True,
        all262_original_commands_and92_typed_spans_approved=True,
        representative_actual105_and_offline111_scope_approved=True,
        records=reloc['text_records'],commands=census['mapped_commands'],relative_skip_fixups=reloc['relative_skip_fixups'],
        actual_record_IDs=sorted(observed),offline_only_conditional_record_IDs=sorted(unseen),
        all111_native_planes888_macro_cases_460_relocated_native_spans_and_inverse_pass=True,
        conditional_risk_assessment='Five Gerhard10 andoneRetainer97 object remainoffline-only. Source-bound sharedpresenters andcomplete per-record native checks resolve display/control risks;no individual visits claimed.',
        evidence={p:sha(Path(p).read_bytes()) for p in sorted(files)},
        not_registered_ROM_orfull_route_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(MAP,mapping)
    successor=deepcopy(doc)
    successor.update(encoder='dialogue-relocatable-v1',status='all111-source-native-andrepresentative-revised-gameplay-approved;registered-integration-pending',
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        approved_reference_map=str(MAP),approved_reference_map_sha256=sha(MAP.read_bytes()),
        actual_visual_review=str(ACTUAL),actual_visual_approval=str(visual),
        fixed_encoder_is_allocation_probe_only_until_complete_reference_map=False)
    for row in successor['records']:
        row['english']=row['english'].removesuffix('{PAD}')
        row['individually_observed_in_revised_gameplay']=row['id'] in observed
        row['context']=row['context'].replace('revised gameplay,typed relocation andregistered integration remainpending.',
            'Revised105-speech gameplay210 complete native/actual holds andtyped relocation pass;registered integration ispending. Six conditional speeches haveoffline native/source coverage only.')
    validate_natural_dialogue_batch(successor)
    save(DOC,successor)
    save(ROOT/'final_source_reference_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        all111_contextual_source_prose_andnative_display_approved=True,
        representative_actual105_speeches210_holds_andnormal_return=True,
        conditional_offline_only=6,proposed_revisions=81,justified_retentions=30,
        registered_ROM_patch_startup_andcompletion_credit_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(approved_B26_records=111,actual_revised_speeches=105,conditional_offline=6,
        complete_commands=262,typed_spans=92,historical_contact_sheet_prefix_reconstructed=True))
