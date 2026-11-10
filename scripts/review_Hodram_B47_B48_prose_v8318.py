"""Whole-outcome editorial decisions from clean Japanese; formatting remains an independent gate."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B47_B48_prose_v8318')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v1.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v1.json')
CURRENT=Path('work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json')
DISPLAY=Path('work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json')
ARTIFACT=Path('work/analysis/Hodram_B48_artifact_identity_v8313/clean_notice_anditem148_established_Ullr_Bow_identity_not_current_dialogue_review.json')

DECISIONS={
 (47,6):('revision',"What?! You found it already? Argh!",'The clean line is surprised that the treasure has already been found and expresses frustrated disappointment. What?! and Argh! preserve Lil\'s emphatic outburst in natural speech. Remove That\'s not fair!, which invents an accusation of unfairness. State found it so the treasure-race callback remains clear.'),
 (47,10):('retention','You win... Oh well.','You win... Oh well. works as Lil\'s rueful concession followed by a resilient shrug. The ellipsis gives the admission a beat before her mood changes. In the complete exchange, the next line turns that defeat into competitive encouragement; no apology, friendship pledge or gift belongs here. Retain the natural existing wording.'),
 (47,13):('revision',"You beat me, so you'd better not lose to anyone else! You have to be the best in the world. I won't settle for less!",'The source links beating Lil to not losing to anyone else, then insists on becoming number one in the world and makes her refusal to accept less explicit. You\'d better and I won\'t settle for less preserve her forceful competitive encouragement. Restore in the world rather than leaving number one without its scope. This is an expectation of future achievement, not a claim of present world supremacy or an instruction to conquer territory.'),
 (48,6):('retention',"Lil Argot appears to have found Ullr's Bow!",'The existing system notice is clear, natural and accurate. Appears to have found retains the source ようです reporting qualification; Lil Argot and Ullr\'s Bow match the clean identity and established item148 name. The exclamation suits a discovery notice. It reports Lil\'s apparent discovery, not player acquisition or a completed transfer. Retain every word.'),
 (48,11):('retention','Hee hee. Too bad, {MACRO:FI}!','The light chuckle and teasing Too bad suit Lil\'s playful winning taunt and the source musical note. The existing punctuation conveys the lilting tone; the note is prose punctuation, not a runtime control or proof of literal singing. Keep the wording, preserve the real FI substitution through explicit markup, and do not add a rank or relationship for さん. This changes macro notation only, not the stored dialogue words.'),
 (48,14):('revision','Want it? Then wait in Amsterdam.','The source condition is wanting this, followed by an instruction for the addressee to wait in Amsterdam. Want it? Then wait keeps Lil\'s brisk taunting voice and the direction of that instruction. Meet me changes the requested action and adds an explicit meeting participant; the clean sentence does not say Lil is already waiting there. Preserve the destination and conditional invitation without promising a handover.'),
}
CONTEXTS={
 47:'One complete three-utterance outcome of the B46 treasure-finding challenge. Lil reacts with surprise and frustration, concedes with a shrug, then presses the person who beat her to become the best in the world. Her demands are competitive encouragement rather than proof of an alliance, romance or achieved world domination. Original event47 excludes completed48; outer eligibility and total chronology remain unproved.',
 48:'A separate complete race outcome begins with a system report of Lil\'s apparent discovery of Ullr\'s Bow. Original scene controls then lead into her light, teasing address to FI and her instruction that the addressee wait in Amsterdam if they want it. Preserve the notice-to-personal-dialogue transition, the uncertainty, the runtime addressee and the conditional destination. No player receipt, accepted bargain, current Amsterdam presence or completed handover is established. Event48 has no matching exclusion; do not infer mutual exclusion or a total chronology.',
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    current,display,artifact=map(read,[CURRENT,DISPLAY,ARTIFACT])
    assert current['source_display_proof_sha256']==sha(DISPLAY.read_bytes()) and len(current['records'])==len(DECISIONS)==6
    assert current['all_six_clean_first_whole_exchange_glosses_precede_current_English_exposure']
    rows=[]
    for original in current['records']:
        row=deepcopy(original);key=row['block'],row['source_record_index'];decision,text,reason=DECISIONS[key]
        old=row['effective_predecessor_paragraph'];comparison=text.replace('{MACRO:FI}','FI')
        assert (comparison==old)==(decision=='retention') and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD','%'])
        source=bytes.fromhex(row['source_hex'])[1:];assert source.count(b'FI')==text.count('{MACRO:FI}') and not any(m in source for m in [b'FA',b'FO'])
        assert all(32<=ord(c)<127 for c in text)
        row.update(english=text,logical_English=text,speaker='System' if row['source_selector']==254 else 'Lil Argot',
            source_meaning=row['first_clean_source_gloss'],context=CONTEXTS[row['block']]+' '+row['first_clean_source_gloss'],localization_note=reason,editorial_finding=reason,
            decision=decision,editorial_decision='revise' if decision=='revision' else 'retain',retention_reason=reason if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            complete_outcome_read_in_source_andEnglish_sequence=True,read_aloud_cadence_andemotional_progression_reviewed=True,
            source_note_count=source.decode('cp932').count('♪'),source_musical_note_function_expressed_in_current_playful_chuckle_andtaunt=key==(48,11),
            source_control_andruntime_substitutions_must_remain_exact=True,source_prose_orcompletion_credit_added=False,
            formatting_actual_effects_policy_andregistered_release_pending=True)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)==dict(revision=3,retention=3)
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,DISPLAY,ARTIFACT,Path(current['source_gloss']),Path(current['source_controls_proof']),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(NAMES,dict(format='dk4-source-context-speaker-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',route=1,route_identity='Hodram',source_gloss=current['source_gloss'],source_gloss_sha256=current['source_gloss_sha256'],
        records=[dict(actor_ID=2,source_given='リル',source_surname='アーゴット',current_name='Lil Argot',decision='retention',localization_reason=display['source_qualified_name_retention_reason'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),source_context_IDs=[r['id'] for r in rows if r['source_selector']==2],
            source_current_field_binding=display['clean_current_Lil_fields'],native_two_getters_andcomplete_style11_plane_reused_through_exact_current_code_font_actors=True,actual_new_scene_headers_pending=True)],
        system_FE_record_IDs=[r['id'] for r in rows if r['source_selector']==254],FE_is_not_actor254_orpersonal_name=True,full207_catalogue_UI_aliases_customnames_review_still_open=True,
        no_new_name_asset_orrenaming_oradditional_dialogue_credit=True,native_proof=str(DISPLAY),native_proof_sha256=sha(DISPLAY.read_bytes()),evidence=evidence,new_credit=0,full_goal_complete=False))
    save(DOC,dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC1.DK4',route=1,route_identity='Hodram',blocks=[47,48],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],
        records=rows,revised=3,retained=3,typed_choice_records=[],names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),source_context=current['source_gloss'],source_context_sha256=current['source_gloss_sha256'],source_current_effective_proof=str(CURRENT),source_current_effective_proof_sha256=sha(CURRENT.read_bytes()),
        source_controls_proof=current['source_controls_proof'],source_controls_proof_sha256=current['source_controls_proof_sha256'],source_display_proof=str(DISPLAY),source_display_proof_sha256=sha(DISPLAY.read_bytes()),
        source_item148_identity_proof=str(ARTIFACT),source_item148_identity_proof_sha256=sha(ARTIFACT.read_bytes()),source_macro_counts=dict(FI=1,FA=0,FO=0),source_note_count=1,
        all_six_four_prose_gates_true_all_formatting_gates_false=True,english_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=True,
        original15_commands_six_complete_preambles_one_FE_one_FI_andtwo_fourbyte_ends_to_preserve=True,one_source_musical_note_conveyed_by_retained_light_chuckle_no_new_singing_fact=True,
        no_invented_unfairness_rank_relationship_conquest_present_world_supremacy_player_acquisition_orhandover=True,
        both_complete_English_exchanges=[dict(block=b,context=CONTEXTS[b],records=[dict(id=r['id'],speaker=r['speaker'],english=r['english'],decision=r['decision']) for r in rows if r['block']==b]) for b in [47,48]],
        status='contextual-prose-reviewed-native-formatting-stored-controls-actual-effects-policy-registered-release-pending',new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence=evidence))
    save(ROOT/'six_contextual_decisions_three_revisions_three_justified_retentions.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),records=6,revisions=3,retentions=3,
        all_six_formatting_gates_pending=True,no_completion_credit_added=True,evidence=evidence,full_goal_complete=False))
    for r in rows:print(r['id'],r['decision'],r['english'])
