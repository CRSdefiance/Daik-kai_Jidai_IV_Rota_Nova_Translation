"""Retain a native counterexample if overlong input overlaps private workspace."""
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save


def main():
    root = Path('work/analysis/duel_native_preflight_v1132')
    assert not root.exists()
    plan = read('work/analysis/duel_layout_native_v1131/compiler_provenance.json')
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    arm = NdsImage.open('out/all_routes_combined_v1105_candidate.nds').read_file('/__arm9__.bin')
    cpu, get = get_machine(arm, Path(catalog['snapshot']).read_bytes())
    cpu.mem_write(0x02470000, Path(plan['binary']).read_bytes())
    text = b'Q' * 200
    cpu.mem_write(0x02468000, text + b'\0')
    call(cpu, plan['entry'] - 0x02000000, [0x02468000], instruction_limit=3000000)
    after = bytes(cpu.mem_read(0x02468000, len(text) + 1))
    result = cpu.reg_read(UC_ARM_REG_R0)
    assert result == 0 and after != text + b'\0'
    root.mkdir(parents=True)
    save(root / 'overlong_workspace_alias_counterexample.json', {
        'compiler_provenance': 'work/analysis/duel_layout_native_v1131/compiler_provenance.json',
        'input_hex': text.hex(), 'after_hex': after.hex(), 'native_result': result,
        'findings': 'Overlong rejected text must be length-checked before workspace writes at offset128.',
        'not_a_release_or_positive_proof': True})
    print('Native preflight counterexample retained:rejected200-byte input aliases workspace;length preflight required.')


if __name__ == '__main__':
    main()
