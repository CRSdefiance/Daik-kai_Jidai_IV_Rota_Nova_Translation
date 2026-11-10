"""Seal21 complete clean-source help meanings and independent logical drafts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
DATA={
0:('Help Contents',
   'See [[1|About the Game]], [[11|Town Commands]], [[82|Commands at Sea]], [[103|Shared Commands]] and [[143|Game Data]]. The [!] mark points out useful tips.',
   'Contents links to the game overview,town,sea,shared commands anddata explanation. The exclamation marker identifies useful information.',
   'Keep all five original destinations in order. The marker representation needs binding to the existing Help presentation before final approval.'),
1:('About the Game',
   'Learn about the game and your objectives. See [[2|Game Overview]], [[3|Game Objectives]], [[6|Choosing a Protagonist]] and [[10|Game Over]].',
   'This section explains the game overview andobjectives,andlinks to overview,objectives,protagonists andgame over.',
   'Use a direct help introduction. Preserve the four destinations andavoid inventing a marketing subtitle.'),
2:('Game Overview',
   'Explore the seas with your companions. The world is divided into seven sea regions, and you lead a faction based in one of them. Several factions compete in each region. Trade and battle with your rivals as you strive to become the strongest power in every region.',
   'A maritime adventure with companions. Seven sea regions,one faction led bythe protagonist witha base inone region,multiple factions ineach;compete throughtrade andcombat toward supremacy everywhere.',
   'Companions are characters,not a multiplayer claim. Keep seven regions andthe separate trade/combat routes to regional power.'),
3:('Game Objectives',
   'Each protagonist has a different goal at the start: Rafael wants to become an accomplished sailor; Lil wants to make a fortune; Hodram wants to make his navy the strongest in the world. Whichever character you choose, collect all seven Proofs of Conquest and achieve supremacy in every sea region to complete the game. See [[4|Proofs of Conquest]].',
   'Initial goals differ:Rafael becoming a capable navigator,Lil earning much money,Hodram making his own navy world strongest. Everyprotagonist clears bycollecting seven proofs andbecoming supreme across allregions.',
   'Retain allthree distinct motivations andboth parts ofthe final objective. Do not imply that Rafael seeks wealth orHodram simply wants money.'),
4:('Proofs of Conquest (Game Objectives)',
   'A Proof of Conquest is an item that shows the greatest strength in a sea region. There is one in each region. Searching at random will never uncover one: gather information from people and follow the clues. Rumor has it that an item called a mysterious trinket can guide sailors to a Proof of Conquest. See [[5|Mysterious Trinkets]].',
   'Eachregion hasone item showing greatest regionalstrength. Blindsearching cannot findit;information andclues matter. A smallmysterious item isrumored toguide sailors toproofs.',
   'Keep the anti-random-search warning andthe rumor qualifier. Mysterious trinket is a provisional source-based term requiring native item/Help consistency binding.'),
5:('Mysterious Trinkets (Game Objectives)',
   'An item known as a mysterious trinket is said to lead adventurers to a Proof of Conquest. What this item is, and how it guides them, remain unknown.',
   'Rumor saysa certain smallitem leadsto a proof. The item identity andthe way itguides adventurers arenot yet known.',
   'Preserve uncertainty about boththe object andits mechanism. Do not add coordinates,a map,magic,an item count orautomatic discovery.'),
6:('Choosing a Protagonist',
   'You can initially choose from three protagonists. Each has different advantages and a different level of difficulty. See [[7|Rafael Castor]], [[8|Lil Argot]] and [[9|Hodram Joakim Bergstrom]].',
   'Initially three protagonists areavailable;their difficulty andbenefits differ. Links nameRafael Castor,Lil Argot andHodram Joakim Bergstrom.',
   'Initially is essential:do not assert that onlythree characters can everbe selected. Approved name locks andLil Argot glossary spelling arepreserved.'),
7:('Rafael Castor',
   'A Portuguese boy who becomes a sailor, inspired by the many adventurers who sailed from Lisbon before him. He has plenty of companions from the start, making him easy to play. His base is Lisbon in the Mediterranean. His [[37|Military Investment]] costs are 20 percent lower than normal. Finding ruins or items gives twice the normal increase in [[184|Power]].',
   'Portuguese boy inspired byLisbon predecessors becomesnavigator. Many earlycompanions makeplay easy;baseLisbon/Mediterranean. Militaryinvestment costs80percent ofnormal;power gains forruins/items discoveries aredoubled.',
   '80 percent ofnormal means20 percent less,not an80 percent discount. The doubledgain isfor discoveries,not allactions. Retain the game’s Mediterranean classification ofLisbon.'),
8:('Lil Argot',
   'A Dutch woman who sets out to make a fortune through world trade. She starts with little money and many powerful rivals nearby, making her challenging to play. Her base is Amsterdam in the North Sea. She sells trade goods for 5 percent more than normal. Selling goods that are in fashion gives twice the normal increase in [[184|Power]].',
   'Dutch woman pursuinggreatwealth throughworldtrade. Lowfunds andstrong nearbyearlyenemies meanhighdifficulty;baseAmsterdam/NorthSea. Tradegoods saleprices5percent higher;powergain sellingfashionablegoods doubled.',
   'Do not turn the5 percent sale benefit intoa purchase discount. Keep the fashion-specific power bonus separate fromordinary trading.'),
9:('Hodram Joakim Bergstrom',
   'A Swedish admiral leading his underfunded navy, determined to make it the strongest in the world. His military position gives him good ships from the start, but powerful rivals are nearby. His base is Stockholm in the North Sea. His country rewards him for winning battles against other factions. Victories give twice the normal increase in [[184|Power]].',
   'Swedish admiral leads budget-poorSwedishnavy andstrives forworldstrongest. Militarystatus grantsgood startingships despitepowerfulnearbyrivals;baseStockholm/NorthSea. Countryreward forvictory versusotherfactions;victorypowergain doubled.',
   'Admiral andnavy areexplicit here. Do not invent a king,a salary,the rewardamount orshipclasses. Joakim andHodram remain user-approved.'),
10:('Game Over',
   'The game ends if any of these happens: your faction has no [[150|Market Share]] in any town; every ship in your fleet is sunk or captured in battle; or every ship in your fleet has no sailors left.',
   'Gameover ifownfactionshare reacheszero everywhere;allships ofownfleet are sunkorcaptured inbattle;or allships ofownfleet havezero sailors.',
   'Keep three alternative conditions. This is not losing one town,one ship,one crew member,all officers,or everyregionalfleet worldwide.'),
11:('Town Commands',
   "Select a building's sign to use its commands. Commands marked Cities Only are available only in [[145|Cities]]. See [[12|Tavern]], [[21|Trade House]], [[26|Guild]], [[34|Inn]], [[35|Palace/Governor's Office]], [[42|Square]], [[44|Shipyard]], [[73|Port]], [[144|Town Data]] and [[103|Commands in Towns and at Sea]]. [!] You may also be able to visit nearby [[80|Ruins]] and other sites.",
   'Towncommands execute byselecting building signs. Cities-only commands requirecity-class settlement. Ten command/datalinks andconditional access toruins etc.',
   'Distinguish general towns fromthe Cities settlement class. Keep palace andgovernor functions together withoutinventing a rank;all12 binary destinations remain inoriginalorder.'),
12:('Tavern',
   'Recruit sailors, gather information and more. [!] Many towns in Arab cultural regions have no taverns for religious reasons, making it harder to recruit sailors. Be careful about starting battles there. See [[13|Order a Drink]], [[14|Buy a Round]], [[15|Recruit Sailors]] and [[16|Plan a Scheme]].',
   'Taverns recruitcrew andgatherinformation. Many Arab-cultural-region towns lacktaverns forreligiousreasons,so recruiting ishard andrashly startingbattles dangerous. Fourcommandlinks.',
   'Preserve the source cultural context andmany qualifier. Describe this gameworld limitation respectfully;do not add a universal claim aboutpeople orreligion.'),
13:('Order a Drink (Tavern)',
   'Order a drink for 5 to 10 gold coins. You may hear about nearby towns or other factions. [!] Tavern women in [[145|Cities]] are well informed, so take the time to talk with them. You might even learn where to find an item.',
   'Costs5–10gold. Mayhear localtown/factioninformation. Citytaverns havewomen whotalk withyou andknowinformation;activeconversation mayrevealitemlocations.',
   'Keep the exactcostrange andpossibility qualifiers. Source doesnot prove that everywoman is a barmaid,romantic partner,proprietor orrelative.'),
14:('Buy a Round (Tavern)',
   'Treat the people in the tavern to drinks. You can hear about nearby towns and other factions, and you may learn about items. Buying a round before you [[15|Recruit Sailors]] makes it easier to attract a crew.',
   'Buydrinks for tavernpatrons;learn nearbytown/factioninformation andpossibly iteminformation. Doingthis beforecrew recruitment helpsattractsailors.',
   'Keep the recruitment preparation benefit withoutguaranteeing a fullcrew ormaking drinks mandatory. No price isstated here.'),
15:('Recruit Sailors (Tavern)',
   "Recruit sailors for your ships. Towns with higher Growth attract more sailors at once, but hiring them costs more gold. If more sailors arrive than you need, the extras are dismissed immediately. Buying drinks beforehand makes recruiting easier. Once they arrive, use [[139|Assign Sailors]] to distribute them among your fleet's ships.",
   'Recruitshipcrew. Higher-town-development yields more atonce butneeds moregold. Excessarrivals aredismissed onthespot. Drinkshelpbeforehand;thenassign recruits toeachfleetship.',
   'Keep recruitment distinct fromsubsequent shipassignment andautomatic excessdismissal. Growth andAssign Sailors require exact current UI binding beforefinalwording.'),
16:('Plan a Scheme (Tavern)',
   'Plot against other factions. This command is available only when your [[118|Strategist]] has an idea. It costs 1,000 gold coins, and the plan may fail. You cannot use it in a sea region with no other factions. For schemes other than Forge Documents, you must have visited a town where another faction has [[150|Market Share]]. See [[17|Lure a Fleet]], [[18|Forge Documents]], [[19|Spread Rumors]] and [[20|Bribery]].',
   'Strategist idea makes schemesavailable;1000gold;failurepossible. Unavailable withoutotherregionalfactions. All butforgeddocuments requirehavingvisited atown withotherfactionshare. Fourcommandlinks.',
   'Preserve the exception andall eligibility rules. Do not promise success,add a fee refund,or implythat every targettown hasbeen visited. Strategist/menu labels awaitUI binding.'),
17:('Lure a Fleet (Tavern > Schemes)',
   "Lure another faction's fleet to a town you choose. Select one destination town in the sea region.",
   'Draw anotherfactionfleet toone selectedtown intheregion.',
   'Do not add a battle,a trap,a fleetcapture orautomatic hostility asan outcome.'),
18:('Forge Documents (Tavern > Schemes)',
   'Forge documents to turn two other factions against each other. There must be at least two other factions. Choose the two you want to make hostile to one another.',
   'Whenmultiple otherfactions exist,forge documents withwording thatmakes twofactions hostile;choosethose two.',
   'Hostility isnot automatically a formal declaration ofwar. Preserve the two-other-faction requirement andplayerselection.'),
19:('Spread Rumors (Tavern > Schemes)',
   "Spread damaging rumors about another faction in a town you choose within the sea region. This reduces that faction's market share there. Your strategist will not think of this scheme if their ability is too low.",
   'Spreadotherfactionbadreputation inone chosentown inregion,loweringtargetsharethere. Lowstrategistability prevents theidea.',
   'Ability is an eligibility condition,not a claimthat strongerstrategists remove a largeramount. No fixedloss orsuccessguarantee isadded.'),
20:('Bribery (Tavern > Schemes)',
   'Bribe a broker in a town where another faction operates to take its market share. Select one town in the sea region. Your strategist will not think of this scheme if their ability is too low.',
   'Bribe anintermediary in a town withanotherfaction toseizeotherfactionshare;chooseonetargettown inregion. Lowstrategistability prevents theidea.',
   'Broker preserves the intermediary role. Do not replace them witha governor,official,spy orcrewmember orclaimthat everysharepoint isstolen.'),
}

if __name__=='__main__':
    source=ROOT/'clean_HELP_source_packet.json';corrected=ROOT/'clean_HELP_source_packet_v2.json'
    output=ROOT/'T00_T20_clean_meanings_andindependent_drafts_v1.json'
    assert not output.exists() and not corrected.exists()
    packet=deepcopy(load(source));assert set(DATA)==set(range(21))
    exposure={21,23,103,105,127,134,144}
    for row in packet['records']:
        if row['topic_id'] in exposure:
            row['earlier_English_unconsulted']=False
            row['exposure_note']='Existing general-help producer was read for its compiler/API context before this clean packet;its older prose was visible. No independent-before-English draft claim ismade forthese nonselected topics.'
    packet.update(previous_source_packet=str(source),previous_source_packet_sha256=sha(source.read_bytes()),
        source_first_independent_draft_claim_limited_to_selected_T00_T20=True,
        no_English_exposure_for_selected21_topics=True,existing_producer_exposure_topic_IDs=sorted(exposure),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(corrected,packet)
    rows=[]
    for row in packet['records']:
        index=row['topic_id']
        if index not in DATA:continue
        assert row['earlier_English_unconsulted']
        heading,english,meaning,note=DATA[index]
        parsed=[];at=0
        import re
        parsed=[int(m[1]) for m in re.finditer(r'\[\[([0-9]+)\|[^\]]+\]\]',english)]
        assert parsed==row['original_link_IDs'],(index,parsed,row['original_link_IDs'])
        assert english.isascii() and heading.isascii() and '\n' not in english
        rows.append(dict(**row,faithful_source_meaning=meaning,independent_heading_draft=heading,
            independent_English_draft=english,localization_note=note,
            necessary_linked_source_context_topic_ids=[37,80,82,103,118,139,143,144,145,150,184],
            current_English_comparison_pending=True,final_UI_term_marker_binding_andformatting_pending=True,
            new_completion_credit=0))
    assert len(rows)==21
    save(output,dict(format='dk4-clean-help-source-meanings-independent-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_packet=str(corrected),source_packet_sha256=sha(corrected.read_bytes()),file_path=packet['file_path'],
        source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],source_archive_sha256=packet['source_archive_sha256'],
        records=rows,independent_drafts_precede_first_selected_current_English_extraction=True,
        approved_names_bound_to='docs/glossary.md',approved_names_glossary_sha256=sha(Path('docs/glossary.md').read_bytes()),
        provisional_terms=['Mysterious Trinket','Power','Strategist','Growth','Assign Sailors','scheme command names','tip marker'],
        complete_topics_not_individual_sentences=True,all_current_help_appendices_andearlier_translations_to_be_preserved=True,
        current_English_unextracted_for_selected21=True,no_new_completion_credit=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Sealed21 complete source meanings/independent drafts;all original links/numbers/conditions preserved. Current-English comparison,term binding andall display checks remain;zero credit.')
