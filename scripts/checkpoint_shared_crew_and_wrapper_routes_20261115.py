"""Bind crew selectors and distinguish forwarding sites from message producers."""

from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP,
)

from scripts import checkpoint_shared_message_producers_20261115 as prior
from scripts import checkpoint_shared_table_callers_20261115 as previous
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine


base, sha = current.base, previous.sha
OUTPUT = prior.inventory.ROOT / 'shared_crew_and_wrapper_routes_20261115_v1.json'
COMMON_ACCESSOR = 0x0205528C
GET_VOICE = 0x0207E988
WRAPPERS = {
    0x53BF0: (0x53BD8, UC_ARM_REG_R0, 0x02053C6C, UC_ARM_REG_R0),
    0x53C38: (0x53C24, UC_ARM_REG_R0, None, None),
    0x53D0C: (0x53CB0, UC_ARM_REG_R1, 0x02053F4C, UC_ARM_REG_R1),
    0x53DA0: (0x53D44, UC_ARM_REG_R1, 0x02053F4C, UC_ARM_REG_R1),
    0x53E20: (0x53DCC, UC_ARM_REG_R1, None, None),
    0x53ED4: (0x53EC0, UC_ARM_REG_R1, 0x02053F4C, UC_ARM_REG_R1),
    0x53F20: (0x53F0C, UC_ARM_REG_R1, 0x02053F4C, UC_ARM_REG_R1),
    0x53FAC: (0x53F9C, UC_ARM_REG_R1, None, None),
    0x53FF4: (0x53FE4, UC_ARM_REG_R1, None, None),
    0x54634: (0x54624, UC_ARM_REG_R0, None, None),
    0x5467C: (0x5466C, UC_ARM_REG_R0, None, None),
    0x546C8: (0x546B8, UC_ARM_REG_R0, None, None),
    0x55298: (0x5528C, UC_ARM_REG_R0, None, None),
}
CREW_HELPERS = (
    (0x123C8, 0x12418, 0x1242C, 0x0207E0B4, 8),
    (0x1242C, 0x1247C, 0x1248C, 0x0207E0B4, 4),
    (0x1250C, 0x1256C, 0x12584, 0x0207E100, 8),
    (0x12584, 0x125E4, 0x12600, 0x0207E100, 4),
)


def put(cpu, pairs):
    for reg, value in pairs:
        cpu.reg_write(reg, value)


def wrappers(ja, en):
    cpus = [machine(raw) for raw in (ja, en)]
    roles = {0x020CB184: VIEW, 0x020CB1A8: VIEW + 0x200, 0x02082478: 0, 0x0207F244: 3}
    outputs, selector_calls = [], []
    target_address = 0
    supplied = 0
    supplied_table = VIEW + 0x400
    dispatch = None
    dispatch_reg = None
    role = 7

    def intercept(u, pc, _size, _data):
        if pc == target_address:
            outputs.append(u.reg_read(UC_ARM_REG_R1 if pc == 0x02055298 else UC_ARM_REG_R0))
            u.emu_stop()
            return
        if pc == dispatch:
            selector_calls.append(u.reg_read(dispatch_reg))
            u.reg_write(UC_ARM_REG_R0, supplied)
        elif pc in roles:
            u.reg_write(UC_ARM_REG_R0, role if pc == 0x02082478 else roles[pc])
        else:
            return
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hooks = [cpu.hook_add(UC_HOOK_CODE, intercept) for cpu in cpus]
    rows = []
    try:
        for site, (entry, input_reg, dispatch, dispatch_reg) in WRAPPERS.items():
            target_address = BASE + site
            span = prior.literal_dependencies(ja, en, entry, site + 4)
            cases = []
            for role in ((3, 7) if entry in (0x53CB0, 0x53D44, 0x53DCC) else (7,)):
                for supplied in (8, 750, 3289):
                    for cpu in cpus:
                        put(cpu, ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_R0, VIEW), (UC_ARM_REG_R1, 17),
                                  (UC_ARM_REG_R2, 19), (UC_ARM_REG_R3, 23),
                                  (input_reg, supplied_table if dispatch else supplied)))
                        cpu.emu_start(BASE + entry, target_address + 4, count=256)
                        assert cpu.reg_read(UC_ARM_REG_PC) == target_address
                        assert outputs == [supplied] and selector_calls == ([supplied_table] if dispatch else [])
                        outputs.clear()
                        selector_calls.clear()
                    cases.append(dict(input_sentinel=supplied, assumed_role=role, original_consumer_reached=False))
            rows.append(dict(site=target_address, entry=BASE + entry, input_register=input_reg,
                optional_table_selector=dispatch, forwarded_cases=cases, code_locks=span,
                upstream_ID_selection_required=True))
    finally:
        for cpu, hook in zip(cpus, hooks, strict=True):
            cpu.hook_del(hook)
    return rows


def crew(ja, en):
    assert prior.inventory.branch_hits(ja, BASE, {0x02012380}) == [(0x020121E8, 0x02012380, 'arm_bl')]
    assert prior.inventory.branch_hits(en, BASE, {0x02012380}) == [(0x020121E8, 0x02012380, 'arm_bl')]
    source = [prior.literal_dependencies(ja, en, lo, hi) for lo, hi in
              ((0x121DC, 0x121EC), (0x12380, 0x123B8), (0x53F4C, 0x53F9C), (0x53C6C, 0x53CB0))]
    cases_by_rom = []
    for arm in (ja, en):
        cpu = machine(arm)
        route_root, = unpack_from('<I', arm, 0x7F250)
        case, voice, observed, tables = 0, 0, [], []
        active_size = 0
        stop = False

        def observe(u, pc, _size, _data):
            if pc in (0x0207E0B4, 0x0207E100, GET_VOICE):
                u.reg_write(UC_ARM_REG_R0, voice if pc == GET_VOICE else case)
            elif pc == COMMON_ACCESSOR:
                observed.append(u.reg_read(UC_ARM_REG_R0))
                if stop:
                    u.emu_stop()
                    return
            elif pc in (0x02053F4C, 0x02053C6C):
                tables.append(u.reg_read(UC_ARM_REG_R1 if active_size == 8 else UC_ARM_REG_R0))
                return
            else:
                return
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, observe)
        outcomes = []
        try:
            stop = True
            mood_ids = {0: 1845, 4: 1858, 5: 1871}
            for case in (0, 4, 5, 6, 255):
                put(cpu, ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_R4, 24), (UC_ARM_REG_R5, VIEW)))
                cpu.emu_start(0x020121DC, COMMON_ACCESSOR + 4, count=256)
                assert observed == [mood_ids.get(case, 24)], (case, observed)
                observed.clear()
            outcomes.append(dict(site=0x020123B4, scope='original role-24 gated caller',
                supported_ids=list(mood_ids.values()), further_unsigned_mood_result=24,
                declared_default_test_values=[6, 255], source_locks=source))

            stop = False
            for entry, site, literal_end, fixture, active_size in CREW_HELPERS:
                results, pointers = [], {}
                for case in (*range(8), 255):
                    for voice in range(active_size):
                        cpu.mem_write(route_root + 0x48, pack('<I', voice if active_size == 4 else 0))
                        call(cpu, entry, (VIEW,))
                        if not tables:
                            assert not observed and cpu.reg_read(UC_ARM_REG_R0) == 0
                            continue
                        table, = tables
                        result, = observed
                        values = unpack_from(f'<{active_size}I', arm, table - BASE)
                        if values[voice] == prior.FALLBACK:
                            expected = next(n for n in values if n != prior.FALLBACK)
                        else:
                            expected = values[voice]
                        assert result == expected
                        pointers[table] = values
                        results.append(dict(supplied_value=case, voice_or_route=voice, table=table, message_ID=result))
                        tables.clear()
                        observed.clear()
                assert results and len(pointers) in (3, 4)
                outcomes.append(dict(site=BASE + site, scope='original crew mood or state selector',
                    supplied_getter=fixture, code_locks=prior.literal_dependencies(ja, en, entry, literal_end),
                    supported_ids=sorted({r['message_ID'] for r in results}), options=pointers, cases=results))
        finally:
            cpu.hook_del(hook)
        cases_by_rom.append(outcomes)
    assert cases_by_rom[0] == cases_by_rom[1]
    return cases_by_rom[0]


def main():
    assert not OUTPUT.exists()
    release, last = map(base.load, (current.RELEASE, prior.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == last['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == last['clean_sha256'] == release['clean_input_sha256']
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    transport, controlled = wrappers(ja, en), crew(ja, en)
    pending = set(base.load(prior.inventory.LEGACY)['pending_ids'])
    assert all(pending.isdisjoint(row['supported_ids']) for row in controlled) and 24 not in pending
    remaining = set(last['still_open_in_historical_inventory'])
    sources = {row['site'] for row in controlled}
    forwarders = {row['site'] for row in transport}
    assert len(sources) == 5 and len(forwarders) == 13
    assert sources.isdisjoint(forwarders) and (sources | forwarders) <= remaining
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        crew_selectors=controlled, forwarding_sites=transport,
        open_historical_sites_after_verified_producers=sorted(remaining - sources),
        other_open_sites_except_forwarding=sorted(remaining - sources - forwarders),
        remaining_shared_keys=len(pending), new_dialogue_credit=0, new_gameplay_runs=0, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (current.RELEASE, prior.OUTPUT, Path(__file__))}))
    print('Bound five crew sites and split 13 forwarding sites from 42 remaining possible producers.')


if __name__ == '__main__':
    main()
