"""Rebind the original40-byte prebattle location control to registered V1456."""
from pathlib import Path
from types import FunctionType
from scripts import native_enemy_capture_fixture_v1433 as previous
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

ROM = Path('out/all_routes_combined_v1456_candidate.nds')

def bound_read(path):
    if str(path).replace('\\','/')=='work/analysis/ship_sinking_release_v1343/registered_release_verification.json':
        old = previous.bound_read(path);config = read('translations/ship_loss_surrender_editorial_release_v1.json')
        new = read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
        assert old['ARM9_sha256']==config['source_arm9_sha256'] and old['COMMON_sha256']==config['source_common_sha256']
        assert new['ARM9_sha256']==config['target_arm9_sha256'] and new['COMMON_sha256']==config['target_common_sha256']
        assert sha(ROM.read_bytes())==new['candidate_sha256']
        return new
    return read(path)

def apply_fixture(arm,raw,request):
    bound = FunctionType(previous.apply_fixture.__code__,{**previous.__dict__,'__file__':__file__,
        'ROM':ROM,'bound_read':bound_read},argdefs=previous.apply_fixture.__defaults__)
    after,receipt = bound(arm,raw,request);assert len(receipt['owned_bytes'])==40
    receipt['loss_surrender_release_binding_sha256'] = sha(Path(__file__).read_bytes())
    receipt['previous_capture_binding_sha256'] = sha(Path(previous.__file__).read_bytes())
    return after,receipt
