from __future__ import annotations


class Lz10Error(ValueError):
    pass


def is_lz10(data: bytes) -> bool:
    if len(data) < 4 or data[0] != 0x10:
        return False
    expected = int.from_bytes(data[1:4], "little")
    return 0 < expected <= 0xFFFFFF


def decompress_lz10(data: bytes) -> bytes:
    if not is_lz10(data):
        raise Lz10Error("not an LZ10 stream")
    expected = int.from_bytes(data[1:4], "little")
    source = 4
    output = bytearray()
    while len(output) < expected:
        if source >= len(data):
            raise Lz10Error("truncated LZ10 flag byte")
        flags = data[source]
        source += 1
        for bit in range(7, -1, -1):
            if len(output) >= expected:
                break
            if flags & (1 << bit):
                if source + 1 >= len(data):
                    raise Lz10Error("truncated LZ10 back-reference")
                pair = (data[source] << 8) | data[source + 1]
                source += 2
                length = (pair >> 12) + 3
                distance = (pair & 0xFFF) + 1
                if distance > len(output):
                    raise Lz10Error("invalid LZ10 back-reference")
                for _ in range(length):
                    output.append(output[-distance])
                    if len(output) >= expected:
                        break
            else:
                if source >= len(data):
                    raise Lz10Error("truncated LZ10 literal")
                output.append(data[source])
                source += 1
    return bytes(output)


def compress_lz10_literals(data: bytes) -> bytes:
    """Create a valid, deterministic literal-only LZ10 stream for tests and small data."""
    if len(data) > 0xFFFFFF:
        raise Lz10Error("LZ10 payload exceeds 24-bit size")
    output = bytearray(b"\x10" + len(data).to_bytes(3, "little"))
    for offset in range(0, len(data), 8):
        output.append(0)
        output.extend(data[offset : offset + 8])
    return bytes(output)

