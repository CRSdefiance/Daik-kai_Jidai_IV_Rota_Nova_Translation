"""Keep terminal test failures;allow complete native draw and Thumb NEG alias."""
from pathlib import Path


def main():
    source = Path('scripts/probe_duel_compiled_fonts_v1136b.py').read_text(encoding='utf-8')
    target = Path('scripts/probe_duel_compiled_fonts_v1136c.py')
    assert not target.exists()
    source = source.replace("duel_compiled_fonts_v1136b')", "duel_compiled_fonts_v1136c')")
    before = '    return cpu,get\n'
    assert source.count(before) == 1
    source = source.replace(before, '''    from scripts.native_call_abi_v764 import call
    def bounded_get(at,*args):
        call(cpu,at,args,instruction_limit=3000000)
        return cpu.reg_read(UC_ARM_REG_R0)
    return cpu,bounded_get
''')
    before = 'draw.update(context=context,string=pointer,expanded_hex=value.hex(),'
    assert source.count(before) == 1
    source = source.replace(before, 'draw.update(context=context,string=pointer,expanded_hex=text.hex(),')
    source = source.replace("'production_caller_scope_and_owned_code_placement_not_yet_implemented':True,",
        "'production_caller_scope_and_owned_code_placement_not_yet_implemented':True,\n"
        "        'terminal_100K_predecessor_stopped_in_original_font_painter_not_restarted_while_live':True,\n"
        "        'native_call_instruction_bound':3000000,")
    target.write_text(source, encoding='utf-8')
    source = Path('scripts/audit_duel_native_ISA_v1137.py').read_text(encoding='utf-8')
    target = Path('scripts/audit_duel_native_ISA_v1137b.py')
    assert not target.exists()
    source = source.replace("duel_native_ISA_v1137')", "duel_native_ISA_v1137b')")
    source = source.replace("'mvns','negs','adcs'", "'mvns','negs','rsbs','adcs'")
    before = "            assert instruction.bytes != b'\\x00\\xbf'"
    assert source.count(before) == 1
    source = source.replace(before, before + "\n            if instruction.mnemonic=='rsbs':\n"
        "                assert instruction.size==2 and int.from_bytes(instruction.bytes,'little')&0xffc0==0x4240\n"
        "                assert instruction.op_str.endswith('#0')")
    target.write_text(source, encoding='utf-8')
    print('Created bounded-font and exact Thumb1 NEG-alias successors;prior failures preserved.')


if __name__ == '__main__':
    main()
