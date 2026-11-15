"""Review Rafael's early confrontations, Aziza's recruitment and artifact rumors."""

import argparse
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_port_wraps_20261114 as parent
from scripts import stage_rafael_port_wraps_20261114 as previous


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_history_wraps_20261114_v2')
CAPTURE = Path('work/rafael_history_wraps_20261114_v1/rafael_startup/capture_report.json')
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_history_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'


DECISIONS = {
    (0, 5): ('Rafael', None,
        'Rafael recognizes the Proof of Conquest for the African region, with awe.',
        'Keep the discovery and established title before the crew realizes they need all seven. Break before the full item title so it reads as a unit.',
        ('Proof of Conquest...!',)),
    (1, 58): ('Rafael', "Then how about Clau's cabin?",
        'Rafael teases Claudio by suggesting putting the object in his cabin.',
        'Keep the nickname and playful proposal. Clau instantly drops the bravado and pleads with him.',
        ("Clau's cabin?",)),
    (9, 36): ('Claudio', "Hey! Nobody told me they had ironclad warships!",
        'Claudio is alarmed to discover the enemy has warships covered in iron armor.',
        'Use the direct nautical description in Claudio’s startled outburst, after the others marvel at the ships.',
        ('ironclad warships!',)),
    (9, 45): ('Claudio', "How can you be so calm? Ah, talk won't help. Come on, get ready for a fight!",
        'He rebukes Rafael for being so unhurried, then dismisses talk and gets them ready to fight.',
        'Keep the jump from incredulity to action so Rafael’s objection to attacking first follows naturally.',
        ('How can you be so calm?', "talk won't help.", 'get ready for a fight!')),
    (14, 14): ('Rafael', "Playing dumb won't help. You're going back to Hamburg, whether you like it or not!",
        'Rafael dismisses the denial and tells the fugitive he will be sent back to Hamburg by force.',
        'Keep Rafael’s existing threat and the fugitive’s destination. Wrap the forced return as a complete phrase.',
        ("Playing dumb won't help.", "You're going back to Hamburg,", 'whether you like it or not!')),
    (15, 17): ('Julian Vermeer', "Glug, glug... Ahh! Hah! What's my country got to do with making money? Cross me and you'll regret it!",
        'Julian swigs his drink, scoffs at the appeal to his homeland and threatens anyone who interferes.',
        'Keep the sounds and contempt up front, then let his response turn into a threat.',
        ("What's my country", 'got to do with making money?', "Cross me and you'll regret it!")),
    (17, 6): ('Rafael', "Peralonso Aguirre! You're suspected of spying. You're coming to Malacca's guild!",
        'Rafael names Peralonso and says he will take him to the Malacca guild on suspicion of espionage.',
        'Keep the charge provisional and its destination specific. Peralonso immediately answers with a boast.',
        ('Peralonso Aguirre!', "You're suspected of spying.", "You're coming to Malacca's guild!")),
    (19, 6): ('Rafael', "So you're Zaganos Bey. You've got a powerful fleet, but ours is a match for it.",
        'Rafael identifies Zaganos Bey, acknowledges his fleet’s strength and says their own can match it.',
        'Keep Rafael’s measured challenge and Zaganos’s full name before the latter threatens him.',
        ("So you're Zaganos Bey.", "You've got a powerful fleet,", 'ours is a match for it.')),
    (20, 28): ('Julio', "It's one thing after another...",
        'Julio comments wearily that one trouble keeps coming after the next.',
        'Keep his dry understatement between Claudio’s alarm and the next panicked outburst.',
        ("It's one thing after another...",)),
    (24, 60): ('Vels', "That's exactly what I can't stand! You're a lion, all right. An old lion whose time has passed!",
        'Vels snaps that he cannot stand Gerhard’s teachings and calls him an old, outdated lion.',
        'Keep both beats of the lion insult before Vels explains that he takes whatever he wants.',
        ("what I can't stand!", "You're a lion, all right.", 'An old lion', 'whose time has passed!')),
    (26, 232): ('Aziza', None,
        'Aziza answers that her father was a pirate, making her a pirate’s daughter.',
        'Keep the existing blunt repetition and opening hesitation. Her next turn explains what she learned from his crew.',
        ('My father was a pirate.', "I'm a pirate's daughter.")),
    (26, 259): ('Aziza', "So when I found out you had his sword, I had to have it. I thought...",
        'Aziza says she was determined to get the sword when she learned they had it, then trails off.',
        'Keep the unfinished explanation. Rafael’s silence leaves her room to explain what the sword meant to her.',
        ('when I found out', 'you had his sword,', 'I had to have it.', 'I thought...')),
    (26, 283): ('Aziza', None,
        'Aziza realizes she was after her father, and says she means to give up piracy.',
        'Keep the existing parallel wording and short final declaration. Rafael offers her a place with his crew immediately after.',
        ("I wasn't chasing a pirate's life.", 'I was chasing my father.', "I'm leaving that life behind.")),
    (34, 12): ('Rafael', "Not so fast. People in Genoa hate you a lot more than I do. They're waiting for you.",
        'Rafael refuses the demand to kill the man and says he is awaited by people in Genoa who hate him much more.',
        'Keep Rafael’s refusal and pointed reminder. Let the last sentence land plainly.',
        ('People in Genoa', 'more than I do.', "They're waiting for you.")),
    (36, 39): ('Janus', None,
        'Janus says they cannot avoid a fight if the fleet belongs to pirates.',
        'Keep his sober assessment between Claudio’s guess and Julio’s identification of the Algiers pirates. The conditional pause leaves the full consequence together on the second line.',
        ("we won't be able to avoid a fight.",)),
    (37, 276): ('Barbarossa', None,
        'Barbarossa allows for exceptions to his offer of help, pointing out that he is a busy man.',
        'Keep the casual qualification and the dry tag after Rafael’s surprise, before the territorial warning.',
        ("Don't count on it every time.", "I'm a busy man, you know.")),
    (37, 338): ('Claudio', "Heh. Maybe pressure suits you.",
        'Claudio suggests Rafael may be the sort who performs well when it counts.',
        'Keep the fond teasing after Rafael admits he only feels frightened now that the negotiation is over.',
        ('Maybe pressure suits you.',)),
    (41, 43): ('Rafael', "Or... becoming a capable seafarer?",
        'Rafael wonders if the required strength might mean becoming a fully capable seafarer.',
        'Keep his tentative question in the exchange about fleet strength, seamanship, wealth, and trade.',
        ('a capable seafarer?',)),
    (233, 29): ('Shopkeeper', "Hmph. You've heard about the chivalrous knights who fought to retake the Holy Land, right?",
        'The shopkeeper scoffs at the listener knowing the Crusaders as knights who valued chivalry and fought to reclaim the Holy Land.',
        'Keep this as the account he challenges. The shopkeeper follows it with the town’s very different recollection.',
        ('chivalrous knights', 'the Holy Land, right?')),
    (234, 42): ('Gerhard', "A small country in the East, yet it produced a man of such courage. I feel as though I've seen the very spirit of the East.",
        'Gerhard marvels that a man with such courage lived in this small eastern country and says he feels he has seen the essence of the people of the East.',
        'Keep the speaker’s period perspective and admiration. Rafael calls the feat incredible and notices how deeply it moved Gerhard.',
        ('a small country in the East,', 'a man of such courage.', "I feel as though I've seen", 'the very spirit of the East.')),
    (234, 55): ('Rafael', "It really moved you, didn't it, Gerhard?",
        'Rafael observes that the story had a strong emotional effect on Gerhard.',
        'Use the specific emotional reaction after Gerhard remarks on the rarity of men like him.',
        ('really moved you,', "didn't it, Gerhard?")),
    (236, 26): ('Julian', "The Medusa Shield is said to be in the Tasman Sea. I had the story on my mind. Your eyes brought it right back.",
        'Julian says her eyes brought back a story he had heard about the Medusa Shield in the Tasman Sea.',
        'Keep the artifact, rumor and connection to her eyes. Her next turn takes the comparison the wrong way.',
        ('the Medusa Shield', 'in the Tasman Sea.', 'I had the story on my mind.', 'Your eyes brought it right back.')),
    (237, 28): ('Gerhard', "He repelled a Muslim army near here, between Tours and Poitiers. It had invaded Iberia and was pushing north.",
        'Gerhard says Charles Martel repelled a Muslim army between Tours and Poitiers after it invaded the Iberian Peninsula and advanced north.',
        'Put the victory and its location together and retain the direction of the army’s advance. Rafael asks why this particular victory matters.',
        ('between Tours and Poitiers.', 'a Muslim army', 'had invaded Iberia', 'was pushing north.')),
    (237, 36): ('Gerhard', None,
        'Gerhard replies that the significance of the victory is what matters.',
        'Keep his succinct response to Rafael’s question and keep the clause about the victory intact before his explanation.',
        ('what his victory meant.',)),
    (238, 13): ('Manuel', "Checking the latest fashions, Admiral? You're always so busy.",
        'Manuel asks if the admiral is keeping an eye on trends and remarks how busy he is.',
        'Keep the courteous small talk prompting Rafael to say he is simply enjoying the town.',
        ('the latest fashions,', "You're always so busy.")),
    (238, 62): ('Manuel', "I just heard about a suit of armor tied to King Attila. It's only a rumor, mind you.",
        'Manuel says he has just heard a tale about armor associated with King Attila and qualifies it as rumor.',
        'Keep the title and the caveat. This sets up Rafael asking what Manuel heard.',
        ('a suit of armor', 'King Attila.', "It's only a rumor, mind you.")),
    (239, 27): ('Yifa', "With something like that, I could really go all out...",
        'Yifa imagines fighting with much less restraint if she had the protective outfit.',
        'Keep her moment of enthusiasm before she remembers her teacher’s warning about relying on gear.',
        ('With something like that,', 'really go all out...')),
    (242, 42): ('Rafael', "Where is it, anyway? It's not somewhere around Africa or India again, is it?",
        'Rafael asks where it might be and suspects another vague lead in the vicinity of Africa or India.',
        'Keep the callback to Samwell’s broad clues and keep the tag intact before his more precise answer.',
        ('Where is it, anyway?', "It's not somewhere", 'Africa or India', 'again, is it?')),
    (242, 47): ('Samwell', None,
        'Samwell brushes off the suggestion and says the helmet is in Britain.',
        'Keep the mock indignation and put the short reply about Britain together before Rafael’s surprise.',
        ("It's in Britain.",)),
    (242, 68): ('Rafael', "After all your hard work, Samwell, I won't forget about the Phoenix Bascinet.",
        'Rafael promises to remember the Phoenix Bascinet in recognition of Samwell’s effort.',
        'Keep Rafael’s encouragement and the established item name before Samwell hopes they find it.',
        ('all your hard work, Samwell,', "I won't forget", 'the Phoenix Bascinet.')),
    (248, 42): ('Jam', "Trouble is, I can't find anyone who's selling it or who's even seen it.",
        'Jam has found neither a seller nor anybody who claims to have seen the statue.',
        'Keep his informal turn from betting scheme to practical hurdle before he proposes Rafael look for it.',
        ('Trouble is,', "who's selling it", "who's even seen it.")),
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
