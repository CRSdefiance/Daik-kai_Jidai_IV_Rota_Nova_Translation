"""Check the Proof and relic advice in the verified native Advice consumer."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_figurehead_navigation_gift_advice_v1 as parent
from scripts import review_proof_and_relic_advice_v1 as editorial
from scripts import stage_item_production_advice_v1 as base
from scripts import stage_weapon_armor_advice_v1 as weapon
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/proof_and_relic_advice_staged_20261111_v1')
ROM = ROOT / 'proof_and_relic_advice_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT.with_name('proof_and_relic_advice_context_v2.json')
FIRST, LAST = editorial.IDS[0], editorial.IDS[-1]
PRIOR = base.load(parent.EVIDENCE)['ownership']['selector']
FRAGMENT = ('A piece of an ancient treasure map.', 'I hear four pieces make a set.')
AMENDMENTS = {
    3182: ('Mediterranean Proof of Conquest.',
           'Identify the item as the regional Proof of Conquest, using the established term as one phrase.'),
    3184: ('Indian Ocean Proof of Conquest.',
           'Restore the full region and the established Proof of Conquest term. Keep the identification concise.'),
    3208: ("This must mark the location of the Mediterranean's Proof of Conquest. I can't read it from this alone.",
           'Keep the confident identification and the inability to read the cloth on its own.'),
    3210: ("I think this holds some record of where the Indian Ocean's Proof of Conquest lies...",
           'Keep the tentative inference and the uncertainty about how the leaf records the location.'),
    **{n: (' '.join(FRAGMENT), editorial.DATA[n][3]) for n in range(3231, 3251)},
}
PHRASES = {
    **{n: (f"{region.removeprefix('the ')}'s Proof of Conquest.",)
       for n, region in zip(range(3188, 3195), editorial.REGIONS, strict=True)},
    3197: ('the area around Turkey.',),
    3205: ('a Caribbean island', 'on the map.'),
    3207: ('the North Sea\'s', 'Proof of Conquest lies.', "I can't make it out"),
    3208: ("Mediterranean's Proof of Conquest.", "I can't read it from this alone."),
    3209: ("Africa's Proof of Conquest.", 'But with only half,', "I can't make it out..."),
    3210: ('I think this holds some record', 'the Indian Ocean\'s', 'Proof of Conquest lies...'),
    3211: ("Southeast Asia's Proof of Conquest.",),
    3212: ("East Asia's Proof of Conquest.",),
    3213: ('No doubt about it.', "the New World's Proof of Conquest.".removeprefix('the ')),
    3214: ('the map to', "North Sea's Proof of Conquest."),
    3215: ('the map to', "Mediterranean's Proof of Conquest."),
    3216: ("Africa's Proof of Conquest.", 'But with only half...'),
    3217: ("the Indian Ocean's", 'Proof of Conquest lies.'),
    3218: ('the map to', 'Southeast Asia\'s', 'Proof of Conquest...'),
    3219: ("East Asia's Proof of Conquest",),
    3220: ('the map to', "New World's Proof of Conquest."),
    3221: ("Even a ruby can't match that red.", 'A beauty like this is rare.',
           "I'd give it to the Boarding Leader."),
    3222: ("I'd give it to a deckhand", 'the Boarding Leader.'),
    3226: ('Now this is a magic sword.', 'The longer I look at it,', 'the more it draws me in.'),
    3227: ('What a lovely mermaid figurine!', 'Give it to the gunner.'),
    3228: ('An animal horn.', "I hear it's prized", 'in Chinese medicine.'),
    3229: ("I can't put into words.", "I'd entrust it", 'a warrior you can count on.'),
    3230: ("You don't often come across", 'a piece this fine.', 'a warrior you can count on.'),
    **dict.fromkeys(range(3231, 3251), FRAGMENT),
}


def stage_environment():
    review = SimpleNamespace(**(vars(editorial.previous) | vars(editorial) | {
        'RELEASE': parent.RELEASE, 'FIRST': FIRST, 'OUTPUT': OUTPUT,
    }))
    env = vars(base) | vars(weapon) | globals() | {'review': review}
    env['transform'] = FunctionType(weapon.transform.__code__, env)
    code = checked_text(getsource(base.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [35, 36]",
    })
    exec(compile(code, __file__ + '::owned-proof-and-relic-common-blocks', 'exec'), env)
    env['check_selector'] = FunctionType(base.check_selector.__code__, env)
    return env


def main():
    if not OUTPUT.exists():
        manuscript = base.load(editorial.OUTPUT)
        for row in manuscript['records']:
            if row['message_ID'] in AMENDMENTS:
                assert row['decision'] == 'revision'
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note)
        manuscript['editorial_amendments'] = sorted(AMENDMENTS)
        base.save(OUTPUT, manuscript)
    FunctionType(base.main.__code__, stage_environment())()


if __name__ == '__main__':
    main()
