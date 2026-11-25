"""Clean-first sailing/trade tutorials andcomplete later exchanges;no current-English comparison."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
OUT = ROOT/'B127_B135_meanings_andindependent_drafts_v1.json'
TEXT = {
127: {
5: ('Julio proposes Ceuta as the first destination.', "First, let's make for Ceuta."),
9: ('He begins practical ship-handling instruction.', "Now, let's get this ship moving."),
13: ('First check the ship’s current heading.', 'First, check which way the ship is facing.'),
16: ('Tell the fleet its course by pointing the ship where it should go.', "Give everyone the fleet's course. Point the ship in the direction you want to go."),
20: ('An FE instruction says heading is chosen with the Control Pad or stylus.', 'Use the Control Pad or stylus to choose which way to sail.'),
23: ('Press the corresponding direction or touch the screen in the desired direction.', 'Press the Control Pad in the direction you want to go, or touch that direction on the screen.'),
26: ('Stylus steering automatically sets the sails optimally;touch the flagship to stop.', 'When you use the stylus, the sails are adjusted automatically. Touch your flagship to stop.'),
29: ('Julio asks whether the explanation was understood;the following choice has two distinct responses.', 'Does that make sense? What do you think?'),
44: ('He encourages the admiral to continue doing well.', 'Keep it up, Admiral!'),
49: ('Rafael can set a heading but wonders whether unfavorable wind prevents progress.', "I can choose a direction, but we won't get anywhere unless the wind catches the sails properly... Will we?"),
54: ('Julio concedes headwinds impede progress but reassures him about the tailwind on this Ceuta route.', "Of course, it's hard to make headway into the wind. But we've got a tailwind on the way to Ceuta, so we should be fine."),
58: ('Rafael is still uncertain about managing it.', 'Will we be all right...?'),
63: ('A reassuring proverb says doing is easier than worrying;Lisbon is a fallback if they cannot make progress.', "You'll find it's easier than you think. If we really can't make headway, we can always return to Lisbon."),
70: ('Long voyages can bring illness,rats andleaks;these examples are not presented as an exhaustive list.', 'All sorts of things can happen on a long voyage. Illness, rats, leaks...'),
73: ('Such trouble often cannot be remedied at sea,so Julio advises reaching port promptly;do not turn this into an absolute prohibition.', "There's often little you can do about those at sea. Best make for port as soon as you can."),
77: ('The system says entering a town’s port restores the fleet from abnormal conditions.', 'If your fleet develops an abnormal condition, put in at a town to recover.'),
80: ('Ceuta is southeast from the present position;the named route chart can confirm it.', "Now, Ceuta is southeast of here. Check the Route Chart to see for yourself."),
},
128: {
12: ('Julio addresses FI andoffers to explain several remaining actions available while sailing.', "Now, FI, there are a few more things you can do at sea. Let me explain them."),
15: ('Rafael politely accepts the explanation.', 'Yes, please.'),
20: ('Julio introduces when full sail andanchoring are useful.', "I'll explain when to set full sail and when to anchor."),
23: ('Full sail gives maximum speed,butthe captain must directly order the sail handlers.', 'Full Sail lets the ship move at top speed. But as captain, you must direct the sail handlers yourself.'),
26: ('Beginners can remain at half sail;enough sail handlers for the number of masts trim the sails automatically.', "Half Sail will do while you're learning. Have one sail handler for each mast and they'll trim the sails for you."),
29: ('Full sail may be too fast to handle easily;half sail may also be more convenient in battle.', 'Full Sail may be too fast to handle easily. Half Sail can be more useful in battle, too.'),
32: ('Anchoring can regroup a spread-out fleet orallow an ambush;these are examples of uses.', 'Anchor can help regroup your fleet when the ships have spread out, or let you lie in wait for an enemy.'),
36: ('Rafael acknowledges the explanation.', 'I see.'),
42: ('At sea,sail opening controls speed;the fleet can also stop in place.', 'At sea, adjust how far the sails are open to change speed. You can also anchor in place.'),
46: ('A increases sail opening/speed;B decreases it.', 'Use A and B to adjust the sails. Press B to slow down or A to speed up.'),
50: ('B changes Full Sail to Half Sail andlowers speed.', 'At Full Sail, press B to switch to Half Sail and slow down.'),
53: ('B changes Half Sail to Anchor andstops the fleet in place.', 'At Half Sail, press B to anchor and stop in place.'),
56: ('A changes Anchor to Half Sail,orHalf Sail to Full Sail.', 'While anchored, press A to set Half Sail. At Half Sail, press A to set Full Sail.'),
60: ('Even Half Sail requires manual sail orders if there are too few sail handlers.', "Remember, even at Half Sail, you'll have to direct the sails yourself if you don't have enough sail handlers."),
63: ('Rafael is surprised by that requirement.', 'What? Really?'),
68: ('Full-speed sailing will eventually be needed;acaptain should learn sail handling.', "You'll need to sail at full speed eventually. A captain ought to know how to handle the sails."),
72: ('Rafael nervously agrees.', 'Y-yes!'),
77: ('The basic way to gain speed is to catch wind from behind the sails.', 'The basic idea is to catch the wind on the back of the sails.'),
81: ('L andR adjust sail direction;proper adjustment raises speed.', 'Use L and R to turn the sails. Adjusting them properly increases your speed.'),
85: ('L turns sails left;R turns them right.', 'Press L to turn the sails left, or R to turn them right.'),
89: ('Stylus use automatically sets optimum sail direction;touch the flagship to stop.', 'When you use the stylus, the sails are adjusted automatically. Touch your flagship to stop.'),
93: ('Watch wind direction andadjust the sails so their back catches the wind relative to the ship’s heading.', "Watch the wind's direction. Adjust the sails so the wind catches them from behind, taking the ship's heading into account."),
97: ('A tailwind makes this relatively easy;aheadwind requires some skill.', "That's fairly easy with a tailwind. A headwind takes a little practice."),
101: ('The on-screen speed gauge shows speed;maximize its bar when adjusting for maximum speed.', 'Check your speed on the on-screen gauge. For the best speed, adjust the sails until the bar is as long as possible.'),
104: ('Julio has covered the basics;furtherlearning depends on Rafael’s own experimentation.', "Well, that covers the basics. The rest is up to you to work out."),
107: ('Rafael enthusiastically agrees to try.', "Understood. I'll give it a try!"),
111: ('Julio feels he has forgotten something.', "Hmm... I feel as though I've forgotten something..."),
114: ('Rafael reacts inquisitively.', '?'),
128: ('Julio remembers andasks FI to head to Athens.', "Ah, that's right! FI, would you mind taking us to Athens?"),
132: ('Rafael identifies Athens as Greek andtowardthe eastern Mediterranean,withsome hesitation.', 'Athens...? Um, in Greece, right? Toward the eastern Mediterranean?'),
137: ('Julio confirms andsays he has business there.', "That's right. I've a little business there."),
140: ('Claudio questions letting the old man’s errand dictate the destination;heis not calling Julio a relative.', "Hey, are we really letting the old man's errands decide where we go?"),
143: ('Julio says the matter concerns everyone’s future,notjust his own business.', "It's not just my business. I'm going to look into something that concerns the future of us all."),
147: ('Rafael wonders whether this means a goal for the group.', 'Our future...? Do you mean something like a goal for us?'),
152: ('Julio agrees,approximately.', 'Hmm. Something like that, yes.'),
155: ('It is not an immediate task,butwillcertainly become necessary later.', "It isn't something we need to act on right away. But we'll certainly need it later."),
164: ('Rafael asks whether going to Athens will make the matter clear.', "And we'll find out what it is when we reach Athens?"),
168: ('Julio confirms.', "That's right."),
174: ('The matter is also necessary to fulfill the promise to Hayreddin.', "We'll need it to keep our promise to Hayreddin, too."),
180: ('Claudio finds this promising andaddresses FI.', 'Hey, FI! This sounds interesting!'),
184: ('Rafael agrees with enthusiasm.', 'Yeah!'),
189: ('Julio urges prompt action on a good purpose andentrusts it to FI.', "No time like the present. I'm counting on you, FI."),
200: ('Janus wonders what awaits them there.', 'I wonder what we will find there.'),
207: ('Claudio cheerfully announces departure in search of their goal.', "All right! Let's go find ourselves a goal!"),
210: ('Rafael is puzzled by that odd announcement.', 'Huh? That sounded strange...'),
},
129: {
5: ('Julio asks FI whether the secret to substantial trading profits has been learned.', "Now, FI, have you got the hang of making a good profit from trade?"),
20: ('The first recommended destination is Portuguese Madeira,asmall island southwest of Lisbon.', 'Hmm. First, look to Madeira, a Portuguese island southwest of Lisbon.'),
24: ('Madeira has sugar andotherlocal goods,andwouldbe an important base for FO to expand into Africa andthe New World.', 'It has sugar and other fine local goods. It should also be an important base when FO expands into Africa and the New World.'),
27: ('If market share remains available in Madeira,investasmuch as possible.', 'If there is any unclaimed market share in Madeira, invest as much as you can.'),
30: ('After building funds through the Lisbon-Ceuta-Madeira trade triangle,secureLas Palmas andVerde next.', 'Once the trade triangle between Lisbon, Ceuta and Madeira has built up your funds, secure a foothold in Las Palmas and Verde next.'),
33: ('Those are gateways to Africa andthe Mediterranean;Verde especially offers many local goods for relatively little investment.', 'They are gateways to Africa and the Mediterranean. Verde in particular offers many local goods for a small investment.'),
36: ('For a time,tradeback andforth between Africa andthe Mediterranean,anduse profits for larger ships andmore market share.', 'For a while, trade back and forth between Africa and the Mediterranean. Use the profits to buy larger ships and increase your market share in the towns.'),
39: ('More fleet cargo holds andmorelocal goods to buy allow larger profits per trading run.', "With more cargo holds in your fleet and more local goods to buy, you'll make more money on each trading run."),
42: ('Then expand the trading range progressively farther.', 'After that, keep expanding your trade farther afield.'),
45: ('Commercial investment can cause new local goods to appear even in a seemingly unprofitable town;thisis not guaranteed.', 'Even a town that seems to have no profitable local goods may start producing something new if you invest in its commerce.'),
48: ('If resources permit,theNew World is an option,butthere is no need to overextend.', "If you can afford it, you might even venture to the New World. There's no need to overdo it, though."),
52: ('Rafael agrees to do his best.', "Understood. I'll do my best."),
58: ('Julio worries about Rafael andrecognizes that older people may worry unnecessarily.', 'Will you be all right...? We old folks always worry more than we need to.'),
62: ('He ultimately encourages Rafael to try his own approach.', 'Well, try doing things your own way.'),
},
132: {
13: ('Rafael announces the decisive battle with Valdes andcalls for everyone’s best effort.', "All right! This is our showdown with Valdes! I'm counting on all of you!"),
25: ('A composed companion checks readiness.', 'Is everyone ready?'),
40: ('A rough companion challenges the enemy andsays he is ready at any time.', "Hah! I'm ready whenever you are! Come and get it!"),
46: ('Claudio enthusiastically commits to the fight.', "Yeah! Let's do this!"),
58: ('Another companion confidently says to leave it to them.', 'Leave it to me!'),
65: ('An enemy speaker recognizes the Portuguese fleet andscorns inexperienced youths for rebelling against the Spanish Empire now.', "So that's the Portuguese fleet I've heard about. Reckless young fools, daring to rise against the Spanish Empire now!"),
68: ('He vows to teach them a lesson andorders all ships to prepare for battle.', "I'll teach them a lesson. All ships, prepare for battle!"),
71: ('A subordinate acknowledges andrelays the order to all ships.', 'Yes, sir! All ships, prepare for battle!'),
75: ('Another enemy speaker remains silent.', '...'),
79: ('An officer orders the battle line to form.', 'Form the battle line!'),
83: ('An enemy officer identifies the Portuguese rebels ahead andorders a charge.', 'Enemy ahead! Portuguese rebels! Charge!'),
},
133: {
5: ('Julio remembers something.', 'Come to think of it...'),
9: ('Rafael reacts inquisitively.', '?'),
14: ('Julio decides to bring Cristina along.', "Yes, yes! That's it. Let's bring Cristina along."),
17: ('Rafael asks who that is.', "Who's Cristina?"),
22: ('Julio identifies his actual granddaughter andsays she is a skilled sword user.', "My granddaughter. She studies the sword, and she's quite skilled."),
25: ('Claudio objects to a woman joining his romantic ideal of a man’s voyage,thenalmost blurts out an existing woman’s presence.', "What, a woman?! Sailing's a man's adventure! I'm against it. We've already got a woman... Oops!"),
28: ('Arcadius coughs andwarns Clau by his familiar nickname.', 'Ahem. Clau...'),
32: ('Claudio recovers andcontinues to object to a woman joining.', 'A-anyway, having a woman aboard is a bad idea, right?'),
35: ('Rafael supports inviting a swordswoman whocouldhelp them.', "I think it's a good idea. She's a swordswoman, right? I'm sure she could help us."),
40: ('Claudio persists in objecting,thenreacts to pain inflicted in the exchange;thetext does not specify the physical action.', "No, I'm against it! Ow, ow! Wh-what are you doing?!"),
43: ('In a parenthesized aside,Arcadius says one woman ortwo makes no difference.', "(One woman or two, what's the difference?)"),
47: ('Rafael privately agrees andsays another woman wouldput Arcadius at ease;retainthird-person reference.', '(Right. Arcadius would feel more at ease with another woman around.)'),
52: ('Arcadius coughs andformally supports the idea.', 'Ahem. I agree as well.'),
56: ('Rafael says having women along makes the journey more enjoyable andasks Clau’s agreement.', 'Having women along will make the journey more fun. Come on, Clau. Is that all right?'),
60: ('Claudio privately gives in,disappointedthat even FI is against him.', '(What? Even you, FI...? All right, all right.)'),
64: ('He grudgingly agrees if the others insist.', 'If you all insist, then fine...'),
67: ('Julio is puzzled by the exchange.', '?'),
71: ('Rafael politely asks where Cristina lives.', 'So, where does she live?'),
76: ('Julio answers London.', 'In London.'),
80: ('Rafael agrees to head there.', "All right. Let's head for London, then."),
},
134: {
6: ('Rafael is startled by an attack.', 'Wh-what was that?!'),
11: ('A sailor reports a surprise pirate ambush thatprevents fighting back.', "An ambush! They look like pirates! They've caught us off guard! We can't fight back!"),
15: ('Claudio recognizes the pirate’s flag andwarns the admiral that this is dangerous;namebinding remains pending.', "What?! That flag... The pirate Verus! We're in trouble, Admiral!"),
19: ('Janus has heard dangerous rumors about the pirate andsays they have caught his attention.', "I've heard of him. He's notorious for being dangerous. Of all the people to spot us..."),
23: ('Claudio urgently warns FI of danger.', 'FI! Look out!'),
27: ('Rafael reacts in shock.', '!!'),
32: ('Claudio cries out in pain.', 'Aaargh!'),
44: ('Arcadius cries Claudio’s full given name in alarm.', 'Claudio!'),
51: ('Rafael asks whether Clau is all right.', 'Clau! Are you all right?!'),
56: ('Claudio dismisses the injury as a scratch andtells him not to worry.', "Just a scratch! Don't worry about me!"),
60: ('Rafael orders immediate retreat at full speed.', 'Gah! Full speed! Get us out of here!'),
65: ('They have somehow shaken off pursuit,butcannotcontinue in this state;Rafael proposes a nearby port.', "We managed to lose them... But we can't go on like this. Let's put in at a nearby port."),
70: ('Claudio rules out Amsterdam as dangerous andasks for another port.', "Amsterdam's too dangerous. Let's choose another port."),
},
135: {
5: ('A companion asks whether the widely traveled admiral has close female acquaintances in taverns aroundthe world.', "You travel all over the world, Admiral. You must be friendly with girls in all sorts of taverns, right?"),
9: ('Rafael denies being particularly close to them.', "I wouldn't say we're that close..."),
14: ('The companion says this is inadequate because tavern girls know information adventurers need.', "That won't do! The girls in taverns know all sorts of things an adventurer needs to hear."),
18: ('Examples are treasure rumors,enemyfleet movements,andruin locations known only to locals.', "Treasure rumors, enemy fleet movements... Sometimes they'll even tell you about unusual ruins only the locals know how to find."),
21: ('He jokingly frames befriending girls worldwide as a requirement for adventurers.', "You're no adventurer if you don't make friends with girls all around the world!"),
25: ('Rafael doubts that befriending them is easy.', "But... It can't be that easy to get close to them, can it?"),
29: ('Simply talking as an ordinary customer is not enough because they converse with dozens of people daily.', "Just chatting as another customer won't do. They talk to dozens of people every day."),
32: ('He recommends a gift that wins the girl’s heart.', "Nothing beats a gift that'll win her heart."),
35: ('Preferences differ;findout what each woman wants andgive a suitable present.', "Of course, they all like different things. Find out what she's interested in and give her a present she'll like."),
43: ('Sakura inOsaka wants the named robe reportedly sold in a North Sea town;approved item-label spelling is pending.', "Take Sakura in Osaka. She'd like a Light Snow Robe. They say you can buy one in a town somewhere on the North Sea."),
52: ('Even an undemanding girl appreciates receiving something she wants.', "Even a girl who doesn't ask for much likes getting something she really wants."),
56: ('Rafael naively concludes the companion’s serial flirting was normal adventurer behavior.', "I see. So flirting with one tavern girl after another was just part of being an adventurer..."),
60: ('The companion stammers a defensive affirmation,preservingthe joke.', 'O-of course!'),
64: ('Rafael earnestly resolves to follow that example.', "All right! I'd better follow your example!"),
69: ('The companion laughs andencourages him.', "Ha ha ha! That's the spirit!"),
},
}
CHOICES = {
'SC0_B127_CHOICE_488_0': ('Rafael says the explanation is completely understood.', "I've got it!"),
'SC0_B127_CHOICE_488_1': ('He worries the wind direction may be unfavorable,ratherthan simply saying he does not understand.', 'The wind might be against us...'),
'SC0_B129_CHOICE_80_0': ('He admits he stillhasmuch to learn about profitable trade.', 'I still have a lot to learn.'),
'SC0_B129_CHOICE_80_1': ('He says he can manage trading now.', "I've got the hang of it."),
}
CONTEXT = {
127: 'The practical sailing tutorial chooses Ceuta as a first destination, teaches heading with the Control Pad or stylus, and explains automatic sail direction plus touching the flagship to stop. The two-choice check separates confidence from a specific wind concern. Julio reassures Rafael about the current route’s tailwind, gives Lisbon as a fallback, and explains voyage troubles/port recovery. Keep headwind difficulty distinct from inability to steer. Preserve qualified at-sea advice rather than claiming every condition is impossible to treat. UI label/control bindings remain pending.',
128: 'Julio distinguishes Full Sail, Half Sail andanchoring, manual sail orders andone sail handler per mast. Half Sail is automatic only with sufficient handlers. A/B change opening/speed;L/R turn sails;stylus use automatically trims them andflagship touch stops. Speed-gauge advice follows wind-direction guidance. The exchange then shifts from Julio remembering an errand to explaining a future shared objective in Athens, including the source-conditioned promise to Hayreddin. Claudio jokes about searching for a goal;Rafael is bemused. Do not turn Julio into a family member orerase FI substitutions. UI/control/name bindings are pending.',
129: 'After a two-choice confidence check, Julio describes a commercial progression: Madeira andits goods, Lisbon-Ceuta-Madeira trading, thenLas Palmas andVerde, more fleet holds/larger ships/market share, possible new goods throughcommercial investment,andoptional New World expansion. Secure a commercial foothold doesnot automaticallymean conquer a city. Preserve investment/market availability conditions andthe optional nature of long-distance expansion. This is a complete tutorial exchange,notreal-world trading guidance.',
132: 'Both sides prepare for a decisive naval battle. Rafael andalternative companions rally;enemy speakers contemptuously call them Portuguese rebels against the Spanish Empire andrelay battle orders. Preserve perspective, varied enthusiasm andprofessional commands without inventing participant ranks orclaiming every conditional companion speaks inone natural event. Source proper-name androle bindings remain pending.',
133: 'Julio proposes bringing his granddaughter Cristina,askilled sword user. Claudio’s masculine-adventure objection nearly exposes a woman already present;Arcadius warns him withthe sourcenickname Clau. A pain reaction andparenthesized asides lead to grudging agreement. Preserve the source’s gender/identity-reveal context, playful reprimand andRafael’s third-person mention ofArcadius,withoutinventing a physical action,recipient,romance orfamily tie. Julio is genuinely Cristina’s grandfather. He is puzzled,thenidentifies London asthe destination.',
134: 'A surprise pirate ambush overwhelms response. Claudio recognizes a flag,Janus knows the pirate’s dangerous reputation,andClaudio warns FI before a cry of pain. Arcadius andRafael react;Claudio minimizes his wound. Rafael orders retreat,andafterescaping proposes a port. Claudio specificallyrules out Amsterdam. Preserve danger,the reaction chain andthe distinction between a scratch claim andactual injury severity. The pirate’s approved spelling is pending;no outside biography is added.',
135: 'A flirtatious companion presents relationships withtavern girls as an adventurer’s source of useful information,thenrecommends gifts tailored toeachwoman’s interests. Sakura/Osaka andthe North Sea robe are a concrete example. Rafael innocently rationalizes the companion’s repeated flirting as professional necessity;the companion stammers,thenencourages imitation. Preserve the joke anddistinct voices,notanarrator’s endorsement ornewromance. Proper item/role labels remain pending.',
}

if __name__ == '__main__':
    assert not OUT.exists()
    packet_path, choices_path = ROOT/'clean_source_packet.json', ROOT/'clean_choice_objects.json'
    packet, choices = map(load,[packet_path,choices_path])
    ordinary = [r for g in packet['groups'] if 127 <= g['block'] <= 135 for r in g['records']]
    captions = [r for r in choices['records'] if r['block'] in [127,129]]
    assert len(ordinary) == sum(map(len,TEXT.values())) == 135 and len(captions) == len(CHOICES) == 4
    assert not [g for g in packet['groups'] if g['block'] in [130,131] and g['records']]
    records = []
    for row in ordinary+captions:
        meaning, draft = CHOICES[row['id']] if row['id'] in CHOICES else TEXT[row['block']][row['source_reference']['record_index']]
        value = deepcopy(row)
        value.update(source_meaning=meaning,independent_English_draft=draft,source_exchange_context=CONTEXT[row['block']],
            source_names_roles_terms_controls_anddynamic_bindings_pending=True,current_English_comparison_pending=True,
            no_blanket_historical_English_exposure_claim=True,
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),new_credit=0)
        if row['id'] in ['DK4_MES_B134_R0015','DK4_MES_B135_R0043','DK4_MES_B132_R0013']:
            value['proper_name_oritem_label_spelling_provisional_until_approved_native_binding'] = True
        if row['block'] in [127,128,129]:
            value['clean_tutorial_meaning_saved_native_controls_andUI_label_comparison_pending'] = True
        records.append(value)
    assert len({r['id'] for r in records}) == len(records) == 139
    save(OUT,dict(clean_packet=str(packet_path),clean_packet_sha256=sha(packet_path.read_bytes()),
        clean_choice_objects=str(choices_path),clean_choice_objects_sha256=sha(choices_path.read_bytes()),
        records=records,complete_blocks=list(range(127,136)),control_only_blocks=[130,131],ordinary_speeches=135,choice_labels=4,
        independent_drafts_precede_current_English_extraction_in_this_intake=True,
        no_blanket_historical_unexposure_orfinal_approval_claim=True,
        current_comparisons_names_terms_controls_allfive_gates_anddisplay_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('139 additionalclean meanings/independent drafts:135 speeches+four choice captions acrossnine whole blocks.254 of351 source drafts saved;97 remain. No final gates orcredit.')
