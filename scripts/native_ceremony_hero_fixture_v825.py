"""Only the already mapped calendar/access and ship-coordinate test inputs.

No captain, party, dialogue, source scheduler or random state is replaced.
The source V816 helpers execute the same unchanged getter/setter code under
V820's source-owned text-only instruction repack.
"""

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_ceremony_yield_control_v823 import source_arm
from scripts.native_ceremony_athens_fixture_v816 import set_condition as eligibility
from scripts.native_ceremony_location_fixture_v816 import relocate as approach


def set_condition(arm,raw,request):
    assert request.get('mode')=='ceremony-Athens'
    mapped=source_arm(arm);after,receipt=eligibility(mapped,raw,request)
    receipt.update(ARM9_sha256=sha(arm),source_equivalent_native_eligibility_ARM9_sha256=sha(mapped),
        actual_captain_and_all_actor_records_preserved=True)
    return after,receipt


def relocate(arm,raw,town):
    mapped=source_arm(arm);after,receipt=approach(mapped,raw,town)
    receipt.update(ARM9_sha256=sha(arm),source_equivalent_native_location_ARM9_sha256=sha(mapped),
        actual_captain_and_all_actor_records_preserved=True)
    return after,receipt
