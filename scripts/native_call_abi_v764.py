"""Bounded native calls with the established full callee-saved ABI checks.

These runs do not collect per-instruction Python coverage sets. Provider and
dispatcher boundary hooks are separate, explicit checks in their own probes.
"""

from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
                              UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                              UC_ARM_REG_SP)

from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP


def call(uc, offset, args, *, instruction_limit=100000):
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
        uc.reg_write(reg, value)
    saved = {reg: 0xA5A51000 + index for index, reg in enumerate(SAVED)}
    for reg, value in saved.items():
        uc.reg_write(reg, value)
    uc.emu_start(BASE + offset, STOP, count=instruction_limit)
    if (uc.reg_read(UC_ARM_REG_PC) != STOP or uc.reg_read(UC_ARM_REG_SP) != STACK
            or any(uc.reg_read(reg) != value for reg, value in saved.items())):
        raise ValueError(f'Native completion or callee-saved ABI failed: PC={uc.reg_read(UC_ARM_REG_PC):#x}, SP={uc.reg_read(UC_ARM_REG_SP):#x}')
