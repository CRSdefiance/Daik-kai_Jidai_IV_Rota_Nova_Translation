"""Stage and verify the proof, map and material catalogue descriptions."""

import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch import relic_map_item_cards_v1 as patch
from scripts import stage_utility_weapon_item_cards_v1 as previous
from scripts.review_relic_map_item_cards_v1 import IDS, OUTPUT, RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

item_table = patch.item_table
ROOT = Path('out/relic_map_item_cards_staged_20261111_v1')
ROM = ROOT / 'relic_map_item_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    2964: ('King Cambyses commissioned this legendary crown to show his power. Around the 5th century BC, he expanded the Achaemenid realm.',
           'Keep his title, the reason he commissioned the crown and the approximate date of expansion.'),
    2965: ('A king of Aksum used this solid gold seal on documents, they say. Aksum thrived in the 2nd-6th centuries and preceded Ethiopia.',
           'Attribute the use to a king and preserve the period and the state’s place before Ethiopia.'),
    2966: ("India's oldest text is dated to about the 15th-10th centuries BC. It reflects early Aryan life and shaped Indian thought.",
           'Keep the approximate period, the people reflected in the text and its influence on Indian thought.'),
    2967: ("A wooden plaque from Kediri, which thrived in 10th- to 13th-century Indonesia. It's said to keep every islander safe.",
           'Keep the material, the Indonesian kingdom and its period, and attribute the protection to tradition.'),
    2968: ('Qin Shi Huang had this copper candlestick made in the 3rd century BC, when he built Epang and other palaces. He is said to have used it.',
           'Restore the copper, the commission, the date and the named palace. Keep his personal use qualified.'),
    2975: ('An old map drawn inside a thick piece of split bamboo.',
           'Keep the thick bamboo and the position of the drawing in the matching catalogue style.'),
    2987: ('This map details the route between an ancient city, now in ruins, and a distant island.',
           'Retain the route, detail and both locations. Make the condition of the city clear.'),
    3001: ('A detailed illustrated plan for assembling the bamboo craft.',
           'Restore that the plan is detailed and illustrated and identify what it assembles.'),
}
context = vars(previous) | globals()
active_rows = FunctionType(previous.active_rows.__code__, context)
build = FunctionType(previous.build.__code__, context)
context.update(active_rows=active_rows, build=build)
stage_source = checked_text(inspect.getsource(previous.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(previous.__file__), Path(__file__)',
})
exec(compile(stage_source, __file__ + '::relic-and-map-stage', 'exec'), context)
stage = context['stage']
offline = FunctionType(previous.offline.__code__, context)


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
