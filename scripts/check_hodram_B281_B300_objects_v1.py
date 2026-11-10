"""Check all source voice objects and the four two-choice/one three-choice menus."""
from pathlib import Path
from scripts import check_hodram_B251_B280_objects_v1 as previous
from scripts.prepare_hodram_B281_B300_formatting_v1 import FORMATTING
from scripts.review_hodram_B281_B300_contextual_v1 import ROOT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'native_objects_v1';PLAN=ROOT/'formatting_v1/initial_plan_v1/automatic_plans.json'
RELEASE=Path('work/hodram_B251_B280_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(previous.source,{
    "assert len(objects)==2 and cases==16 and sum(len(o['physical_record_IDs']) for o in objects)==16":
        "assert len(objects)==18 and cases==144 and sum(len(o['physical_record_IDs']) for o in objects)==131",
    'physical_alternatives=16,':'physical_alternatives=131,',
    'PASS2 compiled4100 objects/16 physical alternatives/16 original target slot cases/18 semantic rejection checks;':
        'PASS18 compiled4100 objects/131 physical alternatives/144 original target slot cases/162 semantic rejection checks;',
    "({'two':4,'three':3}[name])":"({'two':8,'three':3}[name])",
    'Both style objects and all three menus':'All 18 style objects and all five menus',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-native-object-guards-exact-new-scope','exec'),env)
if __name__=='__main__':env['main']()
