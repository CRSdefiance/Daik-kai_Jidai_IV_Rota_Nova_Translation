"""Authorized isolated Gallery access; preserve all unrelated system bits."""

import struct

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_location_fixture_v519 import ARM_SHA, BASE

FIELD = 0x27985C


def enable_gallery(arm, raw):
    if sha(arm) != ARM_SHA or len(raw) != 0x400000:
        raise ValueError('Gallery fixture requires verified V518 ARM9 and 4 MiB RAM')
    before = struct.unpack_from('<H', raw, FIELD)[0]
    after = bytearray(raw)
    struct.pack_into('<H', after, FIELD, before | 15)
    changes = [{'address': BASE + i, 'before': raw[i], 'after': after[i]}
               for i in range(FIELD, FIELD + 2) if raw[i] != after[i]]
    return bytes(after), {'synthetic_gallery_fixture': True,
                          'earned_unlock_verified': False,
                          'system_halfword_before': before,
                          'system_halfword_after': before | 15,
                          'only_low_four_system_bits_set': True,
                          'changes': changes,
                          'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
