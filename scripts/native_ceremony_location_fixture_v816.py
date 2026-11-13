"""Only active ship coordinates at the original Athens port approach."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def relocate(arm, raw, town):
    cfg = read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'], cfg['target_arm9_sha256']) and len(raw) == 0x400000
    assert type(town) is int and town == 19
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x34674, 0x34688), (0x36C70, 0x36CA0), (0xCD6B8, 0xCD6CC))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    assert all(raw[a:b] == arm[a:b] for a, b in spans)
    u = machine(arm); u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args, instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)

    fleet = get(0xCB1A8)+4+get(0x2E58C)*0x84
    assert get(0x34674, (fleet,)) == 0x73, 'Depart normally before changing coordinates'
    ship = get(0x36C70, (fleet+12,))
    assert BASE <= ship < BASE+len(raw)-0x100
    city = get(0xCD6B8, (town,))
    port = [v*128 for v in struct.unpack('<2i', u.mem_read(city+12, 8))]
    target = [port[0], port[1]-128]
    assert all(0 <= n < 2**32 for n in target)
    at = ship+0x10-BASE; prior = list(struct.unpack_from('<2I', raw, at))
    after = bytearray(raw); struct.pack_into('<2I', after, at, *target)
    changes = [dict(address=BASE+i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(BASE+at <= r['address'] < BASE+at+8 for r in changes)
    return bytes(after), dict(synthetic_location_fixture=True, town_id=town, active_ship=ship,
        original_port_world_point=port, fixture_world_point=target, prior_world_point=prior,
        original_source_getter_spans_exact=spans, only_ship_coordinate_bytes_changed=True,
        original_docking_still_required=True, normal_travel_verified=False, changes=changes,
        before_RAM_sha256=sha(raw), after_RAM_sha256=sha(after), ARM9_sha256=sha(arm))
