"""Review Rafael's ship, crew, and tavern dialogue against the clean exchanges."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_homecoming_wraps_20261114 as parent
from scripts import stage_rafael_homecoming_wraps_20261114 as previous


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_seamanship_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_seamanship_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'

DECISIONS = {
    (173, 23): ('Arcadius', "If it's true, we're in real trouble.",
        'Arcadius says that if the report is true, it is a serious matter.',
        'Keep the conditional worry between Claudio’s disbelief and the sailor’s urgent summons.',
        ("If it's true,", "we're in real trouble.")),
    (176, 68): ('Jam', "Where there's a will, there's a way! Yahoo! It's OK if I say it's OK!",
        'Jam quotes the proverb, cheers, then declares his own approval sufficient.',
        'Keep the proverb exact so Rafael can echo it. The repeated OK carries Jam’s comic confidence.',
        ("Where there's a will, there's a way!", "It's OK if I say it's OK!")),
    (177, 43): ('Cesare', "Forgive me. I'm Cesare Tony. I used to own this ship.",
        'Cesare apologizes, gives his name, and identifies himself as the ship’s former owner.',
        'Use his formal introduction and keep the name intact. He next explains how pirates took the ship.',
        ("I'm Cesare Tony.", 'own this ship.')),
    (177, 183): ('Cesare', "Once your market share lets you buy more goods, it's time to buy a ship.",
        'Cesare says to buy a ship once increased market share lets them buy more trade goods.',
        'Keep the threshold clear after the one percent example. The next line moves on to size and price.',
        ('your market share', 'buy more goods,', "it's time to buy a ship.")),
    (178, 147): ('Rafael', "So nine is one plus four plus four. However many they take, I can take just enough to leave five on my turn. That means I win!",
        'Rafael works out that nine is one plus four plus four and that he can always leave five after the opponent’s turn.',
        'Preserve the arithmetic and the order of turns. Janus praises how quickly Rafael understood the strategy.',
        ('one plus four plus four.', 'However many they take,', 'leave five on my turn.', 'That means I win!')),
    (178, 196): ('Fernando', 'Sure. Gambling takes insight and luck.',
        'Fernando says good judgment and luck are important in gambling.',
        'Keep both qualities because Rafael challenges the first and Fernando demonstrates it by reading the couple.',
        ('insight and luck.',)),
    (178, 218): ('Fernando', "Come on, this one's easy. They're breaking up.",
        'Fernando calls it easy and says the couple is talking about breaking up.',
        'Keep his confidence and preserve the whole prediction before the couple proves his point.',
        ("They're breaking up.",)),
    (178, 234): ('Man', "Think what you want. You're selfish too.",
        'The man says she can think as she pleases and returns the charge of selfishness.',
        'Keep the dismissive response and mirrored accusation. The woman then suggests they stop seeing each other.',
        ("You're selfish too.",)),
    (179, 8): ('Manuel', "Still, there's room for improvement. For instance...",
        'Manuel sees room for improvement and begins to give an example.',
        'Keep the evaluative tone and unfinished thought before Rafael asks whether anything is wrong.',
        ("there's room for improvement.", 'For instance...')),
    (179, 80): ('Manuel', "That thrill when a ship's heartbeat shakes you to the core... Oh, pardon me. It's been so long since I sailed. I got a little carried away.",
        'Manuel recalls how a ship’s heartbeat stirred his soul, then apologizes for getting excited after so long ashore.',
        'Keep the image and the moment he catches himself. He accepts their offer in the next turn.',
        ("a ship's heartbeat", 'shakes you to the core...', 'Oh, pardon me.', "It's been so long since I sailed.", 'I got a little carried away.')),
    (179, 122): ('Manuel', "At sea, a shipwright like me can fix a damaged ship from the Lumber Room. At the shipyard, I can help with refits and repairs.",
        'A shipwright repairs a damaged ship from the Lumber Room at sea and can help refit or repair a ship at a shipyard.',
        'Preserve the exact room name, the distinction between the two places and both services.',
        ('a shipwright like me', 'a damaged ship', 'from the Lumber Room.', 'At the shipyard,', 'with refits and repairs.')),
    (180, 46): ('Cesare', "When it comes to ships, we're past needing lessons.",
        'Cesare says they no longer need a lesson about ships.',
        'Keep his polished confidence before the shipwright decides to wait for greener customers.',
        ('When it comes to ships,', "we're past needing lessons.")),
    (180, 72): ('Shipwright', "A square sail is rigged crosswise. That's what makes it a transverse sail.",
        'A square sail is set across the direction of the ship and is a kind of transverse sail.',
        'Keep the technical term and explain it through the direction of the rig. The following turn describes the wind trade-off.',
        ('rigged crosswise.', 'a transverse sail.')),
    (180, 76): ('Shipwright', "A square sail can't turn fore-and-aft. It does well in a following wind. But in a headwind, you can't set it at the best angle.",
        'The square sail cannot be turned lengthwise, works well in a following wind, and cannot take the optimal angle in a headwind.',
        'Keep the game tutorial’s contrast between a following wind and a headwind. The next line introduces lateen sails.',
        ("can't turn fore-and-aft.", 'in a following wind.', 'But in a headwind,', 'at the best angle.')),
    (180, 102): ('Shipwright', "Did you know that with two or more masts, a ship goes faster with the wind off its rear quarter than with the wind straight astern?",
        'The shipwright asks if they knew a ship with two or more masts sails faster with a diagonal wind from behind than with a direct tailwind.',
        'Keep the two-mast minimum and the comparison of directions. His next line asks another listener for the reason.',
        ('two or more masts,', 'off its rear quarter', 'wind straight astern?')),
    (181, 136): ('Yifa', "See that? My paralysis technique!",
        'Yifa boasts that she has demonstrated her paralysis technique.',
        'Keep her proud reveal intact before Claudio insists she only caught him off guard.',
        ('My paralysis technique!',)),
    (183, 101): ('Rafael', 'Your senior? Is it Sanghyeon?',
        'Rafael asks whether the senior student Yifa senses is named Sanghyeon.',
        'Keep the established name and the surprised question. The next replies make clear the senior is a fellow student.',
        ('Is it Sanghyeon?',)),
    (183, 125): ('Rafael', 'His arts? Th-that was one of them too?',
        'Rafael asks with a stammer whether what happened was also one of Sanghyeon’s techniques.',
        'Keep Rafael’s surprise at the dream visit and his connection to the arts Yifa just mentioned.',
        ('Th-that was', 'one of them too?')),
    (184, 15): ('Rafael', 'People like him are everywhere, huh?',
        'Rafael observes that people like Julian exist in every country.',
        'Keep the quiet aside after Julian’s lavish compliment and before he notices Mihwa is distracted.',
        ('People like him', 'are everywhere, huh?')),
    (184, 66): ('Mihwa', "I'm counting on you... Oh. He's gone already.",
        'Mihwa says she is counting on Julian, then notices he has already left.',
        'Play the unfinished farewell before the realization. Rafael speaks up immediately afterward.',
        ("I'm counting on you...", "He's gone already.")),
    (184, 93): ('Mihwa', "I'd be happy to get it from you, too. Aren't I worth a present?",
        'Mihwa would be happy to get the item from them too, and teasingly asks if she is worth a gift.',
        'Keep the invitation and the teasing challenge that makes Claudio unwilling to back out.',
        ("get it from you, too.", "Aren't I worth a present?")),
    (184, 99): ('Rafael', "(Clau's easy to talk into things.) All right, let's look for it together. You said Seoul, right?",
        'Rafael thinks Claudio is easy to persuade, agrees they should all look for it, and confirms the location.',
        'Keep the private aside, group decision and question, followed by Mihwa’s qualified confirmation.',
        ("Clau's easy to talk into things.", "let's look for it together.", 'You said Seoul, right?')),
    (185, 28): ('Reika', 'Is the Silla Gold Crown in fashion? Someone just asked me about it.',
        'Reika jokes that searching for the Silla Gold Crown must be in fashion because someone else just asked her.',
        'Keep the item name and the witty question. Claudio immediately suspects Julian.',
        ('Silla Gold Crown', 'in fashion?', 'Someone just asked me')),
    (186, 99): ('Mihwa', 'They beat you to it this time, Julian.',
        'Mihwa observes that the group got there before Julian this time.',
        'Keep the familiar tease before Julian turns his defeat into another declaration of affection.',
        ('beat you to it', 'this time, Julian.')),
    (186, 125): ('Julian', "How'd you find the Silla Gold Crown so fast?",
        'Julian asks how they found the Silla Gold Crown so quickly.',
        'Keep his curiosity and the item name as Claudio explains the time saved by taking a ship.',
        ('the Silla Gold Crown', 'so fast?')),
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

