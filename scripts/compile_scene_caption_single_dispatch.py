"""Research repair: select the native single-ASCII callback for tracking -1."""

import struct

OFFSET = 0xD574C
ORIGINAL = (0xE28D0004, 0xE5C05000, 0xE5C05001, 0xE1D920D0,
            0xE1A0000A, 0xE28A1024, 0xE5CD2004, 0xE5903000,
            0xE28D2004, 0xE593300C)
REPLACEMENT = (0xE5D92000, 0xE1CD20B4, 0xE59A301C, 0xE3730001,
               0xE1A0000A, 0xE28A1024, 0xE5903000, 0x0593301C,
               0x1593300C, 0xE28D2004)

CP932_SOURCE = (0x0A00000F, 0xE28D0006, 0xE5C05000, 0xE5C05001,
                0xE5C05002, 0xE1D920D0, 0xE1A0000A, 0xE28A1024,
                0xE5CD2006, 0xE1D930D1, 0xE28D2006, 0xE5CD3007,
                0xE5903000, 0xE593300C, 0xE12FFF33, 0xE2899002,
                0xEA00000B)


def compile_scoped_dispatch(source):
    """Keep the controller-icon class paired even when its tracking is -1.

    Both source font classes sharing D4DA8 are locked in full. Their single-
    character callback low bytes differ, permitting an inline class discriminator
    without an extra literal or code pool. Reject new or altered class tables.
    """
    compile_dispatch(source)
    if struct.unpack_from('<17I', source, 0xD5708) != CP932_SOURCE:
        raise ValueError('Native CP932 dispatch source differs')
    if struct.unpack_from('<I', source, 0xD5778)[0] != 0xE2899001:
        raise ValueError('Native ASCII source advance differs')
    needle = struct.pack('<I', 0x020D4DA8)
    references = [i for i in range(len(source) - 3) if source[i:i + 4] == needle]
    if references != [0x152DC4, 0x1603F0]:
        raise ValueError('Unmapped font class shares the paired callback')
    classes = ((0x152DB8, (0x020D508C, 0x020AC30C, 0x020AC2EC, 0x020D4DA8,
                          0x020AC358, 0x020AC330, 0x020D5070, 0x020AC200, 0x020AC078)),
               (0x1603E4, (0x020D508C, 0x020D4D94, 0x020D4D84, 0x020D4DA8,
                          0x020D5140, 0x020D5118, 0x020D5070, 0x020D501C, 0x020D4FC8)))
    for table, callbacks in classes:
        if struct.unpack_from('<9I', source, table) != callbacks:
            raise ValueError('Mapped font class callback table differs')
    # Compact CP932 preparation preserves both byte order and the terminating
    # NUL. Post-indexed byte loads are valid even at odd source addresses.
    cp932 = (0xE4D92001, 0xE4D93001, 0xE1822403, 0xE1CD20B6,
             0xE5CD5008, 0xE1A0000A, 0xE28A1024, 0xE28D2006,
             0xE5903000, 0xE593300C, 0xE12FFF33, 0xEA00000F)
    helper = (0xE593301C, 0xE203C0FF, 0xE35C001C, 0xEA000005)
    ascii_dispatch = (0xE4D92001, 0xE1CD20B4, 0xE1A0000A, 0xE28A1024,
                      0xE5903000, 0xEAFFFFF5, 0x0590C01C, 0x037C0001,
                      0x15903000, 0x1593300C, 0xE28D2004, 0xE12FFF33)
    result = bytearray(source)
    struct.pack_into('<29I', result, 0xD5708, CP932_SOURCE[0], *cp932, *helper, *ascii_dispatch)
    return bytes(result)


def compile_dispatch(source):
    if struct.unpack_from('<10I', source, OFFSET) != ORIGINAL:
        raise ValueError('Native ASCII dispatch source differs')
    if struct.unpack_from('<I', source, OFFSET + 40)[0] != 0xE12FFF33:
        raise ValueError('Native ASCII callback instruction differs')
    if struct.unpack_from('<I', source, 0x160400)[0] != 0x020D501C:
        raise ValueError('Native font class lacks the mapped single-ASCII callback')
    result = bytearray(source)
    struct.pack_into('<10I', result, OFFSET, *REPLACEMENT)
    return bytes(result)
