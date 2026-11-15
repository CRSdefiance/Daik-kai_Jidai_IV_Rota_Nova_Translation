"""Review earlier wraps in Rafael's diplomacy, crew and artifact scenes."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_voyage_wraps_20261114 as parent
from scripts import stage_rafael_voyage_wraps_20261114 as previous


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_alliance_wraps_20261114_v2')
CAPTURE = Path('work/rafael_alliance_wraps_20261114_v1/rafael_startup/capture_report.json')
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_alliance_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'

DECISIONS = {
    (148, 93): ('Rafael', 'So go easy on the Arabian markets.',
        'Rafael confirms that he should avoid interfering too much in Arabian markets.',
        'Keep his practical summary after Uddin offers to share those markets within limits. Uddin confirms and promises to leave Rafael free to act elsewhere.',
        ('go easy on', 'the Arabian markets.')),
    (150, 13): ('Innkeeper', "They say it was for divination. People filled it with water, then floated flowers or leaves to foretell the year's events.",
        'The platter was reportedly used for divination by floating flowers or leaves in water to foretell the year’s events.',
        'Keep the hearsay and distinguish the water from what floats on it. The explanation gives Rafael the idea to try the Evergreen Lotus Leaf.',
        ('They say it was for divination.', 'filled it with water,', 'flowers or leaves', "foretell the year's events.")),
    (151, 117): ('Rafael', "Of course I'm Portuguese! And proud of it! I won't take orders from the King of Spain!",
        'Rafael insists that he is Portuguese and proud of it. He refuses to do as the Spanish king tells him.',
        'Keep the burst of pride as a reply to Claudio’s fear that Rafael has accepted what happened. Arcadius answers with empathy.',
        ("I'm Portuguese!", 'And proud of it!', "I won't take orders", 'the King of Spain!')),
    (151, 155): ('Rafael', "No. Even if we went home, we couldn't beat Spain's forces now that they've absorbed the Portuguese military...",
        'Returning would not give them the strength to beat the Spanish forces after they absorbed the Portuguese military.',
        'Use military for the source’s broader scope. Keep the conditional reasoning that leads into Rafael’s decision to build strength in Asia.',
        ('Even if we went home,', "we couldn't beat", "Spain's forces", 'the Portuguese military...')),
    (151, 208): ('Claudio', "{MACRO:FI}, are you sure? You're not giving up, are you?!",
        'Claudio calls Rafael by name, asks if he is sure and fears he is giving up.',
        'Keep his alarm and complete tag. Rafael answers unequivocally that he will build strength and return.',
        ('are you sure?', "You're not giving up, are you?!")),
    (152, 128): ('Pereira', "See it from my side. I'm Portugal's governor of Indochina. Now I answer to the King of Spain.",
        'Pereira asks Rafael to consider his position as Portugal’s governor of Indochina, now subject to the King of Spain’s orders.',
        'Keep Pereira’s plain appeal and the exact office. Rafael’s next question spells out the danger of backing them.',
        ('See it from my side.', "Portugal's governor of Indochina.", 'Now I answer to the King of Spain.')),
    (152, 136): ('Pereira', "A lot of people count on me to get by. I've got to look after them. That's the hard part of being governor.",
        'Many people’s livelihoods depend on him. Looking after them is the hard part of being governor.',
        'Keep the concern for people’s livelihoods as his reason for refusing. He immediately explains where he still has room to help.',
        ('count on me', "I've got to look after them.", 'the hard part of being governor.')),
    (153, 9): ('Claudio', "Let's polish it. See that Lotion Jar?",
        'Claudio suggests polishing the coin and points out the Lotion Jar nearby.',
        'Keep the casual suggestion and the exact item name. Rafael immediately wonders what is in the jar and tries it.',
        ("Let's polish it.", 'See that Lotion Jar?')),
    (154, 152): ('Rafael', "Given all that, sir, I'm afraid we can't help right away...",
        'Considering the situation, Rafael says he and the crew are unlikely to be able to help the man immediately.',
        'Keep the respectful reluctance and tentative timing. He intends to act soon but gives no promise.',
        ('Given all that, sir,', "I'm afraid we can't help", 'right away...')),
    (155, 9): ('Juan Blanco', "So I hear. They're a tough lot.",
        'Juan confirms the report and has also heard that the newcomers are formidable.',
        'Let the hearsay come through in Juan’s answer before the sailor speculates about Escante’s plan.',
        ('So I hear.', "They're a tough lot.")),
    (156, 17): ('Rafael', None,
        'Rafael says they will deal with it if that possibility comes to pass.',
        'Keep his noncommittal response. Claudio presses him because he sees an immediate threat.',
        ("We'll deal with that if it happens.",)),
    (156, 22): ('Claudio', "{MACRO:FI}! You know we're in their way! At this rate, we're done for!",
        'Claudio calls to Rafael and warns that they are in the rivals’ way and risk defeat if things continue as they are.',
        'Keep his urgency and personal address before Janus interrupts to point out Maldonado.',
        ("You know we're in their way!", "At this rate, we're done for!")),
    (156, 57): ('Janus', 'A dispute over trade, maybe?',
        'Janus wonders if the rivals are fighting over their business interests.',
        'Keep the speculation short so Claudio can answer that both want the New World for themselves.',
        ('A dispute over trade,',)),
    (156, 68): ('Claudio', "Then we're first on their list.",
        'Claudio is certain their crew will be the first target.',
        'Keep Claudio’s confidence as a direct answer to Janus. Rafael’s reply is much less sure.',
        ("we're first on their list.",)),
    (159, 47): ('Arcadius', '{MACRO:FI}... She told me, "I think about {MACRO:FI} all day, every day."',
        'Eirene says Charlotte told her she thinks of Rafael all the time, every day.',
        'Keep both runtime name substitutions. Charlotte’s words answer Rafael’s admission that he cannot stop thinking about her.',
        ('She told me,', 'all day, every day."')),
    (159, 68): ('Arcadius', "Forgive her for leaving like that. She's scared she isn't good enough for you.",
        'Eirene asks Rafael to forgive Charlotte for leaving so suddenly. Charlotte fears she is not his equal.',
        'Use a gentle request and frame the insecurity as Charlotte’s own fear. Eirene explains the family concern in her next turn.',
        ('for leaving like that.', "She's scared", "isn't good enough for you.")),
    (160, 48): ('Yifa', "Neat, huh? I took it all apart!",
        'Yifa is excited by how interesting it is and says she has disassembled the whole object.',
        'Let Yifa take credit for the work. Rafael immediately remarks on her skill with her hands.',
        ('Neat, huh?', 'I took it all apart!')),
    (162, 9): ('Priest', 'You shall rule the Mediterranean. I bestow this upon you.',
        'The priest formally bestows the object on the person destined to rule the Mediterranean.',
        'Keep the ceremonial address and the formal act of giving. Claudio immediately marvels at what they received.',
        ('shall rule the Mediterranean.', 'I bestow this upon you.')),
}

get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())
compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': previous.compile_rows.__globals__['previous']})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

