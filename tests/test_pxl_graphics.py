import struct

from dk4tool.graphics.pxl import PxlImage


def synthetic_pxl() -> bytes:
    header = struct.pack("<5I", 8, 2, 2, 20, 532)
    palette = bytearray(512)
    struct.pack_into("<H", palette, 2, 0x8000)
    struct.pack_into("<H", palette, 510, 0xFFFF)
    return header + bytes(palette) + bytes([0, 1, 255, 0, 0, 255, 1, 0])


def test_pxl_noop_roundtrip_is_exact():
    source = synthetic_pxl()
    assert PxlImage.from_bytes(source).to_bytes() == source


def test_pxl_edit_preserves_dimensions_and_size():
    source = synthetic_pxl()
    image = PxlImage.from_bytes(source)
    image.clear((0, 0, 4, 2), 255)
    rebuilt = image.to_bytes()
    decoded = PxlImage.from_bytes(rebuilt)
    assert (decoded.width, decoded.height) == (4, 2)
    assert len(rebuilt) == len(source)
    assert decoded.indices == bytearray([255] * 8)
