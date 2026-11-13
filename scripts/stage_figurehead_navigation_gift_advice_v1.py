"""Verify the figurehead, navigation and gift advice in the original portrait consumer."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_crew_equipment_advice_v1 as parent
from scripts import review_figurehead_navigation_gift_advice_v1 as editorial
from scripts import stage_item_production_advice_v1 as base
from scripts import stage_weapon_armor_advice_v1 as weapon
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/figurehead_navigation_gift_advice_staged_20261111_v1')
ROM = ROOT / 'figurehead_navigation_gift_advice_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT
FIRST, LAST = editorial.IDS[0], editorial.IDS[-1]
PRIOR = base.load(parent.EVIDENCE)['ownership']['selector']
PHRASES = {
    3147: ('Fit it to any ship', 'the whole fleet', 'pick up speed.'),
    3148: ('They say sailors on a ship', 'fitted with this', "don't get hungry as quickly."),
    3149: ('drive off dangerous clouds.', 'fit it to any ship.'),
    3150: ('a ship that matters to you.',),
    3151: ('the ship with the strongest guns.',),
    3152: ('Fit it to any ship', 'the whole fleet benefits.', 'spot things farther away.'),
    3153: ('It should work on any ship.', 'refresh the spirit', 'ease fatigue...'),
    3154: ('Once this is installed,', 'transfer it to another ship.'),
    3155: ('a ship with plenty of sailors.', 'help in boarding fights.'),
    3156: ("bring heaven's protection", 'to any ship.', 'keep the crew from getting sick.'),
    3159: ('Give it to a lookout.', 'make items and ports', 'easier to spot.'),
    3160: ('Beautiful work.', 'Women around the North Sea', 'how delicate it is.'),
    3161: ('Great seafaring nations', 'its simple charm.'),
    3162: ('Gold dust, eh?', 'I seem to recall hearing', 'women in the north', 'especially fond of gold.'),
    3163: ('You need a strong arm to use it.', 'I heard in Northern Europe',
           'women there who love to cook', 'would be glad to have it.'),
    3164: ('people in Western Europe', 'would be curious about', 'art from the East.'),
    3165: ('Arabian clothing', 'quite mysterious', 'to Europeans.'),
    3166: ('Beautiful poetry.', 'Around the Mediterranean,', "tales of ancient Greece's glory",
           'still fire the imagination.'),
    3167: ('ancient ruins', 'all over the Mediterranean.', 'Someone who grew up there',
           'might find this interesting.'),
    3168: ('Everyone around the Mediterranean', 'knows this statue.', 'plenty would want it.', 'Magnificent...'),
    3169: ('The Mediterranean', 'is known for the finest', 'stained glass.', 'Someone from there',
           'should appreciate this.'),
    3170: ('A girl I met in China', 'wanted this in the worst way.'),
    3171: ('I recall hearing about', 'a woman learning to dance.', 'in a tavern', 'in some Indian Ocean town.'),
    3172: ('a fleet from the East', 'once reached East Africa', 'jade brings good luck.'),
    3173: ('Indian classics', 'widely read', 'in Southeast Asia, too.'),
    3174: ('from Persia to Japan...', 'this piece has deep ties to Asia.'),
    3175: ('It is beautiful...', 'I doubt people in the West', 'what makes it special.'),
    3176: ('piece of craftsmanship.', 'Carpets are very popular', 'in East Asia too.'),
    3177: ('Fine silk, I see.', 'people in the East', 'would appreciate it, too.'),
    3178: ('Pottery thrives in West Africa.', 'recognize the value', 'of this fine piece.'),
    3179: ("hard to get Europe's latest tools", 'in the New World.'),
    3180: ('A beautiful feather.', 'many women in the New World', 'are very fond of animals.'),
}


def main():
    review = SimpleNamespace(**(vars(editorial.previous) | vars(editorial) | {
        'RELEASE': parent.RELEASE, 'FIRST': FIRST,
    }))
    env = vars(base) | vars(weapon) | globals() | {'review': review}
    env['transform'] = FunctionType(weapon.transform.__code__, env)
    code = checked_text(getsource(base.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [35]",
    })
    exec(compile(code, __file__ + '::owned-figurehead-navigation-and-gift-common-block', 'exec'), env)
    env['check_selector'] = FunctionType(base.check_selector.__code__, env)
    FunctionType(base.main.__code__, env)()


if __name__ == '__main__':
    main()
