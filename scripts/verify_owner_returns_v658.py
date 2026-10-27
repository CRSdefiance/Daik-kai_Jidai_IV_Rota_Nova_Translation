"""Native witnesses for every resolved pure-return context and owner candidate."""

import itertools
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_IP, UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.trace_owner_returns_v658 import apply_expr, finite, load_span, units_for
from scripts.trace_resource_owner_tables_v585 import initialize
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/owner_returns_v658')


def arguments(expression):
    if expression[0] == 'constant':
        return set()
    if expression[0] == 'argument':
        return {expression[1]}
    return set().union(*(arguments(a) for a in expression[1:]))


def main():
    fp, np = ROOT / 'flow_proof.json', ROOT / 'native_leaf_summaries.json'
    flow, native, pre = read(fp), read(np), read(ROOT / 'preflight.json')
    assert flow['script_sha256'] == sha(Path('scripts/trace_owner_returns_v658.py').read_bytes())
    assert flow['native_leaf_summaries_sha256'] == sha(np.read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    historical = read(ROOT / 'flow_fork_provenance.json')
    assert sha(Path(historical['historical_source']).read_bytes()) == historical['historical_source_sha256']
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm, units = units_for(rom)
    _, original_units = units_for(clean)
    summaries = {r['entry']: r for r in native['summaries']}
    assert len(summaries) == 64
    for entry, row in summaries.items():
        data = load_span(units, entry, row['bytes'])
        assert sha(data) == row['code_sha256']
        assert data == load_span(original_units, entry, row['bytes'])
        assert all(load_span(original_units, x['address'], 4) == x['value'].to_bytes(4, 'little')
                   for x in row['PC_literal_reads'])
        assert len(row['independent_native_cases']) == 2 and row['code_and_all_PC_literals_exact_clean']
    u = machine(arm)
    for _, base, data in units:
        u.mem_write(base, data)
    writes, cases = [], []
    hook = u.hook_add(UC_HOOK_MEM_WRITE, lambda cpu, access, at, size, value, unused:
                      writes.append((at, size, value)))
    try:
        for row in flow['flow']['source_bound_pure_leaf_returns']:
            definition = summaries[row['callee']]
            required = sorted(arguments(definition['return_expression']))
            assert all(row['input_values'][name] is not None for name in required)
            products = list(itertools.product(*(row['input_values'][name] for name in required)))
            assert 0 < len(products) <= 1024
            observed = set()
            for product in products:
                inputs = dict(zip(required, product, strict=True))
                args = [inputs.get(name, 0) for name in ('r0', 'r1', 'r2', 'r3')]
                ip = inputs.get('ip', 0)
                u.reg_write(UC_ARM_REG_IP, ip)
                expected = apply_expr(definition['return_expression'], {k: finite((v,)) for k, v in inputs.items()})
                assert expected is not None and len(expected) == 1
                executed = call(u, row['callee'] - 0x02000000, args, instruction_limit=100)
                actual = u.reg_read(UC_ARM_REG_R0)
                assert actual == next(iter(expected)) and row['callee'] in executed and not writes
                observed.add(actual)
            assert observed == set(row['returned_values'])
            cases.append({'instruction': row['instruction'], 'callee': row['callee'],
                          'relevant_inputs': required, 'native_input_combinations': len(products),
                          'all_returned_values': sorted(observed),
                          'complete_native_ABI_and_no_memory_writes': True,
                          'unknown_unused_arguments_filled_zero_only_in_isolated_witness': True,
                          'not_an_observation_of_original_caller_execution': True})
    finally:
        u.hook_del(hook)
    assert len(cases) == 1991
    expected = [0x02085460, 0x0210E1D4, 0x0210E1D8, 0x0210E1DC,
                0x0210EBF0, 0x0210EBF4, 0x0210EBF8]
    assert [r['instruction'] for r in flow['flow']['candidates']] == expected
    assert not any(r['kind'] == 'source_bound_pure_leaf_return' for r in flow['flow']['candidates'])
    original, _, executed, written, owners, names = initialize(clean)
    current, _, actual_executed, actual_written, actual_owners, actual_names = initialize(rom)
    assert (executed, written, owners, names) == (actual_executed, actual_written, actual_owners, actual_names)
    assert all(current.mem_read(pc, 4) == original.mem_read(pc, 4) for pc in executed)
    assert all(pc in executed for pc in expected[1:])
    assert arm[0x85420:0x85480] == clean.read_file('/__arm9__.bin')[0x85420:0x85480]
    before = read('work/analysis/frame_callers_v584/crop_argument_census.json')
    source = next(r for r in before['owner_load_cases'] if r['owner_load'] == 0x02085434)
    assert source['call'] == 0x02085470 and source['source_XYWH'] == [80, 216, 8, 8]
    x, y, w, h = source['source_XYWH']
    footprint = {(xx, yy) for xx in range(x, x + w) for yy in range(y, y + h)}
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    cells = [r for r in batch['records'][15:] if r['text'] not in ('M', 'D')]
    assert len(cells) == 5
    image = PxlImage.from_bytes(rom.read_file('/_pxl/__frame.pxl'))
    for cell in cells:
        l, t, r, b = cell['box']
        assert not footprint & {(xx, yy) for xx in range(l, r) for yy in range(t, b)}
        assert b <= image.height and r <= image.width
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'flow_proof_sha256': sha(fp.read_bytes()), 'native_summaries_sha256': sha(np.read_bytes()),
        'all64_leaf_bodies_and_PC_literals_exact_clean_and128_native_cases_pass': True,
        'all1991_resolved_source_call_return_contexts': cases,
        'total_native_context_witnesses': sum(r['native_input_combinations'] for r in cases),
        'all_relevant_finite_input_combinations_original_return_ABI_and_no_write_pass': True,
        'six_existing_candidates_are_complete_original315_owner_initializer_fields': expected[1:],
        'complete_original_initializer_unique_instructions': len(executed),
        'sole_other_frame_candidate_bound_source_XYWH': source['source_XYWH'],
        'source_rectangle_does_not_intersect_any_five_miniature_cell': True,
        'candidate_owner_addresses_not_new_ordinary_parents': flow['flow']['candidates'],
        'new_return_analysis_does_not_find_any_additional_frame_or_Confirm_owner_candidate': True,
        'historical_V619_implementation_and_all_release_hashes_unchanged': True,
        'next_investigation_should_not_repeat_direct_literals_fixed_styles_or_these_pure_returns': True,
        'remaining_input_memory_Thumb_stack_switch_indirect_and_runtime_alias_readers_not_excluded': True,
        'no_new_emulator_GPU_display_guide_or_global_unused_art_credit': True,
        'all18_original_plaques_incomplete22_historical_scopes_retained': True,
        'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), Path('scripts/trace_owner_returns_v658.py'))}}
    save(ROOT / 'proof.json', proof)
    print(f'V658: {len(cases)} source return contexts/{proof["total_native_context_witnesses"]} native combinations; seven old owner candidates reconciled; actual parents remain open.')


if __name__ == '__main__':
    main()
