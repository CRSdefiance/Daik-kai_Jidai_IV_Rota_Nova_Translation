"""Opt-in label-only test: one live commodity name pointer, no stock changes."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.commodity_fidelity import BASE, CHANGES, CHANGES_V2, TABLE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

ARM = 'b05b9f27543c90720602f7a5d5e59299f8f140545b43654bac0a21ba68df12a1'
CORRECTED_ARM = '1f6ed33c8ee91bdeb1667e3f7524f3731ac7b0ba89a07f4be4ee1422cd7851bb'


def substitute(arm, raw, target):
    version = sha(arm)
    names = CHANGES_V2 if version == CORRECTED_ARM else CHANGES
    if version not in (ARM, CORRECTED_ARM) or len(raw) != 0x400000 or type(target) is not int or target not in names:
        raise ValueError('Label fixture requires a pinned commodity-fidelity ARM9,4MiB RAM and a reviewed changed ID')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB124, ())
    manager = u.reg_read(UC_ARM_REG_R0)
    obj = manager + 4 + 90 * 16
    if not BASE <= obj < BASE + len(raw) - 16 or struct.unpack_from('<I', raw, obj - BASE)[0] != 0x0215B66C:
        raise ValueError('Expected initialized original commodity object90')
    name_pointer = struct.unpack_from('<I', arm, TABLE + target * 12)[0]
    at = name_pointer - BASE
    name = names[target][1].encode('ascii') + b'\0'
    if raw[at:at + len(name)] != name:
        raise ValueError('Selected complete name is not resident source-owned V635 data')
    allowed = {struct.unpack_from('<I', arm, TABLE + i * 12)[0] for i in names}
    prior = struct.unpack_from('<I', raw, obj - BASE + 4)[0]
    if prior not in allowed:
        raise ValueError('Unexpected prior commodity label pointer')
    after = bytearray(raw)
    struct.pack_into('<I', after, obj - BASE + 4, name_pointer)
    changes = [{'address': BASE + i, 'before': raw[i], 'after': after[i]}
               for i in range(obj - BASE + 4, obj - BASE + 8) if raw[i] != after[i]]
    return bytes(after), {'synthetic_complete_commodity_label_substitution': True,
                          'commodity_object': obj, 'underlying_commodity_id': 90,
                          'selected_name_id': target, 'English': names[target][1],
                          'old_name_pointer': prior, 'new_name_pointer': name_pointer,
                          'only_one_initialized_name_pointer_changed': True,
                          'no_stock_quantities_prices_categories_icons_or_metadata_changed': True,
                          'normal_goods_acquisition_or_original_item_identity_not_claimed': True,
                          'changes': changes, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
