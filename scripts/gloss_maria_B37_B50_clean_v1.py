"""Seal individual clean-source meanings for286 objects before current-English intake."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B37_B50_clean_20261109')
OUT = ROOT/'all286_clean_meanings_v1.json'
CONTEXT = {
37:'After surviving Kuhn, Lil apologizes to the companions she endangered. Maria places the blame on Kuhn. Hodram leaves for the North Sea and redirects thanks to FI; Lil decides she must return and improve after discovering her limitations. Camille accompanies her. Maria and Xien will deal with Kuhn. Preserve gratitude, regret and growth without making Lil a child or inventing a relationship.',
38:'An Uddin Company representative addresses FA and proposes a joint front. He invokes the long-established Muslim control of these waters and a current struggle against Europeans. Maria challenges whether he means expulsion, and he clarifies a noninterference-for-limited-help bargain. Acceptance and refusal are separate menu branches. Preserve religious identity, territorial conditions and limited assistance as his claims, not an unconditional alliance or external history assertion.',
39:'Defeated Nagalpur mourns his money, company and fleet. Maria dismisses his remaining threat and challenges the notion that money solves everything; Xien agrees and urges calm. An optional Yifa taunt triggers his recognition. Nagalpur remains obsessed with avoiding poverty. Preserve the comedy and his obsession without inventing death, surrender terms or his recovery.',
40:'Maria and Xien discuss Madagascar as a proposed trade-network hub linking several East African routes. Maria sees an analogy with a large island off Ming and proposes building a trading port. Xien questions government approval; Maria cynically invokes officials’ love of bribes, and Richard suggests proceeding in Hangzhou. The plan is prospective, with substantial investment expected; no Taiwan/Tamsui name or claim that the island is uninhabited is spoken yet.',
41:'Maria has an initial town plan; Richard volunteers for government negotiations and then construction management. Conditional companions question his ability. He argues Maria cannot remain in Ming, cites an unverified rumor of suspicious government action, promises to investigate and keep the government in check, and asks for500000 gold to be brought to Hangzhou. Preserve the rumor and future funding, not an enacted payment or proven conspiracy.',
42:'Richard reports that negotiations succeeded and construction of Tamsui has already begun. Maria has500000 gold ready. He then complains that workers brought from England dislike the food and requests five cargo holds of wine to raise morale. Xien suspects an excuse for Richard’s own drinking; Maria agrees to deliver the wine. Preserve source amounts, storage wording and the suspicion rather than confirming Richard’s motive.',
43:'Maria has brought wine and authorizes distribution. Richard reports the completed trading post and FO’s exclusive trading rights. Maria marks an initial success; Xien proposes reinvesting trade profits, and Maria asks Richard to continue overseeing construction. Do not invent full completion of the city, profits already earned or unrestricted rights elsewhere.',
44:'An alternative unfinished-construction visit: facilities are still incomplete, Xien notes slow progress, and Richard again invokes missing wine. Maria reluctantly hopes supplying it will improve work; Richard repeats five holds. Keep this separate from the successful wine-delivery branch and do not assert the wine really is the only cause of delay.',
45:'Maria arrives in Africa, recalls Zheng He and intervenes against Grau’s violent treatment of workers. He claims ownership and invokes the Espinosa Company’s fearsome reputation. Maria rejects ownership of people and condemns exploitative outsiders, using pest/parasite metaphors and a threat to shut the company down within months. She refuses intimidation. Richard later condemns the company with her. Preserve coercion, threats and sarcasm without inventing a government commission, execution or successful liberation.',
46:'After Espinosa’s defeat, a confident young man’s unseen voice gives way to Clifford’s named speech. He welcomes opportunities for England and treats colonial replacement as inevitable. Maria rejects both his entitlement and a successor to Espinosa, threatening danger if her subordinates find him. He withdraws for today but insists someone will take Africa. She conceals this confrontation from Richard with a directions excuse. Preserve the threat, private exchange and dismissive flattery; no ally or office is granted.',
47:'Locals seize defeated Espinosa and accuse him of dispossession, a staged-accident murder and coerced hunger-level labor. They reject his blame of subordinates; Maria lets them take charge of his punishment without specifying execution. A shopkeeper gives an object formerly possessed by Espinosa while referring separately to his search for Africa’s Proof and the people’s hope he would not obtain it. They wish Maria to bring peace and prosperity. Crowd gratitude moves her; optional companions remark on her happiness. Preserve actual father/household ties, distinct alternate speakers and private thoughts; do not identify the gift as the Proof.',
48:'Clau and Rafael discuss the feared FA without recognizing Maria, then her appearance exposes the irony and draws their alarm/flattery. She distinguishes exploiters from honest trade and presses Rafael on Portuguese imperial ambitions. He acknowledges past wrongs and articulates mutual benefit and prosperity through shipping. She responds with respect and asks for Mediterranean intelligence. Regional reports are conditional alternatives, not one contradictory chronology. Preserve Clau/Rafi familiarity, Rafael’s modesty, Maria’s skepticism and the offers of future mutual aid.',
49:'Maldonado is identified by alternative companions, then argues against adding Maria to his enemies. Separate branches describe Escante’s betrayal after Clifford’s removal, betrayal when Clifford proves strong, or pressure from Escante, Clifford and a Swede. Maria condemns piracy; Maldonado invokes dispossessed New World inhabitants and people of mixed ancestry, admits mutual exploitation and profit motives, and proposes fighting Escante together. The tentative acceptance and refusal branches differ. Preserve political nuance and Maria’s conditional trust without making him a selfless liberator or adding ethnic parentage.',
50:'Xien reports Richard’s defection. An FE Hangzhou transition precedes a hidden-speaker monologue contextually linked to Richard: England’s domination is imminent, Maria could have served as a useful subordinate had she confined herself to suppressing wokou, her absence enables a long-prepared plan, and the speaker expects appointment as East Asia governor. The speaker asks Clifford to await good news. An FE notice reports most mainland Ming trading share transferred to Clifford. Preserve prospective appointment and source uncertainty; no static nameplate, completed governorship, exact percentage or historical truth claim is inferred.',
}

MEANINGS = {
37:'''4|Lil is relieved to have survived and bitterly invokes Kuhn.
7|Camille urgently asks whether Lil is all right.
11|Lil says everyone suffered because of her and she cannot find words to apologize.
15|Maria says it is over now and Kuhn is the one at fault.
18|Hodram says they somehow escaped disaster, will return to the North Sea and takes his leave.
22|Camille thanks Hodram.
26|Hodram says the thanks should go to FI.
29|Maria asks what Lil and Camille will do.
33|Lil will return to the North Sea after realizing she cannot compete worldwide as she is.
37|Camille says he will go with Lil.
40|Lil thanks Camille.
44|Maria asks them to leave the rest to her side and says they will defeat Kuhn.
47|Xien refuses to let someone like Kuhn get away with this.
51|Lil takes leave and apologizes for all the trouble she caused.''',
38:'''5|The representative asks if this is FA, who has recently caused a stir in the Indian Ocean.
8|Maria asks who he is.
12|He says he is with the Uddin Company.
16|He says Muslims have long managed these waters and asks Maria not to interfere here.
19|Maria asks whether he means that her people must withdraw from the Indian Ocean.
22|He rejects her hasty inference, says they are busy expelling Europeans and have no time to face her now.
25|He therefore proposes a joint front.
29|He offers some help against Europeans if Maria leaves their territory alone and asks her view.
34|The first menu caption quietly accepts.
36|The second menu caption refuses agreement.
44|On acceptance he laughs approvingly, expects a good partnership and takes his leave.
52|On refusal he says they must defend their own doorstep on Arab pride.''',
39:'''4|Nagalpur cannot believe his defeat and mourns his money, company and fleet.
8|Xien spots Nagalpur and wonders why he is still around here.
11|Maria says he is no longer their enemy or threat because he can do nothing without money.
15|Xien agrees.
27|Yifa mocks him as far less impressive than he seemed.
34|Nagalpur recognizes the speaker and expresses angry resentment.
37|Maria calls the idea of solving everything with money his fantasy and says he has learned it painfully.
41|Nagalpur growls in frustration.
45|Xien says FI is right and tells him to cool his head.
48|Nagalpur cries that he hates poverty and begs anyone for money.
52|Xien concludes that saying anything to him is useless.''',
40:'''4|Maria is impressed to find a substantial town even on an island like this.
8|Xien expects it to develop further as a trade relay point.
12|Maria asks him to explain.
16|He says East African towns including Sofala form a single trade route along a simple coastline.
19|Using Madagascar as a relay allows multiple routes to carry goods between Cape Town and Mogadishu.
22|Maria concludes that an island trading port would diversify East African routes and develop this town too.
26|The geography reminds her of a large island a little way off Ming.
30|Xien doubts that island has a port where they can trade.
34|Maria proposes building one if none exists and seeks agreement.
37|Xien calls that a difficult proposal and says the government will not tolerate unauthorized town construction.
41|Maria asks whether guaranteed profit would change that, cynically saying bribe-loving officials would not oppose it.
45|Richard finds the idea interesting and urges returning to Hangzhou to proceed.
49|Maria imagines a second Madagascar there, requiring considerable investment but becoming a large port eventually.''',
41:'''4|Xien raises the subject of the new town with FI.
7|Maria says the initial plan is nearly ready and government negotiations are the remaining issue.
10|Richard offers to handle the government negotiations.
13|Maria agrees because he suits such work.
17|Richard is pleased to be trusted and asks for one more favor.
20|Maria asks what else he wants.
24|Richard asks to be entrusted with building the town as well.
27|Xien asks whether Richard himself would direct construction.
39|Jam doubts whether Richard can do such work.
45|Richard argues the commander herself cannot stay in Ming solely to devote herself to construction.
49|Maria agrees that she cannot stay because much else remains for her to do.
53|Richard reports rumors of suspicious Ming-government moves in response to their activities.
57|Maria reacts with alarm and asks what he said.
61|Richard promises to discover the truth and keep the government in check while Maria continues sailing.
64|Maria understands and entrusts it to him.
67|Richard says money will be needed after negotiations and asks for about500000 gold.
70|Maria repeats500000 and agrees to prepare it.
73|Richard will begin negotiations and asks that the funds be brought to Hangzhou when ready.''',
42:'''4|Richard warmly addresses FI as admiral and says he has been waiting.
7|Maria asks whether the negotiations progressed well.
11|Richard reports success and says Tamsui’s construction has already begun as FI envisioned.
14|Xien is pleased it worked.
18|Maria approves and says she has500000 gold ready.
23|Richard says construction preparations are now complete and urges a visit to Tamsui.
26|Maria agrees to visit.
30|Richard says construction needs many people; he brought many workers from England, but there is a problem.
33|The workers seem dissatisfied with the local food.
36|Maria asks what follows from that.
40|Richard suggests Western alcohol such as wine would best raise their motivation.
44|Maria hopes that will solve it and asks how much is needed.
47|Richard asks for about five cargo holds’ worth.
51|Xien suspects Richard is using the story as an excuse for his own desire to drink.
55|Maria reluctantly confirms delivery of five holds of wine to Tamsui.
59|Richard requests speed because morale is at stake and says he will go ahead to the town.''',
43:'''4|Richard says he has been waiting for FI.
7|Maria says wine is in storage and tells him to distribute it freely.
11|Richard thanks her, agrees and adds that the trading post is complete.
15|He says FO holds exclusive trading rights in this town, so Maria may use the post without concern.
18|Maria calls being able to trade progress and a first step.
22|Xien says developing the town is now their aim and trade profits should be invested here.
26|Maria wants a much bigger town and asks Richard to continue directing the work.
30|Richard respectfully accepts.''',
44:'''4|Richard welcomes Admiral FA but says the facilities remain unfinished and nothing is ready.
7|Xien says the work is progressing more slowly than he expected.
10|Richard again attributes the problem to having no wine.
14|Maria says this will get them nowhere and thinks alcohol must be provided to improve work efficiency.
18|Richard agrees and requests five holds of wine as soon as possible.''',
45:'''4|Maria realizes she has finally reached Africa, which Zheng He also visited.
8|Grau harshly orders someone to walk faster.
12|Maria notices something with curiosity.
17|Grau orders the person not to stop and threatens killing.
21|Maria privately wonders if the people being driven are local residents and thinks the treatment cruel.
25|Maria tells the man to stop the violence.
29|He challenges her identity, claims the people are his property and rejects her interference.
33|Maria says human beings are not livestock and cannot be someone’s property.
36|He says they work on his plantation and asks what is wrong with using them as he wishes.
39|He calls her an outsider and rejects her lecturing.
42|Maria calls his reasoning self-serving and points out Westerners are outsiders in Africa too.
46|He angrily says she apparently does not know who they are.
49|Maria says she does not want to know.
53|He invokes the Espinosa Company’s terrifying reputation and orders her away if she values her life.
57|Maria dismisses the attempted threat as less impressive than a stray dog’s distant howling.
60|He angrily complains she never stops talking back.
63|Maria uses pest-control imagery to describe eliminating parasites like them infesting countries.
67|He repeats the parasite and pest-control terms in anger and says she should have announced she wanted to die.
71|Maria tells him to warn his boss to find new work because their business will end within a few months.
74|He reacts in disbelief and outrage.
78|Maria clarifies that she will close down this unscrupulous company.
82|He laughs and wonders whether her unusual boldness is courage or mere stupidity.
85|He threatens to seize her and force her to kneel before Espinosa.
89|Maria pities him and says more intelligence would let him live longer.
92|Maria says he will regret his words, promises no mercy next meeting and warns him to be ready.
96|He splutters in anger.
108|Richard says human decency forbids overlooking the Espinosa Company’s wrongdoing.
111|Maria agrees that they cannot let it go unpunished.''',
46:'''4|A dashing young man’s voice asks whether these are the people who defeated Espinosa.
9|Xien reacts in surprise.
13|Clifford is grateful that England can now expand into Africa without concern.
17|He says Espinosa apparently made handsome profits here and calls their luck excellent.
21|Maria says there is a misunderstanding because she never asked for a replacement for Espinosa.
25|Clifford treats this as obvious and dismisses her objection as belated.
28|He says Western great powers each take charge outside Europe; when one fails, another takes over.
31|Maria asks whether he means the world belongs to those powers and calls that self-serving.
35|She condemns Europeans shameless enough to say this openly.
39|She says they will not tolerate such people, cannot guarantee his life if her subordinates find him and orders him away.
42|He calls the beautiful woman frightening and withdraws for today.
45|He will not give up and says someone else will come even if he withdraws.
48|He argues that if the region will be taken anyway, it might as well be him.
51|Maria falls silent.
62|Richard asks who Maria was speaking to and whether there was trouble.
65|Maria denies trouble and says someone only asked directions that she did not know.
68|Richard hesitantly accepts that explanation.''',
47:'''4|Espinosa squeals and demands to know what the people are doing.
15|Richard notices the disturbance.
24|The port worker orders the captive to come.
28|Maria recognizes Espinosa with surprise.
32|The shopkeeper respectfully thanks FA for defeating the scoundrel.
35|Espinosa threatens consequences for this treatment.
38|The port worker tells him to shut up.
42|Espinosa cries out in pain.
46|The worker accuses him of doing as he pleased for far too long.
49|Espinosa feigns ignorance and asks what he means.
53|The worker accuses him of cheating the worker’s father out of house and farmland, after which the father and household disappeared.
56|The shopkeeper says Espinosa killed his friend in a staged accident when the friend tried reporting his wrongdoing back home.
60|The innkeeper says many villagers from her hometown were taken away and forced to work with barely enough food.
64|Espinosa denies knowing and blames foolish subordinates acting on their own.
68|The worker rages at that excuse.
80|Julian expresses disgust and calls the behavior cowardly.
93|Richard condemns Espinosa as inhuman.
102|The shopkeeper condemns him and asks FA to let the locals deal with him.
105|Maria agrees and leaves it to them.
109|The worker orders Espinosa along and promises to make him pay thoroughly for his crimes.
112|Espinosa begs to be saved.
116|Maria is silent.
121|The shopkeeper addresses FA respectfully.
125|Maria responds with curiosity.
129|The shopkeeper asks her to accept something.
136|Maria asks what it is.
140|The shopkeeper says the object was Espinosa’s, who also sought Africa’s Proof; they prayed the Proof would not fall into his hands.
143|He says Maria deserves to be the region’s conqueror and hopes she finds the treasure soon and brings peace and prosperity.
147|Maria thanks him and promises to work to meet their hopes.
157|Xien points out the townspeople gathered and waving to the admiral.
163|Yukihisa politely gives the alternative observation of the waving crowd.
170|Maria contrasts this reception with her time in Ming.
179|Xien says the people understood her desire to fight for them and urges her to respond.
185|Ian gives a polite alternative reassurance that her feelings reached the people and she should respond.
192|Maria nervously tries waving, saying she has never done it before.
201|Xien privately thinks he has never seen FI so happy.
207|Jam privately thinks he has never seen the admiral so happy, then says aloud he is glad he followed her.
211|Maria asks why he suddenly says that and finds it odd.''',
48:'''5|Clau tells Rafael to be careful.
8|Rafael agrees but marvels that such a frightening woman pirate exists in the wide world.
13|Clau says frightening is insufficient to describe FA and begins explaining.
17|Maria notices the conversation with curiosity.
21|Clau alleges she weakens enemies through schemes and diplomacy, then massacres them when off guard; meddling means certain danger.
25|Maria stifles a laugh and chuckles.
29|Rafael notices the reaction.
34|Clau challenges the nearby woman and asks what is funny.
37|Maria apologizes and asks to hear more, specifically what the pirate looks like.
41|Clau admits he has not seen her, but guesses she looks like an ogre.
45|He reports short black hair, black clothes and a scarlet outer jacket.
49|Rafael reacts with surprise.
54|Clau adds a crimson rose at her chest and suddenly suspects her identity.
57|Maria introduces herself as FI FA and offers a greeting.
60|Rafael hesitantly asks whether she is FA.
71|Richard clears his throat and confirms it.
79|Clau yelps, admits his fear was right, hurriedly corrects his apology to politeness and begs for his life.
83|Rafael had not expected such beauty and tells Clau the rumors must be fabrications.
88|Clau hastily agrees and flatters her beauty while denying such a lady could be a terrifying pirate.
98|Richard comments dismissively on Clau’s quick change of tune.
108|Maria rejects flattery, confirms she is FA and notes she is widely feared.
111|She says her targets dominate people by force and steal their wealth, then asks whether the men aid such people.
114|Clau vehemently denies it and says they earn honestly through legitimate trade.
118|Rafael begins describing Portugal, their homeland, which once held sway across the world.
129|Richard responds with curiosity.
135|Maria responds with curiosity in an alternative branch.
142|Rafael says Spain has taken Portugal’s sovereignty, but they dream of reviving its sailors’ vigor.
146|Maria asks if he wants Portugal to replace Spain as ruler of the world.
150|Rafael says Spain’s conquests in the New World differ from their aim.
155|Maria presses whether Spain is wrong and Portugal right.
158|Rafael says he is not claiming Portugal’s past methods were right.
162|He wants fair movement of goods between regions so both sellers and buyers benefit greatly.
166|He hopes shipping can help people live more prosperous lives and regards that as their role.
171|Clau calls him Rafi and marvels that he has thought so deeply.
174|Maria finds his ambition admirable.
178|Rafael fears sounding presumptuous and apologizes for grand talk.
182|Maria clarifies that she meant no criticism and wishes all sailors thought like them.
194|She ends the unproductive wishing and asks whether they know recent Mediterranean affairs.
197|Rafael considers recent events.
210|One report says Spain’s Valdes army dominates, while Ottoman naval power was nearly destroyed after defeat by Italian rulers at Lepanto.
216|An alternative report says Spain and Ottoman Turkey control most regional interests, with admirals Valdes and Pasha skirmishing.
227|He says the Hayreddin pirate family had controlled the Strait of Gibraltar, entrance to the Mediterranean.
239|One outcome says its main strength withdrew east after the Turkish alliance ended and is now no longer seen here.
245|A shorter alternative says the main strength appears to have withdrawn east after that alliance ended.
254|Maria thanks him for the overview and asks for future cooperation, offering help in return when needed.
257|Clau eagerly agrees, especially against the Spanish, and seeks Rafael’s assent.
261|Rafael politely offers their help if they will suffice and welcomes cooperation.''',
49:'''5|Maldonado grumbles that another troublesome person has arrived.
8|Maria reacts with curiosity.
19|Richard identifies Maldonado.
25|Xien gives an alternative identification of Maldonado.
32|Maria repeats the name thoughtfully.
43|Richard identifies him as leader of pirates ravaging the Caribbean.
48|Xien gives an alternative identification of the Caribbean pirate chief.
63|Aziza reacts to the mention of pirates.
70|Maria asks what a pirate wants with her.
74|Maldonado asks her to calm down, says he does not intend to fight them and is already in desperate straits.
85|One version says Escante proposed attacking England’s Clifford together but betrayed Maldonado once that enemy was gone.
96|An alternative says Escante betrayed him as soon as the English enemy proved formidable.
101|Another situation has Escante in Mexico and England’s Clifford attacking from both sides, with a Swede interfering too.
110|He says making more enemies would only tighten the noose on himself.
113|Maria asks what he will do if she wants a fight even though he does not.
116|Maldonado reacts in surprise and anger.
120|Maria asks if he expects her people to leave pirates free to obstruct shipping and torment others.
123|He says he does not recall doing anything to anger her.
126|Maria questions that denial.
130|He says Escante’s gold bound for the homeland was seized by force from New World inhabitants to fund weapons purchases.
133|He argues Maria has no grounds to complain merely because he steals that gold from Escante.
136|He says many Caribbean pirates are New World inhabitants or people of mixed ancestry; village treasure is theirs to reclaim.
139|Maria calls it specious reasoning and says he exploits those local people’s feelings.
143|He freely admits using them, saying they also use his organization to take revenge and make a living; it is mutual.
146|Maria is silent.
150|He dismisses her lack of understanding and proposes joining forces against Escante’s tyranny.
153|He accuses Escante of forceful domination and taking all the wealth people accumulated over years.
157|He says that when nothing remains to take, Escante makes them work on his plantations and asks if this can be ignored.
160|Maria finds a Caribbean pirate’s moral condemnation of others hard to believe sincere.
164|He laughs and admits wanting profit, but qualifies it further.
167|He prefers taking from a villain and wants to see both his subordinates’ joy and Escante’s bitter frustration.
170|Maria remains silent.
174|He invokes the enemy-of-my-enemy principle and asks to unite to defeat Escante.
179|The first menu caption proposes waiting to see how things develop rather than immediate full trust.
181|The refusal caption sternly tells him to stop or enough is enough.
188|Maria tentatively agrees, reserving judgment on whether she should fight him until seeing what happens.
192|He calls the deal settled and promises to handle the region and keep Escante checked.
195|Maria calls it a convenient agreement, temporarily leaves the Caribbean to him and threatens immediate defeat if he betrays the people.
198|He laughs that she may try if she can, but says betrayal is not a concern.
201|Maria doubts his assurance.
209|On refusal Maria ends his excuses, saying she did not come to hear them.
213|He concludes an outsider like her cannot understand local circumstances.
217|He accepts her enmity but warns that Caribbean pirates will not let her have her way easily.''',
50:'''4|Xien urgently calls FI.
8|Maria asks what is wrong, addressing Xien.
12|Xien reports that Richard defected to Clifford’s army.
16|Maria reacts with shock to Richard’s name.
24|An FE transition names Hangzhou.
29|An unseen speaker gives a short amused huff.
33|The speaker’s chuckling builds into loud laughter.
36|He declares that the moment for the kingdom of England to possess the world’s seas has arrived.
40|He addresses FI and says she went too far.
43|He says that had she been content policing wokou in the distant East, England might eventually have employed her as an able subordinate.
46|He says she has truly angered the English.
49|Her absence from the East makes this an opportunity to complete their long-prepared plan.
53|He says she will have nowhere to return because he expects to be appointed East Asia governor.
57|He says he enjoyed their time together and addresses her as the beautiful admiral.
60|He asks Clifford to await good news.
76|An FE notice reports that most mainland Ming market/trading share has fallen to Clifford’s forces.''',
}


def main():
    assert not OUT.exists()
    packet_path = ROOT/'clean_source_packet.json';packet = load(packet_path)
    assert packet['current_English_unconsulted'] and packet['all286_positions_uncredited']
    assert set(CONTEXT) == set(MEANINGS) == set(packet['blocks'])
    rows = []
    for group in packet['groups']:
        number = group['block'];parsed = [line.split('|',1) for line in MEANINGS[number].strip().splitlines()]
        meaning = {int(k):v for k,v in parsed}
        assert len(meaning) == len(parsed) == len(group['records'])
        assert set(meaning) == {r['source_record_index'] for r in group['records']}
        for original in group['records']:
            row = deepcopy(original)
            row.update(source_meaning=meaning[row['source_record_index']],whole_exchange_context=CONTEXT[number],
                source_meaning_pending=False,source_first_independent_meaning_saved=True,
                source_read_with_all_previous_andfollowing_speeches_in_block=True,
                source_meaning_not_final_context_name_orformat_approval=True)
            rows.append(row)
    assert len(rows) == 286 and all(not any(r['review'].values()) for r in rows)
    save(OUT,dict(records=rows,records_count=286,complete_exchanges=14,source_packet=str(packet_path),
        source_packet_sha256=digest(packet_path),all_clean_source_meanings_saved_before_current_conversation_English=True,
        current_English_unconsulted=True,independent_drafts_andcurrent_comparisons_pending=True,
        all_five_gates_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [packet_path,Path(__file__)]}))
    print('Sealed286 individual source meanings/14 whole exchanges; current conversation English unconsulted;zero credit.')


if __name__ == '__main__':main()
