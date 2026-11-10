"""Compare old English only after the complete clean exchange and source screens."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_comparison_v5838')
SOURCE=Path('work/analysis/lil_B200_source_v5826/all19_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B200_clean_context_v5825/all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json')
ACTUAL=Path('work/analysis/lil_B200_source_paths_v5837/one_actual_source_path_and_complete_command_intervals.json')
DISPATCH=Path('work/analysis/lil_B200_dispatches_v5828/all19_source_current_dispatches_no_macros_and12_control_leaves.json')
CONTROLS=Path('work/analysis/lil_B200_controls_v5833/twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json')
NAMES=Path('work/analysis/lil_B200_names_v5831/four_original_progressive_and_catalogue_name_consumers.json')
NAME_FIELDS=Path('work/analysis/collapsed_speaker_lead_v5832/all_route_literal_uses_exact_name_fields_and_localization_finding.json')
HELP=Path('translations/general_help_manuscript_v2.json')
TERMS=Path('guide/research/player-terminology-reference.json')
PROGRESSION=(
    'A collapse sound alarms Carlo. The other person groans and Carlo urgently checks what happened and '
    'whether the person is all right. Original controls transition to an inn room. The stranger stirs, '
    'Carlo recognizes consciousness,and the stranger asks where this is. Carlo explains that the person '
    'had collapsed at the port and was brought to the inn. The stranger apologizes for the trouble. '
    'Carlo reassures the stranger,remarks on their unwell appearance,advises rest and politely prepares '
    'to leave. Called back and asked whether he is a doctor,Carlo explicitly says no. The stranger '
    'offers an unnamed thank-you gift. Carlo initially declines. The stranger insists,Carlo accepts '
    'and repeats a caution to take care. The stranger agrees and thanks him. A separate FE notice '
    'states that Carlo\'s Charm increases by1. No specific diagnosis,carrying method,medical credentials, '
    'spoken book title,romance,kinship,payment or new occupation is established.'
)
if __name__=='__main__':
    assert not ROOT.exists();packet,gloss,actual,dispatch,controls,names,fields=map(read,[SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS])
    assert gloss['prior_English_speech_unread'] and len(gloss['records'])==19
    indices=[r['source_record_index'] for r in packet['records']]
    assert actual['selected_source_speech_indices']==indices and not actual['unvisited_source_indices']
    assert actual['source_end926_return_frame']==7676 and actual['total_frames']==13001
    assert len(actual['command_pairs'])==40 and not actual['source_predicate_observations']
    assert actual['source_effect_offsets_executed']==[906,914] and len(controls['all12_source_current_nonspeech_leaves'])==12
    assert len(names['native_four_consumer_cases']['rows'])==4
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'19':'Carlo Sinat','172':'Collapsed Person'}
    own=next(b for b in fields['selected_native_blocks'] if b['file_path']=='/data/SC2.DK4' and b['block']==200)
    assert len(fields['selected_native_blocks'])==4 and fields['source_blocks_scanned']==1307
    copies=[]
    for b in fields['selected_native_blocks']:
        assert [r['source_hex'] for r in b['all_speech_records']]==[r['source_hex'] for r in own['all_speech_records']]
        assert b['all_native_commands']==own['all_native_commands']
        reference,value=bytes.fromhex(own['source_block_hex']),bytes.fromhex(b['source_block_hex'])
        differences=[i for i,(a,c) in enumerate(zip(reference,value,strict=True)) if a!=c]
        assert differences==([2] if b['file_path']=='/data/SC3.DK4' else [])
        copies.append(dict(file_path=b['file_path'],block=b['block'],direct_role_speeches=8,whole_exchange_speeches=19,
            all_speech_bytes_complete_preambles_and_commands_equal_B200=True,noncommand_header_difference_offsets=differences))
    source_names={r['actor_ID']:r['source_fields'] for r in fields['source_name_fields']}
    assert [f.get('Japanese') for f in source_names[19]]==['カルロ','シナート',None]
    assert [f.get('Japanese') for f in source_names[172]]==['行き倒れ','アフリカ水夫',None]
    port=next(r for r in read(HELP)['records'] if r['id']=='HELP_TOPIC_11')
    assert '[[73|出港所]]' in port['source_Japanese_with_link_IDs'] and '[[73|Port]]' in port['english']
    charm=next(r for r in read(TERMS) if r['japanese']=='魅力');assert charm['english']=='Charm'
    sheets=actual['review_sheets']+actual['transition_sheets'];assert len(sheets)==8
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];sheet.update(viewed_in_full_current_turn=True,original_detail=True)
    binding_path=Path(dispatch['registered_catalog_binding']);binding=read(binding_path)
    assert sha(binding_path.read_bytes())==dispatch['registered_catalog_binding_sha256'];rows=[];matched=[]
    for r in packet['records']:
        row=deepcopy(r);raw=bytes.fromhex(r['current_hex']);body=raw[1:].decode('cp932');assert raw[0]==r['source_selector']
        current=next(x for x in dispatch['speech_dispatch_cases'] if x['id']==r['id'] and x['version']=='current-English')
        match=current['registered_catalog_match'];effective=body;entry=None
        if match is not None:
            entry=binding['records'][match['table_index']]
            assert entry['key_hex']==raw[1:].hex() and entry['route_mask']&4
            assert dict(owner=['/data/SC2.DK4',r['id']],form='body') in entry['requests']
            effective=bytes.fromhex(entry['target_hex']).decode('cp932');matched.append(r['id'])
        expanded=effective.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
        assert current['boundaries'][1]['text_hex']==expanded.encode('cp932').hex()
        paragraph=' '.join(effective.split());observation=next(x for x in actual['speech_observations'] if x['id']==r['id'])
        assert observation['selected_capture'] is not None
        row.update(previous_raw_storage_body=body,previous_effective_template_body=effective,previous_registered_catalog_match=match,
            previous_registered_catalog_entry=entry,previous_display_body=effective,previous_paragraph=paragraph,previous_macro_template_paragraph=paragraph,
            previous_effective_runtime_paragraph=' '.join(expanded.split()),previous_bytes_retained_for_exact_comparison=True,
            actual_source_fixture_observed=True,actual_source_paths=['complete_linear_source'],source_actual_observation=observation,
            clean_first_whole_exchange_gloss_precedes_old_English_comparison=True,prior_English_is_comparison_only_not_translation_source=True)
        rows.append(row)
    ROOT.mkdir(parents=True);context=ROOT/'complete_clean_context_source_scene_names_role_label_and_terms.json'
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS,HELP,TERMS,binding_path,Path(__file__)]}
    save(context,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_exchange_progression=PROGRESSION,
        approved_prose_names={'19':'Carlo','172':'Stranger'},source_name_fields=fields['source_name_fields'],source_role_exact_cross_route_copies=copies,
        actor19_Carlo_Sinat_existing_project_spelling_retained_from_clean_fields=True,
        actor172_label_localization_draft=dict(current='Collapsed Person',proposed='Stranger',source='行き倒れ',
            reason='The label identifies an anonymous person in a collapse/rescue scene. Collapsed Person sounds like an internal condition and remains after the person wakes. Stranger is natural throughout the full exchange and preserves anonymity without adding age,gender,nationality,occupation,diagnosis or a relationship. All four directly observed literal route copies have the same complete19 speeches and native commands;SC3 differs only in header byte2.',
            source_secondary_field='アフリカ水夫',secondary_field_retained_as_evidence_not_silently_promoted_to_player_label=True,
            current_progressive_and_full_getters_bound=True,original_source_portrait_and_current_label_observed=True,
            target_not_encoded_or_applied=True,target_native_display_substitution_consumer_and_registered_release_pending=True,new_name_completion_credit=0),
        Port_term_source_reference=f'{HELP}#/records/{read(HELP)["records"].index(port)}',Charm_term=charm,
        source_FE_impact_index=5,source_FE_stat_notice_index=72,source_FI_FA_FO_counts={'FI':0,'FA':0,'FO':0},
        explicit_not_a_doctor_denial_preserved=True,source_book_card_observed=['Canon of Medicine','Equipment','Surgeon'],
        spoken_thankyou_object_stays_unnamed_no_new_item_title_widget_or_full_effect_fidelity_credit=True,
        source_portrait_name_absence_and_outdoor_inn_picture_and_stat_transitions_preserved=True,
        source_actual_paths=str(ACTUAL),source_actual_paths_sha256=sha(ACTUAL.read_bytes()),source_actual_speeches=19,offline_only_speeches=[],
        source_end926_return_frame=7676,source_content_fixture_cold_boot_frames=13001,viewed_source_sheets=sheets,
        source_roster_funds_RNG_conditions_and_effect_results_unforced=True,
        initialized_Amsterdam_B22_fixture_not_natural_event200_activation_original_location_full_route_or_hardware=True,
        no_new_ROM_or_run_beyond_the_already_recorded_source_fixture=True,new_review_credit=0,evidence=evidence,full_goal_complete=False))
    save(ROOT/'all19_complete_clean_and_predecessor_exchange.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=rows,
        contextual_reconciliation=str(context),contextual_reconciliation_sha256=sha(context.read_bytes()),current_registered_catalog_matches=len(matched),
        current_registered_catalog_matched_IDs=matched,source19_complete_glosses_before_previous_English=True,current_English_prior_comparison_only=True,
        all19_previous_current_stored_runtime_and_logical_refs_exact=True,no_editorial_completion_or_source_prose_credit_added=True,evidence=evidence,full_goal_complete=False))
    for r in rows:print(r['source_record_index'],r['previous_paragraph'])
    print('19 source/runtime paragraphs reconciled after all8 Japanese sheets viewed;Stranger draft pending target validation. Current catalog matches',len(matched),'No credit.')
