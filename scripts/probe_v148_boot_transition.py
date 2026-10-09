"""Compare header-entry startup; explicitly does not emulate a Nintendo DS boot."""

import json
import struct
from pathlib import Path

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_ARM, Uc, UcError
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCES = {
    147: '33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75',
    148: 'bb637907df8e9a4334f29219cd8273ea92731992b2bc4f9852525c68f9fed6af',
}


def probe(version):
    image = NdsImage.open(f'out/all_routes_combined_v{version}_candidate.nds')
    raw = image.read_file('/__arm9__.bin')
    if sha(raw) != SOURCES[version]:
        raise ValueError('Exact saved ARM9 required')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_map(0x04000000, 0x2000)
    machine.mem_map(0x05000000, 0x1000)
    machine.mem_map(0x07000000, 0x1000)
    machine.mem_write(image.rom.arm9RamAddress, raw)
    destination = struct.unpack_from('<I', raw, 0x918)[0]
    events, contracts, tail = [], {}, []
    count = 0

    def hook(uc, address, size, _):
        nonlocal count
        count += 1
        tail.append(address)
        if len(tail) > 24:
            tail.pop(0)
        if address in (0x02000800, 0x0200088C, 0x020008E4, 0x020008EC,
                       0x020009E0, 0x02005310, destination):
            events.append({'pc': address, 'sp': uc.reg_read(UC_ARM_REG_SP)})
        if address == 0x02000A5C:
            contracts['cp15_setup_skipped'] = True
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address in (0x02000A34, 0x02000A38, 0x02000A3C,
                         0x020008B0, 0x020008B4, 0x020008B8):
            contracts['cache_maintenance_skipped'] = True
            uc.reg_write(UC_ARM_REG_PC, address + 4)
        elif address == destination:
            uc.emu_stop()

    machine.hook_add(UC_HOOK_CODE, hook)
    error = None
    try:
        machine.emu_start(image.rom.arm9EntryAddress, 0, count=5000000)
    except UcError as exc:
        error = str(exc)
    pc = machine.reg_read(UC_ARM_REG_PC)
    return {'version': version, 'rom_sha256': sha(image.source.read_bytes()),
            'arm9_sha256': sha(raw), 'header_entry': image.rom.arm9EntryAddress,
            'destination': destination, 'reached_destination': pc == destination,
            'final_pc': pc, 'instruction_count': count, 'events': events,
            'last_pcs': tail, 'error': error, 'hardware_contracts': contracts,
            'pool_sha256_after_startup': sha(bytes(machine.mem_read(0x02387A20, 1504)))}


def main():
    report = {'cases': [probe(v) for v in SOURCES],
              'limitations': ['Not a full DS boot or black-screen reproduction.',
                              'CP15 setup/cache operations modeled; IO starts zero.',
                              'No ARM7, interrupts, physical bus, MPU or display emulation.',
                              'Actual user cold-boot failure remains authoritative.']}
    Path('work/analysis/v148_boot_transition_probe.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
