"""Execute original branch conditions before the reviewed shared messages."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
                               UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                               UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
                               UC_ARM_REG_R11, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as CONTEXT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')


def main():
    context = read(CONTEXT/'native_context.json')
    source = context['pre_fixture_snapshot']
    raw = Path(source['path']).read_bytes()
    assert sha(raw) == source['sha256']
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x56A00, 0x56A90), (0x56B50, 0x56BE0), (0x56CA8, 0x56D34), (0x56E24, 0x56EA4),
             (0x56F9C, 0x56FE0), (0x5762C, 0x578E0), (0x57AD4, 0x57B38),
             (0x57D08, 0x57D70), (0x586A8, 0x5872C), (0x591D0, 0x5923C),
             (0x59F38, 0x59FA0), (0x34674, 0x34688), (0x35320, 0x35370), (0x7DB0C, 0x7DB14)]
    for a, b in spans:
        assert arm[a:b] == clean[a:b], hex(a)
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]

    hit, conditional_stops = [], set()

    def stop(c, pc, size, unused):
        if pc-BASE in conditional_stops and not c.reg_read(UC_ARM_REG_CPSR) & (1 << 30):
            return
        hit.append(pc-BASE)
        c.emu_stop()

    def run(start, ends, regs=()):
        hit.clear()
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        for reg, value in regs:
            u.reg_write(reg, value & 0xffffffff)
        hooks = [u.hook_add(UC_HOOK_CODE, stop, begin=BASE+a, end=BASE+a) for a in ends]
        try:
            u.emu_start(BASE+start, STOP, count=100000)
        finally:
            for h in hooks:
                u.hook_del(h)
        assert len(hit) == 1, (hex(start), hit, hex(u.reg_read(UC_ARM_REG_PC)))
        return hit[0]

    warnings = []
    for start, normal, warning, threshold, adjusted in (
            (0x56A00, 0x56A10, 0x56A68, 50, 'rounded_half'),
            (0x56B50, 0x56B60, 0x56BB8, 40, 'rounded_half'),
            (0x56CA8, 0x56CB0, 0x56D0C, 20, 'direct'),
            (0x56E24, 0x56E30, 0x56E7C, 30, 'arithmetic_half')):
        for amount in (-3, -2, -1, 0, 1, 2, 3, 39, 40, 41, 100):
            for score in (0, 19, 20, 21, 29, 30, 31, 39, 40, 41, 49, 50, 51, 100):
                effective = amount if adjusted == 'direct' else score-(int(amount/2) if adjusted == 'rounded_half' else amount//2)
                branch = run(start, (normal, warning), ((UC_ARM_REG_R0, amount), (UC_ARM_REG_R8, score)))
                assert branch == (warning if effective <= threshold else normal)
                warnings.append({'start': start, 'input': amount, 'score': score, 'effective_score': effective, 'branch': branch})
    accepts = []
    for at, cancelled, accepted in ((0x56A74, 0x56A80, 0x56A84), (0x56BC4, 0x56BD0, 0x56BD4),
                                     (0x56D18, 0x56D24, 0x56D28), (0x56E88, 0x56E94, 0x56E98)):
        conditional_stops.add(cancelled)
        for value in (0, 1):
            branch = run(at, (cancelled, accepted), ((UC_ARM_REG_R0, value),))
            assert branch == (accepted if value else cancelled)
            accepts.append({'start': at, 'confirmation_result': value, 'branch': branch})
        conditional_stops.remove(cancelled)

    crew = []
    for capacity in (1, 9, 10, 100, 1000):
        for required in sorted({0, 1, capacity//2, capacity}):
            for total in sorted({0, 1, max(required-1, 0), required, required+1, max(capacity-1, 0), capacity, capacity+1}):
                for funds in (99, 100):
                    branch = run(0x5762C, (0x57644, 0x57668, 0x57698),
                                 ((UC_ARM_REG_R0, funds), (UC_ARM_REG_R8, 100), (UC_ARM_REG_R6, capacity),
                                  (UC_ARM_REG_R7, required), (UC_ARM_REG_R9, total)))
                    expected = 0x57698 if funds < 100 or total >= capacity else 0x57644 if total < required else 0x57668
                    assert branch == expected
                    crew.append({'capacity': capacity, 'required': required, 'total_after_recruiting': total,
                                 'funds': funds, 'branch': branch})

    actors, towns = get(0xCB184), get(0xCB178)
    here = get(0xB6618)
    city = (here-towns-4)//108
    assert towns+4+city*108 == here
    actor = actors+4+202*32
    scratch = 0x02479000
    u.mem_write(scratch, bytes(256))
    stages = []
    old_stage = bytes(u.mem_read(actor+0x1A, 1))
    try:
        for stage in range(4):
            u.mem_write(actor+0x1A, bytes([stage]))
            branch = run(0x59F38, (0x5964C, 0x5923C, 0x591D0, 0x59F60),
                         ((UC_ARM_REG_R6, actor), (UC_ARM_REG_R7, scratch)))
            assert branch == (0x5964C, 0x5923C, 0x591D0, 0x59F60)[stage]
            stages.append({'supplied_original_relationship_byte': stage, 'branch': branch})
    finally:
        u.mem_write(actor+0x1A, old_stage)

    draws, rng_calls, chance = [], [], []

    def rng(c, pc, size, unused):
        bound = c.reg_read(UC_ARM_REG_R0)
        rng_calls.append(bound)
        result = draws.pop(0)
        assert 0 <= result < bound
        c.reg_write(UC_ARM_REG_R0, result)
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, rng, begin=BASE+0x519D4, end=BASE+0x519D4)
    try:
        for first in range(6):
            for second in range(5):
                draws[:] = [first, second]
                rng_calls.clear()
                branch = run(0x591D0, (0x58F4C, 0x58F24, 0x59138),
                             ((UC_ARM_REG_R0, scratch), (UC_ARM_REG_R1, city), (UC_ARM_REG_R2, actor)))
                assert branch == (0x58F4C if first == 0 else 0x58F24 if second == 0 else 0x59138)
                assert rng_calls == ([6] if first == 0 else [6, 5])
                assert [u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)] == [scratch, city, actor]
                chance.append({'first_draw': first, 'second_draw_if_used': second if first else None,
                               'original_RNG_bounds': list(rng_calls), 'branch': branch})
    finally:
        u.hook_del(hook)

    fleet_index = get(0x2E58C)
    fleet = get(0xCB1A8)+4+fleet_index*0x84
    fleet_bytes = bytes(u.mem_read(fleet, 0x84))
    eligibility = ptr(ptr(fleet)+0x10)
    enabled = [1]

    def eligible(c, pc, size, unused):
        assert c.reg_read(UC_ARM_REG_R0) == fleet
        c.reg_write(UC_ARM_REG_R0, enabled[0])
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    fleet_rows = []
    hook = u.hook_add(UC_HOOK_CODE, eligible, begin=eligibility, end=eligibility)
    try:
        # Native captain sentinel 208 selects faction21, independently of visibility.
        u.mem_write(fleet+8, bytes([208]))
        assert get(0x35320, (fleet,)) == 21
        for enable in (0, 1):
            enabled[0] = enable
            for flags in (0, 2, 8, 10):
                for same_faction in (False, True):
                    for location in (city, 115):
                        for order in (0, 6):
                            u.mem_write(fleet+0x50, bytes([flags]))
                            u.mem_write(fleet+0x3C, bytes([location]))
                            u.mem_write(fleet+0x3F, bytes([location]))
                            u.mem_write(fleet+0x3E, bytes([order]))
                            for family, start, end, total_reg, fleet_reg, own_reg, here_reg, region_fn in (
                                    ('anchored', 0x57AD4, 0x57B38, UC_ARM_REG_R7, UC_ARM_REG_R10, UC_ARM_REG_R5, UC_ARM_REG_R6, 0xB2B48),
                                    ('destination', 0x57D08, 0x57D70, UC_ARM_REG_R7, UC_ARM_REG_R10, UC_ARM_REG_R5, UC_ARM_REG_R6, 0xB2B48),
                                    ('barmaid_anchored', 0x586A8, 0x5872C, UC_ARM_REG_R9, UC_ARM_REG_R7, None, UC_ARM_REG_R10, 0xB51B4)):
                                # Barmaid caller gets the actual player identity, so its
                                # same-faction condition is separately observed below.
                                if family == 'barmaid_anchored' and same_faction:
                                    continue
                                here_value = get(region_fn, (here,))
                                regs = [(fleet_reg, fleet), (total_reg, 0), (UC_ARM_REG_R11, scratch)]
                                if own_reg is not None:
                                    regs.extend(((own_reg, 21 if same_faction else 20), (here_reg, here_value),
                                                 (UC_ARM_REG_R4, fleet_index), (UC_ARM_REG_R8, 108)))
                                else:
                                    regs.extend(((here_reg, here), (UC_ARM_REG_R4, 108), (UC_ARM_REG_R8, fleet_index)))
                                run(start, (end,), regs)
                                actual = u.reg_read(total_reg)
                                player = get(0xCB160)
                                player_id = get(0x397D8)
                                player_faction = get(0x3D030, (player+4+player_id*0x4C,))
                                faction_ok = not same_faction if own_reg is not None else player_faction != 21
                                expected = bool(enable and not flags & 2 and faction_ok and location != 115
                                                and (family == 'destination' or not flags & 8)
                                                and (family != 'destination' or order != 6))
                                assert actual == int(expected), (family, enable, flags, same_faction, location, order, actual, expected)
                                if actual:
                                    assert ptr(scratch) == fleet_index
                                fleet_rows.append({'family': family, 'eligibility': enable, 'flags': flags,
                                                   'same_faction_input': same_faction, 'location': location, 'order': order,
                                                   'accepted': actual})
    finally:
        u.hook_del(hook)
        u.mem_write(fleet, fleet_bytes)
    assert bytes(u.mem_read(fleet, 0x84)) == fleet_bytes
    assert bytes(u.mem_read(actor+0x1A, 1)) == old_stage
    missing = []
    predicate_result = [0]

    def predicate(c, pc, size, unused):
        c.reg_write(UC_ARM_REG_R0, predicate_result[0])
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    player = get(0xCB160)
    player_id = get(0x397D8)
    faction_object = player+4+player_id*0x4C
    h = u.hook_add(UC_HOOK_CODE, predicate, begin=BASE+0x57068, end=BASE+0x57068)
    try:
        for value in (0, 1, 114):
            predicate_result[0] = value
            branch = run(0x56F9C, (0x56FB4, 0x56FCC), ((UC_ARM_REG_R8, faction_object), (UC_ARM_REG_R6, city)))
            assert branch == (0x56FB4 if value == 0 else 0x56FCC)
            missing.append({'supplied_original_57068_result': value, 'branch': branch})
    finally:
        u.hook_del(h)

    villages = get(0xCB118)
    village_objects = {get(0xCACAC, (villages, i)): i for i in range(24)}
    assert 0 not in village_objects and len(village_objects) == 24
    status_value, selected_village, village_events = [31], [None], []
    lookup_order = []

    def status(c, pc, size, unused):
        assert c.reg_read(UC_ARM_REG_R0) == here
        c.reg_write(UC_ARM_REG_R0, status_value[0])
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    def known(c, pc, size, unused):
        index = village_objects[c.reg_read(UC_ARM_REG_R0)]
        lookup_order.append(index)
        # Original caller includes only a zero result from CAD68.
        c.reg_write(UC_ARM_REG_R0, int(index != selected_village[0]))
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    def village_speech(c, pc, size, unused):
        at = c.reg_read(UC_ARM_REG_R2)
        village_events.append({'speaker': c.reg_read(UC_ARM_REG_R0), 'ID': c.reg_read(UC_ARM_REG_R1),
                               'argument_hex': bytes(c.mem_read(at, 256)).split(b'\0')[0].hex()})
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, fn, begin=BASE+a, end=BASE+a)
             for fn, a in ((status, 0xB4A88), (known, 0xCAD68), (village_speech, 0x53FE4))]
    village_cases = []
    try:
        for value in (0, 30, 31):
            status_value[0] = value
            for village in (None, *range(24)):
                selected_village[0] = village
                for formal in (0, 1):
                    village_events.clear(); lookup_order.clear()
                    u.mem_write(scratch, struct.pack('<3I', 0, 0, formal))
                    u.reg_write(UC_ARM_REG_SP, STACK)
                    u.reg_write(UC_ARM_REG_LR, STOP)
                    u.reg_write(UC_ARM_REG_R0, scratch)
                    u.reg_write(UC_ARM_REG_R1, city)
                    u.emu_start(BASE+0x576CC, STOP, count=100000)
                    assert u.reg_read(UC_ARM_REG_PC) in (STOP, BASE+0x53FE4)
                    expected = []
                    if value > 30 and village is not None:
                        source_row = next(r for r in context['all24_village_coordinate_providers_two_modes']
                                          if r['village_ID'] == village and r['table_or_ID'] == (1028 if formal else 1029))
                        expected = [{'speaker': source_row['speaker_or_role'], 'ID': source_row['table_or_ID'],
                                     'argument_hex': source_row['arguments_hex'][0]}]
                    assert village_events == expected, (value, village, formal, village_events, expected)
                    assert lookup_order == (list(range(24)) if value > 30 else [])
                    village_cases.append({'town_provider_value': value, 'only_zero_result_village': village,
                                          'formal_mode': formal, 'lookups': list(lookup_order), 'speech': list(village_events)})
    finally:
        for h in hooks:
            u.hook_del(h)
    save(ROOT/'caller_filters.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'source_context_sha256': sha((CONTEXT/'native_context.json').read_bytes()),
        'source_executable_spans_exact': [{'span': [a, b], 'sha256': sha(clean[a:b])} for a, b in spans],
        'warning_threshold_branches': warnings, 'warning_cancellation_or_scheduling_branches': accepts,
        'crew_shortfall_capacity_and_funds_conditions': crew,
        'relationship_stage_branches': stages, 'private_casual_or_rumor_chance_branches': chance,
        'fleet_candidate_filter_cases': fleet_rows,
        'missing_contract_information_conditions': missing,
        'all150_complete_original_village_selector_cases': village_cases,
        'native_captain_208_sentinel_gets_faction21_not_an_invented_pirate_identity': True,
        'fleet_and_relationship_CPU_fixture_bytes_restored': True,
        'fixture_scope': 'Offline native CPU branch fragments, with source RNG draws and eligibility virtual result supplied;not earned events, actual gameplay or changed ROM bytes.',
        'remaining': 'Production integration,copies,exact patch and actual scenes remain open.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(warnings)} thresholds,{len(accepts)} warning outcomes,{len(crew)} crew gates,4 stages,30 chance selections,{len(fleet_rows)} fleet filters,3 information branches,{len(village_cases)} full village selectors pass.', flush=True)


if __name__ == '__main__':
    main()
