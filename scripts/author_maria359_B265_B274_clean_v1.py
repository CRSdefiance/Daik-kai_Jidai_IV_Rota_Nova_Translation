"""Complete the clean-only359 intake; preserve alternatives and source facts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save,load

ROOT=Path('work/Maria_B253_B274_clean_20261110')
CONTEXTS={
265:"A European tavern patron reports that Istanbul's guild has been looking for the listener. The complete one-line referral does not specify the job or establish previous acquaintance.",
266:"Istanbul's guildmaster apologizes for summoning Maria. Couriers demand high pay yet take over two months for an Istanbul-Ceuta round trip; they collude in claiming this is necessary. He wants Maria to demonstrate30 days so he can demand40 from the couriers, even though40 is the usual trip. Maria's initial outrage becomes surprise at his demand, then understanding. His guild will keep losing money unless the plan succeeds. Preserve the distinct30/40/over-two-month figures, round trip and Ceuta endpoint; do not invent delivery cargo, bet, price agreement or guaranteed success.",
267:"An expedition requires a map, then encounters an eerie forest and giant snake. Fight and flee are alternatives. The fight wounds but explicitly does not kill the snake; some sailors are injured. Flight succeeds safely. Later Maria sinks into a bog; Xien either needs crew assistance or rescues her himself. Keep both rescue variants separate and the source fatigue notice. Personality alternatives point toward a discovery. Do not turn the bog into the different quicksand hazard in B269 or the snake's retreat into death. FI names Maria; Xien's care is not proof of kinship or romance.",
268:"Matilda greets FI, having heard the listener seeks ruins, and recommends the Colosseum as a Roman-era site. The dynamic captain repeats its name; Maria thanks her and Matilda reminds her to buy a map. Preserve Roman context and recommendation rather than claiming that the ruins are already visited. The exact spelling of the personal name remains subject to native/name consumer binding.",
269:"A desert expedition has personality alternatives requiring a map and complaining about heat. Maria rations sips because the route is long. A crewman is caught in quicksand; the menu offers pulling him out herself or calling everyone to help. In the first variant Maria asks him to hold on and other voices call for help for the admiral; FI becomes a little fatigued. In the other she directs the crew to pull him out, with sailor fatigue. Further alternative voices wonder when they will leave the desert and point to a sight. Preserve the male crewman's rescue, differing fatigue notices and uncertain near-exit estimates; no deaths, item uses or guaranteed route length are supplied.",
270:"Safia welcomes FI and thanks her for the improvement in her dancing. As thanks she shares a rumor of a mosque far inland where an ancient king is enshrined and a splendid treasure is kept. Only someone recognized by the king can obtain it, according to rumor. She suggests trying. Do not invent a living monarch, religion change, relationship, dance lesson details or already completed treasure acquisition.",
271:"A shipyard worker asks for shipbuilding and gunnery expertise. Janas, Manuel, Cesare and Charles have source-dependent reply alternatives; Charles is the gunnery expert while the others discuss ships. The worker describes a new European carronade in the game's own terms as long-range and powerful, threatening Islamic fleets' boarding tactics, and is developing armor in response. Preserve those source claims even if historical real-world specifications differ. Missing-specialist branches request a later return. The source R223 uses actor18, despite feminine phrasing; retain its native identity as a binding question rather than silently changing the speaker. In success variants Charles explains powder force, Janas suggests hull angles, Cesare material strength and Manuel armor placement. The shipyard worker completes the design and asks them to notify the guildmaster. No extra engineer rank, guaranteed combat statistics or live naval upgrade effect is invented.",
272:"Later-return completion of the same armor project after bringing specialists. Charles discusses gunnery; Janas/Manuel/Cesare supply alternative shipbuilding replies and design contributions. The worker finishes the design and asks them to tell the guildmaster. Preserve alternatives, source speakers and the distinction from the initial immediate-success variant in B271.",
273:"The guildmaster is delighted the shipyard project is complete. He complains his couriers' ships were quickly sunk by pirates and expects improvement now. He thanks the party on the shipyard worker's behalf and gives an object apparently made in unimaginably ancient times, rare but not particularly useful. Maria asks about it then accepts. The object is not named in this exchange; do not invent a title, magical effect, cargo, gold amount or prior friendship.",
274:"Sakura asks if Maria has a map; Maria may have forgotten it, or Sakura parts with the prepared expedition. Personality alternatives set off and then recognize repeated paths. Menu alternatives use a compass or intuition. Xien warns some places affect compasses; Maria checks the noon sun in the compass variant. In the intuition variant Jam calls her haphazard and Xien points out the irony. One day passes; a new fork suggests escape from the loop, then a dynamic speaker announces the find. Preserve both strategies, the navigation meaning of the magnet/compass, uncertainty, dry humor and exact one-day notice without treating the display fixture as earned progress.",
}
TEXT=r'''DK4_MES_B265_R0005|The Istanbul guild has been looking for the listener.|The Istanbul Guild's been looking for you.
DK4_MES_B266_R0004|Apologizes for summoning them all the way here.|Sorry to call you all the way here.
DK4_MES_B266_R0007|Hired couriers have been slow despite demanding high pay.|The couriers we hire have been taking forever lately. They demand a fortune, then take days and days to finish the job.
DK4_MES_B266_R0010|Maria suggests firing such negligent couriers.|Then why not fire such lazy couriers?
DK4_MES_B266_R0013|Local couriers collude; all claim the same travel time is necessary.|They're all in on it together around here. Whoever I ask, they tell me the same thing: the journey simply takes that long.
DK4_MES_B266_R0016|Maria condemns their collusion.|A nasty little racket.
DK4_MES_B266_R0020|Asks her help because couriers take over two months round trip Istanbul-Ceuta.|That's where you come in. They take over two months to sail from Istanbul to Ceuta and back.
DK4_MES_B266_R0023|Maria thinks two months is outrageous.|Two months? That's outrageous.
DK4_MES_B266_R0027|Wants her to demonstrate a thirty-day round trip.|Isn't it? I want you to show them you can make the round trip in thirty days.
DK4_MES_B266_R0031|Maria surprised: normal trip takes about forty days.|Thirty days? Doesn't it usually take about forty?
DK4_MES_B266_R0035|Wants couriers to do forty days; must demonstrate thirty to make his demand stick.|Yes. I want them to do it in forty days, but to make that demand stick, I need to show them it can be done in about thirty.
DK4_MES_B266_R0038|Maria understands and agrees.|I see... All right.
DK4_MES_B266_R0041|Will continue losing money unless this works; asks her help.|Unless this works, we'll keep losing money. I'm counting on you.
SC3_B267_STYLE_24_0|Polite warning of getting lost without map.|Admiral, we'll lose our way without a map.
SC3_B267_STYLE_24_34|Measured warning of same risk.|Admiral, without a map, we will get lost.
SC3_B267_STYLE_24_66|Youthful objection to proceeding without map.|Admiral, we can't just go on without a map!
SC3_B267_STYLE_24_98|Conversational warning of getting lost.|Admiral, we'll end up lost without a map.
SC3_B267_STYLE_24_134|Rough warning of losing way.|Admiral, we're gonna get lost without a map.
SC3_B267_STYLE_24_170|Elderly warning of losing way.|Admiral, we shall lose our way without a map.
SC3_B267_STYLE_24_208|Child says cannot proceed without map.|Admiral, we can't go on without a map!
SC3_B267_STYLE_24_242|Formal emphatic warning.|Admiral, without a map, we are sure to lose our way.
DK4_MES_B267_R0039|Maria finds the forest eerie.|What an eerie forest...
DK4_MES_B267_R0043|Xien says they must advance cautiously.|We must proceed with caution.
DK4_MES_B267_R0047|Crewman stammers and calls attention to a sight.|A-Admiral! Look!
DK4_MES_B267_R0051|Maria identifies a giant snake.|A giant snake...
DK4_MES_B267_R0055|Xien asks FI whether to fight.|What shall we do, FI? Fight it...?
SC3_B267_CHOICE_486_0|Choose to fight.|Fight
SC3_B267_CHOICE_486_1|Choose to flee.|Flee
DK4_MES_B267_R0070|Maria sees no alternative to defeating it.|We have no choice. We'll have to defeat it.
DK4_MES_B267_R0074|Xien agrees and orders vigilance.|...Indeed. Everyone, stay alert!
DK4_MES_B267_R0077|Chinese crewman's acknowledgment.|Understood!
DK4_MES_B267_R0085|Maria exhales after the fight.|Whew...
DK4_MES_B267_R0089|They did not kill it, but its wounds should prevent attacks for a while.|We didn't finish it off, but with those wounds, it shouldn't attack again for some time...
DK4_MES_B267_R0095|System: some sailors apparently injured.|It seems some sailors were injured.
DK4_MES_B267_R0100|Maria chooses retreat to avoid unnecessary fighting.|...Let's run. I'd rather avoid an unnecessary fight.
DK4_MES_B267_R0103|Xien agrees.|Yes. Quite right.
DK4_MES_B267_R0108|Xien observes that everyone seems to have escaped safely.|It seems everyone has escaped unharmed.
DK4_MES_B267_R0112|Maria agrees pensively.|Yes...
DK4_MES_B267_R0119|Maria surprised by what she encounters.|Ah! What is this?!
DK4_MES_B267_R0123|Xien asks if FI is all right.|FI, are you all right?!
DK4_MES_B267_R0127|Maria thinks she is in a bottomless bog and warns others.|Ugh... It seems to be a bottomless bog. Everyone, be careful!
DK4_MES_B267_R0130|Xien exclaims in alarm.|What?!
DK4_MES_B267_R0141|Tells her to hold on; will rescue her now.|Hold on! I'll get you out!
DK4_MES_B267_R0145|Xien strains, cannot manage alone, orders crew to help.|Nnngh! I can't do it alone... You there, give me a hand!
DK4_MES_B267_R0149|Crew acknowledges.|Right!
DK4_MES_B267_R0153|After effort Xien asks if FI is okay.|Whew... FI, are you all right?
DK4_MES_B267_R0156|Maria thanks Xien for saving her.|Yes, Xien. Thank you. You saved me.
DK4_MES_B267_R0164|Alternate rescue: Xien promises help and strains loudly.|I'll get you out! Hrrrrgh!
DK4_MES_B267_R0167|After effort asks if FI is okay.|Whew... Are you all right, FI?
DK4_MES_B267_R0170|Maria thanks him, is fine now, and marvels at a bog here.|Yes... Thank you. I'm all right now. But a bog in a place like this...
DK4_MES_B267_R0178|System: sailors seem fatigued.|The sailors seem tired.
SC3_B267_STYLE_1514_0|Polite startled alert to something ahead.|Admiral, up ahead...!
SC3_B267_STYLE_1514_18|Urgent alert to look ahead.|Admiral, look ahead!
SC3_B267_STYLE_1514_36|Youthful stammering alert to a sight.|A-Admiral, over there...
SC3_B267_STYLE_1514_56|Conversational startled alert.|Admiral, look!
SC3_B267_STYLE_1514_70|Rough urgent alert to look at that.|Admiral, look at that!
SC3_B267_STYLE_1514_86|Child says that is the thing.|Admiral! There it is!
SC3_B267_STYLE_1514_108|Formal voice exclaims in awe.|Oh...!
DK4_MES_B268_R0005|Matilda greets FI at a good moment.|Oh, FI! Perfect timing.
DK4_MES_B268_R0008|Asks whether listener knows the Colosseum.|Have you heard of the Colosseum?
DK4_MES_B268_R0012|Dynamic captain repeats unfamiliar site name.|The Colosseum?
DK4_MES_B268_R0016|Roman-era ruins; heard the listener sought ruins and wanted to recommend it.|It's a ruin from Roman times. I heard you were looking for ruins, so I thought I'd tell you about it.
DK4_MES_B268_R0020|Maria wants to see it and thanks her.|I'd like to see that. Thank you.
DK4_MES_B268_R0023|Wishes care and reminds her to buy a map.|You're welcome. Take care, and don't forget to buy a map.
SC3_B269_STYLE_24_0|Polite tentative warning of losing way without map.|Admiral, I think we'll get lost without a map...
SC3_B269_STYLE_24_40|Measured statement that a map is necessary here.|Admiral, we need a map here.
SC3_B269_STYLE_24_68|Youthful objection to advancing without consulting map.|Admiral, we can't go on without checking a map!
SC3_B269_STYLE_24_108|Conversational reminder to obtain map first to avoid getting lost.|Admiral, let's get a map first so we don't get lost.
SC3_B269_STYLE_24_162|Rough warning against proceeding without map.|Admiral, going on without a map is a bad idea.
SC3_B269_STYLE_24_204|Elderly warning of losing way.|Admiral, we shall lose our way without a map.
SC3_B269_STYLE_24_242|Child warns of getting lost.|Admiral, we're gonna get lost without a map!
SC3_B269_STYLE_24_284|Formal warning of losing way.|Admiral, without a map, we will lose our way.
SC3_B269_STYLE_392_0|Polite observation of considerable heat.|It's quite hot here, isn't it?
SC3_B269_STYLE_392_24|Terse measured complaint about heat.|So hot...
SC3_B269_STYLE_392_32|Youthful sigh and heat complaint.|Whew, it's hot.
SC3_B269_STYLE_392_48|Conversational emphatic complaint.|It really is hot here.
SC3_B269_STYLE_392_70|Rough drawn-out complaint.|It's so damn hot...
SC3_B269_STYLE_392_84|Elderly observation of considerable heat.|My, but it's hot.
SC3_B269_STYLE_392_102|Child exhales and complains of heat.|Whew, it's so hot.
SC3_B269_STYLE_392_120|Formal conversational complaint.|Goodness, it's hot, isn't it?
DK4_MES_B269_R0070|Long way ahead; Maria tells crew to drink water in small sips.|We've a long way to go. Drink your water a little at a time.
DK4_MES_B269_R0074|Maria notices something puzzling.|?
DK4_MES_B269_R0078|Crewman cries out about quicksand.|Aaaah! Quicksand!
SC3_B269_CHOICE_640_0|Choose to pull him up personally.|Pull him out yourself
SC3_B269_CHOICE_640_1|Choose to call everyone to help.|Call for help
DK4_MES_B269_R0093|Maria encourages him to hold on and grab her.|Hold on! Here, grab my hand!
SC3_B269_STYLE_740_0|Polite alarm for admiral; calls all to help her.|Oh, Admiral! Everyone, help the admiral!
SC3_B269_STYLE_740_36|Rough alarm and command to help admiral.|Admiral! Everyone, give her a hand!
SC3_B269_STYLE_740_72|Conversational alarm and plea for all to help admiral.|Oh, Admiral! Everyone, help her!
SC3_B269_STYLE_740_110|Elderly alarm and command.|Oh, Admiral! Everyone, help the admiral!
SC3_B269_STYLE_740_152|Child cries for admiral and calls everyone to help.|Admiral! Everybody, help her!
SC3_B269_STYLE_740_194|Formal urgent command to help admiral.|Admiral! Everyone, help the admiral!
DK4_MES_B269_R0119|System: FI became a little fatigued.|FI grew a little tired.
DK4_MES_B269_R0124|Maria directs everyone to pull the male crewman out.|Pull him out! Everyone, lend a hand!
SC3_B269_STYLE_1104_0|Conversational encouragement to grab hold.|Here, grab on!
SC3_B269_STYLE_1104_20|Rough imperative to grab hold.|Come on, grab hold!
SC3_B269_STYLE_1104_38|Elderly imperative to grab hold.|Now, take hold!
SC3_B269_STYLE_1104_62|Formal imperative to grab hold.|Here, take hold!
DK4_MES_B269_R0153|System: sailors seem fatigued.|The sailors seem tired.
SC3_B269_STYLE_1266_0|Polite uncertain estimate of nearly leaving the desert.|I think we're nearly out of the desert...
SC3_B269_STYLE_1266_40|Measured expectation of already being out by now.|We should be out of the desert by now...
SC3_B269_STYLE_1266_74|Youthful tired expectation.|We ought to be out of the desert by now...
SC3_B269_STYLE_1266_106|Conversational expectation and uncertainty.|We should be out of the desert by now, shouldn't we...?
SC3_B269_STYLE_1266_140|Rough tentative estimate of nearing exit.|I think we should be out of this desert soon...
SC3_B269_STYLE_1266_176|Elderly uncertain expectation of near exit.|We ought to be nearly out of the desert by now...
SC3_B269_STYLE_1266_216|Child uncertain that desert should be ending.|The desert should be ending by now...
SC3_B269_STYLE_1266_254|Formal tentative expectation of near exit.|We should be nearly out of the desert, but...
SC3_B269_STYLE_1584_0|Polite call to admiral to look.|Admiral! Please look over there!
SC3_B269_STYLE_1584_28|Conversational excited call to look.|Admiral! Look over there!
SC3_B269_STYLE_1584_48|Rough call to look.|Admiral! Have a look at that!
SC3_B269_STYLE_1584_72|Elderly command to look at sight.|Admiral! Look there!
SC3_B269_STYLE_1584_92|Child excited call.|Admiral! Look at that!
SC3_B269_STYLE_1584_116|Formal terse call to a sight.|Admiral! Over there!
DK4_MES_B270_R0005|Safia warmly welcomes FI.|Oh, FI! Welcome!
DK4_MES_B270_R0008|Her dancing improved greatly thanks to FI.|My dancing has improved so much, thanks to you!
DK4_MES_B270_R0011|Will share a useful tip as thanks.|Let me tell you something as a thank-you.
DK4_MES_B270_R0015|Far inland is a mosque enshrining an ancient king, reportedly with splendid treasure.|Far inland from here, there's a mosque dedicated to a king from long ago. They say it holds a magnificent treasure.
DK4_MES_B270_R0019|Rumor: only someone recognized by king can obtain it; suggests trying.|The rumor is that only someone the king approves of can claim it. Why not go and try?
DK4_MES_B271_R0004|Shipyard worker asks for expertise in shipbuilding and gunnery.|Do any of you know much about shipbuilding and gunnery?
DK4_MES_B271_R0015|Janas offers to help and asks what is needed.|If I can be of help... What do you need?
DK4_MES_B271_R0029|Manuel thinks it may be his turn to contribute.|Oh? Is this where I come in?
DK4_MES_B271_R0044|Cesare eagerly responds to being called.|Yes, yes, yes! Did someone call for me?
DK4_MES_B271_R0058|Charles volunteers his cannon expertise.|If it's cannons you need, leave it to me.
DK4_MES_B271_R0065|Maria asks what the matter is.|What's this about?
DK4_MES_B271_R0069|Describes carronade as a recently invented European cannon with long range and power.|Have you heard of the carronade? It's a new cannon invented in Europe. It combines long range with tremendous power.
DK4_MES_B271_R0072|If widespread, it could greatly alter naval warfare.|If it catches on, it could change naval warfare completely.
DK4_MES_B271_R0076|Islamic fleets favor boarding and may no longer match European gunnery warships.|Our Islamic fleets specialize in boarding. We won't stand a chance against Europe's cannon-armed warships.
DK4_MES_B271_R0079|Researching ship armor to counter it.|I'm researching ship armor to counter it.
DK4_MES_B271_R0082|Wants opinions from people with broad ship knowledge and gunnery experts.|I wanted advice from someone who knows all kinds of ships, and from a gunnery expert.
DK4_MES_B271_R0100|Janas knows a little about ships, with reservation.|I know a little about ships, but...
DK4_MES_B271_R0115|Manuel could advise on shipbuilding, but has a reservation.|Hmm. I could advise you on shipbuilding. However...
DK4_MES_B271_R0129|Cesare has insufficient gunnery knowledge.|My knowledge of gunnery is rather lacking.
DK4_MES_B271_R0136|Charles volunteers gunnery expertise.|Leave the gunnery to me.
DK4_MES_B271_R0148|Janas will advise on shipbuilding.|Then I'll advise you on shipbuilding.
DK4_MES_B271_R0165|Manuel reminds them of his shipbuilding expertise.|Don't forget me when it comes to shipbuilding.
DK4_MES_B271_R0182|Cesare enthusiastically invites all ship questions.|If it concerns ships, ask me anything!
DK4_MES_B271_R0218|Maria: none currently versed in European shipbuilding or gunnery.|I'm afraid none of us is familiar with European shipbuilding or gunnery at the moment.
DK4_MES_B271_R0223|Source actor18 says none currently versed in European shipbuilding; preserve this source identity pending native binding.|I'm afraid none of us is familiar with European shipbuilding at the moment.
DK4_MES_B271_R0251|Worker asks them to bring someone if found; will wait patiently.|I see. If you find anyone, please bring them here. I'll be waiting.
DK4_MES_B271_R0257|Charles explains barrel shape and powder explosion transferring force to shot.|First, the barrel is shaped like this. The powder explodes here, and the force is transferred to the cannonball...
DK4_MES_B271_R0269|Janas suggests hull construction angle to disperse cannon impact.|If we build the hull at this angle, it should disperse the force of the shot.
DK4_MES_B271_R0275|Worker understands the amount of damage an attack from this cannon would cause.|...I see. So that's how much damage this cannon would do.
DK4_MES_B271_R0287|Cesare predicts material will not easily break.|With this material, it should not break easily!
DK4_MES_B271_R0301|Manuel suggests armor in two indicated areas as most effective.|Adding armor here and around here would be most effective.
DK4_MES_B271_R0311|Worker finishes and hopes to surprise opponents.|There! It's finished! This'll give them a surprise!
DK4_MES_B271_R0315|Remembers to ask them to tell guildmaster it is finally complete.|Oh, right! Tell the guildmaster for me. It's finally finished!
DK4_MES_B272_R0007|Worker delighted they brought the specialist or specialists.|Oh! You brought them here!
DK4_MES_B272_R0011|Charles confidently offers gunnery expertise.|Yes. Leave the gunnery to me!
DK4_MES_B272_R0023|Janas offers shipbuilding advice.|Then I'll advise you on shipbuilding.
DK4_MES_B272_R0037|Manuel reminds them of his shipbuilding knowledge.|Don't forget me when it comes to shipbuilding.
DK4_MES_B272_R0052|Cesare eagerly invites ship questions.|If it concerns ships, ask me anything!
DK4_MES_B272_R0059|Charles explains barrel and powder explosion transferring force to shot.|Well, the barrel is shaped like this. The powder explodes here, and the force is transferred to the cannonball...
DK4_MES_B272_R0071|Janas proposes hull angle to disperse cannon impact.|If we build the hull at this angle, it should disperse the force of the shot.
DK4_MES_B272_R0077|Worker understands the expected damage.|...I see. So that's how much damage this cannon would do.
DK4_MES_B272_R0089|Cesare predicts material will resist breaking.|With this material, it should not break easily!
DK4_MES_B272_R0103|Manuel recommends armor in indicated areas.|Adding armor here and around here would be most effective.
DK4_MES_B272_R0114|Worker completes project and expects to surprise opponents.|There! It's finished! This'll give them a surprise!
DK4_MES_B272_R0118|Asks them to tell guildmaster it is finally complete.|Oh, right! Tell the guildmaster for me. It's finally finished!
DK4_MES_B273_R0004|Guildmaster surprised and delighted that project is complete.|What? It's finally finished?!
DK4_MES_B273_R0007|Couriers were being quickly sunk by pirates; he complains of incompetence.|Our couriers have been getting sunk by pirates before they can get anywhere. It's been a real problem. Useless lot.
DK4_MES_B273_R0010|Expects their work to improve; credits the party.|This should help them do their jobs a little better. Yes, it's all thanks to you.
DK4_MES_B273_R0014|Offers thanks on shipyard worker's behalf.|Let me thank you on the shipyard worker's behalf.
DK4_MES_B273_R0019|Maria puzzled about the offered object.|...? What's this?
DK4_MES_B273_R0022|Apparently made in unimaginably ancient times; no particular use, but rare.|It's supposed to be unimaginably old. Not much use for anything, but it's unusual, isn't it?
DK4_MES_B273_R0025|Maria agrees and accepts gratefully.|Yes, it is. Thank you. I'll gladly accept it.
DK4_MES_B274_R0011|Sakura asks if Maria has brought a map.|Did you bring the map?
DK4_MES_B274_R0015|Maria forgot and must prepare it.|I forgot. I'd better get one ready.
DK4_MES_B274_R0029|Sakura parts here and wishes safe journey.|Well, this is where we part ways. Take care on your journey.
DK4_MES_B274_R0034|Maria thanks her.|I will. Thank you.
SC3_B274_STYLE_180_0|Polite invitation to set off.|Now, let's go.
SC3_B274_STYLE_180_20|Youthful enthusiastic departure.|Come on, let's go!
SC3_B274_STYLE_180_36|Conversational departure.|All right, let's go.
SC3_B274_STYLE_180_58|Rough casual departure.|Right, let's get going.
SC3_B274_STYLE_180_72|Elderly suggestion to depart.|Well then, shall we go?
SC3_B274_STYLE_180_90|Child exuberant departure.|All right! Off we go!
SC3_B274_STYLE_334_0|Polite feeling they passed here and may be circling.|I think we passed this way earlier. Could we be going in circles...?
SC3_B274_STYLE_334_80|Measured concern that they keep passing same place.|This place... I can't shake the feeling we've been passing the same spot over and over...
SC3_B274_STYLE_334_158|Youthful puzzled impression of circling same place.|Huh? This is strange. It feels like we've been going around and around the same place.
SC3_B274_STYLE_334_242|Conversational recognition of earlier passage.|Oh? Didn't we pass this way before?
SC3_B274_STYLE_334_284|Rough puzzled impression of repeating route.|That's strange. Feels like we've been walking past the same place over and over...
SC3_B274_STYLE_334_348|Elderly feeling of having used same path.|I feel we've already taken this path...
SC3_B274_STYLE_334_386|Child asks whether they passed this road before.|Hey, didn't we come this way already?
SC3_B274_STYLE_334_428|Formal inference of repeated same route.|Hmm. It appears we've been taking the same path over and over...
DK4_MES_B274_R0080|Maria wonders if they are lost.|Have we lost our way?
SC3_B274_CHOICE_864_0|Rely on the compass.|Use the compass
SC3_B274_CHOICE_864_1|Rely on intuition.|Trust your instincts
DK4_MES_B274_R0096|Maria proposes relying on compass.|Let's use the compass.
DK4_MES_B274_R0100|Xien doubts reliability; heard some places make compasses fail.|Will it be reliable? I've heard there are places where compasses don't work.
DK4_MES_B274_R0104|Noon sun's position suggests its reading is correct.|Judging by the position of the midday sun, it seems to be right.
DK4_MES_B274_R0107|Xien understands.|Hmm. I see.
DK4_MES_B274_R0113|Maria heard of places where compasses fail; will rely on intuition here.|I've heard there are places where compasses don't work. Let's trust our instincts here.
DK4_MES_B274_R0125|Jam incredulous at such a haphazard approach.|What?! Seriously? That's awfully haphazard...
DK4_MES_B274_R0128|Xien dryly says Jam is not one to talk.|You're one to talk.
DK4_MES_B274_R0138|System: one day elapsed.|One day passed.
DK4_MES_B274_R0142|Maria has not seen this fork before.|I haven't seen this fork before.
DK4_MES_B274_R0146|Xien relieved they may finally get out.|Whew... It looks like we'll finally get out.
DK4_MES_B274_R0153|Dynamic speaker stammers that the sought thing was found.|A-Admiral! There it is!'''

def main():
    p=ROOT/'authored_B265_B274_v1.json';assert not p.exists()
    records=[r.split('|',2) for r in TEXT.splitlines()]
    packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in records]==expected and len(records)==197
    save(p,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=records,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges only; names/item terms remain provisional.',new_credit=0))
    print('Authored197 clean meanings and independent drafts in10 complete groups; current English unread.')

if __name__=='__main__':main()
