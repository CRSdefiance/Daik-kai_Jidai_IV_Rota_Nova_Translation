"""Original captain-specific CS block loader with only SDK file I/O bridged."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.research_wedding_command_v676 import ROOT
from scripts.verify_village_wrap_v608 import read, save

OBJECT = 0x02480000
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def load(rom, captain, block_id):
    u = machine(rom.read_file('/__arm9__.bin'))
    u.mem_write(0x022796B0, struct.pack('<I', captain))
    u.mem_write(OBJECT - 16, b'\xA5' * (0x2420 + 32))
    handles, operations = {}, []

    def io(cpu, pc, size, unused):
        if pc not in (OPEN, READ, SEEK, CLOSE):
            return
        obj, a, b = [cpu.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        if pc == OPEN:
            name = bytes(cpu.mem_read(a, 128)).split(b'\0')[0].decode('ascii')
            requested = '/' + name.replace('\\', '/').lstrip('/')
            matches = [p for p in rom.path_map() if p.casefold() == requested.casefold()]
            assert matches == [f'/data/SC{captain}.DK4'], requested
            path = matches[0]
            data = rom.read_file(path)
            assert obj not in handles
            handles[obj] = [path, data, 0]
            cpu.mem_write(obj + 0x20, struct.pack('<2I', 0, len(data)))
            operations.append({'operation': 'open', 'PC': pc, 'requested': requested,
                               'path': path, 'sha256': sha(data)})
            result = 1
        elif pc == READ:
            path, data, at = handles[obj]
            assert at + b <= len(data)
            cpu.mem_write(a, data[at:at + b])
            handles[obj][2] += b
            operations.append({'operation': 'read', 'PC': pc, 'path': path, 'offset': at, 'bytes': b})
            result = b
        elif pc == SEEK:
            path, data, _ = handles[obj]
            assert b == 0 and 0 <= a <= len(data)
            handles[obj][2] = a
            operations.append({'operation': 'seek', 'PC': pc, 'path': path, 'offset': a})
            result = 1
        else:
            operations.append({'operation': 'close', 'PC': pc, 'path': handles.pop(obj)[0]})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    h = u.hook_add(UC_HOOK_CODE, io)
    try:
        call(u, 0x24214, (OBJECT,))
        executed = call(u, 0x24134, (OBJECT, block_id), instruction_limit=100000)
        output = bytes(u.mem_read(OBJECT, 0x2420))
        assert not handles
        assert u.reg_read(UC_ARM_REG_R0) == 1
        expected = IlnkContainer.parse(rom.read_file(f'/data/SC{captain}.DK4')).blocks[block_id]
        assert output[8:8 + len(expected)] == expected
        assert struct.unpack_from('<I', output, 4)[0] == block_id
        assert bytes(u.mem_read(OBJECT - 16, 16)) == bytes(u.mem_read(OBJECT + 0x2420, 16)) == b'\xA5' * 16
    finally:
        u.hook_del(h)
    return {'captain': captain, 'block': block_id, 'whole_original_block_bytes': len(expected),
        'block_sha256': sha(expected), 'native_file_operations': operations,
        'full_constructor_and_block_loader_return_ABI_and_guards_exact': True,
        'executed_addresses': sorted(executed), 'explicit_captain_block_and_buffer_inputs_not_runtime_event': True}


def main():
    pre = read(ROOT / 'preflight.json')
    results = {}
    for tag, path in (('current', pre['candidate']), ('clean', 'work/clean.nds')):
        rom = NdsImage.open(path)
        results[tag] = load(rom, 2, 70)
        save(ROOT / 'native_block_loader.json', results)
        print(tag, 'original Lil block70 loader verified', flush=True)
    save(ROOT / 'native_block_loader.json', {'cases': results,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})


if __name__ == '__main__':
    main()
