from __future__ import annotations

import struct
from dataclasses import dataclass

ARM9_LOAD_ADDRESS = 0x02000000


class InputCalendarPatchError(RuntimeError):
    pass


@dataclass(frozen=True)
class Arm9Patch:
    offset: int
    replacement: bytes
    accepted: tuple[bytes, ...]
    description: str


def _fixed(text: str, size: int) -> bytes:
    encoded = text.encode("cp932")
    if len(encoded) > size:
        raise ValueError(f"{text!r} does not fit in {size} bytes")
    return encoded + b"\0" * (size - len(encoded))


def _string_patch(
    offset: int,
    replacement: str,
    size: int,
    description: str,
    *accepted: str,
) -> Arm9Patch:
    replacement_bytes = _fixed(replacement, size)
    accepted_bytes = tuple(_fixed(text, size) for text in accepted)
    return Arm9Patch(
        offset,
        replacement_bytes,
        accepted_bytes + (replacement_bytes,),
        description,
    )


PATCHES = (
    Arm9Patch(
        0x15029C,
        b"Name\0Middle Name\0Last\0Faction\0\0\0",
        (
            _fixed("名", 4)
            + _fixed("ミドルネーム", 16)
            + _fixed("姓", 4)
            + _fixed("勢力名", 8),
            _fixed("1st", 4)
            + _fixed("Middle Name", 16)
            + _fixed("Sur", 4)
            + _fixed("Faction", 8),
            b"Name\0Middle Name\0Last\0Faction\0\0\0",
        ),
        "repacked character-editor popup labels",
    ),
    _string_patch(
        0x14FC3C,
        "Middle: press 英",
        20,
        "middle-name editor heading",
        "ミドルネーム　変更",
        "Middle: Edit",
        "Middle: Edit  ",
    ),
    _string_patch(
        0x14FC64,
        "Faction: press 英",
        20,
        "faction editor heading",
        "勢力名　変更　　　",
        "Faction: Edit",
        "Faction: Edit ",
    ),
    _string_patch(
        0x14FC78,
        "Birthday: Edit",
        20,
        "birthday editor heading",
        "誕生日　変更　　　",
    ),
    _string_patch(0x1502E4, "Done", 8, "character-editor X button", "完了"),
    _string_patch(0x150378, "M\n", 4, "month suffix used by all 12 months", "月\n"),
    _string_patch(0x15037C, "Birth", 8, "birthday popup fallback heading", "誕生日"),
    _string_patch(0x15510C, "英", 4, "restored Latin keyboard-page identifier", "AB", "ABC"),
    _string_patch(0x1550F4, "記", 4, "restored symbol keyboard-page identifier", "#+"),
    _string_patch(0x1331A0, "Days: %6d", 12, "shared duration format", "日数  %6d日"),
    _string_patch(0x133FF4, "~%d d", 8, "approximate voyage duration", "約%d日"),
    _string_patch(0x143D78, "3 Days", 8, "inn 3-day option", "３日"),
    _string_patch(0x143D88, "30 Days", 8, "inn 30-day option", "３０日"),
    _string_patch(0x143D90, "10 Days", 8, "inn 10-day option", "１０日"),
    _string_patch(0x143DA0, "Stay 1 Day", 12, "inn one-day command", "一日泊まる"),
    _string_patch(0x143DAC, "Stay More", 16, "inn continued-stay command", "続けて泊まる"),
    _string_patch(0x143DCC, "Last Mo", 8, "inn previous-month label", "先月"),
    _string_patch(0x143DD4, "This Mo", 8, "inn current-month label", "今月"),
    _string_patch(0x143DDC, "%s Mo. Ago", 12, "relative-month format A", "%sカ月前"),
    _string_patch(0x143DE8, "%s Mo. Ago", 12, "relative-month format B", "%sカ月前"),
    _string_patch(0x16AFB0, "Arr. Mo.", 8, "alternate arrival-month label", "入荷月"),
    Arm9Patch(
        0x14FC28,
        _fixed("Name: press 英", 20),
        (
            _fixed("名　変更　　　　　", 20),
            _fixed("Name: Edit", 20),
            _fixed("Name: Edit    ", 20),
            b"Name: Edit    \0Name\0",
            _fixed("Name: press 英", 20),
        ),
        "name editor heading with Latin-key guidance",
    ),
    Arm9Patch(
        0x14FC50,
        _fixed("Last: press 英", 20),
        (
            _fixed("姓　変更　　　　　", 20),
            _fixed("Last: Edit", 20),
            _fixed("Last: Edit    ", 20),
            b"Last: Edit    \0Last\0",
            _fixed("Last: press 英", 20),
        ),
        "surname editor heading with Latin-key guidance",
    ),
    Arm9Patch(
        0x9E058,
        struct.pack("<I", ARM9_LOAD_ADDRESS + 0x15029C),
        (
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x15029C),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x14FC37),
        ),
        "first-name popup pointer",
    ),
    Arm9Patch(
        0x9E060,
        struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502A1),
        (
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502A0),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502A1),
        ),
        "middle-name popup pointer",
    ),
    Arm9Patch(
        0x9E064,
        struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502AD),
        (
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502B0),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x14FC5F),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502AD),
        ),
        "surname popup pointer",
    ),
    Arm9Patch(
        0x9E068,
        struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502B2),
        (
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502B4),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1502B2),
        ),
        "faction popup pointer",
    ),
    Arm9Patch(
        0x14FC22,
        b"d",
        (b"D", b"d"),
        "Birthday RTTI spelling reused by the calendar heading",
    ),
    Arm9Patch(
        0xA0678,
        struct.pack("<I", ARM9_LOAD_ADDRESS + 0x14FC1D),
        (
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x15037C),
            struct.pack("<I", ARM9_LOAD_ADDRESS + 0x14FC1D),
        ),
        "birthday calendar heading pointer",
    ),
)


def patch_nds_bytes(rom: bytes) -> tuple[bytes, tuple[str, ...]]:
    if len(rom) < 0x30:
        raise InputCalendarPatchError("file is too small to be a Nintendo DS ROM")
    arm9_offset, _, _, arm9_size = struct.unpack_from("<IIII", rom, 0x20)
    arm9_end = arm9_offset + arm9_size
    if arm9_end > len(rom):
        raise InputCalendarPatchError("ARM9 range extends beyond the ROM")

    output = bytearray(rom)
    applied: list[str] = []
    for patch in PATCHES:
        if patch.offset + len(patch.replacement) > arm9_size:
            raise InputCalendarPatchError(
                f"{patch.description} lies outside ARM9 at 0x{patch.offset:X}"
            )
        start = arm9_offset + patch.offset
        current = bytes(output[start : start + len(patch.replacement)])
        if current not in patch.accepted:
            raise InputCalendarPatchError(
                f"unexpected bytes for {patch.description} at ARM9+0x{patch.offset:X}: "
                f"{current.hex().upper()}"
            )
        output[start : start + len(patch.replacement)] = patch.replacement
        applied.append(patch.description)
    return bytes(output), tuple(applied)
