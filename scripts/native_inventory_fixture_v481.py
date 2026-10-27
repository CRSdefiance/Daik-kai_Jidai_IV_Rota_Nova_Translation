"""Explicit synthetic inventory fixtures, using the original game's transfer code.

Only pinned V474/V484/V502/V534/V543 builds and equipment categories 2/3/4 are accepted. This is rendering evidence,
not normal acquisition evidence. Original saves and ROM bytes are never edited.
"""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

ARM_SHA = 'c425bd54d4158a342f38a3950a02160d264eb645bd946cabf84dbe24aeaea2ce'
SUPPORTED_ARM_SHA = (ARM_SHA, 'b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b',
                     'daec11a5dbe1398c0dbb67350b9f5359c6d6c51336076df8c6243d96d3537858',
                     '4a42ec3e5ea9fe4b0df425b22a9d446f44336912b237c2474bafbb8331bc6865',
                     '441e0e20c75f39261febac20078a319263fb76533229705cbb6f2c74a18ea960',
                     '1f94c9c084552fa93cefd80ad195dda054cf9fdaa06a488d2a3943b37822aa5f',
                     '60948e7a8f50abc838cfdf49114782aeeb977b75352dc741e90e8dafd161150e')
BASE = 0x02000000


def transfer(arm, raw, items):
    if sha(arm) not in SUPPORTED_ARM_SHA or len(raw) != 0x400000:
        raise ValueError('Fixture requires a pinned verified equipment build and 4 MiB RAM')
    if not isinstance(items, list) or not 1 <= len(items) <= 12:
        raise ValueError('Supply 1 to 12 equipment item IDs')
    if any(type(i) is not int or not 0 <= i < 218 for i in items) or len(set(items)) != len(items):
        raise ValueError('Item IDs must be unique integers from 0 to 217')
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
        if category not in (2, 3, 4):
            raise ValueError(f'Item {index} is not equipment category 2/3/4')
        call(u, 0x49DE8, (descriptor, item))
        kind = struct.unpack('<I', u.mem_read(descriptor + 4, 4))[0]
        if kind in (2, 3):
            raise ValueError('Choose an unequipped item; fixture must preserve equipped owners')
        call(u, 0x4A53C, (item,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b'\0')[0].decode('cp932')
        call(u, 0x4A610, (descriptor, 0))
        call(u, 0x49F30, (item, descriptor, 6, 0))
        if u.reg_read(UC_ARM_REG_R0) != 1:
            raise ValueError('Native inventory transfer failed')
        call(u, 0x49DE8, (descriptor, item))
        assert struct.unpack('<I', u.mem_read(descriptor + 4, 4))[0] == 0
        permitted.update(range(item, item + 20))
        rows.append({'item_id': index, 'category': category, 'name': name, 'prior_owner_kind': kind,
                     'result_owner_kind': 0})
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{'address': BASE + i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after)) if a != b]
    if any(c['address'] not in permitted for c in changes):
        raise ValueError('Native transfer wrote outside selected items and acquisition bit vector')
    return after, {'synthetic_inventory_fixture': True, 'normal_acquisition_verified': False,
                   'native_transfer_entry': 0x02049F30, 'items': rows, 'changes': changes,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
