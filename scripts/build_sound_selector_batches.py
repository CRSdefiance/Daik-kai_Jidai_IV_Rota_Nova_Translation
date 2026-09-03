from __future__ import annotations

import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE_ROM = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
ARM9_BATCH = Path("translations/sound_selector_arm9.json")
BGM_BATCH = Path("translations/sound_bgm_titles.json")
SOURCE_BASE_SHA256 = "c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf"
ARM9_PATH = "/__arm9__.bin"
MESFILE_PATH = "/COMMON/MESFILE.DK4"
BGM_BLOCK = 36
BGM_POINTER_TABLE_OFFSET = 0x143276
BGM_TAIL_OFFSET = 3532


@dataclass(frozen=True)
class BgmRecord:
    record_index: int
    titles: tuple[tuple[str, str], ...]
    preserve_after_offset: int | None = None


BGM_RECORDS = (
    BgmRecord(46, (("勇躍", "Heroic"), ("エンディング", "Ending"), ("追い風に乗って", "Tailwind"))),
    BgmRecord(47, (("旅立ちのテーマ", "Set Sail"),)),
    BgmRecord(48, (("南へ行こう", "Southbound"),)),
    BgmRecord(49, (("インディアの風", "India Wind"),)),
    BgmRecord(50, (("南海の島々", "South Seas"),)),
    BgmRecord(
        51,
        (
            ("東アジアの海", "E Asia Sea"),
            ("水平線の向こうへ", "Beyond Horizon"),
            ("北欧の街", "N Europe"),
            ("南欧の街", "S Europe"),
            ("イスラムの町", "Islam Town"),
            ("アフリカの町", "Africa Town"),
            ("インドの町", "India Town"),
        ),
    ),
    BgmRecord(
        52,
        (
            ("東南アジアの集落", "SE Asia"),
            ("中国の町", "China Town"),
            ("日本の町", "Japan Town"),
            ("新大陸の町", "New World"),
        ),
    ),
    BgmRecord(53, (("洋上戦闘のテーマ", "Naval Battle"), ("大海戦", "Sea War"))),
    BgmRecord(54, (("海へ続く道", "Sea Road"),)),
    BgmRecord(55, (("本当の宝物", "True Gem"),)),
    # The original slot has only two one-byte cells. Keep this visible as an
    # intentional abbreviation until this fixed title region can safely grow.
    BgmRecord(56, (("波", "Wv"),)),
    BgmRecord(57, (("情熱の炎", "Passion"), ("ラファエル", "Raphael"))),
    BgmRecord(
        58,
        (
            ("ホドラム", "Hodram"),
            ("リルとカミル", "Lil & Kamil"),
            ("探検！探検！", "Explore!"),
            ("暗雲", "Darkness"),
            ("麗しの乙女", "Fair Maiden"),
        ),
    ),
    BgmRecord(59, (("想い", "Feel"), ("陽気な仲間", "Pals"))),
    BgmRecord(60, (("悲しみ", "Sorrow"),)),
    BgmRecord(61, (("海賊王", "Pirate"),)),
    BgmRecord(62, (("征服者", "Victor"),)),
    BgmRecord(
        63,
        (("強敵登場", "Foe Appears"), ("大勝利！", "Victory!"), ("オープニング", "Opening")),
        preserve_after_offset=BGM_TAIL_OFFSET,
    ),
)


SFX_TITLES_4 = (
    ("帆", "Rig"),
    ("嵐", "Wnd"),
    ("雨", "Wet"),
    ("雷", "Zap"),
)


SFX_TITLES_8 = (
    ("成功", "Success"),
    ("剣戟", "Clash"),
    ("再生", "Replay"),
    ("命中", "Hit"),
    ("舵輪", "Helm"),
    ("竜巻", "Tornado"),
    ("沈没", "Sinking"),
    ("決定", "Confirm"),
    ("喝采", "Cheers"),
    ("酒場", "Tavern"),
    ("金貨", "Coins"),
    ("歩行", "Steps"),
    ("着水", "Splash"),
    ("遺跡", "Ruins"),
    ("吹雪", "Snow"),
    ("銃声", "Gunshot"),
    ("発見", "Found"),
    ("雑踏", "Crowd"),
    ("セラ", "Sera"),
    ("仲間", "Ally"),
    ("喚声", "Shout"),
    ("失敗", "Failure"),
    ("追突", "Ram"),
    ("衝撃", "Impact"),
    ("敬礼", "Salute"),
    ("喜び", "Joy"),
    ("砲撃", "Cannon"),
    ("大衝撃", "Big Hit"),
    ("人襲撃", "Ambush"),
    ("獣襲撃", "Beast"),
    ("かもめ", "Gull"),
    ("来る波", "Wave In"),
    ("喝采大", "Ovation"),
    ("敵登場", "Enemy"),
    ("ノック", "Knock"),
    ("イルカ", "Dolphin"),
    ("引く波", "Ebb"),
    ("跳ねる", "Leap"),
    ("扉開く", "Door"),
    ("造船所", "Yard"),
    ("殴る音", "Punch"),
    ("駆け足", "Run"),
    ("倒れる", "Fall"),
    ("必殺技", "Finish"),
)

SFX_TITLES_12 = (
    ("覇者の証", "Conq Proof"),
    ("コウモリ", "Bats"),
    ("金貨の山", "Coin Hoard"),
    ("崩れる音", "Collapse"),
    ("カーソル", "Cursor"),
    ("戦闘開始", "Battle"),
    ("斬り裂き", "Slash"),
    ("敵の滅亡", "Enemy Down"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record_starts(records: list[bytes]) -> list[int]:
    starts: list[int] = []
    cursor = 0
    for record in records:
        starts.append(cursor)
        cursor += len(record) + 1
    return starts


def repack_bgm_records(
    records: list[bytes], starts: list[int]
) -> tuple[list[dict[str, object]], list[int], list[int]]:
    batch_records: list[dict[str, object]] = []
    old_pointers: list[int] = []
    new_pointers: list[int] = []
    for spec in BGM_RECORDS:
        original = records[spec.record_index]
        start = starts[spec.record_index]
        encoded_japanese = [japanese.encode("cp932") for japanese, _ in spec.titles]
        cursor = 0
        positions: list[int] = []
        for title in encoded_japanese:
            position = original.find(title, cursor)
            if position < 0:
                raise ValueError(f"BGM record {spec.record_index}: title source bytes not found")
            positions.append(position)
            cursor = position + len(title)

        source_end = positions[-1] + len(encoded_japanese[-1])
        capacity = source_end - positions[0]
        packed_titles = b"".join(english.encode("ascii") for _, english in spec.titles)
        if len(packed_titles) > capacity:
            raise ValueError(
                f"BGM record {spec.record_index}: English titles need {len(packed_titles)} bytes; "
                f"only {capacity} are available"
            )

        translated = bytearray(original)
        translated[positions[0] : source_end] = packed_titles.ljust(capacity, b" ")
        cursor = positions[0]
        for position, (_, english) in zip(positions, spec.titles, strict=True):
            old_pointers.append(start + position)
            new_pointers.append(start + cursor)
            cursor += len(english)
        batch_records.append(
            {
                "id": f"DK4_MES_B36_R{spec.record_index:04d}",
                "english": " | ".join(english for _, english in spec.titles),
                "replacement_hex": bytes(translated).hex().upper(),
                "status": "translated",
                "context": "Packed BGM selector titles with explicit remapped interior offsets",
            }
        )
    return batch_records, old_pointers, new_pointers


def build_sfx_records(arm9: bytes) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    groups = (
        (0x16ED80, 4, SFX_TITLES_4),
        (0x16ED90, 8, SFX_TITLES_8),
        (0x16EEF0, 12, SFX_TITLES_12),
    )
    for base, slot_size, titles in groups:
        for index, (japanese, english) in enumerate(titles):
            offset = base + index * slot_size
            source = arm9[offset : offset + slot_size]
            if not source.startswith(japanese.encode("cp932") + b"\0"):
                raise ValueError(f"SFX title {japanese!r} source bytes do not match at {offset:#x}")
            if len(english.encode("ascii")) >= slot_size:
                raise ValueError(f"SFX title {english!r} does not leave a null terminator")
            records.append(
                {
                    "id": f"DK4_SFX_TITLE_{index:02d}_{offset:06X}",
                    "offset": offset,
                    "source_hex": source.hex().upper(),
                    "english": english,
                }
            )
    game_over_offset = 0x16EFB4
    game_over_source = arm9[game_over_offset : game_over_offset + 16]
    game_over_japanese = "ゲームオーバー".encode("cp932")
    if not game_over_source.startswith(game_over_japanese + b"\0"):
        raise ValueError("Game Over SFX source bytes do not match")
    records.append(
        {
            "id": "DK4_SFX_GAME_OVER_16EFB4",
            "offset": game_over_offset,
            "source_hex": game_over_source.hex().upper(),
            "english": "Game Over",
        }
    )
    return records


def main() -> None:
    base_data = BASE_ROM.read_bytes()
    if sha256(base_data) != SOURCE_BASE_SHA256:
        raise SystemExit("canonical base ROM hash mismatch")
    image = NdsImage.open(BASE_ROM)
    arm9 = image.read_file(ARM9_PATH)
    mesfile = image.read_file(MESFILE_PATH)
    container = IlnkContainer.parse(mesfile)
    records = container.blocks[BGM_BLOCK].split(b"\0")
    starts = record_starts(records)
    bgm_records, old_pointers, new_pointers = repack_bgm_records(records, starts)

    pointer_source = b"".join(struct.pack("<H", value) for value in old_pointers)
    actual_pointer_source = arm9[
        BGM_POINTER_TABLE_OFFSET : BGM_POINTER_TABLE_OFFSET + len(pointer_source)
    ]
    if actual_pointer_source != pointer_source:
        raise SystemExit("BGM pointer table source does not match the mapped title offsets")
    pointer_replacement = b"".join(struct.pack("<H", value) for value in new_pointers)

    arm9_records = [
        {
            "id": "DK4_BGM_INTERIOR_POINTERS",
            "offset": BGM_POINTER_TABLE_OFFSET,
            "source_hex": pointer_source.hex().upper(),
            "replacement_hex": pointer_replacement.hex().upper(),
            "english": "Mapped English BGM interior offsets",
        },
        *build_sfx_records(arm9),
    ]
    ARM9_BATCH.write_text(
        json.dumps(
            {
                "format": "dk4-arm9-fixed-text-batch-v1",
                "file_path": ARM9_PATH,
                "source_file_sha256": sha256(arm9),
                "records": arm9_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    BGM_BATCH.write_text(
        json.dumps(
            {
                "format": "dk4-ilnk-translation-batch-v1",
                "file_path": MESFILE_PATH,
                "source_file_sha256": sha256(mesfile),
                "records": bgm_records,
                "pointer_map": [
                    {
                        "english": english,
                        "old_offset": old_pointer,
                        "new_offset": new_pointer,
                    }
                    for old_pointer, new_pointer, english in zip(
                        old_pointers,
                        new_pointers,
                        (english for spec in BGM_RECORDS for _, english in spec.titles),
                        strict=True,
                    )
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {ARM9_BATCH} ({len(arm9_records) - 1} SFX titles + pointer map)")
    print(f"wrote {BGM_BATCH} ({sum(len(record.titles) for record in BGM_RECORDS)} BGM titles)")


if __name__ == "__main__":
    main()
