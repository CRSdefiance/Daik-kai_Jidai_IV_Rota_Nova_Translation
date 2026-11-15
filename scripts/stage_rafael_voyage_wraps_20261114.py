"""Review Rafael's travel exchanges and the trade and naval tutorials."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_crew_wraps_20261114 as parent
from scripts import stage_rafael_crew_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior, wraps = previous.base, previous.sha, previous.prior, previous.wraps
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_voyage_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_voyage_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'

# The earlier replay checks transition bodies through the stage's token scanner.
previous_token_scanner = previous.previous.bare_tokens

DECISIONS = {
    (115, 17): ('Claudio', "They're out of their minds! But... they said they'd be back, right?",
        'Claudio calls the group mad, then recalls that they said they would gather here again.',
        'Keep the sharp outburst and his shift to what he overheard. The short question tag belongs with the second thought before Rafael asks what the group is planning.',
        ("out of their minds!", "they said they'd be back, right?")),
    (121, 45): ('Mysterious Old Man', 'Travelers! Thank goodness! Please save my grandson!',
        'The old man is relieved that travelers have arrived and begs them to save his grandson.',
        'Use two urgent beats, relief and a plea. The next reply repeats grandson, then the boy calls out and Rafael sees him drowning.',
        ('Thank goodness!', 'Please save my grandson!')),
    (121, 116): ('Mysterious Old Man', None,
        'He does not know the reward’s provenance, and has heard it is quite valuable.',
        'Keep his uncertainty about both the item’s history and its reported value. Rafael initially refuses what the old man earned for defeating the bandits.',
        ("I don't know its history,", "I'm told it's quite valuable.")),
    (123, 146): ('Maria', "Give up your revenge. What good will it do? It won't give you back what you lost.",
        'Maria urges the group to abandon revenge. It serves no purpose and will not restore their happiness.',
        'Let the challenge lead into the loss Maria is asking them to face. Her next line explains how continued fighting would hurt more of their own people.',
        ('Give up your revenge.', 'What good will it do?', "give you back what you lost.")),
    (123, 196): ('Bandit', "All right. I'll take a chance on you!",
        'After considering the offer and what staying would accomplish, the man decides to take a chance on Maria.',
        'Keep the personal gamble and switch from doubt to commitment. Maria immediately welcomes him.',
        ("I'll take a chance on you!",)),
    (124, 14): ('Benazir', "I can't just take a gift and give nothing back. Here's a tip to say thanks.",
        'Benazir feels she should reciprocate for the gift and offers a useful piece of information.',
        'Use a warm offer in return for the gift. The following two lines explain the building in India and the map needed to find it.',
        ("I can't just take a gift", 'give nothing back.', "Here's a tip to say thanks.")),
    (126, 10): ('Villager', 'You found this knife. You have every right to keep it.',
        'The speaker tells the discoverers they have the right to keep the knife.',
        'Keep the formal acknowledgement in straightforward speech. The villager then explains the discovery’s importance to the community and asks them to accept.',
        ('You found this knife.', 'You have every right to keep it.')),
    (128, 143): ('Julio', "It's not just my business. I'm going to look into something that concerns the future of us all.",
        'Julio says the errand concerns everyone’s future and that he means to look into it.',
        'Retain Julio’s gentle correction after Claudio calls it his private errand. Rafael’s next question picks up the reference to their future.',
        ("It's not just my business.", "I'm going to look into something", 'the future of us all.')),
    (129, 33): ('Julio', "They link Africa to the Mediterranean. Verde has plenty of goods for little investment.",
        'Las Palmas and Verde lie at the gateway between Africa and the Mediterranean. Verde can yield many local specialties for a small investment.',
        'Restore the strategic reason to secure both ports, then give Julio’s practical observation about Verde.',
        ('They link Africa', 'to the Mediterranean.', 'plenty of goods', 'for little investment.')),
    (129, 36): ('Julio', "Trade between Africa and the Mediterranean. Put profits into bigger ships and more market share.",
        'He advises sailing back and forth between the two regions and spending the proceeds on bigger ships and more share in the towns.',
        'Use the same market-share term as the previous tutorial advice. The next line explains why more hold space and goods improve each run.',
        ('the Mediterranean.', 'Put profits into', 'bigger ships', 'more market share.')),
    (129, 48): ('Julio', "If you've got enough to spare, you could try the New World too. No need to push it, though.",
        'He adds that they can venture as far as the New World if they have room to do so, then advises against overextending.',
        'Keep the trip optional and give the reassurance in Julio’s practical voice. Rafael replies that he will try.',
        ("If you've got enough to spare,", 'the New World too.', 'No need to push it, though.')),
    (133, 43): ('Arcadius', None,
        'Arcadius quietly points out that one woman or two makes little difference.',
        'Preserve the understated private joke inside parentheses after Claudio objects to having a woman aboard. Rafael’s aside confirms who Arcadius is counting.',
        ('One woman or two,', "what's the difference?")),
    (134, 19): ('Janus', "I've heard of him. He's got a nasty reputation. Of all the people to spot us...",
        'Janus has heard the rumors about Vels, who is known for being dangerous, and laments that he spotted them.',
        'Keep the immediate recognition and worry, then give Claudio’s shouted warning room to interrupt.',
        ("I've heard of him.", "He's got a nasty reputation.", 'Of all the people to spot us...')),
    (136, 23): ('Claudio', 'The Guiding Staff, I think.',
        'Claudio thinks the treasure is called the Guiding Staff.',
        'Keep the uncertain name as a direct answer to Rafael’s question. The next turn is about why the treasure is valuable.',
        ('The Guiding Staff,', 'I think.')),
    (136, 206): ('Rafael', 'Oh... Th-that was it? Sorry, Julio.',
        'Rafael realizes what Julio meant, stammers, and apologizes.',
        'Restore the stammer and keep the apology direct. Rafael had assumed Julio meant to make him the butt of a joke.',
        ('Th-that was it?', 'Sorry, Julio.')),
    (143, 160): ('Rafael', "It's... nice to meet you. I'm {MACRO:FI} {MACRO:FA}.",
        'Rafael hesitates over his first greeting and then gives his full name.',
        'Keep the faltering greeting and let his name arrive whole. Albuquerque immediately takes over the introductions.',
        ('nice to meet you.', "I'm {MACRO:FI} {MACRO:FA}.")),
    (143, 177): ('Albuquerque', 'Ahem. You do a great deal of business.',
        'Albuquerque clears his throat and concedes that Silveira does business on a wide scale.',
        'Keep the dry understatement after Silveira boasts of his service to Portugal. Silveira takes it as praise.',
        ('a great deal of business.',)),
    (143, 282): ('Albuquerque', "Work together, both of you. I'm counting on you.",
        'Albuquerque urges both men to cooperate fully and says he is counting on them.',
        'Keep the clipped order and the confidence behind it. Both answer before he dismisses them.',
        ('Work together, both of you.', "I'm counting on you.")),
    (143, 380): ('Silveira', "When you're at war with a faction, winning a sea battle hurts their reputation. They'll also lose a little market share in towns near the battle.",
        'A naval victory over a faction at war reduces its reputation and slightly lowers its market share in nearby cities.',
        'Keep the at-war condition and limit the effect to the battle’s vicinity. The next speech explains how to make a contract with one of those cities.',
        ("When you're at war with a faction,", 'winning a sea battle', 'hurts their reputation.', 'a little market share', 'near the battle.')),
    (144, 86): ('Janus', 'Look! The two tablets fit together!',
        'Janus notices the two stone tablets fitting snugly together.',
        'Make the discovery immediate. Claudio exclaims next, and Rafael realizes the tablets have actually become one.',
        ('The two tablets fit together!',)),
    (144, 96): ('Rafael', "The two tablets have become one...",
        'Rafael realizes the two tablets have joined and become one object.',
        'Keep his quiet astonishment after Claudio’s exclamation. The new mark is noticed in the following exchange.',
        ('The two tablets', 'have become one...')),
}


def derive(function, edits):
    env = vars(previous) | globals() | {'previous': previous.previous}
    source = checked_text(getsource(function), edits)
    exec(compile(source, __file__ + '::prior-coverage-and-display-contract', 'exec'), env)
    return env[function.__name__]


get_exchanges = derive(previous.get_exchanges, {
    'extras = {6096, 7436} if block == 84 else set()': 'extras = set()',
})
compile_rows = FunctionType(previous.compile_rows.__code__, vars(previous) | globals() | {'previous': previous.previous})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, vars(previous) | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

