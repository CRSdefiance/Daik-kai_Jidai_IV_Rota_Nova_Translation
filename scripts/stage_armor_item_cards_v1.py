"""Stage and verify the complete armor category through both native item views."""

import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch import reviewed_item_cards as patch
from scripts import stage_utility_weapon_item_cards_v1 as previous
from scripts.review_armor_item_cards_v1 import IDS, OUTPUT, RELEASE, item_table
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/armor_item_cards_staged_20261111_v1')
ROM = ROOT / 'armor_item_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    2866: ('Silver leaf gives this helmet a lovely shine. A narrow slit lets the wearer see.',
           'Keep the silver leaf and move the complete first sentence onto its own row.'),
    2867: ('This helmet has a point like a beak. Its crest shows a bird in flight, a sign of courage in the face of death.',
           'Make the crest and its meaning clear without keeping the old catalogue fragments.'),
    2869: ('This pure white dress somehow warms the heart. Legend says the spirits guard whoever wears it.',
           'Keep both source facts in complete sentences that fit their own rows.'),
    2872: ("Kanem's warriors carried this sturdy shield. Their kingdom flourished in 11th-century central Africa.",
           'Restore the warriors and the flourishing kingdom in two direct sentences.'),
    2876: ('Peacock feathers adorn the back of this mail. It was made to turn heads and offers only modest protection.',
           'Restore the location of the feathers and the maker’s emphasis on appearance over practical use.'),
    2877: ('The ancient Aztec warriors of Tula are said to have worn this legendary helmet to summon courage in battle.',
           'Attribute the helmet’s traditional use to the warriors and keep the cultural terms intact.'),
    2879: ('Fine armor with a mysterious yellow sheen. No one knows its age or materials.',
           'Retain its protective quality and shine. Keep both unknowns without a technical catalogue construction.'),
    2887: ("Charles Martel of the Franks wore this superb armor at the Battle of Tours-Poitiers. Sturdy and handsome, it's fit for a king.",
           'Keep the beauty, strength and royal comparison. Correct the full-width F and avoid assigning Charles Martel a title.'),
    2888: ("This sturdy shield shines of its own accord. It's said to belong to Minerva, goddess of war and one of the twelve Olympians.",
           'Restore the self-generated light and Minerva’s place among the Twelve.'),
}
context = vars(previous) | globals()
active_rows = FunctionType(previous.active_rows.__code__, context)
build = FunctionType(previous.build.__code__, context | {'active_rows': active_rows})
context.update(active_rows=active_rows, build=build)
source = checked_text(inspect.getsource(previous.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(previous.__file__), Path(__file__)',
})
exec(compile(source, __file__ + '::armor-item-stage', 'exec'), context)
stage = context['stage']
offline = FunctionType(previous.offline.__code__, context)


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
