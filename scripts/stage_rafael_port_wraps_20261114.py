"""Review flagged wraps in Rafael's port and artifact exchanges."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_seamanship_wraps_20261114 as parent
from scripts import stage_rafael_seamanship_wraps_20261114 as previous


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_port_wraps_20261114_v2')
CAPTURE = Path('work/rafael_port_wraps_20261114_v1/rafael_startup/capture_report.json')
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_port_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'

DECISIONS = {
    (195,42): ('Shipwright', "I'll take one by this artist!",
        'A buyer wants a piece by the artist who painted the work he points to.',
        'Keep the competitive interruption and the choice of artist before the next buyer selects a particular piece.',
        ("take one by this artist!",)),
    (195,83): ('Sailor', "Ha ha! You don't mince words, do you?",
        'The sailor laughs at the shopkeeper’s blunt remark about the buyers.',
        'Keep the laugh and the amused tag together before the shopkeeper asks him to keep it quiet.',
        ("You don't mince words, do you?",)),
    (199,24): ('Shopkeeper', "I heard there's a good remedy.",
        'The speaker has heard of an effective remedy for the illness.',
        'Keep it a rumor. The other speaker coughs and asks what it is called, prompting the clue about almonds.',
        ("there's a good remedy.",)),
    (200,14): ('Daimyo', "A piece this fine must be the work of a master craftsman.",
        'The daimyo assumes such a fine piece must have been made by a renowned craftsperson.',
        'Keep his admiration and inference after he calls it a work of art. The attendant agrees.',
        ('the work of', 'a master craftsman.')),
    (203,64): ('Sailor', "What are you waiting for? Once it's gone, it's too late.",
        'The sailor objects to waiting because it will be too late once the item sells out.',
        'Keep the impatient pushback. The shopkeeper immediately doubts that it will sell out so soon.',
        ('What are you waiting for?', "Once it's gone,", "it's too late.")),
    (204,16): ('Port Worker', "Really? It's all the rage! You must be the only one in town who hasn't tried it.",
        'The speaker is surprised and says the other man is probably the only person in town who has not smoked it.',
        'Keep the teasing exaggeration and the trend that makes the other man curious.',
        ("It's all the rage!", 'the only one in town', "who hasn't tried it.")),
    (206,49): ('Julio', "No time to stand around! I'm off to buy some of that sake right now!",
        'Julio insists they must act at once and goes to buy the sake he has just heard about.',
        'Keep his sudden enthusiasm and the urgency that makes Rafael call after him.',
        ('No time to stand around!', "I'm off to buy", 'that sake right now!')),
    (208,202): ('Shady Man', None,
        'The seller compliments the successful negotiator and hands over the item.',
        'Keep the grudging compliment before the transaction. The dealer’s next remark shows what he thinks of the price.',
        ("You're pretty good at this.", "Here's the item.", 'Go on, take it.')),
    (208,314): ('Shady Man', "Forget it. I'll sell it elsewhere!",
        'The dealer ends the negotiation and says he will sell to someone else.',
        'Let him dismiss the buyer outright after saying they have no eye for the item.',
        ("I'll sell it elsewhere!",)),
    (213,91): ('Rafael', "No need to replace rope that's still good.",
        'Rafael sees no reason to replace rope that is still usable.',
        'Keep his practical decision. Carlo offers to turn the seller down, and the seller gets angry.',
        ("that's still good.",)),
    (214,47): ('Rafael', "Someone shoved this into my hands.",
        'Rafael says someone forced the object into his hands.',
        'Keep the abrupt explanation before Charles asks what it is and Rafael recognizes a book.',
        ('shoved this into my hands.',)),
    (215,52): ('Mysterious Old Man', "That's right. Here, it's yours.",
        'The old man answers yes and offers the object to Rafael.',
        'Keep the plain offer. The next exchange clarifies that the object is a book about medicinal ingredients.',
        ("Here, it's yours.",)),
    (216,38): ('Rafael', "Huh... Anyway, we're leaving. Hurry up and get ready.",
        'Rafael lets the matter drop and tells Jam to get ready to leave.',
        'Keep the move from bemusement to a practical instruction. Jam asks him to wait a minute.',
        ("we're leaving.", 'Hurry up and get ready.')),
    (218,55): ('Shady Man', "Get on good terms, and you'll hear all sorts of things. The women at the tavern know what's going on.",
        'The seller says being on friendly terms brings useful information because the tavern women are well informed.',
        'Keep the seller’s pitch as his claim and make the information payoff clear after Cristina asks why it matters.',
        ('Get on good terms,', 'all sorts of things.', 'The women at the tavern', "know what's going on.")),
    (218,78): ('Shady Man', "That'll be 9,000 coins. I'm practically giving them away. I won't take a coin less.",
        'The dealer names his price and claims it is a bargain. He rejects even a one-coin discount.',
        'Keep 9,000 and the hard floor. The handover follows if the player accepts.',
        ("That'll be 9,000 coins.", "I'm practically giving", "I won't take a coin less.")),
    (218,103): ('Claudio', "What's with the attitude? You came up to us!",
        'Claudio objects to the dealer’s tone and points out that the dealer approached them first.',
        'Keep both the indignation and the reversal. The dealer doubles down immediately afterward.',
        ("What's with the attitude?", 'You came up to us!')),
    (218,106): ('Shady Man', "Hmph. I don't deal with cheapskates. Now get lost.",
        'The dealer calls the buyers cheap and dismisses them.',
        'Keep his contempt and short dismissal. Claudio says that suits him and leaves.',
        ("I don't deal with cheapskates.", 'Now get lost.')),
    (220,28): ('Mysterious Old Man', "It's the way you carry yourself. Maybe it's because you look strong, too.",
        'The old man sees a likeness in Cristina’s bearing rather than her face and wonders whether it is her apparent strength.',
        'Answer Cristina’s specific question about her face. The uncertainty leaves room for her to take it as encouragement.',
        ('the way you carry yourself.', 'you look strong, too.')),
    (220,44): ('Mysterious Old Man', "Yes, the sword she's said to have used. I don't know what it's worth.",
        'He confirms it is the sword the pirate reportedly used and says he does not know its value.',
        'Keep the attribution and uncertainty. Cristina next asks where the sword is.',
        ("she's said to have used.", "I don't know what it's worth.")),
    (221,27): ('Yukihisa', "Word has reached me of the Muramasa, the legendary cursed blade. It is said to bring ill fortune to Tokugawa, the ruler of Japan. Efforts are under way to destroy these renowned swords.",
        'Yukihisa reports a rumor about the cursed Muramasa, its threat to Tokugawa, and attempts to eradicate the blades.',
        'Keep the letter’s formal register, the report as hearsay and the distinction between the legendary blade and surviving blades of its kind.',
        ('the Muramasa,', 'the legendary cursed blade.', 'ill fortune to Tokugawa,', 'the ruler of Japan.', 'Efforts are under way', 'these renowned swords.')),
    (223,5): ('Cristina', "What a lovely square... Oh? Something's in that little pond. Is that...?",
        'Cristina admires the square, spots something in the pond and trails off.',
        'Keep the gradual discovery before the sound cue and the reveal of the swans.',
        ('What a lovely square...', 'in that little pond.', 'Is that...?')),
    (224,5): ('Guildmaster', "Know Romance of the Three Kingdoms?",
        'The guildmaster asks whether the visitors know Romance of the Three Kingdoms.',
        'Keep the full title as one phrase. The two responses depend on whether the player knows the book.',
        ('Romance of the Three Kingdoms?',)),
    (225,26): ('Mysterious Old Man', "Hmm. There's no mistake. Just as the story says.",
        'The old man confirms what he sees matches the tradition.',
        'Keep his certainty about the match and the story attribution. He explains the tradition in the following turns.',
        ("There's no mistake.", 'Just as the story says.')),
    (225,48): ('Mysterious Old Man', "My family descends from that retainer. We awaited the king of the sea.",
        'The old man’s family descends from the retainer and has waited for the sea king.',
        'Keep both the family connection and the title used in the prophecy. The next line addresses Rafael as the one they awaited.',
        ('descends from that retainer.', 'We awaited', 'the king of the sea.')),
    (226,75): ('Rafael', "Hmm. A traitor's sword... If it's a good blade, Janus doesn't care where it came from. That's just like him.",
        'Rafael reflects that Janus cares about the sword’s quality more than its provenance.',
        'Keep the affectionate observation and the distinction between the traitor and the blade. Manuel gives his own view next.',
        ("A traitor's sword...", "If it's a good blade,", 'where it came from.', "That's just like him.")),
    (227,52): ('Guard', "I brought you word because I thought you could wield such a weapon, Admiral {MACRO:FA}.",
        'The guard tells the admiral because he thought the admiral could handle the rumored weapon.',
        'Keep the cautious estimate and respectful address with the family-name substitution. Manuel then considers where the icy island might be.',
        ('I brought you word', 'you could wield', 'Admiral {MACRO:FA}.')),
    (230,8): ('Rafael', "What kind of weapon? What's it called?",
        'Rafael asks what kind of weapon it is and what it is called.',
        'Keep both questions before Ian names the spear and tells its legend.',
        ("What's it called?",)),
    (230,13): ('Ian', "It's called the Holy Spear of Ares. They say it belonged to Ares, one of the twelve gods of Olympus.",
        'The Holy Spear of Ares is named for the legend that Ares, one of the twelve Olympian gods, owned it.',
        'Keep the item name and attribute the ownership to legend. Rafael still wants to know where it is.',
        ('the Holy Spear of Ares.', 'belonged to Ares,', 'the twelve gods of Olympus.')),
    (230,16): ('Rafael', "Hmm. I still don't see what's so special about it. Where is it?",
        'Rafael is unsure what makes the weapon special and asks where it is.',
        'Keep the mild skepticism and practical follow-up. Ian replies with an indirect clue.',
        ("what's so special", 'Where is it?')),
    (230,36): ('Ian', "Admiral? What's that look for? Surprised I'm interested in legends?",
        'Ian notices Rafael’s expression and asks if his interest in legends is unexpected.',
        'Keep the three beats of notice, question, and inference. Rafael responds candidly, and Ian explains what draws him to the stories.',
        ("What's that look for?", "Surprised I'm interested", 'interested in legends?')),
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

