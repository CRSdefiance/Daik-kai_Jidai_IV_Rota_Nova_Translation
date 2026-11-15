"""Seal natural logical drafts from complete clean exchanges before old-English comparison."""
from copy import deepcopy
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.amend_hodram_B0_B41_clean_meanings_v2 import ROOT, OUT as MEANINGS

OUT = Path('translations/hodram_B0_B41_clean_drafts_v1.json')

ORDINARY = {
0:'''6|This seems to be a book of ancient Indian traditions.
9|Then was Sera's homeland an Indian kingdom?
12|No... India is much too far from Ottoman territory.''',
1:'''6|So this is... Muramasa...
10|Hmm... Such an eerie gleam. One could almost be drawn into it.''',
2:'''6|Yes, this is it! That dull gleam has hardly changed since I parted with it.
10|And to think no one ever picked it up...''',
3:'''6|Look there! That's {MACRO:FO}'s fleet, the ones who've been muscling in on our waters!
9|Yeah!
13|All hands, battle stations! Snake, take command!
16|You got it.
20|Angel! Bring us around to their right rear!
23|All right! You can count on me!
26|Dandy! Are the guns ready?
29|All preparations are complete.
33|Heh... Now this gets my blood pumping. Listen up, you lot!
36|Let's settle who deserves to rule these waters: me or {MACRO:FO}!
39|Yeah!
43|Pirates...
47|Their leader appears to be a woman...
51|Woman or not, she's still a pirate. Prepare for battle.
55|Understood.''',
4:'''43|Finally found you! This time, we're settling things!
46|Yeah!
52|Back for more, are you, {MACRO:FO}? This time, I'll send you to the bottom!''',
5:'''5|You there! Stop your ship. You're Julian Vermeer, aren't you?
8|Hic! ...And what if I am?
11|Betraying your homeland for money is unforgivable.
14|Glug, glug... Ahh! Bah! What's my homeland got to do with making money? Stay out of my way, or you'll regret it!''',
6:'''5|Plett Perrault. You look like a man with plenty of crimes behind him. I can't leave a murderer at large...
8|Who do you think you are?! Acting so high and mighty! Don't tell me you've never done anything wrong in your life!
11|So wrongdoing is all you're capable of. Then there's no reason to hold back. Here we come!''',
7:'''5|Jean Ramusio! Cease your illegal trade and surrender at once!
8|Illegal? Oh, really? Got any proof?
11|You're all the proof I need. You reek of dirty dealings. Shall I beat the truth out of you?
14|You just won't listen, will you? If you're so eager to die, I'll be happy to oblige!''',
8:'''6|Jacob Portunto. Smuggling's been good to you, hasn't it? Well, your easy profits end today.
9|What?! I don't need a lecture from the likes of you!''',
9:'''5|Hernan Berio. I'll take you on. A fight with a skilled opponent ought to make a change.
9|Been a while since anyone came at me. These days, everyone turns tail the moment they see me. Being this strong has its drawbacks.
12|Well, I've been bored long enough myself. Let's have at it!''',
10:'''7|Iscal Yasar? By royal command, I've come to defeat you. Prepare yourself.
11|...Admiral {MACRO:FA}. Now there's a worthy opponent. Let's go!''',
11:'''6|Heeheehee! Whooo are you? Do you waaant to die?
9|At last! There he is!
13|...Yes. He's certainly a dangerous one.
17|Heeheehee! I'll sink you! I'll sink you! I'll sink you!''',
12:'''5|Bwahaha! Learned your lesson? I'll let you off with that for now.
8|If you want to beat me, at least make a name for yourself in the Caribbean first!
12|Stay out of the southern Mediterranean! If I see you again, I'll chase you to the ends of the earth and crush you!''',
15:'''11|Release all the prisoners.
17|Damn!
21|They're pulling out quickly. They aren't pursuing us far... Hm?
25|One of their ships has run aground.
29|Abandoned, was it? Search the ship.
35|Admiral, a moment...
39|What is it?
43|We've found someone who seems rather out of place aboard this ship.
46|Hm?
50|This way.
56|She looks just like a doll...
60|!!
64|Admiral! This woman...!
67|Wait! Ngh... She seems to have mistaken me for a pirate or something.
73|...
77|Understandable. It's all right. You're free now.
80|...
84|Your features... You don't look quite like the other peoples of Africa.
87|And judging by your clothes, you don't seem to be Muslim... Perhaps you come from a distinguished family.
91|...
95|...We don't speak the same language.
107|What shall we do? We can't take her home without knowing where she was brought from.
113|What do we do? Hard to take her home when we don't know where she came from.
120|What about the other prisoners?
130|They all seem to want us to let them go here.
135|They all seem to want to be let go here.
141|They have little reason to trust us either. Very well. Anyone who wishes to leave is free to go.
151|Understood.
157|Understood.
164|You can do as you please, too. ...That knife won't be much protection out there. Take this.
168|Foreign Girl: ?!
171|Giving her a weapon is dangerous! She may try to attack you again!
175|If she wants to cut me, let her.
179|Admiral!
183|Foreign Girl: ...!
194|?!
201|Look out!
205|Foreign Girl: ...
208|Hm? You don't want it?
212|Foreign Girl: (Nods.)
215|...Heh. I see.
226|(Whew... That gave me a fright.)
233|(Whew...)''',
16:'''6|We've won.
10|Of course. If we're to build the strongest fleet, this much is only to be expected.
13|As demanding as ever, I see.
17|...So many lives lost to the sea. Or perhaps I should say they've returned to the mother sea...
21|Manuel...
25|Let us offer some comfort to their spirits.
28|Hm?
32|"The sea and a mother are alike. Each familiar ripple seems to stir the distant memory of a mother's heartbeat.
35|The sea and a mother are alike. In another land, they say, the same sounds, the same letters can stand for both.
39|The sea and a mother are alike. Both are part of bonds that last as long as we live."
42|That's a fine poem. I'm impressed. I had no idea you had such talent.
45|Yes. Most impressive.
49|...The sea accepts everything. I wish we could do the same.
52|...''',
17:'''6|Damn. Lost again... But next time... Ah!
9|Sorry, but you ain't getting a next time.
12|Heh heh heh...
16|What?! Say that again!
20|Huh? Didn't hear me?
24|I said there's no one here who'll take your orders anymore!
27|...Damn you! You've turned on me!
30|There's a commotion over there...
34|The woman pirate's own men seem to have surrounded her.
37|...Bring us closer.
41|All these losses lately, and not a coin to show for it. You're going to answer for that.
45|Answer for it...?
49|Why do you keep chasing {MACRO:FO} around, anyway?
53|Heh. Got a reason you can't tell the rest of us, haven't you?
56|!!
60|All you want is to get the Bloodstained Shamshir back from {MACRO:FO}. Your old man's keepsake, ain't it?
64|That's... That wasn't what I...
68|You've been slipping lately. No one's following a leader who can't make us any money. Get ready!
72|Admiral! They'll kill her if we don't do something!
76|...We can't leave her to that.
80|Then I'm going in.
84|W-wait! Don't be hasty!
88|Huh? Stay out of this, outsider!
91|...Don't get above yourselves, lackeys.
95|This ain't your business! ...While we're at it, finish him off along with Aziza!
99|Al, allow me to assist.
103|I'm in, too! Men who have to gang up on someone are the worst!
106|How about we blow those fellows sky-high?
110|...Pirates! Come on, then. I'll take you!
113|Why...? Why are they fighting for me? We were enemies a moment ago...
117|D-damn it! The odds ain't looking good!
121|Finally noticed, have you?
125|{MACRO:FI} {MACRO:FA}...
129|...You here to save her, too?
133|And if I am?
137|Tch. This is all her fault. Why're we the ones getting...?
140|...Surely you've finished complaining by now. Why not let her go?
143|All you want is Aziza gone, isn't it?
146|So you heard. Nobody's following her anymore.
149|...
153|Then we'll take Aziza with us.
156|!!
160|Is that so? That don't mean we're handing her over for nothing.
164|You want money?!
168|Al, enough. Now, what will it take?
171|One million gold.
176|Aziza... Come with me.
180|...
184|That settles it. So long!
190|Betrayed by my own crew... I've really sunk low. But why did you save me?
193|I couldn't leave you there...
197|Only someone utterly inhumane would have left you in that situation.
200|There is something I have wondered... Why would someone of your caliber fall into piracy?
204|You think too highly of me. ...I didn't fall into it. I'm a pirate's daughter. My father was a pirate.
207|Oh?
211|Those pirates were my father's men. I grew up watching them, copying their swordplay and learning the trade.
214|What became of your father?
218|He died in an accident. ...That sword was his treasure. It disappeared with him...
222|The Bloodstained Shamshir...
225|I wanted to be a great pirate, just like him. I copied everything he did...
229|So when I found out you had the sword, I had to get it back. If I could just do that...
232|...?
236|I thought it would prove I was getting closer to being like him. Heh... But, you know...
240|I realized I didn't really want to be a great pirate. I just wanted something to remember my father by...
243|No wonder they left me. I was chasing something that wouldn't earn a thing. I can't blame them for being angry.
247|...Do you still want to be a pirate?
251|It wasn't piracy I was chasing. It was my father. I'm leaving that life behind.
255|Admiral...
259|Al, I know what you're going to say. Aziza, would you join my ship?
262|I'd be grateful... I'll work my heart out. After all, I owe you my life.
266|And just call me Aziza.
269|One can also choose a life of loyalty to one's benefactor.
272|Things are going to get even livelier...''',
18:'''18|We're pulling out for today! Next time, I'll settle this!
21|Say what you like.
27|Tch. I'll withdraw for now. But I'll never submit! Remember my name: Aziza Nurennahar!
31|...I'll remember.''',
19:'''16|...We're withdrawing for today.
20|Oh! Running away?! You're more of a coward than you look!
23|Don't rise to her taunts!
27|I know. Retreat!
33|They got away!
37|We should withdraw for now.
41|That pirate is no ordinary opponent. She could hold her own as a navy admiral...
45|You thought you could beat me? Next time we meet, be ready to die!''',
20:'''9|Behave yourself. You're coming with us to San Jorge.
12|Damn you! Keep your hands off me! You bas... Mmph!''',
21:'''9|Bind him securely. We're taking him to Hangzhou.
12|Ow, ow, ow! I-I'm sorry for what I've done...''',
22:'''8|What a nuisance you are. No wonder the Basra guild has its hands full.
11|Give me a break! Without me, things around here would've been a whole lot worse!
15|Trying to justify your own crimes... What a vile man. You make me sick.''',
23:'''9|D-damn it... My precious cargo...
12|Forget the stolen cargo. You should be worried about being taken to Calicut.''',
24:'''9|...L-listen. I let you win!
12|I'm handing you over to the Athens guild. Behave yourself until then.''',
25:'''8|...Gah! I... I lost?! No! I won't accept it!
12|Guaaah!
16|Our mission is complete. Return to Stockholm. We must report to His Majesty.
20|Admiral! We found this aboard the enemy ship!
26|Some of his plunder, perhaps... It doesn't look like an ordinary decorative plate.''',
26:'''28|One would think he'd have shown himself by now...
52|We'll keep wiping out pirate fleets, one after another.''',
27:'''9|Eeeheehee! Youuu! I'll curse you! I'll curse you! I'll curse you!
13|...The sooner we hand him to the Havana guild, the better.''',
28:'''5|Finally dealt with that one.''',
29:'''5|There! There it is!
9|Speyer's ship?
13|That's a Hanseatic cog, all right. No mistaking it!
16|But we can't take action outside our own territorial waters.
19|W-what?! They just opened fire on us!
22|What are they doing? Have they mistaken us for someone else?!
26|Signal them!
30|Yes! What's the message?
34|Your fleet may have entered our territorial waters without permission.
38|We request that you stop so we can investigate the circumstances.
41|!!
45|Aaaah!
49|I-it's no use! They don't even seem willing to look at our signals!
52|So they know exactly what they're doing...
56|They mean to dispose of us before any trouble arises.
59|In that case, we needn't hold back. All hands, prepare for battle!
62|Tch. What a nuisance. Teach that slapdash excuse for a fleet what a sea battle's really like!
67|Charles! What's your plan?
71|Let's use the standard tactic: crossing the T.
74|Stay clear of their broadsides and maneuver ahead of their bow or behind their stern. Then bring our broadside to bear and finish them with a volley!
77|Good. I'll leave all the gunnery to you!
81|Leave it to me! You maneuver the ship, and I'll direct the gunners!
85|At last! Time to see what these new guns can do!
88|Control your ship's heading and sail direction just as you do during ordinary movement.
92|Your guns fire automatically when an enemy ship comes within range.
95|Admiral! Assign me to the Quarters as boarding leader!
98|Change your navigators' assignments for battle on the Deck screen.
102|To open the Deck screen, press X and select it from the menu.
106|During battle, assignments to Batteries, Quarters and the Deck are useful.
109|Select Gerhard and assign him to the Quarters.
112|Boarding combat begins automatically when ships touch. Gerhard should prove an effective boarding leader.
116|Come on, Admiral. Give us our heading!''',
30:'''10|You there! Was it you who dared approach my waters?! If you value your lives, get out of the southern Mediterranean!
13|So that's the fellow the man at the port warned us about.
16|Barbarossa! ...I knew it!
19|You know him?
23|Barbarossa Fazul Hayreddin... He carries on the name of Barbarossa, the name synonymous with the pirate chiefs of Algiers.
26|He looks like quite a fighter.
30|Yes. A monster, to put it simply. And what's more...
36|We may be allies, but that doesn't give you leave to trespass! Get out of the southern Mediterranean!
40|So that's the fellow the man at the port warned us about.
43|So it was Barbarossa he meant!
81|Oh? You mean to fight?! Bwahahaha! Then expect no mercy. I'll kill you all!
88|Bwahaha! A wise choice! If you want to take me on, at least make a name for yourself in the Caribbean first!
91|Stay out of the Mediterranean! If I see you again, I'll chase you to the ends of the earth and crush you!''',
32:'''25|Listen up, you lot! Show those ignorant fools from the fringes of Europe how we do things in the Caribbean!
55|Don't be intimidated. Fight as you always do. Here we go! All hands, battle stations!
81|What?!
93|Oh, God!
106|I-it's hopeless... We can't beat that many!
111|I-it's hopeless... Logically speaking, we can't beat that many!
117|...Wait. Those flags...
132|Well met. I'll lend you a hand.
135|Escante's forces!
145|W-we're saved!
151|W-we're saved!
163|Hey, good thing we ran into you! We'll give you a hand!
166|Escante's forces!
176|W-we're saved!
182|W-we're saved!''',
33:'''5|Well done, {MACRO:FA}. A fine performance. You're a dependable ally.
8|Maldonado is dealt with, but those English pirates remain a nuisance.
12|I'd like to maintain our agreement. What do you say?
15|...
34|(Espinosa has begun making serious moves in Africa. We must deal with him quickly.)
38|Hm...
42|(I suggest we accept his offer for now...)
63|Good. I look forward to seeing what you accomplish.
73|I see. A pity. I do hope you won't become an enemy.''',
34:'''6|Bwahahaha! Challenging me outright? You've got nerve! Do try to keep me entertained!
18|Ha! You're a cheerful fool. I'll bet you're going to lose!''',
35:'''6|More unbelievers, one after another! The Indian Ocean's trade routes belong to us Muslims!''',
36:'''6|So the Ming hired southern foreigners! Damn them! I'll show no mercy to anyone in my way!''',
37:'''6|...Admiral. Look over there.
9|Hm?
13|That appears to be a slave ship.
17|I thought human trafficking was prohibited.
21|Yet it remains widespread. Surely our patrol fleet can't turn a blind eye?
40|They have plenty to hide. Whatever our pretext, we've found a target we can strike without shame.
43|...Hmm.
50|Very well. We'll strike just before they enter port! All hands, battle stations!
61|Heh heh. Let's give them a show!''',
38:'''6|There! Lil's fleet!
10|Maria Huamei Li! What have I ever done to you?!
13|Maria...?
17|Lil! That's Kuhn's fleet in disguise! Don't be fooled!
21|Camille?!
25|Kuhn's trying to make you and Maria fight each other!
28|What are you talking about? But... Huh?
31|Is that true, Camille?
35|Yes. I know Kuhn very well. And Maria discovered the plan and warned me herself.
39|I see.
43|Take aim! The unidentified fleet straight ahead!
47|Kuhn! Show yourself!
51|Fire!
55|Hah!
59|Damn it!
63|Is that {MACRO:FO}?! Kuhn, sir, we're at a disadvantage!
66|Tch. That's as far as we go! Withdraw!
70|That's... Kuhn?! Then I've been...!''',
39:'''5|Enemy fleet spotted ahead!
9|Southern foreigners! I'll show you the spirit of Yamato!
21|W-what are those ships?!
27|W-what are those ships?!
34|...Ships clad in iron!
46|I never knew ships like that existed...''',
40:'''6|Stop!
11|!!
15|Such a pity. There's nowhere to run.
19|Bwahahaha! So you're {MACRO:FA}! It seems your heroic exploits end here!
27|Pasha... You really have no intention of sharing the Mediterranean with me, do you?
55|Hmph... A motley rabble. We'll break through!
58|Bwahaha! Insolent wretch! Do you know who you're dealing with?
61|What an ill-mannered general.
65|We'll make a public execution of this upstart! All ships, charge!
68|Aaaah!
72|What happened?!
76|Pasha, sir! W-we're taking fire from the town!
79|W-what?! Why?! What's going on?!
82|I-I don't know! Looks like someone's seized the town's gun batteries!
88|○○×!
92|○×ーッ!!
96|!! Is that...?!
100|Guaaah!
111|Have Mushari's fleet return fire! Withdraw at full speed!
116|Have Mushari's and Arnajud's fleets return fire! Withdraw at full speed!
125|Hey! What happened to my public execution? Come and fight me!
129|Grr! Come on, then! I'll make you cough up blood!''',
}

STYLE = {
(28,36):[
"Let's report to the Malacca guild right away!", "We must report to the Malacca guild at once.",
"Let's hurry and report to the Malacca guild!", "Let's get to the Malacca guild and report this already!",
"We'd best report to the Malacca guild at once.", "Let's hurry and tell the Malacca guild!",
"Shall we go straight to the Malacca guild and report?"],
(30,662):[
"What an enormous fleet! We'd be safer running away!", "An immense fleet... We'd be safer retreating.",
"Whoa, what a huge fleet! Shouldn't we run?!", "That's a huge fleet! Admiral, we'd better run!",
"That's one massive fleet! We'd be better off running!", "An enormous fleet! Retreat would be the wiser course.",
"Whoa, look at all those ships! No way! Let's run!", "An enormous fleet! We'd be safer making a retreat."],
(32,10):["Maldonado's fleet sighted!", "We've found Maldonado's fleet!", "I've spotted Maldonado's fleet!", "Oh! It's Maldonado's fleet!"],
(32,280):["He's brought quite a force!", "He's brought a considerable force.", "He's brought a lot of ships!", "He's got lots of ships with him!",
"He's got quite a force with him!", "He's brought quite a force, all right!", "There are so many of them!", "He's brought quite a force!"],
(32,596):["Admiral, more ships approaching from behind!", "A-Admiral! More ships behind us!", "Admiral, there's more coming up behind us!",
"Admiral! They've come up behind us, too!", "Aaah! More of them behind us!"],
(40,284):["W-we're surrounded! S-so many fleets!", "We're surrounded! S-so many fleets!", "Aaaah! W-we're surrounded! S-so many fleets!",
"W-we're surrounded?! S-so many fleets!", "W-we're surrounded! Th-that's a lot of fleets!", "W-we're surrounded! Such a great many fleets!",
"Th-they've got us surrounded! There are so many!", "W-we're surrounded! S-such an enormous force!"],
(41,10):["Admiral! There it is! A monstrous fish!", "Aaah! A monstrous fish!", "Eek! Th-there it is! A monstrous fish!",
"Admiral! A monster fish just showed up!", "A-Admiral! A monstrous fish!", "Aaah! A monster fish!", "Admiral! A monstrous fish has appeared!"],
}

CAPTIONS = {(30,1100):['Prepare for battle!',"Let's withdraw."],
            (33,414):['Agreed.','I refuse.'],(37,216):['Prepare to attack.',"That's beyond our authority..."]}

SPECIAL = {
(0,9):'The question is a provisional inference, immediately challenged by the next record.',
(0,12):'Preserve the counterargument; India is not established as Sera’s homeland.',
(7,11):'Adapt the dust/dirty-laundry idiom to a coercive spoken accusation, not a factual legal ruling.',
(15,84):'This is Hodram’s tentative observation about appearance, not an omniscient identity finding.',
(15,87):'Keep the religious/social inferences tentative and character-bound.',
(15,164):'The offered weapon is not named in the source; do not add sword ownership or romance.',
(15,212):'Preserve the embedded anonymous-girl label and the nod in answer to not wanting the weapon.',
(16,35):'Keep the unnamed-language statement as hearsay; do not choose a language or correct the fictional poem with external lore.',
(17,103):'Clean selector7 identifies Cristina. Preserve the original v1 gloss as superseded attribution evidence.',
(17,171):'One million is exactly 1,000,000; preserve outgoing demand and currency.',
(17,218):'Death is explicitly an accident; no murder or mutineer responsibility is supplied.',
(25,12):'A pained cry does not independently prove death.',
(29,92):'Automatic cannon fire is a source tutorial mechanic, not a newly inferred feature.',
(29,102):'Preserve X and Deck menu access; final menu consumer binding remains pending.',
(29,112):'Preserve automatic boarding upon ship contact; do not add a manual boarding button.',
(35,6):'Preserve the antagonist’s explicit Muslim identity and exclusive religious claim as his speech.',
(36,6):'Southern foreigners preserves the historical-cultural framing without inventing a nationality.',
(38,66):'Do not remap actor40 to another actor based on an expectation of who ought to answer.',
(40,88):'Source uses ○○× as opaque foreign speech. Preserve its exact lexical symbols; qualify consumer/glyphs before shipment.',
(40,92):'Preserve the source’s opaque symbols and prolonged cry; do not invent a translated order. Consumer/glyph qualification remains pending.',
}


def main():
    assert not OUT.exists()
    meanings = load(MEANINGS)
    assert meanings['records_count']==394
    assert all(digest(p)==h for p,h in meanings['evidence'].items())
    names = ROOT/'draft_names_andterms_reference_v1.json'
    references = load(names)
    assert references['current_eligible_story_English_not_extracted']
    ordinary = {}
    for block,text in ORDINARY.items():
        pairs=[line.split('|',1) for line in text.strip().splitlines()]
        assert len({int(k) for k,_ in pairs})==len(pairs)
        ordinary.update({(block,int(k)):v for k,v in pairs})
    style_groups={}
    for row in meanings['records']:
        if row.get('kind')=='actor-style-alternative':
            style_groups.setdefault((row['block'],row['source_command_offset']),[]).append(row)
    assert set(style_groups)==set(STYLE)
    styles={}
    for key,rows in style_groups.items():
        rows=sorted(rows,key=lambda r:r['source_reference']['offset'])
        assert len(rows)==len(STYLE[key])
        assert sorted(i for row in rows for i in row['source_style_indices'])==list(range(8))
        styles.update({r['id']:v for r,v in zip(rows,STYLE[key],strict=True)})
    result=[]
    for original in meanings['records']:
        row=deepcopy(original)
        kind=row.get('kind')
        if kind=='actor-style-alternative':
            english=styles[row['id']]
            speaker='Native companion role '+str(row['source_selector'])
            note='Keep this physical voice’s register and all source alias slots; do not infer a named participant or biography.'
        elif kind=='typed-choice-label':
            english=CAPTIONS[(row['block'],row['source_command_offset'])][row['source_index']]
            speaker='Player choice caption'
            note='Preserve this choice’s source action, branch index and contrast with the other choice.'
        else:
            key=(row['block'],row['source_reference']['record_index'])
            english=ordinary.pop(key)
            speaker='Native system panel' if row['source_selector']==254 else 'Source actor '+str(row['source_selector'])
            note=SPECIAL.get(key,'Keep the complete exchange’s meaning, uncertainty and character register; named terms remain subject to scoped consumer review.')
        assert english.strip()==english and '\n' not in english and '\r' not in english
        assert not any(t in english for t in ('{LB','{ALIGN','{PAD}','%','\t'))
        for macro in ('FI','FA','FO'):
            assert english.count('{MACRO:'+macro+'}')==row.get('source_macros',{}).get(macro,0),(row['id'],macro)
        if not english.isascii():
            assert row['id'] in ('DK4_MES_B40_R0088','DK4_MES_B40_R0092'),row['id']
        row.update(english=english,speaker=speaker,context=row['whole_exchange_context'],localization_note=note,
            review=dict.fromkeys(('source','context','localization','naturalness','formatting'),False),
            source_first_draft_not_final_comparison_approval=True,current_English_conversation_comparison_pending=True,
            scoped_names_terms_controls_glyphs_andall_display_checks_pending=True,new_credit=0)
        result.append(row)
    assert not ordinary and len(result)==394 and len({r['id'] for r in result})==394
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=result,records_count=394,
        ordinary_drafts=341,physical_style_drafts=47,typed_caption_drafts=6,complete_exchange_blocks=sorted(ORDINARY.keys()|{41}),
        source_meanings=str(MEANINGS),source_meanings_sha256=digest(MEANINGS),
        all394_logical_drafts_written_before_current_ROM_story_English_intake=True,current_English_comparisons=0,
        no_blanket_claim_of_no_historical_English_exposure=True,current_eligible_story_English_not_extracted=True,
        source_names_terms_andnonASCII_symbols_require_scoped_review=True,
        tutorial_priority_blocks=[29],all_five_individual_review_gates_still_pending=True,
        no_ordinary_manual_breaks_padding_oralignment=True,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={str(p):digest(p) for p in (MEANINGS,names,Path('translations/ship_battery_labels_v1.json'),
            Path('translations/ship_quarters_label_v1.json'),Path(__file__))}))
    print('Sealed394 source-first logical drafts; no existing-English comparisons or completion credit yet.')


if __name__=='__main__':
    main()
