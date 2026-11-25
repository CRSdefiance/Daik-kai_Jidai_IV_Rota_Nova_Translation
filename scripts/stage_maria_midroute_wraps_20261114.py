"""Review the flagged Maria dialogue in SC3 blocks 100 through 149."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_maria_opening_wraps_20261114 as parent
from scripts import stage_maria_opening_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/maria_midroute_wraps_20261114_v1')
CAPTURE = ROOT / 'maria_startup/capture_report.json'
RUNTIME = ROOT / 'maria_native_context.json'
REVIEW = parent.TRIAGE.with_name('maria_midroute_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded, expand_bytes = previous.native, previous.expanded, previous.expand_bytes
initial_names = previous.initial_names


DECISIONS = {
    (100, 9): ("Villager", "You found the dagger. It's yours by right.",
        "The finders have a right to keep the dagger.",
        "The villager formally offers the dagger before thanking the party for finding what sustains the tribe. The displayed gold is a separate reward.",
        ("It's yours by right.",)),
    (102, 95): ("Xien", "I'm not the superstitious sort...",
        "Xien says he is not usually inclined to believe superstition.",
        "He broaches a possible source of comfort after Maria confides in him. Keep the hesitance that prompts her question.",
        ("the superstitious sort...",)),
    (102, 118): ("Xien", "They say it guides its bearer toward good and lies somewhere in India.",
        "Xien says the staff reportedly guides its possessor toward good and is said to be in India.",
        "This explains the name Guiding Staff after Maria echoes it. Keep both claims as things Xien has heard.",
        ("guides its bearer", "toward good", "somewhere in India.",)),
    (105, 73): ("Maria", "The people here... So afraid of me.",
        "Maria realizes the townspeople are very afraid of her.",
        "Her halting realization belongs between Xien's silence and her account of doing everything she could to protect them.",
        ("So afraid of me.",)),
    (109, 65): ("Ian", "I'd love to see you stun those Westerners. They're so sure of their own strength.",
        "Ian would enjoy imagining the boastful Westerners astonished by Maria's skill.",
        "Let his dry wit follow his sincere explanation of why he follows Maria, and keep their arrogance tied to their power.",
        ("stun those Westerners.", "of their own strength.",)),
    (112, 32): ("Maria", "I acted on impulse. I'll be more careful. I'm sorry I worried you, Xien.",
        "Maria acted on impulse, says she should be more careful and apologizes for worrying Xien.",
        "Keep her apology personal after Xien gently cautions her. He then returns the conversation to finding the Proof.",
        ("I acted on impulse.", "I'll be more careful.", "I worried you, Xien.",)),
    (116, 24): ("Ian", "You joined us later, so you wouldn't know. She's strict about rewards and punishments. That's how I'd put it.",
        "Ian says Samwell joined too recently to know and that Maria is strict in judging rewards and punishments.",
        "Let Ian answer Samwell with precision before Jam gives the same assessment in his rougher voice. The account that follows illustrates both sides of her judgment.",
        ("You joined us later,", "so you wouldn't know.", "rewards and punishments.", "That's how I'd put it.",)),
    (119, 4): ("Guildmaster", "You're after the Mediterranean Proof of Conquest, aren't you?",
        "The guildmaster asks whether they are looking for the Mediterranean's Proof of Conquest.",
        "Keep the knowing question together before Maria asks how he knows and mentions her search for a map.",
        ("Proof of Conquest, aren't you?",)),
    (121, 47): ("Maria", "We meet again. What brings you here?",
        "Maria acknowledges their meeting again and asks what the other person wants.",
        "Give her a neutral greeting that allows his abrupt question about world conquest to set the tone.",
        ("We meet again.", "What brings you here?",)),
    (127, 12): ("Al", "Fine. If you want me gone, I'm gone.",
        "Al takes the dismissal at face value and says he will leave as requested.",
        "Let him throw the dismissal back at the guildmaster. Xien reacts to the unpleasant scene afterward.",
        ("If you want me gone,", "I'm gone.",)),
    (128, 53): ("Angelo", "Right. Thanks. My kid sister means the world to me. She's missing. I'm looking for her...",
        "Angelo confirms the woman in the pendant is his beloved younger sister, thanks Maria and says he is looking for her.",
        "Confirm their real relationship after Maria asks. His grief and determination motivate his request to join the crew.",
        ("My kid sister", "means the world to me.", "I'm looking for her...",)),
    (128, 77): ("Angelo", "Mamma mia! Hang on, sis! I'm Angelo Puccini. Glad to be aboard!",
        "Angelo exclaims in Italian, calls for his sister to wait and gives his full name after he is hired.",
        "Keep the excited burst and the full self-introduction before Maria gives her name in return.",
        ("Hang on, sis!", "I'm Angelo Puccini.", "Glad to be aboard!",)),
    (129, 63): ("Angelo", "My sister told me you're my family now. She said I should live for myself...",
        "Angelo recalls his sister saying the crew is his family now and that he should live for himself.",
        "Keep this as her message, which Maria later takes up explicitly, following Angelo's admission that he could not accept the death.",
        ("you're my family now.", "live for myself...",)),
    (130, 82): ("Fernando", "Sharp eyes. I'd say he's my equal.",
        "Fernando says the man's powers of observation are about as good as his own.",
        "Keep the self-regarding compliment after Carlo mentions the shopkeeper's complexion. Maria is still unconvinced.",
        ("he's my equal.",)),
    (130, 126): ("Innkeeper", "Listen to me go on. You saved his life. I wanted to thank you.",
        "The innkeeper catches herself talking at length, calls Carlo a lifesaver and says she wants to thank him.",
        "Make the gratitude concrete after she describes how sick Adil was. Carlo redirects the thanks to the travelers.",
        ("You saved his life.", "I wanted to thank you.",)),
    (130, 232): ("Maria", None,
        "Maria realizes this explains Carlo's concern for the man at the shop.",
        "The quiet realization works after Carlo explains how his priorities changed. Keep the turn trailing off before she asks about going home.",
        ("worried about the shopkeeper...",)),
    (135, 328): ("Cesare", "When higher market share means more goods, it's time to buy ships.",
        "Cesare advises buying ships when market share has risen enough to buy more goods.",
        "Use the market-share term from the game. This is the threshold after his advice against buying new ships on small contracts.",
        ("higher market share", "means more goods,", "it's time to buy ships.",)),
    (136, 15): ("Fernando", "New around here, eh? How about we play for a drink? Relax, it's a simple game.",
        "Fernando greets a newcomer and suggests wagering a drink on an easy game.",
        "Use the easy tavern challenge before he explains taking turns with the coins. Preserve the single drink wager.",
        ("How about we play for a drink?", "it's a simple game.",)),
    (136, 88): ("Fernando", "See that couple? We can't hear them, but what do you think they're talking about?",
        "Fernando points out the couple and asks the others to guess what they are saying without hearing them.",
        "The question demonstrates his point about reading people. It should give Maria room to guess that a proposal is underway.",
        ("See that couple?", "We can't hear them,", "what do you think", "they're talking about?",)),
    (136, 95): ("Fernando", "Come on, it's obvious. They're breaking up.",
        "Fernando calls it easy to read and says the couple is talking about breaking up.",
        "Keep his cocky correction of Maria's guess ahead of the scene proving him right.",
        ("They're breaking up.",)),
    (136, 110): ("Man", "Think what you want. You're selfish too.",
        "The man says she can think what she wants and calls her selfish in return.",
        "The blunt answer mirrors her accusation and sets up her decision that they should stop seeing each other. The registered Man label suits the public exchange.",
        ("Think what you want.", "You're selfish too.",)),
    (136, 211): ("Fernando", "I'm Fernando Dias! Call it luck!",
        "Fernando introduces himself and calls the meeting another instance of luck.",
        "Echo the role of luck in gambling and Fernando's decision to stake his life on Maria before she welcomes him.",
        ("I'm Fernando Dias!",)),
    (137, 61): ("Charles", "The admiral has odd tastes...",
        "Charles murmurs that the admiral is fond of odd things.",
        "Keep the dry aside about Maria's choice so the remark about Charles being one to talk still lands.",
        ("has odd tastes...",)),
    (139, 72): ("Mikhail", "Ah, a peppercorn. It grows on tropical trees. Grind it up and you have a spice.",
        "Mikhail confidently identifies the object as a peppercorn from a tropical tree and says grinding it makes a spice.",
        "Preserve what he claims before giving the planting tip. His correction to rabbit droppings is the point of the joke.",
        ("It grows on tropical trees.", "Grind it up", "you have a spice.",)),
    (139, 80): ("Mikhail", "Wait... Rabbit droppings! Ugh!",
        "Mikhail takes another look, realizes he is holding rabbit droppings and recoils.",
        "Let the realization overturn his confident peppercorn advice before the child tells him to throw it away.",
        ("Rabbit droppings!",)),
    (139, 170): ("Mikhail", "No, no! I've made up my mind. I'm coming with you! You'll see how handy my knowledge is. Don't you worry!",
        "Mikhail refuses to back down and insists that he is going and that his knowledge will be useful.",
        "Keep his stubborn repetition after Xien calls him rude. Maria gives in because they invited him first.",
        ("I've made up my mind.", "I'm coming with you!", "my knowledge is.", "Don't you worry!",)),
    (140, 79): ("Maria", "(Huh? Nothing's happened...)",
        "Maria privately wonders at the lack of any apparent event.",
        "The brief thought sets up the immediate surprise attack. Keep the thought in parentheses.",
        ("Nothing's happened...",)),
    (141, 40): ("Sanghyeon", "I'm ashamed to admit it, but it's my fault Yifa grew up so unruly. I failed to guide her.",
        "Sanghyeon is ashamed and blames his inadequate guidance for Yifa growing up unruly.",
        "Keep the formal self-reproach of a senior fellow student. He explains what she did and that their master was unaware.",
        ("I'm ashamed to admit it,", "Yifa grew up so unruly.", "I failed to guide her.",)),
    (142, 54): ("Julian", "Your smile keeps me going! If I find it, will you go out with me?",
        "Julian says Mihwa's smile gives him strength and asks for a date if he gets the Silla Gold Crown.",
        "The crown is named in his preceding promise. Keep the affection and direct condition so she can tease him about getting ahead of himself.",
        ("Your smile keeps me going!", "will you go out with me?",)),
    (142, 64): ("Mihwa", "I'll be waiting... Oh. He's gone.",
        "Mihwa begins saying she will wait, then notices Julian has already left.",
        "Keep the light interruption after he rushes away. Maria overheard them and speaks next.",
        ("I'll be waiting...", "Oh. He's gone.",)),
    (143, 54): ("Reika", "Um, they say the Silla Gold Crown is in the Tomb of King Muryeong. That's all I know...",
        "Reika hesitantly shares a report that the Silla Gold Crown is in the ruins called the Tomb of King Muryeong.",
        "Keep the exact item and site names with the uncertainty of the tip before Maria decides to have a look.",
        ("the Silla Gold Crown", "the Tomb of King Muryeong.", "That's all I know...",)),
    (146, 45): ("Yukihisa", "No, it has nothing to do with our mission. Please don't trouble yourself.",
        "Yukihisa says the matter is unrelated to their purpose and asks Maria not to concern herself.",
        "Keep his formal reluctance after Maria offers help, before she asks whether he will go to Japan on his own.",
        ("our mission.", "Please don't trouble yourself.",)),
}


pair_source = checked_text(previous.get_source, {
    '# The registered B87R139 continuation is one extra FE command in the current stream.':
        '# The registered B116R41 and B116R51 entries each own a second FE panel.',
    'extras = {712} if block == 87 else set()': 'extras = {630, 1026} if block == 116 else set()',
})
env = previous.get_exchanges.__globals__ | globals()
exec(compile(pair_source, __file__ + '::original-Maria-commands-and-B116-continuations', 'exec'), env)
get_exchanges = env['get_exchanges']

compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': initial_names})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

