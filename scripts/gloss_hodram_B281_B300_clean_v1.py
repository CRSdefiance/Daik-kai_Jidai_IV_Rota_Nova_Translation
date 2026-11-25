"""Seal complete clean-source meanings before comparing eligible current English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/Hodram_B281_B300_clean_20261107')
PACKET=ROOT/'clean_source_packet.json';SCOPE=ROOT/'clean_intake_scope_v1.json'
ORDINARY=ROOT/'all242_ordinary_clean_meanings.json';OUT=ROOT/'all384_clean_meanings_before_English.json'

CONTEXT={
281:'Two conditional reminders continue the Hernan pirate job from B279–B280; no new target or reward.',
282:'A palace guard announces the king. The king credits the admiral with opening overseas activity, then requests defeat of Iskal Yasar, an Arab pirate damaging merchant fleets. Preserve formal royal/servant registers without naming the king or inventing a new rank.',
283:'After the pirate defeat, royal thanks/payment become a discussion of the fleet mission. The king argues that recognized supremacy requires all seven Proofs of Conquest; outside, Hodram and Gerhard distinguish uncertain artifact value from the comprehensive strength needed to collect them. Keep Hodram respectful at court and dry/skeptical afterward.',
284:'A retainer urgently relays the king’s summons to Stockholm; Hodram and Gerhard do not know its purpose.',
285:'Conditional reminder of the Indian Ocean pirate target, linked to B282.',
286:'A guildmaster describes William’s violent breakaway band, its former tribute relationship to Maldonado and its hidden leadership. Hodram accepts and proposes provoking William by defeating his subordinate pirates; Gerhard calls it brute force. Allegations remain the speaker’s account, not newly established external history.',
287:'William’s capture brings relief, a generous reward and Havana share. A villager then presents a strongest-warrior legend, initially praises Hodram but candidly admits approaching many strong-looking people with little expectation. The paid search requires an Ancient City Ruins map and the villager offers to accompany the expedition. Preserve the deflating joke, nonrefundable advance and city-gate rendezvous.',
288:'Port-worker referral to Havana’s guild; FA is surname address, not a faction.',
289:'Three conditional William reminders distinguish seeking him, provoking his appearance and capturing him.',
290:'Whole forest expedition: map refusal, varied companion impressions, bear warning, three-way choice, firing/play-dead/other options, intimidation or escape, injuries/fatigue/time and eventual ruins arrival. Preserve every physical voice variant, source alias, uncertain man-eater warning and Emilio’s actual-sleep joke. A warning is not proof of a species, outcome or participant.',
291:'Whole jungle/cave expedition: map refusal, Gerhard/optional Charles, slippery moss, tiger appearance, attack or escape. Shooting risks allies, so Hodram orders close combat; alternative escape observations infer lack of hunger. Preserve optional participation and nonquantified injuries, not invented deaths or guaranteed safety.',
292:'Guild monster request: fishermen call it a monstrous fish that sinks ships by biting; Hodram says encountering it is luck-dependent. Do not identify an unspoken species or promise immediate activation.',
293:'Monster return with praise, a joke about hoping there was only one, payment, Malacca share and an explicitly unverified intact ancient-kingdom ruins rumor.',
294:'Whole map-gated forest expedition: discussion of earlier Christians/possible Byzantine descendants is Gerhard’s question, then skeleton investigation choice, harmful smoke escape/aftermath or moving on, optional Charles’s disappointed curiosity and arrival. Preserve uncertainty, no added theology, plague, gas species, diagnosis or death.',
295:'A welcoming, mildly flirtatious woman offers an explicitly rumored nearby hidden Christian settlement with rock-hewn houses. No relationship or reward is invented.',
296:'Blocked route: Hodram/Gerhard would retreat, but optional Charles proposes blasting the rocks. Large gunpowder requirements lead to making it and buying sulfur at this town’s trade house. Preserve research characterization without adding real-world recipes or quantities.',
297:'Conditional Charles absence/reminder and sulfur delivery thresholds; enough sulfur leads to timber for charcoal, unavailable in this town. Exact thresholds are not spoken.',
298:'Conditional Charles absence/reminder and timber deliveries; enough timber reveals the final missing ingredient, saltpeter, reportedly sold at some Indian Ocean port. Preserve Hodram’s exasperated question and distance complaint.',
299:'Conditional Charles absence/reminder and saltpeter deliveries; enough completes the explosive, evacuation to town and the exact 3,2,1,0 countdown. Do not add a spoken detonation or casualty.',
300:'Whole map-gated expedition: locals avoid the area, a giant snake prompts fight/flight, optional Charles mentions gunpowder, then a bog trap has group-help/solo rescue alternatives, fatigue and companion discovery reactions. Do not rename the snake, call the bog quicksand or invent stat thresholds. B301 is a separate Colosseum tavern clue, not a missing continuation of this exchange.',
}

MEANINGS={
281:'''12|Hodram recalls the task of defeating pirate Hernan, roaming the Mediterranean.
24|The guildmaster angrily urges finishing Hernan quickly.''',
282:'''6|The guard respectfully greets Admiral FA and says the king summons him.
9|The king greets Admiral FA and has a private/particular favor to request.
12|Thanks to the admiral’s achievements, the kingdom’s ships can now operate beyond the Indian Ocean; a problem remains.
16|A powerful enemy appeared in Arab waters, inflicting serious damage on merchant fleets; the king wants him defeated.
19|The Arab pirate is Iskal Yasar; many punitive fleets have been defeated, leaving the admiral the king’s last hope.''',
283:'''6|The guard welcomes Admiral FA back.
9|The king warmly praises FA for defeating the formidable enemy.
12|The king orders the reward brought forward.
16|The king says the reward may be insufficient for the achievement but asks him to accept it.
19|Exactly 250,000 gold coins are received.
28|The king asks FA how the mission is progressing.
31|Hodram responds formally and affirmatively.
35|The king suggests an essential point remains undefined.
39|What would make the fleet Hodram aims to build the strongest in the world?
42|Hodram is puzzled and respectfully asks what the king means.
45|Calling oneself strongest is easy; the title only means something when everyone recognizes it.
48|Hodram echoes the idea of recognition by everyone.
52|The king asks whether Hodram has heard of the symbols of world supremacy coveted by the great powers.
56|Hodram respectfully identifies them as the Proofs of Conquest.
60|The king acknowledges that Hodram already knows of them.
64|The king means those Proofs reportedly scattered throughout the world.
68|Reportedly only people qualified to rule each sea region can acquire its Proof.
72|Collecting all seven would demonstrate the kingdom’s strength domestically and abroad.
76|The king urges this feat to elevate Sweden into the ranks of the great powers.
80|Hodram formally accepts the charge.
85|Hodram dryly observes that hunting ill-understood treasures has now become a royal command.
89|Gerhard questions whether the Proofs truly have the significance the king assigns them.
93|Hodram does not know, though an object so eagerly sought by powerful figures seems unlikely to be worthless.
97|Conversely, people often chase fantasies with little real meaning.
100|Gerhard remains silent.
104|Either way, acquiring the Proofs requires defeating powerful rivals in every region who seek the same thing.
107|It will certainly require sophisticated overall strength beyond local battles.
111|In that sense the Proofs still demonstrate that theirs is the strongest fleet.
115|Gerhard understands: gathering the Proofs can be treated as the mission itself.
119|Hodram confirms that interpretation.''',
284:'''6|A retainer says the king summons the admiral and urgently requests return to Stockholm.
9|Hodram asks in surprise whether it is the king.
13|Gerhard wonders what the king wants.''',
285:'''6|Hodram recalls the task of defeating pirate Iskal in the Indian Ocean.''',
286:'''5|The guildmaster addresses FA, says he was looking for him and has people he wants defeated.
9|Hodram asks whether this is a job and who the opponents are.
12|They were originally petty thugs paying tribute to Maldonado, dabbling in piracy and trafficking.
16|They declared independence while Maldonado was preoccupied with Escante in Mexico and Clifford in England.
19|Their boss is a pirate named William, described as especially vicious.
23|They attack merchant and immigrant ships, kill every prisoner and burn every village they raid.
27|Compared with them, even Maldonado seems much more decent.
31|They do not operate as an openly established faction, and William rarely appears personally.
35|Several bounty hunters sent to find leads on him never returned intact/in sound condition.
39|The guildmaster has no one else to ask.
43|Hodram judges the opponent troublesome, then agrees.
46|The guildmaster is pleased that Hodram accepts.
50|Hodram says this cannot be left alone.
54|The guildmaster praises the reassuring response and supplies an advance.
59|Exactly 25,000 gold coins are received.
65|Gerhard asks how they will find William.
68|Hodram has no lead and says force is their only option.
71|Gerhard asks what he means.
75|Defeating William’s subordinate pirates one after another should eventually provoke him into appearing.
79|Gerhard dryly calls that brute force.''',
287:'''5|Captured William makes shrill, inarticulate angry cries.
9|The guildmaster recognizes William by his voice and notes his capture at last.
12|Hodram expresses relief at finally being free of this burden; he is not the captured prisoner.
16|The impressed guildmaster offers a generous reward.
20|Exactly 180,000 gold coins are received.
46|Havana market share rises slightly, with no quantity specified.
57|The guildmaster wants to introduce someone.
61|The villager greets Hodram reservedly.
65|Hodram gives a questioning reaction.
69|Trusting Hodram’s skill, the villager asks him to find particular ruins.
73|Hodram questions the mention of ruins.
77|Their ancestors reportedly built the ruins to honor warriors.
80|Legend says only someone qualified as the strongest warrior can find them.
84|Hodram asks whether the villager means he is the strongest warrior.
88|The recent pirate defeat convinced the villager.
92|The strongest warrior must possess not only strength but a righteous heart and wisdom.
96|Hodram objects to excessive praise and hesitates to accept such a request.
100|The villager reassures him: frankly the search is as vague as grasping clouds even for his people.
104|They ask every strong-looking person they come across.
108|He apologizes for that but promises no excessive expectation, since no one has achieved it yet.
112|Hodram appreciates his honesty and feels less burdened.
115|The villager offers an advance and explicitly will not demand repayment if the search fails.
119|Exactly 5,000 gold coins are received.
125|First obtain the Ancient City Ruins map, then speak to the villager; he will accompany the search.
128|The villager will wait at this town’s city gate.''',
288:'''6|The port worker recognizes FA and says Havana’s guild has been looking for him.''',
289:'''12|Hodram recalls the task of defeating William in the New World.
23|The guildmaster asks whether William has still not appeared.
28|The guildmaster asks whether William has still not been caught.''',
290:'''62|Hodram orders the expedition onward.
92|The captain role gives a sudden alarmed reaction.
96|Another native companion role warns of immediate danger.
118|Hodram orders firing.
148|Some sailors appear to have suffered minor injuries.
175|Hodram hushes the companion and orders patience/endurance.
179|The companion role remains silent while playing dead.
214|Hodram questions Emilio by name.
218|Emilio makes a sleeping/breathing sound.
222|Hodram realizes Emilio is genuinely asleep.
233|Exactly one day passes.
278|Samwell warns that the bear might eat people and that ill-judged action could endanger them.
305|Sailor fatigue rose considerably and some injuries appear to have occurred.
313|Hodram orders everyone to run.''',
291:'''37|Hodram calls the jungle eerie.
41|Gerhard agrees and hopes nothing happens.
45|Hodram notes a cave.
49|Gerhard says it appears deep but they have no other way forward.
60|Optional Charles believes the cave must be a shortcut to the destination.
66|Hodram responds hesitantly.
70|Gerhard respectfully warns FI to watch his footing because moss is slippery.
73|Hodram acknowledges him.
77|A low animal growl is heard.
100|The companion role cries out that the creature has appeared.
115|Hodram orders firing.
119|An animal growls or roars sharply.
123|A retainer cries out in pain/alarm.
127|Hodram curses the creature’s agility.
152|Shooting will only cause more injuries, so Hodram orders close combat instead.
186|A considerable number of people appear injured; no deaths are stated.
211|A retainer exclaims with relief at being saved.
221|Hodram notices light ahead.
225|Gerhard says they can now leave the cave.''',
292:'''5|The guildmaster says Hodram arrived at a good time and requests a favor.
8|Unsure whether he will be believed, the guildmaster reports frequent monster appearances nearby.
12|Hodram questions the word monster.
16|Fishermen call it a monstrous fish; it bites ships and sinks them.
19|Several ships have actually been devoured by it since the year began, the speaker says.
22|The guildmaster hopes Hodram can handle it and asks him to defeat it.
25|Hodram says whether he encounters it depends on luck.
28|The guildmaster is willing to wait patiently and entrusts him with the task.''',
293:'''5|The guildmaster excitedly praises Hodram for actually defeating it, proving he is extraordinary.
9|Now they can only hope there was just one monster.
12|Hodram reacts sharply to that qualification.
16|The guildmaster brushes it aside and offers payment.
20|Exactly 70,000 gold coins are received.
43|Malacca market share rises slightly, with no quantity specified.
60|The guildmaster recalls an interesting rumor.
63|An entire ancient kingdom’s ruins reportedly remain intact in jungle far inland from this town.
67|Hodram asks whether it is true.
71|No one has found them; it is strictly rumor, though Hodram might succeed.''',
294:'''43|Hodram observes the dense forest.
47|Gerhard suggests that explains why no one has seen this place until now.
58|Optional Charles wants to get out of such a forest quickly.
64|Gerhard wonders whether Christians predating Islamic rule in the region were descendants of the Byzantine Empire.
67|Hodram notes that was centuries ago and hopes for a clue to a Proof.
71|Hodram is shocked by skeletal remains.
75|Gerhard supposes a previous explorer like them died here.
78|Gerhard asks whether they should examine the surroundings as a precaution.
93|Gerhard acknowledges the decision and says caution is best.
96|Hodram asks about smoke, then chokes with throat discomfort/difficulty breathing.
99|Gerhard warns FI not to inhale it and urges immediate departure.
103|Gerhard checks whether everyone is present.
107|A retainer reports everyone safe.
111|Gerhard acknowledges this, then checks whether FI is all right.
115|Hodram says he is all right and asks what that was.
118|It was harmful smoke; Gerhard had heard rumors but did not expect it here.
122|Hodram responds faintly or weakly.
126|Gerhard says the admiral is in danger and urges everyone to hurry through.
135|The sailors appear confused.
143|Gerhard concludes they should not linger in suspicious places and urges continuing.
155|Optional Charles regrets missing a possible explanation of the skeletons.
167|Hodram believes they have reached the place.''',
295:'''6|The woman welcomes the visitor.
10|She says he is rather handsome on closer inspection and offers a useful tip.
14|She asks whether he has heard of a hidden Christian settlement nearby.
17|Hodram has not heard of it.
21|Its inhabitants supposedly live in rock-hewn houses; she emphasizes it is only rumor.''',
296:'''5|Hodram reacts to the blockage.
9|Gerhard wonders whether there was a rockfall and says they cannot pass.
12|Hodram sees no choice but to turn back.
33|Charles remains silent, apparently thinking.
37|Gerhard asks Charles what is wrong and says they are returning.
40|Charles proposes blowing it up.
44|Gerhard is startled and repeats the proposal questioningly.
47|Charles explains that they can blast the obstructing rocks away.
50|Hodram asks whether he is serious: blasting such hard rock would require a great deal of gunpowder.
54|Gerhard says obtaining that much gunpowder all at once would be almost impossible.
57|Charles reassures them that they can make the gunpowder themselves.
60|Hodram asks whether he can make gunpowder.
63|Charles reminds the admiral of his research and offers to make it if they obtain a large supply of sulfur.
67|Gerhard thinks sulfur is sold in this town.
70|Charles says to buy it at the trade house and bring it here.
73|Hodram agrees to obtain sulfur.''',
297:'''11|Hodram wishes Charles were with them.
33|Hodram recalls needing to buy sulfur.
213|Charles says the amount is still nowhere near enough.
232|Charles says it is still insufficient.
243|Charles judges the amount sufficient.
247|Gerhard asks what happens next.
251|They next need timber to make charcoal.
254|Hodram repeats the need for timber.
258|Gerhard says this town does not sell timber, so they must obtain it elsewhere.''',
298:'''11|Hodram wishes Charles were with them.
33|Hodram recalls needing to buy timber.
128|Charles says the amount is still nowhere near enough.
147|Charles says it is still insufficient.
158|Charles judges the amount sufficient.
161|Charles introduces the final requirement but pauses.
165|Hodram asks with exasperation whether there is still more.
169|The essential missing ingredient is saltpeter.
172|Hodram questions the mention of saltpeter.
176|Gerhard believes it is sold in some town on the Indian Ocean.
179|Hodram notes how far away that is.''',
299:'''11|Hodram wishes Charles were with them.
33|Hodram recalls needing to buy saltpeter.
229|Charles says the amount is still nowhere near enough.
247|Charles says it is still insufficient.
258|Charles judges the amount sufficient.
265|Charles announces completion.
269|Charles will set the explosive and tells the others to evacuate to town.
278|Charles announces the start and counts exactly three, two, one, zero.''',
300:'''40|Hodram says even local people apparently avoid this area.
43|Gerhard suspects something is here and urges proceeding with great caution.
46|A retainer alarmedly directs the admiral’s attention to something.
50|Hodram identifies a giant snake with surprise.
54|Gerhard asks what to do, judging it a difficult opponent.
68|Hodram chooses to fight.
72|Gerhard acknowledges and orders a coordinated attack.
75|The retainer acknowledges colloquially.
94|Hodram confirms the creature has been defeated.
98|Gerhard agrees while recovering his breath.
110|Optional Charles says it was formidable and he is glad they had gunpowder.
119|Some sailors appear injured.
124|Hodram judges fighting here unwise.
128|Gerhard acknowledges and orders everyone to withdraw without falling behind.
132|The retainer acknowledges.
137|Gerhard checks that everyone is present.
141|The retainer confirms everyone is present.
148|Hodram gives a sudden startled reaction.
152|Gerhard respectfully asks FI what happened.
155|Hodram believes he is stuck in a bog.
159|Gerhard reacts in alarm.
170|Gerhard promises immediate help.
174|Gerhard strains, finds his strength alone insufficient and calls the others to help.
178|The retainer acknowledges the request.
182|After exertion Gerhard asks whether FI is safe.
186|Hodram thanks Gerhard for saving him.
194|In an alternative rescue, Gerhard promises help and exerts himself loudly.
197|Panting, Gerhard asks whether FI is all right.
201|Hodram apologetically thanks him and had not expected a bog here.
208|The sailors appear fatigued.''',
}

STYLE={
(290,24):['Polite warning: without a map they will get lost.','Plain polite warning: without a map they will get lost.','Informal warning: without a map they will get lost.','Same physical warning as slot0.','Rough warning: without a map they will get lost.','Older-sounding warning: without a map they will get lost.','Drawn-out protest: without a map they will get lost.','Formal older-sounding warning: without a map they will get lost.'],
(290,328):['Dense forest; proceed carefully.','Dense forest; proceed carefully, restrained register.','It is dark and feels unpleasant.','Dense forest; hope they do not get lost.','Rough voice: this forest feels unpleasant.','Older voice: proceed cautiously and carefully.','Hope they find something good.','Dense forest; hope nothing appears.'],
(290,670):['Stammered warning to the admiral: behind him.','Urgent polite instruction not to move; something behind him.','Stammered informal warning: behind him.','A small cry, then stammered warning about something behind.','Same physical warning as slot0.','Older emphatic warning: behind the admiral.','Frightened cry and warning: behind him.','Same physical warning as slot0.'],
(290,970):['Surprise and relief: it ran away.','Same physical announcement as slot0.','The bear ran away, informal.','Surprised feminine-register announcement that it ran off.','Same physical announcement as slot0.','Older voice: it ran away.','Excited celebration: it went away.','Same physical announcement as slot0.'],
(290,1166):['Stammered warning: the bear shows no sign of leaving.','Restrained warning: the bear shows no sign of leaving.','Frustrated informal warning: the bear is not moving at all.','Stammered feminine-register warning: it will not move.','Rough emphatic warning: the damned bear will not flee.','Older worried observation: the bear shows no sign of leaving.','Whining fear: the bear does not seem inclined to leave.','Formal worried observation: no movement can be sensed from the bear.'],
(290,1632):['Sigh of relief: it finally gave up.','Same physical relieved observation as slot0.','Same physical relieved observation as slot0.','Sigh of relief, feminine register: it finally gave up.','Rough sigh of relief: it finally gave up.','A snore-like sound rather than a spoken relief report.','Same physical relieved observation as slot0.','Same physical relieved observation as slot0.'],
(290,1924):['They tried to frighten it, but it will not run.','Amazed that threatening it did not make it flee.','Informal frustrated question: what is with it; it will not flee despite threats.','Feminine register calls it brazen; threats do not scare it off.','Rough voice calls this a gutsy bear; it will not flee.','Older incredulous complaint: threats do nothing; what is happening.','Drawn-out confused complaint: they scared it but it will not run.','Formal voice calls it brazen for not fleeing despite threats.'],
(290,2398):['Danger; an expedition member was attacked; they must escape for their own safety.','Danger; a member was attacked; flee to avoid personal danger.','Informal alarm: a member was attacked, give up and flee.','Feminine-register alarm: a member is being attacked, they should flee.','Rough alarm: perhaps several people were injured; retreat is wiser.','Older urgent warning: the admiral should flee.','Drawn-out frightened pleas that it is dangerous and they should run.','Formal alarm: this is bad; the admiral should flee.'],
(290,3040):['They somehow escaped, polite relief.','Breathless pause and confirmation that they escaped.','Panting informal relief: they seem to have survived.','Feminine-register relief: they seem safe.','Rough breathless question: did they escape.','Same physical relieved question as slot4.','Panting frightened relief, recalling how scary it was.','Older formal voice: out of breath, everyone seems safe, thank goodness.'],
(290,3300):['They left the forest and reached the ruins.','They left the forest; this must be the ruins.','At last out of the forest; excited realization that these are the ruins.','At last out of the forest; reflective identification of the ruins, feminine register.','Rough excited announcement: out of the forest and the ruins are there.','Older relieved observation: out of the forest; those may be the ruins.','Excited relief, then uncertainty whether the strange stones are the ruins.','Older formal announcement: out of the forest; these must be the ruins.'],
(291,24):['Polite warning: wandering aimlessly in the jungle is dangerous.','Restrained warning: aimless travel in such jungle is dangerous.','Informal emphatic warning that wandering such jungle is too dangerous.','Feminine register: without a map they will get lost in this formidable jungle.','Rough voice calls aimless travel in such jungle reckless with one’s life.','Older warning that aimless jungle travel is dangerous.','Drawn-out protest against entering such jungle without a map.','Formal older warning that aimless jungle travel is dangerous.'],
(291,824):['Something is here; a bad feeling.','Something is here; an ominous feeling, restrained/formal.','Informal uneasy observation that something is here.','Feminine-register uneasy question whether something is here.','Rough certainty something is here; a bad feeling.','Older voice senses something and a bad omen.','Simple uneasy question and first-person protest about the feeling.','Same physical uneasy observation as slot0.'],
(291,1246):['Do not shoot in such cramped quarters: risk of hitting allies is too high.','Restrained objection: shooting here may hit allies.','Informal objection: such narrow space risks shooting friends.','Feminine-register objection: firing here could hit allies.','Rough emphatic objection: firing here will hit allies.','Older objection: impossible to shoot here without hitting allies.','Drawn-out plea to the admiral: narrow quarters risk hitting companions.','Formal emphatic objection: far too much risk of hitting allies here.'],
(291,1890):['Panting report that they somehow defeated it.','Restrained report that they somehow defeated it.','Panting informal uncertainty whether they defeated it.','Panting feminine-register impression that they defeated it.','Rough triumphant announcement that it is down.','Older wheezing announcement that they somehow defeated it.','Excited relief: finally defeated it; the tiger was strong.','Older formal panting report that they somehow defeated it.'],
(291,2194):['It apparently was not hungry; it is not pursuing them.','Restrained observation: not hungry, no pursuit.','Informal deduction of no hunger from its failure to chase them.','Feminine-register conclusion of no hunger and relief at not being chased.','Rough deduction of no hunger from no pursuit; relieved escape.','Older deduction: the tiger did not pursue them, so it was not hungry.','Simple observation: that tiger does not seem hungry and is not chasing.','Same semantic observation as slot0 in the source’s restrained formulation.'],
(294,28):['Polite refusal: without a map they cannot proceed.','Restrained refusal: without a map they cannot proceed.','Informal refusal: cannot go farther without a map.','Feminine-register refusal: proceeding without a map is impossible.','Rough complaint: cannot proceed without a map.','Older refusal: cannot proceed without a map.','Drawn-out plea that they need a map.','Formal older refusal: cannot go farther without a map.'],
(300,24):['Polite warning: without a map they will get lost.','Restrained warning: without a map they will get lost.','Informal complaint about proceeding without a map.','Feminine-register warning: they will get lost without a map.','Rough warning: they will get lost without a map.','Older warning: they will get lost without a map.','Drawn-out protest: they cannot proceed without a map.','Formal older warning: they will get lost without a map.'],
(300,1610):['The companion alerts the admiral to something ahead, without naming it.','An urgent polite direction to look ahead.','A stammered warning to look over there.','Same physical warning as slot2.','Rough direct call to the admiral to look.','Older direct call to the admiral to look.','Drawn-out excited identification of something over there, unnamed.','An older-sounding awed exclamation without naming the discovery.'],
}

CAPTIONS={(290,876):['Fight bravely.','Play dead.','Choose another approach.'],(290,1876):['Threaten/frighten it into leaving.','Run away regardless.'],(291,1114):['Order an attack.','Order escape.'],(294,820):['Agree to examine the surroundings as a precaution.','Decline the investigation.'],(300,560):['Choose to fight the giant snake.','Choose to flee.']}


def main():
    assert not any(p.exists() for p in (SCOPE,ORDINARY,OUT))
    packet,styles,menus,names,ledger=map(load,(PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',ROOT/'clean_name_fields.json',Path('translations/editorial_review_current_v1.json')))
    ordinary=[r for g in packet['groups'] for r in g['records']]
    originals=ordinary+styles['records']+menus['records']
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert ledger['records_editorially_completed']==len(credited)==17749
    assert (len(ordinary),len(styles['records']),len(menus['records']),len(originals))==(242,131,11,384)
    assert len({(r['file_path'],r['id']) for r in originals})==384
    assert not any((r['file_path'],r['id']) in credited for r in originals)
    assert styles['object_count']==18 and styles['style_alias_slots']==144 and menus['object_count']==5
    assert [g['block'] for g in packet['groups']]==list(range(281,301))
    assert all(r['source_decode_error'] is None for r in ordinary)
    evidence={str(p):digest(p) for p in (PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',ROOT/'clean_name_fields.json',Path(__file__))}
    save(SCOPE,dict(source_packet=str(PACKET),source_packet_sha256=digest(PACKET),ordinary_speeches=242,
        physical_personality_alternatives=131,physical_style_objects=18,personality_alias_slots=144,
        typed_caption_records=11,typed_choice_objects=5,total_editorial_objects=384,reviewed_block_numbers=list(range(281,301)),
        control_only_blocks=[],excluded_credited_records=[],all_completed_exclusion_keys_checked=17749,
        source_key_overlap_with_completed_credit=0,no_current_English_dialogue_consulted_for_eligible_records=True,
        source_meanings_pending=True,all_five_review_gates_pending=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    seal(PACKET,ORDINARY,MEANINGS,CONTEXT,Path(__file__))
    rows=[]
    for original in load(ORDINARY)['records']:
        row=deepcopy(original);row.update(exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    for original in styles['records']:
        row=deepcopy(original);indices=row['source_style_indices'];key=(row['block'],row['source_command_offset'])
        assert len(STYLE[key])==8
        row.update(source_meaning=STYLE[key][indices[0]],exchange_context=CONTEXT[row['block']],
            personality_voice_notes=[dict(source_index=i,register=STYLE[key][i]) for i in indices],source_only_not_final_English=True)
        rows.append(row)
    for original in menus['records']:
        row=deepcopy(original);key=(row['block'],row['source_command_offset'])
        row.update(source_meaning=CAPTIONS[key][row['source_index']],exchange_context=CONTEXT[row['block']],source_only_not_final_English=True);rows.append(row)
    assert len(rows)==384
    save(OUT,dict(records=rows,records_count=384,ordinary_speeches=242,physical_personality_alternatives=131,typed_captions=11,
        complete_exchange_contexts=CONTEXT,source_meanings=384,remaining_meanings=0,English_drafts=0,current_story_English_compared=0,
        all_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        no_current_English_dialogue_consulted_for_eligible_records=True,source_first_not_new_editorial_completion_credit=True,
        source_names_are_clean_metadata_not_native_consumer_orfinal_localization_approval=True,
        item_stat_andproper_name_final_forms_require_scoped_approved_term_binding=True,
        all_five_review_gates_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False,evidence=evidence))
    print('Sealed 384 source meanings in 20 complete exchanges; no credited overlap and no eligible current-English comparison.')


if __name__=='__main__':main()
