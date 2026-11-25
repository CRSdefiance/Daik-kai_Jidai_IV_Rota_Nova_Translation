"""Check all38 complete style objects and five two-choice/one three-choice menus."""
from pathlib import Path
from scripts import check_hodram_B301_B310_objects_v1 as previous
from scripts.prepare_hodram_B311_B324_formatting_v1 import FORMATTING
from scripts.review_hodram_B311_B324_contextual_v1 import ROOT, OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT = ROOT / 'native_objects_v1'
PLAN = ROOT / 'automatic_plans_v1/automatic_plans.json'
RELEASE = Path('work/hodram_B301_B310_release_v1/registered_release_verification.json')
STARTUP = ROOT / 'own_parent_startup_v1/own_route_context.json'
source = checked_text(previous.source, {
    "assert len(objects)==23 and cases==184 and sum(len(o['physical_record_IDs']) for o in objects)==152":
        "assert len(objects)==38 and cases==304 and sum(len(o['physical_record_IDs']) for o in objects)==236",
    'physical_alternatives=152,': 'physical_alternatives=236,',
    'PASS23 compiled4100 objects/152 physical alternatives/184 original target slot cases/207 semantic rejection checks;':
        'PASS38 compiled4100 objects/236 physical alternatives/304 original target slot cases/342 semantic rejection checks;',
    "({'two':6,'three':3}[name])": "({'two':10,'three':3}[name])",
    'All23 style objects and all four menus': 'All38 style objects and all six menus',
})
env = {**previous.env, **globals(), '__file__': __file__}
exec(compile(source, __file__ + '::same-complete-native-style-and-menu-contracts-new-scope', 'exec'), env)
if __name__ == '__main__':
    env['main']()
