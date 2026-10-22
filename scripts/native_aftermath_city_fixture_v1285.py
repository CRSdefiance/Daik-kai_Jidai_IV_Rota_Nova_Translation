"""Madeira location only; preserve diplomacy and every combat prerequisite."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_battle_fixture_v1269 import ROM, water
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def apply_fixture(arm, raw, request):
    assert request == {'city_context': 'MadeiraNeutral'} and len(raw) == 0x400000
    assert sha(arm) == read('translations/battle_aftermath_editorial_release_v1.json')['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x34674, 0x34688), (0x36C70, 0x36C94), (0xCD6B8, 0xCD6CC),
                   (0x36A24, 0x36A68), (0x519D4, 0x51A28)]:
        assert arm[lo:hi] == clean[lo:hi] and raw[lo:hi] == arm[lo:hi]
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == get(0x2E58C) == 1
    mode = get(0x3F0F8)
    assert list(struct.unpack('<2I', cpu.mem_read(mode+8, 8))) == [0, 0]
    fleets, companies, towns, actors = [get(fn) for fn in [0xCB1A8, 0xCB160, 0xCB178, 0xCB184]]
    own, defender = fleets+4+132, fleets+4+22*132
    assert get(0x34674, own) == 115 and get(0x35320, own) == 2
    assert get(0x34674, defender) == 30 and get(0x35320, defender) == 6
    assert get(0x7EE08, get(0x3697C, defender)) == 46
    mobile = get(0x36C70, own+12)
    assert mobile and get(0x5543C, mobile) > 0 and get(0x55444, mobile) > 0
    port = get(0xCD6B8, 30)
    point = list(struct.unpack('<2i', cpu.mem_read(port+12, 8)))
    candidates = [[point[0]+dx, point[1]+dy] for dx, dy in [(-40, 0), (-60, 0), (0, -40), (0, -60)]]
    terrain = water(arm, candidates)
    water_point = next(row['map_point'] for row in terrain['queries'] if row['collision_free'])
    fields = {mobile+16: struct.pack('<2i', *[v*128 for v in water_point]),
              own+0x34: struct.pack('<2i', *water_point)}
    after, owned = bytearray(raw), set()
    for at, data in fields.items():
        after[at-BASE:at-BASE+len(data)] = data
        owned.update(range(at, at+len(data)))
    changes = [{'address': BASE+i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert len(owned) == 16 and all(c['address'] in owned for c in changes)
    for root, length in [(companies, 4+21*76), (towns, 4+114*108), (actors, 0x1A04), (defender, 132)]:
        assert after[root-BASE:root-BASE+length] == raw[root-BASE:root-BASE+length]
    for off in [0xD9858, 0x51A20]:
        at = struct.unpack_from('<I', arm, off)[0]
        assert after[at-BASE:at-BASE+4] == raw[at-BASE:at-BASE+4]
    return bytes(after), {'context': 'Madeira_neutral_location_only', 'owned_bytes': sorted(owned),
        'changes': changes, 'declared_fields': {str(k): v.hex() for k, v in fields.items()},
        'town_ID': 30, 'original_defender_fleet_ID': 22, 'original_defender_captain_ID': 46,
        'source_port_point': point, 'source_verified_water_point': water_point, 'terrain': terrain,
        'active_ship': mobile, 'only_own_cached_and_live_position_changed': True,
        'diplomacy_actors_IDs_defender_defenses_shares_health_RNG_and_events_unchanged': True,
        'no_battle_state_result_numeric_message_or_eligibility_injection': True,
        'normal_travel_not_claimed': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(bytes(after)),
        'fixture_sha256': sha(Path(__file__).read_bytes())}
