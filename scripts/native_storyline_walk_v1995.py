"""Structural native walk with an explicitly nonmatching previous-result value.

The linear extent walk bridges opaque scene/gameplay effects and does not claim
runtime branch reachability. The selector cases bridge only movie playback and
scene reset, and run the complete original command with saved-register ABI.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/wedding_movie_v676')
OWNER, STREAM, RESULT, LENGTH = 0x02460000, 0x02470000, 0x02468000, 0x02468040
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


def walk(arm, block):
    u = machine(arm)
    u.mem_write(OWNER, bytes(32))
    u.mem_write(STREAM - 16, b'\xA5' * (len(block) + 32))
    u.mem_write(STREAM, block)
    offset, rows, bridges, calls = 8, [], [], []
    limit = 8 + struct.unpack_from('<H', block, 4)[0]
    assert block[:4] == b'CS\0\1' and limit <= len(block) and not any(block[limit:])

    def effect(cpu, pc, size, unused):
        if 0x020293B8 <= pc < 0x0202A600 or 0x02028A28 <= pc < 0x02028A64:
            return
        lr = cpu.reg_read(UC_ARM_REG_LR)
        assert (0x020293B8 <= lr < 0x0202A600 or 0x02028A28 <= lr < 0x02028A64), (pc, lr)
        args = [cpu.reg_read(reg) for reg in REGS]
        bridges.append({'source_offset': offset, 'PC': pc, 'LR': lr, 'args': args, 'opaque_result': 0})
        if pc == 0x020D2B1C:
            calls.append({'source_offset': offset, 'args': args})
        cpu.reg_write(UC_ARM_REG_R0, 0)
        cpu.reg_write(UC_ARM_REG_PC, lr)

    h = u.hook_add(UC_HOOK_CODE, effect)
    error = None
    try:
        while offset < limit:
            assert len(rows) < 5000
            u.mem_write(OWNER + 4, struct.pack('<I', STREAM + offset))
            u.mem_write(RESULT, bytes(48))
            u.mem_write(LENGTH, bytes(4))
            call(u, 0x2A510, (RESULT, OWNER, LENGTH, 0xFFFFFFFF), instruction_limit=20000)
            length = struct.unpack('<I', u.mem_read(LENGTH, 4))[0]
            assert length >= 2 and length % 2 == 0 and offset + length <= limit, (offset, length, limit)
            rows.append({'offset': offset, 'word': struct.unpack_from('<H', block, offset)[0],
                         'native_extent': length, 'result': bytes(u.mem_read(RESULT, 24)).hex()})
            offset += length
        assert bytes(u.mem_read(STREAM, len(block))) == block
        assert bytes(u.mem_read(STREAM - 16, 16)) == bytes(u.mem_read(STREAM + len(block), 16)) == b'\xA5' * 16
    except (AssertionError, ValueError, UcError) as exc:
        error = repr(exc)
    finally:
        u.hook_del(h)
    return {'rows': rows, 'stopped_offset': offset, 'logical_end': limit, 'error': error,
            'opaque_effect_bridges': bridges, 'native_movie_requests': calls,
            'linear_native_extents_not_runtime_branch_reachability': True}

