"""Resolve original message producers behind dialogue wrappers and Market branches."""

from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_SP,
)

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_continue_legacy_calls_20261115 as continuation
from scripts import checkpoint_pending_shared_native_20261115 as inventory
from scripts import checkpoint_shared_table_callers_20261115 as previous
from scripts import register_market_trade_dialogue_20261115 as current
from scripts import review_market_stock_v755 as market
from scripts.probe_button_prompt_native import BASE, STACK, VIEW, machine
from scripts.review_market_contract_v758 import context_cases
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text


base, sha = current.base, previous.sha
OUTPUT = inventory.ROOT / 'shared_message_producers_20261115_v1.json'
DIRECT = {0xEDE0: (0xEDD0, 1991), 0xEEF4: (0xEEE4, 2146),
          0xF984: (0xF974, 1993), 0xFB8C: (0xFB7C, 1992)}
TABLES = {0xEAFC: (0xEAEC, 0x2117340), 0xEB28: (0xEB18, 0x2117340),
          0xEB7C: (0xEB6C, 0x2117360), 0xEBF8: (0xEBE8, 0x21174E0),
          0x104FC: (0x104EC, 0x21175C0), 0x105F4: (0x105D8, 0x2117560)}
CREW_BRANCHES = {
    0xF368: (0xF2E4, 0xF304, 0xF358, UC_ARM_REG_R8, 'r8', {15: 1988, 20: 1987}),
    0xF5C8: (0xF490, 0xF4BC, 0xF5B8, UC_ARM_REG_R7, 'r7', {7: 1982, 12: 1983}),
    0xF8AC: (0xF7FC, 0xF838, 0xF89C, UC_ARM_REG_R8, 'r8', {9: 1985, 16: 1984, 21: 1986}),
}
MARKET_SITES = {0x020BBD80, 0x020BBE54, 0x020BBEB0, 0x020BBFAC, 0x020BC008}
FALLBACK = 0xFFFFFFFF


def literal_dependencies(ja, en, start, end):
    locks = [previous.lock(ja, en, start, end)]
    for at in range(start, end, 4):
        word, = unpack_from('<I', ja, at)
        if word >> 28 == 15 or word & 0x0F7F0000 != 0x051F0000:
            continue
        delta = word & 0xFFF
        offset = at + 8 + (delta if word & 0x800000 else -delta)
        locks.append(previous.lock(ja, en, offset, offset + 4))
    return locks


def named_branches(ja, en):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    cpus = [machine(raw) for raw in (ja, en)]
    records = []

    def check_call(site, start, value):
        for cpu in cpus:
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.mem_write(STACK, pack('<I', VIEW + 0x100))
            previous.run_to(cpu, start, site)
            assert cpu.reg_read(UC_ARM_REG_R3) == value, (hex(site), hex(value))

    for site, (start, value) in (DIRECT | TABLES).items():
        check_call(site, start, value)
        records.append(dict(call=BASE + site, r3_values=[value], locks=literal_dependencies(ja, en, start, site + 4)))

    choices = {1: 1990, 17: 1989}
    for cpu in cpus:
        for value, expected in choices.items():
            cpu.reg_write(UC_ARM_REG_R0, value)
            previous.run_to(cpu, 0xF128, 0xF160)
            assert cpu.reg_read(UC_ARM_REG_R3) == expected
    records.append(dict(call=0x0200F160, r3_values=list(choices.values()), supplied_actor_ids=choices,
                        locks=literal_dependencies(ja, en, 0xF128, 0xF164)))

    for site, (gate, join, transfer, register, register_name, choices) in CREW_BRANCHES.items():
        for instruction in decoder.disasm(ja[join:transfer], BASE + join):
            assert register_name not in [instruction.reg_name(reg) for reg in instruction.regs_access()[1]], instruction.address
        for cpu in cpus:
            for value, expected in choices.items():
                cpu.reg_write(UC_ARM_REG_R0, value)
                previous.run_to(cpu, gate, join)
                assert cpu.reg_read(register) == expected
                previous.run_to(cpu, transfer, site)
                assert cpu.reg_read(UC_ARM_REG_R3) == expected
        records.append(dict(call=BASE + site, r3_values=list(choices.values()), supplied_actor_ids=choices,
                            locks=literal_dependencies(ja, en, gate, site + 4)))

    for at, value in ((0xFDC4, 1981), (0xFDCC, 1980)):
        check_call(0xFDDC, at, value)
    records.append(dict(call=0x0200FDDC, r3_values=[1981, 1980], locks=literal_dependencies(ja, en, 0xFDC4, 0xFDE0)))
    expected = {(row['call'], 0x0200D458 if row['call'] - BASE in TABLES else 0x0200D4D0, 'arm_bl') for row in records}
    for raw in (ja, en):
        assert set(inventory.branch_hits(raw, BASE, {0x0200D458, 0x0200D4D0})) == expected
    return records


def original_narration(ja, en):
    parents = named_branches(ja, en)
    tables = sorted({table for row in parents if row['call'] - BASE in TABLES for table in row['r3_values']})
    ids = sorted({n for row in parents if row['call'] - BASE not in TABLES for n in row['r3_values']})
    locked = [literal_dependencies(ja, en, lo, hi) for lo, hi in ((0xD458, 0xD490), (0xD4D0, 0xD4FC), (0x53F4C, 0x53F9C))]
    words = {table: unpack_from('<8I', ja, table - BASE) for table in tables}
    assert all(any(n != FALLBACK for n in values) for values in words.values())
    for table, slots in words.items():
        assert unpack_from('<8I', en, table - BASE) == slots
    samples = []
    for raw in (ja, en):
        cpu = machine(raw)
        observed, voice = [], 0

        def intercepted(u, pc, _size, _unused):
            if pc == 0x020AC000:
                u.reg_write(UC_ARM_REG_R0, VIEW + 0x400)
            elif pc == 0x0207E988:
                u.reg_write(UC_ARM_REG_R0, voice)
            elif pc == 0x0205528C:
                observed.append(u.reg_read(UC_ARM_REG_R0))
                u.emu_stop()
                return
            else:
                return
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        hook = cpu.hook_add(UC_HOOK_CODE, intercepted)
        result = []
        try:
            for table, slots in words.items():
                fallback = next(n for n in slots if n != FALLBACK)
                for voice, slot in enumerate(slots):
                    cpu.mem_write(VIEW + 0x34, pack('<I', VIEW + 0x800))
                    cpu.reg_write(UC_ARM_REG_SP, STACK)
                    for reg, value in ((UC_ARM_REG_R0, VIEW), (UC_ARM_REG_R1, 0), (UC_ARM_REG_R2, 0), (UC_ARM_REG_R3, table)):
                        cpu.reg_write(reg, value)
                    cpu.emu_start(BASE + 0xD458, BASE + 0xD48C + 4, count=256)
                    requested, = observed
                    observed.clear()
                    assert requested == (fallback if slot == FALLBACK else slot)
                    result.append(dict(table=table, voice=voice, message_ID=requested))

            for n in ids:
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                for reg, value in ((UC_ARM_REG_R0, VIEW), (UC_ARM_REG_R1, 0), (UC_ARM_REG_R2, 0), (UC_ARM_REG_R3, n)):
                    cpu.reg_write(reg, value)
                cpu.emu_start(BASE + 0xD4D0, BASE + 0xD4F8 + 4, count=256)
                assert observed == [n]
                observed.clear()
        finally:
            cpu.hook_del(hook)
        samples.append(result)
    assert samples[0] == samples[1]
    return dict(primary_loaded_sites=[0x0200D48C, 0x0200D4F8], upstream=parents, wrapper_locks=locked,
                supported_ids=sorted(set(ids) | {r['message_ID'] for r in samples[0]}), native_voice_samples=samples[0],
                direct_message_ids=ids, declared_staff_context_stub=True)


def market_branches(ja, en):
    source = checked_text(getsource(market.fragments), {
        'calls.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))':
            'sites.append(u.reg_read(UC_ARM_REG_LR) - 4)\n                            calls.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))',
    })
    outcomes = []
    for arm in (ja, en):
        sites = []
        scope = vars(market) | {'sites': sites}
        exec(compile(source, __file__ + '::original-market-stock-selectors', 'exec'), scope)
        cases = [row for row in scope['fragments'](arm) if 'call_arguments' in row]
        outcomes.append([row | {'call_site': site} for site, row in zip(sites, cases, strict=True)])
    assert outcomes[0] == outcomes[1]
    bound = [row for row in outcomes[0] if row['call_site'] in MARKET_SITES]
    assert {row['call_site'] for row in bound} == MARKET_SITES
    assert {r['call_arguments'][0] for r in bound} <= {767, 768, 769, 770}
    clean_contract, contract = (context_cases(raw)['contract_facility_cases'] for raw in (ja, en))
    assert all(row['native_call'][0] == 761 for row in clean_contract + contract)
    assert [bytes.fromhex(row['argument_hex']).decode('ascii') for row in contract] == ["Governor's Office", 'Palace']
    assert previous.lock(ja, en, 0xBA3D4, 0xBA3DC)
    return dict(stock=bound, stock_sites=sorted(MARKET_SITES), contract_site=0x020BA428,
                current_contract_input_results=contract, supported_ids=[761, 767, 768, 769, 770])


def main():
    assert not OUTPUT.exists()
    release, old_sites, older = map(base.load, (current.RELEASE, previous.OUTPUT, inventory.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256'] == old_sites['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256'] == old_sites['clean_sha256']
    source, rom = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    ja, en = (image.read_file(current.stage.ARM) for image in (source, rom))
    assert sha(en) == release['target_ARM9_sha256']
    narration = original_narration(ja, en)
    trade = market_branches(ja, en)

    shared = base.load(continuation.OUTPUT)
    assert shared['records'] and older['native_indirect_cases']
    source_slots = common_message_entries(source.read_file(current.stage.COMMON), ja)
    registered = owned_entries(rom.read_file(current.stage.COMMON), en, sha(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    spans = (continuation.SETUP, continuation.BRANCH, (0xEF068, 0xEF06C),
             (0x58F4C, 0x59138), (0xBE51C, 0xBE53C), (0xBF328, 0xBF338))
    inherited = [previous.lock(ja, en, lo, hi) for lo, hi in spans]
    reviewed = {n for row in older['native_indirect_cases'] for n in row['observed_ids']}
    assert reviewed == {998, *range(1003, 1020), *range(137, 261)}
    inherited_sites = (0x020590F8, 0x020BE534, 0x020BF330, 0x020EDF80, 0x020EDF98, 0x020EDFCC)
    used = set(narration['supported_ids']) | set(trade['supported_ids']) | reviewed
    pending = set(base.load(inventory.LEGACY)['pending_ids'])
    assert used.isdisjoint(pending)
    resolved = set(narration['primary_loaded_sites']) | MARKET_SITES | {trade['contract_site'], *inherited_sites}
    remaining = set(old_sites['remaining_prior_site_inventory'])
    assert len(resolved) == 14 and resolved <= remaining
    assert all(0x020BA2C8 <= site <= 0x020BC270 for site in (*MARKET_SITES, trade['contract_site']))
    assert all(not 0x020BA2C8 <= site <= 0x020BC270 for site in remaining - resolved)
    save_warning = next(r for r in shared['records'] if r['id'] == 'COMMON_MESSAGE_111')
    assert save_warning['current_hex'] == registered[111].text.hex()
    rows = [dict(id=n, source_reference=reference(source_slots[n]), current_reference=reference(registered[n]),
                 current_hex=registered[n].text.hex()) for n in (111, *sorted(set(narration['supported_ids']) | {750, 751, 752}))]
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        narration=narration, native_market=trade,
        retained_native_proofs=dict(scope='commodity help, shared switch, and Continue warning returned to a no-op sink',
            sites=list(inherited_sites), code_locks=inherited, discarded_warning_id=111),
        exact_source_and_current_records=rows, resolved_call_sites=sorted(resolved),
        still_open_in_historical_inventory=sorted(remaining - resolved), remaining_shared_keys=len(pending),
        new_dialogue_credit=0, new_gameplay_runs=0, other_possible_callers_open=True, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (previous.OUTPUT, current.RELEASE, continuation.OUTPUT,
                                                   inventory.OUTPUT, Path(__file__))}))
    print(f'Bound {len(resolved)} more call sites, leaving {len(remaining - resolved)} in the historical inventory.')


if __name__ == '__main__':
    main()
