"""Allow the measured adaptive helper search to reach native completion."""
from pathlib import Path


def main():
    text = Path('scripts/probe_duel_existing_balancer_v1126.py').read_text(encoding='utf-8')
    target = Path('scripts/probe_duel_existing_balancer_v1126b.py')
    assert not target.exists()
    text = text.replace("duel_existing_balancer_v1126')", "duel_existing_balancer_v1126b')")
    before = '    cpu, get = get_machine(arm, raw)\n    cpu.mem_write(TEMP, head + body)'
    after = '''    cpu, initial_get = get_machine(arm, raw)
    from scripts.native_call_abi_v764 import call
    from unicorn.arm_const import UC_ARM_REG_R0
    def get(at,*args):
        call(cpu,at,args,instruction_limit=3000000)
        return cpu.reg_read(UC_ARM_REG_R0)
    cpu.mem_write(TEMP, head + body)'''
    assert text.count(before) == 1
    text = text.replace(before, after)
    before = '        if issues:\n            findings.append(case)'
    assert text.count(before) == 1
    text = text.replace(before, before + "\n        if len(cases)%500==0:print(f'Native adaptive helper completed:{len(cases)}/4160',flush=True)")
    target.write_text(text, encoding='utf-8')
    print('Created bounded3M-instruction helper successor;first100K observation rejection preserved.')


if __name__ == '__main__':
    main()
