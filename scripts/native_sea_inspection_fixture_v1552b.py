"""Activate one pre-existing Monster Fish fleet and move only the player's five positions."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_ship_sinking_fixture_v1351 as terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v1542_candidate.nds')
ROOT = Path('work/analysis/sea_inspection_fixture_v1552b')
BASE = 0x02000000


def apply_fixture(arm, raw, request):
    assert request == {'sea_inspection_context': 'activate_existing_Monster_Fish'} and len(raw) == 0x400000
    release = read('work/analysis/declaration_responses_release_v1541/registered_release_verification.json')
    assert sha(arm) == release['ARM9_sha256']
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x34674, 0x34688), (0x36C70, 0x36CB8), (0xAB128, 0xAB18C), (0x55850, 0x55874),
             (0x18398, 0x183A8), (0x181BC, 0x181C4), (0x6F610, 0x6F680)]
    assert all(arm[lo:hi] == source[lo:hi] for lo, hi in spans)
    cpu, get = get_machine(arm, raw)
    fleets, models = get(0xCB1A8), get(0xCB148)
    assert get(0x2E58C) == get(0x7F244) == 1
    assert list(struct.unpack('<3I', cpu.mem_read(get(0x3F0F8) + 8, 12))) == [0, 0, 0]
    target = fleets + 4 + 39 * 132
    model = get(0x36C94, target + 12)
    assert model == models + 4 + 149 * 140 and not get(0x36C70, target + 12)
    assert get(0x35320, target) == 21 and get(0x34674, target) == 0
    assert [get(0x183A0, model), get(0x181BC, model)] == [800, 35]
    point = list(struct.unpack('<2i', cpu.mem_read(target + 0x34, 8)))
    assert point == [20136, 4280]
    candidates = [[point[0] + dx, point[1] + dy] for dx, dy in [(0, -40), (-40, 0), (40, 0), (0, 40)]]
    water = FunctionType(terrain.water.__code__, {**terrain.water.__globals__, 'ROM': ROM})
    checked = water(arm, candidates)
    chosen = next(r['map_point'] for r in checked['queries'] if r['collision_free'])
    fields, ships = {}, []
    for slot in range(5):
        mobile = get(0x36C70, fleets + 4 + 132 + 12 + 8 * slot)
        assert mobile and get(0x564C8, mobile)
        hc = [get(0x5543C, mobile), get(0x55444, mobile)]
        assert hc == ([60, 49] if slot == 0 else [25, 19])
        fields[mobile + 16] = struct.pack('<2i', *[v * 128 for v in chosen])
        ships.append({'slot': slot, 'mobile': mobile, 'Hull_Crew': hc,
                      'source_fixed_position': list(struct.unpack('<2i', cpu.mem_read(mobile + 16, 8)))})
    flag_at = target + 0x50
    flag_before = bytes(cpu.mem_read(flag_at, 1))[0]
    assert not flag_before & 8
    fields[flag_at] = bytes([flag_before | 8])
    after, owned = bytearray(raw), set()
    for at, value in fields.items():
        after[at - BASE:at - BASE + len(value)] = value
        owned.update(range(at, at + len(value)))
    after = bytes(after)
    changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert len(owned) == 41 and all(r['address'] in owned for r in changes)
    check_cpu, check = get_machine(arm, after)
    assert check(0x34674, target) == 115
    assert bytes(check_cpu.mem_read(model, 140)) == bytes(cpu.mem_read(model, 140))
    return after, {'context': 'existing_Monster_Fish_inspection', 'owned_bytes': sorted(owned), 'changes': changes,
        'declared_fields': {str(k): v.hex() for k, v in fields.items()}, 'existing_five_own_ships': ships,
        'original_existing_special_fleet': 39, 'original_existing_special_model': model, 'original_model_index': 149,
        'original_special_class': 34, 'original_company': 21, 'stored_Hull_Crew_preserved': [800, 35],
        'original_stored_special_position': point, 'source_verified_own_water_point': chosen, 'terrain': checked,
        'availability_flag_address': flag_at, 'availability_flag_before': flag_before, 'availability_flag_after': flag_before | 8,
        'at_sea_flag_bit8_proven_by_original34674': True,
        'all_other4MiB_bytes_including_models_actors_roles_health_crew_equipment_RNG_and_results_exact': True,
        'artificial_existing_fleet_activation_not_an_earned_or_natural_spawn': True,
        'no_message_ID_renderer_target_type_identity_or_combat_outcome_injected': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'fixture_sha256': sha(Path(__file__).read_bytes())}


if __name__ == '__main__':
    assert not ROOT.exists()
    report = read('E:/Rota Nova translations/Generated/work/emulation_v193/declaration_responses_v1546_1542/capture_report.json')
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 4800)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    after, proof = apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'), raw, {'sea_inspection_context': 'activate_existing_Monster_Fish'})
    ROOT.mkdir(parents=True)
    save(ROOT / 'preflight.json', proof)
    print('Isolated41-byte fixture:40 own-coordinate bytes and one existing-fleet at-sea flag;all model/stat/actor/RNG/outcome bytes preserved.')
