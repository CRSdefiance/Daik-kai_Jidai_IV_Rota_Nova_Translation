"""Clean Japanese meanings followed by independent complete-exchange English drafts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B286_B302_clean_20261110')
CONTEXTS={
286:"Actor204 welcomes the visitor, asks FI about a Goryeo celadon incense burner supposedly somewhere in East Asia, and explains the reported benefit for divination. Her wistful curiosity gives way to a practical warning about pirates nearby and proper equipment. The clean reply controls identify actor0, Rafael, despite this being SC3; do not silently replace him with Maria or infer a new relationship. Keep hearsay about the item and pirates, not confirmed magic or a known location. The artifact title and native speaker-name consumers remain provisional until binding.",
287:"A guildmaster asks Maria for help against organized, well-trained bandits targeting the town's gold and ivory. Local guards have little land-combat experience and inadequate weapons/armor. The request is five cargo holds of armor, expected to be sold somewhere in Europe. Maria anticipates the Mediterranean or North Sea and a potentially lengthy trip. The guildmaster can wait but stresses the town's survival and not forgetting; she repeats the same five-hold quantity. Do not turn holds into five suits or imply a timed deadline absent from the exchange.",
288:"After thanking Maria for the armor, the guildmaster admits expanding the guards revealed a shortage of firearms. He asks for five cargo holds of guns and says payment for everything will come then. Maria agrees. Preserve this next installment of the same quest, the five-hold unit and deferred combined payment; do not invent a second reward amount.",
289:"Maria returns quickly, but the guildmaster says the bandits seem to have noticed the town's stronger armament and started acquiring their own. He now requests two cargo holds of cannons urgently, with combined payment on delivery. Maria dryly complains he should have asked for everything together; he apologizes and asks her not to be cross. She repeats two holds. Preserve the inference about bandit behavior and the frustrating repeated trips rather than inventing a battle outcome.",
290:"The guildmaster believes the strengthened guard should deter the bandits, apologizes for repeated trips and pays costs plus reward. System panels report77000 coins and a small share increase in Sao Jorge. Maria then asks the bandits' hideout location. Startled, the guildmaster asks her intent; she responds teasingly. Rumor places them in ruins deep in the Sahara, and he cautions against recklessness. Do not promise the bandits have already surrendered or identify a particular ruin not named here.",
291:"Complete forest/fog exploration alternatives. Crew personality voices warn about needing a map, set out, then notice fog. Choices are push on or wait for clearing; after a dead end, push on anyway or find another route. Maria may try forcing through trees, tiring sailors, or search for a detour and find a branching path. Waiting includes two separate system ellipses, a one-day passage and relief that fog seems to have cleared. The destination comes into sight without being named. Keep the contrasting confidence, reluctance, childlike enthusiasm and formal/older phrasing. These are conditional alternatives, not a claim every result happens in one continuous playthrough. Do not invent a clearing time guarantee, supplies loss or casualties.",
292:"Complete humid-jungle/cave exploration alternatives. Personality voices warn about wandering without direction or a map. In a pitch-black cave the choices are feeling ahead or making a light. On the dark branch Maria's eyes adjust, the captain feels something, a large snake threatens a party member, and Samwell suggests an Indian python with an uncertain aside. Maria retreats; sailors seem injured. They emerge apparently near ruins, with different degrees of surprise and certainty. The light branch reveals bats: crew panic, Maria thinks they seem harmless and insists on advancing; sailors seem fatigued. Other variants celebrate leaving the jungle and reaching ruins. Preserve snake versus bats, injury versus fatigue, the species uncertainty and uncertainty about location. Dynamic207/208 controls and native identities need binding; do not infer future crew assignments or invent venom/deaths.",
293:"A guide first requires a map to the ruins. Crew variants marvel at an ancient city in this unexpected place. The guide says the map apparently locates the actual ruins off this island, across the water. Maria suggests returning to port, but the guide has a small boat and intends to proceed with it: only this party is qualified, and sailors must not learn the location. After one day they arrive, continue overland and spot the ruins. Preserve the separate island and boat, secrecy/qualification restriction and one day; do not add a secret society, burial site, named island or identity of an unstated destination. Closing crew variants differ in certainty that these are the ruins.",
}
TEXT=r'''DK4_MES_B286_R0005|The named host welcomes the visitor.|Welcome!
DK4_MES_B286_R0009|She asks FI about the Goryeo celadon incense burner, reportedly somewhere in East Asia.|FI, have you heard of the Goryeo Celadon Incense Burner? They say it's somewhere in East Asia.
DK4_MES_B286_R0013|Using it for divination supposedly makes predictions far more accurate; she longs to try.|They say it makes your fortune-telling much more accurate. Oh, I'd love to try it just once...
DK4_MES_B286_R0029|Actor0 responds with mild interest.|Hmm. Really?
DK4_MES_B286_R0034|She remembers something else to mention.|Oh, that reminds me.
DK4_MES_B286_R0038|Pirates seem active nearby lately; she advises proper equipment.|Pirates seem to be causing trouble around here lately. Make sure you're properly equipped.
DK4_MES_B286_R0042|Actor0 is concerned, thanks her and promises caution.|Really? ...That sounds dangerous. Thanks. I'll be careful.
DK4_MES_B286_R0046|She says goodbye.|See you again!
DK4_MES_B287_R0004|The guildmaster asks whether she will accept a job.|Hello there. I've got a job for you. Interested?
DK4_MES_B287_R0008|Maria asks what it is.|What is it?
DK4_MES_B287_R0012|A bandit group has recently been appearing in town.|A band of raiders has been turning up in town lately.
DK4_MES_B287_R0016|Maria is concerned by the mention of bandits.|Bandits? That sounds dangerous.
DK4_MES_B287_R0020|They target the town's gold and ivory and are well trained and organized.|They mainly go after the gold and ivory here. They're well trained and organized, too.
DK4_MES_B287_R0023|Local guards lack land-battle experience and adequate arms/armor, and are struggling.|Our guards have little experience fighting on land, and they're short on weapons and armor. They're having a hard time.
DK4_MES_B287_R0026|He requests five cargo holds of armor, sold somewhere in Europe.|I'd like you to buy five holds of armor for us. You should be able to find it somewhere in Europe.
DK4_MES_B287_R0029|Maria anticipates the Mediterranean or North Sea and warns it may take time.|The Mediterranean or the North Sea, then... This may take a while.
DK4_MES_B287_R0032|He can wait but the matter is vital; he insists she not forget.|I can wait. Still, this is a matter of life and death for us. Please don't forget.
DK4_MES_B287_R0036|Maria confirms five holds of armor and promises to remember.|Five holds of armor. All right. I won't forget.
DK4_MES_B287_R0039|He stresses that promise.|I'm counting on you.
DK4_MES_B288_R0006|He thanks her on delivery.|Ah, thank you!
DK4_MES_B288_R0010|Expanding the guard exposed a shortage of guns as well.|...The thing is, we expanded the guard and realized we're short on guns, too.
DK4_MES_B288_R0014|He apologetically requests five holds of guns and promises combined payment then.|Sorry, but could you bring us five holds of guns, too? I'll pay you for everything then.
DK4_MES_B288_R0018|Maria agrees to the guns.|Guns, then. All right.
DK4_MES_B289_R0005|He notes her quick return.|Oh, you're back already!
DK4_MES_B289_R0009|The bandits seem to have noticed the town's stronger arms and begun arming themselves.|We've got a problem. It looks like they noticed we're better armed. Now they're getting weapons of their own.
DK4_MES_B289_R0012|He says the town now needs cannons too.|At this rate, we'll need cannons, too.
DK4_MES_B289_R0015|He requests two holds urgently and promises combined payment then.|Just two holds. Please bring them as quickly as you can. I'll pay you for everything then.
DK4_MES_B289_R0019|Maria complains he should have made the requests together.|...You could have asked for everything at once.
DK4_MES_B289_R0023|He apologizes and asks her not to be cross.|Sorry about that. Come on, don't be like that.
DK4_MES_B289_R0026|Maria repeats the two-hold cannon request.|Two holds of cannons, then.
DK4_MES_B290_R0005|He is satisfied and believes the stronger guard should deter the bandits.|Perfect! With security this tight, they should give up.
DK4_MES_B290_R0009|He apologizes for the repeated trips and gives costs and reward.|Sorry I made you go back and forth so many times. Here's your payment and reward. Thank you!
DK4_MES_B290_R0014|System awards77000 coins.|Received 77,000 coins.
DK4_MES_B290_R0036|System reports a small share increase in Sao Jorge.|Your market share in Sao Jorge increased slightly!
DK4_MES_B290_R0047|Maria asks where the bandits' hideout is.|By the way, could you tell me where those bandits are hiding?
DK4_MES_B290_R0050|He is startled and asks why she wants to know.|W-what? What are you planning to do?
DK4_MES_B290_R0053|Maria gives a teasing nonanswer.|Oh, I wonder...
DK4_MES_B290_R0057|He finds her unusually curious; rumor places the hideout in ruins deep in the Sahara and he warns against rashness.|You're an odd one. Rumor has it they're hiding in some ruins deep in the Sahara. I wouldn't do anything reckless.
SC3_B291_STYLE_24_0|Formal warning that they may get lost without a map.|Admiral, we may lose our way without a map.
SC3_B291_STYLE_24_36|Firm warning that they will get lost without a map.|Admiral, we'll get lost without a map.
SC3_B291_STYLE_24_68|Casual worried warning about getting lost without a map.|Admiral, we're going to get lost without a map.
SC3_B291_STYLE_24_104|Conversational prediction that they will get lost without a map.|Admiral, I think we'll get lost without a map.
SC3_B291_STYLE_24_140|Rough warning that they will get lost without a map.|Admiral, we'll get lost out here without a map.
SC3_B291_STYLE_24_176|Older firm warning about losing their way without a map.|Admiral, we'll lose our way if we have no map.
SC3_B291_STYLE_24_214|Childlike request that the admiral provide a map.|Admiral, we need a map!
SC3_B291_STYLE_24_240|Formal older warning about losing the way without a map.|Admiral, without a map, we shall lose our way.
SC3_B291_STYLE_348_0|Polite proposal to depart.|Shall we set out, then?
SC3_B291_STYLE_348_22|Conversational proposal to go.|Well, shall we go?
SC3_B291_STYLE_348_40|Energetic invitation to go.|Come on, let's go!
SC3_B291_STYLE_348_56|Friendly proposal to set off.|Well, let's get going.
SC3_B291_STYLE_348_80|Rough energetic departure.|Right, let's move out!
SC3_B291_STYLE_348_100|Older speaker urges a spirited start.|Come along! Let's get moving!
SC3_B291_STYLE_348_124|Childlike enthusiastic departure cry.|Ready, set, go!
SC3_B291_STYLE_520_0|Polite observation that fog is coming in.|The fog is rolling in.
SC3_B291_STYLE_520_20|Formal older observation of incoming fog.|Fog is coming in, I see.
SC3_B291_STYLE_520_40|Conversational observation of incoming fog.|Here comes the fog.
SC3_B291_STYLE_520_56|Conversational concern that it has become foggy.|Oh, it's gotten foggy.
SC3_B291_STYLE_520_76|Rough observation of very heavy fog.|That's some thick fog.
SC3_B291_STYLE_520_96|Older observation that fog has rolled in.|The fog's come in, hasn't it?
SC3_B291_STYLE_520_114|Childlike amazement at the fog.|Wow, look at all this fog!
SC3_B291_CHOICE_674_0|Choice to advance despite the fog.|Keep going
SC3_B291_CHOICE_674_1|Choice to wait until the fog clears.|Wait for it to clear
DK4_MES_B291_R0103|Maria decides to try moving ahead for now.|Let's try moving ahead for now.
SC3_B291_STYLE_758_0|Polite assessment that it seems to be a dead end.|It looks like a dead end.
SC3_B291_STYLE_758_26|Restrained reaction to a dead end.|A dead end...
SC3_B291_STYLE_758_42|Casual disappointed reaction to a dead end.|Aw, it's a dead end.
SC3_B291_STYLE_758_66|Conversational reaction to a dead end.|It's a dead end...
SC3_B291_STYLE_758_82|Older assessment that it seems to be a dead end.|It seems we've reached a dead end.
SC3_B291_STYLE_758_108|Childlike disappointed reaction to a dead end.|Aw, a dead end!
SC3_B291_STYLE_758_132|Formal older dismay at a dead end.|Oh, dear. A dead end.
SC3_B291_CHOICE_938_0|Choice to push on even at the dead end.|Push on anyway
SC3_B291_CHOICE_938_1|Choice to look for a way around.|Look for a detour
DK4_MES_B291_R0143|Maria wonders if they can force a way through the trees.|Could we push our way through the trees?
SC3_B291_STYLE_1018_0|Polite agreement to try.|I'll try.
SC3_B291_STYLE_1018_14|Polite suggestion to try.|Let's try it.
SC3_B291_STYLE_1018_32|Casual speaker thinks the demand is unreasonable but agrees.|This is crazy... All right, I'll try.
SC3_B291_STYLE_1018_72|Conversational agreement to try.|I'll give it a try.
SC3_B291_STYLE_1018_86|Rough speaker commits to going all the way.|All right! Let's go all the way!
SC3_B291_STYLE_1018_112|Older speaker calls the request reckless but will try.|That's a reckless thing to ask. Still, I'll give it a try.
SC3_B291_STYLE_1018_152|Childlike speaker protests the unreasonable demand then agrees energetically.|This is crazy! ...All right, here I go!
DK4_MES_B291_R0173|System reports apparent sailor fatigue.|The sailors seem fatigued.
DK4_MES_B291_R0178|Maria proposes searching for a detour.|Let's look for a way around.
SC3_B291_STYLE_1332_0|Polite excited report of a branching path.|Admiral, I've found a fork in the path!
SC3_B291_STYLE_1332_30|Formal report of a branching path.|Admiral, there's a fork in the path.
SC3_B291_STYLE_1332_58|Casual speaker notices a branching path on closer inspection.|Admiral, look! There's a fork in the path!
SC3_B291_STYLE_1332_94|Conversational report of a path in this direction.|Admiral, there's a path over here!
SC3_B291_STYLE_1332_122|Rough excited report of a path in this direction.|Admiral, there's a path this way!
SC3_B291_STYLE_1332_150|Older speaker thinks they can advance this way.|Admiral, it looks like we can go this way!
SC3_B291_STYLE_1332_182|Childlike call for the admiral to come this way.|Admiral! Over here!
SC3_B291_STYLE_1332_210|Formal older speaker reports a path in this unexpected spot.|There's a path right here!
DK4_MES_B291_R0213|Maria says moving in these conditions is dangerous and chooses to wait for clearing.|It's dangerous to wander around in this fog. Let's wait for it to clear.
SC3_B291_STYLE_1664_0|Polite assessment that waiting seems better.|That seems the better choice.
SC3_B291_STYLE_1664_28|Casual agreement that waiting is good.|That's a good idea.
SC3_B291_STYLE_1664_42|Conversational agreement that waiting is good.|Yes, that's a good idea.
SC3_B291_STYLE_1664_56|Rough agreement to wait.|Yeah. Let's do that.
SC3_B291_STYLE_1664_78|Older speaker sees no other choice.|There's nothing else for it.
SC3_B291_STYLE_1664_104|Childlike agreement to wait.|Okay, let's do that.
SC3_B291_STYLE_1664_126|Formal older speaker calls waiting safer.|That would be safer.
DK4_MES_B291_R0242|First system pause while waiting.|...
DK4_MES_B291_R0246|Longer second system pause while waiting.|......
DK4_MES_B291_R0253|One day passes.|One day passed.
DK4_MES_B291_R0257|Maria thinks the fog has finally cleared and urges departure.|It looks like it's finally cleared. Come on, let's go.
SC3_B291_STYLE_1960_0|Polite report that the destination is coming into sight.|It's coming into view.
SC3_B291_STYLE_1960_18|Casual report that the destination is coming into sight.|There it is. I can see it now.
SC3_B291_STYLE_1960_32|Rough report that it is coming into sight.|It's in sight!
SC3_B291_STYLE_1960_46|Questioning report that it is coming into sight.|Is that it coming into view?
SC3_B292_STYLE_24_0|Polite warning that wandering this jungle aimlessly is dangerous.|Admiral, it's dangerous to wander through a jungle like this without knowing the way.
SC3_B292_STYLE_24_52|Casual protest that aimless jungle travel is impossible.|Admiral, we can't just wander through a jungle like this with no idea where we're going.
SC3_B292_STYLE_24_106|Conversational warning about aimless jungle travel.|Admiral, it's dangerous to wander around a jungle like this with no direction.
SC3_B292_STYLE_24_156|Rough refusal to wander the jungle aimlessly.|Admiral, I'm not wandering around a jungle like this with no idea where we're going.
SC3_B292_STYLE_24_214|Older warning about aimless jungle travel.|Admiral, wandering through such a jungle without direction is dangerous.
SC3_B292_STYLE_24_266|Childlike warning that jungle travel without a map is dangerous.|Admiral, it's dangerous to walk through this jungle without a map!
SC3_B292_STYLE_24_326|Formal older warning about aimless jungle travel.|Admiral, it is dangerous to wander through a jungle like this without knowing the way.
SC3_B292_STYLE_446_0|Conversational proposal to go.|Well, shall we go?
SC3_B292_STYLE_446_16|Polite proposal to go.|Then let us go.
SC3_B292_STYLE_446_36|Enthusiastic urging to set out.|Come on! Let's get moving!
SC3_B292_STYLE_446_62|Friendly proposal to depart.|Well, let's go.
SC3_B292_STYLE_446_84|Rough departure call.|Right, let's go.
SC3_B292_STYLE_446_100|Older departure call.|Well then, off we go.
DK4_MES_B292_R0062|Maria remarks on the very high humidity and difficulty crossing this place.|What a climate... It's so humid. Getting through here won't be easy.
SC3_B292_STYLE_666_0|Restrained discovery of a cave in this place.|There's a cave here...
SC3_B292_STYLE_666_24|Childlike surprise on finding a cave.|Huh? Look, a cave!
DK4_MES_B292_R0089|Maria remarks that it is pitch-black.|It's pitch-black...
DK4_MES_B292_R0093|A crew role addresses the admiral hesitantly.|Admiral...
SC3_B292_CHOICE_770_0|Choice to advance by feeling in the dark.|Feel our way ahead
SC3_B292_CHOICE_770_1|Choice to make a light.|Light a fire
DK4_MES_B292_R0108|Maria's eyes are adjusting; she proposes continuing this way.|My eyes are adjusting... Shall we keep going like this?
DK4_MES_B292_R0112|The captain feels something and wonders what it is.|Hm? What's this I'm touching...?
DK4_MES_B292_R0115|A crew role warns of a giant snake and cries out in alarm for the party, without an explicit count or completed outcome.|Admiral! A giant snake! Ah! The crew!
DK4_MES_B292_R0126|Samwell cries that it is an Indian python, then adds uncertainly that he thinks so.|Whoa! An Indian python! ...I think?
DK4_MES_B292_R0132|Maria judges the opponent too much and orders retreat.|...We can't take this on. Everyone, retreat!
DK4_MES_B292_R0139|System reports that sailors appear injured, with no explicit count.|Sailors seem to have been injured.
DK4_MES_B292_R0145|Maria wonders where they have emerged.|Where have we come out...?
SC3_B292_STYLE_1150_0|Polite uncertainty; they seem to be near ruins.|...I'm not sure, but we seem to be near the ruins.
SC3_B292_STYLE_1150_46|Formal cautious assessment that they appear near ruins.|...I believe we're near the ruins.
SC3_B292_STYLE_1150_76|Casual speaker is unsure where they are but guesses near ruins.|Here? ...Uh, I'm not sure, but aren't we near the ruins?
SC3_B292_STYLE_1150_142|Conversational hesitation and uncertainty that they seem near ruins.|Um... Huh? ...It looks like we're near the ruins.
SC3_B292_STYLE_1150_180|Rough surprised realization that this may be near the ruins.|Whoa! ...Aren't we near the ruins?!
SC3_B292_STYLE_1150_230|Older surprise and assessment they apparently emerged near ruins.|Where are we?! ...Hmm. It seems we've come out near the ruins.
SC3_B292_STYLE_1150_286|Childlike uncertainty, then delight that they seem near ruins.|Here? Um... Huh? I'm not really sure, but it looks like we're near the ruins! Lucky us!
SC3_B292_STYLE_1150_370|Formal older cautious assessment of their position.|Hmm... It appears we're near the ruins.
DK4_MES_B292_R0174|Maria proposes making a light.|Let's get a light going...
DK4_MES_B292_R0178|Maria reacts to bats as yet another obstacle.|Now bats?! Honestly, it's one thing after another...
SC3_B292_STYLE_1688_0|Polite alarm at the overwhelming number.|There are too many!
SC3_B292_STYLE_1688_18|Casual alarm at the overwhelming number.|There's way too many of them!
SC3_B292_STYLE_1688_38|Conversational scream and alarm at an extraordinary number of bats.|Aah! Admiral, there shouldn't be this many!
SC3_B292_STYLE_1688_82|Rough alarm at the overwhelming number.|There's too many of them!
SC3_B292_STYLE_1688_100|Older speaker says they cannot advance while dealing with so many bats.|Admiral! We cannot go on while fighting off so many bats!
SC3_B292_STYLE_1688_170|Childlike scream and disgust at bats.|Aah, bats! They're so creepy!
DK4_MES_B292_R0203|Maria thinks the bats seem harmless and orders advancing without worrying about them.|These bats don't seem dangerous. Ignore them and keep moving.
DK4_MES_B292_R0213|System reports apparent sailor fatigue.|The sailors seem fatigued.
SC3_B292_STYLE_2054_0|Polite excited congratulations on getting through the jungle.|We did it, Admiral! We're out of the jungle!
SC3_B292_STYLE_2054_44|Formal excited report of getting through the jungle.|We've made it through the jungle!
SC3_B292_STYLE_2054_66|Casual excitement on getting through the jungle.|We did it, Admiral! We made it out!
SC3_B292_STYLE_2054_102|Conversational relief on getting through the jungle.|What a relief! We're out of the jungle!
SC3_B292_STYLE_2054_132|Rough celebration on getting through the jungle.|We did it, Admiral! We're through the jungle!
SC3_B292_STYLE_2054_168|Older celebration on getting through the jungle.|We did it! We've made it through the jungle!
SC3_B292_STYLE_2054_202|Formal excited praise on getting through the jungle.|Well done, Admiral! We've made it through the jungle!
SC3_B292_STYLE_2332_0|Polite cautious assessment that they have reached the ruins.|Admiral, it seems we've reached the ruins.
SC3_B292_STYLE_2332_28|Casual identification of the ruins.|Admiral, these are the ruins.
SC3_B292_STYLE_2332_50|Conversational identification of the ruins.|Admiral, this is where the ruins are.
SC3_B292_STYLE_2332_70|Rough cautious assessment of reaching the ruins.|Admiral, looks like we've found the ruins.
SC3_B292_STYLE_2332_92|Older cautious assessment of reaching the ruins.|Admiral, it seems we've reached the ruins.
SC3_B292_STYLE_2332_120|Childlike identification of the ruins.|Admiral! These are the ruins, right?
SC3_B292_STYLE_2332_142|Formal older confirmation of reaching the ruins.|Admiral, we've reached the ruins at last.
DK4_MES_B293_R0011|The guide first asks them to obtain a map to the ruins.|First, please obtain a map to the ruins.
SC3_B293_STYLE_96_0|Polite disbelief at an ancient city in this place.|It's hard to believe there was an ancient city here...
SC3_B293_STYLE_96_56|Restrained amazement at an ancient city here.|An ancient city, in a place like this...
SC3_B293_STYLE_96_92|Casual amazement at an ancient city here.|So there used to be an ancient city here.
SC3_B293_STYLE_96_128|Conversational amazement at an ancient city here.|To think there was an ancient city here...
SC3_B293_STYLE_96_166|Rough amazement at an ancient city here.|An ancient city in a place like this, huh...
SC3_B293_STYLE_96_208|Older disbelief at an ancient city here.|It's hard to believe an ancient city once stood in a place like this.
SC3_B293_STYLE_96_266|Childlike amazement that there was once a town here.|So there used to be a town here, too.
SC3_B293_STYLE_96_310|Formal older amazement at an ancient city here.|To think an ancient city once stood here...
DK4_MES_B293_R0043|The guide says the map appears to place the ruins off this island.|Actually... According to this map, it seems the ruins aren't on this island.
DK4_MES_B293_R0047|Maria is surprised.|What?
DK4_MES_B293_R0053|The guide says they must cross the water.|...We'll have to cross the sea.
DK4_MES_B293_R0058|Maria proposes returning to port.|Then let's return to port.
DK4_MES_B293_R0062|The guide has prepared a small boat and intends to continue with it.|No, I've prepared a small boat. We'll continue in that.
DK4_MES_B293_R0065|Only this party is qualified; the guide wants the ruins' location kept from sailors.|You are the only ones who are qualified. Please make sure the sailors do not learn where the ruins are.
DK4_MES_B293_R0074|One day passes.|One day passed.
DK4_MES_B293_R0078|They arrive and the guide says to continue overland.|We're here. We'll go by land from this point.
DK4_MES_B293_R0081|The guide spots what they seek.|Oh! There it is!
SC3_B293_STYLE_914_0|Polite report that the ruins have been found.|Admiral, we've found the ruins.
SC3_B293_STYLE_914_28|Casual report that the ruins have been found.|Admiral, we found them!
SC3_B293_STYLE_914_54|Conversational identification of the ruins ahead.|Admiral, those are the ruins.
SC3_B293_STYLE_914_74|Rough uncertain assessment that they have found the ruins.|Admiral, looks like we found the ruins.
SC3_B293_STYLE_914_104|Older uncertain assessment that they have found the ruins.|Admiral, it seems we've found the ruins.
SC3_B293_STYLE_914_134|Childlike recognition of the ruins ahead.|Admiral! Those are the ruins, right?
SC3_B293_STYLE_914_166|Formal older cautious recognition of the ruins.|Admiral, it appears we've found the ruins.
DK4_MES_B293_R0110|Maria thinks they have arrived and says she is coming.|It seems we've arrived... I'm coming.'''

def main():
    output=ROOT/'authored_B286_B293_v1.json';assert not output.exists()
    rows=[r.split('|',2) for r in TEXT.splitlines()];packet=load(ROOT/'clean_source_packet.json')
    expected=[r['id'] for g in packet['groups'] if g['block'] in CONTEXTS for r in g['records']]
    assert [r[0] for r in rows]==expected and len(rows)==191
    save(output,dict(contexts={str(k):v for k,v in CONTEXTS.items()},records=rows,current_English_not_consulted=True,
        source_gloss_precedes_independent_draft_in_each_entry=True,source='Complete clean Japanese exchanges only; item terms and native role/voice consumers remain provisional.',new_credit=0))
    print('Authored191 clean meanings andindependent drafts in eight complete groups;current story English unread.')

if __name__=='__main__':main()
