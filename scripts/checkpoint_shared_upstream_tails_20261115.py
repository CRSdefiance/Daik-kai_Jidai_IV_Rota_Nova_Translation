"""Verify the conditional inputs left by the bounded forwarding audit."""

from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_SP

from scripts import checkpoint_shared_crew_and_wrapper_routes_20261115 as crew
from scripts import checkpoint_shared_message_producers_20261115 as producer
from scripts import checkpoint_shared_upstream_ranges_20261115 as prior
from scripts.probe_button_prompt_native import STACK, call


base, current, shared, BASE = prior.base, prior.current, prior.tables, prior.BASE
OUTPUT = prior.OUTPUT.with_name('shared_upstream_tails_20261115_v1.json')
CONDITIONS = (
    (0x1350C, 0x1351C, 4, {0: 1358, 15: 1357}),
    (0x13658, 0x13668, 0, {0: 1360, 1: 1359}),
    (0x59D68, 0x59D78, 0, {0: 819, 1: 818}),
    (0x59D84, 0x59D94, 0, {0: 53, 1: 52}),
    (0x59EF4, 0x59F04, 0, {0: 61, 1: 60}),
    (0x5E10C, 0x5E11C, 0, {0: 1159, 1: 1163}),
    (0x5FBA8, 0x5FBB8, 4, {75: 734, 134: 734, 135: 732, 136: 732}),
    (0xBA354, 0xBA37C, 0, {0: 771, 1: 8, 2: 8, 3: 772, 4: 773, 5: 8, 0xFFFFFFFF: 8}),
    (0xBBED8, 0xBBEE8, 0, {0: 778, 1: 775}),
    (0xBC098, 0xBC0A8, 0, {0: 783, 1: 782}),
    (0xBC0C8, 0xBC0D8, 0, {0: 9, 1: 10}),
    (0x71DC4, 0x71DD4, 4, {0: 0x02117760, 1: 0x021176E0}),
)


def check_tails(ja, en):
    cpus = [shared.machine(arm) for arm in (ja, en)]
    rows = []
    for start, site, input_register, cases in CONDITIONS:
        locks = producer.literal_dependencies(ja, en, start, site + 4)
        register = {0: UC_ARM_REG_R0, 4: UC_ARM_REG_R4}[input_register]
        for cpu in cpus:
            for condition, expected in cases.items():
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.reg_write(register, condition)
                shared.run_to(cpu, start, site)
                assert cpu.reg_read(UC_ARM_REG_R1) == expected
        ids = set(cases.values())
        if site == 0x71DD4:
            locks.append(shared.lock(ja, en, 0x53F4C, 0x53F9C))
            ids.clear()
            for table in cases.values():
                at = table - BASE
                locks.append(shared.lock(ja, en, at, at + 32))
                slots = unpack_from('<8I', ja, at)
                default = next(n for n in slots if n != 0xFFFFFFFF)
                for value, n in enumerate(slots):
                    expected = default if n == 0xFFFFFFFF else n
                    for cpu in cpus:
                        hook = prior.stock.native_return(cpu, 0x7E988, value)
                        call(cpu, 0x53F4C, (shared.VIEW, table))
                        cpu.hook_del(hook)
                        assert cpu.reg_read(UC_ARM_REG_R0) == expected
                    ids.add(expected)
        rows.append(dict(site=BASE + site, register=f'r{input_register}', cases=cases, ids=sorted(ids), code=locks))
    return rows


def main():
    assert not OUTPUT.exists()
    release, previous, work, crew_work = map(base.load, (current.RELEASE, prior.OUTPUT, producer.OUTPUT, crew.OUTPUT))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    candidate = base.digest(current.ROM)
    assert all(data['candidate_sha256'] == candidate for data in (release, previous, work, crew_work))
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256'] == previous['clean_sha256']
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    rows = check_tails(ja, en)
    pending = set(base.load(producer.inventory.LEGACY)['pending_ids'])
    assert all(pending.isdisjoint(row['ids']) for row in rows)
    earlier = {site: str(producer.OUTPUT) for site in work['resolved_call_sites']}
    earlier.update({row['site']: str(crew.OUTPUT) for row in crew_work['crew_selectors']})
    # These two words name previously verified computed destinations.
    earlier.update({0x02059134: str(producer.OUTPUT), 0x020BF334: str(producer.OUTPUT)})
    forwarding = {row['site']: row['entry'] for row in crew_work['forwarding_sites']}
    remaining = {row['address'] for row in previous['still_unbound_reference_candidates']}
    now = {row['site'] for row in rows}
    assert now <= remaining
    left = remaining - now - earlier.keys() - forwarding.keys()
    paths = (prior.OUTPUT, producer.OUTPUT, crew.OUTPUT, current.RELEASE, Path(__file__))
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=previous['clean_sha256'],
        in_scope_conditional_tails=rows, bounded_sites_with_finite_outcomes=len(previous['reference_outcomes']),
        reconciled_previously_checked={site: earlier[site] for site in sorted(remaining & earlier.keys())},
        internal_forwarding={site: forwarding[site] for site in sorted(remaining & forwarding.keys())},
        remaining_common_reference_candidates=[row for row in previous['still_unbound_reference_candidates']
                                               if row['address'] in left],
        retained_other_clean_reference_candidates=previous['other_clean_reference_candidates'],
        retained_other_current_reference_candidates=previous['other_current_reference_candidates'],
        new_gameplay_runs=0, new_dialogue_credit=0, remaining_shared_keys=len(pending), full_goal_complete=False,
        evidence={str(path): base.digest(path) for path in paths}))
    print(f'Checked {len(now)} conditional sites. The matched-reference set has {len(left)} unclassified sites.')


if __name__ == '__main__':
    main()
