"""Seal the remaining Help source meanings and22 connected Info/data drafts before fresh old-English extraction."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

PACKET=Path('work/analysis/Shared_HELP_early_topics_clean_20261104/clean_HELP_source_packet_v2.json')
OUT=Path('work/analysis/Shared_HELP_T133_T201_clean_20261105/clean_meanings_andfirst22_drafts_v1.json')
MEANINGS={
133:'Complete required-ability table,16 positions in source pair order: Mast Sailing80;Lookout Observe70;Deck Health30;Survey Survey120;Helm Sailing60;Captain Command30;Mate Social100;Quarters Swords90;Battery Aim90;Lumber Survey130;Sickbay Observe150;Galley Aim70;Nursery Health130;Chapel Social160;Tactics Tactics120;Purser Finance100.',
134:'Info displays navigator,ship,fleet,Golden Route record andancient-map information;five original destinations/order.',
135:'Select navigator fromlist toview character data;preserve158 link;do not invent a restriction toprotagonist.',
136:'View data foreach fleet ship;select ship fromlist;preserve195 link.',
137:'View fleets belonging toyour faction;select fleet fromlist. Selectingregionalfleet allows delegation-policy changes.',
138:'Select item toview description/item screen;some types canbe equipped/used withsource square button. Unrelated-to-assigned-role equipment makes wearer name red;recommend re-equipping someone else orchangingrole. Current DSbutton pending.',
139:'Assign sailors toships;needed/current/max per ship. SourceD-padleft/right changescurrent per ship;autodistributionavailable. Belowrequired crewslows ship. Policies prioritizeflagship,equalizefractionofmaximum(not equalheads),assignonlyminimum. DScontrols/nativepolicylabels pending.',
140:'Functions include save/load,quit andoption settings;no invented extra functions.',
141:'Record ofGolden Routes discovered;preserve discovery201/report81 links.',
142:'Ancientmap reputedlyshows greattreasure;torntomultiplefragments;visitguildsindifferenttowns tocollectfragments. Preservelegendary/reportedstatus,notcertainnewtreasure facts.',
143:'Hub explaining town,sea,character,faction,tradegoods andshipdata;all6originaldestinations/order.',
144:'Visited-town data selectedonRouteMap;type,culture,condition,growth,arms,share andlocalgoods links. Unvisitedtown data notclaimedavailable.',
145:'Settlementsize affectsavailablecommands. Citylarge,Portsmall,Villagecannotland,resupplyonly. Events canchangeVillageintoPort;notguaranteed.',
146:'Culturalregion affects tradegoodsprices andbuilding signs/availablecommands;do notinventnationalityorarchitecturefacts.',
147:'Towncondition affectsprices:Normalordinary;Warweaponsupothersdown;Plaguefood/medicineupothersdown;Faminefoodupothersdown;Prosperityallup;Depressionalldown;Shortageaffectedcategoryup. All7sourcecases/order.',
148:'TownGrowth riseswithCommercialInvestment;mayaddlocalgoods;alsochangesrecruitablecrewcount andavailablecannontypes. No inventednumericthreshold.',
149:'TownArms riseswithMilitaryInvestmentatPalace/Governor;higherArms meanslesslikelytosurrenderwhenattacked.',
150:'Share setspercentoflocalincominggoodsbuyable;1percentallowsunlimitedsales. CanincreasebyCommercial/MilitaryInvestment andIntro/Recommendationletters,butfirst1percentrequiresPalace/Governorcontract. HomeportaddsHomePortPointsbonusshare;exclusivecontractlink.',
151:'100percentshare createsexclusivecontract/control,monthlytribute andtownattacksonatwarfactions. Cannotnormallycontractatotherfactionexclusiveport;Intro/Recommendationletter orwarwithcontrollingfaction needed. No mandatorybattlewin invented.',
152:'Localgoodsarethose soldbytown;higherGrowthorbringingRawMaterialsmayaddgoods;restockattheirrestockmonths. Do notclaimallgoodsreplenishmonthly.',
153:'Hub foronsea data:coordinates,food/water,sailors,fatigue;fourlinks/order.',
154:'Currentlatitude/longitude visiblewithhigh-abilitySurveyor;noinventednumericthreshold;link123.',
155:'Food/waterbarrelsremaining;zerocausescrewfatiguetoincreasedramatically.',
156:'Totalfleet sailorcount;zeromeansGameOver,notmerelyzerosailorsononeship.',
157:'Crewfatigue:at100sailorsbegintodecrease;highfatiguecanleadtomutiny. Notguaranteedinstantmutinyat100.',
158:'Characterdatahub:mood,physicalcondition,basicattributes,HP/Health,level,skills,equippeditems/weapons/armor. Sevenlinksinsourceorder.',
159:'Sixmentalstateshigh,energetic,relaxed,normal,irritable,confused;lasttworeduceworkefficiency. Cabin/RecreationRoomassignmentsrestorestate. Nativeconditionlabels pending.',
160:'Sixphysicalstateshealthy,fatigued,lightlywounded,severelywounded,neardeath,plague. Poorconditionreducesorpreventswork. Cabinrestorescondition;plagueneedsSurgeonusingmedicine/items. Do notclaimCabin alonecuresplague.',
161:'Basicattributesrepresentpotentialandaffectskills;sixoriginalattributelinks/order.',
162:'Bodilyhardiness;highermeanshardertoknockdown. Nativebasic-attribute labelpending;notautomatically equatedwithHealthskill.',
163:'Speedanddexterity;highervalueshelpincombat. Noinventedattack/speedformula.',
164:'Charismaandmagnanimity;highmakesiteasiertowinpeopleover,notphysicalbeautyalone.',
165:'Wisdomandknowledge;highhelpshandleproblemswell. No inventedlearning/magicbonus.',
166:'Strengthofwill;highhelpsremaincalmincrises. Distinguishbasicattribute fromcurrentmentalstate159.',
167:'Goodfortune;highmakesescapingdanger/crisiseasier,notguaranteedimmunity.',
168:'HPfallsfromwoundsincludingduels;zeroresultsneardeath,notdeath. Inn/Cabin/RecreationRoomgraduallyrestoreHP. HealthdeterminesmaxHP/hardiness;highresistsillness andsuitsAnimalKeeper/Deckhand. Relatedbasicattributesbodilystrengthandwill;all4source links.',
169:'Voyaginglevel;increaseswithsailingandotherexperience. No inventedXPformula.',
170:'Skillsindicatesuitabilityforjobs;individualstartingvaluesvaryandriseatlevelup;equipmentraisesonlysomeskills. Tenlinksinoriginalorder,includingHP/Health.',
171:'Command:leadcrewandcompanionsascaptain/admiral;highsuitsleadership;relatedWillandCharm. NativeCommandalreadybound.',
172:'Sailing:shiphandling;highmakeshandlingquicker,suitsHelmsman/SailHandler;relatedAgilityandWill.',
173:'Aim:concentrationinselectingtarget;highhelpscannonaccuracyandcooking,suitsGunner/ChiefCook;relatedAgilityandLuck.',
174:'Survey:surveyingandchartdrawing;highallowsaccuratepositionacrosswiderarea,suitsSurveyor/Shipwright;relatedAgilityandIntellect. Sextantandsimilaritemsraiseskill;recommendgiveSurveyor. Sextantitemlabelpending.',
175:'Social:diplomaticaptitude;suitsFirstMate/Missionary;relatedIntellectandCharm. AvoidwrongoldSpeechstatlabel.',
176:'Finance:accounting;highhelpsbargainlowerbuyingandhighersellingprices,suitsPurser;relatedIntellectandWill.',
177:'Tactics:cunning/strategicresourcefulness;highmakesinspirationforschemesmorelikely,suitsStrategist;relatedIntellectandLuck.',
178:'Swords:swordaptitude;highhelpsboardingandduels,suitsBoardingLeader;relatedbodilystrengthandAgility.',
179:'Observe:spotthingsanddetectdanger;highhelpsseefarawayandtreatailments,suitsLookout/Surgeon;relatedWillandLuck.',
180:'Currentlyequippeditem/weapon/armor. Selectingemptyslotenablesequipping;selectingoccupiedslotremovesit. NoinventedDSbutton.',
182:'Factionhomeportlocation;whenitsshareinthehomeportreacheszero,homeportmovestoanothertown;HomePortPointslink.',
183:'HomeportbonussharecalledHomePortPoints;flagsdisplaypoints,oneflagonepoint. Factionfleetcountbecomesthisbonusshare. Otherfactionscanonlytakebonussharethroughbattleorscheme. Exactfleet/pointrelationshipretainfornativebinding.',
185:'Relationshipwithprotagonistfaction;sourceclaimsthreelevels,butlinksNormal/Allied/AtWarplusSubordinate. TavernPlot/Guildletterscanchangeit. Resolve3statesversusauxiliarysubordinationcontext;donotsilentlyinventfourorignorethecount.',
186:'Alliance;cannotattackalliedfleets. Nearbyalliedfleetsmayhelpyouinbattle,notguaranteedassistance.',
187:'AtWar:approachingenemyfleetatseaautomaticallystartsbattle;enemyexclusivecontracttownsattack. MaytakeenemyshareviaCommercial/MilitaryInvestmentorbattle.',
188:'Normalrelationshipstate;noinventedfriendshipnumericthreshold.',
189:'Subordinatefactiondoesnotopposeprotagonistfleet. SuccessfulGuildlettersIntimidatecreatesubordination;IntimidaterequiresProof/ConquerorMarkitem4. Exactnativeitem/commandlabels alreadyreviewedbutrebindcurrent.',
190:'Friendshipratingshowsqualityofrelationshipwithprotagonist;higherisbetter. Distinguishnumericalratingfromdiplomaticstate.',
191:'Tradegoodsbought/soldatTradeHouse;town-specificlocalspecialties;pricesvarybytownandmarketconditions;basepricesvarybyculturalregion;type/gradelinks.',
192:'18tradegoodscategories. Goodsinsamecategorysharemarketpriceinfluence;tradingonegoodchangespricesofallgoodsinitcategory. Noinventeddirectionofeachtransaction.',
193:'Grades1through5,1best. IncreasedGrowthimproveslocalgoodsgrades. Highergradeisluxuryandlargerprofitsfrombuying/selling. Noinventedguaranteednetprofittransaction.',
194:'RawMaterialsitemsbecomelocalgoods. BringingtoTradeHousemayaddtownspecialty;cannotaddifunsuitablelocationoralready5goods. Severalcompatibletowns;chooseconvenient/high-shareone. Notguaranteedinanytown.',
195:'ShipdatafromInfo->ShipInfoselectship;durability,crewnumbers,water/food,square-sail,fore-aftsailperformance links/order.',
196:'Current/maxdurability;equalmeansundamaged;belowmaxcanberestoredwithShipyardrepair.',
197:'Required/current/maxsailorsper ship;changeallocationthroughAssignSailors139. Notfleetcountdata156.',
198:'Remainingwater/foodbarrels;zerosharplyincreasescrewfatigue. AnimalKeeper/ChiefCookslowfooddepletion;do notaddwaterbenefitforAnimalKeeper.',
199:'Square-sailperformance=main+secondary;higherimprovesspeedwithfollowingwind. Mainfrommainmastsaillayout/equipment;secondaryfromforemastforward/mizzenmastabaftmainmast. Someshiptypeslackoneorbothsecondarymasts.',
200:'Fore-and-aftsailperformance=main+secondary;higherimprovesspeedinheadwinds. Samecorrectmastlocation/equipmentlogic;donotclaimdirectlyupwindwithouttacking.',
201:'TradingprofitmarginmustEXCEED500percenttoDiscoverGoldenRoute;notatleast500. RecommendreporttoGuild;report81/log141links. Exactprofit-ratioUI/nativeformula pending binding.',
}
DRAFTS={
133:('Ability Requirements','Minimum abilities for each position: Mast: Sailing 80; Lookout: Observe 70; Deck: Health 30; Survey Room: Survey 120; Helm: Sailing 60; Captain\'s Cabin: Command 30; First Mate\'s Office: Social 100; Quarters: Swords 90; Battery: Aim 90; Lumber Room: Survey 130; Sickbay: Observe 150; Galley: Aim 70; Nursery: Health 130; Chapel: Social 160; Tactics Room: Tactics 120; Purser\'s Office: Finance 100.'),
134:('Info','View information about [[135|navigators]], [[136|ships]] and [[137|fleets]], plus the [[141|Golden Route Log]] and [[142|Ancient Map]].'),
135:('Navigators','Select a navigator from the list to view their [[158|character data]].'),
136:('Ship Info','View information about the ships in a fleet. Select a ship from the list to view its [[195|ship data]].'),
137:('Fleet Info','View information about your faction\'s fleets. Select a fleet from the list to view its data. Select a regional fleet to change its assigned policy.'),
138:('Items','View item descriptions, equip items or use them. Select an item from the list to open its item screen. Depending on the item, press Y to equip or use it. [Tip] If an equipped item does not help its wearer\'s assigned role, their name appears in red. Consider giving the item to another navigator or changing the wearer\'s assignment.'),
139:('Assign Sailors','Assign sailors to your ships. Each ship shows its required, current and maximum crew. Press left or right on the D-pad to change the number aboard a ship, or assign everyone automatically. Ships with fewer than the required sailors move more slowly. Flagship First prioritizes the flagship. Balance fills ships to equal proportions of their maximum crews. Minimum assigns only the required crews.'),
140:('Functions','Save or load your game, quit, or change the option settings.'),
141:('Golden Route Log','View information about the Golden Routes you have discovered. See [[201|Discover a Golden Route]] and [[81|Report a Golden Route]].'),
142:('Ancient Map','The Ancient Map is said to reveal the location of a great treasure. It has been torn into several fragments. [Tip] Visit [[26|Guilds]] in different towns to collect the map fragments.'),
143:('Data Guide','An explanation of the information shown for [[144|towns]], [[153|sailing]], [[158|characters]], [[181|factions]], [[191|trade goods]] and [[195|ships]].'),
144:('Town Data','Select a town you have visited on the Route Map to view its information. See [[145|City or Port]], [[146|Culture]], [[147|Condition]], [[148|Growth]], [[149|Arms]], [[150|Share]] and [[152|Local Goods]].'),
145:('City, Port or Village','The size of a settlement determines which commands are available there. Cities are large settlements; ports are smaller ones. You cannot land at a village, but you can take on supplies there. Events may turn a village into a port.'),
146:('Culture','The cultural region a town belongs to affects trade goods prices. Building signs, and the commands available there, also vary by cultural region.'),
147:('Condition','A town\'s condition affects prices. Normal: ordinary prices. War: weapons rise in price; other goods fall. Plague: food and medicine rise; other goods fall. Famine: food rises; other goods fall. Prosperity: prices generally rise. Depression: prices generally fall. Shortage: prices rise for the category in short supply.'),
148:('Growth','Shows how developed a town is. [[23|Commercial Investment]] at the Trade House raises Growth. Higher Growth may add new local goods. It also affects how many sailors you can recruit and the types of cannon you can fit.'),
149:('Arms','Shows how well armed a town is. [[37|Military Investment]] at the Palace or Governor\'s Office raises its Arms rating. The higher the rating, the less likely the town is to surrender when attacked.'),
150:('Share','Your share determines what percentage of a town\'s incoming local goods you can buy. With even 1 percent, you can sell without limit. Raise your share through [[23|Commercial Investment]], [[37|Military Investment]], a [[38|Letter of Introduction]] or a [[39|Letter of Recommendation]]. You must obtain your first 1 percent through a [[36|contract]] at the Palace or Governor\'s Office. At your faction\'s home port, its [[183|Home Port Points]] add bonus share. See [[151|Exclusive Contract]].'),
151:('Exclusive Contract','Reach 100 percent share in a town to obtain an exclusive contract and bring it under your faction\'s control. You receive monthly tribute, and the town attacks factions you are at war with. You cannot obtain a normal contract with a town under another faction\'s exclusive contract. Use a [[38|Letter of Introduction]] or [[39|Letter of Recommendation]], or go to war with the faction that controls it.'),
152:('Local Goods','The trade goods a town sells. Higher Growth or the introduction of suitable raw materials may add new local goods. Goods are replenished when their [[24|restock month]] comes. See [[194|Raw Materials]].'),
153:('Sailing Data','Information shown while at sea. See [[154|Latitude and Longitude]], [[155|Food and Water]], [[156|Sailors]] and [[157|Fatigue]].'),
154:('Latitude and Longitude','Your current coordinates. They appear when you have a sufficiently skilled [[123|Surveyor]].'),
}

if __name__=='__main__':
    assert not OUT.exists()and set(MEANINGS)==set(range(133,202))-{181,184}and set(DRAFTS)==set(range(133,155))
    packet=load(PACKET);path=Path(packet['source_ROM']);assert sha(path.read_bytes())==packet['source_ROM_sha256']
    raw=NdsImage.open(path).read_file('/COMMON/HELP.DK4');assert sha(raw)==packet['source_archive_sha256'];blocks=IlnkContainer.parse(raw).blocks
    sources={r['topic_id']:r for r in packet['records']};records=[]
    import re
    for n in sorted(MEANINGS):
        source=sources[n];assert source['source_hex']==blocks[n].hex();draft=DRAFTS.get(n)
        if draft:
            assert draft[1].isascii()and '\n'not in draft[1]and '  'not in draft[1]
            assert [int(t)for t in re.findall(r'\[\[(\d+)\|',draft[1])]==[r['topic_id']for r in source_links(blocks[n])],n
        records.append(dict(id=source['id'],topic_id=n,source_reference=source['source_reference'],source_hex=source['source_hex'],
            source_Japanese_with_link_IDs=source['source_Japanese_with_link_IDs'],source_meaning=MEANINGS[n],
            heading=draft[0]if draft else None,english=draft[1]if draft else None,speaker='Help narrator',
            context='Complete connected Info/Items/crew setup/data/skills/faction/trade/ship/Golden Route explanations133through201;181/184 are contextual source neighbors already completed, excluded from new credit.',
            localization_note='Draft from clean Japanese; native labels, controls, current comparison and complete display gates remain open. Preserve all numerical boundaries, conditional effects and original destinations.',
            review=dict(source=True,context=True,localization=False,naturalness=bool(draft),formatting=False),
            independent_draft_pending=not bool(draft),current_comparison_pending=True,native_binding_pending=True,new_credit=0))
    OUT.parent.mkdir(parents=True)
    save(OUT,dict(format='dk4-remaining-help67-clean-intake-first22-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_ROM=str(path),source_ROM_sha256=packet['source_ROM_sha256'],source_HELP_sha256=sha(raw),source_packet=str(PACKET),source_packet_sha256=sha(PACKET.read_bytes()),
        records=records,records_count=67,source_meanings=67,sealed_source_drafts=22,remaining_independent_drafts=45,
        earlier_English_exposure_disclosure='Earlier glossary work exposed133,170,172,173,177,178 and neighboring out-of-scope role articles; several Info/data headings and native stats/role labels are already known. Do not claim all old English was unseen. No fresh current-body packet for this67 has yet been extracted.',
        known_draft_binding_risks=dict(topic138='Provisional Y equip/use button; must bind this item consumer.',topic139='DS crew-adjustment controls and automatic-policy labels pending.',
            topic183='Bind fleet-count/home-port-point share relationship.',topic185='Reconcile source three basic relationships with separate subordinate link.',topic201='Bind strict greater-than500 and profit-ratio definition.'),
        all_current_comparisons_localization_native_display_andintegration_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Remaining67 clean meanings sealed;first22 Info/data logical drafts saved,45 drafts remain;no fresh current-body comparison or new credit.')
