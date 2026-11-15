"""Review the complete B50 exchange against clean context and effective English, preserving working wording individually."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_prose_v8138')
CURRENT=Path('work/analysis/Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B50_effective_v8137/all28_effective_English_templates56_original_dispatches_no_FE.json')
GLOSS=Path('work/analysis/Rafael_B50_context_v8135/28_refined_glosses_dye_identity_FA_FI_title_context_before_current_B50_English.json')
NAMES=Path('work/analysis/Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json')
CONTROL=Path('work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json')
ITEM=Path('work/analysis/Rafael_B50_pigment_v8134/original4821_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json')
DOC=Path('translations/rafael_B50_editorial_manuscript_v1.json')
NAME_DOC=Path('translations/rafael_B50_speaker_name_review_v1.json')
REVISIONS={
 14:("Huh, you remembered! Anyway... you got the better of us after all.","Restore Lil's surprised recognition and eventual concession. Got the better of us expresses being outmaneuvered without inventing a race to a particular object, a battle loss or betrayal. Her competitive tone leads into Rafael's awkward acknowledgment."),
 18:("Oh... thanks.","Sourceどうも is an awkward polite acknowledgment here; an explicit apology is unsupported and made the following response depend on an invented apology. Thanks lets Rafael miss Lil's competitive point, with the next line brushing this off before the gift."),
 23:("Never mind that. This is the key to deciphering the treasure map. It's yours.","Renderどうもじゃないわよ as Lil dismissing his bland acknowledgment, rather than Don't apologize. Preserve the concrete aid for deciphering a map and its gift, not a new map or treasure. Clean/native context binds the dye; the source does not require naming it again here or claiming Rafael already has the parchment."),
 31:("Did I really lose to this guy? ...Oh, well.","Replace the literal stage word Sigh with Lil's incredulous spoken question and trailing dismissal. This responds to Rafael's surprise at the gift and preserves the gap between her competitive pride and his mildness, without inventing a naval battle."),
 40:("Hello. You're Mr. {MACRO:FA}, right?","Preserve FA as the surname token, default Castor, and the polite sourceさん as natural surname address. Mr. Castor avoids an unsupported new military rank and fits Camille's courteous introduction. Keep the existing greeting and identity check."),
 49:("That's right. I suppose it's been a while... Ha ha.","久しぶり concerns time since meeting, not whether they technically met at all. Preserve Camille's tentative, slightly awkward reunion and laugh without asserting an exact interval, event sequence or chronology from block numbers."),
 57:("Yeees. I just gave him that dye. I won't need it anymore.","The stretched sourceはい is playful compliance, not No. Restore the actual dye reference and future nonuse. The old she refers incorrectly to Rafael. Him follows the established Rafael identity; it adds no relationship. Do not turn the unexplained nonuse into marriage, pregnancy, retirement or a new occupation."),
 61:("Oh, right. Mr. {MACRO:FA} rules the North Sea now. That's fine, then.","Retain the working present regional-dominance fact and Camille's acceptance, with natural word order. He is answering Lil about Rafael in the third person. Source総帥 is the company/force-leader role distinguished from admiral and captain in the clean opening; respectful Mr. plus surname conveys this social address without inventing a rank. FA remains unchanged."),
 73:("Well, I guess I've found there's more to life than making money.","Restore Lil's personal, tentative discovery of another way to live. The old general maxim Let's say there is more to life lost the personal change that prompts the following exchange. Keep what she has found unnamed so Rafael's bluff and the final joke remain intact."),
 99:("So, no present?","Preserve the brisk follow-up and negative question about anお祝い gesture/present. Avoid an unsupported singular possessive my or an invented wedding/occasion. The surrounding thanks and final private question carry the congratulatory purpose."),
 103:("W-what?! (Oh, no... I have no idea what she means...)","Restore Rafael's stammer and private realization that he has failed to understand. Do not move the final what-were-we-celebrating punch line into this earlier thought. Keep the spoken reaction and parenthesized inner thought distinct."),
 108:("Please don't worry about it. Come on, Lil. Take care, {MACRO:FI}.","Retain the working courteous dismissal, departure and farewell. Remove Commander, which renders the company-leader address as a separate military rank despite the clean opening's distinction. Deference remains in the polite phrasing; FI remains the given-name token, distinct from FA. No shortened or invented nickname."),
 114:("Lil, Camille, thank you! I'll do my best to live up to your expectations!","Restore both source addressees and Rafael's personal effort. Sourceがんばります promises to try, not that a collective we will certainly meet their hopes. His earnest thanks must still sound plausible even though he privately never understood the congratulatory occasion."),
}
RETENTIONS={
 6:'Wait! is a natural urgent call that opens the encounter. It neither names an unseen addressee nor adds why Lil is stopping him.',
 10:'The existing Oh! and name check convey Rafael\'s hesitant recognition naturally. Lil\'s next response makes clear that remembering her name is what surprised her; an extra did-we-meet explanation is unnecessary.',
 27:'What?! Are you sure? accurately conveys surprise at being offered the key and seeks permission to accept. It keeps Rafael\'s mild disbelief without changing the gift into a bargain.',
 37:'Camille\'s relieved There you are! followed by the unfinished preparations is natural and well paced. The wording deliberately leaves the preparations\' purpose unnamed, preserving the later misunderstanding.',
 44:'Y-yes. And you\'re Camille? preserves the reciprocal uncertain name check and Rafael\'s stammer. Camille is the approved name; the line invents no identity revelation, kinship or honorific rank.',
 53:'You aren\'t being rude again, are you? is an idiomatic concerned check after Camille arrives. Again is in the source, and the question remains suspicion rather than a claim that a new offense was witnessed.',
 65:'What? Did something happen? conveys the source question marks and Rafael\'s puzzled request after Camille mentions regional leadership. It does not name the hidden occasion or claim he understands.',
 69:'Still so dense... No, no. You\'re as easygoing as ever. works as a caught insult followed by a face-saving, more agreeable description. The cut thought and self-correction preserve Lil\'s humor; no literal word fracture is needed.',
 77:'Oh. Got it. is an appropriately mild outward acknowledgment. The following private thought exposes that this is a bluff, so making it more genuinely informed would damage the exchange.',
 82:'You just got it?! naturally means only now in direct response to Got it. It preserves Lil\'s incredulity at his apparent delayed understanding without explaining what he ought to have understood.',
 86:'The clipped parenthesized No idea, but play along. is natural comic inner speech. That\'s wonderful! is his spoken bluff and leads directly to both thanks. Keep the contrast rather than adding an invented congratulatory occasion.',
 91:'Thanks! gives Lil the source\'s casual, warm response to the apparent congratulations. It is distinct from Camille\'s more formal thanks and does not specify what she is grateful for.',
 95:'Thank you very much. is a natural polite counterpart to Lil\'s Thanks! and suits Camille\'s courteous voice. It does not introduce a separate favor or reveal the occasion.',
 111:'Bye! Do your best for us too! is a natural cheerful departure and passes on the source encouragement for their share. It does not explicitly announce permanent retirement, a transfer of possessions or a new relationship.',
 119:'What were we celebrating, anyway? preserves the unresolved final joke and Rafael\'s private incomprehension. We is ordinary English for the congratulatory exchange, not a claim that a party occurred or that a gift was actually given.',
}
NAME_REASONS={
 0:'Retain Rafael Castor: cleanラファエル/カストール, approved Rafael, and exact progressive/full getter forms agree. The source FA surname and FI given-name substitutions are distinct. No new rank is made part of the name.',
 2:'Retain Lil Argot: cleanリル/アーゴット and exact prior/current getter forms agree. Her brisk speech and unexplained life change do not justify a new surname, marital label or altered biography.',
 9:'Retain approved Camille and source surname Overijssel. Cleanカミル/オーフェルアイセル and full middleマリヌス remain bound to the existing getters. Keep Marinus in the full getter; the progressive source form omits it. Preparations and congratulations do not authorize marriage, gender revelation or kinship.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAME_DOC.exists()
    current,effective,gloss,names,control,item=map(read,[CURRENT,EFFECTIVE,GLOSS,NAMES,CONTROL,ITEM])
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes()) and current['gloss_packet_sha256']==sha(GLOSS.read_bytes())
    assert set(REVISIONS).isdisjoint(RETENTIONS) and len(REVISIONS)==13 and len(RETENTIONS)==15
    assert len(current['records'])==28 and len(control['all_source_commands'])==37
    speakers={r['actor_ID']:next(g['text'] for g in r['original_getters'] if g['consumer']=='progressive-nameplate') for r in names['complete_clean_andcurrent_name_fields']}
    assert speakers=={0:'Rafael Castor',2:'Lil Argot',9:'Camille Overijssel'}
    rows=[]
    for original in current['records']:
        row=deepcopy(original);index=row['source_record_index'];prior=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        old=prior['effective_predecessor_paragraph'];comparable=old.replace('FI','{MACRO:FI}').replace('FA','{MACRO:FA}').replace('FO','{MACRO:FO}')
        if index in REVISIONS:text,reason=REVISIONS[index];decision='revision';assert text!=comparable
        else:text,reason=comparable,RETENTIONS[index];decision='retention';assert text==comparable
        assert all(32<=ord(c)<127 for c in text) and not any(t in text for t in ['{LB','{ALIGN','{PAD','\n','\r'])
        for token in ['FI','FA','FO']:assert text.count('{MACRO:'+token+'}')==bytes.fromhex(row['source_hex'])[1:].count(token.encode())
        row.update(english=text,logical_English=text,speaker=speakers[row['source_selector']],source_meaning=row['refined_source_gloss'],
            context='Lil concedes being outmaneuvered and gives a map-deciphering aid; Camille arrives amid unnamed preparations; Rafael mistakes an unexplained life change for something he understands and plays along, then remains puzzled about the requested congratulatory present. '+row['refined_source_gloss'],
            localization_note=reason,editorial_finding=reason,decision=decision,editorial_decision='revise' if decision=='revision' else 'retain',retention_reason=reason if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),effective_predecessor_template_hex=prior['effective_predecessor_template_hex'],effective_predecessor_paragraph=old,
            registered_catalogue_match=prior['registered_catalogue_match'],source_context_proof=str(GLOSS),source_context_proof_sha256=sha(GLOSS.read_bytes()),source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),
            current_effective_body_dispatch_andcatalogue_pending=False,source_control_andruntime_substitutions_must_remain_exact=True,
            native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending=True,source_prose_orcompletion_credit_added=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':13,'retention':15}
    assert {r['source_record_index'] for r in rows}==set(REVISIONS)|set(RETENTIONS)
    name_rows=[]
    for r in names['complete_clean_andcurrent_name_fields']:
        actor=r['actor_ID'];name_rows.append(dict(actor_ID=actor,name=speakers[actor],source_clean_fields=r['clean_fields'],current_fields=r['current_fields'],original_getters=r['original_getters'],decision='retention',retention_reason=NAME_REASONS[actor],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),full207_catalogue_UI_custom_names_actual_headers_andnative_font_bounds_pending=True))
    ROOT.mkdir(parents=True);evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,GLOSS,NAMES,CONTROL,ITEM,Path(__file__)]}
    save(NAME_DOC,dict(format='dk4-speaker-name-review-v1',records=name_rows,full207_name_role_alias_review_active=True,no_new_name_assets_orfull207_approval=True,new_credit=0,evidence=evidence,full_goal_complete=False))
    save(DOC,dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC0.DK4',route=0,route_identity='Rafael',block=50,current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],records=rows,revised=13,retained=15,typed_choice_records=[],names_packet=str(NAME_DOC),
        source_packet=current['source_packet'],source_packet_sha256=current['source_packet_sha256'],source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),effective_predecessor_proof=str(EFFECTIVE),effective_predecessor_proof_sha256=sha(EFFECTIVE.read_bytes()),
        complete_source_physical_exchange_speeches_reviewed=28,all28_four_prose_gates_true_all_formatting_gates_false=True,
        english_is_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=True,
        all_original37_commands_nine_nontext_controls_no_relative_predicate_query_oneA000_andfull_end_to_preserve=True,
        source_event50_no_explicit_dependencies_not_natural_scheduler_location_orchronology_proof=True,
        original_FA2_FI1_no_FO_added_andinternal_thoughts_preserved=True,
        source_company_leader_title_not_invented_Commander_rank=True,source_lifechange_preparations_celebration_andfinal_joke_remain_unnamed=True,
        no_scene_captures_new_ROM_registered_layer_orcompletion_credit=True,
        status='complete-source-context-prose-draft-native-display-stored-actual-policy-andregistered-release-pending',evidence=evidence|{str(NAME_DOC):sha(NAME_DOC.read_bytes())},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    save(ROOT/'28_contextual_decisions_one_complete_exchange_individual_revisions_retentions.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAME_DOC),names_sha256=sha(NAME_DOC.read_bytes()),records=28,revisions=13,retentions=15,
        complete_English_exchange=[dict(id=r['id'],speaker=r['speaker'],english=r['english']) for r in rows],
        findings=['Rafael acknowledgment andLil dismissal are a coherent exchange,not an invented apology.','Dye reference andfuture nonuse restored without a new life-event explanation.','Reunion remains tentative without a date or invented earlier event.','FA surname andFI given name stay distinct;company-head deference is not a Commander promotion.','Clipped inner bluff andthe final unknown celebration remain;no marriage orbiography invented.','Rafael names both people andpromises effort rather than a guaranteed collective outcome.'],
        source_context_names_macros_native_entry_andcurrent_effective_dispatch_precede_manuscript=True,
        complete_physical_exchange_review_not_yet_actual_VM_path_or_scene_coverage=True,
        all28_formatting_gates_false_native_actual_policy_registered_release_pending=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B50 contextual draft:28records/13revisions/15individually justified retentions;three scoped name retentions.All formatting gates false;no credit.')
    for r in rows:print(r['source_record_index'],r['speaker'],r['decision'],r['english'])
