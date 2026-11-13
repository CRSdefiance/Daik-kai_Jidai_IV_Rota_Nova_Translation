"""Isolated original battle contact and positive-health recovery, no duel result."""
import inspect
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_sighting_context_v1109 as previous
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
ROM = Path('out/all_routes_combined_v1166_candidate.nds')


def water(arm, points):
    return FunctionType(previous.water.__code__, {**previous.water.__globals__, 'ROM': ROM})(arm, points)


def apply_fixture(arm, raw, request):
    assert len(raw) == 0x400000
    assert sha(arm) == read('translations/duel_editorial_release_v1.json')['target_arm9_sha256']
    if request == {'sighting_context': 'compassAttack8'}:
        code = inspect.getsource(previous.apply_fixture)
        old = "read('translations/sighting_grammar_editorial_release_v1.json')['target_arm9_sha256']"
        assert code.count(old) == 1
        code = code.replace(old, "read('translations/duel_editorial_release_v1.json')['target_arm9_sha256']")
        environment = {**previous.__dict__, 'water': water}
        exec(compile(code, '<V1167-original-hostility-and-location-adapter>', 'exec'), environment)
        after, receipt = environment['apply_fixture'](arm, raw, request)
        receipt.update(ROM_adapter_module_sha256=sha(Path(__file__).read_bytes()),
                       effective_adapter_sha256=sha(code.encode()))
        return after, receipt
    assert request == {'duel_context': 'healthyContact'}
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x737C8, 0x74010), (0xE8CC, 0xED74), (0x7E154, 0x7E1A4),
                   (0x5543C, 0x55454), (0x36A24, 0x36A68), (0x519D4, 0x51A10)):
        assert arm[lo:hi] == source[lo:hi]
    cpu, get = get_machine(arm, raw)
    root, actors = get(0xCB1A8), get(0xCB184)
    assert get(0x7F244) == get(0x2E58C) == 1
    context = list(struct.unpack('<3I', cpu.mem_read(get(0x3F0F8)+8, 12)))
    assert context == [0, 1, 8]
    own, enemy = root+4+132, root+4+8*132
    assert get(0x35320, own) == 2 and get(0x35320, enemy) == 8
    mobiles = [get(0x36C70, fleet+12) for fleet in (own, enemy)]
    assert all(m and get(0x564C8, m) for m in mobiles)
    captains = [actors+0x19E4, get(0x3697C, enemy)]
    hp = [get(0x7E19C, actor) for actor in captains]
    live = [[get(0x5543C, m), get(0x55444, m)] for m in mobiles]
    assert all(v > 0 for v in hp) and all(v > 0 for values in live for v in values), 'Never revive a defeated captain or disabled vessel'
    # Stop navigation before invoking this fixture again if a duel message or
    # duel UI is observed. No healing fixture is authorized during the duel.
    from dk4tool.patch.duel_editorial import current_entries
    templates = current_entries(NdsImage.open(ROM).read_file('/COMMON/MESFILE.DK4'), arm)
    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
    current = raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]
    assert current not in {templates[n].text for n in range(1931, 1951)}, 'Do not heal or relocate during a duel'
    fixed = bytes(cpu.mem_read(mobiles[1]+16, 8))
    point = list(struct.unpack('<2i', fixed))
    point = [int(v/128) for v in point]
    terrain = water(arm, [point])
    assert terrain['queries'][0]['collision_free']
    fields = {own+0x34: struct.pack('<2i', *point), mobiles[0]+16: fixed}
    bounds = []
    for mobile, values in zip(mobiles, live, strict=True):
        model = get(0xAB158, mobile)
        limits = [get(0x183A0, model), get(0xAB18C, model)]
        assert all(0 < value <= limit for value, limit in zip(values, limits, strict=True))
        fields[mobile+24] = struct.pack('<2H', *limits)
        bounds.append(limits)
    for actor, value in zip(captains, hp, strict=True):
        target = max(value, 100)
        get(0x7E154, actor, target)
        assert get(0x7E19C, actor) == target
        fields[actor+0x18] = struct.pack('<H', target)
    after, owned = bytearray(raw), set()
    for address, data in fields.items():
        after[address-BASE:address-BASE+len(data)] = data
        owned.update(range(address, address+len(data)))
    after = bytes(after)
    assert len(owned) == 28
    changes = [{'address': BASE+i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(row['address'] in owned for row in changes)
    for offset in (0xD9858, 0x51A20):
        address = struct.unpack_from('<I', arm, offset)[0]
        assert not set(range(address, address+4)) & owned
        assert raw[address-BASE:address-BASE+4] == after[address-BASE:address-BASE+4]
    assert mobiles[1]+13 not in owned
    return after, {'context': 'healthyContact', 'owned_bytes': sorted(owned), 'changes': changes,
        'declared_fields': {str(k): v.hex() for k, v in fields.items()},
        'positive_captain_HP_before': hp, 'positive_captain_HP_after': [max(v, 100) for v in hp],
        'live_Hull_Crew_before': live, 'unchanged_native_Hull_and_crew_capacity_bounds': bounds,
        'exact_enemy_live_fixed_point': fixed.hex(), 'native_water_point': point, 'terrain': terrain,
        'original_captain_health_setter': BASE+0x7E154,
        'only_own_contact_location_and_positive_health_recovery_not_earned_progression': True,
        'no_healing_or_relocation_after_any_original_duel_message_observed': True,
        'no_actor_captain_ID_or_ownership_changes_no_RNG_or_numeric_message_or_result_override': True,
        'all_other4MiB_RAM_exact': True, 'no_dead_actor_or_disabled_vessel_revived': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
        'fixture_sha256': sha(Path(__file__).read_bytes())}
