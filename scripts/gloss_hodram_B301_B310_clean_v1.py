"""Seal every clean-source meaning before consulting eligible current dialogue."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/Hodram_B301_B310_clean_20261107')
PACKET=ROOT/'clean_source_packet.json';SCOPE=ROOT/'clean_intake_scope_v1.json'
ORDINARY=ROOT/'all73_ordinary_clean_meanings.json';OUT=ROOT/'all234_clean_meanings_before_English.json'

CONTEXT={
301:'Matilda greets the captain, asks whether he knows the Colosseum, identifies it as Roman ruins and offers the information because she heard he was seeking ruins. Hodram welcomes the lead; she reminds him to buy a map. This does not establish a romance or a shared trip.',
302:'A complete map-gated desert expedition with eight-register companion alternatives: heat, rationing water, a sandstorm, continuing or waiting, a second wait/advance choice, fatigue, apparent departures, one day passing and eventual destination sighting. Numeric adjacency does not identify the destination or prove chronology. Departures are not stated deaths; forecasts and questions remain uncertain.',
303:'Safia welcomes the captain and thanks him for the improvement in her dancing. As thanks she relays a rumor of treasure in a mosque far inland that enshrines a former king; only someone recognized by that king can obtain it. Preserve reported status and the invitation to try, without adding a dance lesson, romance, real-world history or guaranteed reward.',
304:'Sakura asks about the map, sees the party off and does not claim to accompany the whole expedition. A swamp blocks the journey; entering gives a shallow shortcut and fatigue, while turning back costs a day and a detour. Gerhard expects arrival soon and a companion spots the destination. Preserve both paths and every source voice alternative.',
305:'Sakura invites Hodram to a temple visit. He objects that he is not Buddhist; she says they are only looking around. His map of a golden temple prompts her recognition and an offer to accompany him partway, after which the map should guide him. No conversion, family relationship, shared full journey or romance is established.',
306:'Two conditional reminders concern the Kinkaku-ji monk’s request for a memento of a Yuan emperor; the named Kublai greatsword is recognized as that object. Preserve the distinction between still seeking it and identifying the held object. Final item terminology needs its source/current label binding.',
307:'The return exchange includes a reminder to unequip the requested object, Hodram calling at the entrance and the monk recognizing it. The monk gives a remote northeastern-China/icy-sea village lead, the map-guardian clan, peninsula/east-coast mountain-foot landmarks, a warning about ordinary ships and mortal danger, and a moral warning against handing the Proof to an evil-hearted person or succumbing to evil desires. Do not invent a named region, ship requirement, religious conversion or relationship.',
308:'Eight complete companion-register reminders to visit the clan guarding the map to a Proof in a village far northeast of China. This block has a voice object and no ordinary speech; it is not control-only. Preserve different urgency, curiosity, questions and the map/Proof distinction without an invented region name.',
309:'A complete map-gated forest expedition with a wolf encounter and three choices. A scare attempt can injure Hodram; a companion can warn/intervene and be hurt, followed by Hodram’s apology and another companion’s reassurance about prompt treatment and the wolf leaving. Escape, fatigue/departures, forest exit and destination sighting are alternatives. Preserve dynamic role distinctions, all eight-slot aliases and uncertainty; no guaranteed healing, animal death, kinship or numerical casualties.',
310:'Meihua answers a city-gate inquiry. Rules forbid telling foreigners, but she says foreign pressure has made the country’s isolation largely nominal and offers to tell him secretly. This is the character’s in-game explanation, not an external historical claim or an already granted legal exemption.',
}

MEANINGS={
301:'''6|Matilda greets FI and says he has arrived at a useful moment.
9|She asks whether he knows the Colosseum.
13|The captain-role speaker repeats Colosseum as a question.
17|Matilda identifies it as Roman-era ruins and says she wanted to tell him because she heard he was searching for ruins.
21|Hodram finds the information helpful and decides to visit promptly.
24|Matilda urges caution and reminds him to buy a map.''',
302:'''71|Hodram says there is a long way ahead and tells the party to use drinking water carefully.
108|Hodram judges that the sandstorm will not subside and orders continued movement.
137|The sailors seem fatigued; some sailors appear to have left the expedition. No death is stated.
141|Hodram judges it better to let the storm pass and decides to wait a little.
180|Hodram says they cannot wait any longer and will proceed into the sandstorm.
187|The sailors seem fatigued.
193|Hodram judges advancing in the sandstorm unwise and says waiting until it subsides is their only choice.
203|Exactly one day passes.
207|Hodram observes that the storm seems to have subsided.''',
303:'''6|Safia warmly welcomes FI.
9|She credits him for a great improvement in her dancing, without specifying the exact prior help here.
12|As thanks, she offers useful information.
16|Far inland from this town is a mosque enshrining a former king, reportedly holding a wonderful treasure.
20|Rumor says only a person recognized by that king can acquire the treasure; she suggests trying a visit.''',
304:'''12|Sakura asks whether the map has been brought.
16|Hodram realizes that he forgot it.
30|Sakura says they part here and wishes the party a safe journey.
35|Hodram acknowledges and thanks her.
98|Hodram orders the party to enter the swamp.
129|Hodram expects that this route has made a considerable shortcut.
133|Gerhard agrees and expects arrival soon.
137|The sailors seem fatigued.
148|Hodram judges the swamp impassable, orders a return and another route.
155|Exactly one day passes.
159|Hodram thinks they have taken a substantial detour.
162|Gerhard agrees, but says they should be arriving soon, with a trailing reservation.
168|A companion excitedly tells the admiral that the destination has been found.''',
305:'''6|Sakura greets FI on noticing him.
10|She plans to visit a Buddhist temple today and invites him along.
13|Hodram says, unfortunately, he is not Buddhist, trailing off.
17|Sakura says that is fine because they are only going to look around.
20|Hodram recalls something related.
24|He asks whether the golden temple shown on his map is near her destination.
27|Sakura repeats golden, recognizes the temple and says it is not nearby, trailing off.
31|She offers to go partway together; afterward, following the map should bring him there.''',
306:'''13|Hodram recalls that the Kinkaku-ji monk asked him to find what was described as a memento of a Yuan emperor.
19|Hodram identifies the named Kublai greatsword as the Yuan emperor’s memento mentioned by the Kinkaku-ji monk.''',
307:'''12|Hodram recalls the Kinkaku-ji monk’s request for a Yuan emperor’s memento.
16|Gerhard reminds him that it must also be removed from equipment.
30|Hodram calls to announce himself at the entrance; this is not an apology.
34|The monk acknowledges Hodram’s arrival, then recognizes the presented object with startled certainty.
38|The monk judges that Hodram should be able to manage the task.
42|He directs them far northeast of China, to a small village near an icy sea where a clan guarding the map should live.
45|Hodram repeats the far-northeast-of-China direction thoughtfully.
49|The monk specifies the base of a huge peninsula and the foot of a high mountain on its eastern coast.
52|The destination is so remote that ordinary ships may struggle to reach it; treating the undertaking lightly could cost their lives.
55|Hodram is silent.
59|The monk forbids giving the Proof to anyone with evil intentions and warns Hodram not to become captive to evil desires himself.
62|Hodram respectfully promises to keep the warning firmly in mind.''',
308:'',
309:'''89|A sailor gives a shrill frightened cry.
94|Hodram orders calm.
98|The sailor nervously asks what Hodram intends to do.
117|Hodram tells the others to leave it to him and says he will drive the wolf off.
140|Hodram exclaims in pain or effort and admits he let his guard down.
167|He dismisses the wound as a mere scratch and tells others not to worry.
174|FI has been injured; this is the captain’s name substitution, not an unspecified sailor.
178|Hodram orders formation and a single concerted push through.
226|Hodram urgently asks whether the injured companion is all right.
249|Hodram says the incident would not have happened had he not lost his balance and sincerely apologizes.
273|Hodram accepts the reassurance.
280|The sailors seem fatigued.
285|Hodram thinks that wolf is hungry and urges immediate flight as the better choice.
294|The sailors are fatigued, stated directly; several seem to have left the expedition. No deaths are specified.''',
310:'''6|Meihua welcomes FI.
9|She asks whether he wants to know where this town’s city gate is.
13|She says the rules actually forbid telling foreigners, trailing into a qualification.
16|She says foreign pressure has made the country’s closed-door policy largely nominal, agrees and offers to tell him secretly.''',
}

STYLE={
(302,24):[
'The companion hesitantly warns that proceeding without a map could lead them astray.',
'The companion directly states that a map is needed here.',
'The companion insists that going ahead without consulting a map is impossible.',
'The companion says they must obtain a map first to avoid getting lost.',
'The companion bluntly warns that going on without a map is a bad idea.',
'The companion warns that they will lose their way without a map.',
'The companion plaintively warns that they will get lost without a map.',
'The companion formally warns that they will get lost without a map.'],
(302,392):['A calm observation that the place is very hot.','A terse complaint about the heat.','A sigh and conversational complaint about the heat.','An emphatic, light complaint about how hot it is.','A drawn-out blunt complaint about the heat.','An older-register observation that it is very hot.','A youthful sigh and complaint about the heat.','A polite, emphatic observation about the heat.'],
(302,596):[
'A severe sandstorm may make continued travel lose the way; ask what to do.',
'A severe sandstorm and possible loss of direction; ask the admiral what to do, with hesitant pauses.',
'An energetic alarm about the severe sandstorm, certain expectation of getting lost and a question about what to do.',
'An elegant anxious observation that a severe sandstorm has arisen, worry about getting lost and a question to the admiral.',
'A blunt observation that the storm is severe and they could get lost; ask whether to go anyway.',
'An older-register observation of the severe storm, likely lost direction and a question about the plan.',
'A youthful anxious observation that the storm has become severe and they would surely get lost; ask what to do.',
'A formal observation that entering the storm is tantamount to losing the way; ask whether to go despite it.'],
(302,1320):['A hesitant acknowledgment followed by proposing to try going onward.','A restrained acknowledgment that if the admiral says so, they will advance.','A reluctant conversational acknowledgment followed by agreement to go.','An elegant, hesitant acknowledgment and agreement to advance.','A blunt acknowledgment and readiness to go.','An older-register acknowledgment of the admiral’s decision and proposal to try advancing.','A doubtful acknowledgment followed by a suggestion to proceed anyway.','A polite acknowledgment that the order is understood and proposal to advance.'],
(302,1786):[
'After waiting, the storm shows no sign at all of subsiding; ask what to do.',
'After a pause, say the storm does not seem likely to subside; ask the admiral what to do.',
'A thoughtful hesitation: even more waiting may not stop the storm; ask what to do.',
'After a pause, elegantly observe that the storm shows no sign of easing; ask what to do.',
'After a pause, bluntly note the storm seems unlikely to subside and ask the admiral what to do.',
'An older-register thoughtful grunt and observation that the storm shows no sign of easing; ask the plan.',
'A youthful thoughtful hesitation that even more waiting may not stop the storm; ask what to do.',
'After a pause, formally note that the storm is unlikely to subside; ask what to do.'],
(302,2582):['A hesitant expectation that they will soon leave the desert.','The desert ought to be behind them by now, with reservation.','A hesitant statement that they should have left the desert by now.','An elegant trailing question that they should be out of the desert by now.','A blunt expectation that they should be getting out of the desert soon.','An older-register expectation that the desert should end shortly, with reservation.','A youthful trailing observation that the desert should be ending now.','A polite expectation that they should be out of the desert shortly, with reservation.'],
(302,2900):['Tell the admiral to look at something, politely.','Tell the admiral to look at something, politely.','Tell the admiral to look, conversationally.','Tell the admiral to look, conversationally.','Tell the admiral to take a look, bluntly.','Tell the admiral to look, in an older imperative register.','Call the admiral’s attention and tell him to look, youthfully.','Call the admiral’s attention to something there, formally.'],
(304,164):['Suggest that they now go onward.','Suggest that they now go onward.','Energetically suggest getting going.','Suggest that they now go onward.','Casually suggest getting going.','Suggest setting out in an older register.','Give an excited departure call.','Formally suggest setting out.'],
(304,296):['A swamp is ahead; ask what to do.','A swamp is ahead; pause and ask the plan.','They have run into a swamp; conversationally ask what to do.','An elegant surprised observation of a swamp and question about the plan.','A blunt observation that they have hit a swamp and question about what to do.','An older-register observation that it is a swamp and question about the plan.','A youthful surprised complaint that they have run into a swamp and question about what to do.','A formally surprised observation that a swamp lies ahead and question about the plan.'],
(304,638):['Observe that the swamp is surprisingly shallow.','Observe that it is shallower than expected.','Observe that it is surprisingly shallow and express relief.','Elegantly observe the surprising shallowness and relief.','Bluntly observe the surprising shallowness.','Give a relieved older-register observation of the surprising shallowness.','Express youthful surprise that it is shallower than expected.','Politely observe that it is shallower than expected.'],
(308,8):[
'Urge a visit to the clan guarding the map to a Proof; confirm the village is far northeast of China.',
'Urge visiting that map-guardian clan as soon as possible and recall that their village is far northeast of China.',
'Wonder what the clan guarding the Proof’s map is like, recall the northeastern-China village and suggest going right away.',
'Suggest visiting the map-guardian clan before forgetting; confirm the village far northeast of China.',
'Bluntly suggest visiting the map-guardian clan soon; ask confirmation that it lives in a village far northeast of China.',
'In an older register, return to the subject of the Proof, suggest visiting the map guardians soon and propose the village far northeast of China.',
'Youthfully express curiosity about the people guarding the Proof’s map and propose visiting the village said to be far northeast of China.',
'Politely express interest in the Proof’s map, propose visiting its guardian clan’s village and recall its far-northeastern-China location.'],
(309,24):['Warn the admiral that they will get lost without a map.','State to the admiral that they will get lost without a map.','Ask whether going without a map would be a bad idea.','Elegantly warn that they could get lost without a map.','Bluntly insist that having no map is dangerous.','Warn the admiral that they will lose their way without a map in an older register.','Youthfully say that going onward requires a map.','Formally warn that they will get lost without a map.'],
(309,322):['Suggest getting going.','Suggest getting going.','Energetically suggest getting going.','Suggest getting going.','Casually suggest getting going.','Suggest going in an older register.','Energetically suggest getting going.','Suggest getting going.'],
(309,422):['Stammer an alarm to the admiral that a wolf is present.','A terse alarm that a wolf is present.','Conversationally stammer an alarm to the admiral about a wolf.','A high frightened cry and alarm about a wolf.','A startled blunt cry that a wolf has appeared.','Stammer an older-register alarm to the admiral about a wolf.','Give a youthful frightened cry and alarm about a wolf.','Stammer a formal alarm to the admiral that a wolf is there.'],
(309,810):['An alarm to the admiral to watch out.','An alarm to the admiral to watch out.','An urgent conversational alarm to the admiral to watch out.','An urgent elegant alarm to the admiral to watch out.','A sudden blunt warning of danger.','An urgent older-register alarm to the admiral to watch out.','An urgent youthful stammered alarm to the admiral to watch out.','An alarm to the admiral to watch out.'],
(309,1006):['Urgently ask whether Hodram is all right, politely.','Urgently ask whether Hodram is all right, politely.','Urgently ask whether he is all right, conversationally.','Urgently ask whether Hodram is all right, politely.','Urgently ask whether Hodram is all right, politely.','Ask whether he is all right in an older direct register.','Ask whether he is all right in a youthful register.','Urgently ask whether Hodram is all right, politely.'],
(309,1214):['Shout a warning of danger.','Shout a warning of danger.','Shout a warning of danger.','Shout a warning of danger.','Give a blunt shouted warning of danger.','Shout a warning of danger.','Give a youthful shouted warning of danger.','Shout a warning of danger.'],
(309,1278):['A cry of pain.','A cry of pain.','A cry of pain.','A high shrill cry of pain.','A cry of pain.','A short older-register yelp of pain.','An exaggerated youthful cry of pain.','A cry of pain.'],
(309,1368):['A pained effort to say they are managing somehow.','A pained effort to say they are managing somehow.','A conversational pained exclamation that it hurts.','An expressive pained cry that it hurts.','A pained, stammered insistence that the injury is not serious.','A pained, stammered older-register reassurance that they are all right.','A tearful youthful cry insisting they are not all right.','A pained effort to say they are managing somehow.'],
(309,1590):[
'Reassure that prompt treatment will make things all right; the wolf has also fled.',
'Tell the admiral not to worry: prompt treatment should heal the injury, and the wolf has fled.',
'Conversationally reassure that prompt treatment is all that is needed and the wolf is gone.',
'Elegantly say prompt treatment is needed and express relief that the wolf is gone.',
'Bluntly tell the admiral not to worry: prompt treatment will heal such a wound, and the wolf is gone.',
'In an older register, urge against dwelling on it: prompt treatment will prevent this wound becoming serious; the wolf has left, settling the incident.',
'Youthfully reassure that prompt first aid will make things all right and express relief that the wolf has fled.',
'Politely reassure that this degree of wound will heal with prompt treatment and the wolf has fled.'],
(309,2364):['Pant and say they should be safe now that they have reached here.','Pant and say they should be safe now that they have reached here.','Pant and tentatively ask whether they are safe here.','Pant and tentatively ask whether they are safe here in an elegant register.','Pant and ask for reassurance that they are safe here, bluntly.','Wheeze and stammer an older-register reassurance that they are safe now.','Give youthful breathless gasps and ask whether fleeing this far makes them safe.','Pant and politely say they should be safe here.'],
(309,2758):['Expect that they will leave the forest soon, politely.','Expect that they will leave the forest soon, politely.','Conversationally ask whether they are nearly out of the forest.','Expect that they will leave the forest soon, politely.','Bluntly expect that they will leave the forest soon.','Expect that they will leave the forest soon in an older register.','Youthfully expect that the forest must be ending now.','Expect that they will leave the forest soon, politely.'],
(309,2938):['Tell the admiral that the destination is coming into view.','Tell the admiral that the destination is coming into view.','Conversationally identify the destination to the admiral.','Elegantly tell the admiral it is coming into view.','Tell the admiral that the destination is coming into view.','Tell the admiral that it is in view in an older register.','Youthfully celebrate finding it and call the admiral’s attention.','Tell the admiral that the destination is coming into view.'],
}

CAPTIONS={(302,1226):['Continue onward.','Wait for the storm to subside.'],
    (302,2272):['Advance into the sandstorm.','Wait a little longer.'],
    (304,576):['Enter the swamp.','Turn back.'],
    (309,738):['Drive the wolf away.','Fight it.','Flee.']}

def main():
    assert not ORDINARY.exists() and not OUT.exists()
    scope,packet,styles,menus=map(load,(SCOPE,PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json'))
    assert scope['total_editorial_objects']==234 and scope['all_completed_exclusion_keys_checked']==18133 and scope['source_key_overlap_with_completed_credit']==0
    assert styles['object_count']==23 and styles['physical_alternatives']==152 and styles['style_alias_slots']==184
    assert menus['object_count']==4 and menus['caption_count']==9
    assert {(o['block'],o['offset']) for o in styles['objects']}==set(STYLE)
    seal(PACKET,ORDINARY,MEANINGS,CONTEXT,Path(__file__))
    ordinary=load(ORDINARY)['records'];assert len(ordinary)==73
    rows=[]
    for original in ordinary:
        row=deepcopy(original);row.update(exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    for original in styles['records']:
        row=deepcopy(original);indices=row['source_style_indices'];key=(row['block'],row['source_command_offset'])
        assert len(STYLE[key])==8 and all(STYLE[key][i]==STYLE[key][indices[0]] for i in indices)
        row.update(source_meaning=STYLE[key][indices[0]],exchange_context=CONTEXT[row['block']],
            personality_voice_notes=[dict(source_index=i,register=STYLE[key][i]) for i in indices],source_only_not_final_English=True)
        rows.append(row)
    for original in menus['records']:
        row=deepcopy(original);row.update(source_meaning=CAPTIONS[(row['block'],row['source_command_offset'])][row['source_index']],
            exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    assert len(rows)==234 and len({r['id'] for r in rows})==234
    save(OUT,dict(records=rows,records_count=234,ordinary_speeches=73,physical_personality_alternatives=152,typed_captions=9,
        complete_exchange_contexts=CONTEXT,source_meanings=234,remaining_meanings=0,English_drafts=0,current_story_English_compared=0,
        all_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        no_current_English_dialogue_consulted_for_eligible_records=True,source_first_not_new_editorial_completion_credit=True,
        source_names_are_clean_metadata_not_native_consumer_orfinal_localization_approval=True,
        neighboring_B311_read_source_only_as_boundary_context_no_credit=True,
        final_item_names_andplace_terms_require_scoped_binding=True,all_five_review_gates_pending=True,
        new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):digest(p) for p in (PACKET,SCOPE,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',ROOT/'clean_name_fields.json',Path(__file__))}))
    print('Sealed234 clean meanings across ten complete blocks; no eligible current English consulted and no new credit.')

if __name__=='__main__':main()
