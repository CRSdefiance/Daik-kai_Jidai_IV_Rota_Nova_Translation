"""Draft logical American English from sealed meanings before current-English exposure."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.meaning_maria335_B137_B151_v1 import ROOT,CONTEXT,key
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

DRAFTS={
137:'''4|Life's been rather dull lately...
9|Ah, that fellow looks like an old hand.
12|More old than old hand, I'd say.
15|You two have a lot in common. Why not have a drink together?
18|And just what is that supposed to mean?!
22|Ho ho! You're lively for an old fellow.
26|What?! I'm still young! You must be enjoying your retirement by now.
30|Retired?! I'm still an active navigator! I can hold my own against any youngster!
34|Oh? Big words from an old man!
38|See? Two of a kind...
42|Don't get so worked up, Xien... Forgive me, but did you say you were a navigator?
46|Indeed. Julio Erneco, at your service. And you... Would you happen to be Admiral FA?
50|I'm honored you've heard of me. Would you be interested in my ship?
53|Of course! Now... Is that an invitation to join your crew?
57|You may take it that way.
61|The admiral has some peculiar tastes...
73|You're one to talk...
80|Well, if that's what FI wants, I won't object...
84|Very well. Once we're sailing together, we'll see which of us is the old man. Though the answer's obvious...
87|Of course. I'm clearly the younger one.
91|Now, now. I'm counting on both of you.
95|So, the old-timers are teaming up! This should be fun!''',
138:'''4|FI, someone seems to be standing near our ship.
9|...A magnificent ship. But...
12|What are you doing here?
16|Admiring the ship. Standing beside her like this, I can almost hear her heartbeat...
20|But this ship... Oh! Could you be Admiral FA?
23|Yes. But you were saying... What's wrong with the ship?
26|She doesn't seem to be getting all the care she needs... Show her a little more love, or you'll make her cry.
30|A ship that cries? How poetic.
33|Who are you?
37|My name is Manuel. I used to be a navigator. Forgive me for speaking out of turn...
41|He's right about the maintenance. It takes a skilled eye to see that at a glance.
45|You clearly have knowledge, experience and a deep love of ships.
48|You seem so fond of ships. I can't imagine why you stopped sailing. Would you mind telling me?
52|I'm sorry... That was a long time ago...
56|Then let me ask something else. Would you consider returning to sea? To life aboard a ship?
59|Do you mean...?
63|I'd like you to look after my ship.
66|...
70|What do you say? Only if you want to, of course.
74|...Thank you. Being close to ships is what I live for. I would be delighted to come aboard.
78|Now then, Admiral. Would you like some advice on refitting the work rooms aboard your flagship?
SC3_B138_CHOICE_1274_0|Please do.
SC3_B138_CHOICE_1274_1|No, thanks.
93|Very well. I'll focus on the rooms that help you prepare for long voyages.
97|Assign people with high Persuasion to the Adjutant's Room and Chapel. They can ease discontent among the sailors.
101|People working in the Galley and Livestock Room can reduce the fleet's consumption of water and food.
105|A ship's doctor in the Infirmary can treat fatigue, disease and injuries among your companions and sailors.
109|Sick or injured navigators will recover faster if you assign them to Private Quarters or the Recreation Room.
113|A ship's carpenter like me can repair damage at sea in the Timber Room. I can also help refit and repair ships at shipyards.
116|That was a rather hurried explanation... Was it helpful?
119|The fleet's fate rests on your judgment, Admiral. Be thorough when refitting your ships. Don't neglect it.
125|I see. Then I'll leave it to you.''',
139:'''4|Oh, are you here to see old Mikhail too?
7|Old Mikhail?
19|Wh-what?! Mikhail?! No, no, this is bad! Don't go near him, FI!
25|Oh, you're not? He's famous around here for knowing just about everything.
29|Shall we meet him, FI? He might be able to help us.
32|Yes, let's.
36|Though you might want to stay away if you've got women with you...
47|Exactly! You'd be much better off staying away!
53|?
57|That must be Mikhail.
61|Oh, you're amazing!
65|Indeed I am! Ho ho ho!
68|Then what's this? Tell me!
72|Ah, that's a peppercorn. It's the fruit of a tropical tree. Grind it up, and you have a spice.
76|It should grow well around Brunei. It could make a very useful trade good.
80|...Hmm? On second thought, that's a rabbit dropping. Filthy thing!
84|Eww! Throw it away!
88|All right, all right. Away it goes!
92|You really do know everything! How did you learn so much?
96|Well, I am a genius. Few can match my knowledge. I could even guess your bust size, my dear.
100|Oh! You dirty old man!
104|Ho ho ho!
108|...His manners aside, he does seem learned. Shall we ask him to join us?
112|...Yes, I suppose so.
116|Wh-who are you people?
120|Your knowledge impressed me. We would be honored to have your help at FO.
124|Join you? I've no intention of leaving this town. And I certainly won't accept an invitation from a man.
128|Please reconsider. We could use your help.
131|Well, even so... Oh!
134|You there, young lady. What's your name?
137|Our admiral, FI FA.
140|FI, eh?
144|Oh, yes. Very nice indeed!
148|?
152|I've decided! I'm coming with you! It's settled!
155|FI, my dear!
159|I'll follow you anywhere!
163|What?!
167|FI, are you all right?! How dare he!
170|No, no! My mind's made up! I'm going with you! I'll put all this knowledge to use. There's nothing to worry about!
173|We did invite him first. I suppose we'll have to see this through. Xien, let him aboard.
177|But this shameless old man...
181|Shameless?! It's just a friendly gesture!
184|You Easterners may not understand, but in the West, it's how we show friendship and affection!
187|I'll pass...
195|Mikhail is a scholar, not a navigator. He cannot be assigned to a position on deck.
199|With Mikhail aboard, you can now view detailed information about items.
202|Try pressing X while an item's information is displayed.
205|I can't help with the ship, but I look forward to joining you. Call on me whenever you want to know about an item.''',
140:'''6|Halt! Who goes there?!
10|Eek!
14|...What is it? What's happened?
18|This person has been following us. But...
22|I had not expected a girl like this...
26|Hey, let go of me!
30|Let her go, Yukihisa. ...Why were you following us?
33|I wanted to ask you a favor.
37|You're with FO, right? Take me aboard your ship!
41|What an abrupt request. Has no one taught this girl manners?
45|...You can't just appear out of nowhere and demand a place aboard. Do you have a reason?
49|I want to travel the world! I'll train wherever I go, get stronger and show my master what I can do!
52|Training, you say? What discipline do you practice?
56|I'm glad you asked! Let me show you my Taoist arts!
59|Taoist arts?
63|Ready your sword! Here I come!
67|Hm!
71|Hyaaah!
75|?
79|(? Nothing seems to have happened...)
82|You're wide open! Hah!
87|Whoa!
91|Hey, nice dodge! That was my paralysis spell!
94|Paralysis? I thought I had simply let my guard down...
97|Hehe! Mysterious, isn't it?
101|Impressive. Closing on Yukihisa that quickly is an achievement in itself.
105|Your footwork and sense of distance... Those come from martial training.
108|...Are you serious about going out into the world?
112|I want to prove my master wrong! ...Please! Take me out into the world!
116|...Wanting to prove someone wrong can help you grow. What's your name?
120|Yifa!
124|Yifa, if you come aboard my ship, you'll work like everyone else. Don't expect special treatment.
128|Just what I wanted!
132|My name is Yukihisa. You won't catch me off guard again!
135|Hehe! Think you can beat my Taoist arts?''',
141:'''9|...Admiral...
13|...
17|...FI...
21|...Hm?
25|Forgive the sudden intrusion. I mean you no harm.
28|We have not met. I am Sang Hyeon, Yifa's senior in our school.
32|I learned that you would be taking Yifa into your care. I came to pay my respects.
36|Yifa's...?
40|I am ashamed to say it, but her unruly ways are entirely the fault of my inadequate guidance.
43|Leaving the mountain without our master's permission to escape her training was inexcusable. Leaving the country was worse still.
47|She does not know this, but our people are forbidden to leave the country.
51|Then you've come to take Yifa back?
54|Even if I wished to, I could not. Breaking that law is a grave offense. Yifa has been expelled from our school.
57|I no longer have any ties to her...
60|Yet we grew up together, as close as a brother and sister.
63|She is still so immature. I cannot stop worrying that she will cause trouble for others.
67|I know I have no right to ask, but please guide Yifa. Do not let her stray from the right path.
70|And...if possible, see that she continues training, even away from the mountain, and follows our master's teachings...
73|Please. Take good care of Yifa.
76|Was that...a dream? It felt so real...
79|Good mooorning! Hey, let's hurry up and leave...
82|Oh!
86|What's wrong?
90|I can sense Sang Hyeon...!
94|The man you trained with? His name is Sang Hyeon?
97|What?! You met him?
100|No... Someone appeared in my dream, said he was your senior fellow student and gave me that name.
104|A dream?
108|...Sang Hyeon...
112|I see... He can't leave the mountain, so he used his arts to visit...
116|His arts...? (I see...)
119|Oh, yes. He asked you to keep training, even away from the mountain.
123|Oh, Sang Hyeon... Hehe. He never stops worrying about me.
127|...Is something wrong?
130|I'll train hard! I can't let Sang Hyeon down!
134|I'll expect that same effort in your work aboard the ship.
137|I know, I know!''',
142:'''6|Mihwa, I live for that radiant smile of yours.
10|Oh, Julian...
14|Working in a tavern must be exhausting if you have to deal with men like that every day...
17|H-huh? This is where you usually smile. Don't you like me anymore?
21|...No, that's not it. Your words usually cheer me up, but...
25|There's something I want so much. Lately, it's all I can think about, day and night...
29|Oh, Mihwa. That sad face doesn't suit you. What could you want so badly?
33|It's called the Silla Gold Crown. Doesn't that name sound mysterious? They say it's incredibly rare.
37|Sounds expensive... I wonder if I can afford it. Where do they sell it?
40|That's the thing... Apparently, you can't buy it in a shop. I heard it's somewhere in Seoul.
43|You can't buy it in a shop? ...Oh! Of course! It must be there!
46|Oh, do you have a lead?
50|Leave it to me! I'll get that Silla Gold Crown and bring back your smile in no time!
54|Your smile is what keeps me going! Oh, and once I get the crown, you'll go on a date with me, right?
57|You haven't even found it yet! Getting ahead of yourself, aren't you? All right. I'll think about it.
61|Yes! Don't forget your promise! I'm off to Seoul!
64|I'll be waiting... Oh. He's already gone...
67|That was an interesting conversation...
71|Oh, you heard? Well, a man like him might be just your type.
75|...Unfortunately, it's the Silla Gold Crown that interests me. Not the man.
79|Oh... Yes, that does make more sense. So, do you have a lead on the crown?
82|None at all. Would you mind telling me what you know?
86|I only know it's in Seoul. And that it's absolutely beautiful.
90|I see... If I have a chance to visit Seoul, I'll look for it too.
94|Oh, really?! If you find it, you have to show me!
97|If I find it. But I think you'd do better to pin your hopes on that man.''',
143:'''5|Welcome.
9|Someone in a tavern might know...
12|Excuse me. Does anyone here know about the Silla Gold Crown?
16|Oh, I do, but...
20|I'm trying to find it. Could you tell me where it is?
23|Hmm... I'm not sure...
27|Do you charge for information?
31|No, it's not that... Someone just asked me the same thing. A very flighty sort of man.
35|That must be Julian, the man I met in Hangzhou...
39|Oh, you know him? And who are you...? Oh!
42|?
46|Could you be FI of FO?
50|Yes, I am...
54|W-well, they say the Silla Gold Crown is in the ruins called the Tomb of King Muryeong. That's all I know...
58|I see. I'll go and have a look. Thank you.
61|N-not at all...
65|(FO's influence can be rather troublesome...)''',
144:'''5|Oh, FI...
9|When did you two meet?
13|Mihwa, the truth is, she found the Silla Gold Crown. She was kind enough to give it to me.
17|So this is the Silla Gold Crown... Look at that gleaming gold! Oh, it's breathtaking...
21|And now it's yours, just as I promised!
25|Oh, it's wonderful! I'll treasure it forever! Thank you!
28|I'm happy for you.
32|It's all thanks to you. Now I need to repay the favor.
35|There's no need.
39|Admiral FI of FO helped me! Let me return the favor. I want to work aboard your ship.
42|Now, now. I'm not sure that counts as returning the favor...
45|Oh, you don't have to worry about my skill. My grandfather sailed all over the world. I've loved ships since I was a boy...
48|I want to be an adventurer like him! I want to see the world!
52|See the world, eh? Perhaps you've inherited his spirit of adventure.
55|...Very well. I liked the nerve you showed in Seoul. Come and sail with us.
59|Yes! Traveling with someone as beautiful as you... This should be a wonderful voyage.
63|Julian?
67|Sorry, Mihwa. I'm leaving, but there's no reason to be jealous. She's my new employer.
71|As soon as I find something even better than the crown, I'll come straight back. Then we can have that date!
75|Oh, Julian... I can never win with you. I'll be waiting.
78|Let's hope this doesn't turn into a voyage of chasing women...''',
145:'''5|Well, well. Fate keeps bringing us together, Admiral.
8|That woman! The pirate from before!
12|FI... This is bad. Everyone around us looks like a pirate too.
15|And how is Her Highness today? Something like that, eh? Now, what'll you have? A drink? Or...?
18|Heh heh heh...
22|Heh!
26|...What do you intend to do with us?
30|Well... You've certainly got nerve. I'll give you that.
33|We don't have to take that tone from a pirate!
36|You've got nerve yourself, old man. We could tear you to pieces in an instant. You sure you want to talk like that?
40|Enough!
44|Eek! Sorry!
48|...You're more reasonable than I expected.
51|...You really are something, princess.
54|Hmph! Don't underestimate me. I've no intention of killing you here. Pirates have our own way of doing things.
57|We'll settle this at sea! Enjoy what time you've got left!
60|I see. We're ready whenever you are.
63|Don't forget you said that! ...Hmm?!
66|What is it?
70|I like you more by the minute. You've got a fine sword there.
73|A sword?
77|Don't understand? Never mind. But be ready. Once something catches my eye, I always take it.
81|...
85|All right, you lot! We're leaving!
89|Aye!
93|Well, well. She commands all those people with a word.
97|Just because I'm a pirate doesn't mean you can look down on me!
100|An interesting pirate.
104|A pirate with some backbone, at least.
108|I suspect she'll be following us for quite a while...''',
146:'''4|Oh?
8|...Say, has Yukihisa found any leads on that sword he's after?
12|No. I don't believe he's found anything yet.
15|Huh. Wonder if the thing even exists.
18|Who knows?
22|...
27|Yukihisa.
31|Ah, Admiral.
35|I hear you're looking for a sword.
39|You heard? But it may be no more than a rumor. We've traveled so much of the world, yet I haven't found a single clue.
42|I'd like to help, if I can.
45|No, this has nothing to do with our purpose. Please don't concern yourself.
49|...Would you consider going to Japan on your own?
52|What?
56|Traveling with us leaves you little time to search, does it? I could give you command of a fleet. Take your time and look properly.
59|I could not possibly borrow our ships for such a personal matter!
63|Dutiful as ever. But isn't it natural for an admiral to choose someone who knows the region?
67|Admiral... Thank you.''',
147:'''4|You know, there's something about India. It feels different from anywhere else.
7|Makes everything people get up to seem pretty small somehow.
10|Once this big job settles down, maybe I'll come here and just laze around for a while.
13|Planning your vacation already? Aren't you getting ahead of yourself?
16|Haha! I know, I know. We've still got a mountain of work to do.''',
148:'''4|The Arabs here don't drink alcohol at all. Apparently, this town's tavern is for foreign sailors.
8|For all the differences between our peoples and faiths, their strength of will and discipline command respect.
12|Indeed.
16|No wonder you're impressed. Can't see you giving up vodka, Ian. Or Yukihisa giving up sake.
20|Heh. True enough. But I meant more than drinking.
23|?
27|Behind their sometimes ruthless fierceness lies a rich love of beauty, and the strength and kindness to protect the weak...
31|I believe we have much to learn from them.
34|Never knew you were so fond of Arab culture, Ian. Personally, this place and my temperament don't mix too well...
37|Hehe. No, I suppose they wouldn't.''',
149:'''5|Bananas! Bananas are the future!
8|Bananas?
12|Yes! With a taste like this, they're sure to catch on.
16|You think so?
20|Of course! If I say they'll catch on, they'll catch on!
23|All right. What would you like me to do?
26|Buy as many bananas as you can!
30|Yes, yes...
34|The age of bananas is upon us! Oh ho ho ho!
37|Bananas may soon be popular in Seville.''',
150:'''5|Tomatoes! Tomatoes are the future!
8|Really? Something that red?
11|The red is what makes them wonderful! Such a passionate red... Ah, it reminds me of a burning love from my youth.
15|...I see. How nice for you.
19|Start making tomato dishes and put them up for sale at once!
22|Understood.
26|Yes. Don't let this tomato craze pass us by!
29|Yes, yes...
33|Well then, do your best! Oh ho ho ho!
36|Tomatoes may soon be popular in Genoa.''',
151:'''6|Nothing beats bread you've baked yourself.
9|I know. My husband loved mine.
12|Does homemade bread really taste that good?
16|It's wonderful! Isn't it?
20|Oh, yes. That bakery on the corner can't compare.
23|Really? Maybe I should try baking some.
27|You should!
31|I'll show you how.
35|Oh, would you? I'd love that!
39|Then let's go and buy the ingredients!
42|What do we need?
46|Well, wheat comes first, of course.
50|Wheat may soon be popular in Amsterdam.''',
}


def main():
    target=ROOT/'all335_independent_drafts_v1.json';assert not target.exists()
    path=ROOT/'all335_clean_meanings_v1.json';meanings=load(path)
    assert meanings['source_meanings_sealed_before_independent_drafts'] and meanings['no_current_story_English_read']
    assert set(DRAFTS)==set(CONTEXT)==set(range(137,152))
    parsed={}
    for number,lines in DRAFTS.items():
        values={}
        for line in lines.splitlines():
            k,v=line.split('|',1);k=int(k) if k.isdigit() else k
            assert k not in values and v.strip();values[k]=v.strip()
        parsed[number]=values
        assert set(values)=={key(r) for r in meanings['records'] if r['block']==number}
    rows=[]
    for original in meanings['records']:
        row=deepcopy(original);english=parsed[row['block']][key(row)]
        assert english.isascii() and not any(v in english for v in ['\n','{LB','{ALIGN','{PAD}'])
        source=row['source_Japanese'];macros=re.findall(r'F[IAOU]',source)
        assert re.findall(r'\bF[IAOU]\b',english)==macros,(row['id'],macros,english)
        row.update(english=english,independent_draft_pending=False,
            localized_independently_from_sealed_clean_meaning=True,logical_paragraph_without_authored_wraps=True,
            names_andUI_terms_provisional_until_consumer_binding=True,contextual_comparison_pending=True,
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),new_credit=0)
        rows.append(row)
    assert len(rows)==335
    save(target,dict(records=rows,source_objects=335,complete_exchanges=15,independent_clean_drafts_before_current_English=True,
        no_current_story_English_read=True,all_five_gates_pending=True,no_authored_line_breaks=True,new_credit=0,
        names_terms_androles_still_require_exact_source_current_consumer_bindings=True,
        explicit_bread_teaching_andprospective_wheat_notice_preserved=True,
        source_meanings=str(path),source_meanings_sha256=digest(path),
        evidence={str(p):digest(p) for p in [path,ROOT/'clean_source_packet.json',Path(__file__)]}))
    print('Sealed335 independent logical English drafts;current comparison,names/terms andall five gates remain pending.')


if __name__=='__main__':main()
