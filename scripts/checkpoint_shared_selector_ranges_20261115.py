"""Resolve the remaining known stock inputs to shared-text selectors offline."""

from pathlib import Path
from struct import pack, unpack_from

from capstone import CS_AC_WRITE, CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm_const import ARM_OP_MEM, ARM_REG_SP
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R8, UC_ARM_REG_SP,
)

from scripts import checkpoint_shared_fixed_arguments_20261115 as previous
from scripts import checkpoint_shared_message_producers_20261115 as producer
from scripts import checkpoint_shared_table_callers_20261115 as shared
from scripts import register_market_trade_dialogue_20261115 as current
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, call, machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_item_production_advice_v1 import CALLERS, FIRST


base = current.base
OUTPUT = previous.OUTPUT.with_name('shared_selector_ranges_20261115_v1.json')
STOCK_ACTOR_COUNT, FALLBACK = 207, 0xFFFFFFFF


def native_return(cpu, offset, value):
    def callback(u, _address, _size, _data):
        u.reg_write(UC_ARM_REG_R0, value)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    return cpu.hook_add(UC_HOOK_CODE, callback, begin=BASE + offset, end=BASE + offset)


def crew_index(ja, en):
    rows = []
    span = producer.literal_dependencies
    cpus = [machine(arm) for arm in (ja, en)]
    for start, site, first in ((0x1228C, 0x12294, 1361), (0x12754, 0x1275C, 1571), (0x128E8, 0x128F0, 1361)):
        for cpu in cpus:
            for index in range(STOCK_ACTOR_COUNT):
                cpu.reg_write(UC_ARM_REG_R4, index)
                shared.run_to(cpu, start, site)
                assert cpu.reg_read(UC_ARM_REG_R0) == first + index
        rows.append(dict(call_site=BASE + site, supported_ids=list(range(first, first + STOCK_ACTOR_COUNT)),
                         scope='stock actor indices supplied to arithmetic', code=span(ja, en, start, site + 4)))

    predicate_lock = shared.lock(ja, en, 0x4A224, 0x4A230)
    for start, site, first, special in ((0x126A8, 0x12704, 1571, (1885, 1886, 1887, 1888)),
                                        (0x12838, 0x12894, 1361, (1881, 1882, 1883, 1884))):
        results = set()
        for cpu in cpus:
            loaded = native_return(cpu, 0xCB190, VIEW)
            seen = []

            def fetch(u, _address, _size, _data):
                seen.append(u.reg_read(UC_ARM_REG_R0))
                u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

            fetched = cpu.hook_add(UC_HOOK_CODE, fetch, begin=0x0205528C, end=0x0205528C)
            try:
                for index in range(STOCK_ACTOR_COUNT):
                    for item_flag in ((0, 4) if index == 27 else (0,)):
                        cpu.mem_write(VIEW + 0x1A5, bytes([item_flag]))
                        seen.clear()
                        call(cpu, start, (index,))
                        expected = special[index - 25 + bool(item_flag)] if 25 <= index <= 27 else first + index
                        assert seen == [expected], (hex(site), index, item_flag, seen)
                        results.add(expected)
            finally:
                cpu.hook_del(fetched)
                cpu.hook_del(loaded)
        rows.append(dict(call_site=BASE + site, supported_ids=sorted(results),
            scope='complete original selector with stock actor input and both item flags for actor 27',
            code=span(ja, en, start, site + 12) + [predicate_lock]))
    return rows


def crew_roles(ja, en):
    rows = []
    for start, site, literal, size in ((0x12674, 0x1268C, 0x126A4, 8), (0x12800, 0x12818, 0x12834, 8),
                                      (0x12764, 0x12770, 0x12788, 4), (0x128F8, 0x12904, 0x1291C, 4)):
        table = unpack_from('<I', ja, literal)[0] - BASE
        locks = producer.literal_dependencies(ja, en, start, site + 4)
        locks.append(shared.lock(ja, en, table, table + 21 * 4))
        loops = {8: (0x53F4C, 0x53F9C), 4: (0x53C6C, 0x53CB0)}
        locks.append(shared.lock(ja, en, *loops[size]))
        if size == 4:
            locks.append(shared.lock(ja, en, 0x7F244, 0x7F254))
        offsets = unpack_from('<21I', ja, table)
        supported = {}
        for role, ptr in enumerate(offsets):
            if not ptr:
                continue
            offset = ptr - BASE
            locks.append(shared.lock(ja, en, offset, offset + size * 4))
            slots = unpack_from(f'<{size}I', ja, offset)
            default = next(value for value in slots if value != FALLBACK)
            supported[role] = [default if value == FALLBACK else value for value in slots]
        for arm in (ja, en):
            cpu = machine(arm)
            for role, expected in supported.items():
                for index, value in enumerate(expected):
                    if size == 8:
                        voice = native_return(cpu, 0x7E988, index)
                        cpu.reg_write(UC_ARM_REG_R4, VIEW)
                        cpu.reg_write(UC_ARM_REG_R5, role)
                        shared.run_to(cpu, start, site)
                        cpu.hook_del(voice)
                    else:
                        state = unpack_from('<I', arm, 0x7F250)[0]
                        cpu.mem_write(state + 0x48, pack('<I', index))
                        cpu.reg_write(UC_ARM_REG_R0, role)
                        shared.run_to(cpu, start, site)
                    assert cpu.reg_read(UC_ARM_REG_R0) == value, (hex(site), role, index)
        rows.append(dict(call_site=BASE + site, role_and_voice_or_route_ids=supported, code=locks,
            null_roles=[role for role, ptr in enumerate(offsets) if not ptr],
            supported_ids=sorted({value for choices in supported.values() for value in choices})))
    return rows


def catalogue(ja, en, runtime):
    prior_cards = shared.unchanged_item_routes(en)
    assert len(prior_cards) == 2 and all(len(row['supported_ids']) == 218 for row in prior_cards)
    stock_count = shared.lock(ja, en, 0x49B48, 0x49BA0)
    assert unpack_from('<I', ja, 0x49B98) == (0xE35400DA,)
    cpu, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    rows = []
    for screen, literal, index_reg, branches in CALLERS:
        assert unpack_from('<I', ja, literal) == (FIRST,)
        for adviser, (start, site) in zip((75, 76), branches, strict=True):
            assert producer.inventory.branch_hits(ja[site:site + 4], BASE + site, {0x02053FE4})
            locks = producer.literal_dependencies(ja, en, start, site + 4)
            for index in range(218):
                cpu.reg_write(index_reg, index)
                shared.run_to(cpu, start, site)
                assert cpu.reg_read(UC_ARM_REG_R0) == runtime.actor_root + 4 + 32 * adviser
                assert cpu.reg_read(UC_ARM_REG_R1) == FIRST + index
            rows.append(dict(call_site=BASE + site, screen=screen, speaker=adviser, supplied_item_indices=[0, 217],
                supported_ids=list(range(FIRST, FIRST + 218)), code=locks + [stock_count]))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    return rows


def actor_and_shipyard(ja, en, runtime):
    cpu, getter, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    issued = []
    for index in range(STOCK_ACTOR_COUNT):
        actor = runtime.actor_root + 4 + 32 * index
        result = getter(0x7EE08, actor)
        assert result == index, (index, result)
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_R4, actor)
        shared.run_to(cpu, 0x58F34, 0x58F40)
        assert cpu.reg_read(UC_ARM_REG_R0) == actor
        assert cpu.reg_read(UC_ARM_REG_R1) == 863 + index
        issued.append(863 + index)
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    actor_lock = producer.literal_dependencies(ja, en, 0x58F24, 0x58F44)
    actor_lock += [shared.lock(ja, en, 0x7EE08, 0x7EE20), shared.lock(ja, en, 0x7F1F4, 0x7F254)]

    # The numeric formatter changes between the ROMs. Execute each one in its
    # caller and confirm that neither changes the message index stored by that caller.
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    writes = [insn.address for insn in decoder.disasm(ja[0x63040:0x63148], BASE + 0x63040)
              if any(op.type == ARM_OP_MEM and op.mem.base == ARM_REG_SP and op.mem.disp == 0x18
                     and op.access & CS_AC_WRITE for op in insn.operands)]
    assert writes == [0x02063040]
    locks = [shared.lock(ja, en, 0x63038, 0x63140), shared.lock(ja, en, 0x63144, 0x63158)]
    cases = []
    for arm in (ja, en):
        cpu = machine(arm)
        native_return(cpu, 0xAC000, VIEW)
        for price in (0, 1, 499, 50000, 999999):
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            shared.run_to(cpu, 0x63038, 0x63044)
            cpu.reg_write(UC_ARM_REG_R8, price)
            cpu.emu_start(0x0206313C, 0x02063154, count=2000)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02063154
            assert cpu.reg_read(UC_ARM_REG_R1) == 804 and cpu.reg_read(UC_ARM_REG_SP) == STACK
            cases.append(price)
    return [dict(call_site=0x02058F40, supported_ids=issued, code=actor_lock,
                 original_getter=0x0207EE08, initialized_stock_actor_inputs=STOCK_ACTOR_COUNT),
            dict(call_site=0x02063154, supported_ids=[804], code=locks, formatter_cases=len(cases),
                 scratch_buffer_fixture=True)]


def main():
    assert not OUTPUT.exists()
    old, release = map(base.load, (previous.OUTPUT, current.RELEASE))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == old['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == old['clean_sha256'] == release['clean_input_sha256']
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    ja, en = base.NdsImage.open(current.stage.CLEAN).read_file(current.stage.ARM), runtime.arm
    index, roles = crew_index(ja, en), crew_roles(ja, en)
    items, other = catalogue(ja, en, runtime), actor_and_shipyard(ja, en, runtime)
    pending = set(base.load(producer.inventory.LEGACY)['pending_ids'])
    scoped = index + roles + items + other
    assert len(scoped) == 17 and {row['call_site'] for row in scoped} == set(old['open_message_sources'])
    hits = {row['call_site']: sorted(pending.intersection(row['supported_ids'])) for row in scoped
            if pending.intersection(row['supported_ids'])}
    assert not hits, hits
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        crew_index=index, crew_role_tables=roles, catalogue=items, actor_lookup_and_shipyard=other,
        known_stock_inputs_resolved=[row['call_site'] for row in scoped], supported_scope_pending_hits=hits,
        remaining_shared_keys=len(pending), historical_forwarders=old['forwarding_sites_open_upstream'],
        scope_limits=['Four role-table call sites have null slots with no input evidence for those slots.',
            'The item advice menu is not replayed with every supplied stock catalogue index.',
            'Indirect producers and custom or unsupported model inputs remain outside these stock checks.'],
        new_dialogue_credit=0, new_gameplay_runs=0, full_goal_complete=False, runtime=runtime.receipt(),
        evidence={str(p): base.digest(p) for p in (previous.OUTPUT, current.RELEASE, Path(__file__))}))
    print(f'Bound supported stock outcomes at {len(scoped)} sites. No supported outcomes reached a pending key.')


if __name__ == '__main__':
    main()
