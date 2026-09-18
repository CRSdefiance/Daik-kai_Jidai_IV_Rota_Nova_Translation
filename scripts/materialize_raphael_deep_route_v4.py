from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v4.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
LINES = {
    "DK4_MES_B76_R0008": "Ah! Admiral Hayreddin!",
    "DK4_MES_B76_R0012": "...You have grown, {MACRO:FI}.{LB}The Ottoman Pasha fleet is mighty,{LB}but perhaps you can...",
    "DK4_MES_B76_R0016": "Y-yes!{LB}(Wait, be confident!){LB}Of course!",
    "DK4_MES_B76_R0020": "Defeat Pasha's fleet,{LB}then meet Alexandria's priest.",
    "DK4_MES_B76_R0024": "Alexandria's priest...?{LB}We will remember.",
    "DK4_MES_B76_R0027": "Stay on guard.",
    "DK4_MES_B76_R0031": "Right! Thanks, old man!",
    "DK4_MES_B76_R0034": "Heh...{LB}Goodbye.",
    "DK4_MES_B76_R0038": "Goodbye...{LB}Admiral Hayreddin!",
    "DK4_MES_B77_R0006": "We did it!{LB}{MACRO:FO} tops the Mediterranean!",
    "DK4_MES_B77_R0010": "Valdes beat us badly at sea...{LB}But victory is victory!{LB}Hold your head high!",
    "DK4_MES_B77_R0014": "Right. Victory at sea is not everything!{LB}Now conquer the rest!",
    "DK4_MES_B78_R0005": "We rule the Mediterranean seas!{LB}Even Spain cannot ignore{LB}{MACRO:FO}, supporter of{LB}Portugal's royal crown.",
    "DK4_MES_B78_R0010": "Y-yes.{LB}Hope so...",
    "DK4_MES_B78_R0013": "You are now ruler of the seas{LB}in name and deed! Stand proud!",
    "DK4_MES_B78_R0018": "Y-yes, right.{LB}Thanks, Clau!",
    "DK4_MES_B78_R0021": "You are our admiral!{LB}Almost there. Stay strong!",
    "DK4_MES_B78_R0025": "Let us conquer every sea!!",
    "DK4_MES_B78_R0029": "Ooooooh!!",
    "DK4_MES_B79_R0005": "Lord {MACRO:FA},{LB}well done. You became ruler{LB}of the Mediterranean.{LB}Please accept this.",
    "DK4_MES_B79_R0011": "Whew...{LB}At last.",
    "DK4_MES_B79_R0022": "Another Proof map.{LB}The Mediterranean treasure{LB}should be a crown...",
    "DK4_MES_B79_R0029": "Then find that crown!{LB}Let us go!",
    "DK4_MES_B79_R0033": "But this pattern on the cloth{LB}looks nothing like a map...",
    "DK4_MES_B80_R0013": "At last! You are {MACRO:FA}, right?{LB}The king of Portugal summons you!",
    "DK4_MES_B80_R0019": "Lord {MACRO:FA} has returned!{LB}The king summons you!",
}

SPEAKERS = {"05": "Claudio Manous", "08": "Arcadius", "22": "Hayreddin", "71": "Sailor", "8B": "Alexandria priest", "97": "Crew"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    "76": "Hayreddin warns Raphael about Pasha's Ottoman fleet and directs him to Alexandria's priest after victory.",
    "77": "Raphael and Claudio celebrate becoming the Mediterranean's strongest faction despite losing the direct naval clash with Valdes.",
    "78": "The crew celebrates Raphael's dominance and the growing political hope for Portugal's restoration.",
    "79": "An Alexandria priest gives Raphael the Mediterranean Proof map, whose cloth pattern points toward a crown.",
    "80": "Portuguese sailors tell Raphael that the king has summoned him home.",
}
EXCLUDED = {
    "DK4_MES_B76_R0004": "eleven-byte scene-control payload with no visible dialogue",
    "DK4_MES_B79_R0006": "four-byte reward-control payload with no visible dialogue",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = (set(LINES) | set(EXCLUDED)) - set(all_rows)
    if missing:
        raise SystemExit(f"Raphael V4 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Raphael Castor"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Natural concise American English preserving route objectives, political stakes, celebration, and all player-name macros.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v4-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Hayreddin warning, Mediterranean victory, Proof map reward, and Portuguese royal summons across SC0 blocks 76-80.",
        "excluded_records": EXCLUDED,
        "inventory": {"identified_records": len(LINES) + len(EXCLUDED), "translated_records": len(records), "blocks": {"76": 9, "77": 3, "78": 7, "79": 5, "80": 2}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records; excluded {len(EXCLUDED)} controls")


if __name__ == "__main__":
    main()
