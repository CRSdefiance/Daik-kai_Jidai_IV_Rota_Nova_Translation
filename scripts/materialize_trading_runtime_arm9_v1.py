from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage

BASE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
ARM9_SHA256 = "ba0d426b975280a51d503f38b62baeda0a7cf21fc18f962dd0ddeb2f36450dd1"

REPAIRS = (
    ("DK4_CITY_TYPE_PORT_RUNTIME", 0x1565E0, 4, "Prt", "Lubeck port-city type value"),
    ("DK4_MARKET_SELL_RUNTIME", 0x15700C, 8, "Sell", "Trading-post Y-button command"),
    ("DK4_MARKET_PORT_FILTER_RUNTIME", 0x157080, 8, "Port", "Market-info port filter"),
    ("DK4_MARKET_CULTURE_FORMAT_RUNTIME", 0x159F7C, 12, "%s Region", "Cultural-region format"),
    ("DK4_MARKET_GERMAN_REGION_RUNTIME", 0x15BD50, 8, "German", "Lubeck cultural region"),
    ("DK4_MARKET_SPEYER_FACTION_RUNTIME", 0x15E778, 20, "Speyer Co.", "Lubeck market-share faction"),
    ("DK4_MARKET_MAP_FORCES_RUNTIME", 0x14C15C, 8, "Forces", "Market-report faction button"),
    ("DK4_MARKET_MAP_WORLD_RUNTIME", 0x14C17C, 8, "Map", "Market-report world button"),
    ("DK4_CATEGORY_SEASONING_REFINED", 0x15A0EC, 8, "Condim.", "Trading category label"),
    ("DK4_CITY_BAHAMAS_REFINED", 0x15BE08, 8, "Bahamas", "World settlement name"),
    ("DK4_GOOD_PLATINUM_TERMINATED", 0x15B860, 8, "Plat.", "Null-terminated commodity name"),
    ("DK4_GOOD_SOYBEAN_TERMINATED", 0x15B880, 8, "Soybean", "Null-terminated commodity name"),
    ("DK4_GOOD_SILK_TERMINATED", 0x15B930, 8, "Silk", "Null-terminated commodity name"),
    ("DK4_GOOD_IRON_TERMINATED", 0x15BD58, 8, "Iron", "Null-terminated commodity name"),
    ("DK4_MARIA_ORG_TERMINATED", 0x15BD60, 8, "Li Clan", "Terminate the adjacent Li family label"),
    ("DK4_GOOD_PALM_OIL_TERMINATED", 0x15BFB0, 8, "P. Oil", "Null-terminated commodity name"),
    ("DK4_GOOD_GOLD_DUST_REFINED", 0x15BBE0, 8, "G. Dust", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_WOOL_CLOTH_REFINED", 0x15BD10, 8, "WoolCl.", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_BLACK_WOOL_REFINED", 0x15BF30, 8, "B. Wool", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_COTTON_CLOTH_REFINED", 0x15BF90, 8, "CotClth", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_HEMP_CLOTH_REFINED", 0x15C058, 8, "HempCl.", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_SMOKED_SALMON_REFINED", 0x15C110, 8, "Smoked", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_TURMERIC_TERMINATED", 0x15BFC0, 8, "Turmer.", "Null-terminated commodity name"),
    ("DK4_GOOD_CINNAMON_TERMINATED", 0x15C35C, 8, "Cinnam.", "Null-terminated commodity name"),
    ("DK4_GOOD_TORTOISESHELL_TERMINATED", 0x15C6A4, 8, "T-Shell", "Null-terminated commodity name"),
    ("DK4_GOOD_SHARK_FIN_REFINED", 0x15C794, 8, "Shk Fin", "Distinct null-terminated commodity name"),
    ("DK4_GOOD_RED_PIGMENT_REFINED", 0x15CE18, 10, "Red Dye", "Distinct null-terminated commodity name"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize trading-screen ARM9 repairs.")
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds"),
    )
    parser.add_argument(
        "--out", type=Path, default=Path("translations/trading_runtime_arm9_v1.json")
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical ROM for trading ARM9 materialization")
    arm9 = NdsImage.open(args.rom).read_file("/__arm9__.bin")
    if sha256(arm9) != ARM9_SHA256:
        raise SystemExit("wrong canonical ARM9 component")

    records = []
    for row_id, offset, size, english, context in REPAIRS:
        encoded = english.encode("ascii")
        if len(encoded) >= size:
            raise SystemExit(f"{row_id}: replacement must leave a null terminator")
        records.append(
            {
                "id": row_id,
                "offset": offset,
                "source_hex": arm9[offset : offset + size].hex().upper(),
                "english": english,
                "context": context,
                "notes": "Runtime screenshot repair; replacement is explicitly null-terminated within the original fixed slot.",
            }
        )

    batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": ARM9_SHA256,
        "records": records,
    }
    args.out.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}: {len(records)} trading ARM9 repairs")


if __name__ == "__main__":
    main()
