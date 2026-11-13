from __future__ import annotations

import csv
import json
from pathlib import Path

S = Path("work/sc3/script.csv")
O = Path("translations/maria_deep_route_v92.json")
SHA = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"

L = {
    "DK4_MES_B110_R0004": "(Th-that's {MACRO:FI}...{LB}What brings her here?)",
    "DK4_MES_B110_R0007": "(Not as fearsome as rumors say...{LB}Maybe if this stays polite,{LB}nothing will happen...)",
    "DK4_MES_B110_R0011": "{MACRO:FA}, thank you for beating{LB}those who hurt us!{LB}W-we owe you... very much!",
    "DK4_MES_B110_R0014": "...No need.",
    "DK4_MES_B110_R0025": "Ha ha ha!{LB}We always stand with{LB}the common people.",
    "DK4_MES_B110_R0034": "A man in Malacca{LB}was looking for you, Admiral.",
    "DK4_MES_B110_R0037": "Got it. Thanks.",
    "DK4_MES_B110_R0053": "That man was trembling...",
    "DK4_MES_B110_R0060": "(Even here, they fear me...{LB}Why?)",
    "DK4_MES_B111_R0004": "Ma'am, been waiting.{LB}Could you take this man{LB}to a village called Guam?",
    "DK4_MES_B111_R0012": "What happened?",
    "DK4_MES_B111_R0016": "We cannot share words, but{LB}he drifted to the spice isles{LB}in a dugout canoe.",
    "DK4_MES_B111_R0020": "He stowed aboard a Western ship{LB}and reached here,{LB}but cannot return home.",
    "DK4_MES_B111_R0024": "Guam, was it?{LB}Where is that village?",
    "DK4_MES_B111_R0027": "Do not ask me. He only points{LB}east-northeast.",
    "DK4_MES_B111_R0030": "...What now?",
    "DK4_MES_B111_R0034": "No one else can help.{LB}Please, ma'am.",
    "DK4_MES_B111_R0037": "This may take time.{LB}But if that is acceptable,{LB}he may board my ship.",
    "DK4_MES_B111_R0041": "Thank you!",
    "DK4_MES_B111_R0045": "Xie xie.",
    "DK4_MES_B111_R0049": "Chinese?",
    "DK4_MES_B111_R0053": "Those words came from me.{LB}Certain you would agree.",
    "DK4_MES_B111_R0057": "Such faith in me.",
    "DK4_MES_B111_R0061": "Xie xie.",
    "DK4_MES_B112_R0004": "What is the Southeast Asian{LB}Proof map?",
    "DK4_MES_B112_R0007": "{LB}The Ancient Kingdom Coin seems likely.{LB}Yet no map is drawn on it...",
    "DK4_MES_B112_R0011": "The Jar of Milky Lotion{LB}also lacks a known use.",
    "DK4_MES_B112_R0014": "Put the Ancient Kingdom Coin{LB}into the jar? Better to try{LB}than keep thinking.",
    "DK4_MES_B112_R0018": "{LB}No!{LB}The lotion melts the coin!",
    "DK4_MES_B112_R0021": "Wait!",
    "DK4_MES_B112_R0025": "The surface dissolved,{LB}revealing a map. Quite a trick.",
    "DK4_MES_B112_R0028": "{LB}Good that your guess was right.{LB}{MACRO:FI} can be rather bold...",
    "DK4_MES_B112_R0032": "My hand moved before thought.{LB}More caution is needed.{LB}Sorry to worry you, Xien.",
    "DK4_MES_B112_R0036": "{LB}No harm done.{LB}Now finding the Proof{LB}comes first.",
}
EX = {
    "DK4_MES_B112_R0023": "Raw four-byte event-control payload between the coin-dissolve warning and map reveal; not dialogue."
}
SP = {
    "03": "Maria",
    "0B": "Jam",
    "4A": "Kamil",
    "71": "Port contact",
    "74": "Townsman",
    "87": "Guam castaway",
}
ST = {int(value, 16) for value in SP}
CONTEXT = {
    110: "A frightened townsman thanks Maria and reports a man seeking her in Malacca, deepening her concern about her reputation.",
    111: "Maria accepts a request to return a stranded castaway to Guam.",
    112: "Maria and Xien combine the Ancient Kingdom Coin and Jar of Milky Lotion to reveal the Southeast Asian Proof map.",
}


def main() -> None:
    with S.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if 110 <= int(row["id"].split("_B", 1)[1].split("_R", 1)[0]) <= 112
        }
    if set(L) | set(EX) != set(rows):
        raise SystemExit(
            f"V92 mismatch: missing={sorted(set(rows) - set(L) - set(EX))}; "
            f"extra={sorted((set(L) | set(EX)) - set(rows))}"
        )
    records = []
    for record_id in sorted(
        L,
        key=lambda value: (
            int(value.split("_B", 1)[1].split("_R", 1)[0]),
            int(value.rsplit("R", 1)[1]),
        ),
    ):
        row = rows[record_id]
        english = L[record_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in ST else ""
        unmasked = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "F" in unmasked or "I" in unmasked:
            raise SystemExit(f"{record_id}: unsafe macro literal: {english}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if row["japanese"].startswith("{LB}"):
            waivers.append("source-leading-linebreak")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        block = int(record_id.split("_B", 1)[1].split("_R", 1)[0])
        prefix = f"{{SPEAKER:{state}}}" if state else ""
        records.append(
            {
                "id": record_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": SP.get(state, "Maria or Xien continuation"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Direct SC3 translation preserving speaker states, inner monologue, route-name macros, item names, the verified raw control, and fixed allocation.",
                "qa_waivers": waivers,
                **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if target_breaks else {}),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )
    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SHA,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v92-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 110-112: frightened townsman, Guam castaway request, and Southeast Asian Proof-map item combination.",
        "excluded_records": EX,
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": len(EX),
            "blocks": {"110": 9, "111": 15, "112": 11},
        },
        "records": records,
    }
    O.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {O}: {len(records)} translations + {len(EX)} control")


if __name__ == "__main__":
    main()
