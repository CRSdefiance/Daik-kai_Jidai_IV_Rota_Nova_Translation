"""Bind the late trade decisions to exact clean and current story records."""

from inspect import getsource

from scripts import prepare_late_trade_exchanges_20261118 as paired
from scripts import review_sakura_expeditions_macao_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, parent = paired.paired.base, paired.parent
SOURCE = paired.ROOT / "paired_source.json"
SOURCE_SHA = "e1d6f2c2b9d74c9777dddb33f1f17653008b4dddff6926590e83c162ecbc5f21"
FOLDER = precedent.FOLDER
DECISIONS = FOLDER / "late_trade_exchanges_decisions_draft_v1.txt"
OUTPUT = FOLDER / "late_trade_exchanges_20261118_prose_v4.json"
HISTORY = (
    (), (), ("lil254_B312_B319_integrated_final_review_v1.json", "lil261_B323_B335_integrated_final_review_v1.json"),
    ("maria315_B286_B302_integrated_final_review_v1.json",),
)
FINAL_WORDING = {
    (2, 319, 57): "I run FO, mister. Don't call me little lady.",
    (2, 319, 269): "Gold and ivory are what we're known for. They fetch a good price, but supplies are limited.",
    (2, 319, 1259): "Gold and ivory are scarce and expensive. You need money up front to trade in them. Only a few people can afford it.",
    (2, 319, 1371): "With a cheaper local specialty, anyone could trade and make an honest living.",
    (2, 319, 1681): "Maybe seeds for tropical crops. I hear they've found all sorts of unfamiliar crops in the New World.",
    (2, 327, 69): "I want you to make New World tomatoes a hit in Genoa, over in the Mediterranean.",
    (2, 327, 399): "Want people to try something this good? Get them talking about how a whole town loves it. That's the fastest way.",
    (2, 327, 521): "I hear a lot of people in Italy like tomatoes. Genoa's a major city there, so I figured it's our best bet.",
    (2, 328, 205): "We're close, FA! At this rate, tomatoes will be a hit in two or three days!",
    (2, 329, 301): "Oh, right. Stop by the guild in Havana again.",
    (3, 289, 219): "Two holds will do. Bring them as fast as you can. I'll pay you for everything when you get back.",
    (3, 289, 331): "Sorry. Go easy on me, will you?",
}
NOTES = {
    (2, 319, 13): "Keep the patronizing greeting so Lil's objection has an object.",
    (2, 319, 57): "Lil asserts that she runs the company. FO is the original faction-name substitution.",
    (2, 319, 141): "The speaker apologizes, then warns Lil that wandering around here is dangerous.",
    (2, 319, 269): "Keep gold and ivory as scarce local specialties that bring high profits.",
    (2, 319, 369): "Silveira is an example of wealthy buyers cornering legitimate goods. The other trade follows from that.",
    (2, 319, 503): "Keep selling people, dealing drugs and poaching as the speaker's examples before Lil names Espinosa.",
    (2, 319, 693): "This branch says Espinosa Company is gone.",
    (2, 319, 777): "This branch promises to bring down Espinosa Company in the future.",
    (2, 319, 847): "This branch says the crew already taught Espinosa a lesson.",
    (2, 319, 921): "The speaker sees a replacement for Espinosa as a regional problem.",
    (2, 319, 1067): "Keep the causal link between the next profiteer and the region's underlying problem.",
    (2, 319, 1175): "He wants a low-cost, profitable specialty that suits the region.",
    (2, 319, 1259): "Both scarcity and high start-up costs restrict who can trade in gold and ivory.",
    (2, 319, 1371): "The cheaper commodity would make legitimate trade accessible.",
    (2, 319, 1461): "He argues that accessible, profitable trade would reduce the incentive to take risks.",
    (2, 319, 1561): "Lil restates the conclusion in terms of ordinary trade and drug dealing.",
    (2, 319, 1681): "Seeds from tropical crops are a suggestion. Reports of unfamiliar crops come from the New World.",
    (2, 327, 69): "The request is to popularize New World tomatoes in Genoa in the Mediterranean.",
    (2, 327, 185): "Keep the guildmaster's comparison with cocoa, tobacco and silver.",
    (2, 327, 279): "Keep the reason some Europeans refuse to taste tomatoes without applying the claim to all Europe.",
    (2, 327, 399): "Word of popularity in one town is the advertising strategy.",
    (2, 327, 521): "The guildmaster has heard tomatoes are liked in Italy and picks Genoa as a major city.",
    (2, 327, 687): "Keep the chapel, the assigned missionary and the free distribution of trade goods in the square.",
    (2, 327, 771): "The Genoa guild already knows about the assignment and will pay Lil.",
    (2, 328, 205): "Keep the FA address and the conditional estimate of two or three more days.",
    (2, 329, 127): "Retain exactly 24,000 gold coins in the speakerless receipt.",
    (2, 329, 247): "The market-share change is small and affects Havana.",
    (2, 329, 301): "The guildmaster sends Lil back to the guild in Havana.",
    (3, 287, 95): "Keep the same bandit term that Maria immediately repeats.",
    (3, 287, 157): "The raids mainly target gold and ivory, and the bandits are well trained and organized.",
    (3, 287, 229): "Limited land-combat experience and inadequate weapons and armor explain the guards' difficulty.",
    (3, 287, 303): "The first order is five holds of armor. Europe is the sourcing hint.",
    (3, 287, 407): "The Mediterranean and North Sea are Maria's suggestions. She expects some delay.",
    (3, 287, 465): "His willingness to wait gives way to the urgency of a life-or-death request.",
    (3, 288, 47): "After increasing the guard he discovers a shortage of guns.",
    (3, 288, 123): "The second order is five holds of guns, with combined reimbursement deferred again.",
    (3, 289, 49): "He believes the bandits noticed the arms purchases and began procuring their own weapons.",
    (3, 289, 219): "He asks for exactly two holds in a hurry and promises to pay for everything then.",
    (3, 289, 293): "Maria's frustration follows three separate requests and repeated promises of payment.",
    (3, 289, 369): "Maria confirms the amount and identifies the cargo as cannons.",
    (3, 290, 21): "The guildmaster thinks the reinforcement should deter the bandits.",
    (3, 290, 91): "He apologizes for the extra trips and pays the expenses and a separate reward.",
    (3, 290, 173): "Restore the currency and keep exactly 77,000 gold coins.",
    (3, 290, 269): "Keep Sao Jorge and the small market-share increase in its original notice.",
    (3, 290, 481): "The location deep in the Sahara is a rumor, followed by a genuine warning.",
}
PHRASES = (
    "little lady.", "someone so young.", "I run FO,", "Don't call me little lady.",
    "be in charge,", "wander around here.", "Watch yourself.",
    "a young woman", "gold and ivory", "greedy types like Silveira", "easy money.",
    "take his place.", "a deeper problem", "a good profit...", "money up front",
    "get into that trade.", "an honest living.", "breaking the law?", "deal drugs.",
    "grow in the tropics.", "the New World", "New World tomatoes", "the Mediterranean.",
    "in Genoa,", "blood-red color", "a whole town loves it.", "a major city there,", "our best bet.",
    "a chapel on the ship", "assign a missionary.", "in the square, right?",
    "We're close, FA!", "two or three days!", "be a hit in two or three days!", "Stop by the guild in Havana again.",
    "the guild in Havana", "Go easy on me, will you?",
    "ask you a favor.", "weapons and armor.", "five holds of armor.", "somewhere in Europe.",
    "the North Sea,", "life and death for us.", "Please don't forget.", "short on guns, too.",
    "five holds of guns,", "I'll pay you for everything", "we're better armed",
    "weapons of their own.", "Two holds will do.", "all at once.", "Two holds of cannons,",
    "the bandits should give up.", "plus a reward.", "77,000 gold coins.",
    "where the bandits are hiding?", "deep in the Sahara.", "anything reckless.",
)

binder = precedent.binder
source = checked_text(getsource(precedent.main), {
    'line.split("|", 2)': 'line.split("|", 3)',
    'chosen = {(int(route), int(pos)): english for route, pos, english in edit_list}':
        'chosen = {(int(route), int(block), int(offset)): english for route, block, offset, english in edit_list}',
    "    history_paths =": "    chosen.update(FINAL_WORDING)\n    history_paths =",
    '            note = NOTES.get(ordinal, gloss)\n            if 43 <= ordinal <= 50:\n'
    '                note = f"Keep the individual companion\'s register and the map\'s distinction from the Proof. {gloss}"\n'
    '            proposed = chosen.get((route, ordinal))':
        '            identity = (route, block, raw["source_offset"])\n'
        '            note = NOTES.get(identity, gloss)\n            proposed = chosen.get(identity)',
    "done.add((route, ordinal))": "done.add(identity)",
    "== 527": "== 74",
})
scope = vars(precedent) | globals()
exec(compile(source, __file__ + "::whole-exchange-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
