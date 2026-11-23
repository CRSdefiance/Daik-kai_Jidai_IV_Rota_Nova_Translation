"""Review the cliff, cave, crossing and monk exchanges against their clean source."""

from inspect import getsource

from scripts import prepare_caves_offshore_monk_20261118 as paired
from scripts import review_desert_censer_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, parent = paired.paired.base, paired.parent
SOURCE = paired.ROOT / "paired_source.json"
SOURCE_SHA = "7555507cf6578aeb13bdf5235700f239b8dccef1a25faa36327f5b09aa848e74"
FOLDER = precedent.FOLDER
DECISIONS = FOLDER / "caves_offshore_monk_decisions_v1.txt"
OUTPUT = FOLDER / "caves_offshore_monk_20261118_prose_v4.json"
HISTORY = (*precedent.HISTORY[:2], ("lil261_B323_B335_integrated_final_review_v1.json",),
           ("maria315_B286_B302_integrated_final_review_v1.json",))
WRAP_ONLY = {
    (0, 2): "Preserve the direct warning and vocative. Keep 'without a map' together.",
    (0, 18): "Preserve the cliff-edge warning and keep 'edge of a cliff' together.",
    (0, 80): "Keep the suggestion to go this way together.",
    (0, 96): "Keep 'a jungle like this' together in the elder's caution.",
    (0, 113): "Keep the captain's question about where they emerged on one line.",
    (0, 119): "Keep 'near the ruins' together in this recognition.",
    (0, 136): "Keep 'through the jungle' together in the crew member's relief.",
    (1, 97): "Keep the emphatic warning about going without even a map together.",
    (2, 117): "Keep 'near the ruins' together during the hesitant answer.",
    (2, 131): "Keep 'through the jungle' together in the crew member's relief.",
    (2, 171): "Use the available width for the question about the village far north.",
}
WRAP_PHRASES = {
    18: ("edge of a cliff.",),
    80: ("go this way!",),
    96: ("a jungle like this.",),
    97: ("a jungle like this", "without even a map!",),
    113: ("Where are we now?",),
    145: ("the map to the ruins.",),
    152: ("way out here.",),
    159: ("Only your party is eligible to go.", "where the ruins are."),
    193: ("From the Castor Company?",),
    205: ("W-we have to",),
    221: ("I hear pirates are running wild",),
    226: ("the dark now...",),
}
FINAL_WORDING = {
    (0, 147): "To think an ancient city stood here...",
    **{(route, 159): "Only your party is eligible to go. Please don't tell the sailors where the ruins are."
       for route in (0, 1, 3)},
    **{(route, 175): "I hear he was a very good man. I hope he's loved where he went to preach."
       for route in range(4)},
    (1, 193): "Rafael? From the Castor Company? What are you doing here?",
    (1, 196): "So they asked you, too. Anyone who looks strong enough, was it?",
    (2, 211): "Ugh! We're pushing through! Everyone, run for the exit!",
    (3, 221): "I hear pirates are running wild around here lately. You'd better make sure you're well equipped.",
    (3, 226): "My eyes are used to the dark now... Shall we keep going?",
}
NOTES = {
    6: "Keep the older crew member's blunt certainty about heading out without a map.",
    17: "Keep the hesitant reaction to discovering where the party has ended up.",
    23: "Keep the familiar scolding and the given-name substitution. The source asks how they ended up here.",
    24: "Rafael is sure he followed the map, so the cliff is a surprise.",
    25: "The menu offers the apparent leap that provokes concern before Rafael reveals the joke.",
    26: "This option takes the detour around the cliff and costs a day.",
    28: "The worried crew member voices disbelief at Rafael's suggestion.",
    32: "A rough, direct objection suits this crew member.",
    33: "The elder admonishes Rafael for the suggestion before the next speaker imagines flying.",
    34: "The younger speaker takes the proposed leap literally and jokes about wanting to fly.",
    36: "Rafael admits he was joking, then directs the crew to climb down.",
    37: "Retain the companion's skeptical aside after Rafael claims it was a joke.",
    41: "The climb results in an apparent injury and increasing crew fatigue. This is a speakerless notice.",
    43: "Retain exactly one elapsed day in all routes and associated outcomes.",
    48: "Keep the speaker uncertain when pointing out what has come into view.",
    56: "This first fog choice continues before the dead end.",
    57: "This alternative waits until the fog clears and costs a day.",
    65: "This second decision comes after the dead end. The captain presses on despite it.",
    66: "This option looks for a way through the obstruction.",
    72: "The elder protests that the order is unreasonable and then agrees to try.",
    74: "Keep the crew's apparent fatigue as a system observation.",
    89: "This speaker backs the safer option without guaranteeing safety.",
    90: "The first timed silence marks a wait in the fog. Preserve the established ellipsis length.",
    91: "The longer timed silence follows the shorter hold while the party waits.",
    92: "This crew member emphasizes the danger of going into the jungle without knowing the way.",
    94: "Keep the speaker's practical warning about proceeding without direction.",
    101: "Preserve the companion's enthusiasm before the heat or cave reaction.",
    110: "This menu decision means proceeding by touch, before being able to see.",
    111: "The other choice provides light and reveals the bats.",
    112: "Rafael chooses to stay in the dark because suddenly making a light might be risky.",
    114: "The lookout hesitates, then gives a tentative location near the ruins.",
    115: "The more reserved voice describes the location as probable.",
    116: "Keep the crew member's uncertainty as they answer the question about where they came out.",
    120: "The youngest voice is briefly disoriented, then excited by the lucky result.",
    126: "The crew member is shocked by the unusual number of bats.",
    128: "The elder specifically says there are too many bats for the group to get through.",
    129: "The young voice recoils from the bats in a short, instinctive outburst.",
    131: "Keep the direct address in the crew member's relief after clearing the jungle.",
    135: "The rougher crew voice celebrates the escape from the jungle and addresses the admiral.",
    145: "The guide asks the group to obtain the map as a prerequisite to the search.",
    147: "Preserve the speaker's wonder about a city having stood in this unlikely spot.",
    152: "The younger speaker uses 'town' here. Other companions call it an ancient city.",
    154: "The guide says the map indicates the ruins may be off the island. Preserve the uncertainty.",
    158: "The guide already has a small boat arranged and plans to use it for the crossing.",
    159: "Keep the whole party's exclusive eligibility and the guide's request for secrecy from the sailors.",
    160: "First confirm arrival by boat, then change to overland travel.",
    171: "The contact asks about a particular village far north in the New World.",
    172: "The contact relays a customer's account. Keep the monk's local origin, reputation, travel and religious purpose.",
    173: "The monk reportedly disappeared after finding the village. The contact wonders what happened.",
    175: "Keep the secondhand account of a virtuous man and the contact's hope that the people he visited are fond of him.",
    176: "The contact makes a casual request to ask about the monk's fate on a future trip north.",
    177: "Hodram notices the humidity and worries about the party becoming exhausted.",
    181: "The warning breaks off as one of the group is in danger. The notice later reports the injury.",
    182: "The speaker blurts out Indian python before qualifying the identification.",
    184: "The speakerless notice reports an apparent injury. The Japanese noun can describe the crew collectively.",
    186: "The older crew member goes from disorientation to recognizing that the ruins are probably nearby.",
    189: "Hodram dismisses the bats and orders the party to continue.",
    193: "This is the recognition branch. Keep Rafael and the Castor Company in the source and retain the surprised question.",
    194: "The unrecognized-person branch asks who he is.",
    195: "Rafael says the guide sent him to search and that he got lost.",
    196: "Echo the guide's claim in clean SC1 B287 R104, offset 1037, that they approach every strong-looking person. The current guide says 'We simply ask every person who appears strong enough.'",
    197: "The guide joins after hearing nothing from the people asked to search. The source gives no fate for the others.",
    198: "Rafael blames his own shortcomings after the guide takes responsibility.",
    205: "Lil stammers when asking whether there's any alternative to continuing.",
    206: "Lil would rather proceed in the dark than find something frightening by lighting the cave.",
    207: "Lil recoils from the snake in the moment.",
    211: "The bats make Lil tell everyone to run through to the exit.",
    217: "Keep the catalog name, celadon, the FI substitution and the reported location in East Asia.",
    218: "Verisa relays the claim about better fortune-telling and wishes she could try it once.",
    219: "The fixed actor 0 reply is Rafael's thoughtful pause. Keep it distinct from Verisa's FI address.",
    221: "Verisa treats the pirate activity as a report and advises the party to prepare its equipment.",
    222: "Rafael acknowledges the danger, thanks Verisa and promises to be careful.",
    226: "Maria's eyes have adjusted to the darkness. She proposes continuing without lighting anything.",
    227: "Maria judges the snake too dangerous to take on and orders a retreat.",
    230: "The bats are a new nuisance in the fire branch. Keep Maria's frustration at repeated trouble.",
    231: "Maria explicitly judges the bats harmless before telling the crew to press on.",
}
PHRASES = (
    "without a map", "lose our way", "climb down the cliff.", "you're joking.",
    "Are you okay?!", "what do we do?", "dead end.", "we may as well try.",
    "signs of fatigue.", "it has passed.", "One day has passed.",
    "if we don't know", "without knowing", "where we're going.", "near the ruins.",
    "near the ruins?!", "all these bats!", "out of the jungle!", "through the jungle!",
    "a map to the ruins.", "an ancient city", "off this island.", "cross the sea.",
    "a small boat.", "the rest of the way", "on foot.", "the location of the ruins",
    "the New World?", "the northern continent", "to spread his faith.", "a respected monk",
    "what happened to him.", "are fond of him.", "what became of him?", "I'm worried",
    "A huge snake!", "One of our people!", "An Indian python!", "back to port.",
    "the Castor Company,", "What are you doing here?", "at random,", "come along myself.",
    "search together.", "don't we?", "without a light!", "Get it away from me!",
    "run to the exit!", "I'll be right there.", "the Goryeo Incense Burner?",
    "somewhere in East Asia.", "try it just once...", "running wild", "well equipped.",
    "Thanks for the warning.", "I'll be careful.", "keep going?", "Everyone, fall back!",
    "where we've come out...", "one thing after another...",
)

binder = precedent.binder
source = checked_text(precedent.source, {
    "if 5 <= ordinal <= 12 or 128 <= ordinal <= 135:":
        "if 1 <= ordinal <= 8 and ordinal not in NOTES or 9 <= ordinal <= 15:",
    "Keep this crew voice and the warning about attempting the route without a map.":
        "Keep this crew voice as the party prepares for the cliff route.",
    "PHRASES + VISUAL_PHRASES.get(ordinal, ())": "PHRASES + WRAP_PHRASES.get(ordinal, ())",
    '            if item["decision"] == "revision":':
        '''            if (route, ordinal) in WRAP_ONLY:
                assert item["decision"] == "retention"
                item.update(decision="revision", wrap_only=True, localization_note=WRAP_ONLY[route, ordinal])
            if item["decision"] == "revision":''',
    "assert done == chosen.keys(), chosen.keys() - done": "assert done == chosen.keys() | WRAP_ONLY.keys(), chosen.keys() - done",
    "== 511": "== 477",
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::whole-exchange-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
