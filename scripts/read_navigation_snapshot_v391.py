"""Read ship fields through original getters in an isolated captured-RAM machine."""

import argparse
import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine


def inspect(path, rom):
    arm = NdsImage.open(rom).read_file('/__arm9__.bin')
    ram = path.read_bytes()
    assert len(ram) == 0x400000
    u = machine(arm)
    u.mem_write(0x02000000, ram)

    def getter(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    environment = getter(0xCB19C)
    fleets = getter(0xCB1A8)
    fleet_index = getter(0x2E58C)
    slot = fleets + 4 + fleet_index * 0x84 + 0xC
    ship = getter(0x36C70, (slot,))
    assert 0x02000000 <= ship < 0x02400000 - 0x100
    # These are raw packed fields, not assumed geographic headings/degrees.
    packed, x, y = struct.unpack('<3I', u.mem_read(ship + 0xC, 12))
    mask = bytes(u.mem_read(environment + 0xE64, 1))[0]
    hazards = struct.unpack('<12I', u.mem_read(environment + 0xE68, 48))
    return {'snapshot': str(path), 'snapshot_sha256': sha(ram),
            'rom': str(rom), 'rom_sha256': sha(rom.read_bytes()),
            'environment': environment, 'fleet_store': fleets,
            'fleet_index': fleet_index, 'ship': ship,
            'packed_word': packed, 'direction_byte': packed >> 24,
            'world_point': [x, y], 'hazard_mask': mask,
            'hazard_points': [list(hazards[i:i + 2]) for i in range(0, 12, 2)],
            'isolated_read_only_snapshot_getters': True,
            'not_live_state_modification': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('snapshots', type=Path, nargs='+')
    parser.add_argument('--rom', type=Path, default=Path('out/all_routes_combined_v388_candidate.nds'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = [inspect(path, args.rom) for path in args.snapshots]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    for row in rows:
        print(json.dumps(row))


if __name__ == '__main__':
    main()
