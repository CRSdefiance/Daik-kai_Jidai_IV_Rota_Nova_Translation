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


def compress_lz10(data: bytes) -> bytes:
    """Create a deterministic greedy LZ10 stream."""
    if len(data) > 0xFFFFFF:
        raise Lz10Error("LZ10 payload exceeds 24-bit size")
    output = bytearray(b"\x10" + len(data).to_bytes(3, "little"))
    candidates: dict[bytes, list[int]] = {}
    position = 0
    while position < len(data):
        flag_position = len(output)
        output.append(0)
        flags = 0
        for bit in range(7, -1, -1):
            if position >= len(data):
                break
            best_length = 0
            best_distance = 0
            key = data[position : position + 3]
            if len(key) == 3:
                minimum = max(0, position - 4096)
                for previous in reversed(candidates.get(key, [])):
                    if previous < minimum:
                        break
                    length = 3
                    maximum = min(18, len(data) - position)
                    while (
                        length < maximum
                        and data[previous + length] == data[position + length]
                    ):
                        length += 1
                    if length > best_length:
                        best_length = length
                        best_distance = position - previous
                        if length == 18:
                            break
            if best_length >= 3:
                flags |= 1 << bit
                pair = ((best_length - 3) << 12) | (best_distance - 1)
                output.extend(pair.to_bytes(2, "big"))
                consumed = best_length
            else:
                output.append(data[position])
                consumed = 1

            for added in range(consumed):
                added_position = position + added
                added_key = data[added_position : added_position + 3]
                if len(added_key) == 3:
                    bucket = candidates.setdefault(added_key, [])
                    bucket.append(added_position)
                    minimum = added_position - 4096
                    while bucket and bucket[0] < minimum:
                        bucket.pop(0)
            position += consumed
        output[flag_position] = flags
    return bytes(output)
