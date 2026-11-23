"""Bind table-driven COMMON requests on the registered cumulative candidate."""

from collections import Counter
from pathlib import Path
from struct import pack, unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R7, UC_ARM_REG_SP,
)

from scripts import checkpoint_pending_shared_native_20261115 as inventory
from scripts import checkpoint_shared_conditional_callers_20261115 as previous
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_treasure_map_documents_v1 import CALLS as MAP_FIELDS


base, sha = current.base, inventory.sha
OUTPUT = inventory.ROOT / 'shared_table_callers_20261115_v2.json'
ARM = current.stage.ARM
STOP_MASK = 0xFFFFFFFF
VOICE_TABLES = {
    0x30B10: (3, UC_ARM_REG_R5, {3: 0x2118980, 2: 0x21189A0}),
    0x31774: (1, None, {0: 0x2117580}),
    0x317A4: (2, None, {0: 0x21175A0}),
    0x33E7C: (4, UC_ARM_REG_R7, {0: 0x2117160, 1: 0x21170E0}),
    0x659D4: (2, None, {0: 0x2117F40}),
    0x659F0: (2, None, {0: 0x2117F80}),
    0x72DE0: (1, None, {0: 0x2116CE0}),
    0x72E50: (1, None, {0: 0x2116FA0}),
    0x72ED8: (1, None, {0: 0x2116FE0}),
    0x72F6C: (2, None, {0: 0x2117240}),
    0x72F7C: (2, None, {0: 0x2117040}),
    0x73030: (2, None, {0: 0x2117280}),
    0x73040: (2, None, {0: 0x2117060}),
    0x9265C: (2, None, {0: 0x21169C0}),
    0x9268C: (2, None, {0: 0x2116A60}),
}


def lock(ja, en, start, end):
    assert ja[start:end] == en[start:end], (hex(start), hex(end))
    return dict(start=BASE + start, end=BASE + end, clean_and_current_sha256=sha(ja[start:end]))


def read_word(cpu, address):
    return unpack('<I', cpu.mem_read(address, 4))[0]


def run_to(cpu, start, end):
    cpu.emu_start(BASE + start, BASE + end, count=64)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + end


def voice_tables(ja, en):
    cpus = [machine(raw) for raw in (ja, en)]
    context = lock(ja, en, 0x53F4C, 0x53F9C)
    controlled_voice = 0

    def voice(cpu, _, _size, _unused):
        cpu.reg_write(UC_ARM_REG_R0, controlled_voice)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    hooks = [cpu.hook_add(UC_HOOK_CODE, voice, begin=BASE + 0x7E988, end=BASE + 0x7E988) for cpu in cpus]
    rows = []
    try:
        for site, (instruction_count, supplied_reg, alternatives) in VOICE_TABLES.items():
            start = site - 4 * instruction_count
            bounds = lock(ja, en, start, site + 4)
            assert inventory.branch_hits(ja[site:site + 4], BASE + site, {0x02053F0C}) == [
                (BASE + site, 0x02053F0C, 'arm_bl')]
            options = []
            for state, table in alternatives.items():
                table_lock = lock(ja, en, table - BASE, table - BASE + 32)
                slots = unpack_from('<8I', ja, table - BASE)
                assert slots[0] != STOP_MASK and all(n <= 3667 or n == STOP_MASK for n in slots)
                outputs = [slots[0] if n == STOP_MASK else n for n in slots]
                for cpu in cpus:
                    if supplied_reg is not None:
                        cpu.reg_write(supplied_reg, state)
                    run_to(cpu, start, site)
                    assert cpu.reg_read(UC_ARM_REG_R1) == table
                    for controlled_voice, expected in enumerate(outputs):
                        call(cpu, 0x53F4C, (3, table))
                        assert cpu.reg_read(UC_ARM_REG_R0) == expected, (hex(site), hex(table), controlled_voice)
                options.append(dict(selected_table=table, native_slots=list(slots), selected_by_voice=outputs,
                                    supplied_condition=state if supplied_reg else None, lock=table_lock))
            cases = sorted({n for option in options for n in option['selected_by_voice']})
            rows.append(dict(call_site=BASE + site, target=0x02053F0C, scope='original eight stock voice selectors',
                supported_ids=cases, code=bounds, options=options))
    finally:
        for cpu, hook in zip(cpus, hooks, strict=True):
            cpu.hook_del(hook)
    return rows, context


def ancient_maps(ja, en):
    rows = []
    for label, (start, site, _, literal, table, first, last) in MAP_FIELDS.items():
        seals = [lock(ja, en, a, b) for a, b in ((start, site + 4), (literal, literal + 4),
                                               (table, table + (last - first + 1) * 4))]
        assert unpack_from('<I', ja, literal) == (BASE + table,)
        expected = sorted(unpack_from(f'<{last - first + 1}I', ja, table))
        assert expected == list(range(first, last + 1))
        for raw in (ja, en):
            cpu = machine(raw)
            selector = UC_ARM_REG_R1 if label == 'artifact_lore' else UC_ARM_REG_R4
            for index in range(last - first + 1):
                cpu.reg_write(selector, index)
                run_to(cpu, start, site)
                assert cpu.reg_read(UC_ARM_REG_R0) == read_word(cpu, BASE + table + 4 * index)
        rows.append(dict(call_site=BASE + site, target=0x0205528C, scope=label,
                         supported_ids=expected, table_fields=seals))
    start, site = 0x5C1C0, 0x5C1CC
    seals = [lock(ja, en, a, b) for a, b in ((start, site + 4), (0x5C45C, 0x5C460))]
    assert unpack_from('<I', ja, 0x5C45C) == (3658,)
    for raw in (ja, en):
        cpu = machine(raw)
        for index in range(10):
            cpu.reg_write(UC_ARM_REG_R5, index)
            run_to(cpu, start, site)
            assert cpu.reg_read(UC_ARM_REG_R1) == 3658 + index
    rows.append(dict(call_site=BASE + site, target=0x02053FE4, scope='ten registered Ancient Map artifact indices',
                     supported_ids=list(range(3658, 3668)), table_fields=seals))
    return rows


def sound_titles(ja, en):
    spans = ((0x108FC0, 0x108FE0), (0x1090D0, 0x1090D8), (0x109268, 0x109278), (0x109308, 0x10930C))
    locks = [lock(ja, en, a, b) for a, b in spans]
    case_count = 0
    for raw in (ja, en):
        cpu = machine(raw)
        cpu.reg_write(UC_ARM_REG_R5, VIEW)
        run_to(cpu, 0x1090D0, 0x1090D8)
        assert read_word(cpu, VIEW + 0x108) == 2
        for index in range(2, 40):
            cpu.mem_write(VIEW + 0x108, pack('<I', index))
            run_to(cpu, 0x109268, 0x109274)
            assert cpu.reg_read(UC_ARM_REG_R0) == 3249 + index
            for delta in (-1, 1):
                cpu.mem_write(VIEW + 0x108, pack('<I', index))
                cpu.reg_write(UC_ARM_REG_R4, VIEW)
                cpu.reg_write(UC_ARM_REG_R1, delta & STOP_MASK)
                run_to(cpu, 0x108FC0, 0x108FE0)
                assert read_word(cpu, VIEW + 0x108) == 2 + (index - 2 + delta) % 38
                case_count += 1
    return dict(call_site=0x02109274, target=0x0205528C, scope='Sound Setup music index and forward/back wrap',
                supported_ids=list(range(3251, 3289)), code_locks=locks, press_cases=case_count)


def square(ja, en, runtime):
    locks = [lock(ja, en, a, b) for a, b in ((0x5FA18, 0x5FB50), (0xB51B4, 0xB51CC),
        (0xB5690, 0xB56A8))]
    cpu, get, provider = runtime.machine(en, runtime.common, runtime.raw, runtime.plan)
    town_root = get(0xCB178)
    towns = []
    share = 0

    def flag(u, _pc, _size, _data):
        u.reg_write(UC_ARM_REG_R0, share)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, flag, begin=BASE + 0xB4A88, end=BASE + 0xB4A88)
    try:
        for index in range(114):
            town = town_root + 4 + index * 108
            info = get(0xB5690, town)
            assert info == BASE + 0x122560 + index * 0x74
            culture = en[info - BASE + 0x15]
            assert ja[info - BASE + 0x15] == culture and 0 <= culture <= 20 and get(0xB51B4, town) == culture
            ids = []
            for share, initial in ((0, 709), (1, 688)):
                selected = get(0x5FA60, 0, town)
                assert selected == initial + culture
                ids.append(selected)
            towns.append(dict(town=index, data_pointer=info, culture_index=culture, message_ids=ids))
    finally:
        cpu.hook_del(hook)
    assert not provider.opens and not provider.reads
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    return dict(call_site=0x0205FA4C, target=0x02053FE4, scope='all 114 native town records; original culture getter with both share branches',
        supported_ids=sorted({n for row in towns for n in row['message_ids']}), towns=towns, code_locks=locks)


def square_conditions(ja, en):
    bounds = lock(ja, en, 0x5FA18, 0x5FB54)
    expected = (682, 683, 684, 685, 686, 687, 687, 687, 687, 687, 687, 687, 658, 687, 687)
    choices = dict(zip((*range(14), STOP_MASK), expected, strict=True))
    state = 0

    def town_state(u, _pc, _size, _data):
        u.reg_write(UC_ARM_REG_R0, state)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    for arm in (ja, en):
        cpu = machine(arm)
        hook = cpu.hook_add(UC_HOOK_CODE, town_state, begin=0x020B2E04, end=0x020B2E04)
        try:
            for state, message in choices.items():
                call(cpu, 0x5FA98, (0, VIEW))
                assert cpu.reg_read(UC_ARM_REG_R0) == message
        finally:
            cpu.hook_del(hook)
    return dict(call_site=0x0205FA2C, target=0x02053FE4, scope='Square special town-state selector',
                supported_ids=sorted(set(expected)), state_fixtures=choices, code=bounds)


def unchanged_item_routes(en):
    earlier, observed = map(base.load, (inventory.current.RELEASE, inventory.OUTPUT))
    assert sha(en) == earlier['target_ARM9_sha256'] and observed['candidate_sha256'] == earlier['candidate_sha256']
    cards = observed['current_thumb_and_owned_table_routes']
    first, last = cards['source_card_original_supported_ids']
    sites = cards['source_card_origins']
    assert (first, last, sites) == (2815, 3032, [0x0204D834, 0x0204E50C])
    return [dict(call_site=site, target=0x0205528C, scope='original supported item catalogue and current relocated getter',
                 supported_ids=list(range(first, last + 1)), earlier_receipt=str(inventory.OUTPUT)) for site in sites]


def fixed_caller_tails(ja, en):
    switch = [lock(ja, en, a, b) for a, b in ((0x16868, 0x169F0), (0x16A00, 0x16A10))]
    pointers = [unpack_from('<4I', arm, 0x169F0) for arm in (ja, en)]
    strings = []
    for i, (source, current_pointer) in enumerate(zip(*pointers, strict=True)):
        fields = {}
        for scope, pointer, arm in (('clean', source, ja), ('current', current_pointer, en)):
            at = pointer - BASE
            body = arm[at:arm.index(0, at)]
            fields[scope] = dict(pointer=pointer, text=body.decode('cp932'), terminated_hex=(body + b'\0').hex())
        strings.append(dict(pointer_field=BASE + 0x169F0 + 4 * i, **fields))
    scheduled = lock(ja, en, 0xAEA7C, 0xAEAA8)
    switch_results = []
    for arm, slots in zip((ja, en), pointers, strict=True):
        cpu = machine(arm)
        selected = []

        def capture(u, _pc, _size, _data):
            selected.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, capture, begin=0x0205528C, end=0x0205528C)
        results = []
        try:
            for request in (-(2 ** 31), *range(-1, 35), 2 ** 31 - 1):
                for variant in (*range(10), STOP_MASK):
                    selected.clear()
                    call(cpu, 0x16868, (request & STOP_MASK, variant))
                    assert len(selected) <= 1
                    result = cpu.reg_read(UC_ARM_REG_R0)
                    if selected:
                        assert result == selected[0] and 0 <= result <= 3667
                    else:
                        assert result in slots
                    results.append(dict(request=request, variant=variant, loaded_COMMON=selected[:],
                                        direct_text_slot=slots.index(result) if not selected else None))
        finally:
            cpu.hook_del(hook)
        switch_results.append(results)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.mem_write(STACK + 4, pack('<I', VIEW))
        run_to(cpu, 0xAEA7C, 0xAEAA4)
        assert cpu.reg_read(UC_ARM_REG_R1) == read_word(cpu, STACK + 0xC) == 1264
    assert switch_results[0] == switch_results[1]
    supported = sorted({n for row in switch_results[0] for n in row['loaded_COMMON']})
    return [dict(call_site=0x020169BC, target=0x0205528C, scope='original signed request and unsigned variant switch',
                 supported_ids=supported, code=switch, selector_cases=switch_results[0], independent_ARM9_strings=strings),
            dict(call_site=0x020AEAA4, target=0x02053FE4, scope='ship name prompt from local stack initialization',
                 supported_ids=[1264], code=scheduled)]


def main():
    assert not OUTPUT.exists()
    prior = base.load(previous.OUTPUT)
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256'] == prior['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256'] == prior['clean_sha256']
    clean_image, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    ja, en = clean_image.read_file(ARM), active.read_file(ARM)
    assert sha(en) == release['target_ARM9_sha256']
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    _, get, provider = runtime.machine(en, runtime.common, runtime.raw, runtime.plan)
    voice_counts = Counter(get(0x7E988, runtime.actor_root + 4 + 32 * n) for n in range(207))
    assert set(voice_counts) == set(range(8)) and not provider.opens and not provider.reads
    voices, voice_context = voice_tables(ja, en)
    rows = voices + ancient_maps(ja, en) + [sound_titles(ja, en), square(ja, en, runtime), square_conditions(ja, en)]
    rows.extend(unchanged_item_routes(en))
    rows.extend(fixed_caller_tails(ja, en))
    historical_source = base.load(inventory.LEGACY)
    pending = set(historical_source['pending_ids'])
    assert all(pending.isdisjoint(row['supported_ids']) for row in rows)
    sites = {row['call_site'] for row in rows}
    remaining = set(prior['unresolved_sites_after_this_receipt'])
    assert len(rows) == len(sites) and sites <= remaining
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        source_conditions_and_runtime_scope_are_per_consumer=True, cases=rows,
        voice_selector_source=voice_context, stock_actor_native_voice_counts=voice_counts,
        remaining_prior_site_inventory=sorted(remaining - sites),
        source_table_sites_resolved=len(sites), remaining_shared_keys=len(pending), new_editorial_credit=0,
        new_gameplay_runs=0, other_possible_callers_open=True, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (inventory.LEGACY, inventory.OUTPUT, previous.OUTPUT, current.RELEASE, Path(__file__))}))
    print(f'Bound {len(sites)} table-driven sites. {len(remaining - sites)} leads remain in this historical site list.')


if __name__ == '__main__':
    main()
