from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN_COMMON = Path("work/files/COMMON/MESFILE.DK4")
OUTPUT = Path("translations/common_at_sea_fixed_v1.json")
FILE_PATH = "/COMMON/MESFILE.DK4"


# Original independently addressed starts, recovered from the clean Japanese
# record layout. Text is deliberately concise, natural, and limited to the
# game's 31-byte dialogue line width.
ENTRIES: dict[int, tuple[list[int], list[str]]] = {
    0: ([0, 64], [
        "Admiral!\nWe need a Marine Captain\nto control the sailors!",
        "Admiral, without a Marine\nCaptain, we cannot control\nthe crew.",
    ]),
    1: ([0], ["Admiral!\nThe sailors won't listen\nwithout a Marine Captain!"]),
    2: ([0, 89], [
        " Sorry, everyone.\nTo apologize, today's a feast!\nLet's enjoy it together!",
        "Hang on a little longer.\nTo make it up to everyone,\nI'll serve a special feast!",
    ]),
    3: ([0, 74], [
        "  Hang on a little longer.\nLet's share a meal today\nand cheer up!",
        "Please be patient a bit longer.\nI'll make it up to everyone\nwith a special feast!",
    ]),
    6: ([0, 30, 50], ["  Hey, stop! Ouch!", "What are you doing?!", "Eek! Stop! Ouch!"]),
    10: ([0, 53], [
        " Stop!\nYou struck the Admiral.\nIsn't that enough?!",
        "Enough! Attacking the Admiral\nwas going too far!",
    ]),
    11: ([0], ["  Enough!\nYou hit the Admiral.\nStill not satisfied?!"]),
    17: ([0, 33], [" Leave it to me, Admiral!", "Right. Leave it to me."]),
    19: ([0, 34, 66], [
        "  Understood. Leave it to me!",
        "That's our Admiral. You get it!",
        "Admiral! A leak!\nThe flagship's hull is damaged.",
    ]),
    22: ([0], ["  A leak!\nThe hull must be damaged."]),
    24: ([0], ["Admiral! We're leaking!\nWater's coming through!"]),
    31: ([0, 22, 42], ["  Fire extinguished!", "Fire extinguished!", "It's okay. Fire's out!"]),
    52: ([0, 44, 64], ["Dizzy...\nI'm starving...\nI can't go on...", "%s\nhas run out.", "%s\nis canceled."]),
    74: ([0, 17, 33], [" No surveyor.", "No surveyor.", "No surveyor is assigned,\nso that city has no route."]),
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fit_entries(source: bytes, starts: list[int], texts: list[str], record_id: str) -> bytes:
    if starts != sorted(set(starts)) or not starts or starts[0] != 0:
        raise ValueError(f"{record_id}: invalid entry starts")
    if len(starts) != len(texts):
        raise ValueError(f"{record_id}: entry count mismatch")
    output = bytearray()
    for position, (start, text) in enumerate(zip(starts, texts, strict=True)):
        end = starts[position + 1] if position + 1 < len(starts) else len(source)
        segment = source[start:end]
        encoded = text.encode("ascii")
        if len(encoded) > len(segment):
            raise ValueError(
                f"{record_id}[{position}]: {len(encoded)} bytes exceed {len(segment)}"
            )
        if any(len(line) > 31 for line in encoded.split(b"\n")):
            raise ValueError(f"{record_id}[{position}]: line exceeds 31 bytes")
        if re.findall(rb"%[-+0-9.*]*[sd]", encoded) != re.findall(
            rb"%[-+0-9.*]*[sd]", segment
        ):
            raise ValueError(f"{record_id}[{position}]: printf macros changed")
        output.extend(encoded.ljust(len(segment), b" "))
    if len(output) != len(source):
        raise ValueError(f"{record_id}: allocation length changed")
    return bytes(output)


def materialize(base_rom: Path, clean_common: Path) -> dict[str, object]:
    accepted = NdsImage.open(base_rom).read_file(FILE_PATH)
    clean = clean_common.read_bytes()
    blocks = [block.split(b"\0") for block in IlnkContainer.parse(clean).blocks]
    records: list[dict[str, object]] = []
    for index, (starts, texts) in sorted(ENTRIES.items()):
        record_id = f"DK4_MES_B07_R{index:04d}"
        replacement = _fit_entries(blocks[7][index], starts, texts, record_id)
        records.append(
            {
                "id": record_id,
                "english": " / ".join(text.replace("\n", " ") for text in texts),
                "replacement_hex": replacement.hex().upper(),
                "status": "translated",
                "context": "At-sea sailor message, translated from the clean Japanese source.",
                "notes": "Every original fixed interior entry point and source indentation is preserved.",
                "structure": "single-entry" if len(starts) == 1 else "packed-multiple-entry",
                "entry_offsets": starts,
            }
        )
    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "common-fixed-dialogue-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": _sha256(accepted),
        "target_locale": "en-US",
        "scope": "Complete source-based replacement of all surviving generic fixed-allocation block-7 at-sea messages",
        "ascii_guard_exemption": "This at-sea renderer preserves the first ASCII glyph; source indentation and proven packed entry offsets are retained exactly.",
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE_ROM)
    parser.add_argument("--clean-common", type=Path, default=CLEAN_COMMON)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    batch = materialize(args.base, args.clean_common)
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(batch['records'])} at-sea records to {args.out}")


if __name__ == "__main__":
    main()
