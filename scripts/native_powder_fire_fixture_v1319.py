"""Rebind unchanged pre-battle prerequisites to the verified registered V1316 ROM."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_aftermath_town_fixture_v1290 as first_mate
from scripts import native_town_gunnery_fixture_v1299 as gunnery
from scripts import native_aftermath_battle_fixture_v1269 as terrain
from scripts.verify_village_wrap_v608 import read

ROM = Path('out/all_routes_combined_v1316_candidate.nds')


def bound_read(path):
    if str(path).replace('\\','/') == 'translations/battle_aftermath_editorial_release_v1.json':
        source = read(path)
        target = read('translations/powder_fire_editorial_release_v1.json')
        assert target['source_arm9_sha256'] == source['target_arm9_sha256']
        proof = read('work/analysis/powder_fire_release_v1315/registered_release_verification.json')
        assert proof['ARM9_sha256'] == target['target_arm9_sha256']
        assert proof['only_COMMON22_native_metadata_and188_byte_table_changed_gate_code_exact']
        return target
    return read(path)


def apply_fixture(arm,raw,request):
    assert request == {'town_context':'SaoTomeGunnery'}
    config = read('translations/powder_fire_editorial_release_v1.json')
    assert sha(arm) == config['target_arm9_sha256']
    assert NdsImage.open(ROM).read_file('/data/WORLDMAP.DK4') == NdsImage.open('out/all_routes_combined_v1266_candidate.nds').read_file('/data/WORLDMAP.DK4')
    water = FunctionType(terrain.water.__code__,{**terrain.__dict__,'ROM':ROM})
    parent = FunctionType(first_mate.apply_fixture.__code__,{**first_mate.__dict__,
        '__file__':__file__,'ROM':ROM,'read':bound_read,'water':water})
    child = FunctionType(gunnery.apply_fixture.__code__,{**gunnery.__dict__,
        '__file__':__file__,'ROM':ROM,'previous':parent})
    after,receipt = child(arm,raw,request)
    receipt.update(registered_ROM=str(ROM),registered_ROM_sha256=sha(ROM.read_bytes()),
        registered_target_config='translations/powder_fire_editorial_release_v1.json',
        original_fixture_modules_sha256={str(Path(module.__file__)):sha(Path(module.__file__).read_bytes()) for module in [first_mate,gunnery,terrain]},
        only_registered_ROM_config_and_matching_terrain_binding_changed=True)
    return after,receipt
