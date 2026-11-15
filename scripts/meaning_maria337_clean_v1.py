"""Seal337 clean-source meanings before consulting current story English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B125_B136_clean_20261109')
CONTEXT={
125:"A European governor greets the admiral using FA and reports that Escante intended a coup for independence from Spain. The fleet prevented it. He then relays hearsay that an unidentified person carried the key to Escante's treasure to the New World's west coast. Maria suspects the Proof map; Xien anticipates the difficulty. The unknown thief, treasure key and map are not conclusively identified, and the report is not an account of a successful independence movement.",
126:"Xien notices that the ceremonial knife and sun-emblem sheath fit. Inserting the knife causes a blinding light; neither knows how. A map appears on the blade, which Maria identifies as the New World Proof map. Preserve the blade/sheath distinction, causal sequence, surprise and uncertainty about the mechanism. The map is obtained, not the Proof itself.",
127:"Al angrily leaves after the guildmaster fires him. Maria sees strength worth recruiting despite his temper; Xien and the guildmaster warn that he causes trouble. She pursues him, describes herself as a private-fleet admiral, and challenges his courage in facing strong Western opponents. Al agrees and gives his first name. Her confidence is pointed and commanding; his roughness is proud rather than mindlessly abusive. No additional rank, completed battle or invented long name is supplied.",
128:"Angelo drops a pendant after bumping past. Yukihisa guesses the pictured woman is a lover; this is corrected when Angelo cries for his sister. Maria returns the pendant, learns he believes his sister is missing, and recruits him so he can search abroad. His claims of sailing experience remain modest. Sisterhood is explicit, romance only an initial guess. Preserve his Italian exclamations and the distinction between this scene's belief and the later revelation; do not reveal her death prematurely.",
129:"Angelo asks the whole crew to hear the truth: his only family, Bianca, died of illness three years ago. Unable to accept it, he convinced himself she was missing and searched the world. Recalling his own fever collapse, he reports her telling him that his companions are now family and that he should live for himself. The scene does not establish a living Bianca or explain whether the encounter was a dream or vision. Xien and Maria encourage him to live for her too and explicitly embrace the crew-as-family bond. His final private promise moves from apology to determination. Addressing Xien as an old man does not establish kinship.",
130:"Carlo negotiates a fair cinnamon price with Adil, then notices his illness and closes the transaction out of concern. The next morning the innkeeper thanks Carlo and offers the delayed visitors a gift; Adil stubbornly returns despite needing rest. Maria recruits Carlo for his commercial skill. He reveals that his daughter caught an epidemic illness, delayed treatment spread it to his wife, and both died a year ago while he neglected them for work. Happy memories make returning alone to Venice unbearable. Maria offers companionship and a new family aboard; he accepts. Retain grief, responsibility and warmth without inventing a diagnosis, gift identity, medical cure or a formal family relationship for the shared innkeeper label. Fernando's observation boast is an alternative utterance, not necessarily an additional fixed participant.",
131:"After drinking, Cristina recognizes a tune and dances. Two patrons admire her appearance and skill, cheer bravo, and applaud. Maria admires a passionate dance unlike those at home; Cristina names it flamenco and Maria hopes to see it again. Patrons appear inside FE panels, not newly assigned name-table actors. Preserve the Spanish dance and celebratory humor without making admiration a romance or inventing nationality for Maria's comparison.",
132:"In hot Calicut, impulsive Jam pursues street food and loses a ten-heads coin-toss wager to Samwell, promising to obey him. Maria suspects the coin; it proves to be two coins stacked with heads on both sides. Samwell turns exposure into a bid to travel with the fleet, claiming he can do anything. Jam wants to work him hard and is drawn into pleading alongside him. Maria admires the ingenuity that outmaneuvered Jam and accepts, while Xien remains skeptical. Samwell mentions boredom with elephants and a first sea voyage; do not invent an elephant-related job, real slavery, money loss, supernatural luck or training/stat outcomes. Richard and Yukihisa comments are alternatives. Keep Jam's rough energy, Samwell's childlike cunning and Maria's dry confidence distinct.",
133:"A Southeast Asian port worker reports that the absent party apparently has not returned. The one-line complete conditional speech supplies neither a gender nor a specific person's name. Preserve uncertainty and leave the referent neutral until exact source call context establishes it.",
134:"A separate Southeast Asian port-worker conditional uses the same absent-party report as B133. Treat it as an individual source record, with the same neutral referent and uncertainty; numeric adjacency does not identify who is away or make it the same activation.",
135:"Maria's crew rescues Cesare from men beating him. He cannot see why his blunt declaration that they are wrong about a flat Earth offended them. His formal, excitable pedantry contrasts with their disbelief. Maria recruits him for his inquisitiveness, ship knowledge and difficulty fitting into ordinary life; he explicitly has past captain and refitting experience. Optional Richard/Yukihisa/Xien reactions remain alternatives. Cesare then gives a complete practical tutorial: one-percent shares permit one to five units of goods; match ships to share and money; small under5,000, medium10,000–20,000, large over50,000; three masts are faster but need more sail handlers; refit up to five cargo rooms; more supply rooms extend range; combat needs large ships and a flagship with marine quarters and guns; two medium ships are cheaper and carry more than one large; retain old mediums for future local fleets. Preserve the source's price ranges and comparisons without filling gaps, revising historical science, adding rank, or claiming current inventory, purchases or tutorial effects.",
136:"Fernando offers a coin-taking game for a drink: take one to three coins per turn and whoever takes the last loses. Keep acceptance/refusal, losing/winning replies, recruitment attempts, coin-toss success/failure and idle variants separate. Maria declines the drink after winning and doubts his observational claims. He correctly reads a couple's breakup from her clenched fist and his avoidance of eye contact; their quarrel confirms it. They are a couple, not established spouses. Maria invites him to FO; he stakes recruitment on heads and may refuse an unlucky captain or accept and introduce himself. Do not invent the initial coin count, which player starts, paid sums, guaranteed wins or outcomes for unvisited branches. Distinguish his boastful gambler voice, the couple's mutual anger and Maria's curious but commanding manner.",
}

MEANINGS={
125:'''4|The governor recognizes and greets Admiral FA.
7|He reports Escante planned a coup to gain independence from Spain; the visitors prevented it.
10|One matter still concerns him.
14|Maria silently asks what he means.
18|He heard that someone recently carried Escante's sought treasure key to the New World's west coast.
22|Maria wonders whether it could be the Proof map.
25|Xien finds the western New World destination daunting.''',
126:'''4|Xien asks FI whether the ceremonial knife would fit the sun-emblem sheath exactly.
8|Maria notices their matching size.
12|Xien suspects they originally belonged together and tries sheathing the blade.
15|He is startled by the sudden event.
21|Maria is dazzled and asks what Xien did.
25|He does not know; the sheath suddenly shone, but it is now safe to open their eyes.
29|Maria notices a map on the blade and wonders when it appeared.
33|Xien does not understand the occurrence.
37|Maria identifies the New World Proof of Conquest map.
40|Xien marvels that sheathing the knife revealed a map, unable to explain it.''',
127:'''4|Al angrily rejects being underestimated.
7|The guildmaster dismisses him and says he is fired.
12|Al agrees to leave as requested.
15|Xien dislikes witnessing someone being fired.
18|Maria asks whether Xien noticed the man's physique.
22|Xien admires the muscles but sees a short temper and a propensity for trouble.
26|Maria suggests handling a difficult man is part of a leader's ability.
29|The guildmaster admires her confidence, recognizes FA and warns the man is hard to manage.
32|Maria asks about his actual fighting skill.
36|The guildmaster has never seen him lose a fight.
39|Xien responds with interest.
43|Maria is satisfied and asks Xien to pursue him.
47|Maria spots him.
51|Al asks what she wants.
55|Maria offers work.
59|Al asks whether she means to hire him and who she is.
62|Maria describes herself as admiral of a private fleet.
66|Al realizes she may be the renowned Admiral FA.
69|Recognition makes Maria's explanation easier.
72|She needs a strong fighter against formidable Western opponents and expects him to join her ship.
76|Al questions whether she is serious about Western enemies.
80|Maria pointedly asks if he is afraid and whether she misjudged him.
83|Al finds it interesting, agrees to help and insists his skill should not be underestimated.
87|Xien welcomes the strength and notes that they have not heard his name.
91|He names himself Al.
95|Maria welcomes him, dislikes empty boasts and expects him to deliver.''',
128:'''4|Angelo apologizes after the encounter.
8|Maria notices something with uncertainty.
12|Yukihisa asks what is wrong.
16|Maria finds the man's dropped pendant containing a woman's portrait.
21|Yukihisa guesses the woman is someone dear to him, perhaps his lover.
24|Maria proposes returning it.
29|Angelo exclaims in Italian for his dear sister and the lost pendant.
32|He frantically cannot find it anywhere.
35|Yukihisa identifies the man to the admiral.
39|Angelo loudly cries for his missing pendant.
42|Yukihisa formally tells him to calm down and asks if this is what he seeks.
46|Angelo joyfully recognizes his sister's pendant.
50|Maria asks whether the woman pictured is his sister.
53|Angelo confirms, thanks them and says he is searching for his missing beloved sister.
57|Maria hopes he finds her.
62|He recognizes her as a seafaring admiral, asks for work and says prior sailing experience makes him useful.
65|He pleads to search for his sister, believing she must be somewhere in the world.
69|Yukihisa asks Maria what she will do.
73|Maria sees the encounter as meaningful and agrees to hire him.
77|Angelo joyfully tells his sister to wait and introduces himself as Angelo Puccini.
80|Maria gives her FI FA name and welcomes working together.''',
129:'''4|Angelo asks to speak with the admiral.
8|Maria agrees, with slight surprise.
12|Xien offers to leave them alone.
16|Angelo asks Xien and everyone else to listen too.
19|Xien agrees.
23|Angelo introduces the subject of his sister Bianca.
27|Xien reminds him that they offered to help.
30|Angelo says that is not what he means.
34|He hesitantly says Bianca is already gone.
38|Maria asks what he means by gone.
42|Bianca, his only family, died of illness three years earlier.
45|Maria is shocked and asks why he said he was searching for her.
48|Angelo could not accept her death when it happened.
52|He convinced himself she was missing and searched the world.
55|Maria responds sympathetically to Angelo.
59|Angelo recalls the time he collapsed with a fever.
63|His sister told him that the crew were his family now and that he should live for himself.
66|Maria silently absorbs this.
70|Xien calls Bianca a good sister who truly worries about Angelo.
74|Xien tells him to live while he has life, for his late sister too.
78|Maria tells him not to sadden Bianca and explicitly affirms that the crew are family.
82|Angelo thanks them and asks for their continued companionship.
85|Maria reciprocates.
89|Angelo privately apologizes to Bianca and promises to live for her too.''',
130:'''4|Carlo orders his usual quantity of cinnamon.
8|Maria notices another customer is already there.
12|The merchant states the price.
16|Carlo notices the higher price.
20|The merchant denies a change and says it is the usual price.
23|Carlo laughs, addresses Adil by name and says he knows the wholesale cost.
26|Adil protests.
30|Carlo argues this year's production and local demand allow a better price.
34|He could buy elsewhere and is not obliged to use the same shop.
38|Adil concedes that Carlo has bested him.
42|Carlo notices something and asks if Adil has a fever.
45|Adil thinks Carlo is finding more fault with his business.
48|Carlo means his illness and recommends an early night.
51|Adil dismisses it, then notices real chills.
54|Carlo postpones buying to tomorrow and tells him to close the shop.
57|Adil agrees and apologetically asks the other visitors to return tomorrow too.
63|Carlo apologizes to the visitors, assuming they also came to trade.
66|Maria asks how he knew the merchant was ill.
70|Carlo points to the man's poor complexion.
82|Fernando boasts that Carlo's perceptiveness may rival his own.
88|Maria did not think the complexion was noticeably bad.
92|Carlo says most would not notice, but he is sensitive to others' health.
96|Maria is privately surprised.
100|Carlo invites her to the trade house tomorrow morning to make up for the delay.
103|Maria agrees to accompany him.
107|The innkeeper warmly thanks Carlo for yesterday.
111|Carlo asks after Adil.
115|She says he is staying in bed at home as a precaution.
118|Carlo hopes he recovers soon.
122|She complains he ignores her and trails off about Carlo's timely intervention.
126|She stops her lengthy talk, calls Carlo a lifesaver and offers thanks.
130|Carlo appreciates it but asks her to thank the delayed travelers instead.
134|She apologizes for delaying them and offers an unspecified modest gift.
140|Carlo thanks her and encourages the hurried travelers to shop first.
144|Adil returns and apologizes to Carlo for yesterday.
147|The innkeeper exclaims in alarm or annoyance at him.
151|Carlo insists Adil should be resting.
154|Adil claims to be fit and refuses to stay in bed on a good day for business.
158|The innkeeper calls him impossible.
162|Carlo is reassured by his energy but warns against overdoing it today.
166|Carlo postpones his own visit another day and asks Adil to serve these visitors.
169|He advises the travelers to value health and family, then says farewell.
172|Maria remains silent in thought.
177|She asks Carlo to wait.
181|Carlo responds.
185|Maria asks Carlo to use his business skill aboard her ship.
189|Carlo is startled by the sudden proposal.
193|Maria says she has considered it since yesterday.
196|Carlo says he is only a merchant, not a sailor.
199|Maria values his market knowledge and says fleets also need business talent.
203|Carlo pauses silently.
207|Maria asks if he dislikes going to sea alone or leaving family behind.
210|Carlo says his family died a year earlier.
213|Maria falls silent.
218|His daughter first caught an epidemic illness; engrossed in work, he neglected her care.
221|Delayed treatment allowed the illness to spread to his wife, and he lost both.
225|Maria responds with sorrow to the revelation.
229|His work felt empty after sacrificing his family; he now values people's health more than business.
232|Maria understands why he worried about the shopkeeper.
236|She asks about returning home.
240|Venice has too many happy memories for him to live there alone.
244|Maria pauses.
248|She offers for him to go to Venice with the crew rather than alone.
252|Carlo is puzzled.
256|Maria says sharing life aboard makes them like family and suggests a new family might be welcome.
260|Carlo asks if they would be his new family.
264|Maria says yes if he wishes.
268|Carlo thanks her and gladly accepts a place aboard.
271|He introduces himself as Carlo Cinato and asks to work well together.''',
131:'''4|Maria wonders whether she drank too much.
8|Cristina also drank quite a lot and notices something.
13|Maria notices the tune changed to music unlike her homeland's.
16|Cristina recognizes it and briefly excuses herself.
19|Maria wonders what she is doing.
24|Patron1 admires the woman.
27|Patron2 agrees she is beautiful and dances well.
32|Maria admires the performance.
36|Both patrons repeatedly cheer bravo.
39|Applause sounds.
43|Cristina says she could not resist dancing to a favorite tune.
46|Maria praises the passionate dance as unlike those in the East.
49|Cristina identifies the dance as flamenco.
52|Maria hopes to see it again.''',
132:'''4|Jam exuberantly reacts to Calicut's expected heat.
15|Richard says this hot climate does not suit his constitution.
20|Xien agrees it is very hot.
27|Maria notices the scenery has changed considerably here.
30|Jam spots a food stall and excitedly tells the admiral it looks delicious.
34|Xien tries to stop him, but he has already run off.
37|Maria reacts with exasperation.
41|Jam calls desperately for the admiral's help.
44|Xien asks whether that is Jam's voice.
47|Maria finds a cry for help unusual for Jam and wonders what happened.
58|Yukihisa guesses strange food caused a stomach upset.
65|Jam apologizes that a strange child has caught him.
70|Samwell identifies the admiral and claims Jam after winning a bet against him.
74|Xien asks who this boy is with surprise.
78|Maria asks what claiming Jam means.
82|Jam says the peddler offered him a bonus if he won a coin toss, tempting him to play.
86|Xien understands he lost, but asks why that makes him the other's property.
90|Samwell says Jam promised to obey anything if heads came up ten times in a row.
93|Jam protests that ten heads in succession normally never happen and cannot believe it.
97|Samwell smugly notes that it really did happen.
100|Maria asks to inspect the coin.
104|Samwell nervously refuses.
107|Xien finds this suspicious.
111|Jam suspects cheating and demands the coin.
114|Samwell cries out.
118|Jam reacts to what he sees.
122|Samwell admits he has been found out.
126|Xien discovers two coins stacked together with heads on both outer sides.
130|Jam angrily curses the child's deception.
133|Samwell laughs and apologizes lightly.
137|Jam says an apology is not enough.
140|Samwell offers to count the bet as his own loss.
143|Xien asks what follows from that.
147|Samwell asks to travel with them and offers to do anything.
158|Yukihisa finds the maneuver brazen.
172|Richard doubts such an impudent man would be useful.
175|Jam privately finds Richard's criticism hypocritical.
181|Xien is speechless at the boy's audacity.
187|Samwell calls them travelers and claims he can do anything useful.
191|Jam relishes working him hard and asks the admiral for permission.
195|Maria pauses without agreeing.
199|Xien says it obviously is not acceptable.
203|Samwell pleads to the admiral.
207|Jam joins the plea, then notices Samwell is asking too.
210|Samwell is tired of elephants, wants to visit other countries and sincerely offers to do anything.
214|Maria agrees.
218|Samwell celebrates.
222|Xien asks FI whether she is really sure.
225|Maria admires his ability to outmaneuver Jam and thinks he may be a valuable find.
229|Jam realizes he may have been used and curses it.
233|Samwell celebrates travel, reveals he has never sailed before and gives his name.
238|Maria welcomes him with a pause.
242|Xien still sees him as a hindrance.''',
133:'''5|The absent party apparently has not returned yet; gender and identity are unstated.''',
134:'''5|The absent party apparently has not returned yet; this is a separate conditional record.''',
135:'''4|A henchman shouts roughly.
8|Cesare squeals and formally begs for help.
18|Richard is startled and asks what happened.
24|Xien asks what is going on.
31|Maria sees someone being beaten over there.
35|Xien sees the victim looks weak and asks whether to help.
39|Maria agrees.
51|Yukihisa condemns attacking the weak and joins the rescue.
68|Xien asks if the young man is all right.
72|Cesare is hurting and says he is not very well.
76|Maria asks why he fought those men.
88|Yukihisa asks if they picked a quarrel and notes villains exist everywhere.
95|Cesare hesitates awkwardly.
99|Maria prompts him with uncertainty.
104|Cesare explains that the men claimed the Earth was flat.
107|Xien asks what that has to do with it.
111|Cesare insists a round Earth is common knowledge and he wanted to correct them.
114|Maria asks what happened next.
118|Cesare began explaining and the men immediately behaved strangely.
122|They scowled, objected to his correction and started hitting him.
126|Xien still does not understand the situation.
129|Cesare says he does not understand either.
133|He merely bluntly told them that they were wrong, after which he trails off.
137|Maria supplies that they became angry.
141|Cesare is astonished she knows that.
144|Xien thinks anyone could work it out.
148|Cesare still cannot understand.
151|He thinks correcting their false knowledge should earn thanks.
154|He would be grateful to learn another truth about the world.
166|Yukihisa notes eccentrics exist in every country too.
172|Xien approves of inquiry but has reservations.
176|Maria pauses thoughtfully.
180|She asks if Cesare knows about ships.
184|Cesare says he was once a captain and enjoyed modifying ships.
195|Yukihisa cannot believe he was a captain.
202|Maria decides that leaves no difficulty.
205|Cesare is puzzled.
216|Richard asks if she intends to take this man aboard.
222|Xien asks FI whether she really intends to take him aboard.
229|Maria likes his curiosity and thinks his personality makes ordinary life difficult.
241|Yukihisa agrees with that assessment.
255|Richard calls the admiral oddly kind in certain situations.
260|Xien similarly calls her unexpectedly softhearted.
266|Cesare hesitantly seeks attention.
270|Maria apologizes for neglecting him and asks what he wants.
273|Cesare asks if she is an admiral.
276|Xien confirms and asks if he knows FO.
280|Cesare realizes she is Admiral FI FA.
284|Maria asks whether he knows her, then offers work as a navigator.
288|Cesare eagerly accepts and begs to sail aboard.
291|Maria settles the matter and asks his name.
294|He introduces himself as Cesare Toni and thanks her.
297|Xien cannot see what the admiral likes about him.
309|Yukihisa calls it a mystery.
321|Cesare begins a further explanation.
325|New contracts and routes alone do not require new ships; a one-percent contract share buys only one to five units of goods.
328|Larger shares and goods availability indicate it is time to buy ships.
332|First consider a ship's size and price.
335|Match ships to shares and funds, or empty capacity will still require unnecessary sailors.
338|Prices indicate size: small below5,000; medium10,000 to20,000; large above50,000.
341|Cheap small ships readily increase fleet cargo capacity despite limited funds.
344|After profitable trading and more funds, replace them with medium ships.
348|Medium ships have two or three masts; three masts are faster but need more sail handlers.
351|Refitting allows up to five cargo rooms; marine quarters and gun decks are unnecessary if not fighting for now.
354|More supply rooms permit longer voyages to distant towns and new routes.
357|Conflict with another power calls for large ships.
360|At least the flagship needs marine quarters and guns for a reasonable chance in naval combat.
363|Funds determine the rest: two medium ships cost less and carry more than one large ship.
366|Eventually large replacements are needed, but keep old medium ships for a future local fleet.
369|Cesare finishes his advice and leaves to prepare departure.''',
136:'''10|Fernando insists the visitor play now that they are here; this is a variant invitation.
15|He invites a newcomer to wager a drink on a simple game.
19|They alternate taking one to three coins from a pile.
23|Whoever takes the final coin loses; he begins after explaining.
SC3_B136_CHOICE_356_0|Accept the game.
SC3_B136_CHOICE_356_1|Decline the game.
46|After winning, Fernando claims his drink.
50|He enjoys it, thanks them and says farewell.
59|After losing, he admits an uncommon defeat and pays the wager.
69|Maria finds him not good enough, declines alcohol and questions his confidence in gambling.
73|Fernando says perception and luck are essential to gambling.
76|He claims to possess both and to be born to gamble.
80|Xien questions the claimed perception, leaving luck aside.
84|Fernando cautions against judging by appearances.
88|He asks what the distant couple are discussing when their words cannot be heard.
91|Maria guesses a proposal.
95|Fernando calls this elementary and says they are breaking up.
99|Maria is puzzled.
103|Fernando tells her to watch.
107|The woman says she cannot accept his thinking anymore and calls him too selfish.
110|The man says she can think that, but he finds her selfish too.
113|The woman concludes they should stop seeing each other.
116|The man agrees that mutual feeling ends the relationship.
119|Maria silently takes it in.
123|Fernando asks whether his prediction was correct.
127|Maria is impressed and asks how he knew.
131|Her fist clenched beneath the table showed suppressed anger rather than romantic conversation.
135|He avoided her gaze throughout, unlike a man facing a woman he loves.
139|Maria is impressed by how much he noticed.
143|He says that perception lets him read an opponent's hand.
146|Combined with his exceptional luck, it lets him win.
149|Maria praises the talent and invites him to test it with FO.
153|Fernando finds this an abrupt proposal.
157|With time to spare, he offers to join if his tossed coin lands heads.
163|On a repeat attempt Maria refuses alcohol and tells him to join FO instead.
167|Fernando recognizes the repeated request and proposes asking the coin again.
192|On failure he will not entrust his life to someone unlucky and leaves.
208|On success he commits to staking his life on her.
211|He introduces himself as Fernando Dias and credits luck.
214|Maria welcomes him.
228|An idle variant says business or prospects have been poor recently.''',
}

def key(row):
    return int(row['id'].rsplit('R',1)[1]) if row['kind']=='ordinary-speech' else row['id']

def parsed(number):
    rows={}
    for line in MEANINGS[number].splitlines():
        k,v=line.split('|',1); k=int(k) if k.isdigit() else k
        assert k not in rows and v.strip(); rows[k]=v.strip()
    return rows

def main():
    target=ROOT/'all337_clean_meanings_v1.json'; assert not target.exists()
    path=ROOT/'clean_source_packet.json'; packet=load(path)
    assert packet['source_only_not_current_English'] and len(packet['groups'])==12 and packet['records']==337
    assert set(CONTEXT)==set(MEANINGS)==set(packet['selected_blocks'])
    rows=[]
    for group in packet['groups']:
        number=group['block']; meanings=parsed(number)
        assert set(meanings)=={key(r) for r in group['records']},number
        block=bytes.fromhex(group['clean_block_hex'])
        for original in group['records']:
            row=deepcopy(original); raw=bytes.fromhex(row['source_hex']); at=row['source_reference']['offset']
            assert block[at:at+len(raw)]==raw and not row['covered']
            row.update(source_meaning=meanings[key(row)],whole_exchange_context=CONTEXT[number],
                source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
                independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
            if row['kind']=='ordinary-speech':row.update(source_selector=raw[0],source_complete_preamble_hex=block[at-5:at+1].hex())
            rows.append(row)
    assert len(rows)==337
    save(target,dict(records=rows,source_objects=337,complete_exchanges=12,source_meanings_sealed_before_independent_drafts=True,
        no_current_story_English_read=True,all_five_gates_pending=True,new_credit=0,
        explicit_pending_term_bindings=['儀式用の小刀','太陽紋の鞘','覇者の証','シェア','操帆手','積荷倉庫','海兵詰所','砲台','物資倉庫','地方艦隊'],
        unresolved_contexts=['B133/B134 absent referent is intentionally neutral; inspect exact source caller before asserting identity.',
            'Angelo fever recollection is reported experience; do not label it a dream, vision or physical return without linked source.',
            'Full names and tutorial UI units are provisional until source/current consumer binding.'],
        evidence={str(p):digest(p) for p in [path,Path(__file__)]}))
    print('Sealed337 clean meanings in12 complete exchanges; current English,drafts andall five gates remain pending.')

if __name__=='__main__':main()
