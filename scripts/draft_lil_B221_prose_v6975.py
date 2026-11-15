"""Review both Crusades responses and the complete Saladin exchange from clean glosses."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B221_prose_v6975')
SOURCE=Path('work/analysis/lil_B221_source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice.json')
CURRENT=Path('work/analysis/lil_B221_consumers_v6968/fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers.json')
CONTEXT=Path('work/analysis/lil_B221_clean_context_v6965/all14_clean_speeches_two_choice_labels_Crusades_Saladin_glosses_before_old_English.json')
OUTPUT=Path('translations/lil_B221_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_B221_choice_manuscript_v1.json')
NAMES=Path('translations/lil_B221_speaker_name_review_v1.json')

DECISIONS={
5:("Hey, you! Don't just pass through our square!",'retain-wording','The existing brusque call and challenge sound natural as the shopkeeper stops a passerby. Our square conveys local identification with this town square; the command does not establish a toll, purchase requirement or guard authority. Lil\'s following Why/what-is-here response connects naturally to the interruption.'),
8:("Why? What's here?",'retain-wording','The two existing short questions are natural practical replies to being stopped. Why asks why she should stop, and what-is-here preserves her question about the town. Their conversational compression keeps her direct curiosity without inventing hostility or a known attraction.'),
11:('Do you know about the Crusades?','revise','Use the natural know-about construction for an event instead of the clipped Know the Crusades. This complete spoken question supports both following Yes/No answers without changing the historical subject or the original menu order.'),
27:('Hmph. A chivalrous army fighting to retake the Holy Land, right?','revise','Preserve the pointed favorable-account challenge in the known-answer branch. Army preserves 軍 and chivalrous preserves 騎士道を重んじた without recasting every member as a knight or inventing individual ranks. Retake preserves 奪回. The sarcastic checking tag leads into his accusation; it is not narrator endorsement.'),
33:('Hmph. In Europe, they apparently call them a chivalrous army that fought to retake the Holy Land...','revise','Keep the alternative branch\'s explicit European attribution and reported apparently framing. Army/chivalrous retains the source collective and value without assigning knight rank to its members. The trailing thought connects to the shared rebuttal rather than merging mutually exclusive responses into one observed exchange.'),
39:('All convenient lies! People here know what the Crusaders were really like.','retain-wording','The existing angry exclamation and complete local-knowledge claim are natural American speech here. All preserves his blanket rejection and people here preserves the town viewpoint. Keep the bitter accusation as this shopkeeper\'s claim, without an independent historical certification or an added religion/population.'),
42:('How so?','retain-wording','The existing idiomatic request for explanation naturally follows the accusation. It conveys Lil\'s どういうこと without a stiff literal repeat, agreement with the shopkeeper or new historical knowledge.'),
46:("I've heard a little about it too. They were after this region's wealth, right? Plunder, slaughter... anything went along the way, so I hear.",'revise','Restore a complete I-have-heard report, the real-objective question and the source\'s anything-went accusation. Keep both plunder and slaughter and the reported-so-I-hear status. This is Al\'s report and checking question to the local speaker, not added battles, victims, dates or narrator-certified history.'),
49:("I can't stand having history twisted to suit them and passed down like that! Our true hero is Saladin, not those Crusaders!",'revise','Restore the indignation about conveniently rewritten history being passed down. Contrast Saladin with the Crusaders collectively rather than narrowing the rejection to one Crusader. Our true hero preserves the speaker\'s local identification and proud declaration without inventing kinship, nationality, religious office or an outside biography.'),
52:("Saladin? Who's he?",'retain-wording','The existing two direct questions naturally convey Lil not recognizing the name. The masculine pronoun follows the source characterization in the same exchange and adds no personal acquaintance or agreement with an account she has not heard.'),
56:('He was a great figure in Islamic history. And he did far more than drive back the Crusaders.','revise','Use complete conversational sentences to introduce Al\'s explanation, retain the explicit Islamic-history context and preserve the more-than-driving-back point. Islamic history describes the named historical context; do not append Islam as the shopkeeper\'s personal name or insert a title, dynasty, date or independently researched achievement.'),
60:('He was humane in battle, in his treatment of prisoners and civilians, and in his peace terms. A fine man who never stooped to dirty tricks.','revise','Preserve all three concrete areas: fighting, treatment of prisoners/ordinary people and terms of peace. Peace terms restores 和睦の条件 instead of reducing it to peace talks. The final spoken apposition naturally reinforces Al\'s admiration in the complete exchange. His categorical praise remains his characterization; add no modern legal certification or extra achievement.'),
63:('Strong and a good person too? Amazing! What a hero!','retain-wording','The existing enthusiastic question and two admiring exclamations work naturally for Lil. They preserve her excitement that strength goes with good character, and What a hero echoes the hero just introduced in the exchange. Do not convert the admiration into romance, personal acquaintance, an oath or a promised gameplay benefit.'),
67:("Come to think of it, I once heard that Saladin's armor had gone missing. If you want to follow his example, why not look for it?",'revise','Restore Al remembering a report he once heard, then making a conditional suggestion tied to Lil\'s admiration. Saladin\'s armor is the ordinary possessive source phrase, not a new global item-title decision. Preserve missing status and uncertainty; do not assert acquisition, location, coordinates, an armor stat or a guaranteed benefit from possessing it.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [OUTPUT,CHOICES,NAMES])
    packet,current,context=map(read,[SOURCE,CURRENT,CONTEXT])
    assert packet['all14_clean_speech_glosses_and_two_labels_precede_old_English']
    assert current['source_context_sha256']==sha(SOURCE.read_bytes())
    assert current['all14_current_templates_equal_raw_storage_without_catalogue_override']
    assert context['all14_clean_speech_glosses_and_both_choice_labels_precede_old_English']
    effective={r['id']:r for r in current['effective_current_records']}
    forms={(r['actor_ID'],r['consumer']):r['text'] for r in current['native_six_distinct_name_consumers']['rows']}
    assert forms=={(2,'progressive-nameplate'):'Lil Argot',(2,'full-catalogue'):'Lil Argot',
        (17,'progressive-nameplate'):'Al Shin',(17,'full-catalogue'):'Al Ferid Shin',
        (85,'progressive-nameplate'):'Square Shopkeeper',(85,'full-catalogue'):'Square Shopkeeper'}
    selectors=current['original_static_selectors']
    voices={r['source_selector']:r['original_voice_class'] for r in selectors['rows']}
    assert voices=={2:3,17:4,85:0}
    rows=[];findings=[]
    for old in packet['records']:
        row=deepcopy(old);body,decision,note=DECISIONS[row['source_record_index']]
        template=bytes.fromhex(row['current_hex'])[1:].decode('cp932')
        before=' '.join(template.split());runtime=effective[row['id']]
        assert runtime['effective_predecessor_paragraph']==before
        assert (body!=before)==(decision=='revise')
        assert body.isascii() and body==' '.join(body.split())
        assert not any(t in body for t in ['{','}','%','FI','FA','FO','FU','\0'])
        selector=row['source_selector']
        row.update(english=f'{{SPEAKER:{selector:02X}}}'+body,
            speaker=forms[selector,'progressive-nameplate'],
            context=context['whole_exchange_context']+' Individual context: '+row['fresh_source_gloss'],
            source_meaning=row['fresh_source_gloss'],localization_note=note,
            editorial_decision=decision,editorial_finding=note,
            retention_reason=note if decision=='retain-wording' else None,
            current_raw_storage_English=template,current_effective_paragraph=before,
            current_effective_runtime_template_hex=runtime['current_effective_runtime_template_hex'],
            current_expanded_runtime_hex=runtime['current_expanded_runtime_hex'],
            current_registered_catalogue_match=None,source_voice_class=voices[selector],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            full_exchange_read_aloud_review=True,no_manual_line_break_padding_or_alignment_authored=True,
            current_complete_native_display_pending=True,registered_integration_pending=True,
            source_prose_or_completion_credit_added=0,
            formatting_reason='Pending B221 whole-paragraph native/stored pages,one original two-choice menu and result routing,four relative fixups,A000/full normal end,complete inverse,actual representative source/English transitions and registered release. Preserve the current native name consumers until the separate wider Shopkeeper layer is validated. No new item-title,acquisition or full-effects approval.')
        rows.append(row)
        findings.append(dict(id=row['id'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],
            previous_English=before,english=body,decision=decision,reason=note))
    assert len(rows)==14 and Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':6}
    choices=[]
    for old in packet['typed_choice_records']:
        row=deepcopy(old);index=row['option_index'];word=['Yes','No'][index]
        previous=bytes.fromhex(row['current_hex']).decode('ascii')
        assert previous.strip()==word
        note=('Retain '+word+' as the natural concise player response to Do you know about the Crusades. It conveys '+['知っている','知らない'][index]+'. The inherited spaces are storage evidence, not authored alignment; the typed formatter owns offsets and padding. Preserve original index '+str(index)+' and prove the resulting branch/cancel behavior separately.')
        row.update(english=word,speaker='Player response to the shopkeeper\'s Crusades question',
            source_meaning=row['fresh_source_gloss'],context=context['whole_exchange_context'],
            localization_note=note,editorial_decision='retain-wording',
            fresh_retained_wording_justification=note,effective_predecessor_paragraph=word,
            previous_raw_storage_body=previous,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_complete_native_display_pending=True,source_prose_or_completion_credit_added=0)
        choices.append(row)
    assert len(choices)==2
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CONTEXT,
        Path('translations/square_shopkeeper_label_manuscript_v2.json'),
        Path('dk4tool/patch/Al_Ferid_name_release_v1.py'),Path(__file__)]}
    base=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],
        formatting_review_pending=True,file_path='/data/SC2.DK4',
        source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],
        current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
        current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        current_strict_native_input=packet['current_strict_native_input'],
        current_consumer_proof=str(CURRENT),current_consumer_proof_sha256=sha(CURRENT.read_bytes()),
        whole_exchange_context=context['whole_exchange_context'],
        source_prose_or_completion_credit_added=0,evidence=evidence,full_goal_complete=False)
    name_rows=[]
    for actor in current['source_name_fields']:
        ident=actor['actor_ID']
        reason={2:'Retain established Lil Argot from cleanリル/アーゴット and both original getters; no new biography, rank or relationship.',
            17:'Retain the established consumer-specific Al Shin dialogue form and Al Ferid Shin full-catalogue form from cleanアル/シン/フェリド. The registered preceding name layer intentionally retains both forms and corrects only Ferid typography. Do not rename the actor to the incomplete Al Ferid handoff shorthand or append a new title, nationality or biography.',
            85:'The existing Square Shopkeeper is an open wider natural-label revision. All ten clean広場の店主 entries are now proposed as Shopkeeper in the separate source-context manuscript. Keep this block\'s exact actor85 preambles and current getters while wider shared-consumer/native/actual/release validation is pending; do not call the awkward current label editorially approved.'}[ident]
        name_rows.append(dict(actor_ID=ident,fields=actor['fields'],
            progressive_name=forms[ident,'progressive-nameplate'],full_catalogue_name=forms[ident,'full-catalogue'],
            decision='retain-established-consumer-specific-forms' if ident!=85 else 'revise-in-separate-wider-role-layer-pending',
            reason=reason,review=dict(source=True,context=True,localization=True,naturalness=ident!=85,formatting=False),
            native_complete_name_planes_and_actual_headers_pending=True,new_name_credit=0,new_dialogue_credit=0))
    save(NAMES,dict(format='contextual-speaker-name-review-v1',**base,records=name_rows,
        Al_Shin_versus_Al_Ferid_Shin_intentional_not_getter_regression=True,
        Shopkeeper_wider_proposal='translations/square_shopkeeper_label_manuscript_v2.json',
        no_name_asset_change_or_global207_name_approval=True,full_catalogue_UI_unvisited=True))
    save(OUTPUT,dict(format='dk4-editorial-manuscript-v1',**base,encoder='dialogue-relocatable-v1',
        records=rows,revised=8,retained=6,speech_objects=14,typed_choice_labels=2,
        all14_four_prose_gates_true_formatting_false=True,no_original_or_invented_FI_FA_FO=True,
        speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),
        historical_and_religious_claims_remain_character_viewpoints=True,
        no_global_item_title_or_unproved_effect_stat_location_added=True))
    save(CHOICES,dict(format='dk4-editorial-typed-choice-manuscript-v1',**base,
        encoder='typed-menu-relocatable-v1',records=choices,revised=0,retained=2,
        source_choice_word=0x2100,source_choice_count=2,source_command_offset=150,
        original_indices_branch_mapping_cancel_and_native_display_pending=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'fourteen_speech_two_choice_decisions_eight_revisions_eight_retentions.json',dict(
        findings=findings,manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        choice_manuscript=str(CHOICES),choice_manuscript_sha256=sha(CHOICES.read_bytes()),
        name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),
        objects=16,revised=8,retained=8,all_retentions_individually_justified=True,
        no_ROM_asset_registry_or_ledger_change=True,native_actual_and_registered_release_pending=True,
        new_review_credit=0,evidence=evidence,full_goal_complete=False))
    print(dict(speeches=14,choices=2,revisions=8,justified_retentions=8,
        formatting_pending=True,Shopkeeper_separate_layer_pending=True,new_credit=0))
