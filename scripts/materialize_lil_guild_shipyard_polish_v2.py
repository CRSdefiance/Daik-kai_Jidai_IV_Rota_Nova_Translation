from __future__ import annotations

import json
import struct
from hashlib import sha256
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import PROFILES

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "out/raphael_natural_v2_accepted_base.nds"
CLEAN = ROOT / "work/clean.nds"
ARM9_HASH = "9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5"
COMMON_HASH = "75d48f50da7b3a4185276048a3779dee3e1dfb503dee5f228f88c9023dbc629c"
POOL_START = 0x1720A8
POOL_END = 0x172464

# The dialogue codec treats an ASCII ``F`` as the start of the FI/FA/FO/FU
# runtime-macro family even when the byte came from a dynamic name expansion.
# Use the CP932 full-width glyph for every live entity-table name that would
# otherwise begin with that reserved byte.  The glyph is visually an F, while
# its two-byte encoding cannot be consumed as a dialogue macro.
RUNTIME_F_NAME_POINTERS = {
    0x120D44: "Ｆerog",
    0x120DA8: "Ｆerid",
    0x120E00: "Ｆernando",
    0x120FC8: "Ｆazul",
    0x120FE0: "Ｆernan",
    0x121088: "Ｆong",
    0x121264: "Ｆlahven",
    0x1221C0: "Ｆollower",
    0x1222C0: "Ｆrancisca",
    0x1223C0: "Ｆaticia",
}


ENTITY_TRANSLATIONS = {
    "広場の店主": "Shopkeeper",
    "アフリカ": "African",
    "イスラム": "Arab",
    "インド": "Indian",
    "東南アジア": "SE Asian",
    "中国": "Chinese",
    "韓国": "Korean",
    "日本": "Japanese",
    "インディオ": "Native",
    "ヨーロッパ": "European",
    "ヨーロッパ１": "European 1",
    "ヨーロッパ２": "European 2",
    "ヨーロッパ３": "European 3",
    "造船所の親父": "Shipwright",
    "衛兵": "Guard",
    "地方領主": "Local Lord",
    "地方王": "Local King",
    "県令": "Magistrate",
    "大名": "Daimyo",
    "祭主": "Priest",
    "祈祷師": "Shaman",
    "高僧": "Monk",
    "神父": "Priest",
    "配下": "Retainer",
    "村民": "Villager",
    "アジア": "Asian",
    "男の子": "Boy",
    "カップル男": "Young Man",
    "カップル女": "Young Woman",
    "貴婦人": "Lady",
    "妖艶な女": "Enchantress",
    "謎の老人": "Old Man",
    "国籍不明": "Unknown",
    "研究生": "Student",
    "オランダ": "Dutch",
    "行き倒れ": "Castaway",
    "アフリカ水夫": "African Sailor",
    "怪しい人": "Stranger",
    "アラブ水夫": "Arab Sailor",
    "オーナー": "Owner",
    "貴婦人３": "Lady",
    "コック": "Cook",
    "酒場親父": "Barkeep",
    "私掠艦隊": "Privateers",
    "教祖": "Sect Leader",
    "イベント用": "Event",
    "信徒": "Follower",
    "アメリカ": "American",
    "野盗": "Bandit",
    "怪物": "Monster",
    "洋上イベント": "Sea Event",
    "探検家": "Explorer",
    "スネーク": "Snake",
    "ロンドン": "London",
    "ドナ": "Donna",
    "セビリア": "Seville",
    "アテネ": "Athens",
    "ハトラ": "Hatra",
    "サフィア": "Safia",
    "大坂": "Osaka",
}


MYSTERY_NAMES = (
    (0x16BD80, 8, "Cursed"),
    (0x16BD88, 12, "Ancient Map"),
    (0x16BD94, 12, "Witch Idol"),
    (0x16BDA0, 12, "Dragon Horn"),
    (0x16BDAC, 12, "Lion's Eye"),
    (0x16BDB8, 12, "Gajarg"),
    (0x16BDC4, 12, "%s Map 4"),
    (0x16BDD0, 12, "Jiganemaru"),
    (0x16BDDC, 12, "%s Map 2"),
    (0x16BDE8, 12, "Old Dagger"),
    (0x16BDF4, 12, "%s Map 3"),
    (0x16BE00, 12, "%s Map 1"),
    (0x16BE24, 16, "King's Shield"),
    (0x16BE34, 16, "Prydwen"),
    (0x16BE44, 16, "Giant Red Spear"),
    (0x16BE54, 16, "Serpent Mask"),
    (0x16BE64, 16, "Flame Gem"),
    (0x16BE74, 16, "Untouched Blade"),
    (0x16BE84, 16, "Twisted Horn"),
    (0x16BEA4, 16, "Eerie Mask"),
    (0x16BEB4, 16, "Gem-Eating Gem"),
    (0x16BEC4, 16, "Ruinous Siren"),
    (0x16BEE4, 20, "Clear Rose Quartz"),
    (0x16BF34, 24, "Star Rose Quartz"),
    (0x16BF4C, 24, "Rutilated Phantom"),
)


def c_string(data: bytes, offset: int, limit: int = 64) -> bytes:
    end = data.find(b"\0", offset, min(len(data), offset + limit))
    if end < 0:
        raise ValueError(f"unterminated string at {offset:#x}")
    return data[offset:end]


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def arm9_record(
    arm9: bytes,
    row_id: str,
    offset: int,
    size: int,
    english: str,
    context: str,
    *,
    forbid_visible_leading_space: bool | None = None,
) -> dict[str, object]:
    encoded = english.encode("ascii")
    if len(encoded) >= size:
        raise ValueError(f"{row_id}: {english!r} leaves no room for a NUL in {size} bytes")
    record: dict[str, object] = {
        "id": row_id,
        "offset": offset,
        "source_hex": arm9[offset : offset + size].hex().upper(),
        "english": english,
        "string_kind": "c-string",
        "context": context,
    }
    if forbid_visible_leading_space is not None:
        record["forbid_visible_leading_space"] = forbid_visible_leading_space
    return record


def guarded_text(text: str, *, entry_guard: int = 2, line_guard: int = 2) -> bytes:
    """Encode visible text with renderer-consumed entry and LF guards."""

    lines = text.split("\n")
    return (
        b" " * entry_guard
        + (b"\n" + b" " * line_guard).join(line.encode("ascii") for line in lines)
    )


def packed_screen_record(
    current: bytes,
    starts: list[int],
    texts: list[str],
    row_id: str,
    context: str,
    *,
    width: int,
    ends: list[int] | None = None,
    entry_guard: int = 2,
    line_guard: int = 2,
    preserve_placeholders: bool = True,
    ascii_guard_exemption: str | None = None,
) -> dict[str, object]:
    """Build a fixed record while preserving every live interior entry point."""

    if len(starts) != len(texts) or starts != sorted(set(starts)):
        raise ValueError(f"{row_id}: invalid packed entry declaration")
    if ends is None:
        ends = starts[1:] + [len(current)]
    if len(ends) != len(starts):
        raise ValueError(f"{row_id}: entry end count mismatch")
    replacement = bytearray(current)
    translated_ranges: list[list[int]] = []
    for index, (start, end, text) in enumerate(zip(starts, ends, texts, strict=True)):
        if not 0 <= start < end <= len(current):
            raise ValueError(f"{row_id}[{index}]: invalid {start}:{end} range")
        if any(len(line) > width for line in text.split("\n")):
            raise ValueError(f"{row_id}[{index}]: visible line exceeds {width} characters")
        encoded = guarded_text(text, entry_guard=entry_guard, line_guard=line_guard)
        if len(encoded) > end - start:
            raise ValueError(
                f"{row_id}[{index}]: {len(encoded)} bytes exceed {end - start}"
            )
        if preserve_placeholders:
            source_macros = [current[start:end][hit : hit + 2] for hit in range(end - start - 1) if current[start + hit] == 0x25 and current[start + hit + 1] in (0x64, 0x73)]
            target_macros = [encoded[hit : hit + 2] for hit in range(len(encoded) - 1) if encoded[hit] == 0x25 and encoded[hit + 1] in (0x64, 0x73)]
            if source_macros != target_macros:
                raise ValueError(f"{row_id}[{index}]: printf placeholders changed")
        replacement[start:end] = encoded.ljust(end - start, b" ")
        translated_ranges.append([start, end])
    record: dict[str, object] = {
        "id": row_id,
        "english": " / ".join(text.replace("\n", " ") for text in texts),
        "display_entries": [
            ("\n" + " " * line_guard).join(text.split("\n")) for text in texts
        ],
        "replacement_hex": bytes(replacement).hex().upper(),
        "entry_offsets": starts,
        "entry_ends": ends,
        "entry_guard_bytes": entry_guard,
        "linebreak_guard_bytes": line_guard,
        "translated_ranges": translated_ranges,
        "text_box_max_chars": width,
        "context": context,
    }
    if ascii_guard_exemption:
        record["ascii_guard_exemption"] = ascii_guard_exemption
    return record


def materialize_entity_names(arm9: bytes) -> None:
    pointer_targets: dict[int, str] = {}
    for pointer_offset in range(0x121600, 0x122501, 4):
        target = struct.unpack_from("<I", arm9, pointer_offset)[0] - 0x02000000
        if not 0x15B000 <= target < 0x15E400:
            continue
        try:
            text = c_string(arm9, target).decode("cp932")
        except UnicodeDecodeError:
            continue
        if text in ENTITY_TRANSLATIONS:
            pointer_targets[pointer_offset] = ENTITY_TRANSLATIONS[text]

    # The previous fixed-slot pass filled these strings to capacity. Redirect
    # their live pointer-table entries so the full names remain NUL-terminated.
    for entry in PROFILES["all"]:
        if not entry.row_id.startswith(("DK4_CITY_", "DK4_SHIP_MODEL_")):
            continue
        encoded = entry.suggested_english.encode("ascii")
        if len(encoded) != entry.source_length:
            continue
        if arm9[entry.offset : entry.offset + entry.source_length] != encoded:
            continue
        if arm9[entry.offset + entry.source_length] == 0:
            continue
        pointer = struct.pack("<I", 0x02000000 + entry.offset)
        start = 0
        while True:
            hit = arm9.find(pointer, start)
            if hit < 0:
                break
            start = hit + 1
            if 0x110000 <= hit < 0x130000:
                pointer_targets[hit] = entry.suggested_english

    pointer_targets[0x11E0B0] = "Arnhem"
    pointer_targets[0x1224A4] = "Hangzhou"
    # Runtime substitutions for the at-sea "%s has run out" warning.  The
    # Japanese strings themselves are too small for "Water", so redirect the
    # two live pointers into the same terminated relocation pool.
    pointer_targets[0x0A4C34] = "Water"
    pointer_targets[0x0A4C38] = "Food"
    pointer_targets.update(RUNTIME_F_NAME_POINTERS)

    pool = bytearray()
    addresses: dict[str, int] = {}
    for text in dict.fromkeys(pointer_targets.values()):
        addresses[text] = POOL_START + len(pool)
        pool.extend(text.encode("cp932") + b"\0")
    if POOL_START + len(pool) > POOL_END:
        raise ValueError("entity-name relocation pool overflow")

    records: list[dict[str, object]] = []
    for pointer_offset, text in sorted(pointer_targets.items()):
        records.append(
            {
                "id": f"DK4_ENTITY_POINTER_{pointer_offset:06X}",
                "offset": pointer_offset,
                "source_hex": arm9[pointer_offset : pointer_offset + 4].hex().upper(),
                "replacement_hex": struct.pack("<I", 0x02000000 + addresses[text]).hex().upper(),
                "english": text,
                "context": "Redirect a live entity, speaker, place, or ship name to terminated English storage.",
            }
        )
    pool_size = POOL_END - POOL_START
    records.append(
        {
            "id": "DK4_ENTITY_NAME_RELOCATION_POOL",
            "offset": POOL_START,
            "source_hex": arm9[POOL_START:POOL_END].hex().upper(),
            "replacement_hex": bytes(pool).ljust(pool_size, b"\0").hex().upper(),
            "context": "NUL-terminated English storage for live entity and ship-name pointers.",
            "notes": f"Uses {len(pool)} of {pool_size} bytes remaining after the accepted item-name pool.",
        }
    )
    write_json(
        ROOT / "translations/entity_ship_names_arm9_v2.json",
        {
            "format": "dk4-arm9-fixed-text-batch-v1",
            "file_path": "/__arm9__.bin",
            "source_file_sha256": ARM9_HASH,
            "target_locale": "en-US",
            "scope": "All live residual entity-role, nationality, place, and starting-ship pointers plus NUL repairs",
            "records": records,
        },
    )


def materialize_arm9_ui(arm9: bytes) -> None:
    records = [
        arm9_record(arm9, "DK4_YARD_RESET_BUTTON_V2", 0x11B5EC, 12, "Undo", "Visible Y-button label in the remodel screen."),
        arm9_record(arm9, "DK4_YARD_EQUIPMENT_TITLE_V2", 0x133154, 12, "Refit", "Narrow remodel-screen heading."),
        arm9_record(
            arm9,
            "DK4_GUILD_TREASURE_PITCH_WRAP_V3",
            0x143D20,
            88,
            "You're in luck!\n This old map may lead\n to legendary treasure.",
            "Guild treasure pitch kept below the renderer's automatic-wrap boundary.",
        ),
        arm9_record(
            arm9,
            "DK4_ASSIGN_FLAGSHIP_FIRST",
            0x133F28,
            32,
            "Assigned to flagship first.",
            "Fleet screen confirmation after flagship-priority sailor assignment.",
        ),
        arm9_record(
            arm9,
            "DK4_ASSIGN_EVENLY",
            0x133F48,
            32,
            "Sailors assigned evenly.",
            "Fleet screen confirmation after even sailor assignment.",
        ),
        arm9_record(
            arm9,
            "DK4_ASSIGN_MINIMUM",
            0x133F68,
            36,
            "Minimum sailors assigned.",
            "Fleet screen confirmation after minimum sailor assignment.",
        ),
        arm9_record(arm9, "DK4_FULL_NAME_FORMAT_A", 0x1484CC, 8, "%s %s", "English full-name composition without the Shift-JIS interpunct."),
        arm9_record(arm9, "DK4_FULL_NAME_FORMAT_B", 0x14FBBC, 8, "%s %s", "Second live English full-name composition format."),
        arm9_record(arm9, "DK4_FULL_NAME_SEPARATOR_A", 0x1484DC, 4, " ", "ASCII separator used by the crew-recruitment full-name composer.", forbid_visible_leading_space=False),
        arm9_record(arm9, "DK4_FULL_NAME_SEPARATOR_B", 0x1484E0, 4, " ", "Second ASCII separator used by the crew-recruitment full-name composer.", forbid_visible_leading_space=False),
    ]
    for row_id, offset, size, english in (
        ("DK4_ITEM_TYPE_WEAPON", 0x13C270, 8, "Weapon"),
        ("DK4_ITEM_TYPE_ARMOR", 0x13C278, 8, "Armor"),
        ("DK4_ITEM_TYPE_MISC", 0x13C280, 8, "Misc"),
        ("DK4_ITEM_TYPE_PRODUCT", 0x13C288, 8, "Product"),
        ("DK4_ITEM_TYPE_FIGURE", 0x13C290, 8, "Figure"),
        ("DK4_ITEM_TYPE_GEAR", 0x13C298, 8, "Gear"),
        ("DK4_ITEM_TYPE_MYSTERY", 0x13C2B0, 12, "Mystery"),
        ("DK4_ITEM_TYPE_PROOF", 0x13C2BC, 12, "Proof"),
        ("DK4_ITEM_TYPE_RUIN_MAP", 0x13C2C8, 12, "Ruin Map"),
        ("DK4_ITEM_TYPE_OLD_MAP", 0x13C2D4, 12, "Old Map"),
        ("DK4_ITEM_TYPE_SEA_GEAR", 0x13C2E0, 12, "Sea Gear"),
        ("DK4_ITEM_TYPE_PROOF_MAP", 0x13C2EC, 12, "Proof Map"),
    ):
        records.append(
            arm9_record(
                arm9,
                row_id,
                offset,
                size,
                english,
                "Item-detail type label used by Guild and inventory screens.",
            )
        )
    for index, (offset, size, english) in enumerate(MYSTERY_NAMES):
        records.append(
            arm9_record(
                arm9,
                f"DK4_MYSTERY_ITEM_{index:02d}",
                offset,
                size,
                english,
                "Mystery Hunt item, ancient-map type, or generated map-title component.",
            )
        )
    write_json(
        ROOT / "translations/shipyard_guild_mystery_ui_arm9_v2.json",
        {
            "format": "dk4-arm9-fixed-text-batch-v1",
            "file_path": "/__arm9__.bin",
            "source_file_sha256": ARM9_HASH,
            "target_locale": "en-US",
            "scope": "Shipyard clipping, Guild wrapping, and all Mystery Hunt item names",
            "fixed_text_policy": {
                "require_c_string_termination": True,
                "maximum_prose_line_characters": 31,
                "forbid_visible_leading_space": True,
                "linebreak_guard_bytes": 1,
            },
            "records": records,
        },
    )


def materialize_common(common: bytes, clean_common: bytes) -> None:
    container = IlnkContainer.parse(common)
    clean_container = IlnkContainer.parse(clean_common)

    shipyard = container.blocks[15].split(b"\0")[63]
    shipyard_text = b"Lateen sails favor\nheadwinds.\nNo square sail behind."
    write_json(
        ROOT / "translations/common_shipyard_layout_v2.json",
        {
            "format": "dk4-ilnk-translation-batch-v1",
            "file_path": "/COMMON/MESFILE.DK4",
            "source_file_sha256": COMMON_HASH,
            "target_locale": "en-US",
            "scope": "Shipyard equipment help reflowed for its narrow visible text box",
            "ascii_guard_exemption": "This help renderer displays leading ASCII bytes literally; explicit line breaks replace sacrificial guards.",
            "fixed_allocation_policy": "screen-entry-layout-v1",
            "records": [
                packed_screen_record(
                    shipyard,
                    [0],
                    [shipyard_text.decode("ascii")],
                    "DK4_MES_B15_R0063",
                    "Lateen sail help in the shipyard equipment screen.",
                    width=24,
                    entry_guard=0,
                    line_guard=0,
                )
            ],
        },
    )

    block32 = container.blocks[32].split(b"\0")
    descriptions: list[dict[str, object]] = [
        packed_screen_record(
            block32[12],
            [89],
            ["Rainbow-colored glass marbles,\ncrafted by a secret process\nknown only to their makers."],
            "DK4_MES_B32_R0012",
            "Rainbow Marbles description with explicit word-boundary wrapping.",
            width=40,
            ends=[181],
            entry_guard=0,
            line_guard=2,
            ascii_guard_exemption="This packed interior item-description entry displays its first byte but consumes two bytes after LF.",
        ),
        packed_screen_record(
            block32[13],
            [77],
            ["A graceful watercolor by Huizong,\nthe artist-emperor of Northern Song."],
            "DK4_MES_B32_R0013",
            "Huizong watercolor description with explicit word-boundary wrapping.",
            width=40,
            ends=[177],
            entry_guard=0,
            line_guard=2,
            ascii_guard_exemption="This packed interior item-description entry displays its first byte but consumes two bytes after LF.",
        ),
        packed_screen_record(
            block32[19],
            [0],
            ["A light silk robe woven from\nexceptionally fine white thread."],
            "DK4_MES_B32_R0019",
            "White silk robe description with its consumed source entry guard.",
            width=40,
        ),
    ]
    write_json(
        ROOT / "translations/guild_item_descriptions_layout_v3.json",
        {
            "format": "dk4-ilnk-translation-batch-v1",
            "file_path": "/COMMON/MESFILE.DK4",
            "source_file_sha256": COMMON_HASH,
            "target_locale": "en-US",
            "scope": "Guild item descriptions with screen-specific entry guards and word-boundary wrapping",
            "ascii_guard_policy": "two-byte-entry-and-line-v1",
            "fixed_allocation_policy": "screen-entry-layout-v1",
            "records": descriptions,
        },
    )

    block33 = container.blocks[33].split(b"\0")
    clean33 = clean_container.blocks[33].split(b"\0")
    maps: list[dict[str, object]] = []

    def marker_starts(source: bytes, markers: list[str]) -> list[int]:
        starts = [0]
        for marker in markers:
            offset = source.find(marker.encode("cp932"), starts[-1] + 1)
            if offset <= starts[-1]:
                raise ValueError(f"missing or unordered packed marker {marker!r}")
            starts.append(offset)
        return starts

    item_rows: dict[int, tuple[list[str], list[str]]] = {
        0: (["木製の札"], [
            "India's oldest scriptures, dating\nfrom the 15th-10th centuries BC.",
            "A wooden Kediri plaque said to\nprotect every islander from harm.",
        ]),
        1: (["水晶をきれい"], [
            "A bronze candlestick used by Qin\nShi Huang while building palaces.",
            "A polished crystal skull whose\ncreation remains a mystery.",
        ]),
        4: (["古びた地図。枯れる"], [
            "An old map carved into stone.",
            "An old map drawn on an unfading\nlotus leaf.",
        ]),
        5: (["古びた地図。太い竹"], [
            "An old map disguised as a pattern.",
            "An old map drawn inside split\nbamboo.",
        ]),
        6: ([], ["An old map carved on a large\nknife blade."]),
        7: (["古代ローマ帝国", "アナトリアの古い"], [
            "South England map with a\nmysterious mark.",
            "Map of ancient Rome and most\nof Italy.",
            "Old Anatolian map marking a\nhidden Christian village.",
        ]),
        8: ([], ["A Sahara map used by caravans\ntrading with legendary Timbuktu."]),
        9: (["インド北部の大帝国"], [
            "A mysterious map with the King's\nMosque marked at its center.",
            "A detailed Mughal map showing the\nroute to Delhi.",
        ]),
        10: ([], ["An ancient Cambodian map with a\npalace-temple at its center."]),
        11: (["偉大なる王の墓所", "黄金の国ジパング"], [
            "A northern China map showing the\nroute to Beijing.",
            "A partly illegible map leading to\na great king's tomb.",
            "A map leading to a legendary\ntemple in golden Zipangu.",
        ]),
        12: ([], ["A map recording travel between a\nruined city and a distant island."]),
        13: ([], ["An Aztec pictorial codex containing\na map of the kingdom."]),
        14: ([], ["Blank parchment; its purpose is\nunknown."]),
        15: (["謎の紋様が刻み", "太古の時代", "古代の王国"], [
            "Cloth covered in strange patterns.",
            "Upper half of a carved tablet.",
            "An ancient, ever-living lotus leaf.",
            "A badly corroded coin from an\nancient kingdom.",
        ]),
        16: (["新大陸の古代王朝"], [
            "Intricate bamboo work made in\nTang-dynasty China.",
            "A ceremonial knife from an ancient\nNew World dynasty; not a weapon.",
        ]),
        17: ([], ["A vivid pigment of unknown origin,\nnot used by ordinary painters."]),
        18: (["謎の紋様が刻み", "古代インドにて", "乳白色の液体", "竹細工の組み", "太陽を形取った", "燃えるように", "古代文字が刻まれた"], [
            "A brass lamp apparently used in\nceremonies.",
            "Lower half of a carved tablet.",
            "An ancient Indian object apparently\nused as tribute.",
            "Jar of milky white liquid.",
            "Bamboo assembly diagram.",
            "A dagger sheath carved with a sun\nemblem.",
            "A fiery red gemstone.",
            "A dagger with ancient writing, used\nin rites to ward off evil.",
        ]),
        19: (["六条の星が"], [
            "A stone mask bearing two carved\nserpents, used by ancient priests.",
            "A crimson crystal with a rare,\nclear six-rayed star.",
        ]),
        21: ([], ["A treasured blade from an eastern\nisland, sharp enough to cut afar."]),
        22: ([], ["A siren figurehead said to wreck\nships with its song."]),
        23: (["女神の姿が"], [
            "A twisted horn of uncertain origin,\nsaid to cure every illness.",
            "A great king's shield bearing a\ngoddess, prized by sailors.",
        ]),
        24: (["古の地図の断片"], [
            "A giant red spear said to ward off\nevil and protect its bearer.",
            "Map fragment. Collect all four.",
        ]),
    }
    for row, (markers, texts) in item_rows.items():
        starts = marker_starts(clean33[row], markers)
        maps.append(
            packed_screen_record(
                block33[row],
                starts,
                texts,
                f"DK4_MES_B33_R{row:04d}",
                "Mystery, map, or artifact description with preserved packed entry boundaries.",
                width=40,
            )
        )
    for row in range(25, 44):
        maps.append(
            packed_screen_record(
                block33[row],
                [0],
                ["Map fragment. Collect all four."],
                f"DK4_MES_B33_R{row:04d}",
                "Ancient-map fragment item description.",
                width=40,
            )
        )

    block40 = container.blocks[40].split(b"\0")
    clean40 = clean_container.blocks[40].split(b"\0")
    appraisal_rows: dict[int, tuple[list[str], list[str]]] = {
        0: ([], ["From the North Sea."]),
        1: ([], ["In North Sea waters."]),
        2: ([], ["From the North Sea."]),
        3: (["秘宝が眠るは地中海", "秘宝が眠るはアフリカ"], [
            "From the Mediterranean.",
            "In Mediterranean waters.",
            "In African waters.",
        ]),
        4: ([], ["In North Sea waters."]),
        5: (["秘宝が眠るはアフリカ"], ["In Mediterranean waters.", "In African waters."]),
        6: ([], ["In African waters."]),
        7: ([], ["In African waters."]),
        8: ([], ["In Indian Ocean waters."]),
        9: ([], ["In Indian Ocean waters."]),
        10: (["秘宝を得たくば", "秘宝が眠るは東南アジア", "秘宝が眠るは東アジア"], [
            "In SE Asian waters.",
            "From Southeast Asia.",
            "In SE Asian waters.",
            "In East Asian waters.",
        ]),
        11: ([], ["Just north."]),
        12: (["はるか北東", "はるか北西", "その北西", "はるか北へ"], [
            "Center.",
            "Far northeast.",
            "Far northwest.",
            "Northwest.",
            "Far north.",
        ]),
        13: ([], ["Far west."]),
        14: (["その北西にてその中央", "その中央にてその中央にてその中央", "その中央にてその中央にてそのやや南", "その中央にてそのやや南", "そのやや南"], [
            "Northwest.",
            "Northwest.",
            "Center.",
            "Center.",
            "Center.",
            "Just south.",
        ]),
        15: (["その西にて"], ["Southeast.", "West."]),
        16: (["そのやや西"], ["Due south.", "Westward."]),
        17: ([], ["Far south."]),
        18: ([], ["Just south."]),
        19: (["そは戦士の護符"], ["Northeast.", "A warrior's charm said to grant\na lion's strength."]),
        20: (["そは蛇神の面"], [
            "A weapon once used in rites\nto drive away evil.",
            "A serpent-god mask said to\nprotect warriors.",
        ]),
        21: (["そは心力を高める", "そは恐ろしき武器"], [
            "A gunner's treasure. Its bearer\nnever misses.",
            "A treasure said to sharpen the\nmind and bring great wealth.",
            "A fearsome blade said to cut\nwithout touching its target.",
        ]),
        22: (["そは異形のツノ", "そは王の盾", "そは破邪の武器"], [
            "A symbol of destruction said to\nsink every opposing ship.",
            "A strange horn said to ward off\nall disease.",
            "King's shield; goddess-blessed\nto repel disaster.",
            "Red spear with the power\nto drive out evil.",
        ]),
        23: ([], ["A strange gem colored like\na living flame."]),
        24: ([], ["A very old dagger engraved with\nwriting no one can read today."]),
        25: (["紅色の水晶"], [
            "A priest's stone mask carved\nwith an eerie serpent.",
            "A crimson crystal that reveals\na star when held to light.",
        ]),
        26: ([], ["A strange crystal containing a\ndiamond--a gem that eats gems."]),
        27: (["セイレーンの姿"], [
            "A blade said to cut things\nwithout even touching them.",
            "A siren statue once used as a\nship's figurehead.\nUnbelievable.",
        ]),
        28: ([], ["A twisted horn some call a\ndragon's horn. It may cure\nillness."]),
        29: ([], ["A great king's shield bearing a\ngoddess--a sailor's finest\ncharm."]),
        30: ([], ["A gigantic red spear.\nIt is said to ward off evil."]),
    }
    for row, (markers, texts) in appraisal_rows.items():
        starts = marker_starts(clean40[row], markers)
        maps.append(
            packed_screen_record(
                block40[row],
                starts,
                texts,
                f"DK4_MES_B40_R{row:04d}",
                "Guildmaster appraisal with preserved packed entry boundaries.",
                width=31,
                entry_guard=1,
                line_guard=2,
                ascii_guard_exemption="Guild appraisals consume one byte at entry and two bytes after LF; the detailed layout policy validates both.",
            )
        )
    write_json(
        ROOT / "translations/common_mystery_items_v1.json",
        {
            "format": "dk4-ilnk-translation-batch-v1",
            "file_path": "/COMMON/MESFILE.DK4",
            "source_file_sha256": COMMON_HASH,
            "target_locale": "en-US",
            "scope": "Complete Mystery Hunt map/item descriptions and Guildmaster appraisals",
            "ascii_guard_policy": "two-byte-entry-and-line-v1",
            "fixed_allocation_policy": "screen-entry-layout-v1",
            "records": maps,
        },
    )

    runtime: list[dict[str, object]] = []
    current0 = container.blocks[0].split(b"\0")
    for row, text in {
        54: "Sailors still unassigned.\nContinue?",
        55: "Sailors still unassigned.\nContinue?",
        56: "Extra sailors remain.\nContinue?",
        57: "Sailors still unassigned.\nContinue?",
    }.items():
        runtime.append(
            packed_screen_record(
                current0[row],
                [0],
                [text],
                f"DK4_MES_B00_R{row:04d}",
                "Fleet assignment warning; the count is already visible in the table above.",
                width=31,
                preserve_placeholders=False,
            )
        )

    current13 = container.blocks[13].split(b"\0")
    clean13 = clean_container.blocks[13].split(b"\0")
    guild_rows: dict[int, tuple[list[str], list[str]]] = {
        0: ([], ["Need %s more sailors.\nRecruit more?"]),
        1: (["これでは必要な人数"], [
            "Need %s more sailors.\nRecruit more?",
            "Need %s more sailors.\nRecruit more?",
        ]),
        2: ([], ["Need %s more sailors.\nRecruit more?"]),
        3: ([], ["Need %s more sailors.\nRecruit more?"]),
        4: (["まだ必要人数に", "船室には"], [
            "Need %s more sailors.\nRecruit more?",
            "Need %s more sailors.\nRecruit more?",
            "%s berths remain.\nRecruit more?",
        ]),
        5: ([], ["%s berths remain.\nRecruit more?"]),
        6: ([], ["%s berths remain.\nRecruit more?"]),
        7: (["まだ船室に%s人の\n余裕があるよう", "まだ水夫は", "まだ船室に%s人の\n余裕がありますよ"], [
            "%s berths remain.\nRecruit more?",
            "%s berths remain.\nRecruit more?",
            "%s berths remain.\nRecruit more?",
            "%s berths remain.\nRecruit more?",
        ]),
        26: (["悪いが品切れだ"], [
            "Your parrot is lively.\nMischievous, but adorable.",
            "Sold out.",
        ]),
        27: ([], ["Which item?"]),
        28: ([], ["Price: %s coins.\nIt may be too expensive.\nBuy it?"]),
        29: ([], ["Price: %s coins.\nBuy it?"]),
        30: (["それは高いですね"], ["Thank you!", "That's expensive.\nCan you lower it?"]),
        31: ([], ["Too expensive.\nLower the price."]),
        32: ([], ["Too high.\nLower it."]),
        33: ([], ["Too expensive.\nCan you go lower?"]),
        34: ([], ["Far too expensive!\nYou can do better."]),
        35: ([], ["Too expensive.\nSurely it can be less?"]),
        36: ([], ["That seems expensive.\nGive me a discount."]),
        37: ([], ["The price is too high.\nCheaper?"]),
        38: (["おいおい\n売れるような"], [
            "All right. %s coins.\nIt's a deal.",
            "You have nothing to sell.",
        ]),
        40: ([], ["I'll pay %s coins.\nDeal?"]),
        41: ([], ["You must be joking.\nThis is one of a kind.\nLook again."]),
        42: ([], ["That item is worth far more.\nYour offer is too low."]),
        43: ([], ["This is extremely valuable!\nDid you inspect it?"]),
        44: ([], ["That price?! You may never find\nanother one."]),
        45: ([], ["You must be joking.\nThis is one of a kind.\nLook again."]),
        46: (["安すぎるよ"], [
            "Don't you know its value?\nLook again.",
            "Far too low! Look carefully.\nThis is extremely valuable.",
        ]),
        47: ([], ["Surely you know this is rare.\nLook again."]),
        48: ([], ["Fine. %s coins."]),
        49: (["金貨１０００枚"], [
            "Thank you!",
            "Letter job: 1,000 coins.\nFor another faction.",
        ]),
    }
    for row, (markers, texts) in guild_rows.items():
        starts = marker_starts(clean13[row], markers)
        runtime.append(
            packed_screen_record(
                current13[row],
                starts,
                texts,
                f"DK4_MES_B13_R{row:04d}",
                "Source-derived sailor, Guild purchase, sale, or bargaining entry.",
                width=31,
                preserve_placeholders=False,
            )
        )

    write_json(
        ROOT / "translations/common_runtime_layout_v4.json",
        {
            "format": "dk4-ilnk-translation-batch-v1",
            "file_path": "/COMMON/MESFILE.DK4",
            "source_file_sha256": COMMON_HASH,
            "target_locale": "en-US",
            "scope": "Crew assignment/join and complete Guild item transaction layout repair",
            "ascii_guard_policy": "two-byte-entry-and-line-v1",
            "fixed_allocation_policy": "screen-entry-layout-v1",
            "records": runtime,
        },
    )


def main() -> None:
    rom = NdsImage.open(BASE)
    arm9 = rom.read_file("/__arm9__.bin")
    common = rom.read_file("/COMMON/MESFILE.DK4")
    clean_common = NdsImage.open(CLEAN).read_file("/COMMON/MESFILE.DK4")
    if sha256(arm9).hexdigest() != ARM9_HASH or sha256(common).hexdigest() != COMMON_HASH:
        raise ValueError("canonical accepted baseline no longer matches this materializer")
    if any(arm9[POOL_START:POOL_END]):
        raise ValueError("reserved post-item relocation pool is no longer empty")
    materialize_entity_names(arm9)
    materialize_arm9_ui(arm9)
    materialize_common(common, clean_common)
    print("materialized entity/name, shipyard/Guild UI, and mystery-item polish batches")


if __name__ == "__main__":
    main()
