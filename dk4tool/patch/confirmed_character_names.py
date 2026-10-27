"""Source-locked confirmed name fields; not a standalone playable release."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE = 0x02000000
SOURCE = "9c03e253a6e91231a7e6d7ee112c07c632a3cfe16b2a33d2d349cc1e45857958"
CLEAN = "0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731"
FIELDS = (
    ("RAFAEL_GIVEN_NAME", 0, 0, 0x15CA40, 12, "ラファエル", "Raphael", "Rafael"),
    ("CAMILLE_GIVEN_NAME", 9, 0, 0x15BF08, 8, "カミル", "Kamil", "Camille"),
    ("JOAKIM_MIDDLE_NAME", 1, 8, 0x15C3D4, 12, "ヨアキム", "Joachim", "Joakim"),
    ("MARIA_SURNAME", 3, 4, 0x15BAB8, 8, "リー", "Lee", "Li"),
    ("MARIA_MIDDLE_NAME", 3, 8, 0x15C1F4, 12, "ホアメイ", "ホアメイ", "Huamei"),
)


def transform(source, clean):
    if sha(source) != SOURCE or sha(clean) != CLEAN:
        raise ValueError("Exact complete V190 ARM9 and clean Japanese source required")
    result, records = bytearray(source), []
    for record_id, index, column, offset, capacity, japanese, old, english in FIELDS:
        field = 0x120B80 + index * 32 + column
        pointer = BASE + offset
        if any(struct.unpack_from("<I", raw, field)[0] != pointer for raw in (source, clean)):
            raise ValueError("Confirmed name owner/table field changed")
        expected = (old.encode("cp932") + b"\0").ljust(capacity, b"\0")
        original = (japanese.encode("cp932") + b"\0").ljust(capacity, b"\0")
        if source[offset:offset + capacity] != expected or clean[offset:offset + capacity] != original:
            raise ValueError("Confirmed name source/allocation differs")
        references = [at for at in range(len(source) - 3)
                      if source[at:at + 4] == struct.pack("<I", pointer)]
        if references != [field]:
            raise ValueError("Confirmed name has unclassified static aliases")
        encoded = english.encode("ascii") + b"\0"
        if len(encoded) > capacity:
            raise ValueError("Complete confirmed name exceeds its verified allocation")
        result[offset:offset + capacity] = encoded.ljust(capacity, b"\0")
        records.append({"id": record_id, "index": index, "column": column,
                        "table_field": field, "pointer": pointer, "offset": offset,
                        "capacity": capacity, "japanese": japanese,
                        "before": old, "after": english,
                        "source_hex": expected.hex(), "replacement_hex": result[offset:offset + capacity].hex()})
    saved = bytes(result)
    old_code, new_code = MainCodeFile(source, BASE), MainCodeFile(saved, BASE)
    if len(old_code.sections) != len(new_code.sections) or any(
        (left.ramAddress, left.bssSize, bytes(left.data)) !=
        (right.ramAddress, right.bssSize, bytes(right.data))
        for left, right in zip(old_code.sections[1:], new_code.sections[1:], strict=True)
    ):
        raise ValueError("Confirmed names change native/staged section ownership")
    restored = bytearray(saved)
    for row in records:
        start, end = row["offset"], row["offset"] + row["capacity"]
        restored[start:end] = source[start:end]
    if bytes(restored) != source:
        raise ValueError("Confirmed names change unrelated bytes, pointers or instructions")
    return saved, {"source_arm9_sha256": sha(source), "target_arm9_sha256": sha(saved),
                   "records": records, "all_other_bytes_and_section_ownership_preserved": True,
                   "requires_complete_text_macro_and_artwork_migration_before_playable_release": True}
