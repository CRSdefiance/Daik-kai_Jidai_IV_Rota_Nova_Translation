"""V653-pinned recovery/proximity for original battle-selection testing.

The V620 fixture body and source-code guards are retained exactly.
"""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_contexts_v618 import terrain_queries
from scripts.probe_button_prompt_native import BASE, call, machine

ARM = 'ab9f748b46388257c9fb847a65b9c06da7920146b985224f5bb0670459ae3fcc'
ORIGIN_ARM = 'a49549b7300e6e101d52cdeabeab857ba32a20a49bbe7bad75f69d17a6f5be3b'
REFERENCE = Path('out/all_routes_combined_v604_candidate.nds')
BOUNDS = (60, 49)  # Valid original V652 committed Even assignment and normal Yard repair values, not guessed maxima.


def apply_fixture(arm, raw, action):
    if sha(arm) != ARM or len(raw) != 0x400000 or action not in ('recover', 'approach', 'recover_and_approach'):
        raise ValueError('Battle fixture requires pinned V653,4MiB RAM and a declared recovery/proximity action')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0xCB1A8, 0xCB1B4), (0x2E58C, 0x2E598), (0x36C70, 0x36C94),
                   (0x5543C, 0x55454), (0xAB158, 0xAB18C), (0x18398, 0x183A8),
                   (0x181B4, 0x181C4), (0x69B5C, 0x69E00)):
        if arm[lo:hi] != clean[lo:hi]:
            raise ValueError('Original fleet/ship state setter/getter or terrain code differs')
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    root = get(0xCB1A8)
    if get(0x2E58C) != 1:
        raise ValueError('Fixture is limited to the original active Hodram fleet1')
    own, enemy = root + 4 + 0x84, root + 4 + 5 * 0x84
    if get(0x36914, (own,)) != 1 or get(0x36914, (enemy,)) != 0:
        raise ValueError('Original own/non-own fleet predicates differ')
    names = []
    for fleet in (own, enemy):
        vt = struct.unpack('<I', u.mem_read(fleet, 4))[0]
        fn = struct.unpack('<I', u.mem_read(vt + 8, 4))[0]
        pointer = get(fn - BASE, (fleet,))
        names.append(bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('cp932'))
    if names[0] != 'Hodram Fleet' or not names[1].startswith('Speyer Co.Fleet '):
        raise ValueError('Expected original Hodram/Speyer fleet identities')
    enemy_mobile = get(0x36C70, (enemy + 12,))
    offscreen_target = None
    if enemy_mobile:
        if (not BASE <= enemy_mobile < BASE + len(raw) - 28
                or struct.unpack('<I', u.mem_read(enemy_mobile, 4))[0] != 0x02143A80):
            raise ValueError('Expected an original Speyer mobile ship')
        enemy_stats = (get(0x5543C, (enemy_mobile,)), get(0x55444, (enemy_mobile,)))
        if any(v == 0 for v in enemy_stats):
            raise ValueError('Original Speyer ship is already disabled; do not synthesize an outcome')
    else:
        if action != 'approach':
            raise ValueError('An offscreen target permits only a location approach')
        model = get(0x36C94, (enemy + 12,))
        if not BASE <= model < BASE + len(raw) - 140:
            raise ValueError('Missing original offscreen ship model')
        name = bytes(u.mem_read(model + 8, 24)).split(b'\0')[0].decode('ascii')
        stats = (get(0x183A0, (model,)), get(0x181BC, (model,)))
        if name != 'Hanse Cog' or stats != (30, 13):
            raise ValueError('Offscreen target differs from observed original V652 frame4800 model30/13')
        offscreen_target = {'model': model, 'name': name, 'persisted_Hull_Crew': list(stats),
                            'original_mobile_not_instantiated_before_location_fixture': True}
        enemy_stats = None
    mobile = get(0x36C70, (own + 12,))
    if not BASE <= mobile < BASE + len(raw) - 28 or struct.unpack('<I', u.mem_read(mobile, 4))[0] != 0x02143A80:
        raise ValueError('Expected an active original CMobileShip')
    model = get(0xAB158, (mobile,))
    if not BASE <= model < BASE + len(raw) - 140:
        raise ValueError('Underlying original ship model is invalid')
    if bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] != b'Vestaros':
        raise ValueError('Recovery is restricted to the observed Vestaros test ship')
    prior = (get(0x5543C, (mobile,)), get(0x55444, (mobile,)))
    canonical = (get(0x183A0, (model,)), get(0x181BC, (model,)))
    if canonical != BOUNDS or any(not 0 < v <= maximum for v, maximum in zip(prior, BOUNDS, strict=True)):
        raise ValueError('Expected original persisted60/49 model and live values within those observed bounds')
    after = bytearray(raw)
    owned = set()
    if action in ('recover', 'recover_and_approach'):
        # The original persisted model stays60/49 while live sailing state falls.
        # Restore the four live scalar bytes, leaving that model entirely exact.
        address = mobile + 0x18
        after[address - BASE:address - BASE + 4] = struct.pack('<2H', *BOUNDS)
        owned.update(range(address, address + 4))
    proximity = None
    if action in ('approach', 'recover_and_approach'):
        vt = struct.unpack('<I', u.mem_read(enemy, 4))[0]
        fn = struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0]
        get(fn - BASE, (0x02460000, enemy))
        point = list(struct.unpack('<2i', u.mem_read(0x02460000, 8)))
        candidates = [[point[0] + dx, point[1] + dy] for dx, dy in
                      ((0, 20), (20, 0), (-20, 0), (0, -20), (16, 16), (-16, 16))]
        reference = NdsImage.open(REFERENCE).read_file('/__arm9__.bin')
        assert arm[0x69B5C:0x69E00] == reference[0x69B5C:0x69E00]
        terrain = terrain_queries(reference, candidates)
        water = next((r['map_point'] for r in terrain['queries'] if r['collision_free']), None)
        if water is None:
            raise ValueError('No declared source-verified water point near Speyer fleet5')
        target = [v * 128 for v in water]
        address = mobile + 16
        after[address - BASE:address - BASE + 8] = struct.pack('<2i', *target)
        owned.update(range(address, address + 8))
        proximity = {'original_enemy_cached_point': point, 'source_verified_water_point': water,
                     'ship_fixed_point': target, 'terrain': terrain,
                     'own_fleet_cached_point_preserved_for_original_next_frame_update': True}
    after = bytes(after)
    changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(r['address'] in owned for r in changes)
    return after, {'synthetic_battle_recovery_or_proximity_fixture': True, 'action': action,
                   'own_fleet': own, 'enemy_fleet': enemy, 'original_fleet_names': names,
                   'active_mobile_ship': mobile, 'underlying_model': model, 'underlying_model_name': 'Vestaros',
                   'enemy_mobile_ship_unchanged': enemy_mobile, 'offscreen_saved_target': offscreen_target, 'enemy_live_Hull_Crew_unchanged': list(enemy_stats) if enemy_stats is not None else None,
                   'prior_mobile_Hull_Crew': list(prior), 'original_persisted_model_Hull_Crew': list(canonical),
                   'recovery_limits_from_original_observed_valid_state_not_claimed_maxima': list(BOUNDS),
                   'persisted_named_model_remains_entirely_unchanged': True,
                   'proximity': proximity, 'changes': changes, 'owned_bytes': sorted(owned),
                   'no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed': True,
                   'normal_travel_earned_repair_or_battle_victory_verified': False,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
                   'fixture_script_sha256': sha(Path(__file__).read_bytes())}
