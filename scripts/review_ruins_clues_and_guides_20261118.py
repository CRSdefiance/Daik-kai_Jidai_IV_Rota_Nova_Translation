"""Review four ruin investigations, preserving their original choices and clues."""

from collections import defaultdict
from pathlib import Path
from types import FunctionType

from scripts import prepare_ruins_clues_and_guides_20261118 as current
from scripts import review_jungle_caves_20261118 as binder


base, parent = current.paired.base, current.parent
SOURCE = current.ROOT / "paired_source.json"
SOURCE_SHA = "c73738e6a021d2b1965905dd11f985bf2d6abe4779c4858a8eaf72c6c7f886b8"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/ruins_clues_and_guides_20261118_prose_v5.json")
HISTORY = (
    ("rafael_B301_B320_integrated_final_review_v1.json",),
    ("hodram_B281_B300_integrated_final_review_v1.json",),
    ("lil361_B283_B298_integrated_final_review_v1.json",),
    ("maria359_B253_B274_integrated_final_review_v1.json",),
)

# Keys follow first occurrence of each exact native word and Japanese body
# in the hash-bound packet. Every route variant retains its own references.
NOTES = {
    1: "Keep the proprietor's friendly greeting and the live first-name address.",
    2: "She has heard of no ruins near town. Keep the limit on her own knowledge.",
    3: "Rafael starts an excited inference and leaves the thought hanging.",
    4: "Keep his enthusiasm about being the first to find the ruins.",
    5: "Her reply punctures his optimism with the dense forest and numerous wild animals.",
    6: "She'll show the party the way inland if they insist. The map warning stands on its own.",
    7: "The speaker muses about what to call the tradition instead of claiming it is verified history.",
    8: "Keep the rumor linking command of the Indian Ocean to the tradition.",
    9: "The question echoes the rumor and then reaches the approved Proof of Conquest term.",
    10: "The companion is nearly sure this is the right interpretation.",
    11: "Rafael takes the clue as a direction to find the Indian Ocean Proof first.",
    12: "The earlier speaker recognizes the crew on their second visit.",
    13: "Keep the polite request to confirm the object as the one previously discussed.",
    14: "He looks before recognizing it. Keep the shift from uncertainty to surprise.",
    15: "Keep his confirmation and the original text of the first Veda.",
    16: "Keep his surprise that someone so young brought it to him.",
    17: "Keep the silent reaction between the surprise and the handover.",
    18: "The speaker decides to entrust the next object to the group.",
    19: "The party tentatively recognizes an old coin and asks what it is.",
    20: "Keep the speaker's final instruction to work out the rest on their own.",
    21: "Rafael remains puzzled by the dismissal.",
    22: "The guide asks for a map and won't continue without one, even for these visitors.",
    23: "The guide recognizes the group came back prepared and can now proceed.",
    24: "The straightforward crew warning makes a map a firm requirement.",
    25: "The measured voice explains why they can't move farther.",
    26: "The familiar voice also connects the missing map to their inability to continue.",
    27: "The companion says going on without a map is impossible.",
    28: "The rough voice interrupts first and then says why they're stopping.",
    29: "The older voice firmly states that they're going no farther without a map.",
    30: "The child calls out to the admiral and says they need a map.",
    31: "The formal companion links the map requirement to this next stretch.",
    32: "Keep the relief on reaching the top after a strenuous climb.",
    33: "The guide goes no farther and offers a brief farewell.",
    34: "Claudio thanks the older guide familiarly and sets off. No title or relationship is needed.",
    35: "Rafael finds the dim forest unsettling.",
    36: "The companion admits disliking places like this in a familiar voice.",
    37: "Claudio speculates that a hidden village may still tell old stories.",
    38: "Rafael hopes the village may hold a clue to the Proof of Conquest.",
    39: "He sees the swift river and asks what to do. The two choices follow.",
    40: "The short menu caption directs the party to try crossing carefully.",
    41: "The other menu caption directs the party upstream before the bridge is mentioned.",
    42: "Keep the sudden cry as the current starts sweeping the speaker away.",
    43: "The first warning asks the admiral to stop and explains that crossing on foot is too dangerous.",
    44: "This warning notices the current first, then urgently calls to the admiral.",
    45: "The familiar voice warns against wading through a current this strong.",
    46: "The speaker fears the current will carry them away before they reach the other side.",
    47: "Keep the rough refusal and the fact that attempting the crossing on foot is the problem.",
    48: "The older companion urgently warns the admiral against crossing on foot.",
    49: "The child calls for the admiral and fears that they'll be swept away.",
    50: "The formal companion is equally emphatic that the current makes the foot crossing impossible.",
    51: "Rafael tells everyone to hold hands and work together against the current.",
    52: "Keep the immediate reply to Rafael's instruction.",
    53: "The companion encourages the others to keep going because they're nearly across.",
    54: "The system reports fatigue and a possible loss from the group without specifying casualties.",
    55: "Claudio notices a log bridge on the map and asks about taking the longer route.",
    56: "Rafael accepts because he sees no other practical option.",
    57: "The group spots what appears to be the bridge on the map.",
    58: "Claudio confirms the bridge while marveling at where it was built.",
    59: "The more cautious companion hesitates at the prospect of crossing there.",
    60: "The rough reply pushes the reluctant companion to cross quickly.",
    61: "The stammer and objection fit the physical push at the bridge.",
    62: "Rafael recognizes the arrival after both routes lead on.",
    63: "Hodram's short observation sets up the thought that the dense forest hid the place.",
    64: "Keep the link between the forest and why the place has gone unnoticed.",
    65: "The companion openly wants to be out of the forest quickly.",
    66: "Keep the companion's conjecture about Christians predating Islamic rule and possible Byzantine descent.",
    67: "Hodram recognizes how far back the story goes and hopes for a clue to a Proof of Conquest.",
    68: "The startled question identifies bones without asserting who's responsible.",
    69: "The companion infers an earlier visitor died here. The explanation remains speculative.",
    70: "The cautious suggestion leads straight to the search decision.",
    71: "Keep this straightforward affirmative choice in its original slot.",
    72: "Keep the refusal in its original slot.",
    73: "The companion accepts and notes that caution is worthwhile.",
    74: "Hodram notices smoke, then has trouble breathing. Keep the broken delivery.",
    75: "The companion warns Hodram by his original given-name substitution and urges a quick exit.",
    76: "Hodram asks whether everyone is accounted for.",
    77: "Keep the report about the group's safety.",
    78: "Reassurance gives way to sudden concern about the admiral.",
    79: "Hodram struggles to say he is all right and asks what the smoke was.",
    80: "The companion knows only a report about harmful smoke and is surprised to encounter it here.",
    81: "Keep Hodram's faltering acknowledgment.",
    82: "The urgent call tells everyone to hurry through because the admiral is in danger.",
    83: "Keep the qualified system report that the sailors are confused.",
    84: "The companion advises against lingering in a suspicious place and urges the party on.",
    85: "The speaker regrets losing the chance to learn about the bones.",
    86: "Hodram tentatively recognizes the place after the party moves on.",
    87: "Keep the shopkeeper's cheerful welcome before she confides the rumor.",
    88: "She looks him over, compliments him and offers a tip. Keep the flirtation light.",
    89: "She asks about a nearby hidden Christian village.",
    90: "Hodram answers briefly and plainly that he hasn't heard of it.",
    91: "Keep the rock-cut homes and the shopkeeper's explicit distinction between rumor and fact.",
    92: "Hodram's short, unfinished reaction comes when he sees the obstruction.",
    93: "The companion thinks it might have been a rockfall and says there's no way through.",
    94: "Hodram reluctantly proposes turning back.",
    95: "Keep Charles's pause before Hodram calls to him.",
    96: "Hodram prompts Charles and says the group is turning back.",
    97: "Keep Charles's sudden proposal and its surprise value in the game scene.",
    98: "Hodram echoes Charles's proposal in disbelief.",
    99: "Keep Charles's aim of clearing the rock from the obstructed path.",
    100: "Keep Hodram's skepticism about the scale of the fictional plan.",
    101: "Hodram doubts the required amount can be obtained all at once.",
    102: "Keep Charles's confidence that the party can make what it needs.",
    103: "Hodram echoes the proposal and questions Charles's ability.",
    104: "Keep Charles's reference to his research and the existing quest condition.",
    105: "The companion thinks the required trade good was available in town.",
    106: "Keep the trade house as the source and the requirement to bring the goods here.",
    107: "Hodram agrees to go buy the requested trade good.",
    108: "Keep Hodram's repeated regret in the variants where Charles can't take part.",
    109: "Keep the short reminder of the required purchase.",
    110: "Charles says the delivery is nowhere near sufficient.",
    111: "Keep this shorter response for the separate insufficient-stock condition.",
    112: "Charles judges this delivery sufficient before proceeding.",
    113: "Hodram asks what they need to do next.",
    114: "Keep the in-game objective and the intended use of the next trade good.",
    115: "Hodram repeats the trade good as he considers it.",
    116: "The companion says there's no local supply and tells the party to look elsewhere.",
    117: "Keep Hodram's brief reminder of the purchase.",
    118: "Charles says there should be enough of the requested stock.",
    119: "Keep the unfinished transition to the last requirement.",
    120: "Hodram reacts with disbelief that there is another step.",
    121: "Keep Charles's announcement of the final in-game requirement.",
    122: "Hodram echoes the name, surprised.",
    123: "The companion says one town on the Indian Ocean should carry the trade good.",
    124: "Hodram complains quietly about the distance.",
    125: "Keep the short quest reminder.",
    126: "Charles says the short delivery is nowhere near sufficient.",
    127: "Charles recognizes they probably have enough and can proceed.",
    128: "Keep Charles's brief announcement that he's done.",
    129: "Keep the instruction to take shelter in town before the scripted event.",
    130: "Keep the original countdown values and excited delivery.",
    131: "The unfamiliar speaker addresses Lil courteously and asks about the ancient kingdom's temple.",
    132: "Keep Lil's abrupt surprise before she learns who is speaking.",
    133: "Keep the admonishing first-name address and identify the visitor as an elder from a nearby village.",
    134: "The companion apologizes and presses Lil to apologize too.",
    135: "Keep the elder's laugh and his easy forgiveness.",
    136: "The elder thinks Lil can find the temple, but trails off before telling her the condition.",
    137: "Lil repeats his unfinished 'but' to invite him to explain.",
    138: "The elder waves the subject away and laughs again.",
    139: "Keep Lil's short puzzled reaction after the elder leaves her without an explanation.",
    140: "Lil blurts out her frustration at failing to solve the Angkor riddle.",
    141: "Keep the same quoted clue as the actual inscription, followed by the question about what it means.",
    142: "Lil returns to the first part of the clue, which pairs gold with the sun and silver with the moon.",
    143: "The companion remembers that the voice has yet to see a star's light.",
    144: "Lil asks whether the star could mean some metal more precious than gold or silver.",
    145: "The companion reports what Alchemy Book may describe and addresses the admiral.",
    146: "Keep Lil's quick, excited reaction before the companion continues.",
    147: "Keep the hearsay about the author traveling to the New World.",
    148: "Lil seizes on the element's obscurity as the promising part of the clue.",
    149: "The companion makes a tentative connection to platinum, which he has sought for years.",
    150: "Lil jumps at the name despite not knowing the metal. Keep her excitement without doubling the punctuation.",
    151: "Keep the reference to the known book and leave the thought unfinished.",
    152: "Lil recognizes the reference and decides to load the platinum aboard.",
    153: "Keep the tentative lead that platinum is mined in southern Africa.",
    154: "The alternate conversation also starts with Lil's frustration.",
    155: "Keep the alternate recitation word for word with the original clue.",
    156: "The companion checks the correspondence between sun and gold and moon and silver.",
    157: "The short answer confirms what the voice actually said.",
    158: "Keep the brief pivot from the known two metals to the star.",
    159: "The reply says that answering this part should solve the riddle.",
    160: "The speaker reasons from the gold and silver to an unknown, unusually rare metal.",
    161: "The next speaker proposes platinum as a possibility.",
    162: "Lil is unfamiliar with the name and asks plainly.",
    163: "Keep the uncertainty about the local source and the in-game book condition.",
    164: "Keep the quick question about which book is needed.",
    165: "The speaker vaguely remembers an alchemy book and reports the author's earlier New World voyage.",
    166: "Keep Lil's brief reaction to the destination.",
    167: "Lil recognizes platinum from the alchemy book and thinks it must be the answer.",
    168: "The revised plan is to carry platinum aboard for the ruins.",
    169: "Keep the seller's local claim and invitation to purchase the metal.",
    170: "Keep the inscription's imperative and its reference to a new star's pure glow.",
    171: "Lil echoes the new star and wonders what to bring.",
    172: "Keep the work chant as a sound rather than an explanation.",
    173: "Lil has brought platinum and asks whether the inscription meant this.",
    174: "Keep the wordless surprise before the voice answers.",
    175: "The voice praises the one who brought the star's radiance. Its speech is ceremonial.",
    176: "Keep the order of the figurative storm and the request for peaceful sleep.",
    177: "Lil notices the coin is quite old before anyone explains it.",
    178: "Keep the open question about the voice's words.",
    179: "The companion has no explanation but thinks the voice sounded satisfied.",
    180: "The coin's use is still unknown, but the speaker is confident it will be useful.",
    181: "Lil is relieved to have climbed to the top.",
    182: "She expects a clue to the Proof of Conquest without claiming she's found it.",
    183: "The companion asks why she thinks that.",
    184: "Lil repeats that it's only a feeling. Keep the refusal to manufacture evidence.",
    185: "Keep the rough advice that a little fear is appropriate here.",
    186: "The companion notices visibility falling before the next speaker names the fog.",
    187: "The admiral receives the direct warning about fog and a call for caution.",
    188: "The speaker cautiously identifies the fog and proposes proceeding carefully.",
    189: "Keep the familiar surprise at sudden thick fog and poor visibility.",
    190: "The speaker can no longer tell where the others are.",
    191: "The rough voice swears after losing sight of the surroundings.",
    192: "The older voice tells the admiral to watch her footing.",
    193: "Keep the child's open astonishment and inability to see anything.",
    194: "The formal speaker's short recognition leaves the alarm understated.",
    195: "The companion checks on Lil by her given-name control after visibility suddenly collapses.",
    196: "Lil mistakes a tree for someone in her way. Preserve the realization and the cry of pain.",
    197: "Keep the plain request for the admiral's decision.",
    198: "Keep the familiar 'What now?' variation.",
    199: "The rough voice asks the admiral for a plan.",
    200: "The older voice phrases the same request more deliberately.",
    201: "The child calls to the admiral and asks what they're to do.",
    202: "The formal companion politely asks for the admiral's decision.",
    203: "The familiar question addresses Lil by the runtime first name.",
    204: "Lil pauses before the two options appear.",
    205: "Keep the choice to wait without promising that the fog will clear.",
    206: "Keep the alternative choice to hurry out of the area.",
    207: "This response checks whether they'll really wait here.",
    208: "This version leaves a hesitant pause while confirming the wait.",
    209: "Keep the familiar echo of the decision.",
    210: "The speaker asks whether Lil meant that they should wait in place.",
    211: "Keep the rough companion's brief incredulous question.",
    212: "The older companion confirms the decision to wait.",
    213: "The child protests the wait because he's already hungry.",
    214: "The formal companion acknowledges the decision and agrees to wait.",
    215: "Keep the incredulous reply to waiting in the fog.",
    216: "Lil expects the party to get separated if it moves and reassures them that the fog should clear.",
    217: "The companion understands and approves Lil's decision.",
    218: "The measured variant acknowledges that it was a sound judgment.",
    219: "The familiar voice realizes the point and praises Lil directly.",
    220: "This version also praises the admiral after an informal realization.",
    221: "Keep the rough speaker's short acknowledgment and admiring reply.",
    222: "The older companion formally recognizes Lil's reasoning.",
    223: "Keep the child's simple praise of the admiral's intelligence.",
    224: "The formal companion credits Lil's reasoning and judgment.",
    225: "Keep Lil's short, self-satisfied agreement.",
    226: "Keep the backhanded 'for you' and live name in the close companion's joke.",
    227: "Lil repeats 'good call' to turn the joke back on the companion.",
    228: "Keep the original system notice that one day elapses.",
    229: "Lil celebrates the fog beginning to clear and urges everyone onward.",
    230: "The first response to moving questions whether the admiral really means it.",
    231: "The speaker doubts that pushing forward is safe.",
    232: "The speaker reacts to entering the fog and then wonders how they'll fare.",
    233: "The rough voice asks bluntly if Lil is serious.",
    234: "The older speaker takes a moment to confirm they're really going.",
    235: "Keep the child's stammer and concern about following.",
    236: "The formal companion asks about the party's safety and trails off.",
    237: "Keep the familiar objection and the question about proceeding safely.",
    238: "Lil brushes off the concern and tells the party to go.",
    239: "Keep the stammer as the companion asks Lil to wait.",
    240: "Lil checks whether everybody is still keeping up.",
    241: "This measured report says some people appear to have become separated.",
    242: "This alternate measured report starts with an uneasy pause.",
    243: "The speaker associates the apparent separations with the lack of visibility.",
    244: "The speaker notices they're a few people short and tentatively infers what happened.",
    245: "The rough voice recognizes the missing companions and says little could be done in the fog.",
    246: "The older voice cautiously concludes some people became separated.",
    247: "The child notices people are missing and guesses the fog separated them.",
    248: "The formal companion thinks a few people were separated in the fog.",
    249: "Keep the lack of visibility and the uncertainty about the people separated.",
    250: "The system reports a small reduction in crew size after the rushed route.",
    251: "Lil sees the destination and asks whether this is the place.",
    252: "The companion appears to confirm arrival.",
    253: "The guildmaster addresses Maria familiarly and asks about shark fin in light of her background.",
    254: "Maria answers attentively, unsure why he is asking.",
    255: "Malacca's lord wants to try a rare delicacy. Keep the request for a possible supply.",
    256: "Maria knows it as a court dish and has never tried it herself.",
    257: "The guildmaster admits this is about what he expected.",
    258: "Maria offers to buy some if she comes across it, without a guarantee.",
    259: "Keep the guildmaster's quick, grateful reply.",
    260: "He asks for an unfamiliar delicacy as the fallback if she can't get shark fin.",
    261: "Maria sees how hard it will be to surprise someone who's tried everything.",
    262: "The guildmaster starts to complain about the gourmand and catches himself.",
    263: "Maria says she found what he asked for and hands over the shark fin.",
    264: "The guildmaster is surprised that it's genuine.",
    265: "Maria expects it may be easier to get in the future, without giving a reason.",
    266: "Keep the familiar praise and promise of a generous payment.",
    267: "The exact reward is 50,000 gold coins.",
    268: "The system reports a small gain in the player's Malacca share on both handover paths.",
    269: "He offers an interesting story as an additional thank-you.",
    270: "The report places the apparently intact ruins deep inland in the jungle. This remains hearsay.",
    271: "Maria finds the claim about the ancient kingdom hard to believe.",
    272: "The speaker makes clear no one has found the ruins and thinks Maria might.",
    273: "The guildmaster greets Maria familiarly and asks about the shark fin.",
    274: "Maria says she couldn't find it and offers an unusual substitute she thinks worth trying.",
    275: "The question gives way to a delighted stammer when the substitute tastes good.",
    276: "Keep Maria's quick, knowing reply.",
    277: "The guildmaster is confident serving the substitute and thanks Maria with a reward.",
    278: "The substitute path awards 30,000 gold coins.",
    279: "Keep Maria's reserved disbelief in the alternate version.",
    280: "The first companion calls the admiral over urgently.",
    281: "The more formal version politely asks the admiral to come over.",
    282: "Keep the familiar companion's direct call to take a look.",
    283: "The rough voice calls Maria over with less ceremony.",
    284: "The older companion invites the admiral to come see what they found.",
    285: "The child's call to the admiral stays direct and excited.",
    286: "The formal companion respectfully asks the admiral to come closer.",
    287: "Maria asks what they found before someone tries digging.",
    288: "The companion volunteers to dig with a familiarly clipped delivery.",
    289: "Maria cautiously identifies the result as a very old coin.",
    290: "Keep Maria's short readiness check addressed to Xien.",
    291: "Xien confirms that the preparations are complete.",
    292: "The companion proposes moving forward cautiously.",
    293: "Keep the surprised recognition of the apparent dead end.",
    294: "Keep the brief hesitation before the two choices appear.",
    295: "The first caption directs the party to push past the obstacle.",
    296: "The second caption directs the party to look for a way through.",
    297: "The first companion reads from the map and thinks they're meant to go through here.",
    298: "The next speaker takes the map as a direction to keep going that way.",
    299: "The familiar speaker says the map points through this very spot.",
    300: "The speaker voices the same reading tentatively.",
    301: "The rough companion reads it as a direction to press directly through.",
    302: "The older voice reads the map and thinks they're supposed to get past the apparent barrier.",
    303: "The child says the map points through here without identifying a structure to cross.",
    304: "The formal companion reads the route aloud and keeps the original small pause.",
    305: "Maria tells everyone to go forward together and avoid getting separated.",
    306: "Keep uncertainty in the notice that some sailors appear to have become separated.",
    307: "Maria spots a path and voices her surprise.",
    308: "The companion credits Maria for seeing the path hidden by trees and proposes continuing.",
    309: "Maria recognizes the destination and admires the view.",
}

# The same wording can serve a repeated source line, with overrides where a
# route already has a natural version. Historical release text stays intact.
EDITS = {}


def revise(index, routes, english):
    for route in routes:
        assert (index, route) not in EDITS
        EDITS[index, route] = english


revise(1, (0, 2), "Oh, FI! Good to see you.")
revise(10, (0,), "Yes. That sounds right.")
revise(11, (0,), "So we've got to find the Indian Ocean Proof first!")
revise(18, (0,), "Well, then. I'll leave this in your care.")
revise(22, (2, 3), "Did you bring a map? Sorry, but even for you, I can't go any farther without one.")
revise(26, (1, 3), "Admiral, we need a map to get any farther.")
revise(28, (1,), "Hold on. We can't go any farther without a map.")
revise(29, (1, 3), "Admiral, we're going no farther without a map.")
revise(36, (0,), "Ugh, I don't like places like this.")
revise(47, (0,), "Forget it, Admiral! You can't wade across a current that fast!")
revise(51, (0,), "Hold hands, everyone! Stick together! Don't get swept away!")
revise(54, (0,), "The crew is tired. Some sailors seem to have become separated.")
revise(59, (0,), "We really have to cross here...?")
revise(64, (1,), "That must be why it's gone unnoticed all this time.")
revise(65, (1,), "The sooner we're out of this forest, the better.")
revise(66, (1,), "Christians who lived here before Islamic rule... Could they be descended from the Byzantines?")
revise(69, (1,), "Someone may have come in here like we did. It looks like they never made it out...")
revise(73, (1,), "Understood. Can't be too careful.")
revise(76, (1,), "Everyone here?")
revise(80, (1,), "It's harmful to breathe. I'd heard rumors about it. I never thought I'd see it here...")
revise(84, (1,), "Hmm... We shouldn't linger anywhere that feels this suspicious. Let's press on.")
revise(86, (1,), "This looks like the place.")
revise(87, (1,), "Oh, welcome!")
revise(88, (1,), "You're quite handsome up close. Here, I'll let you in on something.")
revise(90, (1,), "No, I haven't.")
revise(93, (1,), "Could've been a rockfall. There's no way through like this.")
revise(94, (1,), "I suppose we'll have to turn back.")
revise(105, (1,), "I think they sell sulfur in town.")
revise(116, (1,), "No one in town sells timber. We'll have to buy it somewhere else.")
revise(120, (1,), "There's more?")
revise(124, (1,), "That's quite a way...")
revise(136, (2,), "I believe you'll find it. But...")
revise(140, (2,), "I give up. I can't make any sense of that riddle at Angkor!")
revise(144, (2,), "So it isn't gold or silver... Could the star be an even more precious metal?")
revise(148, (2,), "No one's ever seen it? Then that must be the one!")
revise(150, (2,), "Platinum?! I don't know what that is, but it sounds right!")
revise(152, (2,), "Oh, that! Then let's take some platinum with us!")
revise(159, (2,), "The star's the mystery. Figure that out and we'll have our answer...")
revise(160, (2,), "It has gold and silver but has never known a star's light. Could it mean a really rare metal?")
revise(167, (2,), "Platinum?! Oh, from the Alchemy Book! That must be it!")
revise(176, (2,), "With your wisdom, raise a storm upon the sea! Then let me sleep in peace!")
revise(180, (2,), "Right. I'm sure this coin will come in handy someday.")
revise(184, (2,), "Call it a hunch. It just feels right.")
revise(185, (2,), "Let's be careful. In a place like this, it pays to be a little scared.")
revise(188, (2,), "Looks like fog. Let's watch our step.")
revise(190, (2,), "This fog is thick! I can't tell where anyone is.")
revise(195, (2,), "The fog rolled in so fast. I can hardly see a thing. FI, are you okay?")
revise(216, (2,), "We can't go on in this fog. We'd get separated for sure. Don't worry, it'll clear!")
revise(220, (2,), "Oh, I see! Good idea, Admiral!")
revise(224, (2,), "Ah, I see your reasoning. Well judged, Admiral.")
revise(227, (2,), "I always make good calls!")
revise(233, (2,), "Hold on. Are you serious?")
revise(247, (2,), "Um... We're missing some people. They must've lost us in the fog...")
revise(250, (2,), "Your crew is down a few sailors.")
revise(256, (3,), "That may be hard to find. Even in China it's the sort of thing they serve at the palace. I've never tried it myself.")
revise(260, (3,), "If you can't get any, show us a delicacy we've never seen before.")
revise(262, (3,), "Yeah. That man's taste for fine food... Ah, I'd better hold my tongue. I'm counting on you.")
revise(263, (3,), "I found it. Here you are. Shark fin.")
revise(264, (3,), "Really? It's the real thing!")
revise(265, (3,), "It should be a little easier to get from now on.")
revise(266, (3,), "You really came through! I'll pay you well for this!")
revise(267, (3,), "Received 50,000 gold coins.")
revise(268, (3,), "Your Malacca share rose slightly!")
revise(269, (3,), "As a thank-you, let me tell you something I heard.")
revise(275, (3,), "What's this? ...Th-this is delicious!")
revise(277, (3,), "I'd be proud to serve this! You really came through. Here, take your reward!")
revise(278, (3,), "Received 30,000 gold coins.")
revise(295, (3,), "Push through")
revise(296, (3,), "Look around")
revise(299, (3,), "The map says to go through right here...")
revise(303, (3,), "Hey, it looks like the map says we have to go through here.")
revise(305, (3,), "Let's go, then. Everyone, stay together!")
revise(306, (3,), "Some sailors seem to be missing.")

PHRASES = (
    "Good to see you.", "Indian Ocean Proof", "I'll leave this in your care.", "Did you bring a map?",
    "I'd like to help,", "without one.", "to get any farther.", "without a map.",
    "you can't wade across", "a current that fast!", "even for you", "go any farther without one.",
    "Hold hands, everyone!", "Stick together!", "Don't get swept away!", "have become separated.",
    "We really have to cross here", "gone unnoticed", "get out of this forest",
    "before Islamic rule...", "descended from the Byzantines?",
    "never made it out...", "Can't be too careful.", "It's harmful to breathe.",
    "I'd heard rumors", "Let's press on.", "quite handsome up close.",
    "There's no way through", "have to turn back.", "somewhere else.",
    "that riddle at Angkor!", "an even more precious metal?", "No one's ever seen it?",
    "Then that must be the one!", "it sounds right!", "take some platinum with us!",
    "Figure that out", "we'll have our answer...", "a star's light.", "Could it mean a really rare metal?",
    "Alchemy Book!", "raise a storm upon the sea!", "Then let me sleep in peace!",
    "come in handy someday.", "Call it a hunch.", "it pays to be a little scared.",
    "Let's watch our step.", "I can't tell where anyone is.", "FI, are you okay?",
    "We'd get separated for sure.", "Don't worry, it'll clear!", "Good idea, Admiral!", "Well judged, Admiral.",
    "make good calls!", "Are you serious?", "lost us in the fog...", "down a few sailors.",
    "at the palace.", "I've never tried it myself.", "a delicacy", "never seen before.",
    "Even in China", "I'd better hold my tongue.", "I'm counting on you.", "Here you are.",
    "It's the real thing!", "a little easier",
    "I'll pay you well for this!", "gold coins.", "Your Malacca share",
    "let me tell you something I heard.", "Th-this is delicious!", "I'd be proud to serve this!",
    "Here, take your reward!", "the map says", "right here...", "we have to go through here.",
    "Everyone, stay together!", "sailors seem to be missing.",
)


def main():
    assert base.digest(SOURCE) == SOURCE_SHA
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["complete_source_current_binding"] and len(packet["groups"]) == 20
    assert packet["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    history_paths = [[Path("translations") / filename for filename in names] for names in HISTORY]
    historical = []
    for paths in history_paths:
        historical.append({key: (path, row) for path in paths
                           for key, row in binder.binder.index_history(path).items()})
    hashes = {path: base.digest(path) for paths in history_paths for path in paths}
    pairs = defaultdict(list)
    for group in packet["groups"]:
        for row in group["records"]:
            pairs[row["native_command_word"], row["Japanese"]].append((group, row))
    assert list(NOTES) == list(range(1, len(pairs) + 1))
    review = FunctionType(binder.review_one.__code__, vars(binder) | {
        "NOTES": tuple(NOTES.values()), "EDITS": EDITS, "PHRASES": PHRASES,
    })
    records, revised = [], set()
    for pos, variants in enumerate(pairs.values(), 1):
        for group, row in variants:
            route, block = group["route"], group["block"]
            path, prior = historical[route][block, row["source_offset"]]
            item = review(row, group, prior, pos, path, hashes[path])
            if item["decision"] == "revision":
                revised.add((pos, route))
            records.append(item)
    assert revised == EDITS.keys(), (EDITS.keys() - revised, revised - EDITS.keys())
    records.sort(key=lambda row: (row["route"], row["block"], row["source_reference"]["offset"]))
    assert len(records) == len({(r["file_path"], r["id"]) for r in records}) == 350
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(SOURCE), source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], clean_input_sha256=release["clean_input_sha256"],
        formatting_and_registration_pending=True, additional_review_credit=0, records=records))
    print(binder.binder.Counter((r["kind"], r["decision"]) for r in records), flush=True)


if __name__ == "__main__":
    main()
