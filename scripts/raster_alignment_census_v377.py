"""Independent work areas for large native alignment census surfaces.

Original V257 raster contracts retained; view/context/text sit beyond the
192-row pixel buffer so their writes cannot corrupt its image or guards.
"""
import struct

from ndspy.code import MainCodeFile
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.patch.common_dialogue_alignment import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import SAVED, STACK, STOP, call, machine


def paint_long(u, entry, args):
    # Large stored paragraphs need more than the short-prompt100k budget.
    # Keep the exact original return/stack/saved-register checks.
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
        u.reg_write(reg, value)
    saved = {reg: 0xA5A51000 + index for index, reg in enumerate(SAVED)}
    for reg, value in saved.items():
        u.reg_write(reg, value)
    u.emu_start(BASE + entry, STOP, count=1000000)
    assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
    assert all(u.reg_read(reg) == value for reg, value in saved.items())


def raster(arm, text, entry, tracking=0, size=(240, 64), complete=True):
    u = machine(arm)
    u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, ctx, string = 0x02450000, 0x02473000, 0x02474000, 0x02475000
    width, height = size
    pixels = width * height // 2
    original = struct.pack("<5I", 4, width // 4, height, 0x02452000 - header, 20)
    u.mem_write(header - 16, b"\xA5" * (20 + pixels + 32))
    u.mem_write(header, original + bytes(pixels))
    u.mem_write(view - 16, b"\xA5" * 80)
    call(u, 0xD3D80, (view,))
    u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
    call(u, 0xD3AFC, (view, header, 0, 0))
    font = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(font + 4, struct.pack("<2I", 6, 16))
    kanji = NdsImage.open("out/all_routes_combined_v255_candidate.nds").read_file("/GRP/KANJI.FNT")
    u.mem_write(struct.unpack_from("<I", arm, 0xD19B8)[0], kanji)
    call(u, 0xD5160, (ctx, view, 1))
    call(u, 0xD5A10, (ctx, 1))
    u.mem_write(ctx + 28, struct.pack("<i", tracking))
    u.mem_write(string, text + b"\0")
    try:
        paint_long(u, entry, (ctx, string))
    except Exception:
        print('Raster fault', hex(u.reg_read(UC_ARM_REG_PC)), hex(u.reg_read(UC_ARM_REG_SP)),
              'r4', hex(u.reg_read(UC_ARM_REG_R4)), 'text', repr(text), flush=True)
        raise
    returned = u.reg_read(UC_ARM_REG_R0) - string
    if complete:
        assert returned == len(text)
    assert bytes(u.mem_read(string, len(text) + 1)) == text + b"\0"
    assert bytes(u.mem_read(header, 20)) == original
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + pixels, 16)) == b"\xA5" * 16
    assert bytes(u.mem_read(view - 16, 16)) == bytes(u.mem_read(view + 48, 16)) == b"\xA5" * 16
    assert struct.unpack("<i", u.mem_read(ctx + 28, 4))[0] == tracking
    packed = bytes(u.mem_read(header + 20, pixels))
    indices = bytes(n for b in packed for n in (b & 15, b >> 4))
    return indices if complete else (indices, returned)
