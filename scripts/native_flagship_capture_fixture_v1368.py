"""Rebind the exact40-byte prebattle position fixture to registered V1364.

Only the verified ROM/ARM hash and terrain-ROM binding change. The historical
loaded-position reference stays V1350;no game predicate or actor/result guard
is weakened,and no additional owned byte is introduced.
"""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from scripts import native_ship_sinking_fixture_v1351 as initial
from scripts import native_ship_sinking_fixture_v1352 as actual_position
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

ROM = Path('out/all_routes_combined_v1364_candidate.nds')


def bound_read(path):
    if str(path).replace('\\','/')=='work/analysis/ship_sinking_release_v1343/registered_release_verification.json':
        old = read(path)
        config = read('translations/flagship_capture_precision_release_v1.json')
        new = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
        assert old['ARM9_sha256']==config['source_arm9_sha256']
        assert old['COMMON_sha256']==config['source_common_sha256']
        assert new['ARM9_sha256']==config['target_arm9_sha256']
        assert sha(ROM.read_bytes())==new['candidate_sha256']
        return new
    return read(path)


def apply_fixture(arm,raw,request):
    water = FunctionType(initial.water.__code__,{**initial.__dict__,'ROM':ROM})
    env = {**initial.__dict__,'__file__':__file__,'ROM':ROM,'water':water,'read':bound_read}
    prior = SimpleNamespace(**env)
    prior.apply_fixture = FunctionType(initial.apply_fixture.__code__,env)
    fixture = FunctionType(actual_position.apply_fixture.__code__,
        {**actual_position.__dict__,'__file__':__file__,'previous':prior})
    after,receipt = fixture(arm,raw,request)
    assert len(receipt['owned_bytes'])==40
    receipt.update(registered_ROM_binding_adapter_sha256=sha(Path(__file__).read_bytes()),
        source_fixture_sha256=sha(Path(initial.__file__).read_bytes()),
        source_actual_position_fixture_sha256=sha(Path(actual_position.__file__).read_bytes()),
        only_registered_ROM_release_and_terrain_binding_changed=True)
    return after,receipt
