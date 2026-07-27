from __future__ import annotations


class FixedInsertError(ValueError):
    pass


def replace_fixed(
    data: bytes, offset: int, original_length: int, replacement: bytes, padding: bytes = b"\0"
) -> bytes:
    if offset < 0 or original_length < 0 or offset + original_length > len(data):
        raise FixedInsertError("replacement range lies outside the file")
    if len(replacement) > original_length:
        raise FixedInsertError(
            f"replacement is {len(replacement)} bytes; maximum is {original_length}"
        )
    if len(padding) != 1:
        raise FixedInsertError("padding must be exactly one byte")
    result = bytearray(data)
    result[offset : offset + original_length] = replacement + padding * (
        original_length - len(replacement)
    )
    return bytes(result)

