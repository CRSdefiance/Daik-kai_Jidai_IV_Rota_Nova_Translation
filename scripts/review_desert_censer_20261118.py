"""Bind the desert choices, celadon exchanges and Maria's map scenes to their clean records."""

from inspect import getsource
from types import FunctionType

from scripts import prepare_desert_censer_20261118 as paired
from scripts import review_sakura_expeditions_macao_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, parent = paired.paired.base, paired.parent
SOURCE = paired.ROOT / "paired_source.json"
SOURCE_SHA = "8d1545d885df919291b123e2c965dd0b1fbc43182118338a5857a1c9a8e70219"
FOLDER = precedent.FOLDER
DECISIONS = FOLDER / "desert_censer_decisions_v1.txt"
OUTPUT = FOLDER / "desert_censer_20261118_prose_v2.json"
HISTORY = precedent.HISTORY
NOTES = {
    1: "The speaker remembers an earlier obligation to tell the captain. Retain the given-name substitution.",
    2: "The discovery of the illustrated map and the interpretation of the old kingdom's ruins are both secondhand.",
    4: "The speaker cannot say where the map is and encourages the captain to look for it.",
    9: "Use the rough crew voice for the warning about getting lost without a map.",
    10: "The crew member expects the party to get lost. Keep the certainty and the direct address.",
    11: "The younger crew voice makes the map warning immediate and emphatic.",
    18: "Rafael acknowledges the obvious heat and gets the party moving again.",
    24: "This warning belongs to a separate selectable speaker variant. Keep the address and swarm.",
    28: "The choice commits the party to fighting the scorpions, distinct from driving them away or running.",
    29: "The choice means drive the animals off, whether the encountered animals are wolves or scorpions.",
    30: "The concise verb is an immediate decision to run.",
    32: "Relief as the scorpions run off turns into confidence in the admiral.",
    33: "Keep the fleeing scorpions and the crew member's direct praise of the admiral.",
    34: "The crew member calls attention to the retreat, then responds with familiar praise.",
    35: "The rougher speaker celebrates the scorpions' retreat and the admiral's reliability.",
    36: "The older speaker's approval follows the threat subsiding.",
    37: "The youngest speaker is excited that the admiral drove the scorpions off.",
    38: "The respectful speaker expresses relief and trust after the scorpions flee.",
    47: "The crew member's startled urgency leads immediately to treatment.",
    51: "The FE notice names the injured captain and explicitly costs one day for treatment.",
    53: "Rafael volunteers and audibly shoos the scorpions away.",
    56: "Keep the repeated coaching as the crew tries to move without attracting the scorpions.",
    62: "The falling luggage breaks the attempted quiet. Avoid assigning blame for dropping it.",
    72: "After the cry of pain, the crew member tells the injured person to stay alert.",
    75: "The notice hedges about the injured crew. The Japanese noun can describe the crew collectively.",
    78: "Keep the item catalog name and restore celadon. Rafael does not receive the East Asia clue here.",
    80: "The fortune-teller presents greater accuracy as hearsay and wistfully wants to try the burner once.",
    84: "The captain reacts to the danger, thanks the fortune-teller and says they will be careful.",
    86: "The fortune-teller recognizes the returning captain and greets them warmly.",
    87: "Her readings have improved since receiving the incense burner. The reading is her way of thanking the captain.",
    88: "She asks the captain to sit down before the two silent holds.",
    89: "Preserve each intentional silent hold before she gives the location.",
    90: "The ruins are deep in the desert, far inland from the current town. She is confident the sought object is there.",
    95: "Keep this guarded cry distinct from the party's spoken reaction and the later FE notice.",
    100: "Keep the catalog name, the celadon material and the secondhand clue that it is somewhere in East Asia.",
    107: "Lil's thanks, lingering fright and dislike of bugs carry the joke.",
    108: "Lil hesitates even as she volunteers to scare the scorpions off.",
    110: "The companion identifies the supposed sting as a cactus spine still stuck in Lil.",
    112: "The crew member reassures Lil that the sting is only a cactus spine.",
    113: "The familiar crew voice teases Lil about her reaction once the mistake is clear.",
    117: "Lil relaxes at the diagnosis and repeats her dislike of bugs.",
    120: "The clan guards the map to the Proof. This speaker confirms the village location with the admiral.",
    121: "The speaker urges a prompt visit and reports the village location secondhand.",
    122: "Curiosity about the clan leads the speaker to suggest going immediately.",
    123: "The speaker wants to meet the clan before the crew forgets and checks the direction.",
    124: "The familiar speaker urges a visit soon and expects confirmation of the village location.",
    125: "The older speaker recalls the Proof and proposes heading to the map guardians' village soon.",
    126: "The younger speaker is curious who guards the map and wants to visit the village.",
    127: "The formal speaker wonders about the map and checks the remembered direction after proposing a visit.",
    150: "The alarmed crew member asks Maria what she intends to do just before the choice.",
    151: "The menu commits the party to fighting the wolves, distinct from dispersing them or running.",
    165: "The notice identifies the wounded captain with the original given-name substitution and reports no treatment duration.",
    166: "Maria tells the party to draw swords and press on before another sailor is hurt.",
    175: "The injured speaker can just about manage and falters from pain.",
    178: "The crew member stammers but tries to play down the wound.",
    181: "Maria accepts responsibility for the injury and apologizes before the crew consoles her.",
    187: "The older speaker says prompt care keeps this wound from becoming serious and declares the danger over.",
    191: "The notice reports apparent fatigue after the encounter.",
    192: "Maria reads the wolves as very hungry and calls for immediate retreat.",
    193: "The notice reports fatigue as fact and the crew departures as apparent.",
    195: "The winded speaker wonders whether they have run far enough.",
    205: "The younger voice is uncertain but talks themself into expecting an end to the forest.",
    212: "Her firsthand visit establishes the name and scale of the Forbidden City. She invites Maria to see for herself.",
    220: "The formal warning states that progress is impossible without the map.",
    230: "This first choice turns back before looking for another route.",
    231: "This choice first checks whether the party can bypass the dead end.",
    241: "After the crew reports no path onward, Maria decides to look for another way while heading back.",
    242: "The system reports one elapsed day after the forest detour.",
    247: "Maria is curious about the illustrated map and asks where it is.",
    248: "Maria acknowledges that the heat comes with the desert and tells the group to press on.",
    252: "Maria orders a quiet retreat without provoking the scorpions.",
}
PHRASES = (
    "ancient illustrated map", "old kingdom", "near town.", "where it is.",
    "without a map.", "count on you, Admiral.", "count on you, Admiral!",
    "You're amazing, Admiral!", "and fast!", "right away!", "a sailor was injured.",
    "the Goryeo Incense Burner?", "It's made of celadon.", "somewhere in East Asia.",
    "to try it just once...", "Thanks for the warning.", "for the warning.",
    "I'll be careful.", "since you gave me", "that incense burner.",
    "read your fortune", "to thank you.", "deep in the desert,", "far inland from here.",
    "what you're looking for", "Don't provoke them.", "a cactus spine.",
    "the map to the Proof.", "the map to the Proof?", "northeast of China, right?",
    "northeast of China!", "northeast of China, isn't it?",
    "northeast of China.", "Shall we visit", "its guardians' village?",
    "Let's keep moving.", "Look out!", "I let my guard down.", "Stay with me!",
    "the wolves are gone.", "The wolves have run off,", "right away", "It'll heal",
    "You all right?", "left the party.", "Think we're safe here?", "before long.",
    "without a map?", "out of the woods soon.", "the Forbidden City",
    "look for another way.", "One day has passed.", "fighting the scorpions",
)
VISUAL_PHRASES = {
    4: ("why not look for it?",),
    34: ("Knew we",),
    35: ("came through again, Admiral.",),
    36: ("Well done, Admiral.",),
    38: ("Well done, Admiral.",),
    55: ("Nice and quiet now.",),
    56: ("Quiet now.",),
    59: ("Quietly now.",),
    110: ("a cactus spine",),
    120: ("far northeast of China, right?",),
    124: ("far northeast of China, right?",),
    126: ("far northeast of China!",),
    127: ("far northeast of China, isn't it?", "Let's visit"),
    182: ("treat it right away.",),
    205: ("forest, right?",),
}
FINAL_WORDING = {
    (3, 120): "Admiral, let's visit the clan that guards the map to the Proof. Their village's far northeast of China, right?",
    (3, 124): "Admiral, let's hurry to their village and meet the clan guarding the map to the Proof. Far northeast of China, right?",
    (3, 127): "Admiral, I'm curious about the map to the Proof. Let's visit the guardians' village. Far northeast of China, isn't it?",
    (3, 248): "It's a desert. Of course it's hot. Let's keep moving.",
}

binder = precedent.binder
source = checked_text(getsource(precedent.main), {
    'chosen = {(int(route), int(pos)): english for route, pos, english in edit_list}':
        'chosen = {(int(route), int(pos)): english for routes, pos, english in edit_list for route in routes}',
    'assert len(chosen) == len(edit_list)': 'assert len(chosen) == sum(len(routes) for routes, _, _ in edit_list)',
    "    history_paths =": "    chosen.update(FINAL_WORDING)\n    history_paths =",
    'if 43 <= ordinal <= 50:': 'if 5 <= ordinal <= 12 or 128 <= ordinal <= 135:',
    "Keep the individual companion's register and the map's distinction from the Proof.":
        "Keep this crew voice and the warning about attempting the route without a map.",
    '"PHRASES": PHRASES}': '"PHRASES": PHRASES + VISUAL_PHRASES.get(ordinal, ())}',
    '== 527': '== 511',
})
scope = vars(precedent) | globals()
exec(compile(source, __file__ + "::paired-contextual-ledger", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
