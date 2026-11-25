"""Whole-exchange clean-Japanese editorial review; five gates remain separate from display approval."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B137_B45_B46_prose_v8241')
CURRENT=Path('work/analysis/Hodram_B137_B45_B46_current_v8239/28_exact_clean_current_refs_after_whole_source_glosses.json')
EFFECTIVE=Path('work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v1.json')
REVISIONS={
 (137,14):("You were with that brat! What do you want?!","Keep Charles's sharp recognition and hostile demand. With that brat conveys the source association and derogatory小娘 without inventing a friendship, kinship or occupation. His following silence and eventual acceptance of Hodram's response must remain distinct."),
 (137,17):("I had to come and apologize to all of you... I'm so sorry! She said such awful things...","Restore Camille's urgent wish to apologize to everyone, direct contrition and dismay at Lil's words. This answers Charles's hostility and leads into the hesitant defense of Lil. The source concerns insults, not an invented physical assault or a new apology by Lil herself."),
 (137,28):("Once she decides someone's a business rival, she just... can't seem to talk to them any other way.","Once she decides preserves Camille's account of Lil's perception, rather than treating every target as an objectively established rival. The hesitation and can't seem to make his explanation tentative and apologetic; any other way refers back to the witnessed rude speech."),
 (137,32):("She's kind, really. It's just... she tends to jump to conclusions, and she gets so convinced she's right... Please forgive Lil!","Preserve the qualified defense, both hasty conclusions and strongly held assumptions, and Camille's uncomfortable attempt to explain them. So convinced she's right is natural English for the source's strong思いこみ; it does not excuse the insult or introduce a diagnosis. The plea comes before Gerhard's deliberate silence."),
 (137,47):("Thank you for your gracious apology. With someone as capable as you at her side, it's no wonder she's able to make the most of her talents.","Replace compressed Your apology is welcome/You help her talent shine with Hodram's complete courteous acknowledgment and explicit recognition of Camille's ability. At her side describes the supported association, without romance, a newly assigned rank or a recruitment offer. The praise motivates Camille's flustered modest response."),
 (137,50):("N-no... You're too kind.","Use an idiomatic modest response to praise. The source's stammer and denial are polite self-effacement, not a literal claim that Hodram has praised the wrong person. You're too kind adds no event or relationship."),
 (137,58):("Oh, thank you so much! Well... I'll be going, then!","Preserve Camille's relieved gratitude and polite, slightly hesitant departure. I'll be going, then expresses失礼します naturally after the reassurance without inventing another appointment or motive. It leads into Hodram's silent pause after the exit."),
 (137,82):("Hm... Come to think of it, our own fleet is getting short-handed.","Restore Hodram's reflective change of subject and the developing staffing need inそろそろ. This is his assessment after Gerhard praises the visitor, not proof of a precise roster count or an order to recruit Camille."),
 (137,86):("We'll need more capable people if we're to expand the fleet.","Replace the impersonal passive More talent is needed with Gerhard's natural professional agreement. Retain the conditional relationship between fleet expansion and capable personnel, without guaranteeing recruits or increasing an already fixed ship count."),
 (137,89):("Many countries around the Mediterranean live by sea trade. We might find capable people in major cities like Lisbon and Seville.","Restore the countries' maritime-trade context, the broader capable people rather than only sailors, both named cities andかもしれません uncertainty. Live by sea trade is idiomatic for海洋貿易立国. Do not silently relocate Lisbon or Seville, promise a recruit, or convert the advice into an already completed journey."),
 (137,92):("Agreed. It would also be worth extending our trade routes to the towns around the Mediterranean.","Keep Hodram's considered agreement and prospective route-network expansion as an additional benefit. Replace through that sea with a natural explicit regional reference. The proposal does not establish that the routes, contracts or visits have already occurred."),
 (46,10):("So I hear you're the richest person in these waters? Then let's have a contest!","Preserve reported regional wealth as a question and Lil's brisk challenge. Remove captain, which narrows the comparison to an unsupported class, and make the contest explicit so Hodram's following question is coherent. No agreed wager, strongest-fleet claim or world dominance is added."),
 (46,14):("A contest?","Echo Lil's勝負 as a puzzled question. Duel wrongly specified a physical fight; the next speech defines a first-to-find treasure contest. Hodram has not accepted it or asked for combat."),
 (46,19):("This is the key to deciphering a treasure map. Whichever of us finds the treasure first will rule the North Sea!","Correct reveals a map to the source's aid for deciphering a map, and make the thing being found explicitly the treasure. The mutual you-or-me race and North Sea supremacy remain Lil's boast about the proposed contest, not a newly established rank or present ownership. Original4800 identifies Red Dye separately; the dialogue need not insert its name. This speech does not explicitly give Hodram a new map or announce that he has accepted or won."),
 (46,23):("And no holding back! This is serious. I'm not losing to you, of all people!","Render手かげんなし and真剣しょーぶ as a serious contest, rather than combat-oriented No mercy. Restore Lil's especially defiantあんたにだけは with of all people. I'm not losing is competitive resolve, not an objective guarantee of the outcome or an invented feud."),
 (46,51):("A key to a map? What does she mean...?","Keep Hodram's puzzled reflection after Lil's challenge. What does she mean asks about her unexplained statement; the old What is it could instead ask for the already identified object's name. Preserve uncertainty and the trailing thought without preemptively solving the map mechanic or adding spoken/private staging before actual presentation is checked."),
}
RETENTIONS={
 (137,6):"Hm? is a natural short questioning reaction from Charles on noticing the visitor. The following hostile recognition supplies the identification; no extra greeting or relationship is needed.",
 (137,10):"Um... Sorry about before. naturally preserves Camille's hesitant attempt to begin an apology. The next lines develop exactly what happened, so repeating the whole confrontation here would spoil the pacing.",
 (137,21):"Retain the exact ellipsis as Charles's deliberate silence after Camille's urgent apology. Do not manufacture agreement, an insult or a new judgment. Its separate speaker preamble and actual pause still need display verification.",
 (137,25):"She never meant to anger you. is clear, natural English for Camille's explanation of Lil's intent. It follows the silence and sets up the business-rival explanation without denying that Lil's words were offensive.",
 (137,35):"Retain the exact ellipsis as Gerhard's source silence after the plea. This preserves the pause before Hodram takes control of the conversation without adding forgiveness or disapproval.",
 (137,39):"Your name was Camille, wasn't it? is a natural courteous check of the visitor's name and preserves the approved Camille. The current registered runtime catalogue already supplies this effective wording despite the older stored Kamil sentence. Retain the working effective text, not that obsolete storage spelling. The source君 does not require a new rank or family address.",
 (137,43):"What? Oh, yes. works as Camille's startled response followed by a hesitant confirmation of his name. It answers Hodram's name check naturally without adding an identity revelation or new stammering facts.",
 (137,54):"Don't worry. We choose our enemies carefully. We won't harm either of you. Tell her that. preserves Hodram's restrained reassurance, deliberate choice of enemies and message for Lil. Her is unambiguous in this exchange. The compact closing instruction remains appropriate to his authority; no romantic partner, recruitment or alliance is invented.",
 (137,74):"Retain Hodram's exact ellipsis after Camille leaves. It gives the encounter a quiet beat before Gerhard's assessment. A spoken opinion here would duplicate or alter the following exchange.",
 (137,78):"A promising young man. is a natural concise assessment from Gerhard of the departing visitor and conveys先行きが楽しみ. The established source identity supports young man. It does not imply secret ancestry, a threat or a recruitment promise.",
 (45,7):"The Argot Company boss is waiting for you in Amsterdam. is natural casual port-worker speech and conveys the established Lil referent of姐さん without inventing a sister relationship. Boss suits the familiar address and existing company context; it is not a new military rank. Keep Amsterdam and the waiting invitation, not a completed meeting.",
 (46,6):"Wait! is a natural urgent interruption from Lil and matches待ちなさいよ. The next speech explains the challenge, so no extra name or motive belongs here.",
}
CONTEXTS={
137:"After Lil's earlier B44 confrontation, Camille returns to apologize. Charles is hostile, Camille hesitantly defends Lil, and Gerhard pauses. Hodram acknowledges Camille's ability and reassures him before the polite departure. Gerhard's praise then leads Hodram to consider staffing needs, and the men discuss prospective Mediterranean recruitment and trading routes.",
45:"The port worker passes on the Argot Company's invitation to Amsterdam. The source event excludes completed46; prerequisite queries do not prove a total chronology, natural activation or that the meeting has already happened.",
46:"Lil challenges the reported richest person in the region to find treasure first. An original4800 resource with Red Dye/layout0 accompanies her explanation of a map-deciphering key. Lil insists on a serious contest and refuses to lose; Hodram remains puzzled. Event46 requires137 and45, but no natural activation, gift of a new map, acceptance or victory is established by this prose review.",
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    current,effective,names=map(read,[CURRENT,EFFECTIVE,NAMES])
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    assert set(REVISIONS).isdisjoint(RETENTIONS) and len(REVISIONS)==16 and len(RETENTIONS)==12
    assert len(current['records'])==28 and sum(len(g['all_current_commands']) for g in current['groups'])==60
    getters=read(effective['native_names_packet'])['native_twelve_progressive_andfull_getters']['rows']
    speakers={r['actor_ID']:r['text'] for r in getters if r['consumer']=='progressive-nameplate'}
    assert speakers=={1:'Hodram Bergstrom',2:'Lil Argot',9:'Camille Overijssel',16:'Gerhard Ardelknatts',18:'Charles Rochefort',113:'Port Worker'}
    speakers[16]='Gerhard Adernkatz'
    rows=[]
    for original in current['records']:
        row=deepcopy(original);key=row['block'],row['source_record_index']
        prior=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        old=prior['effective_predecessor_paragraph']
        if key in REVISIONS:text,reason=REVISIONS[key];decision='revision';assert text!=old
        else:text,reason=old,RETENTIONS[key];decision='retention';assert text==old
        assert all(32<=ord(c)<127 or c=='…' for c in text)
        assert not any(t in text for t in ['{LB','{ALIGN','{PAD','\n','\r','FI','FA','FO'])
        if '…' in text:assert text==old=='…'
        row.update(english=text,logical_English=text,speaker=speakers[row['source_selector']],source_meaning=row['first_clean_source_gloss'],
            context=CONTEXTS[row['block']]+' '+row['first_clean_source_gloss'],localization_note=reason,editorial_finding=reason,
            decision=decision,editorial_decision='revise' if decision=='revision' else 'retain',retention_reason=reason if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            effective_predecessor_template_hex=prior['effective_predecessor_template_hex'],effective_predecessor_paragraph=old,registered_catalogue_match=prior['registered_catalogue_match'],
            source_context_proof=current['source_gloss'],source_context_proof_sha256=current['source_gloss_sha256'],source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),
            current_effective_body_dispatch_andcatalogue_pending=False,physical_neighbors_not_yet_proved_actual_path=False,
            physical_neighbors_match_one_source_TEXT_path_per_block_not_all_effect_path_attainability=True,
            source_control_andruntime_substitutions_must_remain_exact=True,native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending=True,
            source_prose_orcompletion_credit_added=False))
        rows.append(row)
    assert Counter(r['decision'] for r in rows)==dict(revision=16,retention=12)
    assert {(r['block'],r['source_record_index']) for r in rows}==set(REVISIONS)|set(RETENTIONS)
    ROOT.mkdir(parents=True)
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NAMES,Path(current['source_gloss']),Path(__file__)]}
    save(DOC,dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC1.DK4',route=1,route_identity='Hodram',blocks=[137,45,46],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        current_archive_sha256=current['current_archive_sha256'],records=rows,revised=16,retained=12,typed_choice_records=[],names_packet=str(NAMES),
        required_registered_name_asset='Gerhard Adernkatz owned12-byte correction;research reference8215 is not a registered dependency',
        source_context=current['source_gloss'],source_context_sha256=current['source_gloss_sha256'],effective_predecessor_proof=str(EFFECTIVE),effective_predecessor_proof_sha256=sha(EFFECTIVE.read_bytes()),
        complete_clean_exchange_speeches_reviewed=28,prior_clean_B44_callbacks_reviewed=27,all28_four_prose_gates_true_all_formatting_gates_false=True,
        english_is_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=True,
        all60_original_commands_eight_relatives_two_raw8000_full_ends_and4800_layout0_hide4700_to_preserve=True,
        source_zero_FI_FA_FO_no_macros_added_Hodram_defaults6_9_15_distinct_from_other_routes=True,
        three_silence_records_preserved_without_added_words=True,effective_Camille_catalogue_wording_retained_not_obsolete_stored_Kamil=True,
        no_new_kinship_rank_romance_crew_guarantee_mapgift_contest_acceptance_orvictory=True,
        no_scene_captures_new_ROM_registered_layer_orcompletion_credit=True,
        status='complete-source-context-prose-draft-native-display-stored-actual-policy-andregistered-release-pending',
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    save(ROOT/'28_contextual_decisions_three_exchanges_individual_revisions_retentions.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=28,revisions=16,retentions=12,
        complete_English_exchanges=[dict(block=b,context=CONTEXTS[b],records=[dict(id=r['id'],speaker=r['speaker'],english=r['english'],decision=r['decision']) for r in rows if r['block']==b]) for b in [137,45,46]],
        findings=['Duel corrected to a contest;Lil challenges reported regional wealth,not strongest captain.','Key deciphers a treasure map;it doesnot reveal orgrant a new map,andtreasure is the object ofthe race.',
          'Mediterranean trading context,capable people,both cities andpossible ratherthan guaranteed recruitment restored.','Hodram complete courteous praise supports Camille modest reply;no new alliance orromance.',
          'Three original silences retained;Charles association doesnot invent friendship.','Existing effective Camille name-check retained withruntime catalogue provenance.','Port-worker Argot Company boss retained withindividual source/context justification.'],
        source_context_andown_captain1_effective_dispatch_precede_manuscript=True,all28_formatting_gates_false=True,
        no_new_actual_gameplay_orregistered_integration_coverage=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Hodram28:16revisions/12justified retentions;allfour prose gates true/formattingfalse;noROM orcredit change.')
    for r in rows:print(r['block'],r['source_record_index'],r['speaker'],r['decision'],r['english'])
