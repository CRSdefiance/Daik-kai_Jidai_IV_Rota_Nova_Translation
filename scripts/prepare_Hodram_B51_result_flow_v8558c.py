"""Supply the caller's source-established frame-pointer precondition."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_result_flow_tools_v8558c')
    assert not root.exists()
    result = derive('scripts/prove_Hodram_B51_result_flow_v8558b.py', 'scripts/prove_Hodram_B51_result_flow_v8558c.py', {
        "Path('work/analysis/Hodram_B51_result_flow_v8558b')": "Path('work/analysis/Hodram_B51_result_flow_v8558c')",
        'UC_ARM_REG_R10, UC_ARM_REG_SP': 'UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_SP',
        '(UC_ARM_REG_SP, stack), (UC_ARM_REG_R6, 1)': '(UC_ARM_REG_SP, stack), (UC_ARM_REG_R11, stack + 12), (UC_ARM_REG_R6, 1)',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result,
        reason='The fragment entry follows original add fp,sp,#12 at 0x0202404C. Initialize that frame pointer as well as SP before entering after the parser return. All native instructions, addresses, result and register assertions remain unchanged.',
        both_stopped_producers_preserved=True, no_ROM_orcredit_change=True))
