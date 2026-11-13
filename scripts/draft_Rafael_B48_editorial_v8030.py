"""Fresh clean-source B48 localization with explicit individual revisions and justified retentions."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_prose_v8030')
CURRENT=Path('work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B48_effective_v8029/all91_effective_English_templates182_original_dispatches4_FE.json')
NATIVE_NAMES=Path('work/analysis/Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json')
PATHS=Path('work/analysis/Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json')
OUT=Path('translations/rafael_B48_editorial_manuscript_v1.json')
NAMES_OUT=Path('translations/rafael_B48_speaker_name_review_v1.json')
EDITS={
49:("Don't be so quick to complain!","Use the natural American idiom for Claudio's habit of immediately finding fault;not the speed at which he speaks."),
56:("Claudio, you're always complaining.","Restore Rafael addressing his companion;the predecessor read as a detached narrator statement. Full established English name naturally renders the familiar shortened address."),
75:("Proof of... Conquest?","Claudio sounds out the same unfamiliar term;do not replace it with a different title,Ruler's Proof."),
81:("Oh, right... Julio, what was that errand you mentioned?","Restore the optional clean B128 callback andspecific errand question,rather than asking why Julio is in Athens."),
86:("I'm going to look into the Proof of Conquest.","On this exclusive introduction the term must be named in full for the first time;preserve Julio's intention to go investigate."),
97:("That's what I'm going to find out.","Preserve the gently evasive joke andthe investigation/return;the predecessor's vague answer lost his intended action."),
101:("??","Retain the brief nonverbal confusion;normalize the two question marks for the English prose rather than inventing a spoken explanation."),
106:("Just wait a bit. I'll be right back.","Restore the promised return in natural speech;do not add a new instruction about a specific location."),
109:("Uh... all right.","Convey Rafael's hesitant acknowledgment of Julio's puzzling answer,rather than a possible demand to repeat it."),
125:("Deck, hold, anywhere is fine. Just take me to some faraway country.","Preserve the requested distant country andwillingness to accept any space aboard,not merely getting away locally."),
129:("At your age, could you even swab the deck?","Preserve the worker's dismissive rhetorical question instead of declaring the man's inability as a fact."),
132:("Oh, don't say that. Please?","Restore the older traveler's pleading,conversational appeal;Please,reconsider was unnecessarily stiff."),
140:("Oh! You're a sailor from the ship that just came in, aren't you? Would you take me aboard?","Restore recognition of the recently arrived ship andthe polite individual request;no new rank is supplied by Hans."),
155:("I suppose that's a no, then...?","Preserve tentative disappointment after Claudio's objection;avoid an accusatory refusal attributed to Rafael before he has decided."),
164:("I'm Hans Letzel, a naturalist.","Use the reviewed current source-compatible identity consistently;Retzel disagreed with both native name getters. Naturalist expresses the natural-history research role without implying a medical doctor."),
175:("I see...","Restore Rafael's acknowledgment of the reason for the voyage,not just a thinking noise."),
180:("Now that's impressive!","Give Claudio a natural emphatic reversal into sincere admiration,rather than a stiff standalone adjective."),
209:("Could you take one more person aboard?","Natural English request retaining exactly one companion;do not invent their relationship before the assistant is introduced."),
212:("??","Preserve the short puzzled reaction with English punctuation;do not invent speech."),
221:("...I'm Arcadius Eudoxios. It's a pleasure to meet you.","Preserve the quiet opening andpolite reserved introduction. The spoken source omits the middle name Eirene;do not import the full-catalogue form."),
236:("(You're one to talk. Still, he makes even you look sturdy.)","The source-bound Janus group makes the addressee clear. Use natural second person instead of addressing Janus as you andthen naming him in the third person."),
247:("And it's not just his dedication to learning. He's a promising... young man.","Restore the not-only-academic suggestion andhesitant presented identity,without explaining concealed characterization or inventing an attraction or relationship."),
250:("I've studied navigation a little, but I still have a lot to learn from all of you.","Restore modest little study andthe newcomer's courteous acknowledgment;avoid the stilted curriculum description."),
280:("It's reassuring to have such a knowledgeable scholar with us, isn't it, Claudio?","Preserve Rafael's reassurance at the scholar's knowledge andfamiliar question to Claudio,rather than a flat guaranteed utility claim."),
284:("Yeah, guess so. Keep up the good work, Doctor! ...And you too, Arcadius!","Retain Claudio's casual endorsement andpointed extra beat. Use the just-established name for a natural English address;Assistant need not become a new title or insulting nickname."),
316:("??","Preserve Claudio's brief confusion at the recognition;English punctuation only."),
331:("Interested? I don't even know what the Proof of Conquest is!","Restore Rafael's ignorance andcomic need for an explanation;Not really falsely expressed disinterest."),
336:("They're treasures scattered across the seas, said to be claimed by those who rule each region.","Restore reported belief rather than stating destiny as fact;preserve multiple regional treasures andthe rulership association."),
339:("Much is still a mystery, but I think we may have a lead on where to find the treasures.","Preserve incomplete knowledge anda tentative lead. This does not establish a solved location or guaranteed discovery."),
347:("According to an ancient text, there are seven treasures in all. The ancient Seven Sages marked the places where they were to be sealed on maps of various shapes.","Preserve source attribution,all seven treasures,the ancient Seven Sages,intended sealing places andvaried map shapes. Remove the unnatural sealing place compression without shortening meaning for layout."),
350:("Someday, whoever comes to rule each sea is destined to obtain its map. That's what it says.","Keep the text's reported destiny andregional map. Obtain avoids inventing a giver or delivery mechanic."),
354:("Then if we collected them ourselves...!","Restore the unfinished conditional realization andown effort;do not turn it into a settled ability claim."),
361:("Ruler of the seas...","Natural reflective echo of Julio's explanation;avoid the abrupt new Sea king label."),
366:("Let's do it! We'll earn them ourselves!","Preserve personal determination andwinning through their own efforts;this is a character's resolve,not a system guarantee."),
370:("You're always the most eager, {MACRO:FI}! I don't really understand all this, but first we've got to see one of those Proofs.","Retain the effective catalogue-selected English words andClaudio's teasing skepticism. Normalize its stray full-width I to ordinary I andpreserve the exact source FI substitution;raw storage was not the effective predecessor."),
379:("Yeah! We'll find them!","Preserve determined pursuit of the treasures;one unnecessarily narrowed the stated goal. This path contains no Hayreddin challenge."),
385:("All right! We'll find them, and someday we'll challenge Hayreddin too!","Preserve plural goal andprospective Hayreddin ambition only in the event37-complete alternative;no present attack or guaranteed victory."),
393:("Good heavens! What kind of ship have I joined?","Restore Hans's lightly comic questioning astonishment at the bold ambition,without declaring disaster or regret."),
406:("I recently heard a rumor that someone took one of the Proof of Conquest maps to southern Africa.","Restore recent hearsay andone of the maps;do not invent the person's identity,a city or a location out at sea."),
427:("Hans Letzel, the naturalist, has joined you!","Restore the complete surname andconsistent natural-history role;Letze was truncated in storage. Joined you avoids implying that Hans is an assignable navigator."),
431:("Hans isn't a navigator, so you can't assign him on the Deck screen.","Preserve the exact navigator/deck-assignment limitation. Sailor conflated a profession with the specific gameplay crew role."),
435:("With Hans aboard, you can now view detailed item information.","Restore the player's newly available viewing action;avoid the awkward suggestion that Hans mysteriously reveals information on his own."),
}
RETAIN={
5:"The concise exclamation conveys Rafael's delighted recognition of Athens as a center of learning andphilosophy. The source's introductory reminder need not become an extra literal clause.",
17:"Generic you is natural American speech including the speaker;the city making one want to study conveys its scholarly atmosphere without a new instruction or plot fact.",
32:"Exactly can answer Rafael's learning remark even when Janus is absent. The measured may andcomplete formal sentence suit Cesare;no forced archaic stiffness is needed.",
38:"The direct second-person complaint is natural Claudio speech andleaves the addressee unstated,as the utterance itself does. Do not insert Cesare's name,especially in source paths omitting his preceding remark.",
61:"Yeah,yeah andGot it capture Claudio's exaggerated compliance;Enough from me naturally renders his promise to be quiet.",
71:"Perfect timing/Time to investigate naturally announces Julio's research in this source alternative. His later return promise andexit establish that he goes to do it;the named term remains complete.",
92:"The short question is a natural puzzled response after either complete term introduction. This Proof refers to the immediately named concept.",
116:"The brief question preserves the change of attention andcuriosity without inventing what Rafael has recognized.",
121:"The worker's curt hyperbolic dismissal anddirection to try elsewhere are natural in this exchange;they are his refusal,not an independently proved universal shipping rule.",
136:"The concise polite interruption naturally asks what is wrong andlets the traveler explain.",
144:"Captain is explicitly supported by the source address,andfree ride preserves the worker's practical objection. Old man does not imply kinship.",
148:"The contemplation andquestion naturally establish Rafael considering whether to bring the traveler;no acceptance or refusal is premature.",
152:"Another old man conveys Claudio's exaggerated complaint without adding family ties or a precise new crew count.",
159:"The request to hear the reason before deciding preserves Rafael's fair,considerate response andreads naturally in the full exchange.",
167:"The whole world as his subject is clear after naturalist;the urgent second sentence preserves Hans's passion andplea without an added biography.",
171:"The single ellipsis is the deliberate silent beat before Claudio's reversal. It is meaningful nonverbal dialogue,not a placeholder or authored layout break.",
184:"The full established English name naturally renders the familiar source nickname in Rafael's surprised address;no separate character is introduced.",
189:"The fluent complete speech retains aged determination,dangerous seas,research andsincere respect. Dedication naturally conveys the figurative driving of the aged body;no literal whip is needed.",
192:"The stumble andagreement preserve Rafael's surprise at Claudio's reversal,then the invitation welcomes Hans naturally.",
197:"The surprised question andthanks preserve Hans's relief andgratitude without an invented bargain.",
200:"Admiral is explicit in this source address,andthe polite additional-favor request fits Hans. It is not inferred from an unrelated honorific.",
204:"The direct short question naturally invites the additional request.",
217:"The assistant role,one conspicuously hesitant young...man description andthroat-clearing introduction preserve the characterization without revealing a hidden identity.",
232:"The parenthetical aside andslender observation preserve Janus's private reaction. He follows the identity Hans has just presented;the line does not assert a diagnosis or disclose a reveal.",
239:"Ahem is the natural English throat-clearing intervention completing the optional aside;no invented reprimand is necessary.",
254:"The warm reassurance andonly getting started preserve Rafael's humility andwelcome rather than inventing veteran expertise.",
258:"The concise formal response preserves the reserved newcomer's relief.",
262:"Hans's three enthusiastic sentences preserve his delight that matters have gone well andhis excitement about the voyage;grand expresses source praise without a new objective.",
273:"Should conveys Janus's optimistic expectation of an enjoyable voyage without a guarantee.",
288:"The enthusiastic idiomatic response preserves Hans's acceptance of the encouragement.",
292:"The courteous reserved joining acknowledgment andtrailing pause work for the assistant's voice;no new relationship or job is added.",
296:"The call is a natural English hail on Julio's return,not a newly invented greeting scene.",
300:"The brief recognition correctly turns Rafael's attention back to Julio.",
305:"The surprised recognition naturally conveys finding the sought person here;it does not state an invented travel history.",
308:"The delighted recognition expresses the source surprise naturally without inventing how long the two have known each other.",
312:"There you are is a natural search-and-find idiom,preserving Julio finding the man he sought. No extra literal explanation is required before Rafael's surprised question.",
320:"The shocked question preserves Rafael realizing that this was Julio's intended contact.",
324:"Acquaintance andfor years preserve the exact relationship andresearch duration. No family,mentor orlifelong intimate friendship is inferred.",
327:"The question naturally asks whether the crew shares the research interest;too is supported by Julio's interest andHans's work.",
343:"The excited question expresses Julio hoping Hans has discovered something;it is not a narrator assertion that the mystery is solved.",
358:"Truly naturally conveys name andsubstance together. The conditional you'd follows Rafael's unrealized collection;no completed kingship is claimed.",
389:"The compact startled repetition preserves the assistant's response to Hayreddin's name in that specific alternative.",
396:"The chuckle,late realization andfearless admiral characterization preserve Julio's affectionate amusement. Fears nothing is a character idiom,not literal invulnerability.",
403:"The familiar reflective English expression preserves Hans's approving comment about youth.",
409:"Really is a natural request for confirmation andsurprised response to the rumor.",
414:"May be false/could yield preserve uncertainty andpossible African information rather than a guaranteed map discovery. The next line makes the decision to go explicit.",
418:"The agreement andAfrica destination preserve Rafael's acceptance of the uncertain lead.",
438:"The existing direct UI instruction exactly preserves X andthe required item-information context;no wording change improves its clarity.",
441:"The natural elderly phrasing distinguishes inability to do shipboard work from the useful offer of item knowledge. No claim that Hans cannot travel aboard is added.",
}
NAME_REASONS={
0:"Retain user-approved Rafael Castor fromcleanラファエル/カストール andboth native getters.",
4:"Retain Janus Pasar fromcleanジェナス/パサー andboth getters;Pasar is distinct fromPasha andimplies no political association.",
5:"Retain Claudio Manaus fromcleanクラウディオ/マナウス andboth getters;full English name can naturally render familiarClau addresses.",
6:"Retain Julio Erneco fromcleanフリオ/エルネコ andboth getters;no family tie toanother shared surname is inferred here.",
7:"Retain source-compatible current Cristina Erneco fromクリスティナ/エルネコ. This fixes no wider Cristina/Christina counterpart lead andclaims no national naming biography.",
8:"Retain Arcadius Eudoxios inprogressive speech andthe literal introduction. Preserve clean/current middleエイレネ/Eirene only inits original full-name consumer;do not add it tothis spoken introduction or explain concealed characterization.",
13:"Retain source-compatible established Cesare Tony fromチェザーレ/トーニ. The English spelling is readable andkeeps the identity;do not invent a national biography orforce an alternative spelling merely by nationality.",
75:"Retain current Hans Letzel as the source-compatible rendered identity fromハンス/レッツェル;Japaneseレ does not by itself mandate an EnglishR overL. Both native getters agree onLetzel. Normalize this batch's literal Retzel/Letze tothat complete identity;historical workflowRetzel remains a consistency lead,not evidence ofa different character or a user-locked spelling. No original Latin spelling authority is claimed.",
113:"Retain natural role Port Worker forclean出港所の兄貴 inthis complete departure-office exchange. Familiar兄貴 does not establish brotherhood,rank,management or a personal name. Europe metadata is not part ofthe native displayed name. Wider counterpart consumers stay open.",
}

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES_OUT.exists()
    current,effective,names,paths=map(read,[CURRENT,EFFECTIVE,NATIVE_NAMES,PATHS])
    assert current['all91_clean_whole_context_glosses_precede_current_English_exposure']
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    assert len(effective['source_current_dispatches'])==182 and len(paths['representative_text_paths'])==32
    assert set(EDITS).isdisjoint(RETAIN) and set(EDITS)|set(RETAIN)=={r['source_record_index'] for r in current['records']}
    effective_rows={r['id']:r for r in effective['effective_current_records']}
    fields={r['actor_ID']:r for r in names['complete_clean_andcurrent_name_fields']}
    display={i:next(g['text'] for g in r['original_getters'] if g['consumer']=='progressive-nameplate') for i,r in fields.items()}
    evidence={str(p):sha(Path(p).read_bytes()) for p in [CURRENT,EFFECTIVE,NATIVE_NAMES,PATHS,Path(__file__)]}
    rows=[]
    for original in current['records']:
        row=deepcopy(original);i=row['source_record_index'];before=effective_rows[row['id']]
        predecessor=before['effective_predecessor_paragraph'].replace('FI','{MACRO:FI}')
        english,reason=EDITS[i] if i in EDITS else (predecessor,RETAIN[i])
        assert ('{MACRO:FI}' in english)==(i==370)
        assert not any(token in english for token in ['{LB','{ALIGN','{PAD','\n','\r'])
        if i in RETAIN:assert english==predecessor
        else:assert english!=predecessor
        meaning=row['source_gloss']
        if i==38:meaning="Claudio complains in the second person about the addressee's stiff personality andasks whether something can be done about it. The utterance supplies no name;do not universally assign the line toCesare across optional paths."
        if i==427:meaning="The system announces that natural-history scholar/doctorハンス・レッツェル has joined the party. Preserve the complete reviewed proper name andthe non-navigator qualification inthenext panel."
        context=row['full_clean_exchange_context']+'; '+row['source_branch_refined_gloss']
        if i==38:context+='; Earlier provisional Cesare addressee is superseded:Cesare remarkR32 is optional,butthis complaint is common. Preserve unnamedsecond person;do not rewrite the stored branch.'
        row.update(english=english,logical_English=english,speaker='System' if row['source_selector']==254 else display[row['source_selector']],
            source_meaning=meaning,context=context,localization_note=reason,
            decision='revision' if i in EDITS else 'retention',editorial_decision='revise' if i in EDITS else 'retain',
            retention_reason=None if i in EDITS else reason,editorial_finding=reason,effective_predecessor=before,
            original_voice_class=None if row['source_selector']==254 else next(v['original_voice_class'] for v in names['native_static_selector_andvoice_resolution']['rows'] if v['source_selector']==row['source_selector']),
            whole_exchange_situation_voice_andprogression_reviewed=True,exact_source_macros_preserved=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=True,new_credit=0)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':42,'retention':49}
    name_rows=[]
    for actor in sorted(fields):
        name_rows.append(dict(actor_ID=actor,name=display[actor],decision='retain',reason=NAME_REASONS[actor],
            clean_current_fields=fields[actor],source_speech_IDs=[r['id'] for r in rows if r['source_selector']==actor],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            name_asset_changed=False,native_font_bounds_complete_names_actual_B48_headers_andcatalogue_UI_pending=True,
            no_original_Latin_biographical_orhidden_identity_claim=True,new_credit=0))
    save(NAMES_OUT,dict(format='dk4-source-bound-speaker-name-review-v1',records=name_rows,
        native_proof=str(NATIVE_NAMES),native_proof_sha256=sha(NATIVE_NAMES.read_bytes()),
        full207_name_role_alias_review_active=True,Hans_historical_Retzel_current_Letzel_andstored_Letze_finding_explicit=True,
        Arcadius_progressive_andfull_middle_name_consumers_kept_distinct=True,
        new_credit=0,full_goal_complete=False))
    path_reviews=[]
    for index,path in enumerate(paths['representative_text_paths']):
        exchange=[next(r for r in rows if r['id']==ident) for ident in path['source_speech_IDs']]
        assert all(r['review']['source'] and r['review']['context'] and r['review']['localization'] and r['review']['naturalness'] for r in exchange)
        path_reviews.append(dict(source_path=index,source_results=path['raw_results'],source_speech_IDs=path['source_speech_IDs'],
            complete_English_exchange=[dict(id=r['id'],speaker=r['speaker'],english=r['english']) for r in exchange],
            finding="Athens learning/crew teasing leads into Julio's correct optional errand introduction,thenconsiderate hearing ofthe traveler,Claudio's sincere reversal,hesitant assistant welcome,Julio/Hans recognition,source-attributed seven-treasure legend,Rafael's growing ambition,correct conditional Hayreddin beat,uncertain African lead,four distinct role/UI panels andHans's offer. No concatenated exclusive introductions,no named addressee added tothe common complaint,no hidden identity explanation.",
            whole_source_English_path_situation_voices_humor_andprogression_reviewed=True,
            not_actual_gameplay_orindividual_conditional_scene_coverage=True))
    ROOT.mkdir(parents=True)
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],route=0,route_identity='Rafael',block=48,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        records=rows,revisions=42,retentions=49,source_current_packet=str(CURRENT),effective_packet=str(EFFECTIVE),
        names_packet=str(NAMES_OUT),source_path_packet=str(PATHS),all32_complete_English_exchange_reviews=path_reviews,
        complete_clean_glosses_B128_B37_callbacks_names_andbranch_context_precede_current_comparison=True,
        all91_current_effective_templates_reviewed_one_catalogue_selected_R370=True,
        source_macro_counts=dict(FI=1,FA=0,FO=0),all91_formatting_gates_false=True,formatting_review_pending=True,
        body_only_logical_draft_native_prefix_markup_stored_padding_andlayout_owned_by_formatter=True,
        source_selectors=sorted({r['source_selector'] for r in rows}),FE_panels=4,typed_menu_count=0,
        no_invented_kinship_rank_fixed_addressee_hidden_identity_guaranteed_discovery_orcompleted_ambition=True,
        Hans_Letzel_consistency_andfull_trailing_l_restored_without_name_asset_change=True,
        Proof_of_Conquest_term_retained_from_existing_source_compatible_name_seven_regional_treasures_not_war_requirement=True,
        retrospective_early_wrap_review_still_required_no_manual_breaks_authored=True,
        status='91-source-context-prose-decisions-reviewed-native-pages-stored-actual-policy-release-pending',
        evidence=evidence|{str(NAMES_OUT):sha(NAMES_OUT.read_bytes())},new_credit=0,new_emulator_runs=0,full_goal_complete=False)
    save(OUT,doc)
    save(ROOT/'91_contextual_decisions32_path_reviews42_revisions49_retentions.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES_OUT),names_sha256=sha(NAMES_OUT.read_bytes()),
        records=rows,path_reviews=path_reviews,revisions=42,retentions=49,
        all91_source_context_localization_naturalness_gates_true_formatting_false=True,
        R38_provisional_named_addressee_corrected_from_complete_conditional_context=True,
        existing_working_wordings_retained_with49_individual_reasons=True,
        all_old_translations_source_first_glosses_andproofs_preserved=True,
        native_stored_reference_actual_policy_registered_release_andstartup_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B48:91 contextual decisions/42revisions/49justified retentions,32source paths,nine scoped name retentions. Four prose gates pass;formatting/native/stored/actual/release pending.No credit.')
