"""Review Hodram's artifact, diplomacy, and crew exchanges in blocks 100–171."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_hodram_opening_wraps_20261114 as parent
from scripts import stage_hodram_opening_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
PRIOR_ROOT = Path('work/hodram_rumor_wraps_20261114_v1')
ROOT = Path('work/hodram_rumor_wraps_20261114_v3')
CAPTURE = PRIOR_ROOT / 'hodram_startup/capture_report.json'
RUNTIME = ROOT / 'hodram_native_context.json'
REVIEW = parent.TRIAGE.with_name('hodram_rumor_wraps_context_v3.json')
PROOF = ROOT / 'stored_and_native.json'

DECISIONS = {
    (100, 38): ('Port Worker', "A few islands lie off this cape. They say there's a strange spot on one that glows like amber.",
        'Several islands lie off the cape, and one reportedly has a strange amber-colored glow.',
        'Keep the islands, color and hearsay. Charles wonders whether a mineral vein produces the glow.',
        ('A few islands lie off this cape.', 'a strange spot', 'glows like amber.')),
    (101, 24): ('Hodram', "Don't worry about Cristina. She's more capable than most men. She's like Athena reborn...",
        'Hodram reassures Julio about Cristina, praises her ability above most men, and compares her with Athena.',
        'Keep the comparison that puzzles Julio and leads to the Roman name.',
        ("Don't worry about Cristina.", "She's more capable than most men.", "She's like Athena reborn...")),
    (101, 31): ('Hodram', "The Romans called her Minerva.",
        'Hodram identifies Athena with Minerva in Roman mythology.',
        'Keep the mythological name and short clarification before Julio says he knows little about the gods.',
        ('called her Minerva.',)),
    (103, 35): ('Samwell', "Tracking them down takes real work. I'm bored with it already.",
        'Samwell finds tracking these things down difficult and has grown bored.',
        'Keep the abrupt change of interest. He immediately explains how quickly his enthusiasms fade.',
        ('takes real work.', "I'm bored with it already.")),
    (104, 20): ('Janus', "They say Aristarchus made it. A brilliant astronomer of the Hellenistic age...",
        'Janus attributes the object to Aristarchus, a brilliant astronomer of the Hellenistic period.',
        'Keep the maker, period and attribution as hearsay before Hodram asks whether it is true.',
        ('Aristarchus made it.', 'the Hellenistic age...')),
    (105, 11): ('Emilio', None,
        'Emilio insists that eating matters and adds that he is looking for something.',
        'Keep the earnest defense and mystery. Hodram asks what he is searching for.',
        ('Eating is important!', "Besides, I'm looking for something.")),
    (105, 23): ('Hodram', "Best food in the world? Who decides? How could you judge that?",
        'Hodram questions who judges the best food in the world and how it can be judged.',
        'Keep his skeptical questions before Emilio declares that Hestia’s Pot provides the answer.',
        ('Best food in the world?', 'Who decides?', 'How could you judge that?')),
    (108, 16): ('Yukihisa', "What an eerie glow... It feels as if it could draw me in.",
        'Yukihisa describes the blade’s uncanny light as almost drawing him inside.',
        'Keep his lingering fascination with Muramasa between the recognition and his formal closing.',
        ('What an eerie glow...', 'it could draw me in.')),
    (110, 5): ('Priest', "Do you seek the Proof of Conquest?",
        'The priest wonders whether they are seeking the Proof of Conquest.',
        'Keep the formal verb and the full title as a question before the group’s silence.',
        ('the Proof of Conquest?',)),
    (110, 23): ('Hodram', "What is this Proof of Conquest?",
        'Hodram asks what the Proof of Conquest is.',
        'Keep the full term intact before the priest explains its meaning.',
        ('this Proof of Conquest?',)),
    (111, 19): ('Donna', "Why not go while you're in Seville? I'll show you the way.",
        'Donna suggests visiting during the stop in Seville and offers directions.',
        'Keep it an invitation after the pilgrimage site’s reputation rather than a requirement.',
        ("while you're in Seville?", "I'll show you the way.")),
    (115, 50): ('Gerhard', "Get the villagers to safety at once!",
        'Gerhard urgently proposes evacuating the people in the village.',
        'Keep the immediate call to protect the villagers before Hodram orders the expedition to prepare.',
        ('to safety at once!',)),
    (121, 110): ('Mysterious Old Man', "I don't know where it came from. I'm told it's worth quite a bit.",
        'He does not know the object’s origin but has heard it is valuable.',
        'Keep his uncertainty and the reported value before Hodram hesitates to accept the reward.',
        ("I don't know where it came from.", "worth quite a bit.")),
    (123, 92): ('Maria', "If you hate all Europeans and attack without distinction, you're just as guilty as the brutes you fight.",
        'Maria says hating all Europeans and attacking without distinction makes them as guilty as the brutal people they oppose.',
        'Keep her distinction between the men who committed the abuses and everyone else. The bandit immediately bristles.',
        ('hate all Europeans', 'attack without distinction,', "as guilty as the brutes")),
    (123, 107): ('Bandit', "Th-then what are we supposed to do?!",
        'The bandit hesitates and challenges Maria to say what they should do.',
        'Keep the stammer before Maria answers with a political goal.',
        ('what are we supposed to do?!',)),
    (123, 110): ('Maria', "The European powers' rivalry has caused fighting on seas all over the world. That struggle has to end.",
        'Maria says the rivalry between the European powers causes conflict on the world’s seas and must end.',
        'Preserve the cause and the proposed action as her direct answer to the bandit.',
        ("The European powers' rivalry", 'seas all over the world.', 'That struggle has to end.')),
    (123, 149): ('Bandit', "All right. I'll take a chance on you!",
        'The bandit decides to bet on Maria.',
        'The existing expression works as a tentative commitment after he gives up staying. Keep that commitment together.',
        ("I'll take a chance on you!",)),
    (129, 20): ('Diogo', "I'm afraid these waters are closed to trade. Leave at once.",
        'Diogo says nobody is allowed to trade in this region and commands them to leave.',
        'Keep the universal restriction and his formal dismissal before Hodram disputes Diogo’s authority.',
        ('are closed to trade.', 'Leave at once.')),
    (129, 108): ('Diogo', "You've outlived your usefulness. Now get out of my sight!",
        'Diogo says they have outlived their usefulness and must leave.',
        'Keep his contempt after the grudging thanks and turn it into a direct dismissal.',
        ("you've outlived your usefulness.", 'Get out of my sight!')),
    (131, 9): ('Hodram', "Where did that come from? Befriending women at taverns isn't why we sail.",
        'Hodram asks why Julian brought up friendly tavern acquaintances, then says that is not the purpose of their voyage.',
        'Keep his dry surprise and the distinction between the voyage and social visits. Julian explains their knowledge next.',
        ('Where did that come from?', 'Befriending women at taverns', "isn't why we sail.")),
    (132, 68): ('Charles', "Do we need an unscientific relic to prove our actions are right?",
        'Charles questions whether an unscientific object is needed to establish that their actions are right.',
        'Keep his scientific skepticism and moral objection before Gerhard asks if he was listening.',
        ('an unscientific relic', 'our actions are right?')),
    (132, 83): ('Charles', "Why care what anyone else thinks? As long as we stay on the course we believe is right, that's enough.",
        'Charles says outsiders’ opinions should not matter if the crew pursues what they believe is right.',
        'Keep the principle and the sailing metaphor before he asks Gerhard why he needs everyone’s agreement.',
        ('what anyone else thinks?', 'we believe is right,', "that's enough.")),
    (132, 110): ('Hodram', "You're right. If we follow the course we believe is right, we have no need of it.",
        'Hodram agrees the relic is unnecessary while they follow what they believe is the right course.',
        'Echo Charles’s words to make the agreement audible before Charles affirms it.',
        ("You're right.", 'the course we believe is right,', 'we have no need of it.')),
    (132, 133): ('Gerhard', "No harm done. Keep that honesty.",
        'Gerhard accepts Charles’s apology and encourages his frankness.',
        'Keep the older officer’s encouraging response before he asks Charles to come with him.',
        ('Keep that honesty.',)),
    (140, 23): ('Diogo', "It's quite all right. I'd like a word with you.",
        'Diogo quiets the confrontation and says he has something to discuss with the group.',
        'Keep his restraint after the other man’s threat and before Hodram asks why Diogo chose him.',
        ("It's quite all right.", "I'd like a word with you.")),
    (142, 8): ('Hodram', "What's wrong? There's no need to worry. They won't seize you while you're in this town. Even slave traders won't break the law in public.",
        'Hodram reassures the frightened girl that she will not be seized in town because even slave traders avoid breaking the law in public.',
        'Keep the reassurance specific to the town and the public setting he is relying on.',
        ("What's wrong?", "There's no need to worry.", "They won't seize you", "in this town.", 'break the law in public.')),
    (142, 54): ('Gerhard', "In public, he's a powerful man who controls most of Africa's trade. We've made ourselves a dangerous enemy.",
        'In public the man has power over most African trade, and Gerhard says they have made a dangerous enemy.',
        'Keep the contrast with Gerhard’s allegations and Hodram’s judgment that he is too powerful to challenge now.',
        ('In public,', "most of Africa's trade.", 'a dangerous enemy.')),
    (142, 233): ('Hodram', "Good, you understand! I'm {MACRO:FI}. What's your name?",
        'Hodram thinks she understands him, gives his name, and asks her name.',
        'Keep the pleasure and direct language of the teaching exchange. The other speaker is still learning the language.',
        ('Good, you understand!', "I'm {MACRO:FI}.", "What's your name?")),
    (146, 9): ('Gerhard', "How do we use the leaf with the Kushan Platter? I haven't a clue.",
        'Gerhard has no idea how the leaf and the Kushan Platter are to be combined.',
        'Keep the item name whole before Hodram proposes floating the leaf in water.',
        ('use the leaf', 'the Kushan Platter?', "I haven't a clue.")),
    (148, 32): ('Gerhard', "Shall we soak it in the Lotion Jar?",
        'Gerhard proposes dipping the item in the Lotion Jar.',
        'Keep the suggestion and exact item label. Charles offers the same method in the alternate reply.',
        ('in the Lotion Jar?',)),
    (150, 60): ('Julian', None,
        'Julian reacts with delight and says he loves this sort of work.',
        'Keep the spontaneous enthusiasm and reflow the thought before Charles discovers the markings.',
        ('I love this sort of thing!',)),
    (151, 5): ('Hodram', "The Ceremonial Knife and the Sun-Crest Sheath... Their sizes match so closely it's uncanny. They seem to belong together.",
        'Hodram finds the two items’ matching sizes uncanny and thinks they look like a set.',
        'Keep both item labels and the deduction supported by Gerhard’s reply.',
        ('The Ceremonial Knife', 'the Sun-Crest Sheath...', 'They seem to belong together.')),
    (154, 5): ('Hodram', "The Patterned Cloth... It must be a map to the Mediterranean Proof of Conquest, but...",
        'Hodram recognizes the cloth as a map to the Mediterranean Proof of Conquest but hesitates.',
        'Use the regular name for the same seven regional Proofs. Gerhard says the cloth has yet to look like a map.',
        ('The Patterned Cloth...', 'Proof of Conquest, but...')),
    (156, 14): ('King', "I name you supreme naval commander. May our navy prosper under you.",
        'The king appoints Hodram the highest-ranking naval commander and expects the navy to develop and achieve more.',
        'Keep the appointment, future expectation and rank Hodram repeats to himself.',
        ('supreme naval commander.', 'our navy prosper under you.')),
    (156, 22): ('Charles', "(The ideal post for the admiral!)",
        'Charles privately says the appointment suits Hodram perfectly.',
        'Keep the aside and the rank Charles addresses him by.',
        ('for the admiral!)',)),
    (157, 5): ('Guildmaster', "Go wherever the hell you want! You're too much trouble. You're fired!",
        'The man tells Al to go wherever he likes and fires him for being difficult to employ.',
        'Keep the escalating anger and explicit dismissal before Al dismisses it in turn.',
        ('Go wherever the hell you want!', "You're fired!")),
    (157, 90): ('Al', "We just met! What's the hurry?",
        'Al says they have only just met and calls Hodram impatient.',
        'Keep the surprise and pointed question before Hodram defends being decisive.',
        ("What's the hurry?",)),
    (159, 112): ('Barkeep', "Sorry, but I have to let you go.",
        'The barkeep reluctantly dismisses Ian.',
        'Keep the regret and plain dismissal after he says a sword is the wrong way to deal with customers.',
        ('I have to let you go.',)),
    (159, 197): ('Hodram', "No need to thank us. I have a favor to ask. It calls for a swordsman like you.",
        'Hodram says thanks are unnecessary and asks a favor because he trusts Ian’s swordsmanship.',
        'Keep the reason for approaching Ian before he asks what he can do.',
        ('No need to thank us.', 'a swordsman like you.')),
    (160, 93): ('Carlo', "Most people wouldn't notice. I can usually tell when someone's unwell.",
        'Carlo says ordinary observers would miss it because he is sensitive to others’ physical condition.',
        'Specify health, which explains his remark about the man Hodram thought looked well.',
        ("Most people wouldn't notice.", "someone's unwell.")),
    (160, 141): ('Carlo', "Thank you, ma'am. In a hurry, travelers? Go ahead and shop first.",
        'Carlo thanks the woman, then asks whether the travelers are in a hurry and lets them shop first.',
        'Name the change of addressee so the invitation to shop goes to the crew.',
        ("Thank you, ma'am.", 'In a hurry, travelers?', 'Go ahead and shop first.')),
    (160, 208): ('Hodram', "You don't want to leave? Is it your children?",
        'Hodram asks whether Carlo objects to leaving and guesses he does not want to part from his children.',
        'Keep children as Hodram’s guess before Carlo reveals his family died.',
        ("You don't want to leave?", 'Is it your children?')),
    (162, 14): ('Samwell', "Oh! You're not my usual customers. You're travelers, right?",
        'Samwell finds the customers unusual and guesses that they are travelers.',
        'Keep his sudden change from selling goods to sizing up the crew as potential traveling companions.',
        ('usual customers.', "You're travelers, right?")),
    (162, 17): ('Samwell', "Perfect! Take me with you! I'm sick of looking at elephants. I want to see other countries. How about it?",
        'Samwell asks to join them because he is tired of seeing elephants and wants to see other countries.',
        'Keep the blunt reason alongside his eagerness. Hodram responds by asking about his skills.',
        ('Take me with you!', 'looking at elephants.', 'other countries.', 'How about it?')),
    (163, 24): ('Charles', "Science says no! Physically impossible!",
        'Charles rejects a ship vanishing as scientifically and physically impossible.',
        'Keep both objections and his agitation before the sailor insists it happened.',
        ('Physically impossible!',)),
    (166, 88): ('Jam', "Where there's a will, there's a way! Yahoo! It's OK if I say it's OK!",
        'Jam quotes a proverb, lets out a cheer and declares his own approval sufficient.',
        'Keep the refrain and brash self-approval consistent with the parallel Rafael speech.',
        ("Where there's a will,", "It's OK if I say it's OK!")),
    (167, 125): ('Cesare', "Once your market share lets you buy more goods, it's time to buy a ship.",
        'Cesare advises buying a ship when a larger share lets them buy more trade goods.',
        'Keep the causal threshold and match the corresponding advice in Rafael’s tutorial.',
        ('your market share', 'buy more goods,', "it's time to buy a ship.")),
    (168, 225): ('Claudio', "I looked. It's carved there! I can't believe it!",
        'Claudio reports having looked and can scarcely believe the mark was actually carved there.',
        'Keep the report and the surprise before Cesare asks about the mark.',
        ('I looked.', "It's carved there!", "I can't believe it!")),
    (169, 16): ('Fernando', "New here, huh? Care to bet a drink? It's a simple game.",
        'Fernando greets a newcomer and proposes a simple game with a drink at stake.',
        'Keep the friendly wager and its unit. He explains the coin-taking rules next.',
        ('Care to bet a drink?', "It's a simple game.")),
    (169, 96): ('Fernando', "That's easy. They're breaking up.",
        'Fernando thinks the signs are obvious and says the couple is breaking up.',
        'Give him the same confident prediction as in Rafael’s parallel encounter.',
        ("They're breaking up.",)),
    (169, 111): ('Man', "Think what you like. So are you.",
        'The man tells her to think what she likes and returns the accusation of selfishness.',
        'Keep the dismissive first sentence and echo her accusation directly before she ends the relationship.',
        ('Think what you like.', 'So are you.')),
    (169, 132): ('Fernando', "She had her fist clenched under the table. She was holding back her anger. That's no way to talk about love.",
        'Fernando points to her clenched fist as evidence she was holding back anger, a posture at odds with talk of love.',
        'Keep the physical observation, inference and punch line before he points out the man’s averted gaze.',
        ('under the table.', 'holding back her anger.', 'talk about love.')),
    (169, 140): ('Hodram', "I see... You have a sharp eye.",
        'Hodram acknowledges that Fernando’s powers of observation are exceptional.',
        'Keep the admiring reply after Fernando explains the clues. Fernando goes on to apply that insight to gambling.',
        ('You have a sharp eye.',)),
    (170, 48): ('Hodram', "If the drink's so bad, why drink it?",
        'Hodram asks why Julio drinks the liquor if he dislikes it.',
        'Keep the dry retort to Julio’s complaint, setting up his saying about making do.',
        ('why drink it?',)),
    (170, 181): ('Julio', "Don't lie to me! Don't play dumb on account of my age. Come on, out with it!",
        'Julio objects to lies and demands that they stop playing dumb and tell him, despite his age.',
        'Keep his stubbornness and familiar challenge before Hodram admits they already plan to look.',
        ("Don't lie to me!", "Don't play dumb", 'on account of my age.', 'out with it!')),
    (170, 196): ('Julio', "Ho ho ho! Surprised, are you? I'm a man of the sea. Still going strong!",
        'Julio laughs, asks why they are surprised, and says he is a man of the sea who is still active.',
        'Keep the laugh and the emphatic claim before he offers to make himself useful.',
        ('a man of the sea.', 'Still going strong!')),
    (171, 78): ('Shipwright', "Triangular sails are lateen sails. They're rigged fore and aft. Unlike square sails, they can't turn crosswise.",
        'The shipwright says sailors call triangular sails lateen sails and explains that fore-and-aft rigging prevents them turning across the ship.',
        'Keep the name and contrast with the square sail for the next line about upwind and downwind performance.',
        ('Triangular sails are lateen sails.', 'rigged fore and aft.', 'Unlike square sails,', 'turn crosswise.')),
    (171, 98): ('Shipwright', "We call the stern sail a jigger spanker. We rig it fore and aft. It needs its own small mast. So only big ships can carry it.",
        'The stern sail is also called a jigger spanker. It is fore-and-aft and needs the equivalent of a small additional mast, so only large ships can use it.',
        'Preserve the game’s established sail label and the mechanical reason it requires a large ship.',
        ('a jigger spanker.', 'We rig it fore and aft.', 'its own small mast.', 'So only big ships can carry it.')),
}

get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())
compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': previous.initial_names})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())


def native_runner(runtime):
    prior_proof = PRIOR_ROOT / PROOF.name
    prior_review = REVIEW.with_name('hodram_rumor_wraps_context_v1.json')
    proof, review = map(base.load, (prior_proof, prior_review))
    assert base.digest(prior_review) == proof['review_sha256']
    receipt = runtime.receipt()
    assert proof['candidate_sha256'] == receipt['candidate_sha256']
    for field in ('ARM9_sha256', 'COMMON_sha256', 'snapshot', 'captain'):
        assert proof['native_runtime'][field] == receipt[field]
    cache = {}
    for row in review['records']:
        for label, raw_field in (('before', 'current_hex'), ('after', 'target_hex')):
            body = bytes.fromhex(row[raw_field])[1:]
            item = row[f'{label}_native']
            assert all(sha(bytes.fromhex(page['native_plane_hex'])) == page['plane_sha256'] for page in item['pages'])
            cache[row['source_selector'], body] = item
    counts = {'fresh_processor_alignments': 0, 'reused_processor_alignments': 0}

    def render(ctx, selector, body, paint=None):
        if paint is None:
            return previous.native(ctx, selector, body)
        item = cache.get((selector, body))
        if item is None:
            counts['fresh_processor_alignments'] += 4
            return previous.native(ctx, selector, body, paint)
        counts['reused_processor_alignments'] += 4
        return item

    dependencies = {str(path): base.digest(path) for path in (prior_proof, prior_review)}
    return render, counts, dependencies


source = checked_text(getsource(previous.main), {
    '    runtime = bind_runtime()': '    runtime = bind_runtime()\n    native, counts, reused = native_runner(runtime)',
    'verified_default_name_expansion=default, native_runtime=runtime.receipt()))':
        'verified_default_name_expansion=default, native_runtime=runtime.receipt(),\n'
        '        exact_render_reuse_dependencies=reused, **counts))',
})
env = previous.main.__globals__ | globals()
exec(compile(source, __file__ + '::fresh-changed-pages-and-exact-prior-reuse', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
