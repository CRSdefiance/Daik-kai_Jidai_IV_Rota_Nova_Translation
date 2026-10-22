"""Replay actual original lower paints using their recorded SDK clock returns."""

import argparse
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_MEM_READ, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.observe_filter_clock_v693 import ROOT
from scripts.research_town_scene_v644 import setup
from scripts.run_village_visits_v664 import CAP
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read, save

OUTPUT, BYTES = 0x022E1794, 98304


def region(row, name):
    item = row['regions'][name]
    data = Path(item['path']).read_bytes()
    assert sha(data) == item['sha256'] and len(data) == item['bytes']
    return data


def replay(case, index):
    folder = CAP / ('filter_clock_v693_' + case)
    event = read(folder / 'clock_observer/events.json')
    assert not event['errors'] and event['no_game_CPU_RAM_VRAM_IO_ITCM_DTCM_writes']
    row = event['paints'][index]
    pre = read(ROOT / 'preflight.json')
    rom = NdsImage.open(pre['cases'][case]['ROM'])
    raw, dtcm, io, lcdm = (region(row, k) for k in ('RAM', 'DTCM', 'IO', 'LCDM'))
    assert int.from_bytes(region(row, 'MDTC'), 'little') == 0x027E0000
    u, mapping = setup(rom, raw, io, lcdm, dtcm)
    itcm = region(row, 'ITCM')
    u.mem_write(0x01FF0000, itcm)
    u.mem_write(0x01FF8000, itcm)
    cpu = struct.unpack('<32I', bytes.fromhex(row['entry_CPU128_hex']))
    assert cpu[2] == 0x020D32B8 and not cpu[20] & 0x20
    regs = [getattr(arm_const, 'UC_ARM_REG_R' + str(i)) for i in range(13)]
    regs += [arm_const.UC_ARM_REG_SP, arm_const.UC_ARM_REG_LR]
    u.reg_write(arm_const.UC_ARM_REG_CPSR, cpu[20])
    for reg, value in zip(regs, cpu[4:19], strict=True):
        u.reg_write(reg, value)
    executed, clocks, writes, reads_before_write = set(), [], set(), set()

    def code(uc, pc, size, unused):
        executed.add(pc)
        if pc == 0x020E4F98:
            assert uc.reg_read(arm_const.UC_ARM_REG_LR) == 0x02000FA8
            item = row['clocks'][len(clocks)]
            origin = struct.unpack('<Q', uc.mem_read(0x02170374, 8))[0]
            assert origin == item['origin']
            tick = item['tick']
            uc.reg_write(arm_const.UC_ARM_REG_R0, tick & 0xFFFFFFFF)
            uc.reg_write(arm_const.UC_ARM_REG_R1, tick >> 32)
            uc.reg_write(arm_const.UC_ARM_REG_PC, uc.reg_read(arm_const.UC_ARM_REG_LR))
            clocks.append(item)

    def memory(uc, access, address, size, value, unused):
        if OUTPUT <= address < OUTPUT + BYTES:
            assert address + size <= OUTPUT + BYTES
            if access == UC_MEM_READ:
                reads_before_write.update(p for p in range(address, address + size) if p not in writes)
            else:
                writes.update(range(address, address + size))

    h1 = u.hook_add(UC_HOOK_CODE, code)
    h2 = u.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, memory, begin=OUTPUT, end=OUTPUT + BYTES - 1)
    try:
        u.emu_start(cpu[2], 0x020D3314, count=12000000)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    assert u.reg_read(arm_const.UC_ARM_REG_PC) == 0x020D3314
    assert clocks == row['clocks']
    actual = bytes(u.mem_read(OUTPUT, BYTES))
    returned_raw = Path(row['return_RAM']['path']).read_bytes()
    assert sha(returned_raw) == row['return_RAM']['sha256']
    expected = returned_raw[OUTPUT - 0x02000000:OUTPUT - 0x02000000 + BYTES]
    diffs = [i for i, (a, b) in enumerate(zip(actual, expected, strict=True)) if a != b]
    returned_cpu = struct.unpack('<32I', bytes.fromhex(row['return_CPU128_hex']))
    destination = ROOT / case
    destination.mkdir(exist_ok=True)
    name = f'paint_{index:03d}_{row["entry_frame"]}'
    output = destination / (name + '.bin')
    output.write_bytes(actual)
    image = Image.new('RGB', (256, 192))
    image.putdata(rgb(struct.unpack('<49152H', actual)))
    image.save(destination / (name + '.png'))
    snapshot_code = []
    for pc in sorted(executed):
        if 0x02000000 <= pc < 0x02400000:
            assert bytes(u.mem_read(pc, 4)) == raw[pc - 0x02000000:pc - 0x02000000 + 4], hex(pc)
        elif 0x01FF0000 <= pc < 0x02000000:
            off = (pc - 0x01FF0000) & 0x7FFF
            assert bytes(u.mem_read(pc, 4)) == itcm[off:off + 4], hex(pc)
        else:
            raise AssertionError(hex(pc))
        snapshot_code.append(struct.pack('<I', pc) + bytes(u.mem_read(pc, 4)))
    result = {'case': case, 'index': index, 'entry_frame': row['entry_frame'],
        'return_frame': row['return_frame'], 'actual_clock_inputs': clocks,
        'stop_PC': u.reg_read(arm_const.UC_ARM_REG_PC), 'output': str(output), 'output_sha256': sha(actual),
        'complete_output_bytes_different_from_actual_return': len(diffs), 'first_differences': diffs[:25],
        'bytes_written': len(writes), 'output_bytes_read_before_written': len(reads_before_write),
        'actual_return_registers_match': [u.reg_read(r) for r in regs] == list(returned_cpu[4:19]),
        'actual_return_CPSR_match': u.reg_read(arm_const.UC_ARM_REG_CPSR) == returned_cpu[20],
        'unique_executed_instructions': len(executed), 'executed_snapshot_code_sha256': sha(b''.join(snapshot_code)),
        'no_graphics_or_game_getter_bridges_only_exact_observed_SDK_tick_inputs': True, 'mapping': mapping}
    save(destination / (name + '.json'), result)
    print('V693 replay', {k: result[k] for k in ('case', 'index', 'entry_frame',
        'complete_output_bytes_different_from_actual_return', 'bytes_written', 'output_bytes_read_before_written',
        'actual_return_registers_match', 'actual_return_CPSR_match')}, flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('source', 'current'))
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    count = len(read(CAP / ('filter_clock_v693_' + args.case) / 'clock_observer/events.json')['paints'])
    for index in range(count) if args.index is None else [args.index]:
        replay(args.case, index)
