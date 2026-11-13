"""Stage both item views and verify the complete crew-role equipment run."""

import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch import crew_equipment_item_cards_v1 as patch
from scripts import stage_utility_weapon_item_cards_v1 as previous
from scripts.review_crew_equipment_item_cards_v1 import IDS, OUTPUT, RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

item_table = patch.item_table
ROOT = Path('out/crew_equipment_item_cards_staged_20261111_v1')
ROM = ROOT / 'crew_equipment_item_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    2919: ('A small mask invented to keep out smells from the Livestock Room. Each is carefully made by hand.',
           'Keep the singular item, the established Livestock Room label and the emphasis on careful handwork.'),
    2920: ('These stylish boots take a lot of precious rubber to make. They keep feet clean in the Livestock Room.',
           'Preserve the material, its value and quantity, and why the boots are used in the Livestock Room.'),
    2928: ('A famous Muslim merchant once used these trading scales. They measure without the slightest error.',
           'Preserve the merchant and the absolute precision in two complete sentences.'),
}
context = vars(previous) | globals()
active_rows = FunctionType(previous.active_rows.__code__, context)
build = FunctionType(previous.build.__code__, context)
context.update(active_rows=active_rows, build=build)
stage_source = checked_text(inspect.getsource(previous.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(previous.__file__), Path(__file__)',
})
exec(compile(stage_source, __file__ + '::crew-equipment-stage', 'exec'), context)
stage = context['stage']
offline = FunctionType(previous.offline.__code__, context)


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
