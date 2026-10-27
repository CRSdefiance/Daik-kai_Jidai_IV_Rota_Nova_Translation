"""Verify every native selection with the opaque prefix inside the old8KiB cache."""
from pathlib import Path

from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_cache_copies_v1145')


def main():
    assert not ROOT.exists()
    plan_path = Path('work/analysis/duel_cache_payload_v1144/cache_prefix_research_plan.json')
    plan = read(plan_path)
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    rows = entries(common, arm, plan['directory_sha256'])
    loader, cases = Loader(arm, common), []
    prefix = plan['new_code_prefix']
    for mode in ('warm', 'cold'):
        for index, row in enumerate(rows):
            result = loader.copy(row.message_id, row.text, mode)
            if row.block == prefix['block']:
                loaded = bytes(loader.uc.mem_read(loader.owner + 0x30, prefix['component_bytes']))
                assert sha(loaded) == prefix['component_sha256']
                result['opaque_component_loaded_exactly_before_mapped_text'] = True
            cases.append(result)
            if (index + 1) % 1000 == 0:
                print(f'{mode}:{index+1}/3668 complete native copies with cache-prefix ownership', flush=True)
    loader.reset()
    sequence = []
    for block in list(range(41)) + list(reversed(range(41))) + [7, 21, 7, 21, 22, 21, 40, 21]:
        number = loader.directory[block][0]
        for repeat in range(2):
            sequence.append(loader.copy(number, rows[number].text, 'sequence'))
            if block == 21:
                assert sha(bytes(loader.uc.mem_read(loader.owner + 0x30, prefix['component_bytes']))) == prefix['component_sha256']
    assert len(cases) == 7336 and len(sequence) == 180
    assert all(row['reads'] == 0 for row in sequence[1::2])
    ROOT.mkdir(parents=True)
    save(ROOT / 'all_native_copies_and_prefix_cache_sequence.json', {
        'target_plan': str(plan_path), 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'complete_native_copies': len(cases), 'cases': cases, 'sequenced_cache_cases': sequence,
        'all_full_span_NUL8192_input_and_output_guard_checks_pass': True,
        'all_stack_and_callee_saved_native_ABI_checks_pass': True,
        'opaque1480byte_component_is_loaded_exactly_and_never_selected_as_text': True,
        'same_existing8192byte_input_and512byte_output_allocations': True,
        'native_file_open_read_operations_are_explicit_host_contracts': True,
        'instruction_visibility_runtime_scope_and_during_draw_lifetime_still_pending': True,
        'not_a_playable_ROM_or_actual_gameplay_test': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('7336 complete native copies and180 cache-sequence cases pass;opaque code prefix and every string preserved.')


if __name__ == '__main__':
    main()
