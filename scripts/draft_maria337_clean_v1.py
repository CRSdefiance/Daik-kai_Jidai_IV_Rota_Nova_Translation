"""Independent paragraphs from sealed clean meanings; no current-English input."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.meaning_maria337_clean_v1 import ROOT,CONTEXT,key
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

DRAFTS={
125:'''4|Ah, Admiral FA!
7|Escante was plotting a coup to break away from Spain. Thanks to you, we stopped it before it could happen.
10|There's one thing that still concerns me, though.
14|?
18|I've heard that someone recently took the key to the treasure Escante was after to the west coast of the New World.
22|Could it be... the map to the Proof?
25|The western New World... This won't be easy.''',
126:'''4|By the way, FI, wouldn't the Ceremonial Knife fit perfectly in the Sun Emblem Sheath?
8|Now that you mention it, they are the same size.
12|Perhaps they originally belonged together. Let's try putting the blade in the sheath...
15|Good heavens! What is this?!
21|It's blinding! ...What did you do, Xien?
25|I don't know... The sheath suddenly started shining... It's safe to open your eyes now.
29|Oh? There's a map on the blade. When did that get there?
33|What in the world...?
37|This is... the map to the New World's Proof of Conquest!
40|Putting the knife in its sheath made a map appear...? I can't make any sense of it.''',
127:'''4|Don't give me that! I'm no pushover!
7|Suit yourself! You're fired!
12|Fine. You want me gone? I'm out of here.
15|Oh dear... It's never pleasant watching someone get fired.
18|Did you see the build on that man?
22|An impressive set of muscles, certainly. But he has quite a temper. Trouble must follow him everywhere.
26|Wouldn't you say handling difficult men is part of being a good leader?
29|You've got confidence, I'll give you that. ...Wait, are you FA? I'll warn you now: he won't be easy to handle.
32|What about his fighting skills?
36|Well, I've never seen him lose a fight.
39|Oh?
43|Then there's no problem. Come on, Xien. Let's catch up with him.
47|There he is.
51|You want something?
55|I'm offering you a job.
59|A job? You want to hire me? ...Who are you?
62|You could call me the admiral of a private fleet.
66|Wait... You're Admiral FA?
69|You've heard of me. That makes this easier.
72|We're going up against some powerful Western enemies. I need strong fighters. You'll join my ship, won't you?
76|Western enemies...? Are you serious?
80|Oh, are you scared? Perhaps I misjudged you.
83|Hah! Sounds interesting! All right, I'll help you. Just don't underestimate what I can do.
87|That's reassuring. We haven't heard your name yet, though.
91|I'm Al.
95|Welcome aboard. I should warn you, I have no patience for men who are all talk. I'm counting on you.''',
128:'''4|Whoa, sorry about that!
8|...?
12|What's wrong?
16|That man must have dropped this... A pendant? There's a woman's portrait inside...
21|Someone dear to him, no doubt. His sweetheart, perhaps...
24|Then let's give it back.
29|Mamma mia! My dear sister! I've lost my pendant!
32|It's gone! Gone! I can't find it anywhere!
35|Admiral, that's him. Over there.
39|My pendant! Where did it go?!
42|You there! Compose yourself! Is this what you're looking for?
46|My sister! My pendant!
50|Your sister? The woman in this picture is your sister?
53|That's right. Thank you. She's very dear to me. She's missing, and I'm trying to find her...
57|I see. I hope you find her...
62|If you're an admiral, you must be a sailor, right? Hey, how about hiring me? I've sailed a few times. I'll be useful!
65|Please, I want to find my sister. I don't know where she is, but she must be somewhere in this world!
69|What will you do, Admiral?
73|...Well, perhaps we met for a reason. All right. You're hired.
77|Mamma mia! Wait for me, sis! I'm Angelo Puccini. Glad to be aboard!
80|I'm FI FA. I'll be counting on you, too.''',
129:'''4|...Admiral, there's something I need to tell you.
8|Oh? Of course...
12|Then perhaps the rest of us should leave you alone...
16|Xien... No, I want all of you to hear this.
19|Very well.
23|It's about my sister, Bianca...
27|We did say we'd help you find her.
30|No, that's not it.
34|...Bianca... She's gone.
38|Gone...?
42|Bianca was the only family I had. She died of an illness three years ago...
45|She died...? Then why did you say you were looking for her...?
48|When Bianca died... I couldn't accept it...
52|I convinced myself she'd gone missing. I searched all over the world...
55|Angelo...
59|When I collapsed with that fever...
63|My sister told me you were my family now... And that I should live for myself...
66|...
70|She sounds like a good sister... She truly cares about you.
74|As long as you're alive, you must keep living. For your sister, too.
78|That's right, Angelo. Don't make her sad. She's right. We are your family.
82|Yeah... Thank you. I hope you'll keep putting up with me.
85|And you with us.
89|...Bianca... I'm sorry. From now on... I'll live for you, too.''',
130:'''4|My usual order of cinnamon, please.
8|(Someone's already here?)
12|You got it. Here's the price.
16|Oh? You've raised your prices.
20|Have not. That's what I always charge.
23|Ha ha! Don't be silly, Adil. You think I don't know what you paid for it?
26|Now, come on...
30|Given this year's harvest and the demand around here, I'm sure you can do a little better.
34|I could always try somewhere else. There's no law saying I have to buy from the same shop every time.
38|Ugh... All right, all right. I can't win with you.
42|Hm? ...Adil, are you running a fever?
45|What now, Carlo? Still finding fault with the way I do business?
48|That's not what I mean. You've got a fever. Get to bed early tonight.
51|Oh, stop... Huh? I really am getting the chills.
54|You see? I'll do my shopping tomorrow. Close up for the day.
57|Hmm... I'll take your advice. Sorry, you folks over there. You'll have to come back tomorrow, too.
63|I'm sorry about that. You came here to trade, too, didn't you?
66|How did you know he was ill?
70|His color was off.
82|Hmm. His powers of observation might even rival mine.
88|Really...? He didn't look that bad to me...
92|Most people wouldn't notice. I'm rather sensitive to people's health.
96|(Well...)
100|Would you come back to the trade house with me tomorrow morning? I think I can make up for today.
103|Yes, let's do that.
107|Carlo! Thank you for yesterday!
111|How's Adil?
115|Home in bed today. Better safe than sorry.
118|I see. I hope he's better soon.
122|That man never listens to a word I say. If you hadn't spoken to him yesterday...
126|Oh, listen to me going on. You're a lifesaver. I wanted to thank you.
130|Thank you. I appreciate it, but thank these travelers instead. They had to put off their business overnight.
134|Oh dear, I'm sorry we held you up. It's not much, but... would you take this?
140|Thank you, ma'am. You folks are in a hurry, aren't you? Go ahead and do your shopping first.
144|Hey, Carlo! Sorry about yesterday!
147|You!
151|Adil! You're supposed to be resting!
154|Hmph! I'm as fit as ever. On a fine day for business like this, you won't catch me lazing around in bed!
158|You're impossible!
162|Ha ha! I'm glad you've got your energy back, but don't overdo it today.
166|I'll stop by another day. Take care of these folks for me.
169|Take good care of your family and your health, travelers. I'll be seeing you.
172|...
177|...Wait.
181|Hm?
185|Carlo, was it...? How would you like to put those business skills to work aboard my ship?
189|Now, hold on. Where did that come from?
193|It isn't sudden. I've been thinking about it since yesterday.
196|I'm no sailor. I'm just a merchant.
199|Then you know the markets, don't you? A fleet needs people with a head for business, too.
203|...
207|Don't you want to go to sea alone? Or is it that you don't want to leave your family?
210|My family... They're gone. They died a year ago.
213|...
218|First my daughter caught an illness that was going around. I was so absorbed in my work... I didn't take proper care of her.
221|By the time she got treatment, it was too late. My wife caught it, too... I lost them both.
225|I'm so sorry...
229|The work I'd neglected my family for felt empty after that... Ever since, I've cared more about people's health than business.
232|Oh... So that's why you were worried about the shopkeeper...
236|...What about going home?
240|To Venice? Too many happy memories there. I couldn't bear living there alone.
244|...
248|If you don't want to go back to Venice alone, come with us.
252|?
256|When you share a life aboard a ship, you're practically family. A new family might not be such a bad thing.
260|You... You're saying you'd be my new family?
264|If you'd like us to be.
268|...Thank you. I'd be happy to sail with you.
271|My name is Carlo Cinato. I look forward to working with you.''',
131:'''4|Perhaps I've had a little too much to drink...
8|I've had quite a lot myself. Oh...
13|The music's changed... We don't hear anything like this back home.
16|This tune... Excuse me a moment...
19|What is it...?
24|[Patron 1] Wow, look at her!
27|[Patron 2] Yeah! She's beautiful, and she can dance!
32|How wonderful...
36|[Patrons 1 and 2] Bravo! Bravo! Braaavo!
39|[Applause]
43|I couldn't resist dancing... I love this tune.
46|That was beautiful... We don't have such passionate dances in the East.
49|Oh, this is called flamenco.
52|I'd love to see you dance again.''',
132:'''4|Whoo! That's Calicut for you! It's hot!
15|Oh, this won't do. This sort of heat doesn't agree with my constitution...
20|Hmm. It certainly is hot.
27|The scenery's quite different this far from home.
30|Hey, Admiral! They're selling something over there! Looks delicious!
34|Jam, wait a moment... Ah, he's gone already.
37|Honestly...
41|Admiral! Heeelp!
44|Hm? Was that Jam?
47|That's not something you hear from him often. What's happened?
58|Did he eat something strange and upset his stomach?
65|Oh, Admiral! Sorry! I can't believe I let this happen... This weird kid's got me...
70|Oh, are you the admiral? He lost a bet to me. He's mine now.
74|Who is this boy?!
78|Yours...? What do you mean?
82|He's a peddler. He said he'd throw in a little extra if I won a coin toss, so...
86|And you lost... But how does that make you his?
90|Oh, that. He promised to do anything I said if I tossed heads ten times in a row.
93|Nobody gets ten heads in a row! Not normally! Damn it, I can't believe this!
97|But I did, didn't I? Heh heh.
100|...Let me see that coin.
104|Huh? N-no!
107|Hm? That's suspicious.
111|You cheated, didn't you?! Give me that!
114|Aaah!
118|!
122|Aw, you caught me.
126|You've put two coins together. Heads on both sides.
130|Damn it! You little brat! You tricked me!
133|Heh heh. Sorry.
137|You think sorry's going to cut it?!
140|Then how about we say I lost that bet instead...?
143|And what do you propose to do about it?
147|Take me with you! I'll do anything!
158|What a brazen way to ask...
172|Hmph! What use could someone so impertinent possibly be?
175|(You're one to talk...)
181|...The nerve of him. I'm speechless.
187|You're travelers, right? I can do all kinds of things. I'll be really useful!
191|Yeah, I like that! I'll work you to the bone! ...Is that all right, Admiral?
195|...
199|Of course it isn't.
203|Pleeease, Admiral!
207|Come on, Admiral, please! ...Hey, why are you asking, too?!
210|I've had enough of elephants! I want to see other countries! I mean it. I'll do anything!
214|...All right.
218|Y-yes!
222|FI! Are you sure about this?
225|Yes. Anyone who can run rings around Jam has some talent. We may have found a real gem.
229|...Wait. Did this kid just use me? Damn it!
233|Yes! I get to go somewhere new! I've never been on a ship before, either. I'm Samwell. Nice to meet you!
238|...Welcome aboard.
242|Hmm... He still looks like dead weight to me...''',
133:'''5|Doesn't look like they're back yet.''',
134:'''5|Doesn't look like they're back yet.''',
135:'''4|Hey! Hey!
8|Eeek! I require immediate assistance!
18|W-what's that?!
24|What's going on?!
31|Someone's being beaten over there!
35|He doesn't look as though he could put up much of a fight... Shall we help him?
39|Yes.
51|Attacking the weak is unforgivable! I shall join you!
68|Are you all right, young man?
72|Ow, ow... Not... terribly all right, I'm afraid.
76|Why were you fighting those men?
88|Did they pick a quarrel with you? It seems every country has its villains...
95|Well, you see...
99|?
104|They were claiming that the Earth is flat...
107|...And what of it?
111|The Earth is round! That is common knowledge now! I thought I ought to correct their mistaken understanding.
114|...And then?
118|I began to explain. At once, they started behaving most strangely.
122|They suddenly scowled and said, "Who asked you?" Then they started hitting me...
126|Hmm? I'm still not sure I understand.
129|Nor do I, I'm afraid...
133|All I said was, "To put it plainly, you're wrong!" And then...
137|...They got angry.
141|Wh-what?! How did you know?!
144|...I think anyone could have worked that out.
148|Really...? I'm afraid I still don't understand.
151|What they knew was wrong! I corrected it for them! Surely they ought to have thanked me!
154|I would be grateful to anyone who taught me! It means one more truth about the world has come to light!
166|Hmm. It seems every country has its eccentrics, too.
172|A thirst for knowledge is a fine thing, but...
176|...
180|Do you know anything about ships?
184|Ships? Of course! I was once a captain, in fact. Refitting ships was a hobby of mine!
195|This man was a captain?! ...I can scarcely believe it.
202|...I see. Then I don't see a problem.
205|?
216|Admiral... Surely you don't intend to take this man aboard?
222|Surely you don't mean to take him aboard, FI?
229|Yes. I like his curiosity. Besides... with that personality, I doubt he finds ordinary life easy.
241|That much is certainly true...
255|Honestly... The admiral chooses the strangest moments to be kind.
260|Honestly... She can be softhearted in the strangest ways.
266|Um...
270|Oh, I'm sorry. We left you out of the conversation. What is it?
273|Um... Are you an admiral?
276|Indeed. Have you heard of FO?
280|Then you're... Admiral FI FA...?
284|You've heard of me? That makes this easy. Would you like to work for me as a navigator?
288|Yes! Most certainly! Please allow me to sail with you!
291|Then it's settled. Your name?
294|Cesare Toni! Thank you very much indeed!
297|Hmm. What does the admiral see in him? I don't understand...
309|A mystery indeed...
321|Now then, if I may...
325|When you're still signing contracts and expanding your routes, you don't need new ships yet. A 1 percent share only lets you buy one to five units of goods.
328|Once your shares grow and you can buy more goods, it's time to buy ships.
332|The first things to consider are a ship's size and price.
335|Choose a ship to suit your shares and funds. Otherwise, you'll need more sailors without being able to buy enough goods to fill its hold.
338|A ship's price tells you its size. Under 5,000 gold is small; 10,000 to 20,000 is medium; over 50,000 is large.
341|Small ships are very cheap. Even with limited funds, you can easily increase the amount of cargo your fleet can carry.
344|Once you've traded for a while and have money to spare, replace them with medium ships.
348|Medium ships have either two or three masts. Three masts are faster, of course, but need more sailors to work the sails.
351|With refitting, you can have up to five cargo holds. If you don't intend to fight for a while, you won't need marine quarters or gun decks.
354|If you want to open routes to distant towns, add more supply holds. You'll be able to sail much farther.
357|If you're going to take on another power, however, you'll need large ships.
360|At least your flagship should have marine quarters and guns. You'll have a hard time winning naval battles without them.
363|The rest depends on your funds. Two medium ships cost less than one large ship and can carry more goods.
366|You'll eventually replace them with large ships, but if you plan to form local fleets, you may want to keep your old medium ships rather than sell them.
369|That concludes my advice. I shall begin preparations for departure. Until then!''',
136:'''10|Now that you're here, you've got to play.
15|A new face, eh? How about a little wager? The loser buys a drink. It's just a simple game.
19|Here are some coins. We take turns taking one, two or three. Your choice.
23|Whoever takes the last coin loses. Simple, right? Here we go.
SC3_B136_CHOICE_356_0|I'll play.
SC3_B136_CHOICE_356_1|No, thanks.
46|I'll take that drink, then.
50|...Ah, that's good. Thanks. See you around.
59|Damn, you got me. Been a while since I lost. Here you go.
69|You've still got a ways to go... Oh, I don't need a drink. Were you really that confident in your gambling?
73|Sure. Gambling takes a sharp eye and good luck.
76|I've got both. You could say I was born to gamble.
80|Luck aside, a sharp eye, you say?
84|Better not judge a man by his looks.
88|For instance... That couple over there. We can't hear them, but what do you think they're talking about?
91|A marriage proposal, perhaps?
95|Come on, this is easy. They're breaking up.
99|?
103|Just watch.
107|I've heard enough! I can't put up with the way you think anymore! You're so selfish!
110|You're free to think that. But I think you're the selfish one.
113|Oh, really? Then perhaps we shouldn't see each other anymore.
116|If we both feel that way, this is goodbye.
119|...
123|Well? I was right, wasn't I?
127|I'm impressed... How did you know?
131|She had her fist clenched under the table. She was holding back her anger. That's no way to talk about love.
135|And he never looked her in the eye. Does that look like a man sitting across from the woman he loves?
139|I'm impressed. You noticed all that?
143|Sure. With an eye like mine, I can read my opponent's hand.
146|Add my luck to that, and I win.
149|Quite a talent. How about putting it to the test with FO?
153|Whoa, that's a sudden offer.
157|...Well, I've got time on my hands. I'll toss this coin. If it's heads, I'll join you.
163|Never mind the drink. Come join FO already.
167|That again? ...All right, let's ask the coin one more time.
192|Hah. I won't put my life in the hands of someone with no luck. See you.
208|Hah. That settles it. I'll stake my life on you!
211|The name's Fernando Dias! That's luck for you!
214|I'll be counting on you.
228|Things have been pretty lousy lately.''',
}

NOTES={
(125,7):'Independence was a thwarted coup objective; do not turn the warning into a successful secession.',
(125,18):'Keep the report as hearsay and the person unidentified; do not identify the treasure key with certainty.',
(126,37):'The regional map, not the Proof itself, has been discovered. Item labels await exact binding.',
(127,62):'Private fleet is explicit; no official commission, national service or additional rank is invented.',
(128,21):'Sweetheart is a tentative mistaken guess, corrected by the sister revelation.',
(128,53):'This scene presents Angelo as searching for a missing sister. Do not anticipate the later death revelation.',
(129,16):'Use Xien in the familiar address; no grandfather relationship is implied.',
(129,42):'Preserve only family, illness and exactly three years. Later crew-as-family language is explicit in source.',
(129,63):'Keep this as Angelo reporting his sister\'s words; do not decide whether it was a dream, apparition or physical meeting.',
(130,218):'Preserve epidemic illness and neglect of care; do not add a diagnosis or a deliberate refusal to seek treatment.',
(130,221):'Keep delayed treatment and transmission to the wife without inventing a medical mechanism.',
(130,240):'Happy memories make solitude painful; do not change Venice into an unloved home or an invitation to forget his family.',
(131,39):'English stage cue preserves the source\'s applause, with no new native sound effect or speaker.',
(132,90):'Exactly ten consecutive heads and a promise to do anything, not a cash stake or real ownership contract.',
(132,126):'Two coins are physically stacked to create heads on both sides; retain the method rather than an unexplained lucky coin.',
(132,210):'Keep elephants without inventing his occupation or the reason for his boredom.',
(133,5):'Neutral singular/plural they preserves the absent referent and uncertain report; exact source caller still needs contextual binding.',
(134,5):'Identical wording is independently source-supported, not duplicate completion credit.',
(135,133):'His blunt correction sets up Maria\'s deduction; keep the self-important phrasing and unfinished thought.',
(135,184):'Past captain experience and ship refitting are explicitly supported despite the comic disbelief.',
(135,325):'Preserve 1 percent and one-to-five goods capacity; use percent as a word. Exact goods/UI unit remains provisional.',
(135,338):'Preserve all three stated ranges without filling the price gaps or inventing a new classification.',
(135,348):'More masts require more sail crew, not helmsmen or marines.',
(135,351):'Preserve maximum five cargo spaces and the conditional noncombat advice. Final room labels await source/UI binding.',
(135,363):'The two-medium versus one-large price and cargo comparison is explicit, not a generalized balance recommendation.',
(136,19):'Retain alternating one-to-three coin choices without inventing the starting total or first player.',
(136,107):'The couple\'s quarrel supports a breakup but does not establish marriage, age or family roles.',
(136,157):'Recruitment is conditional on heads; success and failure remain separate native branches.',
}

def parsed(number):
    rows={}
    for line in DRAFTS[number].splitlines():
        k,v=line.split('|',1); k=int(k) if k.isdigit() else k
        assert k not in rows; rows[k]=v
    return rows

def main():
    target=ROOT/'all337_independent_drafts_v1.json'; assert not target.exists()
    path=ROOT/'all337_clean_meanings_v1.json'; meanings=load(path)
    assert meanings['source_meanings_sealed_before_independent_drafts'] and meanings['no_current_story_English_read']
    rows=deepcopy(meanings['records']); assert len(rows)==337 and set(DRAFTS)==set(CONTEXT)
    drafts={n:parsed(n) for n in DRAFTS}
    for number,values in drafts.items():assert set(values)=={key(r) for r in rows if r['block']==number},number
    for row in rows:
        number,index=row['block'],key(row); english=drafts[number][index]
        assert english.strip()==english and not any(t in english for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert english.isascii(),row['id']
        assert sorted(re.findall(r'F[IAOU]',row['source_Japanese']))==sorted(re.findall(r'\bF[IAOU]\b',english)),row['id']
        row.update(english=english,independent_English_draft=english,whole_exchange_context=CONTEXT[number],
            independent_clean_first_draft=True,independent_draft_pending=False,current_English_comparison_pending=True,
            localization_note=NOTES.get((number,index),'Natural American paragraph from the sealed clean meaning and complete exchange; exact names, terms, contextual comparison and display approval remain pending.'),
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
            natural_dialogue_policy='natural-dialogue-v2',target_locale='en-US',new_credit=0)
    save(target,dict(records=rows,source_objects=337,complete_exchanges=12,source_meanings=str(path),source_meanings_sha256=digest(path),
        current_English_not_consulted=True,whole_clean_exchanges_read_before_drafting=True,all_five_review_gates_pending=True,
        source_controls_and_future_automatic_layout_not_authored_in_prose=True,explicit_pending_term_bindings=meanings['explicit_pending_term_bindings'],
        unresolved_contexts=meanings['unresolved_contexts'],new_credit=0,
        evidence={str(p):digest(p) for p in [path,Path(__file__)]}))
    print('Saved337 independent drafts across12 complete exchanges; current-English comparison, names/terms andall five gates remain pending.')

if __name__=='__main__':main()
