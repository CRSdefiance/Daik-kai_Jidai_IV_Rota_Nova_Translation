"""Source-first mountain, cliff and Istanbul-job exchanges with credited context preserved."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import save

ROOT = Path('work/Lil361_B283_B298_clean_20261110')
TEXT = r'''@293
DK4_MES_B293_R0012|The guide asks whether they brought a map and refuses to go farther without one, even at their request.|Did you bring a map? Even for you, I'm not going any farther without one.
DK4_MES_B293_R0025|The guide acknowledges that they have brought a map.|Good, you brought a map.
SC2_B293_STYLE_194_0|A polite companion says they cannot proceed without a map.|Admiral, we can't go any farther without a map.
SC2_B293_STYLE_194_40|A reserved companion says a map is required to proceed.|Admiral, without a map, we cannot proceed.
SC2_B293_STYLE_194_78|A casual companion tells the Admiral they cannot proceed without a map.|Admiral, we can't keep going without a map.
SC2_B293_STYLE_194_112|A feminine voice says it is impossible to proceed without a map.|We can't go any farther if we don't have a map.
SC2_B293_STYLE_194_146|A rough voice objects that they cannot proceed without a map.|Hey, we ain't going any farther without a map.
SC2_B293_STYLE_194_184|An older companion says a map is necessary to go farther.|Admiral, we can't go on without a map.
SC2_B293_STYLE_194_216|A childlike companion pleads that they need a map.|Admiral, we need a map!
SC2_B293_STYLE_194_244|An older formal voice says a map is needed beyond this point.|Admiral, we cannot continue beyond this point without a map.
DK4_MES_B293_R0069|Lil exhales in relief at finally completing the climb.|Whew... We finally made it to the top!
DK4_MES_B293_R0072|The guide says this is where they part and urges caution.|This is where we part ways. Take care.
DK4_MES_B293_R0075|Lil confidently believes these ruins hold a clue to the Proof.|I'm sure these ruins hold a clue to the Proof...
DK4_MES_B293_R0086|A companion asks why she thinks so.|Huh? Why?
DK4_MES_B293_R0093|Lil admits it is merely an intuition.|Just a feeling. I don't know why, but I have a feeling.
DK4_MES_B293_R0104|A companion urges caution, saying a place like this warrants being almost timid.|Let's be careful. In a place like this, there's no such thing as too cautious.
DK4_MES_B293_R0111|A companion notices difficulty seeing ahead.|Huh? I can't really see ahead...
SC2_B293_STYLE_908_0|A polite companion warns the Admiral about fog and urges care.|Admiral, it's fog! Be careful!
SC2_B293_STYLE_908_36|A reserved voice thinks it is fog and recommends proceeding carefully.|It seems to be fog. Let's proceed with caution.
SC2_B293_STYLE_908_70|A casual voice notes thick fog and inability to see anything around them.|That's some thick fog. I can't see a thing around us.
SC2_B293_STYLE_908_114|A feminine voice says the heavy fog makes it impossible to tell where anyone is.|What thick fog! I can't tell where anyone is.
SC2_B293_STYLE_908_174|A rough voice is frustrated because fog obscures the surroundings.|Great... I can't see a thing through this fog.
SC2_B293_STYLE_908_208|An older companion warns the Admiral of fog and to watch their footing.|Admiral, it's fog. Mind your footing.
SC2_B293_STYLE_908_242|A childlike voice exclaims about the thick fog and inability to see.|Wow, that's thick fog! I can't see anything!
SC2_B293_STYLE_908_290|An older formal voice observes the fog.|Fog, is it...
DK4_MES_B293_R0142|A companion says the thick fog quickly obscured everything and asks FI if she is all right.|What thick fog! Everything disappeared in no time. Are you all right, FI?
DK4_MES_B293_R0149|Lil angrily asks who is in her way, then realizes she hit a tree and cries out in pain.|Who's standing in my way?! ...Oh, I walked into a tree. Oww!
SC2_B293_STYLE_1420_0|A polite companion asks the Admiral what to do.|Admiral, what should we do?
SC2_B293_STYLE_1420_20|A casual companion asks the Admiral what to do next.|What now, Admiral?
SC2_B293_STYLE_1420_38|A rough companion asks the Admiral for a decision.|Admiral, what's the plan?
SC2_B293_STYLE_1420_60|An older voice asks the Admiral what they are going to do.|What are we to do, Admiral?
SC2_B293_STYLE_1420_84|A childlike voice calls to the Admiral and asks what to do.|Admiral! What do we do now?
SC2_B293_STYLE_1420_110|An older formal voice asks for the Admiral's decision.|What shall we do, Admiral?
DK4_MES_B293_R0186|A companion asks FI what they should do.|What should we do, FI?
DK4_MES_B293_R0193|Lil pauses to consider.|Let's see...
SC2_B293_CHOICE_1620_0|The first choice is to wait for a while.|Wait a while
SC2_B293_CHOICE_1620_1|The second choice is to hurry out of this location.|Hurry out of here
SC2_B293_STYLE_1686_0|A polite companion asks whether they are waiting here.|Are we going to wait here?
SC2_B293_STYLE_1686_22|A reserved companion tentatively confirms that they will wait here.|We're to wait here, then...?
SC2_B293_STYLE_1686_46|A casual companion checks that they are waiting at this spot.|We're waiting here, right?
SC2_B293_STYLE_1686_68|A feminine voice asks if she means to wait here.|You mean we're waiting here?
SC2_B293_STYLE_1686_90|A rough voice checks that the plan is to wait.|We're waiting, huh?
SC2_B293_STYLE_1686_108|An older companion confirms that they will wait.|So we wait, then?
SC2_B293_STYLE_1686_124|A childlike voice complains about waiting because they are hungry.|What? We have to wait? But I'm hungry!
SC2_B293_STYLE_1686_172|An older formal voice understands that they will wait.|I see. We shall wait, then.
DK4_MES_B293_R0242|A companion objects to waiting right here in the fog.|What? Here, in all this fog?
DK4_MES_B293_R0249|Lil says advancing is impossible because they would get separated, and confidently expects the fog to clear.|We can't go through fog like this. We'd get separated for sure. Don't worry! I'm sure it'll clear!
SC2_B293_STYLE_2052_0|A polite companion understands and praises the Admiral's judgment.|I see. Just what I'd expect from you, Admiral.
SC2_B293_STYLE_2052_28|A reserved companion reflects and praises the Admiral.|Hmm... Well judged, Admiral.
SC2_B293_STYLE_2052_54|A casual companion understands and praises the Admiral.|Oh, I get it. Nice thinking, Admiral!
SC2_B293_STYLE_2052_80|A feminine voice realizes the reasoning and enthusiastically praises the Admiral.|Oh, of course! That's our admiral!
SC2_B293_STYLE_2052_108|A rough companion understands and acknowledges the Admiral's good judgment.|So that's it. Good thinking, Admiral!
SC2_B293_STYLE_2052_142|An older companion understands and praises the Admiral.|I see. Well thought out, Admiral.
SC2_B293_STYLE_2052_170|A childlike voice understands and calls the Admiral clever.|Ohhh! You're so smart, Admiral!
SC2_B293_STYLE_2052_206|An older formal voice admires the Admiral's reasoning.|Ah, so that is your reasoning. Well considered, Admiral.
DK4_MES_B293_R0278|Lil smugly accepts the praise.|Of course.
DK4_MES_B293_R0284|A companion concedes the point while teasing that it is a good decision for FI.|That's true. Pretty good judgment, for you, FI!
DK4_MES_B293_R0288|Lil indignantly insists that she always shows good judgment.|I always have good judgment!
DK4_MES_B293_R0300|The system announces that one day has passed.|One day has passed.
DK4_MES_B293_R0304|Lil celebrates the clearing fog and calls everyone onward.|Yes! The fog's clearing! Come on, everyone. Let's go!
SC2_B293_STYLE_2558_0|A polite companion asks whether the Admiral is serious about proceeding.|Admiral, are you serious?
SC2_B293_STYLE_2558_20|A casual companion doubts whether this plan will be safe.|Are you sure we'll be all right?
SC2_B293_STYLE_2558_42|A feminine voice is startled at proceeding through this fog and doubts its safety.|We're going through this?! ...Will we be all right?
SC2_B293_STYLE_2558_80|A rough companion incredulously asks if the plan is serious.|Hey, are you serious?
SC2_B293_STYLE_2558_102|An older voice asks whether they really will go.|Are we really going, then?
SC2_B293_STYLE_2558_122|A childlike voice stammers and worries whether they will be safe.|R-really? Are we gonna be okay...?
SC2_B293_STYLE_2558_154|An older formal voice doubts the plan's safety.|Will we be all right...?
DK4_MES_B293_R0342|A companion is surprised at going through the fog and worries about safety.|What, through this fog? Will we be all right...?
DK4_MES_B293_R0348|Lil confidently reassures the companion and urges moving.|We'll be fine! Come on, let's go!
DK4_MES_B293_R0359|A companion urgently asks her to wait.|W-wait for me!
DK4_MES_B293_R0367|Lil asks whether everyone is following.|Is everyone keeping up?
SC2_B293_STYLE_2942_0|A polite companion tentatively reports that some people have become separated.|It looks as though some of us got separated...
SC2_B293_STYLE_2942_38|A reserved companion reports apparent separation of party members.|...It seems some of the party became separated.
SC2_B293_STYLE_2942_74|A casual voice thinks some got separated because visibility was poor.|It was so hard to see, I think some of us got separated...
SC2_B293_STYLE_2942_126|A feminine voice thinks a few are missing and have apparently become separated.|We're a few short... It looks like some of us got separated...
SC2_B293_STYLE_2942_180|A rough voice thinks some got separated and says the fog made it unavoidable.|Looks like some of us got separated. Couldn't help it in this fog, I guess...
SC2_B293_STYLE_2942_238|An older voice tentatively reports several people separated.|...It seems a few of us got separated.
SC2_B293_STYLE_2942_274|A childlike voice notices not everyone is present and assumes they got separated in the fog.|Um... We're missing some people. They must've got lost in the fog...
SC2_B293_STYLE_2942_330|An older formal voice thinks fog caused several people to become separated.|Hmm... It seems a few of us became separated in the fog.
DK4_MES_B293_R0396|A companion thinks poor visibility in the fog caused several people to become separated.|We couldn't see through the fog, so it looks like some of us got separated.
DK4_MES_B293_R0403|The system announces a small reduction in sailor numbers, without stating deaths.|Your crew has decreased slightly!
DK4_MES_B293_R0415|Lil excitedly recognizes the destination.|Oh, is this it?!
DK4_MES_B293_R0427|A companion thinks they have arrived.|Looks like we're here!
@294
DK4_MES_B294_R0005|Lil notices a sign saying the way ahead is a dead end.|Huh? It says there's a dead end ahead.
DK4_MES_B294_R0008|The guide apologizes and reports the road to the ruins was recently blocked by a rockfall.|Sorry about that. I hear a recent rockfall has blocked the road to the ruins.
DK4_MES_B294_R0018|Lil asks whether this means they cannot go to the ruins.|Then we can't get to the ruins?
DK4_MES_B294_R0024|A polite alternative asks whether they cannot reach the ruins.|Does that mean we can't reach the ruins?
DK4_MES_B294_R0031|The guide thinks access will be impossible for a while.|Hmm... Probably not for a while.
DK4_MES_B294_R0035|Lil asks how long a while means.|How long is "a while"...?
DK4_MES_B294_R0039|The guide has no idea; since no one goes so far out, it could be ten or twenty years.|Who knows? Nobody goes all the way out there. Could be ten years, could be twenty...
DK4_MES_B294_R0051|A companion asks FI what to do because they cannot wait that long.|What now, FI? We can't wait that long, can we?
DK4_MES_B294_R0057|The guide says that if they insist on going there is a somewhat dangerous option of climbing a cliff.|If you're set on going, there's another way. It's a bit dangerous, but you could climb the cliff.
DK4_MES_B294_R0061|Lil is surprised at the prospect of climbing a cliff.|The cliff?
DK4_MES_B294_R0065|The guide says even local people rarely attempt the climb.|Even the locals hardly ever attempt it.
DK4_MES_B294_R0069|Lil defiantly declares that she will show she can climb it.|Then I'll show you I can climb it!
DK4_MES_B294_R0076|After the preserved credited line acknowledges her resolve, the guide agrees to lead them to the cliff, asks for a map and proposes meeting here.|All right, I'll take you to the cliff. Bring a map, and we'll meet here.
DK4_MES_B294_R0080|Lil asks about the required map.|A map?
DK4_MES_B294_R0084|The destination is a hidden Christian settlement; even the guide does not know the exact route beyond the cliff and thinks a map can be bought somewhere in the Mediterranean.|Yes. It's a hidden Christian settlement. Even I don't know the exact route once we're up the cliff. I think you can get a map in one of the Mediterranean towns.
@295
DK4_MES_B295_R0005|The contact wants the visitor to find an item.|There's something I'd like you to find.
DK4_MES_B295_R0008|The emperor intends to show his collection to an honored guest, a vassal king he is inviting.|His Majesty the Emperor is inviting a vassal king to visit. He plans to show his collection to his honored guest.
DK4_MES_B295_R0011|Lil asks about the collection.|His collection?
DK4_MES_B295_R0015|The emperor collects rare objects from all over the world and especially wants one item added before the exhibition.|His Majesty collects rarities from around the world. There's one item he's determined to add before he shows his collection.
DK4_MES_B295_R0018|Lil asks which item he means.|What's that?
DK4_MES_B295_R0022|The item is the Heavenly Wristband, said to grant its owner exceptional leadership ability.|It's called the Heavenly Wristband. They say it grants its owner exceptional powers of leadership.
DK4_MES_B295_R0026|Lil responds with mild interest.|Hmm.
DK4_MES_B295_R0030|The contact speculates that it is probably intended to display the Ottoman Empire's grandeur.|Well, it's probably meant to show off the grandeur of the Ottoman Empire.
DK4_MES_B295_R0033|Lil skeptically reflects that rulers everywhere are equally vain.|Grandeur, huh... Rulers are just as vain no matter where you go.
DK4_MES_B295_R0037|The contact has heard that the emperor even ordered the ceremony postponed until the item is found.|I hear he's even ordered the ceremony postponed until it's found.
DK4_MES_B295_R0040|Lil is incredulous and compares the emperor's behavior to a child's.|Is he serious?! He's acting like a child...
DK4_MES_B295_R0043|The contact asks her not to be so critical, pleads for the item to be brought here and needs only a one-day loan.|Come on, don't say that. Please, find it and bring it here. You only have to lend it to us for one day.
DK4_MES_B295_R0046|Rumor places the wristband somewhere in the New World, and the contact entrusts the task to her.|Rumor has it it's somewhere in the New World. I'm counting on you.
@296
DK4_MES_B296_R0018|Lil wonders where the Heavenly Wristband could be because the New World is vast.|Where could the Heavenly Wristband be? The New World's a big place...
DK4_MES_B296_R0023|Lil reminds herself to deliver the Heavenly Wristband to Istanbul's guild promptly.|I need to get this Heavenly Wristband to the guild in Istanbul right away.
DK4_MES_B296_R0039|The contact asks whether the Heavenly Wristband is still unfound.|Still haven't found the Heavenly Wristband?
@297
DK4_MES_B297_R0005|The contact thanks her for finding the item and asks her to wait just one day.|Oh, you found it? Thank you! Now, just wait one day.
DK4_MES_B297_R0013|The contact says the emperor was delighted, his own standing was saved and he will give a generous reward.|His Majesty was delighted! You really saved my reputation. I'll make sure you're well rewarded!
DK4_MES_B297_R0016|The system awards 25,000 gold coins.|Received 25,000 gold.
DK4_MES_B297_R0040|The system announces a small increase in Istanbul market share.|Your market share in Istanbul has increased slightly!
DK4_MES_B297_R0051|The grateful contact offers to answer any questions about this town.|If there's anything you want to know about this town, just ask.
DK4_MES_B297_R0054|Asked about ruins, the contact says he knows a particularly good site and offers to guide her.|Ruins? I know a good one. I'll show you the way.
@298
DK4_MES_B298_R0006|A messenger says Istanbul's guild was looking for the visitor.|The guild in Istanbul was looking for you.
'''

CONTEXTS = {
    '293': 'Map-gated mountain ascent; guide parts at the summit. Lil\'s confidence in a Proof clue is intuition. Fog prompts caution and a tree-collision gag. Waiting costs one day, clears fog and earns praise/teasing; hurrying separates crew members and reduces their number, without asserting deaths. Preserve all voice alternatives and distinct branch consequences.',
    '294': 'Rockfall blocks the normal route to ruins, possibly for ten or twenty years because it is rarely visited. Lil insists on climbing a dangerous cliff few locals attempt. Earlier credited R73 acknowledges her resolve and must remain as exact context without duplicate draft or credit. Guide agrees to meet here with a map, explains a hidden Christian settlement and his own incomplete route knowledge, and tentatively points to Mediterranean towns for a map.',
    '295': 'Guild wants Heavenly Wristband for the emperor\'s collection display to a visiting vassal king. Leadership power is reported lore; imperial grandeur is the contact\'s speculation. Lil mocks royal vanity and childish postponement. Only a one-day loan is requested; New World location is rumor. Do not invent a sale, confiscation or relationship to the emperor.',
    '296': 'Alternative reminders for the Heavenly Wristband job: vast New World search, delivery to Istanbul guild once acquired, or contact asking if found. Keep states separate without claiming acquisition from the reminders.',
    '297': 'Wristband is received on the agreed one-day loan. Contact reports emperor\'s pleasure and saved reputation, pays25,000 gold and grants a small Istanbul share increase; then offers information and a ruins guide. No permanent surrender, additional item reward or precise ruins identity is invented.',
    '298': 'A messenger relays Istanbul guild\'s search for the visitor, without inventing a reason, rank or new task.',
}


def main():
    out = ROOT / 'authored_B293_B298_v1.json'
    assert not out.exists()
    records = []
    active = None
    for line in TEXT.splitlines():
        if not line:
            continue
        if line.startswith('@'):
            active = line[1:]
            continue
        assert active in CONTEXTS
        records.append(line.split('|', 2))
    assert len(records) == 121
    save(out, dict(contexts=CONTEXTS, records=records, whole_clean_exchanges_read_before_drafting=True,
        current_English_not_consulted=True, source_name_item_title_andnative_consumer_bindings_pending=True, new_credit=0))


if __name__ == '__main__':
    main()
