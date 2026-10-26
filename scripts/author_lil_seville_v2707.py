"""Source-first whole B28/B29 exchange;natural v2 prose,formatting pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_prose_v2707')
PACKET=Path('work/analysis/lil_Seville_source_v2704b/complete20_clean_current_native_context.json')
CONTROLS=Path('work/analysis/lil_Seville_controls_v2706b/source_bound_B28_B29_presenter_and_control_contract.json')
BRANCHES=Path('work/analysis/lil_Seville_branches_v2705/original_relative_skip_operand_proof.json')
OUT=Path('translations/lil_seville_encounter_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_seville_choices_editorial_draft_v1.json')
# Faithful gloss,localized paragraph,individual reason. The complete20-object
# exchange is reviewed before these paragraphs are written;storage neighbors are
# never treated as proof that mutually exclusive responses occur consecutively.
PROSE={
(28,6):('Valdes identifies Lil contemptuously as the little country merchant girl who has recently been encroaching on Spanish territory.',
 "So you're that little merchant girl from the sticks who's been making trouble in Spanish territory lately?",
 'Restore his full contemptuous identification andaccusatory question. From the sticks naturally carries the rural put-down;making trouble preserves his allegation without the older unsupported implication that she has been raiding orcommitting piracy. This is Valdes opinion,not narrator fact.'),
(28,17):('Gerhard hesitantly suspects that he recognizes the man.',
 'Could that be...?',
 'Retain the natural restrained recognition question anddeliberate trailing uncertainty. The man is the visible interlocutor in this exchange;repeating this man oradding a name would not improve the English. The identity is confirmed only in the later beat.'),
(28,24):('Lil demands to know who Valdes is andobjects that he does not know how to treat a lady respectfully.',
 'And who do you think you are? Is that any way to speak to a lady?!',
 'Preserve both the indignant challenge andthe complaint about manners. The rhetorical English carries her offended dignity naturally without inventing an actual noble title or a relationship.'),
(28,35):('Fernando addresses Lil andasks her to ignore him,because Fernando does not want to become involved in trouble.',
 "{MACRO:FI}, just ignore him... I don't want to get dragged into trouble.",
 'Restore the personal reluctance andrisk of becoming involved instead of the older clipped generic No need for more trouble. Preserve the genuine captain-name macro andthe trailing hesitation without authoring a line break or inventing earlier trouble.'),
(28,42):('Valdes scoffs that a country girl needs no courtesy,introduces himself as Pedro de Valdes,a Spanish naval admiral,andasserts that he controls this region.',
 "Hmph! Country girls don't deserve courtesy! I'm Admiral Pedro de Valdes of the Spanish navy. I command this region!",
 'Restore the contemptuous grunt,complete self-introduction,explicit source admiral rank,navy andregional authority claim. The established Pedro de Valdes spelling agrees withthe Japanese name andprior approved prose. His claim ofcommand is speech,not a new proof ofpolitical ownership. No invented Lord,kinship orhigher rank is added.'),
(28,54):('Gerhard confirms his earlier suspicion that the man is Valdes.',
 'So it is Valdes...',
 'Retain the complete natural confirmation andtrailing reserve. It follows the earlier uncertain recognition andValdes self-introduction without adding surprise,a relationship or a new title.'),
(28,61):('Valdes demands confirmation that Lil understands what it means to make an enemy oftheir Spanish Invincible Armada.',
 "You know what it means to make an enemy of Spain's Invincible Armada, don't you?!",
 'Restore the complete intimidating rhetorical question andthe source conventional Invincible Armada designation. The term preserves cultural/story context andValdes boast;it is not a narrator guarantee ofinvincibility orvictory. No new enemy,weapon orwar result is invented.'),
(28,65):('Lil reacts silently withanellipsis andemphatic exclamation.',
 '...!!',
 'Preserve the native punctuation-only response that the Japanese-only CSV filter omitted. Localize punctuation to the English ellipsis/exclamation convention without inventing spoken words,an attack or an emotional diagnosis. The typed4000speech command and02speaker state establish that this is a real dialogue beat.'),
(28,69):('Valdes says it is not too late:quietly withdrawing fromthis region is acceptable,butrefusal will lead him to crush Lil.',
 "It's not too late. Withdraw from this region quietly, and I'll leave it at that. Refuse, and I'll crush you!",
 'Keep the opportunity to back down,the region,acceptance condition andthreat. Remove the older and live:the source makes no explicit survival guarantee ordeath threat. I will leave it at that naturally expresses the conditional よし;his threat remains speech intent,not a guaranteed outcome.'),
(28,81):('Janus gives a flustered cry andurges that they withdraw.',
 "W-whoa! Let's back down...",
 'Preserve the stammered alarm andinclusive appeal. Back down is natural in this intimidation exchange;the source does not order sailing to a new port orinvent a casualty. Do not add a title,age orrelationship to Janus.'),
(28,99):('After Lil agrees to withdraw,Valdes expresses surprise that she is reasonable,warns her never to interfere again,andsays he will show no mercy next time.',
 "Oh? You're more reasonable than I expected! Don't interfere again. Next time, there'll be no mercy!",
 'Restore the surprised condescension andcomplete warning rather than the unnatural A sensible surprise. Preserve again andnext time;do not change the threat into a present attack or a promised death.'),
(28,103):('The system reports that the player market share in Seville has decreased.',
 'Our share in Seville has fallen.',
 'Retain the clear existing system report. The trading context supplies market share;the source does not give a percentage,total loss,permanent ownership change or a different town. Preserve the raw FEselector andits separate anonymous paper consumer.'),
(28,115):('Gerhard reluctantly acknowledges that Valdes appears stronger,andcounsels building their strength for now.',
 'It pains me to admit it, but he seems stronger than we are. We should build up our strength for now.',
 'Restore the reluctant personal acknowledgment,appearance qualification in ようです,andcomplete measured advice. Stronger remains general as in the source;do not invent a comparison ofspecific weapons orpersonal muscles. The advice is temporary anddoes not guarantee a future victory.'),
(28,134):('Janus addresses Lil respectfully andstammers to ask whether they are really going to fight.',
 '{MACRO:FI}... A-are we really going to fight?!',
 'Restore the fearful stammer andcomplete question. Use the genuine captain-name macro for the polite address instead of inventing Lady,Miss,a rank orkinship. The question does not assert that combat has already begun.'),
(28,140):('Valdes infers that Lil wants a painful lesson,accepts the challenge andthreatens lifelong regret.',
 "So you want to learn the hard way... Very well. You'll regret this for the rest of your life!",
 'Localize 痛い目 by its threatening effect as learn the hard way. Preserve the escalating inference,acceptance andlifelong-regret threat as a complete exchange beat. No death,prisoner treatment,weapon or actual result is added.'),
(29,6):('In the follow-up Valdes infers that Lil will not understand until she has had a painful lesson.',
 "Looks like you'll have to learn the hard way.",
 'Restore the source inference andconditional need for a painful lesson. The older Pain is the only lesson you understand asserted a lasting psychological trait. The natural idiom conveys the threat without inventing a particular punishment or an actual injury.'),
(29,9):('Lil says she has changed her mind,she too has pride,andwill not give in to military force.',
 "I've changed my mind! I've got my pride, too! I'm not giving in to force!",
 'Restore her explicit personal change ofmind andpride as well as the refusal. Force refers to Valdes military intimidation already established in the conversation;the English does not invent a new army,weapon or battle result. Her defiance remains distinct from Gerhard caution andJanus alarm.'),
(29,13):('Valdes scoffs,allows Lil to do as she pleases,andthreatens to crush her withhis full strength.',
 "Hmph. Suit yourself. I'll crush you with everything I've got!",
 'Keep the contemptuous dismissal andrestore the full-strength promise in 全力で,which the older Prepare to be crushed omitted. Everything I have got is idiomatic threat language,not a new guarantee that every ship orcrew member will be used orlost.'),
}
CHOICE_PROSE={
0:('Lil accepts the demand andsays she will back down in this situation.',"All right. I'll back down.",'Restore the complete acknowledgment andpersonal withdrawal reply instead of the clipped Withdraw. The situation supplies here;the English makes no promise to withdraw forever anddoes not invent a future plan. Preserve stored option0andits original outcome branch.'),
1:('Lil emphatically refuses to back down.',"I'm not backing down!",'Restore the complete emphatic refusal instead of the isolated Never. It naturally carries her defiant voice andcontrasts withoption0without a new insult or military claim. Preserve stored option1andthe original branch order.'),
}
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,OUT,CHOICES]);packet=read(PACKET);control=read(CONTROLS);branch=read(BRANCHES)
    assert control['source_context_sha256']==branch['source_context_sha256']==sha(PACKET.read_bytes())
    assert len(control['all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE'])==36 and len(branch['cases'])==280
    records=[]
    for source in packet['records']:
        r=deepcopy(source);key=(r['block'],r['source_record_index']);gloss,english,note=PROSE[key];prefix=r['source_presentation_prefix_hex'].upper()
        decision='retain-wording' if key in [(28,17),(28,54),(28,103)] else 'revise'
        if decision=='retain-wording':assert english==' '.join(r['current_English'].split())
        r.update(english='{SPEAKER:'+prefix+'}'+english,source_meaning=gloss,localization_note=note,editorial_decision=decision,
            context=packet['scope']+' This record belongs to the complete original scene/branch indicated by its native command andancestor offsets;storage order alone is not a consecutive exchange.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='fresh-source-context-prose-reviewed;current-native-formatting-reference-map-and-registered-integration-pending')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        records.append(r)
    choices=[]
    for source in packet['typed_choice_records']:
        r=deepcopy(source);gloss,english,note=CHOICE_PROSE[r['option_index']]
        r.update(english=english,source_meaning=gloss,localization_note=note,editorial_decision='revise',context='Original B28typed2100reply choice follows Valdes conditional threat. Stored0accepts withdrawal;stored1refuses. Preserve source branch order,pointer table andnormal modal-result handling. B29is a separate original follow-up action,not an automatic second reply.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='fresh-source-context-prose-reviewed;typed-native-menu-layout-and-integration-pending')
        choices.append(r)
    assert len(records)==18 and len(choices)==2 and sum(r['editorial_decision']=='retain-wording' for r in records)==3
    ROOT.mkdir(parents=True)
    common=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],required_runtime_ARM9_sha256=packet['current_ARM9_sha256'],source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),control_contract=str(CONTROLS),control_contract_sha256=sha(CONTROLS.read_bytes()),branch_proof=str(BRANCHES),branch_proof_sha256=sha(BRANCHES.read_bytes()),formatting_review_pending=True,completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False)
    save(OUT,dict(**common,format='dk4-natural-dialogue-manuscript-v2',encoder='dialogue-relocatable-v1',dialogue_profile='lil-opening-editorial-native-v1',scoped_B28_B29_profile_still_required=True,records=records,
        revised=15,retained=3,no_authored_line_breaks_or_padding=True,no_ROM_registered_release_or_actual_Seville_approval=True))
    save(CHOICES,dict(**common,format='dk4-native-two-choice-editorial-manuscript-v1',records=choices,revised=2,retained=0,typed_command=0x2100,stored_order=[0,1],no_ROM_or_actual_selection_claim=True))
    save(ROOT/'complete_exchange_editorial_review.json',dict(source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),
        full_exchange_objects=20,fresh_individual_glosses_and_localization_reasons=20,revisions_proposed=17,justified_retentions=3,includes_previously_omitted_native_silent_reaction=True,source_unsupported_piracy_and_survival_implications_removed=True,
        original_choices_and_separate_followup_kept_distinct=True,all_prose_one_logical_paragraph_without_authored_breaks=True,source_prose_credit_added=0,completion_credit_added=0,current_native_reference_map_release_and_representative_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('20Seville objects freshly reviewed:17proposed revisions/3justified retentions;fullchoice/conditional/follow-up context andomitted silence preserved. Formatting/relocation/release pending;no credit orROM edit.')
