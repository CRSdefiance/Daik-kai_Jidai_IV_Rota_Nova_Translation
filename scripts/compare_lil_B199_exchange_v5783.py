"""Reconcile complete clean context and actual source observations with prior English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_comparison_v5783')
SOURCE=Path('work/analysis/lil_B199_source_v5767/all31_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B199_clean_context_v5765/all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json')
ACTUAL=Path('work/analysis/lil_B199_source_paths_v5782/one_actual_source_path_and_complete_command_intervals.json')
DISPATCH=Path('work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json')
CONTROLS=Path('work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json')
NAMES=Path('work/analysis/lil_B199_names_v5772/six_original_progressive_and_catalogue_name_consumers.json')
NAME_FIELDS=Path('work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json')
CAPTION=Path('translations/common_scene_labels_manuscript_v1.json')
PROGRESSION=(
 'Samwell asks Camille who the man in a portrait is and whether he is famous. Camille identifies Rocco Alemkel '
 'and gives a qualified assessment of his reputation among navigators. Impatient Lil interrupts and announces '
 'she is going ahead. Camille apologizes; Samwell promises to follow and provokes Lil with an explicit body-size '
 'taunt. Her retaliation starts a comic chase with four impact sounds. Camille calls the runtime FI name, '
 'complains about thrown objects and reacts with Ow. Samwell taunts the thrower and Lil pursues him. '
 'Camille grumbles about always having to clean up, notices something and judges a book to look very old. '
 'Lil calls him onward. His question about Samwell receives her irritated dismissal; his private thought '
 'infers another escape. She challenges his grin and he stammers an apology, redirecting her to the found object. '
 'She asks if it is a gift and continues with that interpretation despite two unfinished corrections. '
 'Her delight at the unusual present turns into thanks and a renewed invitation to go. Camille yields awkwardly '
 'and privately wonders whether that was okay. No deliberate gift purchase, settled ownership or romance is established.'
)

if __name__=='__main__':
    assert not ROOT.exists()
    packet,gloss,actual,dispatch,controls,names,fields,caption=map(read,[SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS,CAPTION])
    assert gloss['prior_English_speech_unread'] and len(gloss['records'])==31
    indices=[r['source_record_index'] for r in packet['records']]
    assert actual['selected_source_speech_indices']==indices and not actual['unvisited_source_indices']
    assert actual['source_end1162_return_frame']==10776 and actual['total_frames']==13001
    assert len(actual['command_pairs'])==56 and not actual['source_predicate_observations']
    assert actual['source_effect_offsets_executed']==[1152]
    assert len(controls['all16_source_current_nonspeech_leaves'])==16
    assert len(names['native_six_consumer_cases']['rows'])==6
    assert len(fields['B199_clean_name_fields'])==3
    sheets=actual['review_sheets']+actual['transition_sheets']
    assert len(sheets)==10
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        sheet.update(viewed_in_full_current_turn=True,original_detail=True)
    rows=[]
    for r in packet['records']:
        row=deepcopy(r);raw=bytes.fromhex(r['current_hex']);body=raw[1:].decode('cp932')
        assert raw[0]==r['source_selector']
        current=next(x for x in dispatch['speech_dispatch_cases'] if x['id']==r['id'] and x['version']=='current-English')
        assert current['registered_catalog_match'] is None
        expanded=body.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
        assert current['boundaries'][1]['text_hex']==expanded.encode('cp932').hex()
        paragraph=' '.join(body.split())
        observation=next(x for x in actual['speech_observations'] if x['id']==r['id'])
        assert observation['selected_capture'] is not None
        row.update(previous_display_body=body,previous_paragraph=paragraph,previous_macro_template_paragraph=paragraph,
            previous_effective_runtime_paragraph=' '.join(expanded.split()),previous_bytes_retained_for_exact_comparison=True,
            actual_source_fixture_observed=True,actual_source_paths=['complete_linear_source'],source_actual_observation=observation,
            clean_first_whole_exchange_gloss_precedes_old_English_comparison=True,
            prior_English_is_comparison_only_not_translation_source=True)
        rows.append(row)
    portrait=next(r for r in caption['records'] if r['id']=='COMMON_MESSAGE_3534')
    assert portrait['japanese']=='ロッコの肖像画' and portrait['english']=="Rocco's Portrait{PAD}"
    assert rows[1]['source_Japanese']=='その人は、ロッコ＝アレムケルって\n人だよ'
    assert rows[1]['previous_paragraph']=="That's Rocco Alemkel."
    ROOT.mkdir(parents=True)
    context=ROOT/'complete_clean_context_actual_source_and_project_name_reconciliation.json'
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,ACTUAL,DISPATCH,CONTROLS,NAMES,NAME_FIELDS,CAPTION,Path(__file__)]}
    save(context,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        complete_exchange_progression=PROGRESSION,approved_prose_names={'2':'Lil','9':'Camille','22':'Samwell'},
        portrait_subject_name=dict(Japanese='ロッコ＝アレムケル',project_English='Rocco Alemkel',
            given_name_existing_source_caption=portrait,source_dialogue_ID=rows[1]['id'],
            surname_basis='Existing project spelling Alemkel is consistent with the clean アレムケル; retain as the game name.',
            no_external_historical_identity_or_official_Latin_name_claim=True),
        source_name_fields=fields['B199_clean_name_fields'],Samwell_untranslated_full_catalogue_middle_field_remains_open=True,
        source_FE_four_impacts_not_stat_notice_or_named_speaker=True,
        original_FI_one_runtime_name_preserved=True,private_parentheses_source_indices=[70,115],
        source_book_card_observed=['Rocco\'s Sailing Guide','Equipment','Helmsman'],
        spoken_book_stays_unnamed_no_new_item_title_or_widget_fidelity_credit=True,
        source_portrait_name_absence_and_distinct_picture_layouts_preserved=True,
        source_actual_paths=str(ACTUAL),source_actual_paths_sha256=sha(ACTUAL.read_bytes()),
        source_actual_speeches=31,offline_only_speeches=[],source_end1162_return_frame=10776,
        source_content_fixture_cold_boot_frames=13001,viewed_source_sheets=sheets,
        source_roster_funds_RNG_conditions_and_effect_results_unforced=True,
        initialized_Amsterdam_B22_fixture_not_natural_event199_activation_original_location_full_route_or_hardware=True,
        no_new_ROM_or_run_beyond_the_already_recorded_source_fixture=True,new_review_credit=0,
        evidence=evidence,full_goal_complete=False))
    save(ROOT/'all31_complete_clean_and_predecessor_exchange.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=rows,
        contextual_reconciliation=str(context),contextual_reconciliation_sha256=sha(context.read_bytes()),
        current_registered_catalog_matches=0,source31_complete_glosses_before_previous_English=True,
        current_English_prior_comparison_only=True,all31_previous_current_stored_runtime_and_logical_refs_exact=True,
        no_editorial_completion_or_source_prose_credit_added=True,evidence=evidence,full_goal_complete=False))
    print('31 source/current paragraphs reconciled;all31 Japanese panels observed,ten source sheets viewed. Project Rocco Alemkel retained;English layout/release pending.')
