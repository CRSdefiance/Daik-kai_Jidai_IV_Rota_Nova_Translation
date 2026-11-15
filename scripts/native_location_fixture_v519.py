"""Opt-in isolated ship location fixture; never edits the ROM or donor save."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

BASE = 0x02000000
ARM_SHA = '5e65a8cfe1384783edc6eb8243ea72f5369729c55f5b2d06ffee2968207cf074'


def relocate(arm, raw, town):
    if sha(arm) != ARM_SHA or len(raw) != 0x400000:
        raise ValueError('Location fixture requires verified V518 ARM9 and 4 MiB RAM')
    if type(town) is not int or town not in (59, 60):
        raise ValueError('This fixture is limited to Osaka 59 and Naha 60')
    u = machine(arm)
    u.mem_write(BASE, raw)

    def getter(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    fleets = getter(0xCB1A8)
    index = getter(0x2E58C)
    ship = getter(0x36C70, (fleets + 4 + index * 0x84 + 0xC,))
    if not BASE <= ship < BASE + len(raw) - 0x100:
        raise ValueError('Invalid active ship pointer')
    city = getter(0xCD6B8, (town,))
    port = [v * 128 for v in struct.unpack('<2i', u.mem_read(city + 12, 8))]
    # Port-adjacent water position. Original docking logic must still run.
    target = [port[0], port[1] - 1900]
    offset = ship + 0x10 - BASE
    prior = list(struct.unpack_from('<2I', raw, offset))
    after = bytearray(raw)
    struct.pack_into('<2I', after, offset, *target)
    changes = [{'address': BASE + i, 'before': raw[i], 'after': after[i]}
               for i in range(offset, offset + 8) if raw[i] != after[i]]
    return bytes(after), {
        'synthetic_location_fixture': True,
        'normal_travel_verified': False,
        'town_id': town, 'original_port_world_point': port,
        'prior_world_point': prior, 'fixture_world_point': target,
        'active_ship': ship, 'changes': changes,
        'only_ship_coordinate_bytes_changed': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
    }
