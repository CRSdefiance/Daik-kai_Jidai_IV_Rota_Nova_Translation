"""Declared barmaid gift fixtures:original transfer,only one gift and history.

No earned acquisition or relationship advancement is claimed.
"""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

SUPPORTED_ARM_SHA = ('d7f302ed2b142f675006ecf3b94ff14b2921dc6d43706cf4e867dfec882baa49', 'd2d2670bfbbb8ce1c3433b0c1a6220f385ef8beba5678bea9e9d4bb612b57abb')
BASE = 0x02000000


def transfer(arm, raw, items):
    if sha(arm) not in SUPPORTED_ARM_SHA or len(raw) != 0x400000:
        raise ValueError('Fixture requires a pinned verified equipment build and 4 MiB RAM')
    if not isinstance(items, list) or not len(items) == 1:
        raise ValueError('Supply exactly one of the four declared gift IDs')
    if any(type(i) is not int or i not in (129, 132, 139, 143) for i in items) or len(set(items)) != len(items):
        raise ValueError('Only Gold Dust129,Celestial Turban132,Jade Jewel139,and Seoul gift143 are declared')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB190, ())
    store = u.reg_read(UC_ARM_REG_R0)
    descriptor = 0x02470020
    # Original acquisition-history bit vector, literal used by native 49F30.
    history = struct.unpack_from('<I', arm, 0x4A0EC)[0]
    permitted = set(range(history, history + 28))
    rows = []
    for index in items:
        item = store + 4 + index * 20
        call(u, 0x4A448, (item,))
        category = u.reg_read(UC_ARM_REG_R0)
        if category != 7:
            raise ValueError(f'Item {index} is not gift category7')
        call(u, 0x49DE8, (descriptor, item))
        kind = struct.unpack('<I', u.mem_read(descriptor + 4, 4))[0]
        if kind != 6:
            raise ValueError('Gift must remain in its original unowned kind6')
        call(u, 0x4A53C, (item,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b'\0')[0].decode('cp932')
        call(u, 0x4A610, (descriptor, 0))
        call(u, 0x49F30, (item, descriptor, 6, 0))
        if u.reg_read(UC_ARM_REG_R0) != 1:
            raise ValueError('Native inventory transfer failed')
        call(u, 0x49DE8, (descriptor, item))
        assert struct.unpack('<I', u.mem_read(descriptor + 4, 4))[0] == 0
        call(u, 0x4A224, (item,))
        acquired = u.reg_read(UC_ARM_REG_R0)
        assert acquired == 4
        permitted.update(range(item, item + 20))
        rows.append({'item_id': index, 'category': category, 'name': name, 'prior_owner_kind': kind,
                     'result_owner_kind': 0, 'acquired_flag_after': acquired})
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{'address': BASE + i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after)) if a != b]
    if any(c['address'] not in permitted for c in changes):
        raise ValueError('Native transfer wrote outside selected items and acquisition bit vector')
    return after, {'synthetic_inventory_fixture': True, 'normal_acquisition_verified': False,
                   'native_transfer_entry': 0x02049F30, 'items': rows, 'changes': changes,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
