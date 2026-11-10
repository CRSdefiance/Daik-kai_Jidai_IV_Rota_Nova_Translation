"""Whole-exchange American English decisions; logical prose only,formatting still unapproved."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_prose_v8088')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B49_effective_v8087/all61_effective_English_templates122_original_dispatches_no_FE.json')
GLOSS=Path('work/analysis/Rafael_B49_branch_gloss_v8085/61_refined_glosses256_paths_B39_B41_context_before_current_English.json')
PATHS=Path('work/analysis/Rafael_B49_source_paths_v8082/156250_compositions_distinct_complete_text_paths_and61_source_memberships.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
MENTIONED=Path('work/analysis/Rafael_B49_mentioned_names_v8084/three_clean_mentioned_identities_six_native_getters_component_only_review.json')
DOC=Path('translations/rafael_B49_editorial_manuscript_v1.json')
NAME_DOC=Path('translations/rafael_B49_speaker_name_review_v1.json')
# Every retention is checked against effective runtime wording,not raw storage.
# Reasons concern this complete exchange andits original branches,not earlier approvals.
DECISIONS=[
(5,"Hm? What's all that noise at the trade house? Let's go see.",'revision','Correct Guild to the clean 交易所 trade house. Rafael hears a nearby commotion and goes to investigate; the new phrasing gives that curious, unhurried opening naturally.'),
(12,'Hey! You there!','retention','The sharp call is natural American English and starts Lil\'s confrontation directly without inventing an insult or relationship.'),
(15,'Lil! No fighting!','retention','Camille\'s short, familiar objection naturally tries to head off a fight. It does not establish parental, family or romantic status.'),
(20,'You have to be blunt about this! Camille, stay out of it.','retention','Lil insists on plain speaking and rebuffs Camille\'s mediation. The brisk wording preserves her forceful voice without an invented rank or relationship.'),
(32,"What's going on? Things seem awfully tense.",'revision','Restore Janus\'s wondering question and turn the awkward hostile-atmosphere gloss into a natural, observant aside. This remark is conditional; later lines do not assume it was spoken.'),
(38,'Did you need something?','revision','Use Rafael\'s innocent, helpful question so Lil can immediately echo Need something?! The old Do you need me? blurred the source exchange\'s repeated phrase.'),
(43,'Need something?! Who gave you permission to trade in the North Sea?!','revision','Preserve Lil\'s incredulous echo and permission demand. Remove our North Sea, which unnecessarily expanded her local territorial assertion to the whole region.'),
(47,'What was that, girl? You trying to make us angry?','retention','The clipped challenge suits Claudio\'s gruff, patronizing bluster and the source じょーちゃん address. Us renders his familiar older-man self-reference without inventing brothers or kinship.'),
(51,'Sorry, but... what exactly is going on here?','retention','Rafael\'s hesitant apology and request for an explanation already sound natural and preserve his genuine confusion rather than apologizing for a proven wrongdoing.'),
(55,'Are you stupid?','revision','Keep Lil\'s blunt insult in ordinary American speech. The source asks whether Rafael is foolish; no new motive or personal history is supplied.'),
(67,"Ha! That's rather harsh.",'retention','Janus\'s restrained amusement and polite understatement fit his optional reaction to Lil\'s insult. The reply remains understandable when it is omitted.'),
(74,"I'm only going to say this once. Listen carefully.",'revision','The source promises one explanation and demands attention. This is your only warning turned that into a stronger, more specific threat before the later conditional challenge.'),
(77,'Uh... yes.','retention','The hesitant compliance preserves Rafael\'s mild, slightly bewildered manner. It acknowledges listening rather than accepting a treaty or a ban.'),
(82,"People all over the world are working hard to make money. It's the same in these waters.",'revision','Translate 儲けようとがんばる as effort to make money. Fighting to get rich introduced a stronger conflict claim; these waters keeps the regional business context natural.'),
(86,'Could you be more polite?','retention','Camille again tries to soften Lil\'s manner. The concise request is idiomatic and supports the placating voice established at the start.'),
(90,"It's fine! Anyway, this area is Argot Company territory. Got it?",'revision','Lil rejects Camille\'s correction, so Good! reversed the response. Preserve her claim of territory as her assertion in the argument, without asserting control over every North Sea area.'),
(93,'Uh...','retention','The noncommittal acknowledgment fits Rafael\'s bewilderment and leaves room for Lil\'s next question about his competence.'),
(98,'Is this guy for real? Is he really an admiral?','revision','The source questions Rafael\'s demeanor and status,not his trustworthiness. Keep the disbelieving questions so the alternative Claudio/Janus confirmations answer them naturally.'),
(107,"Yeah. That's it.",'retention','Claudio\'s brusque confirmation works as the source alternative when Janus\'s confirmation is not selected. Do not stage both confirmations as one mandatory exchange.'),
(112,"Yes. He's a fine admiral.",'retention','Janus\'s polite, slightly emphatic confirmation is natural and leaves its wry delivery to the scene. It substitutes for Claudio\'s reply and does not establish a new rank.'),
(118,'What a letdown.','retention','The short reaction naturally conveys Lil\'s deflation after the unexpectedly mild admiral and his companion\'s confirmation.'),
(122,'But you seem decent. All right, let me explain.','retention','Seem preserves Lil\'s provisional judgment that the party is not bad. The turn from confrontation to explanation reads naturally.'),
(126,'The North Sea covers a pretty big area, right?','retention','The conversational question introduces the regional explanation clearly and retains Lil\'s brisk, instructive tone.'),
(129,'Yeah.','retention','Claudio\'s brief agreement is a natural answer to the preceding size question and needs no extra attitude or information.'),
(142,"Up north, there's that navy guy, Hodram Ber... something. For now, anyway.",'revision','Keep approved Hodram and the deliberately unfinished ベル... surname joke rather than completing Bergstrom. Navy guy preserves the casual older-man reference without an uncle relationship or an invented naval rank; for now remains.'),
(158,'Around England, an admiral named Clifford is in charge.','retention','The existing sentence clearly preserves the local geographical description and source surname component. England is a source-compatible scoped rendering here; the wider イギリス consumer lead is not globally resolved or renamed, and James is not added.'),
(175,'Over in Germany, Martin Speyer of the Hanseatic League is keeping things running. Somehow.','revision','The source casually says Speyer is somehow managing affairs around Germany. Barely held together risked claiming a national political collapse. Preserve Lil\'s dismissive impression, the League and source-compatible name.'),
(183,"As for the rest, we're hoping to claim most of it ourselves.",'revision','Restore the source\'s prospective wish and most-of-the-other-areas qualification. The company hopes to acquire territory; it does not already control the rest or assert a certain outcome.'),
(187,"But Lil, isn't trade fair once you sign a contract with a city?",'retention','Rafael\'s rhetorical question already makes the source contract condition and fair-trading objection clear. It remains his question,not an added unconditional guarantee about every trade mechanic.'),
(192,"I know that! I'm saying I'd like you to leave us alone for a while.",'revision','Lil admits she knows how contracts work and wants her company left alone temporarily. The old leave it alone could refer to the contract system instead of her company.'),
(196,'How convenient for you.','retention','This idiomatic, cynical response conveys Claudio\'s criticism of a self-serving request without copying Japanese syntax.'),
(200,"Well, that's a little...",'retention','Rafael\'s unfinished hesitation naturally conveys reluctance without turning it into an explicit refusal or a completed pact.'),
(205,"Aren't you trying to take on the whole world?",'retention','The idiom preserves Lil\'s challenge about their worldwide ambitions in the existing story context. It does not add an order to attack every country.'),
(208,'Yes. We are.','retention','The plain, unselfconscious affirmation fits Rafael\'s mild demeanor and gives Lil\'s following deflated reaction its comic contrast.'),
(213,'Ugh, you take all the fight out of me.','revision','Render Lil\'s loss of bluster rather than criticizing a dull answer. The idiom is natural in the quarrel and does not claim an actual battle occurred.'),
(225,'We do have a goal.','retention','Janus\'s optional, understated affirmation already fits his polite voice and confirms ambitions without inventing a more specific conquest plan.'),
(238,'Then why not head for Africa, or sail west to the New World?','revision','Keep both destination suggestions and the western direction in the event41-incomplete version. The source offers alternatives; it does not issue a literal forced-travel command.'),
(244,"The world's huge! Look beyond this sea! Head west to the New World, or solve the mysteries of the far East!",'revision','Restore the push to look elsewhere and the explicit west/far-East directions in the event41-complete version. Event41 is Hans\'s advice,not proof that Africa was cleared or a Proof obtained.'),
(250,"Hm. That's one way to look at it.",'revision','Give Rafael\'s thoughtful acknowledgment a natural spoken idiom instead of the stiff one viewpoint. He entertains her argument without an invented strategic commitment.'),
(255,'So, stay out of our way for a while.','retention','The direct, temporary request fits Lil\'s pushiness and refers back to leaving her company alone. It does not assert a permanent trading ban.'),
(259,"If you want to challenge us head-on, that's another matter. We've got plans of our own, you know. Got it?",'revision','Preserve the conditional challenge and Lil\'s unspecified plans. Answer in kind promised a particular reciprocal response that the source leaves open.'),
(262,'W-wait, Lil...','retention','Camille\'s stammered attempt to interrupt is already natural and reinforces the repeated effort to restrain Lil.'),
(266,"More or less. You're asking us to form a pact, aren't you?",'retention','Rafael gently recognizes Lil\'s request for 協定. The question identifies an agreement she wants; it does not claim a signed formal alliance,marriage or other new relationship.'),
(271,"Wh-what? You're sharp about the strangest things! That makes it sound like we're asking you for a favor!",'revision','Restore the teasing contrast with Rafael\'s earlier confusion and Lil\'s concern about appearing to ask from a weaker position. Begging made her position more desperate than the source.'),
(275,"Heh. You really hate to lose, don't you?",'revision','Use a gentle, natural teasing observation after Lil\'s flustered protest. Do not invent a completed contest that she has already lost.'),
(279,'Hey! Are you making fun of me?','revision','Keep Lil\'s indignant question in ordinary spoken English instead of the mechanically clipped Mocking me?'),
(283,'No, not at all.','retention','Rafael\'s polite denial is natural and lets the incongruity with his chuckle carry the humor.'),
(296,'Heh heh...','revision','Render the quiet くすくす laugh as an utterance rather than a narrator\'s Giggle instruction. Keep the amusement without explaining a hidden identity,gender or relationship.'),
(311,'Good grief, {MACRO:FI}. We might be better off making money in other waters.','retention','The effective wording already gives Julio\'s wry, tentative practical advice naturally. Preserve FI as the same runtime first-name substitution,not an invented literal Rafael or a profit guarantee.'),
(328,"You're enemies with Valdes of Spain, right?",'revision','Make Lil\'s common-enemy question natural while preserving Valdes\'s Spanish affiliation. Do not assert a new alliance with her company.'),
(331,"Enemies? Well, Spain has its eye on Portuguese territory... So yes, we are.",'revision','Keep Rafael\'s considered acknowledgment and Spain\'s prospective territorial aim. The old perhaps weakened the explicit 確かに conclusion; no invasion already taking place is invented.'),
(336,"Then we have the same enemy! We shouldn't be fighting each other. Exactly!",'retention','Lil\'s quick argument and self-affirming Exactly! already read naturally. The line supports avoiding conflict,not a statement that a formal alliance was signed.'),
(343,'Uh...','retention','The hesitant acknowledgment works both with and without the optional Valdes exchange. It does not explicitly agree to a battle,treaty or an unspoken named reference.'),
(356,"So you're telling us to try somewhere else.",'revision','Janus is summing up Lil\'s request. The old we should go elsewhere turned that reported meaning into his own unsolicited advice.'),
(363,"Right, then! You understand, don't you? We're busy too, so see you around!",'revision','Restore Lil\'s brisk understanding-check before her abrupt departure. Do not turn her presumption into proof of a formally settled agreement.'),
(367,'Lil, wait! S-sorry for the commotion! Please excuse us. Lil, wait!','revision','Preserve Camille\'s stammer,apology and repeated call after Lil; the frantic rhythm is part of the exchange\'s humor and needs no invented relationship.'),
(381,"The storm's passed...",'revision','Restore Arcadius\'s dry 台風一過 metaphor after Lil\'s departure. All calm lost the joke; this is figurative and does not add a weather event.'),
(388,"I don't like it, but you decide, {MACRO:FI}. I'll go along with your decision.",'revision','Retain the working effective catalogue-selected words and Claudio\'s grudging loyalty. Normalize its full-width I glyphs to ordinary ASCII I and preserve the exact FI substitution; raw storage was not the effective predecessor.'),
(392,"Let's leave this sea for later. She's hard to dislike. Besides, I bet she's scary when she's angry.",'revision','Preserve postponement,the inability to dislike Lil and the impression-based joke about her temper. Avoid a flat certainty about future behavior or a new romantic motivation.'),
(405,"That's wise, as long as the North Sea isn't all we have left.",'revision','Keep Arcadius\'s explicit remaining-region qualification in natural speech. It does not declare that the North Sea actually is the last region.'),
(409,"Then we'll head for another sea for now.",'retention','The existing closing proposal is natural and temporary. It is selected with Arcadius\'s preceding qualification; the common earlier decision also works when this ending is absent.'),
]
NAME_REASONS={
0:'Retain approved Rafael and source-compatible Castor. The clean protagonist identity and original current getters agree; no new title or kinship is supplied.',
2:'Retain Lil Argot for clean リル/アーゴット. The company association belongs to Lil\'s own dialogue; the spelling is compatible with the established source identity without a new biography.',
4:'Retain Janus Pasar for ジェナス/パサー. Pasar remains distinct from パシャ/Pasha; his conditional polite remarks and alternate confirmation do not create a new rank.',
5:'Retain Claudio Manaus for クラウディオ/マナウス. His familiar self-reference is localized as us in the threat,not as literal brothers or a family relationship.',
6:'Retain Julio Erneco for フリオ/エルネコ. The optional practical advice and FI address do not establish kinship with anyone sharing the surname.',
8:'Retain progressive Arcadius Eudoxios and preserve the source full-name middle Eirene in its own getter. The chuckle and dry asides do not justify revealing an identity or adding romantic/gender exposition.',
9:'Retain approved Camille and source-compatible Overijssel; preserve Marinus in the full getter,not as a new spoken form. Repeated restraint and apology support Camille\'s voice without inventing kinship,romance or a rank.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAME_DOC.exists()
    current,effective,gloss,paths,names,mentioned=map(read,[CURRENT,EFFECTIVE,GLOSS,PATHS,NAMES,MENTIONED])
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes()) and current['gloss_packet_sha256']==sha(GLOSS.read_bytes())
    assert len(DECISIONS)==len(current['records'])==61 and paths['distinct_text_path_count']==256
    choices={i:(text,decision,reason) for i,text,decision,reason in DECISIONS};assert len(choices)==61
    speakers={r['actor_ID']:r['text'] for r in names['native_fourteen_progressive_andfull_getters']['rows'] if r['consumer']=='progressive-nameplate'}
    rows=[]
    for original in current['records']:
        row=deepcopy(original);index=row['source_record_index'];text,decision,reason=choices[index]
        prior=next(r for r in effective['effective_current_records'] if r['id']==row['id']);old=prior['effective_predecessor_paragraph']
        comparable=old.replace('FI','{MACRO:FI}').replace('FA','{MACRO:FA}').replace('FO','{MACRO:FO}')
        if decision=='retention':assert text==comparable,(index,text,comparable)
        else:assert text!=comparable,(index,'unchanged revision')
        assert '\n' not in text and '\r' not in text and not any(m in text for m in ['{LB','{ALIGN','{PAD'])
        assert all(32<=ord(c)<127 for c in text)
        assert text.count('{MACRO:FI}')==bytes.fromhex(row['source_hex'])[1:].count(b'FI')
        row.update(english=text,logical_English=text,speaker=speakers[row['source_selector']],
            source_meaning=row['refined_source_gloss'],context='North Sea trade-house confrontation after the B39 Amsterdam signal; '+row['refined_source_gloss'],
            localization_note=reason,editorial_finding=reason,decision=decision,editorial_decision='retain' if decision=='retention' else 'revise',
            retention_reason=reason if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            effective_predecessor_template_hex=prior['effective_predecessor_template_hex'],effective_predecessor_paragraph=old,
            registered_catalogue_match=prior['registered_catalogue_match'],
            source_branch_context_proof=str(GLOSS),source_branch_context_proof_sha256=sha(GLOSS.read_bytes()),
            source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),
            source_control_andruntime_substitutions_must_remain_exact=True,
            current_effective_body_dispatch_andcatalogue_pending=False,
            native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending=True,
            source_prose_orcompletion_credit_added=False)
        rows.append(row)
    counts=Counter(r['decision'] for r in rows);assert sum(counts.values())==61
    byid={r['id']:r for r in rows};reviews=[]
    for p in paths['representative_text_paths']:
        ordered=[byid[i] for i in p['source_speech_IDs']];ids=set(p['source_speech_IDs']);v=p['raw_results']
        assert len(ordered)==p['source_speech_count'] and len(ids)==len(ordered)
        assert ('DK4_MES_B49_R0107' in ids)!=('DK4_MES_B49_R0112' in ids)
        assert ('DK4_MES_B49_R0238' in ids)!=('DK4_MES_B49_R0244' in ids)
        assert ('DK4_MES_B49_R0405' in ids)==('DK4_MES_B49_R0409' in ids)
        reviews.append(dict(path=p['path'],source_speech_IDs=p['source_speech_IDs'],raw_results=v,composition_count=p['composition_count'],
            complete_English_exchange=[dict(id=r['id'],speaker=r['speaker'],english=r['english']) for r in ordered],
            shared_complete_exchange_andall_variable_chunks_contextually_reviewed=True,
            no_claim_of256_separate_human_or_emulator_playthroughs=True,
            findings=['Need something echo preserved.','Exactly one Claudio/Janus admiral confirmation.','Optional regional claims stay conditional;remaining territory is prospective.',
                'Exactly one event41 destination suggestion;event41 doesnot mean Africa cleared.','Pact is Rafael\'s interpretation of the request,not an asserted signed alliance.',
                'Common Uh works without the optional common-enemy exchange.','Camille\'s apology and optional storm joke close the confrontation.',
                'Optional Arcadius qualification has its own selected Rafael response.']))
    name_rows=[]
    for r in names['complete_clean_andcurrent_name_fields']:
        actor=r['actor_ID'];name_rows.append(dict(actor_ID=actor,name=speakers[actor],source_clean_fields=r['clean_fields'],current_fields=r['current_fields'],original_getters=r['original_getters'],
            decision='retention',retention_reason=NAME_REASONS[actor],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            full207_catalogue_UI_custom_names_actual_headers_andnative_font_bounds_pending=True))
    ROOT.mkdir(parents=True)
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,GLOSS,PATHS,NAMES,MENTIONED,Path(__file__)]}
    save(NAME_DOC,dict(format='dk4-speaker-name-review-v1',records=name_rows,mentioned_component_proof=str(MENTIONED),mentioned_component_proof_sha256=sha(MENTIONED.read_bytes()),
        no_new_name_assets_orfull207_approval=True,full207_name_role_alias_review_active=True,new_credit=0,evidence=evidence,full_goal_complete=False))
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC0.DK4',route=0,route_identity='Rafael',block=49,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],records=rows,
        revised=counts['revision'],retained=counts['retention'],typed_choice_records=[],names_packet=str(NAME_DOC),
        source_packet=current['source_packet'],source_packet_sha256=current['source_packet_sha256'],source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),
        effective_predecessor_proof=str(EFFECTIVE),effective_predecessor_proof_sha256=sha(EFFECTIVE.read_bytes()),
        complete_source_text_paths_reviewed=256,all61_four_prose_gates_true_all_formatting_gates_false=True,
        english_is_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=True,
        all_original154_commands56_relatives13_raw_predicates_query41_seven_A000_C281_andfull_end_to_preserve=True,
        source_event49_requires39_excludes151_not_natural_scheduler_orlocation_coverage=True,
        two_original_FI_substitutions_preserved_no_FA_FO_added=True,
        current_catalogue_R388_working_words_retained_two_fullwidth_I_normalized=True,
        no_scene_captures_new_ROM_registered_layer_orcompletion_credit=True,
        status='complete-source-context-prose-draft-native-display-stored-actual-policy-andregistered-release-pending',
        evidence=evidence|{str(NAME_DOC):sha(NAME_DOC.read_bytes())},new_credit=0,new_emulator_runs=0,full_goal_complete=False)
    save(DOC,doc)
    save(ROOT/'61_contextual_decisions256_paths_individual_revisions_retentions.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAME_DOC),names_sha256=sha(NAME_DOC.read_bytes()),
        records=61,revisions=counts['revision'],retentions=counts['retention'],complete_English_path_reviews=reviews,
        source_context_native_names_paths_andcurrent_effective_dispatch_precede_manuscript=True,
        all61_formatting_gates_false_native_actual_policy_registered_release_pending=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B49 complete contextual draft:',dict(counts),'61records/256source paths;seven scoped name retentions. All formatting gates false;no credit.')
