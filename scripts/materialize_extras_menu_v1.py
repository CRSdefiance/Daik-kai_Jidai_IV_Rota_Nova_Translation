from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.rom.nds import NdsImage

ROOT = Path(__file__).resolve().parents[1]
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds"
TRANSLATIONS = ROOT / "translations"
ARM9_SHA256 = "6a7eb231463336a44c4e89d8630adf00ede862bdab11cbe1f1e1fedc23e3f5af"

ARM9_RECORDS = (
    ("DK4_EXTRAS_NEXT_PAGE", 0x16D900, "次頁", "Next", "Extras page navigation"),
    ("DK4_EXTRAS_PREVIOUS_SHARED", 0x138954, "前頁", "Prev", "Shared page button"),
    ("DK4_EXTRAS_NEXT_SHARED", 0x138964, "次頁", "Next", "Shared page button"),
    ("DK4_EXTRAS_NEXT_ONLINE_A", 0x16E4A0, "次頁", "Next", "Online page button"),
    ("DK4_EXTRAS_PREVIOUS_ONLINE_A", 0x16E4A8, "前頁", "Prev", "Online page button"),
    ("DK4_EXTRAS_PREVIOUS_ONLINE_B", 0x16E4B0, "前頁", "Prev", "Online page button"),
    ("DK4_EXTRAS_NEXT_ONLINE_B", 0x16E4B8, "次頁", "Next", "Online page button"),
    ("DK4_EXTRAS_CAREERS", 0x16D950, "職業紹介", "Careers", "Online feature menu"),
    ("DK4_EXTRAS_OVERVIEW", 0x16D95C, "ゲーム概要", "Overview", "Online feature menu"),
    (
        "DK4_EXTRAS_GETTING_STARTED",
        0x16D990,
        "冒険のはじまり",
        "First Steps",
        "Online feature menu",
    ),
    (
        "DK4_EXTRAS_ONLINE_VERSION",
        0x16D9C0,
        "Online版のご紹介",
        "Online Version",
        "Extras root menu",
    ),
    (
        "DK4_EXTRAS_CREATE_STORY",
        0x16D9D4,
        "創り出すストーリー",
        "Create a Story",
        "Online feature menu",
    ),
    (
        "DK4_EXTRAS_ABOUT",
        0x16D9E8,
        "おまけ機能について",
        "About Extras",
        "Extras root menu",
    ),
    (
        "DK4_EXTRAS_PLAY_YOUR_WAY",
        0x16DA10,
        "自由な遊び方が可能！",
        "Play Your Way!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_CHARACTER_DRAMA",
        0x16DA70,
        "様々な人々との人間ドラマ",
        "People shape your story.",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_ORDERS",
        0x16DA8C,
        "勅命を受け、さらなる冒険へ",
        "Orders lead to adventure!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_VAST_WORLD",
        0x16DAA8,
        "胸がおどる壮大な冒険空間！",
        "A vast world of adventure!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_UNCHARTED_WORLD",
        0x16DAC4,
        "目指すのは、地図に無い世界――",
        "Chart the unknown world!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_MAKE_HISTORY",
        0x16DAE4,
        "海の彼方へ漕ぎ出し、名を刻め！",
        "Sail beyond. Make history!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_CHANGING_WORLD",
        0x16DB04,
        "変化が生み出すかつてない刺激！",
        "Change brings fresh thrills!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_OWN_SHIP",
        0x16DB24,
        "自分だけの船で大海原を駆けろ！",
        "Sail far in your own ship!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_LIVE_AS_SAILOR",
        0x16DB44,
        "世界を舞台に、船乗りとして生きる",
        "Live as a sailor worldwide.",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_TRADE_FORTUNE",
        0x16DB68,
        "多彩な交易品を売買してひと儲け！",
        "Trade goods and make a fortune!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_NAVAL_BATTLE",
        0x16DB8C,
        "洋上で繰り広げられる、熱き戦い！",
        "Fierce battles rage at sea!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_NATION_STORY",
        0x16DBB0,
        "所属国で大きく変わるストーリー！",
        "Your nation shapes your story!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_NEW_ALLIES",
        0x16DBD4,
        "出会った仲間とともに冒険に出発！",
        "Set sail with newfound allies!",
        "Online overview caption",
    ),
    (
        "DK4_EXTRAS_OFFICIAL_SITE",
        0x16DC48,
        "さあ、『大航海時代 Online』\n公式サイトにアクセスして\nさらなる航海の旅へ！\n",
        "Visit the Online website\nand begin a new adventure!\n",
        "Online promotional closing page",
    ),
    (
        "DK4_EXTRAS_SERVICE_NOTICE",
        0x16DC94,
        "都合により、ネットワーク\nコンテンツのサービスを変更\n終了する場合があります。\nご了承ください。\n",
        "Online services may change\nor end without notice.\nThank you for understanding.\n",
        "Online service disclaimer",
    ),
    (
        "DK4_EXTRAS_TIE_IN_STEP_2",
        0x16DCF4,
        "ＳＴＥＰ２\n本製品で、その「村」を探し当て\n「約束の言葉」を使うと、\n「村」との交易が可能になり\n高価な交易品が登場します。\n",
        "STEP 2\nFind the village in this game\nand enter the secret phrase.\nTrade there to purchase\nvaluable new goods.\n",
        "Online tie-in instructions",
    ),
    (
        "DK4_EXTRAS_TIE_IN_STEP_1",
        0x16DD70,
        "ＳＴＥＰ１\nまずは『大航海時代 Online』を\nプレイして、特定のキャラクター\nから「村の名前」と\n「約束の言葉」を聞き出します。\n",
        "STEP 1\nPlay Uncharted Waters Online.\nA certain character will tell\nyou a village name and its\nsecret phrase.\n",
        "Online tie-in instructions",
    ),
    (
        "DK4_EXTRAS_TIE_IN_VILLAGES",
        0x16DDEC,
        "「村」は全部で２４カ所。\n登場する交易品も「村」ごとに\n異なります。\nどんな交易品が登場するか、\nぜひ、あなたの目で確かめて\nください。\n",
        "There are 24 villages in all,\neach with different trade goods.\nVisit them to discover every\nspecial item for yourself.\n",
        "Online tie-in village explanation",
    ),
    (
        "DK4_EXTRAS_TIE_IN_INTRO",
        0x16DE74,
        "パソコン版ゲームソフト\n『大航海時代 Online』との\nタイアップについて紹介します。\n『大航海時代 Online』を\nあわせてプレイすることで、\n本製品の楽しさが広がります。\n",
        "Learn about this game's\ntie-in with the PC title\nUncharted Waters Online.\nPlaying both games opens\nnew ways to enjoy this game.\n",
        "Extras Online-version introduction",
    ),
)

ARM9_EXACT_RECORDS = (
    (
        "DK4_TITLE_OPTIONS_FULL",
        0x13796C,
        "4F70747300000000",
        "Options",
        "Title menu; exact eight-byte slot ending immediately before Map",
        "ascii",
    ),
    (
        "DK4_OPTIONS_STATE_ON",
        0x1385CC,
        "5669657700000000",
        "On",
        "Options prompt current-state label",
        "ascii",
    ),
    (
        "DK4_OPTIONS_STATE_OFF",
        0x1385DC,
        "4869646500000000",
        "Off",
        "Options prompt proposed-state label",
        "ascii",
    ),
    (
        "DK4_OPTIONS_SAIL_HELP_PROMPT_COMPLETE",
        0x13880C,
        "8CBB8DDD0A827282818289828C814082678285828C829081460A25730A82728285829481402573814800000000000000000000000000",
        "Ｓａｉｌ　Ｈｅｌｐ：\n%s\nＣｈａｎｇｅ　ｔｏ　%s？",
        "Complete Sailing Help prompt, including the previously untouched heading",
        "cp932",
    ),
    (
        "DK4_OPTIONS_REPORT_PROMPT_NATURAL",
        0x138844,
        "827182858290828F82928294829381460A25730A8272828582948140257381480000000000000000000000000000000000000000",
        "Ｒｅｐｏｒｔｓ：\n%s\nＣｈａｎｇｅ　ｔｏ　%s？",
        "Options report prompt",
        "cp932",
    ),
)

ONLINE_HASHES = {
    0: "0ec6a8ef3d5c4c64ce9724424155960b9fbf1a12e8039f66af4819b5b5559af4",
    50: "2d493dca0a89487d98d5c876bc484ae8accf1cb9b29d80a77564e968f8086e68",
    51: "14a53f3b96db1dabb67a671ac99587be0498a239ac4cd48ebd6c9a7600c5a8ff",
    52: "1d6719f8048ea85074e0a2f4cf28ab406a9244975ff262b24063c631edacd749",
    53: "10496bb34fb34b0589ff59bacc9cbdf6e792f39c631d372bd434aecc9e5448cf",
    54: "f70e2d1fc84e5111b33a9c708eb223251a9d1cf74c3cf3234c55d2ee2ab8e4e1",
    55: "a8eee67635e515dc3485f53ad79b6471efe695002868e50798d2be9e7a630a8d",
    56: "982afc7980427a1a58699fc1166a565a4a0c99b53ad46e8b9bdda145a717a447",
    57: "483ee8e180e357747d9d3b75fb1fe70f885941d6fbe412aabaa887730f66563d",
    58: "3531995c9b0f72d90e297f0d41c6831a23550d44ba36b59c1b6262b7355652fa",
    59: "bb8211b96f523f3df7838c3105befb93384f3673e68fbde7aff313a80573d9c0",
    60: "fd67b7ddc3e0a3678465905d11a964a21e455704107ae6d8a9474a2f8c906cf9",
    61: "321de0e90ec236fd7ecb223051812c01475f2f99c290daa53093bdc1edf76cdf",
    62: "630d37bfd1714ca9a0edbcd6dece139ba2aaf03ff5014bf9c521502e5ec66ace",
}

ONLINE_CARDS = {
    50: "Take command as captain.\nSet sail across the boundless\nseas of the online world!",
    51: "Work with other players,\nor overcome trials alone.\nEvery encounter and hardship\ncreates a new story!",
    52: "Seek ports and trade goods,\nor hunt pirates relentlessly.\nChoose your own path--even\nbecome a wanted outlaw!",
    53: "Chart new sailing regions\nand seek greater adventures.\nTake to seas filled with\nthrills and spectacle!",
    54: "Choose from about 50 careers.\nGain experience, switch jobs,\nand develop as you wish!",
    55: "ADVENTURE CAREERS\nThe world hides many mysteries.\nSeek ruins and treasures,\nand pursue great discoveries!",
    56: "TRADE CAREERS\nTrade hundreds of goods and\ninfluence market prices.\nFind rarities and open a bazaar!",
    57: "COMBAT CAREERS\nMaster cannon and boarding combat\nto escort merchants and explorers.\nForm a pirate fleet with friends!",
    58: "Meet many characters\nthroughout your travels.\nYour nation determines which\nstory will unfold!",
    59: "Your actions shape world affairs!\nIn wars for national prestige,\nyour vote may decide which\nport becomes the next target.",
    60: "Invite players you meet\nto form a fleet. Combine skills\nto solve mysteries and\nbattle pirates together!",
    61: "Ships come in many sizes.\nCustomize their materials,\nweapons, sails, and emblems!",
    62: "Explore 3D landmarks and cities,\nfrom the pyramids to Pisa.\nAdventure stretches endlessly\nbefore you!",
}


def _dump(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


def encode_pair_phase_multiline(text: str) -> bytes:
    """Encode live Extras text with protected, pair-phase-safe line breaks."""

    markup = text.rstrip("\n").replace("\n", "{LB}")
    return tokens_to_bytes(
        parse_markup(markup),
        guard_linebreaks=True,
        pair_phase_safe_breaks=True,
    )


def main() -> None:
    image = NdsImage.open(BASE_ROM)
    arm9 = image.read_file("/__arm9__.bin")
    if hashlib.sha256(arm9).hexdigest() != ARM9_SHA256:
        raise SystemExit("canonical ARM9 hash does not match Extras source")

    records: list[dict[str, object]] = []
    for row_id, offset, japanese, english, context in ARM9_RECORDS:
        source = japanese.encode("cp932") + b"\0"
        actual = arm9[offset : offset + len(source)]
        if actual != source:
            raise SystemExit(f"{row_id}: source mismatch at {offset:#x}")
        encoded = encode_pair_phase_multiline(english)
        if len(encoded) >= len(source):
            raise SystemExit(
                f"{row_id}: English needs {len(encoded) + 1} bytes; slot has {len(source)}"
            )
        records.append(
            {
                "id": row_id,
                "offset": offset,
                "source_hex": source.hex().upper(),
                "english": encoded.decode("ascii"),
                "context": context,
                "notes": "Source-locked Extras localization; preserves the original terminator.",
            }
        )
    for row_id, offset, source_hex, english, context, encoding in ARM9_EXACT_RECORDS:
        source = bytes.fromhex(source_hex)
        actual = arm9[offset : offset + len(source)]
        if actual != source:
            raise SystemExit(f"{row_id}: source mismatch at {offset:#x}")
        encoded = english.encode(encoding)
        if len(encoded) >= len(source):
            raise SystemExit(
                f"{row_id}: English needs {len(encoded) + 1} bytes; slot has {len(source)}"
            )
        records.append(
            {
                "id": row_id,
                "offset": offset,
                "source_hex": source_hex,
                "english": english,
                "encoding": encoding,
                "context": context,
                "notes": "Source-locked in-place expansion; does not touch the following Map label.",
            }
        )
    _dump(
        TRANSLATIONS / "extras_menu_arm9_v1.json",
        {
            "format": "dk4-arm9-fixed-text-batch-v1",
            "file_path": "/__arm9__.bin",
            "source_file_sha256": ARM9_SHA256,
            "target_locale": "en-US",
            "scope": "Complete Extras and Online live-text localization",
            "records": records,
        },
    )

    for number, expected_hash in ONLINE_HASHES.items():
        path = f"/_pxl/online/Online{number:02d}.pxl"
        source = image.read_file(path)
        if hashlib.sha256(source).hexdigest() != expected_hash:
            raise SystemExit(f"{path}: source hash mismatch")
        if number == 0:
            graphic_records = [
                {
                    "id": "DK4_EXTRAS_ONLINE_LOGO",
                    "box": [58, 88, 184, 120],
                    "text": "UNCHARTED WATERS",
                    "erase": "dark-text",
                    "threshold": 170,
                    "color_index": 20,
                    "outline_index": 255,
                    "maximum_size": 18,
                },
                {
                    "id": "DK4_EXTRAS_ONLINE_PC_COPY",
                    "box": [62, 143, 190, 170],
                    "text": "PC VERSION\nOfficial website",
                    "erase": "dark-text",
                    "threshold": 170,
                    "color_index": 0,
                    "maximum_size": 12,
                },
            ]
        else:
            graphic_records = [
                {
                    "id": f"DK4_EXTRAS_ONLINE_CARD_{number:02d}",
                    "box": [0, 0, 256, 192],
                    "text": ONLINE_CARDS[number],
                    "erase": "solid",
                    "erase_color_index": 0,
                    "color_index": 15,
                    "outline_index": 1,
                    "maximum_size": 13,
                }
            ]
        _dump(
            TRANSLATIONS / f"extras_online{number:02d}_graphics_v1.json",
            {
                "format": "dk4-pxl-label-batch-v1",
                "file_path": path,
                "source_file_sha256": expected_hash,
                "target_locale": "en-US",
                "scope": "Extras Online promotional graphics localization",
                "records": graphic_records,
            },
        )


if __name__ == "__main__":
    main()
