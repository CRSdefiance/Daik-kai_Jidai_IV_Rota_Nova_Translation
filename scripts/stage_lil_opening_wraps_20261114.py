"""Review the early Lil wrap leads in their complete original exchanges."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_hodram_final_wraps_20261114 as parent
from scripts import stage_hodram_final_wraps_20261114 as precedent
from scripts import stage_hodram_opening_wraps_20261114 as opening
from scripts import stage_hodram_rumor_wraps_20261114 as exact_reuse
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = precedent.base, precedent.sha, precedent.prior
ARM, CLEAN, IlnkContainer = precedent.ARM, precedent.CLEAN, precedent.IlnkContainer
FILE = '/data/SC2.DK4'
PRIOR_ROOT = Path('work/lil_opening_wraps_20261114_v1')
ROOT = Path('work/lil_opening_wraps_20261114_v2')
CAPTURE = PRIOR_ROOT / 'lil_startup/capture_report.json'
RUNTIME = ROOT / 'lil_native_context.json'
REVIEW = parent.TRIAGE.with_name('lil_opening_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'
DEFAULTS = {'FI': 'Lil', 'FA': 'Argot', 'FO': 'Argot Co.'}

DECISIONS = {
    (3, 33): ('Aziza', "Heh... This gets my blood pumping. Listen up, you lot!",
        'Aziza relishes the impending confrontation and calls for her crew’s attention.',
        'Keep her relish and rough address after her three orders and before she challenges the other fleet’s claim to these waters.',
        ('This gets my blood pumping.', 'Listen up, you lot!')),
    (10, 37): ('Camille', "What could we do? They're unbelievably strong.",
        'Camille tells Lil there was nothing they could do against an opponent this strong.',
        'The reassurance answers her frustration. Gerhard follows by reminding her everyone survived.',
        ('What could we do?', "They're unbelievably strong.")),
    (12, 9): ('Angel', None,
        'Angel tells the defeated Aziza she will not be given another chance.',
        'Keep the dry answer to Aziza’s unfinished “next time” and leave the threat in a single phrase.',
        ("there won't be", 'a next time for you.')),
    (12, 60): ('Snake', "You just want the Bloodstained Shamshir back from {MACRO:FO} because it's your father's keepsake!",
        'Snake accuses Aziza of wanting only to recover her late father’s sword from Lil’s company.',
        'Keep the sword’s approved item title and the accusation about the keepsake. Snake corners her in front of her crew.',
        ('the Bloodstained Shamshir', 'back from {MACRO:FO}', "your father's keepsake!")),
    (12, 99): ('Cristina', "I'm in, too! Men who need a whole gang to win make me sick!",
        'Cristina joins Al and Yukihisa, disgusted with men who can fight only by relying on superior numbers.',
        'Use Cristina’s direct contempt as she joins the defense. Fernando volunteers immediately afterward.',
        ("I'm in, too!", 'a whole gang', 'make me sick!')),
    (12, 163): ('Dandy', None,
        'Dandy proposes settling Aziza’s release for two million coins.',
        'The plain bargaining line works. Keep two million together and keep the contrast with Lil’s immediate one-million counteroffer.',
        ('two million coins.',)),
    (12, 233): ('Aziza', "When I heard you had the sword, I had to have it. I thought if I got it back...",
        'Aziza says hearing that they held the sword made her desperate to recover it and starts to explain why.',
        'Keep the unfinished thought that Lil reacts to and Aziza completes. She has just explained how she imitated her father.',
        ('I had to have it.', 'I thought if I got it back...')),
    (12, 240): ('Aziza', "...it'd prove I was more like him. Heh. But you know...",
        'Aziza thought retrieving the sword would prove she was closer to being like her father.',
        'Continue the interrupted thought. The rueful laugh and trailing turn lead to her admission that she wanted a way to remember him.',
        ("it'd prove I was more like him.", 'But you know...')),
    (14, 16): ('Lil', None,
        'After losing, Lil vows she will win the next time they meet.',
        'The blurt and promise already sound like Lil. Keep “going to win” together before Aziza challenges the boast.',
        ('Next time we meet,', "I'm going to win!")),
    (17, 12): ('Lil', "You're a prisoner, remember? You'll face punishment in Calicut. Shouldn't you worry about yourself before your cargo?",
        'Lil tells the prisoner he will be punished in Calicut and should worry about himself before his cargo.',
        'Keep the pointed question as an answer to his concern about the cargo and retain the destination and consequences.',
        ("You're a prisoner, remember?", "You'll face punishment in Calicut.",
         "Shouldn't you worry about yourself", 'before your cargo?')),
    (20, 18): ('Barbarossa', "Allies or not, I won't let you trespass on my territory. Leave the southern Mediterranean!",
        'Barbarossa forbids the intrusion despite their alliance and orders the fleet out of the southern Mediterranean.',
        'Keep the conditional meaning and the territorial order. Gerhard recognizes him right afterward.',
        ('Allies or not,', "I won't let you trespass", 'on my territory.', 'Leave the southern Mediterranean!')),
    (21, 81): ('Escante', "Well? The lesson's free of charge. I give ladies special treatment. Give them another volley!",
        'Escante mockingly waives the fee for his lesson and orders another volley.',
        'Keep his affected courtesy and the abrupt switch to orders. It answers the crew’s sarcasm about their “welcome.”',
        ("The lesson's free of charge.", 'special treatment.', 'another volley!')),
    (25, 29): ('Fernando', "Losing his company over a stupid feud... I bet he has regrets.",
        'Fernando imagines the regret of being ruined over a pointless feud.',
        'Keep Fernando’s rough sympathy for Speyer between Camille’s pity and Lil’s insistence that Speyer brought it on himself.',
        ('over a stupid feud...', 'I bet he has regrets.')),
    (26, 72): ('Camille', "This is bad, {MACRO:FI}! We need to get out of town. They say he's vicious...",
        'Camille urgently calls for them to leave town and says the man is rumored to be dangerous.',
        'The warning builds on the sailor’s fear. Keep the address, the rumor and the unfinished delivery before the stranger asks about Clifford.',
        ('This is bad, {MACRO:FI}!', 'We need to get out of town.', "he's vicious...")),
    (26, 101): ('Lil', "Exactly! What a nightmare. ...Wait.",
        'Lil agrees reflexively, then pauses as the stranger’s self-reference sinks in.',
        'Keep the quick change from agreement to dawning recognition before she stammers out Clifford’s name.',
        ('What a nightmare.',)),
    (26, 261): ('Lil', "Huh? Do I look that odd?",
        'Lil is surprised that Camille thinks what she is wearing looks odd.',
        'The puzzled question answers Camille’s objection to her outfit and sets up his explanation of Clifford’s standing.',
        ('Do I look that odd?',)),
    (26, 312): ('Camille', "Still... I didn't expect this...",
        'Camille trails off as he expresses surprise at how Lil looks in her new outfit.',
        'Keep the lingering reaction before Lil asks what he thinks and he quips about what a dress can do.',
        ("I didn't expect this...",)),
    (27, 91): ('Gerhard', None,
        'Gerhard tells Hodram he has heard of him and introduces himself by his full name.',
        'The courteous brevity works. Keep Gerhard Adernkatz together before Hodram recognizes him as the pirate hunter.',
        ("I've heard of you.", "I'm Gerhard Adernkatz.")),
    (28, 6): ('Valdes', "So you're the little merchant girl from the sticks who's been stirring up trouble in Spanish territory?",
        'Valdes belittles Lil as a provincial young merchant who has recently been encroaching on Spanish territory.',
        'Keep the class insult and accusation. The confrontation is at sea, and Lil challenges his manners in reply.',
        ('little merchant girl', 'from the sticks', 'Spanish territory?')),
    (30, 41): ('Clifford', "Our alliance rattled Valdes into splitting his forces. That's why he lost...",
        'Clifford credits the alliance with throwing Valdes off and forcing him to divide his strength, resulting in his defeat.',
        'Keep the causal sequence before Lil asks what Clifford will do now that their immediate objective is settled.',
        ('Our alliance', 'splitting his forces.', "That's why he lost...")),
    (34, 91): ('Lil', None,
        'Lil repeats the unfamiliar name and asks what it is and whether the man is ill.',
        'Keep the item’s name and her sincere concern before the man explains how the victim was hooked.',
        ("Goddess' Temptation...?", "What's that?", "Isn't he sick?")),
    (34, 176): ('Lil', "I'm a merchant, too. I won't stand for this! Who's selling that stuff? I'll teach them a lesson!",
        'Lil says she cannot forgive a fellow merchant’s conduct and demands to know who is selling the drug.',
        'Keep the merchant’s personal stake and the escalation from indignation to a threat. Her companions share her anger.',
        ("I'm a merchant, too.", "I won't stand for this!", "Who's selling that stuff?", 'teach them a lesson!')),
    (36, 114): ('Lil', 'Yes! Espinosa surrendered to me.',
        'Lil confirms Espinosa surrendered to her.',
        'The proud confirmation suits the listener’s disbelief after learning the narcotics trade has been stopped. Keep the surrender phrase together.',
        ('Espinosa surrendered to me.',)),
    (39, 25): ('Research Student', "I hoped to get government aid for a governor's office, but...",
        'The student intended to obtain government aid to build a governor’s office.',
        'Keep the practical next step and hesitation. Lil sees its investment potential before hearing the aid requires gold.',
        ('government aid', "a governor's office, but...")),
    (43, 85): ('Camille', "Any company can trade those goods. Check our market share in that town before we decide.",
        'Camille explains that all factions can buy and sell the new goods and advises considering market share in the town.',
        'Keep the tutorial’s actual rule and distinguish access to the goods from the monopoly Fernando explains next.',
        ('Any company can trade those goods.', 'Check our market share', 'in that town', 'before we decide.')),
    (44, 77): ('Camille', "Yes! Back to the Mediterranean. Let's take on Hayreddin!",
        'Camille proposes returning to the Mediterranean and challenging Hayreddin.',
        'Keep the enthusiasm and goal before the crew mate reacts to the chance to face the Pirate King.',
        ('Back to the Mediterranean.', "Let's take on Hayreddin!")),
    (44, 130): ('Lil', "No. We're off to the Mediterranean!",
        'Lil rejects the suggestion of another destination and confirms they are going to the Mediterranean.',
        'The decisive reply works in the alternate exchange. Let the full sentence fit without a break in the destination.',
        ("We're off to the Mediterranean!",)),
    (48, 12): ('Georg', "Come in, everyone. You too... Oh?",
        'Georg ushers in the party, then hesitates as he notices Camille.',
        'Keep the cordial invitation and the moment of surprise before Camille asks whether something is on his face.',
        ('Come in, everyone.',)),
}


get_exchanges = FunctionType(opening.get_exchanges.__code__, opening.get_exchanges.__globals__ | globals())
expand_bytes = FunctionType(opening.expand_bytes.__code__, opening.expand_bytes.__globals__ | globals())
expanded = FunctionType(opening.expanded.__code__, opening.expanded.__globals__ | globals())
bind_source = checked_text(opening.bind_source, {
    'actual_captain_getter=1': 'actual_captain_getter=2',
    'captain=1': 'captain=2',
})
env = opening.bind_runtime.__globals__ | globals()
exec(compile(bind_source, __file__ + '::original-Lil-context', 'exec'), env)
bind_runtime = env['bind_runtime']
native = FunctionType(opening.native.__code__, opening.native.__globals__ | {
    'expand_source': lambda: opening.initial_names.macro.expand,
    'expand_bytes': expand_bytes,
}, argdefs=opening.native.__defaults__)
contract_source = checked_text(opening.contract_source, {
    "macro_ascii_lengths={'FI':6,'FA':9,'FO':15}, macro_widths={'FI':36,'FA':54,'FO':90}":
        "macro_ascii_lengths={'FI':3,'FA':5,'FO':9}, macro_widths={'FI':18,'FA':30,'FO':54}",
})
env = opening.contract.__globals__ | globals()
exec(compile(contract_source, __file__ + '::measured-Lil-substitution-widths', 'exec'), env)
contract = env['contract']
compile_source = checked_text(precedent.compile_source, {'Original Hodram exchange': 'Original Lil exchange'})
padding = FunctionType(precedent.padding_env['fit_storage_padding'].__code__,
                       {'display_cells': lambda line: len(expand_bytes(line))})
env = precedent.compile_env | globals() | {'previous': opening.initial_names, 'fit_storage_padding': padding}
exec(compile(compile_source, __file__ + '::same-Lil-exchange-with-storage-padding', 'exec'), env)
compile_rows = env['compile_rows']

reuse_source = checked_text(getsource(exact_reuse.native_runner), {
    'hodram_rumor_wraps_context_v1.json': 'lil_opening_wraps_context_v1.json',
    "for row in review['records']:": "for row in review['records'] + review['unchanged_leads']:",
    'previous.native(ctx, selector, body': 'native(ctx, selector, body',
})
env = globals().copy()
exec(compile(reuse_source, __file__ + '::verified-page-reuse', 'exec'), env)
native_runner = env['native_runner']
env = precedent.main.__globals__ | globals()
exec(compile(exact_reuse.source, __file__ + '::fresh-Calicut-page-and-exact-reuse', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
