"""Review Rafael's homecoming, recruitment and follow-up exchanges."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_alliance_wraps_20261114 as parent
from scripts import stage_rafael_alliance_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN = previous.FILE, previous.ARM, previous.CLEAN
IlnkContainer = previous.previous.IlnkContainer
ROOT = Path('work/rafael_homecoming_wraps_20261114_v6')
CAPTURE = Path('work/rafael_homecoming_wraps_20261114_v1/rafael_startup/capture_report.json')
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_homecoming_wraps_context_v6.json')
PROOF = ROOT / 'stored_and_native.json'

DECISIONS = {
    (163, 5): ('Rafael', "This Patterned Cloth has to be the map to the Mediterranean Proof, right?",
        'Rafael checks whether the Patterned Cloth is indeed the map to the Mediterranean Proof.',
        'Retain the item name and inquisitive tag. Janus doubts its appearance, and Claudio reaches for the Brass Lamp.',
        ('This Patterned Cloth', 'has to be the map', 'the Mediterranean Proof, right?')),
    (164, 44): ('King', "The Proofs, you mean. I've asked a great deal of you. You're the only one I can turn to.",
        'The king guesses Rafael means the Proofs and acknowledges how much he has asked of him. He has no one else to rely on.',
        'Give the king a plain admission of dependence before Rafael pledges to finish the work.',
        ('The Proofs, you mean.', "I've asked a great deal of you.", "You're the only one I can turn to.")),
    (164, 68): ('King', "Very well. I'll think it over while you see your task through and make your way home.",
        'The king will consider an appropriate reward by the time Rafael achieves his real objective and returns.',
        'Keep the reward implicit after Rafael politely declines. The king defers the matter until Rafael comes back from what he set out to do.',
        ("I'll think it over", 'see your task through', 'make your way home.')),
    (165, 13): ('King', "It's about the treasure you seek.",
        'The king says he called Rafael to discuss the treasure Rafael is searching for.',
        'Keep the direct answer in the king’s register. The next speech identifies the seven Proofs and their purpose.',
        ('the treasure you seek.',)),
    (165, 16): ('King', "The seven Proofs of Conquest are said to be scattered across the world. If we show them to the Pope, we can ask him to recognize the authority of the Portuguese Crown again.",
        'Seven legendary Proofs are said to exist around the world. Showing them to the Pope would let them negotiate for renewed recognition of the Crown’s authority.',
        'Keep the reported number and the conditional diplomatic purpose. The next turn explains how the Proofs could unite Portugal again.',
        ('The seven Proofs of Conquest', 'are said to be scattered', 'across the world.', 'If we show them to the Pope,', 'of the Portuguese Crown again.')),
    (166, 85): ('King', "If we show the Pope the seven Proofs of Conquest you found, I hear he'll back our bid to restore the Portuguese Crown's authority.",
        'The king reports that if they show the Pope the seven Proofs Rafael gathered, the Pope will push for renewed recognition of the Portuguese Crown.',
        'Preserve the reported commitment and distinguish pressing for recognition from already granting it. Rafael responds with surprise.',
        ('If we show the Pope', 'the seven Proofs of Conquest', 'you found,', "he'll back our bid", "the Portuguese Crown's authority.")),
    (166, 100): ('King', "In the King of Portugal's name, I appoint you viceroy of the Estado, all our overseas trade territories!",
        'In the King of Portugal’s name, Rafael is made viceroy over all overseas trading territories, identified in the source as the Estado.',
        'Keep all the territories and the formal rank, which Rafael repeats in disbelief.',
        ("In the King of Portugal's name,", 'I appoint you viceroy', 'the Estado,', 'overseas trade territories!')),
    (166, 392): ('Al', "Boy, this is hard to watch. It's making me itch.",
        'Al finds the scene hard to bear and says it is making his back itch.',
        'Keep Al’s comic physical discomfort. The next speaker points out that he is grinning as he watches.',
        ('this is hard to watch.', "It's making me itch.")),
    (166, 489): ('Cristina', 'Honestly! Have you no manners?',
        'Cristina reproaches the group for being rude.',
        'Keep her sharp group rebuke after the others make excuses. Fernando points out they all watched anyway.',
        ('Have you no manners?',)),
    (166, 695): ('Samwell', "Wow! Now there'll be even more scenes we can't afford to miss!",
        'Samwell exclaims that there will be even more scenes worth watching.',
        'Keep his glee as the others tease Claudio. Cristina’s quieter line about Eirene follows.',
        ("there'll be even more", "we can't afford to miss!")),
    (166, 807): ('Cesare', "How shall I put it... The writing's a little awkward.",
        'Cesare hesitates, then calls the writing awkward.',
        'Keep his affected tact and the qualified criticism. Charlotte’s preceding Portuguese letter retains its source spelling as an attempt the crew comments on.',
        ('How shall I put it...', "The writing's a little awkward.")),
    (166, 818): ('Charles', 'Hmm... The meaning is clear, at least.',
        'Charles concedes that the meaning comes through.',
        'Keep his dry qualification after Cesare’s criticism. Angelo then tells them to keep those comments to themselves.',
        ('The meaning is clear, at least.',)),
    (166, 877): ('Claudio', "Heh. We know where to go first!",
        'Claudio jokes that their first destination is settled.',
        'Keep the teasing shorthand after Rafael quietly says Charlotte’s name. Rafael stammers and Claudio tells him to hurry.',
        ('where to go first!',)),
    (167, 54): ('Claudio', "Still the same old optimist, huh? You make everything sound so simple.",
        'Claudio teases Rafael for being as optimistic and simple as ever.',
        'Keep his familiar teasing before he raises a real objection to recruiting the strong man.',
        ('the same old optimist, huh?', 'sound so simple.')),
    (167, 63): ('Claudio', "A guy like that won't be easy to bring aboard...",
        'Claudio thinks it will be hard to recruit the man.',
        'Give his objection a plainspoken turn. Julio shares the doubt, and Rafael argues that they should try anyway.',
        ('A guy like that', "won't be easy", 'to bring aboard...')),
    (167, 95): ('Claudio', "(Oh, he's sure of himself.)",
        'Claudio privately remarks on how self-assured the man is.',
        'Keep the dry aside inside parentheses while Rafael improvises a polite answer.',
        ("he's sure of himself.",)),
    (167, 114): ('Al', "Bodyguard work. It's a dangerous world. There's work to be had.",
        'Al works as a bodyguard when there is no fighting, and a dangerous world supplies that work.',
        'Let Al answer brusquely. The follow-up asks what he is doing now, and he admits he was fired.',
        ('Bodyguard work.', "It's a dangerous world.", "There's work to be had.")),
    (168, 93): ('Claudio', 'Wanted to be a navigator, right?',
        'Claudio reminds Angelo that he said he wanted to be a navigator.',
        'Keep the confirmation question short and familiar. Angelo answers cautiously and Claudio turns to Rafael.',
        ('be a navigator, right?',)),
    (168, 171): ('Julio', 'Well now! You know your trade!',
        'Julio is surprised and impressed by Angelo’s grasp of the matter.',
        'Keep lively approval after Angelo criticizes small deals in the Mediterranean. Angelo continues with the reasons.',
        ('You know your trade!',)),
    (168, 186): ('Rafael', "Hmm, you've got a point. Contract fees and investment costs are high here. There's barely room for us to get in.",
        'Rafael recognizes that fees and investment costs are high and leave little room for a new entrant.',
        'Keep the realization and both types of cost. Angelo then explains the opportunities outside the Mediterranean.',
        ('Contract fees', 'investment costs', 'are high here.', "There's barely room", 'to get in.')),
    (168, 196): ('Rafael', 'Wow, you know trade too!',
        'Rafael is impressed that Angelo knows about trade as well.',
        'Use a brisk reaction before Angelo credits what he heard from sailors.',
        ('you know trade too!',)),
    (169, 7): ('Barkeep', 'Ian, take this over for me, please.',
        'The barkeep asks Ian to carry something over.',
        'Keep the simple service instruction and Ian’s name. Ian acknowledges it before the patrons notice him.',
        ('take this over for me, please.',)),
    (169, 102): ('Barkeep', "Ian, I don't think you're cut out for this work.",
        'The barkeep doubts that the work suits Ian.',
        'Keep his quiet judgment before he explains why drawing a sword on customers is a problem.',
        ("I don't think", "you're cut out for this work.")),
    (169, 114): ('Barkeep', "I'm sorry. I'll have to let you go.",
        'The barkeep apologetically dismisses Ian.',
        'A short apology and decision fit the disappointed tone. Ian accepts without arguing.',
        ("I'll have to let you go.",)),
    (170, 135): ('Carlo', "That's kind of you. But thank these travelers. They agreed to wait until morning to trade.",
        'Carlo is pleased, but redirects the thanks to the travelers for agreeing to delay their trade overnight.',
        'Preserve that the travelers agreed to wait. The innkeeper apologizes for holding them up and offers a gift.',
        ("That's kind of you.", 'thank these travelers.', 'agreed to wait', 'until morning to trade.')),
    (170, 206): ('Claudio', 'He drove a hard bargain yesterday.',
        'Claudio agrees that Carlo was skillful at bargaining the previous day.',
        'Keep the casual corroboration. Carlo answers that he has been a merchant a long time.',
        ('drove a hard bargain',)),
    (170, 256): ('Rafael', "Oh... That's why you helped the shopkeeper...",
        'Rafael sees that Carlo’s experience explains why he helped the shopkeeper.',
        'Keep the realization unfinished as he takes in Carlo’s loss. He then asks whether Carlo will go home.',
        ('you helped the shopkeeper...',)),
    (170, 308): ('Claudio', "Then it's settled. Oh, and we're counting on those trading skills of yours, too.",
        'Claudio declares the matter settled and adds that they are counting on Carlo’s skill as a professional merchant.',
        'Keep the playful afterthought about Carlo’s skills. Carlo gives his name and accepts the welcome.',
        ("Then it's settled.", "we're counting on", 'those trading skills of yours,')),
}

get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())


def contract():
    original = previous.compile_rows.__globals__['contract']
    source = checked_text(getsource(original), {
        'int(line==3 and not final and not terminal),cost[2]+protected':
            'protected+int(not final and length<14 and not terminal),'
            'cost[2]+int(line==3 and not final and not terminal and not text.endswith(chr(44)))',
    })
    env = original.__globals__.copy()
    exec(compile(source, __file__ + '::penalize-sparse-incomplete-rows', 'exec'), env)
    return env['contract']()


compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': previous.compile_rows.__globals__['previous']})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
main = FunctionType(previous.main.__code__, previous.main.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

