"""Original transition scene painters, with all diagnostic failures retained."""
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_INVALID, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.research_town_scene_v644 import setup
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/movie_transition_bitmaps_v648')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
LOWER, UPPER, SIZE, CTX = 0x022E1794, 0x022F9794, 98304, 0x023117AC


def main():
    rom = NdsImage.open(read(ROOT / 'preflight.json')['candidate'])
    rows = []
    for label, f in [('rafael', 3140), ('lil', 2860), ('hodram', 3120)]:
        folder = CAP / ('movie_transition_bitmaps_v648_' + label)
        state = read(folder / f'capture_native_state_{f:06d}/native_state.json')
        raw = (folder / f'capture_gpu_state_{f:06d}/arm9_main_ram.bin').read_bytes()
        io, vram, dtcm, itcm = [Path(state['regions'][k]['path']).read_bytes() for k in ['9REG', 'LCDM', 'DTCM', 'ITCM']]
        u, mapping = setup(rom, raw, io, vram, dtcm)
        u.mem_write(0x01FF0000, itcm)
        u.mem_write(0x01FF8000, itcm)
        u.mem_write(LOWER, b'\xA5' * (2 * SIZE))
        u.reg_write(UC_ARM_REG_SP, STACK)
        executed, writes, invalid, calls = set(), set(), [], []
        contexts, methods = {}, set()
        for context in (CTX, CTX + 24):
            nodes, node = [], struct.unpack_from('<I', raw, context - BASE + 16)[0]
            while node:
                assert node not in {n['node'] for n in nodes} and len(nodes) < 50
                vt = struct.unpack_from('<I', raw, node - BASE)[0]
                method = struct.unpack_from('<I', raw, vt - BASE + 12)[0]
                nodes.append({'node': node, 'method': method})
                methods.add(method)
                node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
            contexts[context] = nodes

        def code(cpu, address, size, unused, executed=executed, methods=methods, calls=calls):
            executed.add(address)
            if address in methods:
                calls.append([address, cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)])

        def write(cpu, kind, address, size, value, unused, writes=writes):
            if LOWER <= address < UPPER + SIZE:
                writes.update(range(address, address + size))

        def fail(cpu, kind, address, size, value, unused, invalid=invalid):
            invalid.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'size': size, 'access': kind})
            return False

        u.hook_add(UC_HOOK_CODE, code)
        u.hook_add(UC_HOOK_MEM_WRITE, write)
        u.hook_add(UC_HOOK_MEM_INVALID, fail)
        error = None
        try:
            for context in contexts:
                u.reg_write(UC_ARM_REG_R4, context)
                u.reg_write(UC_ARM_REG_R5, context + 12)
                u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
                assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314
        except (AssertionError, ValueError, UcError) as exc:
            error = repr(exc)
        output = bytes(u.mem_read(LOWER, SIZE * 2))
        (ROOT / f'{label}_{f}_native_surfaces.bin').write_bytes(output)
        row = {'route': label, 'frame': f, 'error': error, 'invalid': invalid, 'calls': calls,
            'contexts': contexts,
            'PC': u.reg_read(UC_ARM_REG_PC), 'destination_bytes_written': len(writes),
            'surface_lower_vs_captured_RAM_byte_differences': sum(a != b for a, b in zip(output[:SIZE], raw[LOWER-BASE:LOWER-BASE+SIZE])),
            'surface_upper_vs_captured_RAM_byte_differences': sum(a != b for a, b in zip(output[SIZE:], raw[UPPER-BASE:UPPER-BASE+SIZE])),
            'executed': sorted(executed), 'mapping': mapping, 'not_final_verification': True}
        rows.append(row)
        print(label, 'error', error, 'invalid', invalid[:2], 'calls', len(calls), 'bytes', len(writes), 'surface diff', row['surface_upper_vs_captured_RAM_byte_differences'], flush=True)
    save(ROOT / 'native_scene_diagnostic.json', rows)


if __name__ == '__main__':
    main()
