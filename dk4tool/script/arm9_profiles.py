from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Arm9ProfileEntry:
    row_id: str
    offset: int
    japanese: str
    suggested_english: str
    context: str
    notes: str = ""

    @property
    def source_bytes(self) -> bytes:
        return self.japanese.encode("cp932")


STARTUP_ENTRIES = (
    Arm9ProfileEntry("DK4_TITLE_OPTIONS", 1276268, "設定", "Opts", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_CONTINUE", 1276400, "つづきから", "Continue", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_EXTRAS", 1276412, "おまけ機能", "Extras", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_NEW_GAME", 1276424, "はじめから", "New Game", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_GALLERY", 1276436, "ギャラリー", "Gallery", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_RACE", 1276568, "大航海レース", "Grand Race", "Title menu"),
    Arm9ProfileEntry("DK4_BUTTON_BACK", 1160460, "戻る", "Back", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_BUTTON_DONE", 1160476, "決定", "Done", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_BUTTON_EDIT", 1160516, "変更", "Edit", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_SELECT_BORN", 1376968, "生まれ", "Born", "Character selection"),
    Arm9ProfileEntry(
        "DK4_SELECT_HEADING",
        1376976,
        "キャラクター選択",
        "Choose Captain",
        "Character selection",
    ),
)


CHARACTER_ENTRIES = (
    Arm9ProfileEntry("DK4_LIL_NAME", 1423728, "リル", "Lil", "Lil character record"),
    Arm9ProfileEntry("DK4_LIL_LAST", 1428632, "アーゴット", "Argot", "Lil character record"),
    Arm9ProfileEntry(
        "DK4_LIL_ORG", 1434148, "アーゴット商会", "Argot Co.", "Lil character record"
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_1",
        1375612,
        "商魂たくましいオランダの少女",
        "A bold Dutch merchant girl  ",
        "Lil biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_2",
        1375641,
        "幼なじみの相棒カミルとともに、",
        "With childhood friend Camille,",
        "Lil biography",
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_3",
        1375672,
        "一旗揚げようと世界の海に飛び出す",
        "Sails the world to make her mark",
        "Lil biography",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_NAME", 1428032, "ラファエル", "Raphael", "Raphael character record"
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_LAST", 1428572, "カストール", "Castor", "Raphael character record"
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_ORG",
        1434132,
        "カストール商会",
        "Castor Co.",
        "Raphael character record",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_1",
        1375708,
        "船乗りに漠然と憧れるポルトガルの少年",
        "Portuguese youth dreaming of the sea",
        "Raphael biography",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_2",
        1375745,
        "友人にそそのかされて海に出ることになる",
        "A friend urges him to sail the world. ",
        "Raphael biography",
        "Trailing space preserves the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_3",
        1375784,
        "初めてプレイする方におすすめ",
        "Recommended for new players.",
        "Raphael biography",
    ),
    Arm9ProfileEntry("DK4_HODRAM_NAME", 1425716, "ホドラム", "Hodram", "Hodram character record"),
    Arm9ProfileEntry(
        "DK4_HODRAM_LAST", 1433556, "ベルグストロン", "Bergstrom", "Hodram character record"
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_ORG",
        1435492,
        "ベルグストロン軍",
        "Bergstrom Fleet",
        "Hodram character record",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_1",
        1375816,
        "再独立を果たしたスウェーデンの提督",
        "An admiral of newly free Sweden   ",
        "Hodram biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_2",
        1375851,
        "海軍とは名ばかりの私掠艦隊を率いる",
        "Commands a navy of privateers     ",
        "Hodram biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_3",
        1375886,
        "自国の艦隊を世界最強にすべく活動する",
        "Aims to make his fleet the strongest",
        "Hodram biography",
    ),
    Arm9ProfileEntry("DK4_MARIA_NAME", 1425456, "マリア", "Maria", "Maria character record"),
    Arm9ProfileEntry("DK4_MARIA_LAST", 1424056, "リー", "Lee", "Maria character record"),
    Arm9ProfileEntry("DK4_MARIA_ORG", 1424736, "リー家", "LiFam", "Maria character record"),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_1",
        1375924,
        "倭寇に苦しめられる人々を守るために",
        "Guards people from pirate raids   ",
        "Maria biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_2",
        1375959,
        "国法である鎖国政策をあえて無視し、",
        "Defying the national isolation law",
        "Maria biography",
    ),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_3",
        1375994,
        "私設艦隊を率いて戦う明（みん）の女提督",
        "A Ming admiral leading her own fleet  ",
        "Maria biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
)


PROFILES = {
    "startup": STARTUP_ENTRIES,
    "characters": CHARACTER_ENTRIES,
    "all": STARTUP_ENTRIES + CHARACTER_ENTRIES,
}


def profile_names() -> tuple[str, ...]:
    return tuple(PROFILES)


def export_profile_rows(
    arm9: bytes, profile: str, include_drafts: bool = False
) -> list[dict[str, object]]:
    entries = PROFILES[profile]
    rows: list[dict[str, object]] = []
    for entry in entries:
        source = entry.source_bytes
        actual = arm9[entry.offset : entry.offset + len(source)]
        if actual != source:
            raise ValueError(
                f"{entry.row_id}: ARM9 source mismatch at 0x{entry.offset:X}; "
                f"expected {source.hex().upper()}, found {actual.hex().upper()}"
            )
        rows.append(
            {
                "id": entry.row_id,
                "file_path": "/__arm9__.bin",
                "container_path": "",
                "encoding": "shift_jis",
                "source_offset": entry.offset,
                "source_length": len(source),
                "source_hex": source.hex().upper(),
                "japanese": entry.japanese,
                "english": entry.suggested_english if include_drafts else "",
                "status": "draft" if include_drafts else "untranslated",
                "context": entry.context,
                "speaker": "",
                "notes": entry.notes,
                "max_bytes": len(source),
                "allow_expand": "false",
                "pointer_group": "",
                "control_profile": "default",
                "wrap_width": 38,
            }
        )
    return rows

