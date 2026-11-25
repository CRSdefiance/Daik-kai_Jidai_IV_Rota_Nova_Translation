"""Seal335 individual clean meanings before independent drafts or current English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B137_B151_clean_20261109')
CONTEXT={
137:'Julio and Xien competitively deny being old after another crew member calls them alike. Maria turns the quarrel into recruitment. The old-men pair joke conveys resemblance, not kinship or retirement; conditional crew replies remain alternatives.',
138:'Manuel admires the ship but sees inadequate maintenance. Maria respects his experience and love of ships, tactfully accepts his refusal to discuss his past, and invites him aboard. Optional flagship-room advice covers morale, consumption, healing and carpentry; exact installed UI room names require later binding.',
139:'A local warns about learned Mikhail, especially with women present; Julio emphatically opposes meeting him. Mikhail jokes about pepper/rabbit droppings and bust size, refuses male recruitment, then insists on joining after seeing Maria. His unwelcome familiarity and self-serving Western-custom defense remain his claims. No actual grandparent relationship, age for the women, specific physical act or narrator endorsement is invented. Three FE tutorials explain that this scholar is not a sailor, cannot be assigned on deck, and unlocks detailed item information with X.',
140:'Yukihisa catches Yifa following the party. She wants worldwide training to prove herself to her master. Her claimed Taoist immobilization appears ineffective, but she attacks during the distraction; Maria and Yukihisa recognize real martial potential without confirming supernatural success. Maria accepts her on equal working terms. Familiar sister/brother forms of address do not establish family.',
141:'Sang Hyeon appears during Marias sleep, identifies himself as Yifas senior fellow disciple, and says she violated the ban on leaving their country and was expelled from the school. He cannot take her back, but their childhood sibling-like bond motivates his private appeal for guidance and continued training. Maria calls it a vivid dream; Yifa attributes it to a magical visit because he cannot leave the mountain. Preserve those perspectives, not an objective explanation or biological brotherhood.',
142:'Julian courts Mihwa, who is preoccupied with the rare Silla crown reportedly in Seoul and unavailable in shops. She agrees only to consider a date, though he eagerly calls it a promise. Maria is interested in the crown, not Julian, and offers a conditional search without promising success.',
143:'A Seoul tavern informant hesitates to disclose the crown location after Julians inquiry. Recognizing Maria and FO makes her nervous and helpful. She reports the Tomb of King Muryeong, with no further information; Maria privately finds the organizations influence troublesome. Do not turn tentative reporting into confirmed ownership or specify a threat.',
144:'Julian acknowledges Maria found the crown and gave it to him. He presents it to Mihwa, then asks to repay Maria by joining. His grandfather really sailed around the world; Julians own skill is a boast, and he wants to become an adventurer. Maria cites his boldness in Seoul. He flirts with Maria, reassures Mihwa and promises a better gift/date; Maria worries the journey will become womanizing.',
145:'The previously encountered female pirate and her crew surround Maria and Xien. The pirate stops a subordinate threatening them, insists on settling things at sea instead of killing them here, and notices a fine sword. Maria is puzzled; preserve the ambiguous attraction/target without inventing an item transfer or literal royal rank from mocking princess. The crew obeys her departure order; Maria anticipates more pursuit.',
146:'Jam and Ian discuss Yukihisas unsuccessful sword search. Maria privately offers him an independent fleet command to Japan so he can search; he refuses misuse of organizational ships for personal purposes. She reframes it as an admirals sensible choice of someone familiar with the region. No sword is obtained, fleet assignment mechanically completed or personal debt invented.',
147:'Jam reflects that India makes human activity feel small and daydreams about relaxing there after the major undertaking. Maria teases his premature vacation plans; he acknowledges much remains. Keep the contemplative contrast within his casual voice.',
148:'Crew members discuss Arab abstinence and a tavern catering to foreigners. Ian admires discipline, beauty and protection of the weak despite ethnic/religious differences and occasional fierceness. Jam jokes about Ians vodka and Yukihisas sake and admits his own temperament does not suit the local culture. These are character observations, not newly asserted universal historical facts.',
149:'An imperious woman predicts bananas will become fashionable, overrides a skeptical respondent, and orders as many as can be bought. The FE notice forecasts a possible Seville banana fashion, not an active shortage, fixed profit or already established boom.',
150:'The same pair discusses tomatoes: the womans enthusiasm for their red color evokes youthful passion, while the respondent is dry and compliant. She orders tomato dishes prepared for sale. The FE notice forecasts possible tomato fashion in Genoa, not a guaranteed current market condition.',
151:'Three women discuss baking bread at home. One explicitly mentions her husband; the others are not therefore assigned husbands. A woman offers to teach another to bake, then they shop for ingredients, starting with wheat. The FE notice forecasts wheat becoming fashionable in Amsterdam. Preserve cooking instruction, not invented trading advice or a flour-for-wheat commodity substitution.',
}
MEANINGS={
137:'''4|Julio complains of recent boredom.
9|Xien notices a seasoned-looking man.
12|Maria thinks elderly describes him better than seasoned.
15|A crew member suggests the two alike old men drink together.
18|Xien indignantly asks what alike means.
22|Julio laughs that Xien is lively for an old fellow.
26|Xien insists he is still young and assumes Julio is retired.
30|Julio insists he is an active navigator who can match younger men.
34|Xien challenges the old fellows bold claim.
38|The crew member says this proves their resemblance.
42|Maria asks Xien not to get worked up, then politely confirms the stranger is a navigator.
46|He introduces Julio Erneco and recognizes Admiral FA with uncertainty.
50|Maria is honored by the recognition and asks his interest in her ship.
53|Julio is interested and asks whether this is a recruitment invitation.
57|Maria confirms that interpretation.
61|The crew member finds the admirals taste peculiar.
73|Fernando says the critic is hardly one to talk.
80|Xien will not oppose FIs decision despite reluctance.
84|Julio agrees; sailing together will show which man is old, though he claims the result is obvious.
87|Xien insists he is obviously the younger one.
91|Maria calms them and says she relies on both.
95|The crew member jokes about the new old-men duo and coming amusement.''',
138:'''4|Xien alerts FI to someone near their ship.
9|The stranger admires the ship but has a reservation.
12|Maria asks what he is doing there.
16|He was looking at the ship and poetically feels its heartbeat nearby.
20|He begins a criticism, then suddenly recognizes possible Admiral FA.
23|Maria confirms and returns to his unfinished observation about the ship.
26|He thinks maintenance inadequate and personifies the ship crying unless shown more care.
30|Xien remarks on the poetic expression.
33|Maria asks who he is.
37|He names himself Manuel, says he used to be a navigator, and apologizes for his presumption.
41|Xien admits the maintenance deficit and respects its immediate detection as skill.
45|Maria recognizes knowledge, experience and affection for ships.
48|She asks why someone who plainly loves ships quit sailing, if he is willing to tell her.
52|He apologetically avoids discussing his past.
56|Maria changes tack and asks whether he would return to sea and shipboard life.
59|He asks what she means.
63|Maria wants him to care for her ship.
66|He is silent.
70|She asks his decision, making clear it depends on his willingness.
74|He thanks her, calls proximity to ships his purpose in life and gladly accepts.
78|He offers advice on refitting the flagships assigned work rooms.
SC3_B138_CHOICE_1274_0|Accept the offered explanation.
SC3_B138_CHOICE_1274_1|Politely decline it.
93|He will especially explain rooms useful in preparing for long-distance voyages.
97|Assigning high-persuasion people to the adjutants room and chapel eases sailor discontent.
101|Staff in the galley and animal room reduce fleet water and food consumption.
105|A ships doctor in the infirmary treats fatigue, epidemics and injuries of companions and sailors.
109|Ill or injured navigators recover faster in private quarters or the recreation room.
113|A carpenter like him repairs damaged ships at sea in the timber room and helps refitting and repairs at shipyards.
116|He hopes the hurried explanation proved useful.
119|The fleets fate depends on the admirals judgment; refit carefully rather than neglect it.
125|On refusal he acknowledges the choice and leaves it to Maria.''',
139:'''4|A local asks whether they too came to see old Mikhail.
7|Maria repeats the unfamiliar reference.
19|Julio reacts strongly to the name and urges FI not to meet him.
25|The local corrects the assumption and notes the old man is famous locally for knowledge.
29|Xien suggests FI meet someone potentially useful.
32|Maria agrees.
36|The local warns against visiting with women present.
47|Julio vehemently agrees that they should not go.
53|Maria is puzzled.
57|Maria identifies the man as Mikhail.
61|A woman excitedly praises the old man.
65|Mikhail smugly agrees and laughs.
68|Another woman asks about an object.
72|Mikhail calls it pepper fruit, a tropical tree fruit ground for spice.
76|He says it should grow near Brunei and become useful trade goods.
80|He then realizes this particular object is rabbit droppings and calls it filthy.
84|The woman recoils and asks him to throw it away.
88|He casually discards it.
92|The first woman marvels at his knowledge and asks its reason.
96|He boasts of genius and superior knowledge, then claims he can even guess her bust size.
100|She squeals that the old man is a lecher.
104|He laughs.
108|Xien acknowledges his learning despite his personality and proposes recruitment.
112|Maria reluctantly agrees.
116|Mikhail demands to know who they are.
120|Xien praises the knowledge and requests help for FO.
124|Mikhail refuses to leave the town and rejects an invitation from a man.
128|Xien presses the request politely.
131|Mikhail hesitates, then suddenly notices something.
134|He asks the accompanying womans name.
137|Xien identifies their admiral FI FA.
140|Mikhail repeats FI with excessive familiarity.
144|He enthusiastically approves.
148|Maria is confused.
152|Mikhail abruptly decides to come with them.
155|He calls out FI affectionately.
159|He vows to follow her anywhere.
163|Maria exclaims in alarm.
167|Xien checks FIs safety and condemns his insolence.
170|Mikhail stubbornly insists on joining and says his useful knowledge makes worry unnecessary.
173|Maria notes they invited him first and allows his boarding despite the situation.
177|Xien objects to the shameless man.
181|Mikhail denies shamelessness, calling it affectionate physical familiarity.
184|He claims Western friendship and affection use such familiarity, which Easterners may not understand.
187|Maria declines that familiarity.
195|The scholar Mikhail is not a navigator and cannot be assigned on deck.
199|His presence enables detailed item information.
202|Try pressing X while item information is displayed.
205|He cannot do shipboard work but offers to be called for questions about items.''',
140:'''6|Yukihisa challenges a suspicious follower.
10|The follower squeals.
14|Maria asks what happened.
18|Yukihisa says this person has followed them and hesitates.
22|He had not expected the follower to be such a girl.
26|She demands release.
30|Maria tells Yukihisa to release her and asks why she followed.
33|The girl wants a favor from Maria, using a familiar older-sister address without kinship.
37|She identifies Maria with FO and asks to board her ship.
41|Xien criticizes the abrupt request and her manners.
45|Maria asks her reason rather than accepting the sudden demand.
49|She wants worldwide training, strength and a chance to prove her master wrong.
52|Yukihisa asks which discipline she studies.
56|She welcomes the question and offers to show Taoist arts.
59|Yukihisa questions that claim.
63|She asks him to ready his sword and announces her attack.
67|He reacts sharply.
71|She shouts with exertion.
75|He is puzzled.
79|Maria privately thinks nothing seems to have happened.
82|The girl exploits his opening and attacks.
87|He dodges with an exclamation.
91|She praises his evasion and calls the move an immobilization spell.
94|He questions immobilization and thinks it was merely his own lapse.
97|She smugly calls it mysterious.
101|Maria praises even her ability to close on Yukihisa so quickly.
105|Yukihisa recognizes movement and distance judgment grounded in martial training.
108|Maria asks whether she is serious about going out into the world.
112|The girl repeats the wish to prove her master wrong and pleads for worldwide travel.
116|Maria notes that motivation can drive growth and asks her name.
120|She introduces Yifa.
124|Maria requires full work and no special treatment aboard.
128|Yifa welcomes those terms.
132|Yukihisa introduces himself and vows not to be caught off guard again.
135|Yifa teasingly asks whether he can defeat her Taoist arts.''',
141:'''9|An indistinct formal address reaches sleeping Maria.
13|Maria remains silent.
17|The visitor calls FI respectfully.
21|Maria stirs in surprise.
25|He apologizes for the intrusion and denies suspicious intent.
28|He introduces Sang Hyeon as Yifas senior fellow disciple.
32|He learned Maria would care for Yifa and came to pay respects.
36|Maria repeats his connection to Yifa.
40|He blames inadequate guidance for her unrestrained upbringing.
43|She left the mountain without the masters permission to escape training, and even left the country; he calls this impermissible.
47|She does not know their people are forbidden to leave the country.
51|Maria asks whether he came to bring her back.
54|He cannot; violating the national ban was serious and she was expelled from their school.
57|He says they now have no formal connection.
60|Nevertheless they grew up together like actual brother and sister.
63|He worries that her immaturity will cause trouble for others.
67|He asks Maria to guide her away from wrongdoing despite the imposition.
70|If possible, she should continue training after leaving the mountain and obey the masters teachings.
73|He earnestly entrusts her care to Maria.
76|Maria wonders if the vivid encounter was a dream.
79|Yifa bursts in with an exuberant morning greeting and impatient departure request.
82|She suddenly reacts.
86|Maria asks what is wrong.
90|Yifa senses her senior fellow disciples presence.
94|Maria asks whether that persons name is Sang Hyeon.
97|Yifa is startled that Maria met him, using familiar brotherly address without biology.
100|Maria says someone claiming that relationship introduced himself in her dream.
104|Yifa questions the dream.
108|She fondly thinks of Sang Hyeon.
112|She concludes he used his arts to visit because he cannot leave the mountain.
116|Maria questions magic aloud and privately understands.
119|Maria relays his request to continue training after leaving the mountain.
123|Yifa laughs affectionately at his enduring worry.
127|Maria hesitates and asks what is wrong.
130|Yifa promises diligent training so as not to disappoint Sang Hyeon.
134|Maria expects the same energy for shipboard duties.
137|Yifa cheerfully says she knows.''',
142:'''6|Julian romantically declares he lives for Mihwas radiant smile.
10|Mihwa affectionately reacts to him.
14|Maria imagines tavern work is hard with men like him every day.
17|Julian expects her usual smile and fears she dislikes him.
21|She denies it; his words normally cheer her.
25|Something she deeply wants now occupies her waking and sleeping thoughts.
29|He dislikes seeing her sad and asks what she wants.
33|She names the Silla Gold Crown, calls its name mysterious and reports its rarity/value.
37|He worries about expense and affordability and asks where it is sold.
40|It apparently is not sold in shops; she heard it is in Seoul.
43|Not being sold prompts his sudden idea of a likely place.
46|She asks whether he has a lead.
50|He promises to get the crown quickly and restore her smile.
54|Her smile powers him; he asks whether bringing the crown will earn a date.
57|She calls him premature and agrees only to consider it.
61|He celebrates as if promised a date and immediately leaves for Seoul.
64|She starts to say she has hopes, then realizes he is already gone.
67|Maria finds the overheard conversation interesting.
71|Mihwa thinks Julian might suit Maria romantically.
75|Maria clarifies her interest is the crown rather than the man.
79|Mihwa accepts that as more natural and asks whether Maria has a crown lead.
82|Maria has none and requests Mihwas information.
86|Mihwa knows only it is in Seoul and very beautiful.
90|Maria may search if she visits Seoul.
94|Mihwa excitedly asks to see it if Maria obtains it.
97|Maria agrees conditionally but advises relying on Julian rather than herself.''',
143:'''5|The tavern woman welcomes visitors.
9|Maria thinks someone in a tavern may know.
12|She asks whether anyone knows of the Silla Gold Crown.
16|The woman says she does, with hesitation.
20|Maria asks to be told its location.
23|The woman deliberates.
27|Maria asks whether an information fee is required.
31|It is not money; a very frivolous-seeming man just asked the same thing.
35|Maria identifies him as likely Julian from Hangzhou.
39|The woman asks their connection and Marias identity, then realizes it.
42|Maria reacts with a question.
46|The woman asks whether she is FI of FO.
50|Maria confirms.
54|The woman nervously reports the crown is said to be in the Tomb of King Muryeong ruins, with no further knowledge.
58|Maria will visit and thanks her.
61|The woman nervously demurs.
65|Maria privately finds FOs powerful influence troublesome.''',
144:'''5|Julian recognizes FI.
9|Mihwa asks when they became acquainted.
13|Julian admits Maria found the crown and he only received it from her.
17|Mihwa marvels at the crowns shining gold and breathtaking beauty.
21|Julian presents it as his promised gift.
25|Mihwa thanks him and promises to treasure it forever.
28|Maria is glad for them.
32|Julian credits Maria and wants to repay her.
35|Maria says repayment is unnecessary.
39|He insists on repaying Admiral FI of FO by working aboard her ship.
42|Xien doubts whether this counts as repayment.
45|Julian says not to worry about skill, citing his grandfathers worldwide sailing and his own childhood love of ships.
48|He wants to become an adventurer like his grandfather and see the world.
52|Xien considers whether he inherited his grandfathers adventurous temperament.
55|Maria accepts, impressed by his boldness in Seoul.
59|Julian celebrates traveling with a beautiful woman like Maria.
63|Mihwa pointedly calls his name.
67|He apologizes, says he is leaving and tells her not to be jealous of his new employer.
71|He promises to return with something finer than the crown and asks for a date.
75|Mihwa gives in affectionately and will wait.
78|Maria hopes the voyage will not consist of courting women.''',
145:'''5|The female pirate says fate seems to keep bringing them together.
8|Maria recognizes the earlier female pirate.
12|Xien warns FI that the surrounding people also seem to be pirates.
15|The pirate mockingly greets a princess and asks whether she wants liquor or something else.
18|A pirate chuckles menacingly.
22|Another pirate snickers.
26|Maria asks their intention toward her party.
30|The leader admires Marias steady nerve.
33|Xien rejects a pirates right to address them so.
36|A subordinate calls him bold for an old man and threatens to tear them apart instantly.
40|The leader sharply stops the subordinate.
44|He fearfully apologizes.
48|Maria unexpectedly finds the leader reasonable.
51|The pirate grudgingly calls Maria a remarkable princess.
54|She rejects being underestimated and says she will not kill them here because pirates have their own ways.
57|She promises to settle things at sea and threatens future death.
60|Maria understands and is ready whenever the pirate is.
63|The pirate tells her to remember those words, then notices something.
66|Maria asks what is wrong.
70|The pirate likes Maria more after noticing a fine sword.
73|Maria questions the sword reference.
77|The pirate dismisses her incomprehension and promises to take whatever she has marked as her target.
81|Maria is silent.
85|The leader orders her crew to withdraw.
89|The crew answers in unison.
93|Xien admires commanding so many with one order.
97|The pirate warns against underestimating her because she is a pirate.
100|Maria finds her interesting.
104|Xien acknowledges spirit despite her piracy.
108|Maria expects persistent pursuit for some time.''',
146:'''4|Maria notices something.
8|Jam asks whether Yukihisa found any clue to the sword he seeks.
12|Ian thinks he has no lead yet.
15|Jam wonders whether the sword exists.
18|Ian does not know.
22|Maria is silent.
27|Maria addresses Yukihisa.
31|He acknowledges the admiral.
35|She heard he seeks a sword.
39|He says it may be only rumor, having found no clue despite worldwide travel.
42|Maria would like to help if possible.
45|He says it is unrelated to their purpose and asks her not to worry.
49|Maria asks whether he would go to Japan independently.
52|He is surprised.
56|She offers him a fleet and time for a thorough search away from their main voyage.
59|He refuses to borrow organizational ships for private matters.
63|Maria recognizes his dutifulness but says choosing someone familiar with a region is a natural admirals decision.
67|Yukihisa gratefully thanks her.''',
147:'''4|Jam remarks on Indias distinctive atmosphere.
7|Human affairs feel very small to him there.
10|After their big undertaking settles down he might spend idle time there.
13|Maria teases the prematurity of vacation planning.
16|Jam laughs and acknowledges their huge remaining workload.''',
148:'''4|Maria observes Arab abstinence and says this towns tavern reportedly serves foreign sailors.
8|Ian admires Arab strong will and rigor across differences of people and religion.
12|Yukihisa agrees.
16|Jam cannot imagine Ian giving up vodka or Yukihisa sake, explaining their admiration.
20|Ian concedes that point but says his praise extends beyond alcohol.
23|Maria asks implicitly for explanation.
27|Ian sees love of beauty and strong kindness protecting the weak behind sometimes merciless fierceness.
31|He thinks they have much to learn from them.
34|Jam did not know Ian admired Arab culture and finds it incompatible with his own temperament.
37|Maria amusedly agrees it would not suit Jam.''',
149:'''5|The woman declares bananas the coming fashion.
8|The respondent incredulously asks about bananas.
12|She believes the flavor will certainly catch on.
16|The respondent doubts it.
20|She overrules doubt by insisting her judgment settles it.
23|The respondent gives in and asks for instructions.
26|She orders as many bananas as can be bought.
30|The respondent complies perfunctorily.
34|She grandly repeats that the banana age is coming and laughs.
37|FE forecasts bananas may become fashionable in Seville.''',
150:'''5|The woman declares tomatoes the coming fashion.
8|The respondent doubts such bright-red food will catch on.
11|She loves the passionate red, which recalls a burning youthful love.
15|The respondent dryly says that is nice for her.
19|She orders tomato dishes cooked and offered for sale immediately.
22|The respondent agrees.
26|She warns not to miss this tomato fashion.
29|The respondent complies perfunctorily.
33|She encouragingly dismisses the respondent with grand laughter.
36|FE forecasts tomatoes may become fashionable in Genoa.''',
151:'''6|The first woman says homemade bread is best.
9|The second agrees and says her husband loved it.
12|The third asks if baking ones own bread really tastes that good.
16|The first enthusiastically affirms and seeks agreement.
20|The second says the corner bakery cannot compare.
23|The third considers baking some herself.
27|The first encourages her.
31|The second offers to teach her to bake.
35|The third is pleased by the offer.
39|The first proposes immediately shopping for ingredients.
42|The second asks what they need.
46|The third says wheat should come first.
50|FE forecasts wheat may become fashionable in Amsterdam.''',
}


def key(row):
    return int(row['id'].rsplit('R',1)[1]) if row['kind']=='ordinary-speech' else row['id']


def main():
    target=ROOT/'all335_clean_meanings_v1.json';assert not target.exists()
    path=ROOT/'clean_source_packet.json';packet=load(path)
    assert packet['source_only_not_current_English'] and len(packet['groups'])==15 and packet['records']==335
    assert set(CONTEXT)==set(MEANINGS)==set(packet['selected_blocks'])
    rows=[]
    for group in packet['groups']:
        number=group['block'];meanings={}
        for line in MEANINGS[number].splitlines():
            k,v=line.split('|',1);k=int(k) if k.isdigit() else k
            assert k not in meanings and v.strip();meanings[k]=v.strip()
        assert set(meanings)=={key(r) for r in group['records']},number
        block=bytes.fromhex(group['clean_block_hex'])
        for original in group['records']:
            row=deepcopy(original);raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
            assert block[at:at+len(raw)]==raw and not row['covered']
            row.update(source_meaning=meanings[key(row)],whole_exchange_context=CONTEXT[number],
                source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
                independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
            if row['kind']=='ordinary-speech':row.update(source_selector=raw[0],source_complete_preamble_hex=block[at-5:at+1].hex())
            rows.append(row)
    assert len(rows)==335
    save(target,dict(records=rows,source_objects=335,complete_exchanges=15,source_meanings_sealed_before_independent_drafts=True,
        no_current_story_English_read=True,all_five_gates_pending=True,new_credit=0,
        provisional_terms_andnames_require_current_native_bindings=['Yifa','Sang Hyeon','Julian','Mihwa','Manuel','Mikhail','Silla Gold Crown','Tomb of King Muryeong','Seoul','all eight work-room labels','wheat'],
        unresolved_contexts=['B145 sword reference retained without inventing a specific item transfer or a literal royal title.',
            'B141 senior-disciple relationship is explicitly sibling-like, not biological; dream and magical-visit accounts remain attributed.',
            'B139 affectionate physical familiarity is implied but no exact physical act is supplied by these spoken lines.',
            'B149/B150/B151 trend notices are prospective; wheat bread-learning exchange must remain cooking instruction.'],
        evidence={str(p):digest(p) for p in [path,Path(__file__)]}))
    print('Sealed335 clean meanings in15 complete exchanges;current English,drafts andall five gates remain pending.')


if __name__=='__main__':main()
