"""Whole B52 source/choice exchange: two revisions and three individually justified retentions."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_prose_v8632')
CURRENT=Path('work/analysis/Hodram_B52_current_v8631/current_effective.json')
GLOSS=Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')
DISPLAY=Path('work/analysis/Hodram_B52_source_display_v8626/source_display.json')
SOURCE_VIEW=Path('work/analysis/Hodram_B52_source_names_v8630/three_source_pages_role_andHayreddin_component_review.json')
VM=Path('work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')
TERM=Path('translations/lil_goods_mediterranean_editorial_manuscript_v6.json')
DOC=Path('translations/hodram_B52_editorial_manuscript_v1.json')
NAMES=Path('translations/hodram_B52_speaker_name_review_v1.json')

CONTEXT=('A gruff port worker asks whether the addressee intends to make an enemy of Hayreddin\'s group. '
    'The typed player choices deny that intention or confidently accept the prospect of opposition. '
    'On the source choice0 structural path, the worker tells the party to leave before being noticed and the normal166 end preserves the carried value. '
    'On choice1, the worker comments on the addressee\'s dangerous boldness and flagged224 returns kind1 while clearing the value. '
    'Original menu getters, provider sizes, bridged returns, caller forwarding, branch extents and both end contracts are bound offline; '
    'neither path is yet an actual controller visit or natural optional activation. Event52 requires30 and excludes74, but outer scheduling, '
    'original location and full chronology remain unexecuted. Numeric adjacency does not prove continuity with B51. '
    'The source supplies the named group, not an asserted blood relationship, government rank, nationality or crime.')

SPEECHES={
    6:dict(decision='revision',english="Are you planning to make an enemy of Hayreddin's outfit?",
        finding='The existing Will you oppose the Hayreddin family? makes the named group sound like a proven biological family and loses the conversational question about intention.',
        reason='Use the established Hayreddin component and outfit as an informal group term appropriate to the gruff port worker. The clean 一家 names the organization in this warning; the independently reviewed comparison of the player company with the same group also supports that organizational sense. Outfit changes no proper-name spelling and asserts no blood kinship, criminality, rank or new faction identity. Are you planning to make an enemy of preserves the question about intending opposition, rather than announcing existing hostility. Read with Not at all. and Bring it on., the question sets up two natural, distinct responses. Wording is chosen for meaning and voice; relocation and automatic full-width wrapping own fit.'),
    21:dict(decision='retention',english='Then get out before they notice you.',
        finding='The existing complete sentence already gives the source follow-up and prospective warning naturally.',
        reason='Retain the exact logical wording. Then follows the denial of an intention to oppose the group; the brisk, blunt get out conveys the colloquial さっさと引き上げな, and before they notice you preserves 見つからないうちに without adding capture, pursuit or a guaranteed escape. They refers naturally to the group just discussed. This is advice to withdraw, not a new official expulsion or proof of a particular building or town. Its complete sentence and urgent cadence sound natural after Not at all.; no revision is needed simply because this line is being revisited.'),
    33:dict(decision='revision',english="You've got a death wish, huh?",
        finding='A death wish. compresses the worker\'s conversational comment into a bare label.',
        reason='Restore a complete, colloquial reaction directed at the addressee. In this response to Bring it on., death wish is an idiomatic assessment of dangerous boldness for 命知らず, not a factual assertion that the player wants to die. The contraction and huh? express the casual commenting だねえ in American English. Preserve the danger implied by the source without adding a threat, promised death, admiration, past feat or battle outcome. Read aloud as the worker\'s reaction, it remains distinct from the preceding withdrawal advice.'),
}
CHOICES={
    0:dict(decision='retention',english='Not at all.',
        finding='The current wording is a natural denial; its three trailing ASCII spaces are storage padding rather than prose.',
        reason='Retain Not at all. as the concise, idiomatic answer denying the intention in the worker\'s question, for そんな気はない. It leads naturally to Then get out before they notice you. and does not assert surrender, allegiance or a new relationship. Preserve the old padded bytes as evidence. The typed-table compiler owns terminators, offset words and alignment; removing storage-only spaces does not change this editorial wording or earn a second review credit. Complete menu centering, bounds and controller behavior remain to be checked.'),
    1:dict(decision='retention',english='Bring it on.',
        finding='The existing choice already conveys confident willingness to face the prospective opponent in natural American English.',
        reason='Retain the exact logical wording for 相手になろう. As the affirmative alternative to Not at all., Bring it on. accepts the prospect of opposing the group with a short, confident challenge. It is an idiomatic player choice, not proof that battle has started, a victory promise or a statement of an invented relationship or rank. The worker\'s following comment about dangerous boldness responds naturally to this confidence. The label remains typed UI rather than an independently spoken Hodram nameplate line.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    current,gloss,display,view,vm,term=map(read,[CURRENT,GLOSS,DISPLAY,SOURCE_VIEW,VM,TERM])
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==7229 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert current['all5_source_units_uncredited_in_current_ledger'] and current['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert len(current['records'])==3 and len(current['typed_choices'])==1 and len(current['typed_choices'][0]['records'])==2
    assert view['all_three_complete_Japanese_speech_pages_andone_reused_role_plane_directly_viewed'] and vm['reused_original_kind2_value_forwarding_kind3_carry_cases']==50
    termrows=[r for r in term['records'] if r['id'] in ['DK4_MES_B44_R0055','DK4_MES_B44_R0102']]
    assert len(termrows)==2 and all('ハイレディン一家' in r['source_Japanese'] and "Hayreddin's clan" in r['english'] for r in termrows)
    allsource=current['records']+current['typed_choices'][0]['records'];completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert len(completed)==7229 and not completed&{historical_key(r) for r in allsource}
    rows=[];choices=[]
    for original in allsource:
        row=deepcopy(original);typed=row['kind']=='typed-choice';choice=CHOICES[row['option_index']] if typed else SPEECHES[row['source_record_index']]
        text=choice['english'];old=row['current_effective_paragraph'] if typed else row['effective_predecessor_paragraph']
        assert (text==old)==(choice['decision']=='retention')
        assert text==text.strip() and not any(v in text for v in ['\n','\r','{LB','{ALIGN','{PAD','  ','%'])
        if not typed:assert row['source_selector']==113 and not any(m in bytes.fromhex(row['source_hex'])[1:] for m in [b'FI',b'FA',b'FO'])
        row.update(english=text,logical_English=text,speaker='Hodram (player choice)' if typed else 'Port Worker',source_meaning=row['first_clean_source_gloss'],context=CONTEXT,localization_note=choice['reason'],finding=choice['finding'],decision=choice['decision'],retention_reason=choice['reason'] if choice['decision']=='retention' else None,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),whole_exchange_andboth_choice_response_paths_read=True,read_aloud_cadence_andemotional_progression_reviewed=True,prior_raw_storage_preserved=row['current_raw_storage_English'],prior_effective_paragraph_preserved=old,no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,source_controls_runtime_substitutions_andtyped_choices_must_remain_exact=True,formatting_native_stored_actual_policy_atomic_andregistered_integration_pending=True,source_prose_orcompletion_credit_added=False)
        if not typed:row['planned_English_markup']='{SPEAKER:71}'+text
        (choices if typed else rows).append(row)
    allrows=rows+choices
    assert len(allrows)==len({historical_key(r) for r in allrows})==5 and Counter(r['decision'] for r in allrows)==dict(revision=2,retention=3)
    role=view['scoped_role_review'];component=view['mentioned_component_review']
    save(NAMES,dict(format='dk4-scoped-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=[dict(actor_ID=113,speaker='Port Worker',decision='retention',context=CONTEXT,retention_reason=role['reason'],localization_note=role['reason'],exact_source_current_native_binding=role['source_andcurrent_fields_andreused_consumers'],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),complete_unchanged_native_role_plane_directly_viewed=True,actual_B52_header_binding_pending=True)],mentioned_components=[dict(**component,context=CONTEXT,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),same_named_group_outfit_is_common_noun_not_new_proper_name=True)],scoped_actor_IDs=[113],mentioned_actor_IDs=[34],source_name_review=str(SOURCE_VIEW),source_name_review_sha256=sha(SOURCE_VIEW.read_bytes()),player_choice_labels_are_typed_UI_not_spoken_nameplate_lines=True,no_new_name_asset_orall207_name_review_credit=True,wider_Port_Worker_other_contexts_full_names_aliases_catalogue_andcustom_names_pending=True,new_credit=0,full_goal_complete=False))
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='natural-dialogue',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC1.DK4',route=1,route_identity='Hodram',blocks=[52],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],records=rows,typed_choice_records=choices,total_editorial_objects=5,physical_speech_objects=3,typed_choice_objects=2,revised=2,retained=3,names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),source_menu_andstructural_paths=str(VM),source_menu_andstructural_paths_sha256=sha(VM.read_bytes()),approved_named_component=dict(english='Hayreddin',source='ハイレディン',exact_component_review=component),group_sense_comparison_evidence=dict(path=str(TERM),sha256=sha(TERM.read_bytes()),records=[dict(id=r['id'],source_reference=r['source_reference'],source_Japanese=r['source_Japanese'],reviewed_English=r['english']) for r in termrows],wording_note='The same organization can be described as clan in a formal capability comparison and outfit in this gruff warning. Neither source establishes blood kinship; this is common-noun voice variation, not a new faction name.'),source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=0,source_relative_sites=4,source_query_sites=0,source_opaque_commands=4,source_distinct_end_words=['00000000','00000080'],source_native_opaque_scope_not_effect_semantics_oractivation=True,all3_speeches_andtwo_choices_clean_first_glossed_before_current_English=True,whole_exchange_andchoice_context_reviewed=True,all_four_prose_gates_true_all_formatting_gates_false=True,ordinary_wrapping_owned_by_formatter=True,no_new_ROM_registered_integration_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'contextual_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),records=[dict(id=r['id'],source_reference=r['source_reference'],source_hex=r['source_hex'],current_reference=r['current_reference'],current_hex=r['current_hex'],prior=r['prior_effective_paragraph_preserved'],english=r['english'],decision=r['decision'],finding=r['finding'],reason=r['localization_note']) for r in sorted(allrows,key=lambda r:r['source_reference']['offset'])],revisions=2,individually_justified_retentions=3,complete_editorial_objects=5,scoped_role_retentions=1,mentioned_name_component_retentions=1,all_four_prose_gates_true_all_formatting_gates_false=True,exact_source_current_refs_two_canonical_choice_IDs_andold_padding_preserved=True,no_native_formatting_actual_branch_fullroute_hardware_orregistered_credit_claim=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,GLOSS,DISPLAY,SOURCE_VIEW,VM,TERM,DOC,NAMES,Path(__file__)]}))
    for row in sorted(allrows,key=lambda r:r['source_reference']['offset']):print(row['id'],row['decision'],repr(row['english']))
    print('B52 contextual prose: two revisions/three justified retentions; four prose gates true, formatting false. Role and mentioned name reviewed; no ROM orcompletion credit.')
