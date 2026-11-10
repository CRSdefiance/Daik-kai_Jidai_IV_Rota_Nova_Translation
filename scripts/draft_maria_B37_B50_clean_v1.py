"""Seal286 logical US-English drafts from the saved clean meanings, before current-dialogue intake."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B37_B50_clean_20261109')
MEANINGS = ROOT/'all286_clean_meanings_v1.json'
OUT = ROOT/'all286_clean_meanings_andindependent_drafts_v1.json'

DRAFTS = {
37:'''4|We made it... That Kuhn...
7|Lil! Are you all right?!
11|Yes... Everyone, this was all my fault... I don't know how to apologize...
15|It's over now. Kuhn's the one to blame.
18|We seem to have escaped the worst. I'll be heading back to the North Sea. I'll take my leave, then...
22|Thank you, Hodram.
26|FI's the one you should thank.
29|What will you two do?
33|I'm going back to the North Sea too. I've realized I'm nowhere near ready to take on the world...
37|Lil... I'll go with you.
40|Thank you, Camille!
44|Leave the rest to us. We'll defeat Kuhn.
47|We can't let a scoundrel like that get away with this!
51|Well, then... I'm sorry for all the trouble I've caused...''',
38:'''5|You must be FA, the one who's been causing such a stir in the Indian Ocean lately.
8|And you are?
12|I'm with the Uddin Company.
16|I don't mean to offend, but we Muslims have long run things in these waters. We'd rather you didn't interfere.
19|What do you mean? You want us to pull out of the Indian Ocean?
22|Don't jump to conclusions. We're busy driving out the Europeans. We don't have time to deal with you as well. So...
25|I'd like to propose a joint front.
29|Leave our territory alone, and we'll give you what help we can when you run into trouble with the Europeans. What do you say?
34|...All right.
36|I can't agree to that.
44|Ha ha ha! That's more like it. I think we'll make good partners. Until next time.
52|Can't be helped, then. Our honor as Arabs is at stake. We'll defend our own waters.''',
39:'''4|H-how could I...?! Oh, my money! My company! My fleet!
8|Oh, that's Nagalpur... What's he still doing here?
11|He's no threat to us anymore. Without money, he can't do a thing.
15|Quite right...
27|Hah! All show and no substance!
34|Y-you! Argh, how dare you...!
37|The idea that money can solve everything is just a fantasy of yours. Haven't you learned that the hard way?
41|Grrr...!
45|FI is right. Cool your head for a moment.
48|Aaaah, I don't want to be poor! Somebody, money! Money! Give me money!
52|...There's really no getting through to him.''',
40:'''4|Who would have thought an island like this would have such a fine town?
8|Indeed. It will probably grow even more as a hub for trade.
12|How so?
16|There are several towns along Africa's east coast, including Sofala. But the coastline is so straight that the trade route is essentially a single line.
19|Use Madagascar as a stop along the way, though, and goods can travel by several routes between Cape Town and Mogadishu.
22|So if this island serves as a trading port, East Africa won't have just one trade route, and this town will grow too.
26|This arrangement seems familiar... Come to think of it, there's a large island a little way off Ming.
30|Ah... But that island has no port where we could trade, does it?
34|Then we'll build one. Why not?
37|You do set difficult tasks... The government won't stand by while you build a town without permission.
41|What if we told them it was sure to turn a profit? Those officials love bribes more than anything. Why would they object?
45|Oh, that sounds most interesting! Let's return to Hangzhou and get things moving.
49|Imagine a second Madagascar there... It would take a considerable investment, but in time it should become a major port!''',
41:'''4|By the way, FI, about the new town...
7|The initial plan is almost ready. The rest depends on negotiations with the government.
10|Admiral, if it's government negotiations you need, please leave them to me.
13|...Very well. You are well suited to that sort of work.
17|Oh, you'll entrust it to me? Then I have one more favor to ask...
20|Hm? What else?
24|Might you leave the town's construction to me as well?
27|Oh? You would direct the work yourself?
39|Hold on. Are you sure you can handle a job like that?
45|Surely you can't remain in Ming yourself just to devote all your time to building a town...
49|You're right... I can't. There's still so much I have to do...
53|Besides... Rumor has it the Ming government is making some suspicious moves in response to our activities.
57|What did you say?!
61|I'll find out what's going on and keep the government in check. Please continue your voyages as usual, Admiral.
64|...I see. All right. I'll leave it to you.
67|We'll need funds for construction once the negotiations are complete. Could you have about 500,000 gold ready?
70|500,000... Yes, I'll have it ready.
73|Then I'll begin negotiations at once. Please bring the funds to Hangzhou when you have them.''',
42:'''4|Admiral FI! I've been waiting for you!
7|Did the negotiations go well?
11|Of course! Everything went smoothly. Construction of Tamsui is already underway, just as you envisioned, Admiral FI.
14|Oh, so it worked out.
18|Excellent. I have the 500,000 gold ready as well.
23|That completes our preparations for construction. Do pay Tamsui a visit.
26|Of course I will.
30|The work requires a great many people. I brought plenty of workers over from England, which was all well and good, but...
33|They seem rather unhappy with the food here.
36|And?
40|I believe the best way to raise their spirits would be to treat them to some Western drink. Wine, for instance.
44|...If that will solve it. How much do you need?
47|Five cargo holds' worth should do...
51|That sounds suspicious. Aren't you just using this as an excuse to get a drink yourself?
55|...Very well. So I need to bring five holds of wine to Tamsui?
59|Yes, and as soon as possible, please. Their morale is at stake, after all. I'll head back to the town ahead of you...''',
43:'''4|I've been waiting for you, Admiral FI.
7|There's wine in storage. Let them drink their fill.
11|Thank you. I shall do just that. ...Oh, and the trading post is complete.
15|FO holds exclusive trading rights here, so you're free to use it without concern.
18|We can trade here now. That's progress. We've taken the first step.
22|Now we must work on developing the town. Invest the profits from trade back into it.
26|I want to see it grow into a much bigger town... Richard, please continue overseeing the work.
30|Certainly. Leave it to me.''',
44:'''4|Admiral FA! Welcome. I'm afraid the facilities are still unfinished, though. There's nothing ready for you yet...
7|The work seems to be moving more slowly than I expected.
10|Yes, well, without wine...
14|...We're getting nowhere like this. We'd better give them something to drink so they'll work more efficiently.
18|Quite so. Please bring five holds of wine as soon as you can.''',
45:'''4|So this is it... I've finally reached Africa, the land Zheng He visited too...
8|Come on, move it!
12|Hm?
17|Don't stop! Do you want to die?!
21|(Are those local people he's driving along? ...What cruel treatment.)
25|You there! Stop hurting them!
29|Huh? Who are you? These people belong to me. You've got no business interfering!
33|People aren't livestock. No one can own another human being.
36|They work on my plantation! What's wrong with using them however I please?
39|You're an outsider! Don't lecture me!
42|How convenient. Here in Africa, you Westerners are outsiders too.
46|...Why, you! You don't know who we are, do you?!
49|I have no desire to find out.
53|You've said enough! We're the Espinosa Company! Our name can silence a crying child! Now get lost if you want to live!
57|Was that meant to frighten me? I've heard stray dogs make more impressive threats.
60|Y-you...! You've always got an answer, don't you?!
63|I deal with pests. Parasites like you, infesting countries around the world. It's my job to get rid of them.
67|P-parasites? Pests?! Woman, if you wanted to die, you should've said so!
71|Go back and tell your boss to start thinking of a new line of work. Your business will be finished in a few months.
74|What did you say?!
78|Didn't you understand? I said I'm going to shut down this corrupt company.
82|Gah ha ha ha! You're a rare one! Are you brave, or just stupid?
85|All right! I'll drag you in myself and make you kneel before Espinosa!
89|You poor fool. A little more sense, and you might live longer...
92|You're the one who'll regret those words. The next time we meet, I won't show you any mercy. Be ready.
96|...Why, you...!
108|As decent human beings, we cannot overlook the Espinosa Company's crimes.
111|Of course. We can't let them get away with this.''',
46:'''4|[A confident young man's voice] Hm? Are you the ones who defeated Espinosa?
9|!?
13|I'm grateful. Now we English can expand into Africa without a care.
17|Espinosa seems to have made a very handsome profit here. What splendid luck.
21|...You seem to have misunderstood. I don't recall asking for someone to take Espinosa's place.
25|Why object now? Isn't it obvious?
28|The Western powers each take charge of the world outside Europe. When one falls, the next simply takes his place.
31|Are you saying the world belongs to your great powers...? How convenient for you.
35|So Europe still has plenty of shameless people who can say such things openly.
39|We won't tolerate people like you. If my subordinates find you, I can't promise you'll leave alive. Get out of here.
42|My, my. Such a beauty, and so frightening. Very well. I'll withdraw for today.
45|But I won't give up. Even if I pull out, someone else will come.
48|If it's going to be taken anyway, why shouldn't I be the one to take it?
51|...
62|Admiral, who were you speaking to? Was there some trouble?
65|...Nothing at all. Someone asked for directions, but I didn't know the way.
68|I... see.''',
47:'''4|Eek! W-what are you doing?!
15|Hm?
24|Get over here!
28|Espinosa?!
32|FA, thank you for defeating this scoundrel.
35|Y-you think you'll get away with treating me like this?!
38|Shut your mouth!
42|Gah! O-ow!
46|You've had your own way for far too long!
49|W-what are you talking about?
53|Don't tell me you've forgotten! You cheated my father out of his house and farmland! Now he and his whole household are missing!
56|My friend tried to report your crimes back home. You killed him and made it look like an accident!
60|So many people from my village have been taken away! They're forced to work all over the place with barely enough to eat!
64|I-I know nothing about it! My idiot subordinates did all of that on their own!
68|You... you bastard!
80|Unbelievable... There's no word for it but cowardice.
93|Inhuman...
102|You monster! FA, would you leave dealing with him to us?
105|Yes. I'll leave him to you.
109|You heard her! Come on! You'll pay for every last thing you've done!
112|H-help me!
116|...
121|FA...
125|Hm?
129|Please accept this.
136|What is it?
140|It belonged to Espinosa. He was searching for Africa's Proof of Conqueror too. We prayed it would never fall into his hands...
143|You're the one who deserves to rule these waters. Please find the treasure soon and bring peace and prosperity to this land.
147|Thank you. I'll do my best to live up to your hopes.
157|Look. The townspeople have gathered to wave to you, Admiral.
163|Look, Admiral. The townspeople have gathered to wave to you.
170|So different from when I was in Ming...
179|They understand how you feel, Admiral. They know you fight for them. Go on, wave back.
185|Your feelings have reached them, Admiral. They know you fight for them. Go on, wave back to them.
192|L-like this? I've never waved to a crowd before...
201|(I've never seen FI look so happy...)
207|(I've never seen the admiral look so happy...) I'm really glad I came with you, Admiral...
211|What brought that on all of a sudden? How strange.''',
48:'''5|Hey, Rafael. You'd better watch yourself.
8|You're right, Clau. But to think there's such a frightening woman pirate out there... The world really is a big place.
13|Frightening? That doesn't even begin to cover it. This FA...
17|Hm?
21|She weakens her enemies with schemes and diplomacy, then wipes them all out the moment they let their guard down. Cross her, and one life won't be nearly enough.
25|Pfft... Hee hee hee.
29|Hm?
34|Hey! You there! What's so funny?!
37|...Forgive me. Tell me a little more. What does this woman pirate look like?
41|Never seen her myself, so I couldn't say... Probably has a face like an ogre, though.
45|From what I've heard, she's got short black hair, wears black clothes and a scarlet jacket...
49|What?!
54|And a crimson rose on her chest... D-don't tell me you're...!
57|Me? I'm FI FA. Pleased to meet you.
60|Y-you're... FA?
71|Ahem! That's right.
79|E-eek! I knew it! Sorry! I mean, I'm terribly sorry! P-please spare me!
83|I had no idea you were so beautiful... Clau, those rumors must be made up...
88|Y-yeah! Someone as beautiful as you couldn't possibly be a terrifying woman pirate! Ha... ha ha!
98|Hmph. Listen to him change his tune.
108|Spare me the flattery. I am FA. Apparently I'm feared in quite a few places.
111|But my targets are people who rule by force and steal others' wealth. Are you helping anyone like that?
114|N-not at all! We make an honest living through honest trade. Right?
118|Portugal, our homeland... Once, its power reached across the world.
129|Hm?
135|Hm?
142|Spain has taken away our sovereignty, but we dream of making Portugal a country bustling with sailors again.
146|I see... So you'd like Portugal to replace Spain as ruler of the world?
150|The conquests Spain is carrying out in the New World aren't what we're aiming for.
155|Then Spain is wrong, and Portugal is right?
158|...Of course I'm not saying Portugal's old ways were right.
162|I just want goods to flow fairly between places. That way, both the people selling and the people buying can benefit greatly.
166|I hope shipping can make the world a place where people live a little more prosperously... I think that's the part we should play.
171|Rafi... You've really thought about all that?
174|Hmm. That's quite an admirable ambition.
178|...Was I being presumptuous? I'm sorry for talking so grandly.
182|No, that isn't what I meant. I was wishing all sailors thought the way you do...
194|But wishing won't get us anywhere... Oh, do you know the Mediterranean well? I'd like to hear about the situation there lately.
197|Lately? Well, let's see...
210|Spain's Valdes Fleet is by far the strongest. The Ottoman navy was nearly destroyed after losing to the Italian rulers at Lepanto.
216|Spain and the Ottoman Turks control most of the interests in the Mediterranean. Admirals Valdes and Pasha keep skirmishing with each other.
227|Hayreddin's pirates used to control the Strait of Gibraltar, the gateway to the Mediterranean...
239|Since their alliance with the Turks ended, their main forces seem to have withdrawn east. You hardly see them here anymore.
245|Since their alliance with the Turks ended, their main forces seem to have withdrawn east.
254|I see. That gives me a good picture. Thank you. May I ask for your help again? Of course, I'll help you too if you need me.
257|Of course! Especially if you're taking on those Spanish bastards. We'd help in a heartbeat! Right?
261|Yes. If we can be of any help, we'd be happy to work with you.''',
49:'''5|Hmph. Here comes another complication.
8|Hm?
19|That's Maldonado!
25|That fellow is Maldonado!
32|Maldonado...
43|He's the chief of the pirates who ravage the Caribbean.
48|He leads the pirates who've been ravaging the Caribbean.
63|Pirates...
70|What would a pirate want with me?
74|Hey, easy there. I'm not looking for a fight with you. I've already got more trouble than I can handle.
85|That bastard Escante talked me into joining forces against Clifford of England. Then, once the enemy was gone, he turned on me!
96|That bastard Escante talked me into joining forces against Clifford of England. Then, the moment he saw how tough the enemy was, he turned on me!
101|I'm caught between Escante in Mexico and Clifford of England. On top of that, that Swedish bastard had to stick his nose in!
110|Why would I make more enemies? I'd only be tightening the noose around my own neck.
113|You may not want a fight, but what if I do?
116|What?!
120|Do you think we'll let pirates roam free, disrupting shipping and making people's lives miserable?
123|Hey, I don't remember doing anything to anger you.
126|Don't you?
130|All that gold Escante sends home was taken from the people of the New World by force, wasn't it? So he can buy weapons.
133|Just because I take it off him doesn't give you any right to complain.
136|Plenty of Caribbean pirates are New World locals or people of mixed ancestry. Those riches came from our own villages. What's wrong with taking them back?
139|...That's just an excuse. You're exploiting those people's feelings, aren't you?
143|Exploiting them? Sure I am. They use my organization to get revenge and earn a living too. It goes both ways.
146|...
150|If you don't get it, fine. More to the point, why don't we join forces? You can't stand Escante's tyranny either, can you?
153|He rules people by force and takes every last bit of wealth they've built up over the years!
157|And when there's nothing left to take, he makes them work on his plantations! Can you just let that happen?
160|A Caribbean pirate lecturing me about right and wrong... I find it hard to believe you're sincere.
164|Heh heh. I just want to make money. That's the truth. But...
167|If I'm going to steal, it feels better taking from a villain. I want to see my men's happy faces and that bastard Escante choking on his own frustration.
170|...
174|Besides, the enemy of my enemy is my friend, right? What do you say? Let's join up and take Escante down.
179|...Let's wait and see.
181|That's enough!
188|Hmph... Very well. I can wait and see how things develop before deciding whether to fight you.
192|Good! We've got a deal. Leave this region to me. I'll keep that bastard Escante in check.
195|What a convenient agreement. I'll leave the Caribbean to you for now, but betray the people and I'll crush you at once. Remember that.
198|Heh heh. If you can. But you don't need to worry about betrayal.
201|...We'll see.
209|I've heard enough. I didn't come here for your excuses.
213|...Guess an outsider like you just can't understand how things work around here.
217|If you want me as an enemy, fine. But don't think you'll get your way so easily. I'll show you what Caribbean pirates are made of!''',
50:'''4|FI!!
8|Xien?
12|T-terrible news! Richard has defected to the Clifford Fleet!
16|Richard?!
24|Hangzhou--
29|Heh.
33|Heh heh... Ha ha ha ha ha!
36|At last, the time has come... The Kingdom of England will rule the world's seas!
40|FI... You went too far...
43|Had you been content to keep the wokou in check in the Far East, England might have taken you on as a useful subordinate one day...
46|You've truly angered us English...
49|With FI away from the East, this is the perfect chance to complete the plan we've spent years preparing...
53|You have nowhere to return to now. I'm to be appointed governor-general of East Asia! Heh heh heh...
57|I did enjoy our time together, my beautiful admiral.
60|Clifford... You may look forward to good news.
76|Clifford's forces have taken control of most of the trading rights in mainland Ming!!''',
}


def main():
    assert not OUT.exists()
    source = load(MEANINGS)
    assert source['all_clean_source_meanings_saved_before_current_conversation_English'] and source['current_English_unconsulted']
    indexed = {}
    for block,text in DRAFTS.items():
        parsed = [line.split('|',1) for line in text.strip().splitlines()]
        for key,draft in parsed:
            identity = (block,int(key));assert identity not in indexed
            indexed[identity] = draft
    assert len(indexed) == len(source['records']) == 286
    rows = []
    for original in source['records']:
        row = deepcopy(original);draft = indexed.pop((row['block'],row['source_record_index']))
        assert draft and draft.isascii() and draft == draft.strip()
        assert not any(s in draft for s in ['\n','\r','\t','{LB','{PAD','{ALIGN'])
        body = bytes.fromhex(row['source_hex'])
        if row['kind'] == 'ordinary-speech':body = body[1:]
        macros = dict(Counter(re.findall(r'F[A-Z]',body.decode('cp932'))))
        assert dict(Counter(re.findall(r'F[A-Z]',draft))) == macros,(row['id'],macros,draft)
        if (row['block'],row['source_record_index']) == (48,227):
            row['source_gloss_refinement'] = dict(previous=row['source_meaning'],
                reason='一家 denotes Hayreddin’s pirate band here; no biological kinship is established.')
            row['source_meaning'] = 'He says Hayreddin’s pirate band had controlled the Strait of Gibraltar, entrance to the Mediterranean.'
        row.update(independent_English_draft=draft,localized_draft_pending=False,source_macros=macros,
            independent_draft_precedes_current_English_intake=True,current_English_comparison_pending=True,
            no_blanket_historical_English_unexposure_claim=True)
        assert not any(row['review'].values())
        rows.append(row)
    assert not indexed
    save(OUT,dict(records=rows,records_count=286,complete_exchanges=14,
        translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_meanings_andlogical_drafts_all_saved_before_current_conversation_English_intake=True,
        current_English_unconsulted=True,all_five_gates_pending=True,
        contextual_comparisons_names_terms_consumers_andfresh_display_pending=True,
        source_gloss_kinship_clarification_not_new_story_fact=True,
        native_default_name_assumptions_not_used_to_shorten_prose=True,
        new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [MEANINGS,ROOT/'clean_source_packet.json',Path('docs/glossary.md'),Path(__file__)]}))
    save(ROOT/'clean_draft_qualification_v1.json',dict(source_objects=286,complete_exchanges=14,
        source_meanings=286,independent_drafts=286,current_comparisons=0,
        all_source_bindings_andnative_macro_counts_exact=True,macro_occurrences=dict(sum((Counter(r['source_macros']) for r in rows),Counter())),
        kind_counts=dict(Counter(r['kind'] for r in rows)),
        all286=str(OUT),all286_sha256=digest(OUT),all_five_gates_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed286 independent logical drafts/14 exchanges;all21 native substitutions exact;current dialogue unconsulted,zero credit.')


if __name__ == '__main__':main()
