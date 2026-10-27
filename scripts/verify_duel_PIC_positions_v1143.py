"""Execute the PIC formatter at linked and real cache bases with read/write closure."""
from pathlib import Path
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_MEM_READ
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK
from scripts.verify_duel_native_layout_v1134 import elf_functions
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_PIC_positions_v1143')
INPUT = 0x02468000


def main():
    assert not ROOT.exists()
    plan_path = Path('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    plan = read(plan_path)
    binary = Path(plan['binary']).read_bytes()
    assert sha(binary) == plan['binary_sha256']
    symbols = elf_functions(Path(plan['ELF']).read_bytes())
    layout_symbol = next(row for row in symbols if row['name'] == 'duel_layout' and row['kind'] == 2)
    offset = (layout_symbol['address'] & ~1) - 0x02470000
    assert offset == 44
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    arm = NdsImage.open('out/all_routes_combined_v1105_candidate.nds').read_file('/__arm9__.bin')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    matrix_path = Path('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    matrix = read(matrix_path)
    ROOT.mkdir(parents=True)
    positions = []
    for base in (0x02470000, 0x0228E70C, 0x0228E72C):
        cpu, get = get_machine(arm, raw)
        cpu.mem_write(base, binary)
        counts = {'data_reads': 0, 'data_writes': 0, 'deepest_stack': 0}

        def access(u, operation, address, size, value, data):
            if operation == UC_MEM_READ:
                allowed = (base <= address and address + size <= base + len(binary) or
                           INPUT <= address and address + size <= INPUT + 1024 or
                           STACK - 512 <= address and address + size <= STACK)
                counts['data_reads'] += 1
            else:
                allowed = (INPUT <= address and address + size <= INPUT + 1024 or
                           STACK - 512 <= address and address + size <= STACK)
                counts['data_writes'] += 1
            assert allowed, (hex(base), operation, hex(address), size)
            if STACK - 512 <= address < STACK:
                counts['deepest_stack'] = max(counts['deepest_stack'], STACK - address)

        handle = cpu.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, access)
        for index, row in enumerate(matrix['cases']):
            text, expected = bytes.fromhex(row['input_hex']), bytes.fromhex(row['generated_hex'])
            cpu.mem_write(INPUT - 16, b'\xa5' * 1056)
            cpu.mem_write(INPUT, text + b'\0')
            call(cpu, (base + offset | 1) - 0x02000000, [INPUT], instruction_limit=3000000)
            actual = bytes(cpu.mem_read(INPUT, 128)).split(b'\0')[0]
            assert cpu.reg_read(UC_ARM_REG_R0) == len(row['lines']) and actual == expected
            assert bytes(cpu.mem_read(INPUT - 16, 16)) == bytes(cpu.mem_read(INPUT + 1024, 16)) == b'\xa5' * 16
            if (index + 1) % 1500 == 0:
                print(f'PIC base{base:#x}:{index+1}/4700 complete outputs/data-access checks', flush=True)
        cpu.hook_del(handle)
        assert bytes(cpu.mem_read(base, len(binary))) == binary
        positions.append({'base': base, 'layout_entry': base + offset | 1,
                          'all4700_bytes_rows_memory_bounds_and_full_callee_saved_ABI_exact': True,
                          'native_data_access_counts': counts,
                          'no_reads_from_link_address_when_executed_at_another_base': base != 0x02470000})
    proof = ROOT / 'PIC_native_position_matrix.json'
    save(proof, {'compiler_provenance': str(plan_path), 'binary_sha256': sha(binary),
        'component_bytes': len(binary), 'duel_layout_entry_offset': offset,
        'all14100_positioned_native_cases_pass': True, 'positions': positions,
        'data_reads_limited_to_loaded_component_owned_input_and_bounded_stack': True,
        'all_code_and_readonly_data_unchanged_after_each_matrix': True,
        'existing_COMMON_single_cache_base_verified_as_one_position': 0x0228E70C,
        'cache_resident_draw_entry_font_path_scope_and_lifetime_still_pending': True,
        'no_ROM_registry_or_completion_credit_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('14100 PIC layout cases pass at three bases,including existing COMMON cache;scope/lifetime/cache visibility remain open.')


if __name__ == '__main__':
    main()
