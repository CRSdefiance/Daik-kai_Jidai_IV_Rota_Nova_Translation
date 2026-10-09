"""In-place whole-string preflight for the native name editor's end insertion."""

import struct

START, END = 0xB091C, 0xB0944
ORIGINAL_WORDS = (0xEA000002, 0xE0D700D1, 0xE2855001, 0xE4C60001,
                  0xE59800A0, 0xE1550000, 0xAA000002, 0xE1D700D0,
                  0xE3500000, 0x1AFFFFF6)


def branch(at, target, opcode):
    distance = target - at - 8
    if distance & 3 or not -(1 << 25) <= distance < 1 << 25:
        raise ValueError('Branch target outside ARM range')
    return opcode | ((distance >> 2) & 0xFFFFFF)


def replacement():
    words = (0xE1A00007, branch(0xB0920, 0xCED28, 0xEB000000),
             0xE59810A0, 0xE0850000, 0xE1500001,
             branch(0xB0930, 0xB0A08, 0x8A000000),
             0xE0D700D1, 0xE3500000, 0x14C60001,
             branch(0xB0940, 0xB0934, 0x1A000000))
    return struct.pack('<10I', *words)


def apply(source):
    expected = struct.pack('<10I', *ORIGINAL_WORDS)
    if source[START:END] != expected:
        raise ValueError('Native name end-insertion source differs')
    result = bytearray(source)
    result[START:END] = replacement()
    return bytes(result)
