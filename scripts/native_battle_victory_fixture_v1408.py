"""Rebind the original40-byte prebattle location fixture to registered V1404."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from scripts import native_ship_sinking_fixture_v1351 as initial
from scripts import native_ship_sinking_fixture_v1352 as actual_position
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

ROM = Path('out/all_routes_combined_v1404_candidate.nds')


def bound_read(path):
    if str(path).replace('\\','/')=='work/analysis/ship_sinking_release_v1343/registered_release_verification.json':
        old = read(path)
        capture = read('translations/flagship_capture_precision_release_v1.json')
        victory = read('translations/battle_victory_editorial_release_v1.json')
        new = read('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
        assert old['ARM9_sha256']==capture['source_arm9_sha256']
        assert old['COMMON_sha256']==capture['source_common_sha256']
        assert capture['target_arm9_sha256']==victory['source_arm9_sha256']
        assert capture['target_common_sha256']==victory['source_common_sha256']
        assert new['ARM9_sha256']==victory['target_arm9_sha256']
        assert new['COMMON_sha256']==victory['target_common_sha256']
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
        only_registered_ROM_release_chain_and_terrain_binding_changed=True,
        original_ordinary_cannons_crew_health_roles_actors_and_enemy_unchanged=True)
    return after,receipt
