"""Execute compiled native layout against independent DP and memory guards."""
from pathlib import Path
import struct

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1134 import layout
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_native_layout_v1134')
INPUT, CODE = 0x02468000, 0x02470000


def elf_functions(raw):
    shoff = struct.unpack_from('<I', raw, 32)[0]
    entsize, count = struct.unpack_from('<HH', raw, 46)
    sections = [struct.unpack_from('<10I', raw, shoff + index * entsize) for index in range(count)]
    symbols = []
    for section in sections:
        if section[1] != 2:
            continue
        strings = sections[section[6]]
        names = raw[strings[4]:strings[4] + strings[5]]
        for at in range(section[4], section[4] + section[5], section[9]):
            name, value, size, info, other, index = struct.unpack_from('<IIIBBH', raw, at)
            label = names[name:].split(b'\0')[0].decode('ascii')
            if value >= CODE and (label.startswith('$') or info & 15 == 2):
                symbols.append({'name': label, 'address': value, 'bytes': size, 'kind': info & 15})
    return symbols


def main():
    assert not ROOT.exists()
    compiler_path = Path('work/analysis/duel_layout_native_v1133/compiler_provenance.json')
    compiler = read(compiler_path)
    binary = Path(compiler['binary']).read_bytes()
    assert sha(binary) == compiler['binary_sha256'] and compiler['entry'] == CODE | 1
    assert sha(Path(compiler['source']).read_bytes()) == compiler['source_sha256']
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    prior = read('work/analysis/duel_full_name_fonts_v1119/all4160_source_name_layouts_corrected_phase.json')
    rom_path = Path('out/all_routes_combined_v1105_candidate.nds')
    assert sha(rom_path.read_bytes()) == catalog['candidate_sha256']
    arm = NdsImage.open(rom_path).read_file('/__arm9__.bin')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    cpu, get = get_machine(arm, raw)
    cpu.mem_write(CODE, binary)
    stores = {'calls': 0, 'input_low': 1024, 'input_high': 0, 'deepest_stack_bytes': 0}

    def memory(u, access, address, size, value, data):
        if INPUT <= address and address + size <= INPUT + 1024:
            stores['input_low'] = min(stores['input_low'], address - INPUT)
            stores['input_high'] = max(stores['input_high'], address + size - INPUT)
        elif STACK - 512 <= address and address + size <= STACK:
            stores['deepest_stack_bytes'] = max(stores['deepest_stack_bytes'], STACK - address)
        else:
            raise AssertionError(f'Native formatter escaped private input/stack:{address:#x}+{size}')
        stores['calls'] += 1

    hook = cpu.hook_add(UC_HOOK_MEM_WRITE, memory)
    ROOT.mkdir(parents=True)
    negatives = [b'', b' Leading', b'Trailing ', b'Two  spaces', b'Line\nBreak', b'Tab\tBreak',
                 b'A' * 25, b'\x82', b'\x82\x20', b'\xa0', b'Q' * 200,
                 b' '.join([b'A'] * 33), b' '.join([b'Longword'] * 12)]
    rejected = []
    for text in negatives:
        cpu.mem_write(INPUT - 16, b'\xa5' * 1056)
        cpu.mem_write(INPUT, text + b'\0')
        call(cpu, compiler['entry'] - 0x02000000, [INPUT], instruction_limit=3000000)
        assert cpu.reg_read(UC_ARM_REG_R0) == 0
        assert bytes(cpu.mem_read(INPUT, len(text) + 1)) == text + b'\0'
        assert bytes(cpu.mem_read(INPUT - 16, 16)) == bytes(cpu.mem_read(INPUT + 1024, 16)) == b'\xa5' * 16
        rejected.append({'input_hex': text.hex(), 'rejected_without_text_or_guard_change': True,
                         'stack_and_callee_saved_registers_exact': True})
    cases = []
    for item in catalog['all4160_complete_word_layouts']:
        cases.append((item['actor_slot'], item['message_ID'], bytes.fromhex(item['paragraph_hex']), 'source'))
    records = [row for row in read('translations/duel_editorial_manuscript_v3.json')['records'] if row['message_id'] < 1951]
    arguments = [b'Abcdefghijklmnop'[:count] for count in range(1, 17)]
    arguments += [b'\x82\x60' * count for count in range(1, 9)]
    arguments += [b'a' + b'\x82\x60' * 7 + b'z', b'\x82\x60' * 4 + b'BCDEFGHI', b'A B C D E F G H']
    for index, argument in enumerate(arguments):
        for record in records:
            cases.append((index, record['message_id'], record['english'].encode('ascii').replace(b'%s', argument), 'legal-name-stress'))
    assert len(cases) == 4700
    rows = []
    for slot, number, text, kind in cases:
        expected, lines = layout(text)
        cpu.mem_write(INPUT - 16, b'\xa5' * 1056)
        cpu.mem_write(INPUT, text + b'\0')
        call(cpu, compiler['entry'] - 0x02000000, [INPUT], instruction_limit=3000000)
        count = cpu.reg_read(UC_ARM_REG_R0)
        actual = bytes(cpu.mem_read(INPUT, 128)).split(b'\0')[0]
        if count != len(lines) or actual != expected:
            save(ROOT / 'first_native_reference_failure.json', {'slot': slot, 'message_ID': number,
                'input_hex': text.hex(), 'native_rows': count, 'native_hex': actual.hex(),
                'expected_rows': len(lines), 'expected_hex': expected.hex(), 'kind': kind})
            raise AssertionError('Native formatter/reference mismatch;retained failure proof')
        assert bytes(cpu.mem_read(INPUT - 16, 16)) == bytes(cpu.mem_read(INPUT + 1024, 16)) == b'\xa5' * 16
        if kind == 'source':
            assert expected.hex() == prior['layouts'][len(rows)]['generated_hex']
        rows.append({'slot': slot, 'message_ID': number, 'kind': kind, 'input_hex': text.hex(),
                     'generated_hex': actual.hex(), 'lines': lines,
                     'native_rows_and_all_generated_bytes_equal_independent_DP': True,
                     'only_owned1024_bytes_and_bounded_stack_written': True})
        if len(rows) % 500 == 0:
            print(f'Compiled native DP completed:{len(rows)}/4700', flush=True)
    cpu.hook_del(hook)
    assert bytes(cpu.mem_read(CODE, len(binary))) == binary
    functions = elf_functions(Path(compiler['ELF']).read_bytes())
    assert all(row['address'] & 1 for row in functions if row['kind'] == 2)
    proof = ROOT / 'compiled_native_DP_matrix.json'
    save(proof, {'compiler_provenance': str(compiler_path), 'compiler_provenance_sha256': sha(compiler_path.read_bytes()),
        'candidate': str(rom_path), 'candidate_sha256': catalog['candidate_sha256'],
        'all4700_native_outputs_match_independent_physical_phase_DP': True,
        'all4160_source_outputs_exact_to_prior_complete_font_reference': True,
        'legal_name_stress540_cases_include1to16ASCII_1to8doublebyte_mixed_and_spaced_names': True,
        'all13_invalid_inputs_reject_without_changing_input_or_guards': rejected,
        'cases': rows, 'native_memory_write_bounds': stores, 'ELF_functions_and_mapping_symbols': functions,
        'compiled_code_and_readonly_table_remain_exact': True,
        'actual_native_function_executes_no_Python_layout_boundary_substitution': True,
        'text_after_original_macro_expansion_is_the_declared_input_contract': True,
        'caller_scope_owned_code_placement_native_fonts_registered_integration_and_actual_still_pending': True,
        'no_ROM_registry_or_completion_credit_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    path = Path('translations/editorial_review_current_v1.json')
    ledger = read(path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(compiled_native_formatter_matrix=str(proof),
        native4700_complete_outputs_match_independent_reference=True,
        formatting_status='compiled-native-layout-matrix-pass;owned-placement-font-integration-and-actual-open')
    save(path, ledger)
    print('4700 compiled native DP cases and13 rejection controls pass;owned-placement/fonts/integration/actual gates remain open.')


if __name__ == '__main__':
    main()
