"""Run unchanged complete style/two-choice/three-choice contracts for this scope."""
import inspect
from pathlib import Path
from scripts import check_hodram_B211_B230_objects_v1 as previous
from scripts.prepare_hodram_B251_B280_formatting_v1 import FORMATTING
from scripts.review_hodram_B251_B280_contextual_v1 import ROOT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'native_objects_v1';PLAN=ROOT/'formatting_v1/initial_plan_v1/automatic_plans.json'
RELEASE=Path('work/hodram_B231_B250_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'
source=checked_text(inspect.getsource(previous.main),{
    'assert len(objects)==4 and cases==32 and sum(len(o[\'physical_record_IDs\']) for o in objects)==29':
        'assert len(objects)==2 and cases==16 and sum(len(o[\'physical_record_IDs\']) for o in objects)==16',
    'physical_alternatives=29,':'physical_alternatives=16,',
    'PASS4 compiled4100 objects/29 physical alternatives/32 original target slot cases/36 semantic rejection checks;':
        'PASS2 compiled4100 objects/16 physical alternatives/16 original target slot cases/18 semantic rejection checks;',
    'All four style objects and three menus':'Both style objects and all three menus',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-typed-native-object-contracts-exact-new-scope','exec'),env)
if __name__=='__main__':env['main']()
