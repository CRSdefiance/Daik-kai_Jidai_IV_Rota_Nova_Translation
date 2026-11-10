"""Check all 23 voice objects and three two-choice/one three-choice menus."""
from pathlib import Path
from scripts import check_hodram_B281_B300_objects_v1 as previous
from scripts.prepare_hodram_B301_B310_formatting_v1 import FORMATTING
from scripts.review_hodram_B301_B310_contextual_v1 import ROOT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'native_objects_v1';PLAN=ROOT/'formatting_v1/initial_plan_v1/automatic_plans.json'
RELEASE=Path('work/hodram_B281_B300_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(previous.source,{
    "assert len(objects)==18 and cases==144 and sum(len(o['physical_record_IDs']) for o in objects)==131":
        "assert len(objects)==23 and cases==184 and sum(len(o['physical_record_IDs']) for o in objects)==152",
    'physical_alternatives=131,':'physical_alternatives=152,',
    'PASS18 compiled4100 objects/131 physical alternatives/144 original target slot cases/162 semantic rejection checks;':
        'PASS23 compiled4100 objects/152 physical alternatives/184 original target slot cases/207 semantic rejection checks;',
    "({'two':8,'three':3}[name])":"({'two':6,'three':3}[name])",
    'All 18 style objects and all five menus':'All23 style objects and all four menus',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-complete-native-voice-and-menu-contracts','exec'),env)
if __name__=='__main__':env['main']()
