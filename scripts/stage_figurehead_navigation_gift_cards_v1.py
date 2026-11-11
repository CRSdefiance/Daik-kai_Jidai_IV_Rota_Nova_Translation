"""Verify both displays for the new figurehead, navigation and gift descriptions."""

import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch import figurehead_navigation_gift_cards_v1 as patch
from scripts import stage_utility_weapon_item_cards_v1 as previous
from scripts.review_figurehead_navigation_gift_cards_v1 import IDS, OUTPUT, RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

item_table = patch.item_table
ROOT = Path('out/figurehead_navigation_gift_cards_staged_20261111_v1')
ROM = ROOT / 'figurehead_navigation_gift_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    2937: ('The king stands at the head of his troops, urging them on. His example inspires the crew.',
           'Keep the king’s position and encouragement. End on the effect his example has on the crew.'),
    2944: ('Finely crushed gold, valuable even as dust. Its beauty is quite unlike that of gold bars.',
           'Preserve the value and compare the beauty of the two forms of gold in a complete second sentence.'),
    2945: ("This stone mill grinds flour for bread dough. It's an ideal gift for a hardworking woman.",
           'Keep the purpose of the mill and the source’s specific gift description in two sentences.'),
    2946: ("Huizong's graceful watercolor shows his refined upbringing. A Northern Song emperor, he excelled at painting and calligraphy.",
           'Restore the two arts and imperial title and preserve the source’s attribution of the painting’s grace to his upbringing.'),
    2947: ('A beautiful woman is said to have come from Heaven. She forgot this turban when she went back.',
           'Keep her descent, her return and the accidental loss, all within the legend.'),
    2952: ('Gold crown from Silla, first state to unite the Korean Peninsula. Remarkably ornate for a piece from around the 7th century.',
           'Keep the full geographic reference, the approximate date and the source’s appraisal of the artistry.'),
}
context = vars(previous) | globals()
active_rows = FunctionType(previous.active_rows.__code__, context)
build = FunctionType(previous.build.__code__, context)
context.update(active_rows=active_rows, build=build)
stage_source = checked_text(inspect.getsource(previous.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(previous.__file__), Path(__file__)',
})
exec(compile(stage_source, __file__ + '::figurehead-navigation-gift-stage', 'exec'), context)
stage = context['stage']
offline = FunctionType(previous.offline.__code__, context)


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
