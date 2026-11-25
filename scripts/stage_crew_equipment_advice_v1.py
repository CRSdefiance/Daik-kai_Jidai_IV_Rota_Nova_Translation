"""Verify the crew-equipment advice in the original shared portrait consumer."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_weapon_armor_advice_v1 as parent
from scripts import review_crew_equipment_advice_v1 as editorial
from scripts import stage_item_production_advice_v1 as base
from scripts import stage_weapon_armor_advice_v1 as weapon
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/crew_equipment_advice_staged_20261111_v1')
ROM = ROOT / 'crew_equipment_advice_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = editorial.OUTPUT
FIRST, LAST = editorial.IDS[0], editorial.IDS[-1]
PRIOR = base.load(parent.EVIDENCE)['ownership']['selector']
PHRASES = {
    3108: ('the Sail Handler', 'on the mainmast.'),
    3109: ('A lookout needs to know', 'which way the ship is heading.'),
    3110: ("the ship's exact heading.",),
    3111: ('Deck work is dull.', 'Reading some poetry', 'would make a nice change.'),
    3112: ('Deck work is dull.', 'A story might be a good diversion.'),
    3113: ('Deck work is dull.', 'A good joke or two', 'ought to liven things up.'),
    3114: ('A survey chart', 'is only as accurate', 'the tools used to make it.'),
    3115: ('With accurate timekeeping,', "the ship's exact speed.", 'That should aid surveying.'),
    3116: ('Learn the tricks', 'that come with practice', 'a better helmsman'),
    3117: ("A captain's ability", "the heavens' favor."),
    3118: ('A captain needs charisma', 'to win over the officers.'),
    3119: ("Keeping the sailors' spirits up", "is part of a captain's job, too."),
    3120: ('A First Mate', 'disgruntled sailors', 'negotiate with other factions.'),
    3121: ('A voyage is easier on the nerves', 'a First Mate', "knows the world's geography."),
    3122: ('A Boarding Leader', 'how to command troops, too.'),
    3123: ('One shout from the Boarding Leader', 'can rally the fighters.'),
    3124: ('A Boarding Leader you can count on', 'knows how to fight', 'is skilled with a sword.'),
    3125: ('A Boarding Leader you can count on', 'knows how to fight', 'is skilled with a sword.'),
    3126: ('a bigger part in gunnery', 'than you might think.'),
    3127: ('A Gunner ought to know', 'how gunpowder behaves.'),
    3128: ("an archer's focus", 'to its very limit.'),
    3129: ('A fine edge like this', 'is a great help to a shipwright.'),
    3130: ('What an edge!', 'would be glad to have it.'),
    3131: ('An edge like this', "a shipwright's best friend."),
    3132: ('Some of the old medical arts', 'were quite remarkable.'),
    3133: ('Knowing how the body works', 'is the foundation of medicine.'),
    3134: ('medicine in the Islamic world', 'is remarkably advanced.'),
    3135: ('Wonderful...', "A cook couldn't ask", 'for a better pot.'),
    3136: ('Dress like a cook,', 'somehow you feel', 'make delicious food.'),
    3137: ('Tending livestock is hard work.', 'Even a little relief', 'would be welcome.'),
    3138: ('Those are stylish boots.', 'tending animals', 'more comfortable.'),
    3139: ('Just the sort of thing', 'missionaries dream of having.'),
    3142: ('The best victory', 'you win without fighting.'),
    3143: ('The power to see the future...', 'the great strategists of old', 'had that gift.'),
    3144: ('Outwitting the enemy', 'is the heart of strategy.'),
    3145: ('even the trickiest totals', 'in the blink of an eye.'),
    3146: ('I doubt anyone could overcharge', 'buy your goods for a pittance.'),
}


def main():
    review = SimpleNamespace(**(vars(editorial.previous) | vars(editorial) | {
        'RELEASE': parent.RELEASE, 'FIRST': FIRST,
    }))
    env = vars(base) | vars(weapon) | globals() | {'review': review}
    env['transform'] = FunctionType(weapon.transform.__code__, env)
    code = checked_text(getsource(base.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [34, 35]",
    })
    exec(compile(code, __file__ + '::owned-crew-equipment-common-blocks', 'exec'), env)
    env['check_selector'] = FunctionType(base.check_selector.__code__, env)
    FunctionType(base.main.__code__, env)()


if __name__ == '__main__':
    main()
