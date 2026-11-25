"""Review Maria's flagged scene wraps in SC3 blocks 0 through 99."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_lil_final_wraps_20261114 as parent
from scripts import stage_hodram_opening_wraps_20261114 as opening
from scripts import stage_lil_late_wraps_20261114 as template
from scripts import stage_lil_opening_wraps_20261114 as lil
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = template.base, template.sha, template.prior
ARM, CLEAN, IlnkContainer = template.ARM, template.CLEAN, template.IlnkContainer
FILE = '/data/SC3.DK4'
ROOT = Path('work/maria_opening_wraps_20261114_v1')
CAPTURE = ROOT / 'maria_startup/capture_report.json'
RUNTIME = ROOT / 'maria_native_context.json'
REVIEW = parent.TRIAGE.with_name('maria_opening_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
DEFAULTS = {'FI': 'Maria', 'FA': 'Li', 'FO': 'Li Clan'}
initial_names = opening.initial_names


DECISIONS = {
    (4, 33): ("Diogo", "People of the New World will have a country of their own. What a bold, glorious idea!",
        "Diogo proposes a country for the people who live in the New World and praises the idea as wonderful and bold.",
        "Keep his self-congratulation between the appeal against colonial rule and Maria's accusation that he is dressing up his greed.",
        ("the New World", "a country of their own.", "bold, glorious idea!",)),
    (5, 5): ("Aziza", "Look there! That's {MACRO:FO}, the fleet muscling in on our waters!",
        "Aziza points out the fleet that has been encroaching on her group's territory.",
        "Keep her territorial pirate voice and the fleet name as the reason her crew cheers.",
        ("Look there!", "the fleet muscling in", "on our waters!",)),
    (6, 42): ("Aziza", None,
        "Aziza has finally found her opponent and vows to settle things this time.",
        "Keep the triumphant opener and the threat that rallies her crew. Give settling the score an unbroken line.",
        ("settling the score!",)),
    (13, 7): ("Lil", "Damn it! I lost to that vile brute!",
        "Lil curses at losing to someone she considers vulgar.",
        "Give Lil the blunt first-person complaint that prompts the reminder they are lucky to be alive.",
        ("I lost to that vile brute!",)),
    (13, 35): ("Lil", "It's embarrassing to keep getting rescued. I'll get stronger. Just watch!",
        "Lil is embarrassed at repeatedly needing to be rescued and vows to grow stronger.",
        "Her determination answers Maria's reassurance, and the next speaker cheers it on.",
        ("to keep getting rescued.", "I'll get stronger.", "Just watch!",)),
    (19, 36): ("Maria", None,
        "Maria decides to have their own ship brought alongside.",
        "Keep her composed order after Xien senses trouble. Reflow the full nautical instruction.",
        ("Bring us alongside, please.",)),
    (19, 40): ("Angel", None,
        "Angel blames repeated defeats and lack of earnings on Aziza and says she must answer for them.",
        "Let his accusation turn sharply from money to blame. Aziza immediately questions that blame.",
        ("We keep losing,", "not making any money.", "answer for that.",)),
    (19, 88): ("Al", "...Watch your place, lackeys.",
        "Al tells the underlings not to get above themselves.",
        "The curt contempt works after they try to dismiss him as an outsider. Preserve his terse interruption.",
        ("Watch your place, lackeys.",)),
    (19, 180): ("Aziza", "You give me too much credit. I didn't stoop to piracy. I'm a pirate's daughter. My father was a pirate.",
        "Aziza deflects the praise and explains she was born to a pirate father, so she has not lowered herself by taking up piracy.",
        "Answer Yukihisa's actual choice of words. She follows this by explaining how she learned from her father's crew.",
        ("give me too much credit.", "stoop to piracy.", "a pirate's daughter.", "My father was a pirate.",)),
    (21, 17): ("Maria", "...You're right. I underestimated you.",
        "Maria admits that she underestimated Aziza.",
        "Her cool acknowledgment answers Aziza's challenge and leaves room for Aziza's next taunt.",
        ("I underestimated you.",)),
    (29, 119): ("Camille", "With {MACRO:FI} on our side, we can win!",
        "Camille says that having Maria on their side would be worth a hundred men.",
        "Keep his sudden confidence when Maria intervenes for Lil. A direct expression of confidence carries the idiom in his short turn.",
        ("on our side,", "we can win!",)),
    (29, 153): ("Maria", "This isn't our fight. We're pulling out.",
        "Maria decides to withdraw because the fight is none of their business.",
        "Keep the brisk command in the withdrawal branch distinct from her intervention in the other branch.",
        ("This isn't our fight.", "We're pulling out.",)),
    (31, 21): ("Maria", "Kuhn's fleet in disguise... He's shown his true colors at last. We have to help Lil now!",
        "Maria reacts to Kuhn's fleet disguised as hers, says he has revealed his true character, and resolves to help Lil immediately.",
        "Answer Xien's account of the false colors with recognition and urgency before he spots another fleet.",
        ("fleet in disguise...", "his true colors", "help Lil now!",)),
    (31, 60): ("Hodram", None,
        "Hodram calls his crew into action and orders every hand to battle stations.",
        "Keep the brisk order after Maria calls for action against Kuhn. All hands and battle stations should read as one command.",
        ("All hands, battle stations!",)),
    (33, 80): ("Jam", None,
        "Jam calls Maria frightening and admits he admires her.",
        "The casual tag and hesitation capture his fondness. Xien's approval and the following declaration of loyalty support that reading.",
        ("She's terrifying,", "pretty great, huh?",)),
    (35, 6): ("Hodram", "Excuse me. Sorry to barge in like this...",
        "Hodram apologizes for arriving without warning.",
        "A courteous interruption sounds natural before Maria asks who he is.",
        ("Sorry to barge in like this...",)),
    (38, 5): ("Abraham", "Are you {MACRO:FA}? I hear you've been making waves in the Indian Ocean lately.",
        "Abraham asks whether this is the person who has recently caused a stir in the Indian Ocean.",
        "Let his conversational opening carry a little wryness and keep the family name substitution before Maria asks who he is.",
        ("Are you {MACRO:FA}?", "been making waves", "in the Indian Ocean lately.",)),
    (38, 22): ("Abraham", "Now, don't jump to conclusions. We're busy driving out the Europeans. We've got no time for you right now. So...",
        "Abraham tells Maria not to jump to conclusions and says driving out the Europeans leaves no time to take her on.",
        "Keep the firm reassurance with its time limit. He is leading into a proposal to join forces.",
        ("don't jump to conclusions.", "driving out the Europeans.", "We've got no time", "for you right now.",)),
    (39, 8): ("Xien", None,
        "Xien recognizes Nagarpur and is surprised that he is still there.",
        "Keep the wry question after his lament. Maria dismisses him as a threat in the next turn.",
        ("What's he still doing here?",)),
    (41, 49): ("Maria", None,
        "Maria agrees that she cannot remain to build the town and says she has much left to do.",
        "The quiet acknowledgment works after the crew raises the cost of staying in Ming, before the rumor of official suspicion.",
        ("You're right... I can't.", "still so much I have to do...",)),
    (43, 18): ("Maria", "We can trade now. That's progress. We've taken the first step.",
        "Maria calls the new ability to trade progress and the first step.",
        "The existing measured optimism works after the announcement of exclusive trading rights. Keep her first-step assessment together before the investment advice.",
        ("We can trade now.", "That's progress.", "We've taken the first step.",)),
    (47, 60): ("Innkeeper", "They've taken people from my village, sent them every which way, and made them work with barely anything to eat!",
        "Many of her fellow villagers have been taken to different places and forced to work on almost no food.",
        "Keep this as her specific accusation after two others describe dispossession and murder. The next speaker denies responsibility.",
        ("people from my village,", "barely anything to eat!",)),
    (47, 211): ("Maria", "Where'd that come from? You're acting odd.",
        "Maria wonders what suddenly prompted the remark and finds it strange.",
        "She is bemused by the sudden declaration of loyalty, since she did not hear his private thought.",
        ("Where'd that come from?", "You're acting odd.",)),
    (48, 83): ("Rafael", "I had no idea you were so pretty... Clau, those rumors must be made up...",
        "Rafael blurts out his surprise at Maria's beauty and tells Claudio the rumors must be baseless.",
        "Keep his awkward candor and turn to Claudio so Claudio's exaggerated reassurance plays off it.",
        ("I had no idea you were so pretty...", "those rumors must be made up...",)),
    (48, 142): ("Rafael", "Spain rules us now, but we dream of seeing Portugal bustling with sailors again.",
        "Spain has deprived Portugal of sovereignty. Rafael dreams of his country bustling again with the energy of sailors.",
        "Rafael speaks plainly about the loss of self-rule and his dream. Maria asks whether he wants Portugal to rule in Spain's place.",
        ("Spain rules us now,", "we dream of seeing Portugal", "bustling with sailors again.",)),
    (48, 178): ("Rafael", "...Did I speak out of turn? I'm sorry if I sounded full of myself.",
        "Rafael asks if he was presumptuous and apologizes for sounding self-important.",
        "Keep his self-conscious reply to Maria's thoughtful praise. She immediately reassures him.",
        ("Did I speak out of turn?", "sounded full of myself.",)),
    (48, 257): ("Claudio", "Of course! If you're up against those Spanish bastards, we'll join you in a heartbeat! Right?",
        "Claudio readily offers help, especially against the Spanish, and asks his companion to agree.",
        "Use Claudio's brash eagerness, directed at the situation they just discussed, before Rafael's courteous agreement.",
        ("those Spanish bastards,", "in a heartbeat!",)),
    (49, 139): ("Maria", "...That's a flimsy excuse. You're playing on the locals' feelings, aren't you?",
        "Maria calls his defense specious and accuses him of taking advantage of the local people's feelings.",
        "She challenges his reasoning after he claims to reclaim the villages' own treasures. Keep the charge personal so his candid answer lands.",
        ("a flimsy excuse.", "the locals' feelings,", "feelings, aren't you?",)),
    (53, 69): ("Maria", "The Proofs were relics tied to gods, heroes, and legends revered in each region. Who knows if they're even genuine?",
        "The Proofs are relics connected to revered regional gods, heroes, and legends. Their authenticity is uncertain.",
        "Keep her measured skepticism before she explains how accepting the relics as genuine gave them their significance.",
        ("relics tied to", "gods, heroes, and legends", "in each region.", "even genuine?",)),
    (53, 144): ("Ian", None,
        "Ian agrees that now the crew holds the Proofs, the outcome depends on their own efforts.",
        "The respectful agreement answers Maria without overstating the relics' power. Keep her title and the immediate lead into Xien's retirement joke.",
        ("No, Admiral.", "Now that we hold the Proofs,", "what we do with them.",)),
    (54, 74): ("Maria", "The Proofs were relics tied to gods, heroes, and legends revered in each region. Who knows if they're even genuine?",
        "The Proofs are relics connected to revered regional gods, heroes, and legends. Their authenticity is uncertain.",
        "This alternate version preserves the same recognition and the following explanation of belief as the preceding variant.",
        ("relics tied to", "gods, heroes, and legends", "in each region.", "even genuine?",)),
    (54, 150): ("Ian", None,
        "Ian agrees that now the crew holds the Proofs, the outcome depends on their own efforts.",
        "The respectful agreement works in this version of the exchange, too. Leave the effort with the crew so Xien's retirement joke follows.",
        ("No, Admiral.", "Now that we hold the Proofs,", "what we do with them.",)),
    (54, 448): ("Cesare", "Oh! It's time to go out in front of all those people! I-I'm getting awfully nervous!",
        "Cesare realizes they are about to appear before a crowd and stammers about how nervous he is.",
        "Keep his overexcited dread between Maria's readiness and her command to form ranks.",
        ("in front of all those people!", "I-I'm getting awfully nervous!",)),
    (55, 62): ("Angelo", "(That's strange... I could've sworn I was on a ship. Oh, well. Bianca's here.)",
        "Angelo thinks he should be on a ship, then dismisses the discrepancy because Bianca is there.",
        "Use his private voice in the dream. He accepts the reunion momentarily before asking where Bianca has been.",
        ("I was on a ship.", "Oh, well.", "Bianca's here.",)),
    (55, 152): ("Angelo", None,
        "Angelo begs Bianca not to go and tries to treat her departure as a joke that has gone too far.",
        "The simple plea and denial suit him after she tells him to live on. Keep the second thought intact before her final request.",
        ("Don't go...", "this isn't funny.",)),
    (57, 79): ("Mivor", "A pleasure! I'm M-Mivor! Mivor Genz. At your service!",
        "Mivor introduces himself with an emphatic hiccup over his first name and uses a formal greeting.",
        "Keep the comically formal diction and the repeated first name as he mistakes the other man's connection to Cristina.",
        ("I'm M-Mivor!", "Mivor Genz.", "At your service!",)),
    (58, 314): ("Cristina", "Oh, enough already! Can we set sail? He's driving me crazy!",
        "Cristina calls Mivor noisy and exasperating and begs the crew to leave quickly.",
        "Keep her sharp exit request after he gleefully misreads her words, just before he promises to wait forever.",
        ("Oh, enough already!", "Can we set sail?", "He's driving me crazy!",)),
    (60, 36): ("Janus", "Yes. I like machinery. I'm good with ships, and I can fix them, too.",
        "Janus likes machinery and knows how to handle and repair ships.",
        "Keep the parallel recruitment wording from Hodram's route. His plain practical answer leads directly into Maria's question about terms.",
        ("I like machinery.", "I'm good with ships,", "I can fix them, too.",)),
    (60, 94): ("Richard", "Do you know who you're talking to?!",
        "Richard demands whether Janus knows whom he is addressing.",
        "Use a direct, indignant challenge after Richard objects to indulging Janus. Janus sidesteps it and gives an appointment.",
        ("who you're talking to?!",)),
    (61, 63): ("Charles", "Oh, it's you. Can it wait? I'm busy. I'm this close to proving my theory...",
        "Charles asks the caller to come back later because he is busy and close to proving his theory.",
        "Keep the distracted greeting and his immediate priorities before the complaint about the blasts.",
        ("Can it wait?", "I'm this close", "to proving my theory...",)),
    (61, 87): ("Xien", "Well, I can't blame you if you don't know who you're talking to.",
        "Xien says Charles's skepticism is understandable if he does not recognize his listener.",
        "Use a gently chiding lead into Xien's introduction and praise of Maria.",
        ("I can't blame you", "who you're talking to.",)),
    (61, 94): ("Xien", "As for her accomplishments... well, I could go on all day listing them! Now do you see who you're talking to?",
        "Xien's long list of achievements is elided. He says there are too many to list and asks what Charles thinks.",
        "Let the ellipsis and boast suggest the omitted roll call. Keep the teasing challenge before Charles offers his science.",
        ("As for her accomplishments...", "I could go on all day", "who you're talking to?",)),
    (61, 112): ("Charles", "Oh, this sounds like fun! I'm Charles Jean Rochefort. Pleased to meet you!",
        "Charles is excited and introduces himself as Charles Jean Rochefort.",
        "The pleased enthusiasm and explicit full name belong here after their joking exchange. Keep the full name together.",
        ("Charles Jean Rochefort.", "Pleased to meet you!",)),
    (64, 60): ("Sailor", "I ask every time a ship comes in. You're the hundredth person I've asked.",
        "The sailor has asked arrivals as they come off ships, and Maria is the hundredth person.",
        "Make the repeated question and the count explicit after he says what kind of captain he wanted to find.",
        ("every time a ship comes in.", "the hundredth person",)),
    (73, 23): ("Port Worker", "Huh? How do you know all that stuff?",
        "The man is bewildered that Charles knows something so complicated.",
        "Keep the unstudied surprise after Charles's description of the bee in amber, before Charles explains science.",
        ("How do you know", "all that stuff?",)),
    (75, 22): ("Maria", "Is it mail made of peacock feathers?",
        "Maria guesses the mail is made of peacock feathers.",
        "Keep the armor type already named and the mistaken construction clear for Samwell's correction.",
        ("made of peacock feathers?",)),
    (75, 34): ("Samwell", "But they say it stops enemies in their tracks just by how it looks. That's the best thing about it, apparently.",
        "Samwell has heard that the armor's overwhelming appearance makes enemies freeze, which is supposed to be its chief benefit.",
        "Use his enthusiastic sales pitch and keep the claim secondhand. Maria then asks where the armor is.",
        ("stops enemies", "in their tracks", "just by how it looks.",)),
    (78, 10): ("Emilio", "Hey, eating's important! Besides, there's something I'm looking for.",
        "Emilio says eating matters and that he also has something he is looking for.",
        "Keep his cheerful defense of a running habit and the hook for Maria's immediate question.",
        ("eating's important!", "there's something", "I'm looking for.",)),
    (78, 22): ("Maria", "The best food in the world... How could you be sure nothing else tastes better?",
        "Maria doubts that anyone can decide a dish is the world's best because there may be something better.",
        "Keep her thoughtful skepticism before Emilio's certainty about Hestia's Pot.",
        ("The best food in the world...", "nothing else tastes better?",)),
    (85, 22): ("Maria", "(Different from the others... Am I reading too much into it?)",
        "Maria privately senses a difference from the others and wonders if she is overthinking it.",
        "Keep the thought tentative between her polite consent and the formal prayer.",
        ("different from the others...", "Am I reading too much into it?",)),
    (87, 198): ("Xien", None,
        "Xien asks whether Maria can solve the puzzle and admits he is no good at such problems.",
        "The conversational admission works after Maria comments on the arithmetic. Keep the name and the complete question together.",
        ("Can you solve it, {MACRO:FI}?", "this sort of thing.",)),
    (88, 44): ("Maria", "Oh! We've walked into a nightmare.",
        "Maria reacts in alarm as she realizes they have stumbled into an appalling situation.",
        "Keep her alarm after the men cheer an attack on the village. Give the whole realization a readable flow before Xien counts their guns.",
        ("walked into a nightmare.",)),
    (97, 114): ("Bandit", "Dunno if it has anything to do with that Proof you're after, but this was hidden in the ruins.",
        "The man does not know if the object hidden in the ruins is connected to the Proof Maria seeks.",
        "Keep his rough, tentative delivery and let Maria identify the tablet only in the following turn.",
        ("that Proof you're after,", "hidden in the ruins.",)),
}


def bind_runtime():
    release, report = base.load(parent.RELEASE), base.load(CAPTURE)
    validate_capture(report)
    assert report['ROM_sha256'] == release['candidate_sha256'] == base.digest(parent.ROM)
    assert report['frames'] == 4001
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    base.save(RUNTIME, dict(candidate_sha256=release['candidate_sha256'], cold_boot=True,
        savestate=False, actual_captain_getter=3, read_only_snapshot=report['read_only_RAM_snapshot'],
        capture_report=str(CAPTURE), capture_report_sha256=base.digest(CAPTURE),
        previously_validated_system_unlock_fixture=True, earned_unlock_verified=False))
    runtime = initial_names.RegisteredRuntime(parent.RELEASE, RUNTIME, captain=3)
    assert sha(runtime.arm) == release['target_ARM9_sha256']
    return runtime


get_source = checked_text(opening.get_source, {
    '# Block 84 already contains two registered FE continuation commands.':
        '# The registered B87R139 continuation is one extra FE command in the current stream.',
    'extras = set()': 'extras = {712} if block == 87 else set()',
})
env = opening.get_exchanges.__globals__ | globals()
exec(compile(get_source, __file__ + '::pair-original-Maria-commands', 'exec'), env)
get_exchanges = env['get_exchanges']

expand_bytes = FunctionType(opening.expand_bytes.__code__, opening.expand_bytes.__globals__ | globals())
expanded = FunctionType(opening.expanded.__code__, opening.expanded.__globals__ | globals())
macro_source = checked_text(getsource(initial_names.macro.expand), {'captain==2': 'captain==3'})
macro_env = vars(initial_names.macro).copy()
exec(compile(macro_source, __file__ + '::original-Maria-name-consumer', 'exec'), macro_env)
native_source = checked_text(getsource(initial_names.native), {
    "body.replace(b'FI', b'Rafael').replace(b'FA', b'Castor')": 'expand_bytes(body)',
})
native_env = vars(initial_names) | {'expand_source': lambda: macro_env['expand'], 'expand_bytes': expand_bytes}
exec(compile(native_source, __file__ + '::original-Maria-name-display', 'exec'), native_env)
native = native_env['native']

contract_source = checked_text(opening.contract_source, {
    "macro_ascii_lengths={'FI':6,'FA':9,'FO':15}, macro_widths={'FI':36,'FA':54,'FO':90}":
        "macro_ascii_lengths={'FI':5,'FA':2,'FO':7}, macro_widths={'FI':30,'FA':12,'FO':42}",
})
env = opening.contract.__globals__ | globals() | {'previous': initial_names}
exec(compile(contract_source, __file__ + '::measured-Maria-substitution-widths', 'exec'), env)
contract = env['contract']

compile_source = checked_text(lil.compile_source, {'Original Lil exchange': 'Original Maria exchange'})
padding = FunctionType(template.compile_rows.__globals__['fit_storage_padding'].__code__,
                       {'display_cells': lambda line: len(expand_bytes(line))})
env = template.compile_rows.__globals__ | globals() | {'previous': initial_names, 'fit_storage_padding': padding}
exec(compile(compile_source, __file__ + '::preserve-Maria-storage-and-controls', 'exec'), env)
compile_rows = env['compile_rows']
main = FunctionType(template.main.__code__, template.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

