"""Build and verify the next 50 native Advice portraits over the registered item hints."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.patch import item_production_advice_v1 as wrapper
from scripts import register_item_production_advice_v1 as parent
from scripts import review_weapon_armor_advice_v1 as editorial
from scripts import stage_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/weapon_armor_advice_staged_20261111_v1')
ROM = ROOT / 'weapon_armor_advice_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT
FIRST, LAST = editorial.IDS[0], editorial.IDS[-1]
PRIOR = previous.load(parent.EVIDENCE)['ownership']['selector']
ROLE = ('Boarding Leader',)
PHRASES = {
    **dict.fromkeys((3058, 3061, 3064, 3066, 3076), ("I'd give this to a deckhand", 'or the Boarding Leader.')),
    **dict.fromkeys((3069, 3070), ('a brave fighter', 'you can count on.')),
    **dict.fromkeys((3085, 3090, 3091, 3094, 3095), ("I'd make sure a deckhand or", 'the Boarding Leader had this.')),
    3059: ('They say Lohengrin was a swan', 'in human form, with uncanny powers.', 'awfully sharp, too.'),
    3062: ("For the price, it isn't much", 'of a weapon. It might make you look', 'a little grander, though.'),
    3065: ('could use it, Admiral.', 'Or you could wield it yourself.'),
    3071: ('They call it Gentian.', 'Anyone who can wield it well', 'a formidable warrior.'),
    3072: ('This is just the thing', 'for a skilled Boarding Leader.'),
    3073: ("I'd make sure this went", 'to a skilled Boarding Leader.'),
    3075: ('to a deckhand for protection.',),
    3077: ('Give this fine piece', 'to a formidable fighter', 'you can trust.'),
    3078: ('one of your crew, Admiral,', 'or wield it yourself.'),
    3079: ('This is a fine weapon.', 'I can feel some unseen power in it.'),
    3080: ('So this is the legendary...', "I never thought I'd see it", 'for myself.'),
    3081: ('Now this is a magic sword.', 'The longer I look at it,', 'the more it draws me in.'),
    3083: ('Even someone who doubts', 'their fighting skills', 'could handle this.'),
    3096: ('a confident fighter', 'equipment of this quality.'),
    3097: ('A confident fighter', 'equipment like this.'),
    3098: ('a confident fighter', 'equipment of this quality.'),
    3099: ('Even the admiral', 'by this armor.'),
    3100: ("You don't often come across", 'an item this fine.'),
    3101: ("You don't often come across", 'an item this fine.'),
    3103: ('There is a power within it', 'that words cannot describe.'),
    3104: ('Armor worthy of a true hero!',),
    3105: ("A great conqueror's dignity", 'and bearing... What a sight!',
           'This is what makes', 'being a naturalist worthwhile.'),
    3106: ('worthy of the admiral.',),
}


def transform(source, exact_parent_arm_sha):
    assembly = FunctionType(wrapper.assembly.__code__, vars(wrapper) | {
        'PRIOR': PRIOR, 'FIRST': FIRST, 'LAST': LAST,
    })
    native = FunctionType(wrapper.previous.transform.__code__, vars(wrapper.previous) | {
        'SOURCE': exact_parent_arm_sha, 'PRIOR': PRIOR, 'assembly': assembly,
    })
    return native(source)


def stage_build(release, runtime, rows):
    code = checked_text(getsource(previous.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [34]",
    })
    env = vars(previous) | globals()
    exec(compile(code, __file__ + '::one-owned-common-block', 'exec'), env)
    return env['stage'](release, runtime, rows)


def main():
    review = SimpleNamespace(**(vars(editorial.previous) | vars(editorial) | {
        'RELEASE': parent.RELEASE, 'FIRST': FIRST,
    }))
    env = vars(previous) | globals() | {'review': review, 'stage': stage_build}
    env['check_selector'] = FunctionType(previous.check_selector.__code__, env)
    FunctionType(previous.main.__code__, env)()


if __name__ == '__main__':
    main()
