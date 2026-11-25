"""Clean-only meanings followed by independent drafts; no current story English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save,load

ROOT=Path('work/Maria_B253_B274_clean_20261110')
CONTEXTS={
253:"A European port worker recognizes FA and reports that London's guild has been looking for her. This complete conditional referral does not state the reason; do not invent prior acquaintance or kinship from familiar address.",
254:"London's guildmaster asks Maria to find a rumored African remedy that instantly cures scurvy among his hired navigators. Maria can agree to search or already possess it. He asks only to borrow the Lime Drops for one month, and promises a reward when she returns. Keep the initial ignorance and possession alternatives distinct, his warm rough gratitude and her restrained helpfulness. Addressing her as an elder sister expresses familiarity, not kinship. Item title remains provisional until its native consumer is bound.",
255:"Maria delivers the requested scurvy remedy after finding it. The London guildmaster borrows it for about a month and promises a reward on her return. This is the later-delivery variant, not a second loan in the same exchange. Keep the one-month term and lending rather than sale.",
256:"Separate conditional Maria reminders: she wonders where the scurvy cure is, or recognizes the Lime Drops and needs to deliver them to London's guild. They do not occur as a single contradictory monologue. The medicine is a source quest item, with no invented acquisition location or guaranteed player effect.",
257:"Maria thinks it is about time to retrieve the Lime Drops lent to London's guild. Preserve the approximate readiness rather than announcing a precise elapsed-time value or automatic return.",
258:"The guildmaster thanks Maria because everyone recovered; the system reports20,000 gold and a small London share rise. Maria asks about ruins. He says they are some distance from London but accessible with a map, and reports strange people who expelled the caretaker and conduct creepy ceremonies. They bought up the maps locally; another town might sell one. Preserve hearsay, uncertainty and the distinction between their actions and the neighboring residents' complaints; no invented cult identity or guaranteed stock.",
259:"A jungle expedition has physical personality alternatives warning against entering without a map. Maria complains of humidity; Xien warns of beasts. A deep cave must be crossed, but a tiger appears. Menu alternatives are attack or flee. In the fight, gunfire risks hitting allies in cramped space, so Maria orders close combat; victory and numerous injuries are reported. In flight, the tiger's failure to pursue suggests it was not hungry, and the crew is relieved. Xien spots light and Maria sees the way out. Preserve every personality alternative as a distinct source body, the child's explicit tiger wording, injury severity, uncertainty in hesitant victory variants and alternative outcomes. Do not invent deaths, magic, tiger death where only defeat is stated, or simultaneous activation of all variants.",
260:"Malacca's guildmaster asks Chinese Maria about obtaining precious shark fin for the local lord. She explains that even in China it is used in palace cuisine and she has never eaten it. She offers to look without guaranteeing success. He will also accept an unprecedented delicacy; she dryly notes the lord has likely tried everything. He begins to criticize the man's gourmet habits, then catches himself. Preserve the cultural and class context without adding a royal title, modern factual commentary or a guaranteed supply.",
261:"Maria delivers shark fin and expects future supplies to become somewhat easier. The guildmaster promises a generous reward; the system reports50,000 gold and a slight Malacca share increase. As thanks he shares a rumor of an entire ancient kingdom's ruins preserved deep in the jungle. Maria is skeptical; he stresses nobody has found them and she might. Preserve uncertainty and the distinction between a rumored location and an established discovery.",
262:"Alternative completion of Malacca's food request: Maria found no shark fin but offers a different rare food whose identity is not given in these lines. The guildmaster tastes and loves it, and says he can confidently serve it. Reward30,000 gold and a small share increase, then the same uncertain ancient-ruins rumor. Do not name the food or merge this reward with the shark-fin route.",
263:"Personality alternatives call the admiral over to a find. Maria asks what it is; a Chinese crewman offers to dig, and she identifies very old coins. No exact date, treasure title, quantity or value is established. Keep the alternative voices without turning them into one chorus.",
264:"A guildmaster-guide requires a map and later parts from the expedition. Personality alternatives likewise block proceeding without one. Maria asks Xien about preparations, Yukihisa urges caution, and the party meets a dead end. The menu offers force a way through or investigate. The force variant reads the map as requiring passage and some sailors leave; the investigate variant finds a path hidden by trees, and Xien praises FI. Maria admires the destination. Preserve conditional paths, map necessity and departures rather than inventing sailor deaths or a physical mechanism for the obstruction.",
}
TEXT=r'''DK4_MES_B253_R0005|The worker has found FA; London's guild was seeking her.|Oh, there you are! You're FA, right? The London Guild's been looking for you.
DK4_MES_B254_R0004|A small job: the guild's hired navigators suffer badly from scurvy.|I've got a job for you. The navigators we hire have been suffering terribly from scurvy.
DK4_MES_B254_R0008|World travelers might know a good solution.|You sail all over the world, so I thought you might know something that could help.
DK4_MES_B254_R0012|Rumored instant scurvy cure hidden near Africa; asks whether she knows it.|They say there's a wondrous medicine hidden somewhere around Africa that cures scurvy in an instant. Know anything about it?
DK4_MES_B254_R0023|Maria does not know.|I'm afraid not...
DK4_MES_B254_R0027|Asks her to find it; borrowing is sufficient.|I see. I'd really like you to find it for us. We'd only need to borrow it, of course.
DK4_MES_B254_R0031|Agrees to look.|All right. I'll see what I can find.
DK4_MES_B254_R0035|Emphatic thanks and indebtedness.|Thank you! I'll owe you one!
DK4_MES_B254_R0044|Possession variant: thinks she has the requested thing.|Oh, in that case... I think this is what you mean.
DK4_MES_B254_R0047|Surprised FA already has it; praises her competence.|You already have it! I should've known I could count on you, FA!
DK4_MES_B254_R0051|Requests a loan until all navigators recover, estimating one month.|Could you lend it to us until all our navigators are well again? Let's say... one month.
DK4_MES_B254_R0054|Willingly agrees.|Of course.
DK4_MES_B254_R0058|Her agreement confirms his good judgment of her.|I knew I was right about you!
DK4_MES_B254_R0065|System: the Lime Drops were lent.|Lent the Lime Drops.
DK4_MES_B254_R0069|Promises reward after a month; asks her to return; thanks.|I'll have a reward for you in a month. Don't forget to come back for it. Thanks again!
DK4_MES_B255_R0004|Asks whether this is the requested object.|Is this what you meant?
DK4_MES_B255_R0008|Delighted she found it; praises FA.|You found it! I knew I could count on you, FA!
DK4_MES_B255_R0012|Thanks and requests about a month's loan for navigators' recovery.|Thanks. I'll borrow it until all our navigators are well again. About a month should do it.
DK4_MES_B255_R0016|Agrees to the loan.|Of course.
DK4_MES_B255_R0024|System: the Lime Drops were lent.|Lent the Lime Drops.
DK4_MES_B255_R0028|Promises reward in one month and reminds her to return.|I'll have a reward for you in a month. Don't forget to come back for it. Thanks again!
DK4_MES_B256_R0012|Maria wonders where the scurvy remedy can be found.|...Where could I find a medicine that cures scurvy?
DK4_MES_B256_R0017|Recognizes the Lime Drops as the cure and needs to deliver them soon.|So the scurvy cure is these Lime Drops. I'd better get them to the London Guild...
DK4_MES_B257_R0005|Thinks it is about time to retrieve the borrowed item.|It should be about time to get the Lime Drops back from the London Guild.
DK4_MES_B258_R0004|Thanks; everyone recovered completely because of her help.|There you are! You really saved us. Thanks to you, everyone's back to full health.
DK4_MES_B258_R0012|System reward:20,000 gold coins.|Received 20,000 gold.
DK4_MES_B258_R0037|System: share in London rose a little.|London share rose slightly!
DK4_MES_B258_R0048|Asks about famous ruins in this town.|By the way, are there any famous ruins around here?
DK4_MES_B258_R0051|Ruins are somewhat far from London but easy with a map; strange people recently frequent them.|They're a little way from London, but easy enough to reach with a map. Some strange people have been hanging around there lately, though.
DK4_MES_B258_R0054|Prompts him about the strange people.|Strange people?
DK4_MES_B258_R0058|They expelled the caretaker and conduct creepy ritual-like acts; neighbors reportedly bothered.|They drove out the caretaker and started holding some kind of creepy ceremonies. I hear the neighbors are fed up with them.
DK4_MES_B258_R0061|Xien is interested and asks about the map.|Hmm. And where might we find this map?
DK4_MES_B258_R0064|Those people bought the maps locally; other towns may have some for sale.|Those people bought up the maps here, so you won't find one in this town. Another town might have one for sale.
SC3_B259_STYLE_24_0|Polite warning against aimless jungle wandering.|Admiral, it's dangerous to wander through the jungle without knowing the way.
SC3_B259_STYLE_24_46|Measured polite warning about this jungle.|Admiral, wandering aimlessly through a jungle like this is dangerous.
SC3_B259_STYLE_24_98|Youthful emphatic warning about aimless wandering.|Admiral, it's much too dangerous to wander around in a jungle like this!
SC3_B259_STYLE_24_156|Conversational warning that without a map they will get lost in the dense jungle.|Admiral, we'll get lost in this huge jungle without a map!
SC3_B259_STYLE_24_216|Rough warning that reckless jungle wandering risks life.|Admiral, you'd have to be crazy to wander into a jungle like this without knowing the way.
SC3_B259_STYLE_24_270|Elderly warning against aimless jungle wandering.|Admiral, it's dangerous to roam a jungle like this without knowing the way.
SC3_B259_STYLE_24_322|Child does not want to enter without a map.|Admiral, I don't wanna go in that jungle without a map!
SC3_B259_STYLE_24_384|Formal emphatic warning.|Admiral, wandering through such a jungle without knowing the way is dangerous indeed.
DK4_MES_B259_R0036|Maria finds the humidity high and heat oppressive.|...It's terribly humid here. So hot and sticky.
DK4_MES_B259_R0039|Xien attributes it to jungle and warns of lurking beasts; choose route carefully.|Hmm, it is a jungle, after all... Wild beasts lurk in places like this, Admiral. We must choose our path carefully.
DK4_MES_B259_R0042|Finds a cave that seems deep.|A cave. It looks quite deep...
DK4_MES_B259_R0045|Xien thinks they must pass through it.|Hmm. It seems we must go through it.
DK4_MES_B259_R0049|Maria agrees to proceed.|...Yes. Let's go.
DK4_MES_B259_R0053|A low animal growl.|Grrrr...
SC3_B259_STYLE_800_0|Uneasy polite detection of something present.|...There's something in here. I have a bad feeling about this...
SC3_B259_STYLE_800_32|Measured detection and ominous feeling.|...Something is here. I fear this bodes ill...
SC3_B259_STYLE_800_62|Youthful hesitant detection and bad feeling.|Something's... in here. I've got a bad feeling...
SC3_B259_STYLE_800_92|Conversational uneasy question; bad feeling.|There's something in here, isn't there...? I have a bad feeling about this...
SC3_B259_STYLE_800_126|Rough certainty something is present and bad premonition.|Something's in here, all right. I've got a bad feeling...
SC3_B259_STYLE_800_166|Elderly detection and bad feeling.|...There's something here. I've an uneasy feeling...
SC3_B259_STYLE_800_198|Child hesitantly detects something and feels uneasy.|...There's... something in here, right? I don't like this...
DK4_MES_B259_R0076|Dynamic speaker cries that it has appeared.|Th-there it is!
SC3_B259_CHOICE_1090_0|Command to attack.|Attack!
SC3_B259_CHOICE_1090_1|Command to flee.|Run!
DK4_MES_B259_R0091|Maria orders someone to shoot.|! Someone, shoot it!
DK4_MES_B259_R0095|Animal roar.|GRAWR!
DK4_MES_B259_R0099|Crewman cries in pain.|Aaagh!
DK4_MES_B259_R0103|Maria strains and remarks on its speed.|Ugh! It's so fast!
SC3_B259_STYLE_1228_0|Polite objection: shooting in cramped space has very high friendly-fire risk.|We can't! In such a tight space, we're far too likely to hit our own men!
SC3_B259_STYLE_1228_72|Measured objection: could shoot allies in cramped space.|We mustn't! In such close quarters, we could shoot our own men...!
SC3_B259_STYLE_1228_136|Youthful objection to risking shooting allies.|We can't! We might shoot our own men in a tight space like this!
SC3_B259_STYLE_1228_200|Emphatic conversational objection to possible friendly fire.|No! If we shoot in here, we could hit our own men!
SC3_B259_STYLE_1228_274|Rough objection: would hit allies in this confined space.|No good! Shoot in a place this cramped and we'll hit our own men!
SC3_B259_STYLE_1228_332|Elderly objection: impossible to shoot without hitting allies.|No! We can't shoot in such close quarters without hitting our own men!
SC3_B259_STYLE_1228_400|Child calls admiral; might shoot companions.|Admiral! It's so cramped, we might shoot our friends!
SC3_B259_STYLE_1228_462|Formal objection to extremely high friendly-fire risk.|We cannot! Firing in such confined quarters is far too likely to hit our own men!
DK4_MES_B259_R0128|More people are only getting hurt; switches to close combat.|We're only getting more people hurt. ...Switch to close combat!
SC3_B259_STYLE_1882_0|Panting polite report of barely managing to defeat it.|Hah... hah... We managed to bring it down...
SC3_B259_STYLE_1882_32|Matter-of-fact report of managing to defeat it.|We managed to defeat it.
SC3_B259_STYLE_1882_52|Panting youthful uncertain victory report.|Hah... hah... I think... we got it...
SC3_B259_STYLE_1882_86|Panting conversational tentative victory report.|Hah... hah... It looks like we got it...
SC3_B259_STYLE_1882_120|Rough terse victory report.|...Got it!
SC3_B259_STYLE_1882_134|Wheezing elderly report of managing to win.|Whew... whew... We managed to defeat it!
SC3_B259_STYLE_1882_166|Child finally defeated it and remarks the tiger was strong.|We finally beat it! That tiger sure was strong!
SC3_B259_STYLE_1882_208|Panting formal victory report.|Hah... hah... We managed to defeat it!
DK4_MES_B259_R0162|System: apparently a considerable number were injured.|It seems many people were injured.
SC3_B259_STYLE_2186_0|Polite inference it was not hungry because it is not chasing them.|It seems it wasn't hungry. It isn't following us.
SC3_B259_STYLE_2186_44|Measured inference of no hunger and no pursuit.|Apparently it wasn't hungry. It isn't pursuing us.
SC3_B259_STYLE_2186_92|Youthful inference from the lack of pursuit.|It wasn't hungry after all. See? It's not chasing us.
SC3_B259_STYLE_2186_158|Conversational realization and relief at no pursuit.|So it wasn't hungry... Thank goodness it's not chasing us.
SC3_B259_STYLE_2186_226|Rough inference from no pursuit and relief.|It's not chasing us, so it must not've been hungry... What a relief.
SC3_B259_STYLE_2186_300|Elderly inference that the tiger was not hungry.|The tiger isn't pursuing us. It seems it wasn't hungry after all.
SC3_B259_STYLE_2186_364|Child says the tiger seems not hungry and is not following.|That tiger doesn't seem hungry. It's not chasing us.
SC3_B259_STYLE_2186_418|Polite inference and no pursuit.|It seems it wasn't hungry after all. It isn't following us.
DK4_MES_B259_R0187|Crewman's frightened relief.|Whew! We're safe!
DK4_MES_B259_R0197|Xien calls FI and spots a light ahead.|Hmm... FI, I can see light over there.
DK4_MES_B259_R0200|Maria thinks this will let them leave the cave.|Now we can get out of this cave...
DK4_MES_B260_R0004|Greets FI familiarly; asks if she knows shark fin as a Chinese person.|Hello there, FI. You're from China, so you know about shark fin, don't you?
DK4_MES_B260_R0007|Maria puzzled but confirms.|? Yes.
DK4_MES_B260_R0010|Malacca's lord wants to try it; asks whether such a precious item can be obtained.|The lord of Malacca wants to try some. But shark fin's a rare delicacy, isn't it? I'd like to know if we can get any.
DK4_MES_B260_R0013|Difficult; even in China it is palace cuisine and Maria has never eaten it.|That might be difficult. Even in China, it's used in palace cuisine. I've never tried it myself.
DK4_MES_B260_R0017|Resigned confirmation of his suspicion.|I thought as much... Yes, that figures.
DK4_MES_B260_R0020|Offers to buy it if found somewhere, without guarantee.|If I come across any, I'll buy some for you. I can't promise anything, though.
DK4_MES_B260_R0024|Grateful acceptance.|Oh, thank you!
DK4_MES_B260_R0028|If impossible, asks her to suggest a delicacy unlike any seen before.|If you really can't find any, introduce us to some delicacy we've never seen before.
DK4_MES_B260_R0032|Maria finds this a difficult request, assuming he has sampled the world's foods.|A delicacy he's never seen? ...That's a tall order. I suppose he's already tried everything the world has to offer.
DK4_MES_B260_R0036|Agrees and starts criticizing gourmet habits, then restrains dangerous speech.|Yes. Honestly, that man's taste for fine food... Ah, I'd better watch what I say. Well, I'm counting on you.
DK4_MES_B261_R0004|Maria delivers the requested shark fin.|I found what you asked for. Here you are. Shark fin.
DK4_MES_B261_R0007|Amazed; confirms it is genuine.|Really?! Incredible! It's the real thing!
DK4_MES_B261_R0010|Expects obtaining it to be somewhat easier from now on.|I think it should be a little easier to obtain from now on.
DK4_MES_B261_R0013|Praises her competence; will be generous with reward.|You really came through! All right, I'll make your reward a generous one!
DK4_MES_B261_R0018|System:50,000 gold coins received.|Received 50,000 gold!
DK4_MES_B261_R0042|System: Malacca share rose slightly.|Malacca share rose slightly!
DK4_MES_B261_R0059|Offers an interesting story as thanks.|Let me tell you something interesting as a thank-you.
DK4_MES_B261_R0063|Rumor: complete ancient kingdom ruins survive deep inland in jungle.|They say the ruins of an ancient kingdom still stand, completely intact, deep in the jungle far inland from here.
DK4_MES_B261_R0067|Maria finds an ancient kingdom hard to believe.|An ancient kingdom... That's a little hard to believe.
DK4_MES_B261_R0071|Nobody has found them; only rumor; she might find them.|No one's actually found them yet. It's only a rumor, mind you. But you might be able to find them.
DK4_MES_B262_R0004|Asks about her shark-fin search.|Ah, there you are. Any luck finding shark fin?
DK4_MES_B262_R0007|No shark fin, but obtained something rare she thinks worth trying.|I'm afraid I couldn't find any. But I found something unusual. I think it's worth a try.
DK4_MES_B262_R0011|Asks what it is, then finds it delicious.|What's this? ...It's delicious!
DK4_MES_B262_R0014|Maria expected that reaction.|Isn't it?
DK4_MES_B262_R0018|Can serve this confidently; praises her and offers reward.|I can serve this with confidence! You really came through. Here, take your reward!
DK4_MES_B262_R0024|System:30,000 gold coins received.|Received 30,000 gold!
DK4_MES_B262_R0048|System: Malacca share rose slightly.|Malacca share rose slightly!
DK4_MES_B262_R0065|Offers interesting story as thanks.|Let me tell you something interesting as a thank-you.
DK4_MES_B262_R0069|Rumor: ancient kingdom ruins intact in jungle far inland.|They say the ruins of an ancient kingdom still stand, completely intact, deep in the jungle far inland from here.
DK4_MES_B262_R0073|Maria finds it hard to believe.|That's a little hard to believe...
DK4_MES_B262_R0077|Only rumor; nobody has found ruins; she might.|No one's actually found them yet. It's only a rumor, mind you. But you might be able to find them.
SC3_B263_STYLE_12_0|Polite call for admiral to come over.|Admiral, please come over here!
SC3_B263_STYLE_12_28|Formal polite call to come this way.|Admiral, please come this way!
SC3_B263_STYLE_12_56|Youthful excited call.|Admiral, come here!
SC3_B263_STYLE_12_76|Rough familiar call.|Admiral, come over here!
SC3_B263_STYLE_12_102|Elderly invitation to come and see.|Admiral, come and have a look!
SC3_B263_STYLE_12_126|Child calls admiral over.|Admiral! Come here!
SC3_B263_STYLE_12_150|Deferential call to come over.|Admiral, would you come over here?
DK4_MES_B263_R0022|Maria asks what the find is.|What's this?
DK4_MES_B263_R0026|Crewman offers to dig it up.|I'll dig it up!
DK4_MES_B263_R0030|Maria thinks the coins are very old.|These coins look very old.
DK4_MES_B264_R0011|Guide asks about map and refuses to proceed without one even for them.|Did you bring the map? Even for you, I'm not going any farther without one.
DK4_MES_B264_R0024|Approves that they brought a map.|Good. You brought the map.
SC3_B264_STYLE_194_0|Polite map requirement.|Admiral, we can't go any farther without a map.
SC3_B264_STYLE_194_40|Formal map requirement.|Admiral, without a map, we cannot proceed.
SC3_B264_STYLE_194_78|Youthful map requirement.|Admiral, we can't go on without a map.
SC3_B264_STYLE_194_112|Conversational impossibility without map.|We can't go any farther if we don't have a map.
SC3_B264_STYLE_194_146|Rough objection to going on without map.|Hold on. We can't go any farther without a map.
SC3_B264_STYLE_194_184|Elderly warning of map necessity.|Admiral, we cannot go on without a map.
SC3_B264_STYLE_194_216|Child pleads that a map is needed.|Admiral, we need a map!
SC3_B264_STYLE_194_244|Formal requirement of map for the way ahead.|Admiral, we need a map to proceed any farther.
DK4_MES_B264_R0068|Guide parts here and wishes them caution.|Well, this is where we part ways. Take care.
DK4_MES_B264_R0071|Maria asks Xien if preparations are ready.|Xien, are we ready?
DK4_MES_B264_R0075|Xien confirms all is prepared.|Yes. Everything is ready.
DK4_MES_B264_R0087|Yukihisa urges cautious advance.|Admiral, let us proceed with caution...
DK4_MES_B264_R0094|Maria confronts an unexpected dead end.|A dead end...
DK4_MES_B264_R0098|Xien ponders.|Hmm...
SC3_B264_CHOICE_716_0|Force a way through the obstruction.|Force a way through
SC3_B264_CHOICE_716_1|Investigate the situation.|Investigate
SC3_B264_STYLE_748_0|Polite tentative map reading: force through here.|According to the map... we're supposed to make our way through here.
SC3_B264_STYLE_748_40|Measured tentative map reading: go straight on.|According to the map, we're meant to keep going this way...
SC3_B264_STYLE_748_78|Youthful explanation that the map says go through here.|The map says we're supposed to get through here...
SC3_B264_STYLE_748_130|Conversational tentative reading of route through obstacle.|According to the map, it looks like we're meant to go through here...
SC3_B264_STYLE_748_174|Rough reading that route goes through here.|From the look of this map, we're supposed to get through here.
SC3_B264_STYLE_748_222|Elderly tentative reading of route beyond here.|Hmm. According to the map, we seem to be meant to make our way past here.
SC3_B264_STYLE_748_284|Child tentative reading that they must cross here.|Um, the map makes it look like we have to get past here.
SC3_B264_STYLE_748_340|Formal map reading requiring passage.|According to the map... we are to make our way through here.
DK4_MES_B264_R0131|Maria orders advance and tells everyone not to get separated.|Then let's go! Everyone, stay together!
DK4_MES_B264_R0138|System: some sailors appear to have left.|It seems some sailors have left.
DK4_MES_B264_R0146|Maria finds a path here.|Oh? There's a path here.
DK4_MES_B264_R0149|Trees hid it; Xien praises FI's noticing and proposes proceeding.|Hidden by the trees, was it? Well spotted, FI. Now, let us go on.
DK4_MES_B264_R0157|Maria recognizes destination and admires view.|This is the place... What a wonderful view.'''

def main():
    p=ROOT/'authored_B253_B264_v1.json';assert not p.exists()
    records=[r.split('|',2) for r in TEXT.splitlines()]
    packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in records]==expected and len(records)==162
    save(p,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=records,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges only; names/item terms remain provisional.',new_credit=0))
    print('Authored162 clean meanings and independent drafts in12 complete groups; current English unread.')

if __name__=='__main__':main()
