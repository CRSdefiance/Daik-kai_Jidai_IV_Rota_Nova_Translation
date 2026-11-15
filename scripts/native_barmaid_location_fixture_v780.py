"""Opt-in ship-coordinate fixture near Hamburg/Sofala;original docking still runs."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def relocate(arm, raw, town):
    expected = read('work/analysis/barmaid_integration_v780/prospective_common_repack.json')['target_ARM9_sha256']
    if sha(arm) not in ('d7f302ed2b142f675006ecf3b94ff14b2921dc6d43706cf4e867dfec882baa49', expected) or len(raw) != 0x400000:
        raise ValueError('Exact V778/V780 and4MiB RAM required')
    if type(town) is not int or town not in (5, 34):
        raise ValueError('Only Hamburg5 and Sofala34 are declared for this fixture')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x34674, 0x34688), (0x36C70, 0x36CA0), (0xCD6B8, 0xCD6CC)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    fleet = get(0xCB1A8)+4+get(0x2E58C)*0x84
    assert get(0x34674, (fleet,)) == 0x73, 'Depart normally before applying coordinate fixture'
    ship = get(0x36C70, (fleet+0xC,))
    assert BASE <= ship < BASE+len(raw)-0x100
    city = get(0xCD6B8, (town,))
    port = [v*128 for v in struct.unpack('<2i', u.mem_read(city+12, 8))]
    target = [port[0], port[1]-1900]
    assert all(0 <= v < 2**32 for v in target)
    at = ship+0x10-BASE
    prior = list(struct.unpack_from('<2I', raw, at))
    after = bytearray(raw)
    struct.pack_into('<2I', after, at, *target)
    changes = [{'address': BASE+i, 'before': raw[i], 'after': after[i]} for i in range(at, at+8) if raw[i] != after[i]]
    assert raw[:at] == after[:at] and raw[at+8:] == after[at+8:]
    return bytes(after), {'synthetic_location_fixture': True, 'normal_travel_verified': False,
                          'town_id': town, 'original_port_world_point': port, 'prior_world_point': prior,
                          'fixture_world_point': target, 'active_ship': ship, 'changes': changes,
                          'only_ship_coordinate_bytes_changed': True, 'original_docking_still_required': True,
                          'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
