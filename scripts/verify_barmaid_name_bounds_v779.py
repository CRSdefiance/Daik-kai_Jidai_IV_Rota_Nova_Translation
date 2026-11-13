"""Verify the actual16-byte first-name editor,setter,getter and17-byte I/O loop."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_barmaid_dialogue_v779 import ROOT, CURRENT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_village_wrap_v608 import save

EDITOR, RECORD, OWNER, IO = 0x02430000, 0x02430100, 0x02430400, 0x02430800


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x9DE24, 0x9DE80), (0xCD6E0, 0xCD6EC), (0x1371C, 0x13724),
             (0x830B0, 0x830D8), (0x82FB8, 0x82FE0)]
    assert all(arm[a:b] == source[a:b] for a, b in spans)
    names = [b'A'*n for n in range(1, 17)] + ['ア'.encode('cp932')*n for n in range(1, 9)]
    results = []
    for name in names:
        u = machine(arm)
        u.mem_write(EDITOR+0x54, struct.pack('<I', RECORD))
        u.mem_write(RECORD+8, b'Original\0')
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R4, EDITOR)
        keyboard = []
        def keyboard_contract(c, at, size, unused):
            assert c.reg_read(UC_ARM_REG_R1) == 16 and c.reg_read(UC_ARM_REG_R0) == STACK+4
            c.mem_write(STACK+4, name+b'\0')
            keyboard.append(16)
            c.reg_write(UC_ARM_REG_R0, 1)
            c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, keyboard_contract, begin=BASE+0xAEB98, end=BASE+0xAEB98)
        u.emu_start(BASE+0x9DE24, BASE+0x9DE80, count=10000)
        u.hook_del(hook)
        assert keyboard == [16] and bytes(u.mem_read(RECORD+8, len(name)+1)) == name+b'\0'
        assert u.reg_read(UC_ARM_REG_SP) == STACK
        u.mem_write(OWNER+0x1C, b'\xA5'*25)
        u.reg_write(UC_ARM_REG_R4, RECORD)
        u.reg_write(UC_ARM_REG_R5, OWNER)
        u.emu_start(BASE+0xCD6E0, BASE+0xCD6EC, count=10000)
        expected = (name+b'\0').ljust(17, b'\xA5')
        assert bytes(u.mem_read(OWNER+0x20, 17)) == expected
        assert bytes(u.mem_read(OWNER+0x1C, 4)) == bytes(u.mem_read(OWNER+0x31, 4)) == b'\xA5'*4
        call(u, 0x1371C, (OWNER,))
        assert u.reg_read(UC_ARM_REG_R0) == OWNER+0x20
        serialization = []
        for mode, start, end, helper in (('save', 0x830B0, 0x830D8, 0x46BE0), ('load', 0x82FB8, 0x82FE0, 0x469DC)):
            calls = []
            u.mem_write(OWNER+0x1C, b'\xA5'*25)
            if mode == 'save':
                u.mem_write(OWNER+0x20, expected)
            u.reg_write(UC_ARM_REG_R4, IO)
            u.reg_write(UC_ARM_REG_R5, OWNER)
            u.reg_write(UC_ARM_REG_SP, STACK)
            def byte_io_contract(c, at, size, unused):
                position = len(calls)
                assert position < 17
                assert c.reg_read(UC_ARM_REG_R0) == IO and c.reg_read(UC_ARM_REG_R1) == OWNER+0x20+position
                assert c.reg_read(UC_ARM_REG_R2) == 0
                if mode == 'save':
                    assert bytes(c.mem_read(OWNER+0x20+position, 1)) == expected[position:position+1]
                else:
                    c.mem_write(OWNER+0x20+position, expected[position:position+1])
                calls.append(position)
                c.reg_write(UC_ARM_REG_R0, 1)
                c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))
            hook = u.hook_add(UC_HOOK_CODE, byte_io_contract, begin=BASE+helper, end=BASE+helper)
            u.emu_start(BASE+start, BASE+end, count=10000)
            u.hook_del(hook)
            assert calls == list(range(17)) and u.reg_read(UC_ARM_REG_SP) == STACK
            assert bytes(u.mem_read(OWNER+0x20, 17)) == expected
            assert bytes(u.mem_read(OWNER+0x1C, 4)) == bytes(u.mem_read(OWNER+0x31, 4)) == b'\xA5'*4
            serialization.append({'mode': mode, 'native_iterations': len(calls), 'full_field_hex': expected.hex(),
                                  'byte_IO_helper_and_physical_save_are_contracts': True})
        results.append({'name_hex': name.hex(), 'editor_limit': 16, 'complete_setter_getter_NUL_and_guards_exact': True,
                        'save_load': serialization})
    save(ROOT/'captain_first_name_bound.json', {'candidate_sha256': sha(CURRENT.read_bytes()),
                                               'source_current_spans': spans, 'capacity': 16, 'serialized_bytes': 17,
                                               'field_offset': 0x20, 'cases': results,
                                               'original_editor_dispatch_copy_getter_and_complete_loops_verified': True,
                                               'keyboard_UI_and_physical_IO_not_executed': True,
                                               'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('24 first-name editor/setter/getter and17-byte save/load cases pass;16-byte limit verified.', flush=True)


if __name__ == '__main__':
    main()
