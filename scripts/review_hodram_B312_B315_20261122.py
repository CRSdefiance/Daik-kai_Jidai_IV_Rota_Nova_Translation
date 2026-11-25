"""Review the map rumor, scorpion encounter, and incense-burner conversations."""
from scripts import review_hodram_B311_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, ROOT = previous.base, previous.ROOT
OUTPUT = ROOT / "B312_B315_contextual_v1.json"
GLYPHS = set()
CONTEXTS = {
    312: "A hostess tells the captain about the recently found map and a nearby kingdom's ruins. She does not know where to find the map.",
    313: "The party encounters scorpions in the desert. Several crew reactions depend on style and choice. Two retreat reports match exactly. The quiet escape can be interrupted by dropped gear.",
    314: "The hostess tells the captain about a celadon incense burner and then warns about nearby piracy.",
    315: "The hostess credits her better readings to the gift, offers a fortune as thanks, and directs the captain toward the ruins.",
}
DECISIONS = {
    312: """
6|Oh, FI! I meant to tell you something and it completely slipped my mind.|slipped my mind.|She recognizes the captain and remembers the news she had been meaning to share.
10|I heard someone found an ancient illustrated map the other day. It seems to show ruins of an old kingdom near town.|an ancient illustrated map;ruins of an old kingdom;near town.|Keep the recent discovery, map type, nearby kingdom ruins and her secondhand account.
13|||The captain shows interest and immediately asks where the map is now.
16|Sorry, I don't know where it is. Why not go look for it if you're interested?|I don't know where it is.;if you're interested?|She has no location and suggests that the interested captain look for it.
""",
    313: """
SC1_B313_STYLE_24_0|||This polite warning gives the direct consequence of traveling without a map.
SC1_B313_STYLE_24_40|Admiral, we'll get lost without a map.|without a map.|The measured voice makes the same prediction in a plain sentence.
SC1_B313_STYLE_24_72|||The casual crew member warns they will end up lost. The emphasis suits this voice.
SC1_B313_STYLE_24_108|||This crew member repeats the warning with a colloquial contraction.
SC1_B313_STYLE_24_148|||The rougher voice says they will get themselves lost if they press on without a map.
SC1_B313_STYLE_24_188|||The older voice states the danger of losing their way plainly.
SC1_B313_STYLE_24_226|||The youthful speaker calls out urgently about getting lost without a map.
SC1_B313_STYLE_24_268|Admiral, we're sure to lose our way without a map.|lose our way;without a map.|The formal speaker stresses the certainty of getting lost.
SC1_B313_STYLE_376_0|||The shared crew line notes how hot it really is in the desert.
SC1_B313_STYLE_376_18|||The casual voice draws out a complaint about the heat.
SC1_B313_STYLE_376_34|||The rougher voice complains about the heat in everyday language.
SC1_B313_STYLE_376_50|||The older voice remarks on the heat and invites agreement.
SC1_B313_STYLE_376_60|||The youthful voice groans in the heat before the captain responds.
65|||The captain accepts the desert heat as inevitable and orders the party to continue.
68|||The sailor stammers before the crew identifies the scorpions.
SC1_B313_STYLE_546_0|||The shared warning identifies a swarm and keeps the startled stammer.
SC1_B313_STYLE_546_28|Whoa! A swarm of scorpions!|A swarm of scorpions!|The casual speaker exclaims at the swarm. Natural word order keeps it immediate.
SC1_B313_STYLE_546_54|||The speaker gives a brief scream and stammers on the name of the animals.
SC1_B313_STYLE_546_80|A-Admiral! Look at all those scorpions!|all those scorpions!|The rough voice stammers at the sight and names the scorpions explicitly.
SC1_B313_STYLE_546_112|||The older speaker reacts to finding a whole swarm. Preserve the named threat.
SC1_B313_STYLE_546_140|||The youthful lookout shouts in surprise and names the scorpions.
92|||The captain tells everyone to calm down before deciding what to do.
96|||The sailor falters and asks what they should do. Keep the audible hesitation.
SC1_B313_CHOICE_782_0|||Fight selects direct action against the scorpions.
SC1_B313_CHOICE_782_1|||Drive them off chooses to disperse the scorpions without fighting.
SC1_B313_CHOICE_782_2|||Run selects the escape branch with the whispered departure.
115|||The captain takes responsibility and gives a brief sound of effort.
SC1_B313_STYLE_856_0|Look, they're running away! We can count on you, Admiral.|running away!;count on you, Admiral.|Two slots share a burst of relief and praise the admiral as dependable.
SC1_B313_STYLE_856_56|||The measured speaker sees the scorpions flee and congratulates Hodram.
SC1_B313_STYLE_856_88|||The casual speaker is relieved they ran and calls the admiral dependable.
SC1_B313_STYLE_856_136|Hey, they took off! We knew we could count on you, Admiral.|Hey, they took off!;count on you, Admiral.|The rough voice admires his reliability as the scorpions run. Remove the unsupported reference to another occasion.
SC1_B313_STYLE_856_182|||The older crew member adds a warm remark about being in good hands.
SC1_B313_STYLE_856_234|||The youthful voice is openly delighted that they ran and praises the admiral.
SC1_B313_STYLE_856_278|||The formal speaker notes that they ran, congratulates the admiral and calls him dependable.
139|||The captain says he will personally drive the scorpions off. The wording matches the choice.
SC1_B313_STYLE_1252_0|Look, they're running away! We can count on you, Admiral.|running away!;count on you, Admiral.|The same two slots recognize the retreat and praise the admiral on this branch.
SC1_B313_STYLE_1252_56|||This branch uses the same congratulations from the measured speaker.
SC1_B313_STYLE_1252_88|||The casual voice matches its report and praise on the other branch.
SC1_B313_STYLE_1252_136|Hey, they took off! We knew we could count on you, Admiral.|Hey, they took off!;count on you, Admiral.|Match the same rough voice and present success on both branches.
SC1_B313_STYLE_1252_182|||The older speaker expresses relief and confidence in the same cadence as before.
SC1_B313_STYLE_1252_234|||The youthful voice repeats its delight and praise after the scorpions flee.
SC1_B313_STYLE_1252_278|||The measured voice repeats that the admiral is dependable following the retreat.
162|||The captain cries out abruptly when injured.
SC1_B313_STYLE_1624_0|||The shared crew line calls directly to the admiral and asks if he is all right.
SC1_B313_STYLE_1624_28|||This casual voice asks the same urgent question in fewer words.
SC1_B313_STYLE_1624_50|||The rough voice asks if the admiral is all right without embellishment.
SC1_B313_STYLE_1624_74|||The youthful crew member urgently calls the title alone.
189|||The captain curses and explains that he let his guard down.
SC1_B313_STYLE_1756_0|||The measured voices urgently call for treatment.
SC1_B313_STYLE_1756_24|We've got to treat him, fast!|treat him, fast!|The casual and young variants both insist on immediate care.
SC1_B313_STYLE_1756_48|||This alarm adds a cry of dismay before the need for immediate care.
SC1_B313_STYLE_1756_78|||The rough voice uses a short, direct order to attend to the injury.
SC1_B313_STYLE_1756_100|||The older speaker says treatment is urgent. The brief sentence fits the scene.
SC1_B313_STYLE_1756_124|||The formal speaker calls for prompt care in a measured but urgent voice.
228|||Keep the given-name substitution, the injury and the exact day spent in place receiving treatment.
236|||The captain apologizes and says he is all right now. His short reply fits the return to the expedition.
242|||The captain orders a quiet withdrawal and tells everyone to avoid provoking the scorpions.
SC1_B313_STYLE_2118_0|||The shared crew line calls the group together and repeats the soft instruction to stay quiet.
SC1_B313_STYLE_2118_40|||The shared rougher delivery says they are moving and repeats the need for quiet.
SC1_B313_STYLE_2118_80|Come on, everyone. Nice and quiet now...|Nice and quiet now...|Keep one drawn-out whisper to convey the repeated instruction naturally.
SC1_B313_STYLE_2118_118|||This speaker makes the same quiet departure request in her own voice.
SC1_B313_STYLE_2118_158|||The older speaker announces the departure and repeats the quiet instruction.
SC1_B313_STYLE_2118_202|Come on, everybody. Shh... Nice and quiet...|Nice and quiet...|The youthful voice calls to everyone and softens into a whisper before they move.
275|||Keep the short sound of the gear landing before the sailor explains it.
279|Oops! Our gear fell!|Our gear fell!|The sailor recognizes what fell. The plain reply follows the sudden thud.
SC1_B313_STYLE_2472_0|||The shared phrase clearly signals alarm at the noise.
SC1_B313_STYLE_2472_16|||The short shared gasp is an immediate reaction to the dropped gear.
SC1_B313_STYLE_2472_24|||The rougher voice reacts with a compact warning before the injury.
SC1_B313_STYLE_2472_34|||The older and formal voices both react in dismay.
303|||The sailor cries out in pain before anyone asks about the injury.
SC1_B313_STYLE_2556_0|||The crew member stammers out a check and asks the sailor to hold on.
SC1_B313_STYLE_2556_34|||The measured voice urgently checks on the sailor and asks him to hold on.
SC1_B313_STYLE_2556_62|||Three slots share the stammer and encouragement to hang in there.
SC1_B313_STYLE_2556_92|||The rougher voice uses an abrupt direct address and then reassures the sailor.
SC1_B313_STYLE_2556_126|||The older voice stammers in alarm before asking the sailor to hold on.
SC1_B313_STYLE_2556_158|||The formal voice stammers before asking the sailor to stay with them.
331|||The captain orders the group to rush past the scorpions immediately.
336|||The notice reports an apparent injury to one sailor.
355|||The sailor observes they appear to have made it to the destination.
""",
    314: """
6|||The hostess greets the captain before asking about an item.
10|||Keep the approved Goryeo Incense Burner label, its celadon description and the uncertain location somewhere in East Asia.
14|They say it makes fortune-telling a lot more accurate. Oh, I'd love to try it just once...|a lot more accurate.;try it just once...|She describes a rumored improvement to her readings and her own wistful wish to try it.
30|||The captain gives a short listening response, leaving room for the next subject.
35|Oh, one more thing.|Oh, one more thing.|The hostess remembers another subject and gets the captain's attention.
39|||She warns about recent pirate activity around here and advises the captain to equip the crew properly.
43|||The captain reacts to the warning, thanks her and promises to be careful.
47|||The hostess gives a brief farewell after the warning.
""",
    315: """
6|||The hostess welcomes the captain back warmly before discussing the gift.
10|That incense burner you gave me has made my readings much more accurate. Let me tell your fortune as thanks.|That incense burner;much more accurate.;tell your fortune as thanks.|She credits the gift and offers a reading as thanks.
14|||The brief invitation to sit follows the offer to tell the captain's fortune.
18|||Her silence belongs to the reading itself.
22|||The captain waits for the reading without adding a spoken response.
26|||The hostess locates the ruins deep in the desert far inland and expresses her own confidence about what the captain seeks.
""",
}
review = checked_text(previous.review, {"len(records) == 80": "len(records) == 97"})
scope = previous.scope | globals()
exec(compile(review, __file__ + "::map-scorpions-and-fortune", "exec"), scope)
if __name__ == "__main__":
    scope["main"]()
