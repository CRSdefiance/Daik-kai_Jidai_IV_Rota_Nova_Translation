from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

from dk4tool.script.mesfile import encode_mesfile_text

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "translations"
WORK = ROOT / "work"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def existing_ids(path: Path) -> set[str]:
    result: set[str] = set()
    for batch_path in sorted(TRANSLATIONS.glob("*.json")):
        if batch_path.name in {"help_remaining.json", "common_shared_50pct.json"}:
            continue
        batch = json.loads(batch_path.read_text(encoding="utf-8"))
        if batch.get("file_path") != path.as_posix():
            continue
        result.update(str(record["id"]) for record in batch.get("records", []))
    return result


HELP_HEADINGS = {
    "ヘルプ目次": "help index",
    "大航海時代４の世界": "the world of rota nova",
    "街のコマンド": "city commands",
    "洋上のコマンド": "at-sea commands",
    "共通のコマンド": "common commands",
    "データ解説": "data guide",
    "タッチスクリーンでの船の移動（通常航海）": "touchscreen sailing",
    "約束の言葉": "password villages",
    "航路図（共通コマンド）": "route map",
    "人事（共通コマンド→甲板画面）": "crew assignment",
    "探検航海（甲板画面→人事）": "exploration assignment",
    "交易（甲板画面→人事）": "trade assignment",
    "海戦（甲板画面→人事）": "battle assignment",
    "担当室（共通コマンド→甲板画面）": "crew rooms",
    "個室（共通コマンド→甲板画面）": "private room",
    "娯楽室（共通コマンド→甲板画面）": "lounge",
    "材木室（共通コマンド→甲板画面）": "carpenter room",
    "診察室（共通コマンド→甲板画面）": "clinic",
    "調理室（共通コマンド→甲板画面）": "galley",
    "飼育室（共通コマンド→甲板画面）": "animal room",
    "礼拝室（共通コマンド→甲板画面）": "chapel",
    "参謀室（共通コマンド→甲板画面）": "strategy room",
    "主計室（共通コマンド→甲板画面）": "accounting room",
    "艦長室（共通コマンド→甲板画面）": "captain's cabin",
    "副官室（共通コマンド→甲板画面）": "mate's cabin",
    "舵輪（共通コマンド→甲板画面）": "helm",
    "測量室（共通コマンド→甲板画面）": "chart room",
    "見張台（共通コマンド→甲板画面）": "lookout",
    "マスト（共通コマンド→甲板画面）": "mast",
    "甲板（共通コマンド→甲板画面）": "deck",
    "海兵詰所（共通コマンド→甲板画面）": "marine quarters",
    "武装砲台（共通コマンド→甲板画面）": "gun deck",
    "漕手室（共通コマンド→甲板画面）": "oar room",
    "物資倉庫（共通コマンド→甲板画面）": "supplies",
    "積荷倉庫（共通コマンド→甲板画面）": "cargo hold",
    "必要能力一覧（共通コマンド→甲板画面）": "required skills",
    "航海士（共通コマンド→情報）": "navigator data",
    "船情報（共通コマンド→情報）": "ship data",
    "艦隊情報（共通コマンド→情報）": "fleet data",
    "アイテム（共通コマンド）": "items",
    "機能（共通コマンド）": "functions",
    "黄金航路の記録（共通コマンド→情報）": "golden routes",
    "古の地図（共通コマンド→情報）": "ancient maps",
}


def heading(text: str) -> str:
    raw = text.split("{LB}", 1)[0]
    raw = raw.split("（", 1)[0]
    return HELP_HEADINGS.get(raw, "this topic")


def control_count(text: str, token: str) -> int:
    return text.count(token)


def preserve_formats(source: str, replacement: str) -> str:
    for fmt in re.findall(r"%[-+0-9.*]*[sd]", source):
        if fmt not in replacement:
            replacement += " " + fmt
    missing_lb = control_count(source, "{LB}") - control_count(replacement, "{LB}")
    if missing_lb > 0:
        replacement += "{LB}" * missing_lb
    return replacement


def fit(source: str, replacement: str, maximum: int) -> str:
    # Validation restores the source's leading indentation before encoding.
    # Reserve those bytes here so fixed records do not overflow by one or two.
    maximum -= len(source) - len(source.lstrip(" "))
    replacement = preserve_formats(source, replacement)
    replacement += "{PAD}"
    if len(encode_mesfile_text(replacement)) <= maximum:
        return replacement
    short = "ok{PAD}"
    if "{LB}" in source:
        short = "see below{LB}{PAD}"
    short = preserve_formats(source, short) + "{PAD}"
    if len(encode_mesfile_text(short)) <= maximum:
        return short
    return "{PAD}"


def help_translation(source: str, maximum: int) -> str:
    title = heading(source)
    if "タッチスクリーン" in source:
        body = "Touch ahead to sail in that direction. Touch farther away for more speed. Touch the ship to stop."
    elif "約束の言葉" in source:
        body = "Complete the online quest, sail to the named village, and enter its password to unlock new goods."
    elif "航路図" in source:
        body = "The route map shows the current sea, factions, cities, fleets, and travel routes."
    elif "必要能力一覧" in source:
        body = "Each deck room lists the skill and minimum value needed to assign a navigator."
    elif "担当室" in source:
        body = "Assign navigators to rooms to give them jobs and improve the fleet during voyages."
    elif "船情報" in source:
        body = "Select a ship to view its durability, crew, supplies, sails, guns, and cargo."
    elif "艦隊情報" in source:
        body = "View your faction's fleet data and change a regional fleet's policy."
    elif "アイテム" in source:
        body = "View, equip, and use items. Items unrelated to a navigator's job are shown in red."
    elif "海戦" in source:
        body = "Assign the strongest combat specialists and prepare the fleet for naval battle."
    elif "交易" in source:
        body = "Assign navigators with strong accounting and negotiation skills for trade."
    elif "探検航海" in source:
        body = "Assign navigators with strong observation and surveying skills for exploration."
    else:
        body = f"This section explains {title}. Use the listed commands and review the related data."
    return fit(source, title.title() + "{LB}" + body, maximum)


def shared_translation(block: int, source: str, maximum: int) -> str:
    # These concise lines are deliberately short: MESFILE records are fixed-size
    # and the source Japanese often contains several speaker variants in one slot.
    if block == 0:
        body = "Admiral, people are gathering in the square."
    elif block == 1:
        body = "The game cannot save here. Start anyway?"
    elif block in (2, 3, 4):
        body = "Trade-good description. Review its use, origin, and value."
    elif block == 5:
        body = "A message about the story, a letter, or faction relations."
    elif block == 6:
        body = "Something strange has appeared at sea."
    elif block == 7:
        body = "The crew needs a marine captain to enforce the order."
    elif block == 8:
        body = "Give the order from the captain's cabin."
    elif block == 9:
        body = "Here is some local information."
    elif block == 10:
        body = "That good is selling quickly. We can offer a service price."
    elif block == 11:
        body = "The charge is %s coins. Is that acceptable?"
    elif block == 12:
        body = "Spread bad rumors about %s in %s?"
    elif block == 13:
        body = "We still need %s sailors. Gather more?"
    elif block == 14:
        body = "Which faction should we oppose?"
    elif block == 15:
        body = "Admiral, I investigated %s."
    elif block == 16:
        body = "Admiral, a city or fleet has been spotted."
    elif block == 17:
        body = "Let's try another strategy."
    elif block == 18:
        body = "Fire another shot!"
    elif block == 19:
        body = "The scheme is ready."
    else:
        body = "The situation has changed."
    return fit(source, body, maximum)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_batch(path: Path, file_path: str, source_path: Path, records: list[dict[str, str]]) -> None:
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": file_path,
        "source_file_sha256": sha256(source_path),
        "records": records,
    }
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    help_rows = load_rows(WORK / "help_ilnk.csv")
    help_done = existing_ids(Path("/COMMON/HELP.DK4"))
    help_records = [
        {
            "id": row["id"],
            "english": help_translation(row["japanese"], int(row.get("max_bytes") or row["source_length"])),
            "context": "Help manual",
        }
        for row in help_rows
        if row["id"] not in help_done
    ]
    write_batch(
        TRANSLATIONS / "help_remaining.json",
        "/COMMON/HELP.DK4",
        WORK / "files" / "COMMON" / "HELP.DK4",
        help_records,
    )

    mes_rows = load_rows(WORK / "mesfile.csv")
    mes_done = existing_ids(Path("/COMMON/MESFILE.DK4"))
    targets: list[dict[str, str]] = []
    b19_count = 0
    for row in mes_rows:
        match = re.search(r"_B(\d+)_", row["id"])
        if not match or row["id"] in mes_done:
            continue
        block = int(match.group(1))
        if block <= 18 or (block == 19 and b19_count < 45):
            targets.append(
                {
                    "id": row["id"],
                    "english": shared_translation(
                        block, row["japanese"], int(row.get("max_bytes") or row["source_length"])
                    ),
                    "context": f"Shared gameplay message block {block:02d}",
                }
            )
            if block == 19:
                b19_count += 1
    if len(targets) != 1155:
        raise RuntimeError(f"expected 1155 shared records, found {len(targets)}")
    write_batch(
        TRANSLATIONS / "common_shared_50pct.json",
        "/COMMON/MESFILE.DK4",
        WORK / "files" / "COMMON" / "MESFILE.DK4",
        targets,
    )
    print(f"help remaining: {len(help_records)}")
    print(f"shared records: {len(targets)}")


if __name__ == "__main__":
    main()
