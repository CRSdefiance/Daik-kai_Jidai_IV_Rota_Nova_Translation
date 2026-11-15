"""Use code/data mapping symbols to audit the exact verified ARM946 binary."""
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_duel_native_layout_v1134 import elf_functions
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_native_ISA_v1160')
BASE = 0x02470000


def main():
    assert not ROOT.exists()
    ordinary_path = Path('work/analysis/duel_layout_native_v1159/compiler_provenance.json')
    symbols_path = Path('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    ordinary, symbol_build = read(ordinary_path), read(symbols_path)
    binary = Path(ordinary['binary']).read_bytes()
    assert sha(binary) == ordinary['binary_sha256'] == symbol_build['binary_sha256']
    assert Path(symbol_build['binary']).read_bytes() == binary
    elf = Path(symbol_build['ELF']).read_bytes()
    assert sha(elf) == symbol_build['ELF_sha256']
    symbols = elf_functions(elf)
    functions = [row for row in symbols if row['kind'] == 2]
    assert {row['name'] for row in functions} == {'duel_draw', 'duel_layout', 'word_hash'}
    assert all(row['address'] & 1 for row in functions)
    mappings = sorted((row['address'], row['name']) for row in symbols if row['name'].startswith(('$t', '$d')))
    assert mappings and mappings[0] == (BASE, '$t.0')
    ranges, instructions = [], []
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    allowed = {'push','pop','add','adds','sub','subs','mov','movs','ldr','ldrb','ldrh','ldrsb','ldrsh',
               'str','strb','strh','lsls','lsrs','asrs','cmp','cmn','tst','ands','eors','orrs','bics',
               'mvns','negs','rsbs','adcs','sbcs','rors','muls','stm','ldm','b','beq','bne','bcs','bcc',
               'bhs','blo','bhi','bls','bge','bgt','ble','blt','bmi','bpl','bvs','bvc','bx','bl','blx'}
    for index, (start, name) in enumerate(mappings):
        end = mappings[index + 1][0] if index + 1 < len(mappings) else BASE + len(binary)
        assert BASE <= start < end <= BASE + len(binary)
        ranges.append({'kind': 'Thumb code' if name.startswith('$t') else 'literal or readonly data',
                       'start': start, 'end': end, 'bytes': end - start})
        if not name.startswith('$t'):
            continue
        current = list(decoder.disasm(binary[start - BASE:end - BASE], start))
        assert sum(instruction.size for instruction in current) == end - start
        for instruction in current:
            assert instruction.mnemonic in allowed, instruction
            assert instruction.size == 2 or instruction.mnemonic in ('bl', 'blx')
            assert instruction.bytes != b'\x00\xbf'
            if instruction.mnemonic=='rsbs':
                assert instruction.size==2 and int.from_bytes(instruction.bytes,'little')&0xffc0==0x4240
                assert instruction.op_str.endswith('#0')
            if instruction.mnemonic=='blx' and instruction.op_str=='r2':
                assert instruction.address==BASE+0x22
                assert int.from_bytes(binary[0x28:0x2c],'little')==0x020D5404
            elif instruction.mnemonic in ('bl', 'blx'):
                assert instruction.op_str.startswith('#')
                target = int(instruction.op_str[1:], 0) & ~1
                assert any((row['address'] & ~1) == target for row in functions)
            instructions.append([instruction.address, instruction.bytes.hex(), instruction.mnemonic, instruction.op_str])
    assert sum(row['bytes'] for row in ranges) == len(binary) == 1480
    ROOT.mkdir(parents=True)
    proof = ROOT / 'exact_binary_ISA_and_reproduction.json'
    save(proof, {'ordinary_compiler_provenance': str(ordinary_path), 'symbol_compiler_provenance': str(symbols_path),
        'same1480byte_code_with_and_without_debug_symbols': True,
        'compiler_binary_SHA256': ordinary['compiler_sha256'], 'verified_binary_SHA256': sha(binary),
        'ELF_functions': functions, 'mapped_code_and_data_ranges': ranges, 'instructions': instructions,
        'all_code_Thumb1_or_ARMv5_BL_BLX_no_Thumb2_or_ARMv6_NOP': True,
        'only_three_internal_functions_and_one_exact_D5404_call_no_unresolved_or_library_calls': True,
        'ELF_mapping_symbols_were_required_empty_symbol_table_is_not_an_ISA_proof': True,
        'PIC_reference_link_address': BASE,
        'single_register_call_exact_literal_original_D5404':0x020D5404,
        'PIC_all14100_positioned_source_and_name_stress_cases':'work/analysis/duel_PIC_positions_v1143/PIC_native_position_matrix.json',
        'existing_COMMON_cache_position_and_complete_native_fonts_independently_verified_in_V1151': True,
        'no_ROM_registry_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Exact1480-byte binary reproduced;{len(instructions)} Thumb1/ARMv5 instructions classified with literal/data ranges;no library calls.')


if __name__ == '__main__':
    main()
