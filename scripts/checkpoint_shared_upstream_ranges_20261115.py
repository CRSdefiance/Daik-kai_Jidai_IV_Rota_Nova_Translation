"""Reconcile known and bounded incoming arguments for shared-text forwarding."""

from collections import Counter
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import checkpoint_shared_fixed_arguments_20261115 as fixed
from scripts import checkpoint_shared_selector_ranges_20261115 as stock
from scripts import checkpoint_shared_table_callers_20261115 as tables
from scripts import checkpoint_shared_wrapper_inputs_20261115 as prior
from scripts.inventory_native_common_extended_calls import ALL_TARGETS, joined_context_argument
from work.current_amsterdam_square_20261114_v1 import scan_legacy_registers as flow
from work.current_amsterdam_square_20261114_v1 import scan_legacy_tables as voice


base, current, BASE = prior.base, prior.current, prior.BASE
OUTPUT = prior.OUTPUT.with_name('shared_upstream_ranges_20261115_v1.json')


def known_outputs(candidate):
    receipts = {
        fixed.OUTPUT: ('conditional_argument_sites', 'stack_argument_sites'),
        stock.OUTPUT: ('crew_index', 'crew_role_tables', 'catalogue', 'actor_lookup_and_shipyard'),
        tables.OUTPUT: ('cases',),
    }
    result = {}
    for path, groups in receipts.items():
        data = base.load(path)
        assert data['candidate_sha256'] == candidate
        for group in groups:
            for row in data[group]:
                result[row['call_site']] = dict(ids=row['supported_ids'], receipt=str(path))
    return result, receipts


def finite_arguments(clean, deployed, address, register, decoder):
    original, current = [flow.window(arm, address, register) for arm in (clean, deployed)]
    if original and current and original['values'] == current['values']:
        return original['values'], 'bounded control flow', dict(clean=original, candidate=current)

    start, end = address - BASE - 64, address - BASE
    if clean[start:end + 4] != deployed[start:end + 4]:
        return None, None, dict(reason='local instructions differ')
    context = list(decoder.disasm(clean[start:end], BASE + start))
    if len(context) != (end - start) // 4 or any(not row.id for row in context):
        return None, None, dict(reason='local instructions unbound')
    values = [joined_context_argument(context, arm, BASE, register) for arm in (clean, deployed)]
    if values[0] is None or values[0] != values[1]:
        return None, None, dict(reason='no finite matched local argument')
    return values[:1], 'bounded instruction tail', dict(start=BASE + start,
        end=address + 4, matched_code_sha256=tables.sha(clean[start:end + 4]))


def classify(ja, en, incoming, native, pending):
    unresolved, scoped, leads = [], [], []
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    decoder.skipdata = True
    remaining = set(incoming['entries_with_other_upstream_sites'])
    for address, entry, kind, component in incoming['all_shared_reference_candidates']:
        if entry not in remaining:
            continue
        row = dict(address=address, entry=entry, kind=kind, component=component)
        if kind != 'arm_bl' or component != 'ARM9 section 0':
            unresolved.append(dict(**row, reason='pointer or non-primary ARM call form'))
            continue
        if address in native:
            group = native[address]
            ids = group['ids']
            basis, proof = 'previously checked native selector', dict(receipt=group['receipt'])
        else:
            register, width = voice.NATIVE.get(entry, (ALL_TARGETS.get(entry), None))
            assert register in ('r0', 'r1')
            values, basis, proof = finite_arguments(ja, en, address, register, decoder)
            if values is None:
                unresolved.append(dict(**row, **proof))
                continue
            ids = values
            if width:
                groups = [voice.load_table(ja, value, width) for value in values]
                if not all(slots and slots == voice.load_table(en, pointer, width)
                           for slots, pointer in zip(groups, values, strict=True)):
                    unresolved.append(dict(**row, reason='missing or changed selector table', pointers=values))
                    continue
                proof['typed_tables'] = [{'address': pointer, 'slots': slots}
                                        for pointer, slots in zip(values, groups, strict=True)]
                ids = sorted({n for slots in groups for n in slots if n >= 0})
        if not ids or min(ids) < 0 or max(ids) > 3667:
            unresolved.append(dict(**row, reason='output outside the mapped catalogue', values=ids))
            continue
        hits = sorted(pending.intersection(ids))
        scoped.append(dict(**row, basis=basis, ids=ids, pending_hits=hits, proof=proof))
        if hits:
            leads.append(dict(**row, pending_ids=hits))
    return scoped, unresolved, leads


def main():
    assert not OUTPUT.exists()
    incoming, release = map(base.load, (prior.OUTPUT, current.RELEASE))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    candidate = base.digest(current.ROM)
    assert candidate == incoming['candidate_sha256'] == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == incoming['clean_sha256'] == release['clean_input_sha256']
    ja, en = (base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, current.ROM))
    pending = set(base.load(prior.producer.inventory.LEGACY)['pending_ids'])
    reused, dependencies = known_outputs(candidate)
    accepted, unresolved, leads = classify(ja, en, incoming, reused, pending)
    assert len(accepted) + len(unresolved) == len(incoming['all_shared_reference_candidates']) - 7
    assert any(row['address'] == 0x02063154 and row['ids'] == [804] for row in accepted)
    assert all(any(row['address'] == address and row['ids'] == [ident] for row in accepted)
               for address, ident in ((0x02041F6C, 98), (0x02041FD8, 99)))
    summary = [dict(entry=entry, inputs_with_finite_outcomes=sum(row['entry'] == entry for row in accepted),
                    other_inputs=sum(row['entry'] == entry for row in unresolved))
               for entry in incoming['entries_with_other_upstream_sites']]
    dependencies = [*dependencies, prior.OUTPUT, current.RELEASE, Path(flow.__file__), Path(voice.__file__), Path(__file__)]
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=incoming['clean_sha256'],
        reference_outcomes=accepted, by_entry=summary, still_unbound_reference_candidates=unresolved,
        pending_hits=leads, counts_by_proof=dict(Counter(row['basis'] for row in accepted)),
        other_clean_reference_candidates=incoming['clean_only_reference_candidates'],
        other_current_reference_candidates=incoming['current_only_reference_candidates'],
        remaining_shared_keys=len(pending), new_gameplay_runs=0, new_dialogue_credit=0, full_goal_complete=False,
        scope='Bounded inputs and typed table slots. Computed entries, roles outside verified stock inputs, and actual display are outside this audit.',
        evidence={str(path): base.digest(path) for path in dependencies}))
    print(f'Matched finite values at {len(accepted)} incoming references. {len(unresolved)} shared references remain unbound.')
    print(f'Pending-key leads in scope: {leads}')


if __name__ == '__main__':
    main()
