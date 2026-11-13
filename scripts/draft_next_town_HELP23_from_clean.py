"""Seal clean meanings andfull article drafts for the next market-through-square group."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('work/analysis/Shared_HELP_early_topics_clean_20261104/clean_HELP_source_packet_v2.json')
OUT=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104')
TEXT={
21:('Trade goods andgather information;Source Item gifts may add local products,not guaranteed. Preserve all three command links anditem-category/local-product links.',
"Buy and sell trade goods, and gather information. [!] If you bring an item from the [[194|Source Items]] category to a town's market, you may be asked to give it to the town. Giving it may add a new [[152|local product]]. See [[22|Trade]], [[23|Commercial Investment]] and [[24|Market Info]]."),
22:('Trade only with own market share;price depends on town state;maximum stock depends on share andremaining supply;restock month;profitable route discovery;accountant bargaining/buyout;Lil5 percent sale bonus.',
"Buy and sell trade goods in towns where your faction has [[150|Market Share]]. Prices depend on factors such as the [[147|town's condition]]. The most you can buy depends on your market share and the stock remaining. Stock recovers in the [[24|restocking month]]. A high profit margin can lead to a [[201|Golden Route discovery]]. [!] An [[119|accountant]] may negotiate lower prices or let you buy out the stock. [!] Lil sells goods for 5 percent more."),
23:('Commercial investment1-20 units;cost perunit50 percentGrowth;raisesGrowth;share only whenunallocated orenemyowns share;higherGrowth mayaddlocalproducts.',
"Invest in the town's commerce, from 1 to 20 units at a time. Each unit costs gold equal to half the town's Growth. Investment raises Growth. Your [[150|Market Share]] also rises if the town's total share is below 100 percent, or if a faction [[187|at war]] with you holds a share there. Higher Growth may add new [[152|local products]]."),
24:('Market prices/restocking month;other towns cost50-200;redbuyprices meanin fashion;preservetrendlink.',
"View trade goods' market prices and restocking months. Information about other towns costs 50 to 200 gold coins. A red purchase price marks goods that are in fashion. See [[25|Trends]]."),
25:('Fashion increasesprice;natural ormissionary-created;bulk sales maygrantfree share orletters inmonopoly towns;lettersmayenablepreviouslyunavailablecontracts,noguarantee.',
"Goods that are in fashion rise sharply in price. Trends can arise naturally or be started by a [[117|Missionary]]. Selling large amounts of fashionable goods may earn you market share for free. In towns under an [[151|Exclusive Contract]], you may receive a Letter of Introduction or Recommendation instead. Take a [[38|Letter of Introduction]] or [[39|Letter of Recommendation]] to the governor's office, and you may be able to sign a contract in a town that would not let you before."),
26:('GuildCityonly fromheading;buy/sellitems,sendnegotiationletters,reportGoldenRoutes;AncientMaps soldthere;all3links.',
"Buy and sell items, send negotiation letters, and report Golden Routes. The guild also sells [[142|Ancient Maps]]. See [[27|Send Negotiation Letter]] and [[81|Report Golden Route]]."),
27:('Letters tootherfactionsinsameregion;deputyrole required;1000cost;mayfail;nootherfactions meansunavailable;allsixlinks.',
"Send a letter to another faction in the same sea region. You need a [[121|deputy]] to use this command. It costs 1,000 gold coins, and negotiations may fail. You cannot use it in a region with no other factions. See [[28|Goodwill]], [[29|Make Alliance]], [[30|Break Alliance]], [[31|Ceasefire]], [[32|Declare War]] and [[33|Intimidate]]."),
28:('Goodwillletterincreasesspecifiedotherfactionfriendshipslightly.',
"Send a friendly letter to another faction. Your Friendship with that faction rises slightly."),
29:('AgreementgreatlyincreasesFriendship,statusAllied,mayhelpinbattle notguaranteed.',
"Make an agreement with another faction. Your Friendship rises greatly, and your relationship becomes [[186|Allied]]. The faction may help you in battle."),
30:('BreakagreementlowersFriendship.',
"Break your agreement with another faction. Your Friendship with that faction falls."),
31:('Offerceasefiretoat-war faction;onlyeffectiveifaccepted;letterarrivingduringbattle discarded.',
"Offer a ceasefire to a faction you are [[187|at war]] with. If the other faction accepts, the fighting ends. A letter that arrives during a battle is discarded."),
32:('DeclarewarFriendshipfalls greatly,statusatwar;enemyPowerred;sharecanbetakenbyinvestmentorbattle.',
"Declare war on another faction. Your Friendship falls greatly, and your relationship becomes [[187|At War]]. A faction's Power appears in red while you are at war with it. [!] You can take market share from enemy factions through investment or battle."),
33:('Demandfactionsubordination;requiresregionalProofanddeputypersuasion>=200;doesnotsayguaranteedsuccess.',
"Demand that another faction become your subordinate. You can use this command only if you have that sea region's [[4|Proof of Conquest]] and your deputy has a Persuasion score of at least 200."),
34:('Inn1goldpernight;sailorFatiguefallsabout10;navigatorscondition/HP recover;strategistmaycollectfactionintel;crosscontrolcancelsconsecutiveresting,exactcontrolneedsbinding.',
"Stay at the inn for 1 gold coin per night. Each night reduces your sailors' [[157|Fatigue]] by about 10 and restores your navigators' condition and HP. [!] A [[118|Strategist]] may gather information about other factions while you stay. [!] To stop resting for consecutive nights, select the X."),
35:('Palace/governorcontracts,militaryinvestment;preserveall sixcommandlinks.',
"Sign a contract with the town or invest in its defenses. See [[36|Contract]], [[37|Military Investment]], [[38|Use Letter of Introduction]], [[39|Use Letter of Recommendation]], [[40|Lend Item]] and [[41|Retrieve Item]]."),
36:('1-20contractunitsgrantcorrespondingshare,enablestrade;cannotifalready3factionsorotherfactionstotal100.',
"Sign a contract with the town, from 1 to 20 units at a time. You gain [[150|Market Share]] according to the number of units, allowing you to trade there. You cannot sign a contract if the town already has contracts with three factions, or if other factions already hold a combined 100 percent share."),
37:('1-20militaryunits;cost50percentArmsorRafael40;raisesArmsandconditionalshare;surrenderresistanceandbetterships/cannons,noguaranteedimmunity.',
"Invest in the town's defenses, from 1 to 20 units at a time. Each unit costs gold equal to 50 percent of the town's Arms, or 40 percent for Rafael. Investment raises Arms. Your [[150|Market Share]] also rises if the town's total share is below 100 percent, or if a faction [[187|at war]] with you holds a share there. Higher Arms makes the town less likely to surrender when attacked and lets you buy better ships and cannons."),
38:('Marketletterintroduction;Portclassonly;existingcontract+5;otherwisecontractevenother100take1;notif3factionsorown100.',
"Give the ruler or governor a [[25|Letter of Introduction from the market]]. It works only in towns classed as Ports. If you already have a [[36|contract]], your [[150|Market Share]] rises by 5 percent. Otherwise, you can sign a contract. Even if other factions hold a combined 100 percent share, you can take 1 percent from them to sign. You cannot use the letter if the town already has contracts with three factions, or if you already hold 100 percent of its share."),
39:('Recommendationanytownclass;existingcontract+10;otherwisecontractevenother100take1;notif3factionsorown100.',
"Give the ruler or governor a [[25|Letter of Recommendation from the market]]. It works in towns of any size. If you already have a [[36|contract]], your [[150|Market Share]] rises by 10 percent. Otherwise, you can sign a contract. Even if other factions hold a combined 100 percent share, you can take 1 percent from them to sign. You cannot use the letter if the town already has contracts with three factions, or if you already hold 100 percent of its share."),
40:('Lendowneditemtoruler/governoronlyhomebase;monthlyrentbyvalue;cannotlendProof,ProofMaps,AncientMaps.',
"Lend an item you own to the ruler or governor at your home port's palace or governor's office. You receive rent each month while it is on loan, based on the item's value. You cannot lend a [[4|Proof of Conquest]], a map to a Proof, or an [[142|Ancient Map]]."),
41:('Retrieveitempreviouslylent;homebasepalace/governoronly.',
"Retrieve an item you have lent out. You can do this only at your home port's palace or governor's office."),
42:('Squareinformation;retailshopsignboards;TrendsInfoselectsignlearnfashionedgoods;DistributeGoodslink.',
"Gather information in the square, where retail shops display their signs. Select a sign under Trend Info to learn about goods that are [[25|in fashion]]. See [[43|Distribute Trade Goods]]."),
43:('Givegoodsfreelocalresidents;Missionaryrequired;maystarttrendnearbytowns,noguarantee.',
"Give trade goods to the townspeople for free. You need a [[117|Missionary]] to use this command. The goods you distribute may become [[25|fashionable]] in nearby towns."),
}

if __name__=='__main__':
    assert not OUT.exists() and set(TEXT)==set(range(21,44))
    source=load(SOURCE);records=[]
    for row in source['records']:
        topic=row['topic_id']
        if topic not in TEXT:continue
        meaning,draft=TEXT[topic]
        assert draft.isascii() and '\n' not in draft
        records.append(dict(id=row['id'],topic_id=topic,source_reference=row['source_reference'],source_hex=row['source_hex'],
            source_sha256=row['source_sha256'],source_Japanese_with_link_IDs=row['source_Japanese_with_link_IDs'],
            original_link_IDs=row['original_link_IDs'],clean_meaning=meaning,full_article_English_draft=draft,
            current_English_not_extracted_for_this_comparison_yet=True,
            no_wholly_unconsulted_prior_English_claim=topic in [21,23],
            first_draft_not_final_gate_orretention=True))
    OUT.mkdir();save(OUT/'clean_meanings_andfull_drafts_v1.json',dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        records=records,records_count=23,new_credit=0,translation_policy='natural-dialogue-v2',target_locale='en-US',
        prior_producer_English_exposure_disclosed_topic_IDs=[21,23],
        current_full_article_comparisons_all_fifth_gates_andintegration_pending=True,
        open_terms_andcontrol_bindings=['119 accountant role','121 deputy role andPersuasion score','194 Source Items category','local product152','command labels27-33','Inn34 cross cancel control','Proof-map item class40','Trend Info42'],
        no_manual_linebreaks_orprose_shortening=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Next23 complete clean-source meanings andfull drafts sealed;prior21/23 English exposure disclosed. Comparisons/terms/display/integration remain;zero credit.')
