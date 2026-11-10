"""Complete clean-first meanings/drafts,including early trade/crew/route tutorials."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
OUT = ROOT/'B136_B140_meanings_andindependent_drafts_v1.json'
TEXT = {
136: {
5: ('Claudio calls FI’s attention.', 'Hey, FI!'),
9: ('Rafael asks what is going on.', 'What is it?'),
14: ('Claudio excitedly reports hearing a rumor of a remarkable treasure.', 'I heard a rumor about some incredible treasure!'),
18: ('Rafael asks the treasure’s name.', "Oh? What's it called?"),
23: ('Claudio tentatively gives the named staff’s name;approved item spelling is pending.', "Something called the Guiding Staff, I think."),
26: ('Rafael asks what makes it remarkable.', "What's so incredible about it?"),
31: ('Claudio saw a Guild buying-list price higher than he had ever seen,andhasheard nobody has found the item yet.', "The Guild's buying list offered a higher price than anything I've ever seen! And apparently nobody's even found it yet!"),
34: ('Rafael asks him to get to the point.', 'And?'),
39: ('Claudio says finding it wouldmake them rich andenthusiastically urges immediate departure.', "If we find it, we'll be rich! Come on, let's go!"),
43: ('Rafael asks where they wouldbe going.', 'Go...? Go where?'),
48: ('Claudio circularly answers that they should go where the staff is.', "Where the Guiding Staff is, of course! Where else?"),
52: ('Rafael repeats the practical question.', 'And where is that?'),
57: ('Claudio admits he does not know.', "Huh? ...I don't know."),
60: ('Rafael points out that this gives them no way to search.', "Then how are we supposed to look for it?"),
65: ('Claudio concedes the point.', '...Good point.'),
69: ('Rafael chides Claudio for unreliable information andquestions whether the treasure even exists.', "Come on, think it through. With information that vague, we can't even be sure it exists."),
73: ('Claudio is deflated andconcedes the idea may not work.', "...Yeah, you're right. So much for that."),
76: ('He dejectedly wonders why he is so gullible orsimple-minded.', 'Why am I always such a sucker...?'),
79: ('Rafael notices Claudio’s dejection.', 'Clau...?'),
84: ('Julio affectionately addresses FI as a little boy out of old habit;no family relationship is asserted.', '...FI, kiddo.'),
88: ('Rafael greets Julio andasks him to stop using the childish familiar address.', "Oh, Julio. ...Would you please stop calling me 'kiddo'?"),
92: ('Julio apologizes for slipping into an old habit.', "Oh, sorry. Old habits, you know."),
95: ('Julio raises the subject of the named staff.', 'Well... About that Guiding Staff.'),
98: ('Rafael checks whether Julio means the treasure Claudio just mentioned.', 'The treasure Clau was talking about?'),
102: ('Julio offers to tell Rafael about it,leadingto two alternative responses.', 'Would you like to hear what I know?'),
116: ('The staff is said to guide people toward goodness,notnecessarily wealth ornavigation.', 'The Guiding Staff is said to lead people toward goodness.'),
120: ('Rafael asks whether it actually exists.', 'Then it really exists?'),
125: ('Julio limits the claim to legend.', 'According to legend, yes.'),
129: ('Rafael wonders where it is.', 'I wonder where it is...'),
134: ('Julio gives India as its rumored location.', 'They say it is in India.'),
138: ('Rafael overinterprets the legend as proof of existence;preservehis mistaken certainty.', 'Then it really does exist!'),
143: ('Julio again stresses that it is only a legend.', "Mind you, it's only a legend."),
147: ('Rafael regrets how he spoke to Claudio andresolves to apologize.', "I see. After what I said to him... I owe Clau an apology."),
152: ('He thanks Julio.', 'Thank you, Julio!'),
157: ('Julio tries to stop orcall after him.', 'Ah, wait!'),
161: ('Julio observes that Rafael has already left.', "Off he's gone."),
165: ('Julio hopes this will cheer Claudio,becausehis dejection makes the atmosphere gloomy andspoils Julio’s enjoyment ofdrinking.', "Well, that should cheer Claudio up. He's so gloomy when he's down that I can't even enjoy my drink."),
168: ('Julio had forgotten the staff legend andwonders whether FI really intends to seek it.', "I'd forgotten all about that legend, though. Is FI really going to look for it...?"),
179: ('He decides it does not matter andplans to invite Janus for a drink.', "Well, never mind. I think I'll ask Janus to join me for a drink."),
189: ('In the other branch,Rafael distrusts Julio’s story andaccuses him andClau ofplanning a trick.', "There you go again. You and Clau are trying to trick me, aren't you? I'm not falling for it."),
193: ('Julio is surprised anddenies that intent.', "What? I'd do no such thing."),
196: ('Rafael accuses them ofmaking him the butt ofjokes over drinks;the source food idiom is figurative.', "You want to make me the butt of your jokes while you drink. I know what you're up to."),
200: ('Julio repeats his denial,thenirritably gives up arguing.', "I said I'd do no such thing! ...Oh, never mind."),
203: ('He explains that he only approached because Claudio was dejected andhe hoped Rafael wouldhelp.', "Clau was feeling down after what happened. I only spoke to you because I hoped you could do something about it."),
206: ('Rafael is embarrassed to learn the actual intent andapologizes.', "What? Oh, is that why...? I'm sorry, Julio."),
210: ('Julio accepts his understanding andurges him to cheer Claudio up.', '...As long as you understand. Now go and cheer Clau up.'),
214: ('Rafael agrees.', 'Oh, yes!'),
219: ('Julio grumbles about looking after them,thenjokes that the mention ofdrinking has made him want a drink.', "What a handful they are. And all that talk of drinks... Now I want one myself."),
230: ('He decides to ask Janus for a drink.', "That's it. I'll ask Janus to join me for a drink."),
236: ('He chuckles mischievously andlooks forward to drinking.', 'Heh heh heh. Time for a drink!'),
},
137: {
6: ('The trading principle is buying goods cheaply andselling them at a higher price.', 'Buy low and sell high. That is the basis of trade.'),
9: ('Trading between the Mediterranean andAfrica can produce quick profits once such travel becomes possible.', 'Once you can sail between the Mediterranean and Africa, you can turn a quick profit.'),
13: ('Because long voyages are initially impractical,startlocally andlearn how things work.', "Long voyages are a bit much to start with, so try things out close to home."),
16: ('Watch prices in each town to find profitable opportunities.', 'Check the market prices in each town and look for a chance to make a good profit.'),
19: ('From the present Lisbon location,buying saffron oralmonds andselling around Ceuta is recommended.', 'Here in Lisbon, try buying saffron or almonds and selling them in Ceuta.'),
22: ('Few initial ships andholds limit the quantity that can be traded at once.', "You won't have many ships or cargo holds at first, so you can't trade much at once."),
26: ('A trading unit fills one cargo hold;thehold count determines buying capacity.', 'One unit of goods fills one cargo hold. The number of holds determines how much you can buy.'),
30: ('Market share also affects transaction quantity;highershare permits more trade.', 'Your market share also limits how much you can trade at once. The greater your share, the more you can trade.'),
44: ('Rafael asks how to increase market share.', 'Market share...? How do I increase it?'),
48: ('Where unclaimed share remains,investors at the palace ortradehouse receive a share.', 'If any market share is unclaimed, you can gain some by investing at the palace or trade house.'),
52: ('This can wait until profits andmore ships make it relevant;firsttry trading.', "Don't worry about that just yet. It matters once you've made some money and have more ships. First, give trading a try."),
60: ('Choose the confirmation command to finish the transaction once satisfied,thenpractice.', 'When everything looks right, choose Confirm to complete the deal. Now, give it a try.'),
},
138: {
6: ('The ship must be made operational,andthe party needs ordinary sailors to handle it.', "First, we need to get the ship moving. We can't manage it by ourselves. We'll need sailors."),
10: ('Offering drinks helps recruit sailors bydemonstrating the admiral’s generosity orlarge-heartedness.', 'A good way to attract sailors is to treat everyone to a drink. Show them what a generous admiral you are.'),
14: ('People appreciate free drinks,butinitially the needed crew can probably be recruited without this expense.', "Nobody minds a free drink. But at first, you should be able to find the sailors you need without buying a round."),
18: ('Julio prompts trying the recruit-sailors command to see how many willjoin.', "Now, let's see how many turn up when you choose Recruit Sailors."),
21: ('After recruitment,allocate sailors;withonly one ship,the flagship-priority setting is acceptable.', 'Next, assign your sailors. If you have only one ship, Flagship Priority will do.'),
25: ('More sailors reduce the number ofdays the fleet can remain at sea;takecare when hiring beyond requirements.', 'Adding sailors shortens the number of days you can stay at sea. Be careful about hiring more than you need.'),
29: ('Julio asks the player to try it.', 'Now, give it a try.'),
},
139: {
5: ('Julio asks FI whether things are going well andoffers to explain potentially confusing routes.', "FI, is everything going well so far? Routes can be a little confusing. Would you like me to explain them?"),
19: ('Agreements with neighboring towns orports establish a route connecting them.', 'Make agreements with neighboring towns or ports, and a route will connect them.'),
23: ('FO currently has agreements withLisbon andCeuta.', 'For example, FO has agreements with Lisbon and Ceuta.'),
27: ('Because these towns are neighbors,FO has a route between them.', 'Since those two towns are neighbors, FO has a route between them.'),
30: ('A connected route plus captain andsurveyor roles onthe Deck screen enables automatic travel.', 'With a Captain and Surveyor assigned on the Deck screen, you can use Auto Sail along an established route.'),
34: ('Rafael asks about the automatic-travel command.', 'Auto Sail?'),
39: ('Connected routes remove the need for individual steering orders;choosea destination andthe navigators willhandle sailing.', "As long as the routes connect, you needn't give every steering order. Just choose a destination, and we navigators will take care of the sailing."),
42: ('Select automatic travel at the port andchoose a destination fromthe route chart.', 'Choose Auto Sail at the port, then select your destination on the Route Chart.'),
55: ('Julio introduces a complication.', 'However...'),
59: ('Rafael reacts inquisitively.', '?'),
64: ('Nobody inthis fleet can currently fill the surveyor role.', "Nobody in this fleet can serve as Surveyor..."),
67: ('Claudio irreverently challenges the old man’s inability to survey despite his advice;no family relation is implied.', "You talk so big, old man, but you can't even do a little surveying?"),
71: ('Julio asks them to go toLisbon andbuy a sextant,sayinghe can manage withit.', "...Very well. Go to Lisbon and buy a sextant. With that, I'll find a way to manage."),
74: ('The item must be equipped toJulio specifically,notmerely bought orcarried.', "Don't forget to equip me with it."),
77: ('Rafael asks about equipment.', 'Equip?'),
82: ('Examining the purchased item willshow how;Julio again tells them tohead for Lisbon.', "Take a good look at the item after you buy it. You'll see. For now, head for Lisbon."),
85: ('Rafael agrees hesitantly.', 'Y-yes.'),
102: ('Julio encourages them to do their best.', 'Well, do your best.'),
},
140: {
5: ('Janus recommends investment at the palace orgovernor’s residence to raise town armament against attacks.', "If you want to raise a town's Arms against enemy attacks, invest at the palace or governor's residence."),
9: ('The speaker cites Portugal’s forts in towns onthe route tothe Indian Ocean as trading bases.', 'Portugal built forts in towns along the way to the Indian Ocean and used them as trading bases.'),
12: ('The resulting construction expertise shouldreduce the military investment needed toraise town armament compared withother nations;no exact discount is stated.', "Thanks to the building techniques developed there, we should be able to raise a town's Arms with less military investment than other nations need."),
16: ('Rafael acknowledges the useful information.', "I see. All right, I'll remember that."),
},
}
CHOICES = {
'SC0_B136_CHOICE_1086_0': ('Rafael accepts Julio’s offer to tell him about the staff.', 'Please, tell me.'),
'SC0_B136_CHOICE_1086_1': ('He dismisses the subject andrefuses more discussion;thefollowing accusation branch is not confident prior knowledge.', "No, I've had enough."),
'SC0_B137_CHOICE_704_0': ('He asks what market share means.', 'Market share?'),
'SC0_B137_CHOICE_704_1': ('He acknowledges understanding.', 'I see.'),
'SC0_B139_CHOICE_112_0': ('He politely accepts the route explanation.', 'Yes, please.'),
'SC0_B139_CHOICE_112_1': ('He declines because he already understands.', "No, thanks. I understand."),
}
CONTEXT = {
136: 'Claudio’s excitement over an expensive rumored treasure collapses when he cannot identify a location. Rafael’s practical criticism hurts him. Julio’s familiar childhood address irritates Rafael before an offer to share lore. Inone branch,Julio repeatedly limits the staff’s existence/location tolegend,butRafael mistakes this forcertainty andrushes toapologize. Inthe other,Rafael accuses Julio andClaudio ofmaking him the butt ofdrunken jokes;Julio reveals a sincere wish tocheer Claudio up. Both branches end withJulio deciding todrink withJanus. Preserve the shift fromnaivety throughhurt andapology tothe drinking punchline. The food metaphor is notliteral eating. No source familiar address creates a father/son relationship. The staff’s approved label remains pending.',
137: 'A complete first-trade tutorial:buy low/sell high,startnear Lisbon,saffron/almonds forCeuta,one hold pertransaction unit,andlimits fromhold count andmarket share. A two-choice question optionally leads tohowshare isgained byinvestment whereunclaimedshare remains. The mentor explicitlydefers this untilthe fleet grows,thenasks the player toconfirm a deal. Preserve capacity units andconditions;bind current command labels androles beforefinal gates.',
138: 'The recruiting tutorial explains whyordinary sailors areneeded,whybuying drinks canhelp,andwhythis extraexpense is probablyunnecessary atthestart. After recruitment,the player allocates sailors;Flagship Priority is sufficient forone ship. More sailors shorten endurance,sohiring beyond requirements needs care. Generosity ischaracter framing,nota newstat-bonus claim. Command labels andactual control bindings remain pending.',
139: 'An optional route tutorial explains neighboring-port agreements usingLisbon/Ceuta andFO,thenrequires bothCaptain andSurveyor roles forautomatictravel. Aftergiving instructions,Julio realizes nobody canyetfillSurveyor. Claudio teases him;Julio asksforLisbon’s sextant andexplicitlyrequires equipping ithimself. Preserve the comic obstacle afterthe practical explanation,noinventedfamily tie,andthe difference between buying andequipping. No historical instrument correction overrides thegame’s source. Labels/itemrolebindings remain pending.',
140: 'Janus offers military-investment advice,connecting Portugal’s fort-building onits Indian Ocean trading route toless investment needed forcityarmament. It isgame dialogue witha qualifiedexpected benefit,notanindependent historical/economic claim. Preserve thepalace/governor-office alternatives andavoidadding a numericaldiscount orcombatbonus. UIlabels andmechanics needthe establishednative bindings.',
}

if __name__ == '__main__':
    assert not OUT.exists()
    packet_path, choices_path = ROOT/'clean_source_packet.json', ROOT/'clean_choice_objects.json'
    packet, choices = map(load,[packet_path,choices_path])
    ordinary = [r for g in packet['groups'] if 136 <= g['block'] <= 140 for r in g['records']]
    captions = [r for r in choices['records'] if r['block'] >= 136]
    assert len(ordinary) == sum(map(len,TEXT.values())) == 91 and len(captions) == len(CHOICES) == 6
    records = []
    for row in ordinary+captions:
        meaning, draft = CHOICES[row['id']] if row['id'] in CHOICES else TEXT[row['block']][row['source_reference']['record_index']]
        value = deepcopy(row)
        value.update(source_meaning=meaning,independent_English_draft=draft,source_exchange_context=CONTEXT[row['block']],
            source_names_roles_terms_controls_anddynamic_bindings_pending=True,current_English_comparison_pending=True,
            no_blanket_historical_English_exposure_claim=True,
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),new_credit=0)
        if row['block'] in [137,138,139,140]:
            value['clean_tutorial_meaning_saved_native_controls_andUI_label_comparison_pending'] = True
        if row['block'] == 136:
            value['treasure_label_andsource_uncertainty_binding_pending'] = True
        records.append(value)
    assert len({r['id'] for r in records}) == len(records) == 97
    save(OUT,dict(clean_packet=str(packet_path),clean_packet_sha256=sha(packet_path.read_bytes()),
        clean_choice_objects=str(choices_path),clean_choice_objects_sha256=sha(choices_path.read_bytes()),
        records=records,complete_blocks=list(range(136,141)),ordinary_speeches=91,choice_labels=6,
        independent_drafts_precede_current_English_extraction_in_this_intake=True,
        no_blanket_historical_unexposure_orfinal_approval_claim=True,
        current_comparisons_names_terms_controls_allfive_gates_anddisplay_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Last97 clean meanings/independent drafts saved:91 speeches/six captions. All351 source objects nowdrafted beforecurrent-English extraction;comparison/control/name/display gates remain.')
