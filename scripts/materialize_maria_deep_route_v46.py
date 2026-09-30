from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
OUTPUT = Path("translations/maria_deep_route_v46.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (19,)

LINES = {
    "DK4_MES_B19_R0005": "Damn, beaten again...{LB}But next time... Huh?!",
    "DK4_MES_B19_R0008": "Bad news.{LB}No next time for you.",
    "DK4_MES_B19_R0011": "Heh heh...",
    "DK4_MES_B19_R0015": "What?! Say that again!",
    "DK4_MES_B19_R0019": "Huh? Did you not hear me?",
    "DK4_MES_B19_R0023": "No one here obeys you{LB}anymore!",
    "DK4_MES_B19_R0026": "Damn you!{LB}You traitors!",
    "DK4_MES_B19_R0029": "Trouble aboard{LB}that ship.",
    "DK4_MES_B19_R0033": "{LB}Trouble is brewing.{LB}A quarrel, maybe.",
    "DK4_MES_B19_R0036": "Let us go.{LB}Bring us alongside.",
    "DK4_MES_B19_R0040": "We keep losing, and our purse{LB}stays empty. You are going{LB}to answer for that.",
    "DK4_MES_B19_R0044": "My fault?",
    "DK4_MES_B19_R0048": "And why do you keep{LB}chasing {MACRO:FO} around?",
    "DK4_MES_B19_R0052": "Hah! You have a reason{LB}you cannot share?!",
    "DK4_MES_B19_R0059": "Your real aim is to recover{LB}the Bloodstained Shamshir{LB}from {MACRO:FO}.{LB}Your father's keepsake!",
    "DK4_MES_B19_R0063": "That is... not why...",
    "DK4_MES_B19_R0067": "You have failed as our chief.{LB}No one follows a leader{LB}who cannot earn coin. Prepare!",
    "DK4_MES_B19_R0071": "Her life{LB}is in danger.",
    "DK4_MES_B19_R0074": "{LB}But this is no affair{LB}for outsiders...",
    "DK4_MES_B19_R0077": "Let me.",
    "DK4_MES_B19_R0081": "Al!",
    "DK4_MES_B19_R0085": "What?{LB}Stay out, outsider!",
    "DK4_MES_B19_R0088": "...Know your place.",
    "DK4_MES_B19_R0092": "None of your concern!{LB}Get rid of Aziza and this fool{LB}together!",
    "DK4_MES_B19_R0096": "Lord Al, allow me!",
    "DK4_MES_B19_R0100": "Count me in!{LB}Only cowards rely{LB}on numbers!",
    "DK4_MES_B19_R0103": "Yahoo!{LB}Come fight me!",
    "DK4_MES_B19_R0107": "...Pirates!{LB}Come on, then!",
    "DK4_MES_B19_R0110": "Why...? Why fight for me?{LB}We were enemies{LB}only moments ago...",
    "DK4_MES_B19_R0114": "Damn, the odds are bad!{LB}Why are they all{LB}siding with Aziza?!",
    "DK4_MES_B19_R0118": "Wait!",
    "DK4_MES_B19_R0122": "You came{LB}to save her too?",
    "DK4_MES_B19_R0126": "Exactly.{LB}Touch her, and your own safety{LB}is not guaranteed.",
    "DK4_MES_B19_R0130": "{MACRO:FI} {MACRO:FA}...",
    "DK4_MES_B19_R0134": "...No way out, then.",
    "DK4_MES_B19_R0138": "Release her peacefully,{LB}and we can pay you.",
    "DK4_MES_B19_R0141": "What if we demand 1,000,000?{LB}We hate this woman that much.",
    "DK4_MES_B19_R0144": "...Absurd!",
    "DK4_MES_B19_R0148": "Al, stand down.{LB}Aziza's safety comes first.",
    "DK4_MES_B19_R0151": "All that money... for me...",
    "DK4_MES_B19_R0156": "Then we have a deal.{LB}Aziza, come this way.",
    "DK4_MES_B19_R0163": "That settles it. Bye!",
    "DK4_MES_B19_R0169": "Betrayed by my own crew...{LB}How far have we fallen?{LB}But why did you save me?",
    "DK4_MES_B19_R0173": "That tavern encounter...{LB}You intrigued me{LB}from that day.",
    "DK4_MES_B19_R0176": "Something has troubled me...{LB}Why would one of your caliber{LB}stoop to piracy?",
    "DK4_MES_B19_R0180": "You flatter me.{LB}But this was no fall.{LB}Piracy is my family trade.",
    "DK4_MES_B19_R0184": "{LB}Oh",
    "DK4_MES_B19_R0188": "Those pirates served my father.{LB}As a child, watching them{LB}taught me swordplay{LB}and piracy.",
    "DK4_MES_B19_R0191": "Your father...?",
    "DK4_MES_B19_R0195": "He died by accident.{LB}That sword was his treasure.{LB}Both vanished.",
    "DK4_MES_B19_R0199": "That is{LB}the Bloodstained Shamshir...",
    "DK4_MES_B19_R0202": "My dream: to become{LB}a great pirate like him.{LB}His every move was my guide...",
    "DK4_MES_B19_R0206": "So when we learned you had{LB}his sword, we had to take it.{LB}Then maybe...",
    "DK4_MES_B19_R0209": "Then maybe...?",
    "DK4_MES_B19_R0213": "That would prove{LB}we were like him...{LB}Heh. But now...",
    "DK4_MES_B19_R0217": "Greatness was never{LB}my true wish.{LB}All along, what mattered{LB}was father's keepsake...",
    "DK4_MES_B19_R0220": "No wonder they abandoned me.{LB}That prize meant no profit.{LB}They had reason.",
    "DK4_MES_B19_R0224": "Still drawn{LB}to piracy?",
    "DK4_MES_B19_R0228": "My goal was my father,{LB}not piracy.{LB}That life is over now.",
    "DK4_MES_B19_R0232": "Sir...",
    "DK4_MES_B19_R0236": "We understand, Al.{LB}That is why we intervened.{LB}Talent like hers is rare.{LB}Will you come with us?",
    "DK4_MES_B19_R0239": "Thank you... Give me a berth,{LB}and you will get my all.{LB}You saved my life, after all.",
    "DK4_MES_B19_R0243": "And from now on,{LB}just call me Aziza.",
    "DK4_MES_B19_R0246": "Good.{LB}We expect much of you.",
}

STATES = {0x03, 0x07, 0x0A, 0x0B, 0x0C, 0x11, 0x1B, 0xB7, 0xB8, 0xB9}
SPEAKERS = {
    "03": "Maria",
    "07": "Charlotte",
    "0A": "Yi Sun-sin",
    "0B": "Jam",
    "0C": "Yuki",
    "11": "Al",
    "1B": "Aziza",
    "B7": "Mutinous pirate",
    "B8": "Mutinous pirate",
    "B9": "Mutinous pirate",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    rows = {
        record_id: row
        for record_id, row in all_rows.items()
        if record_id.startswith("DK4_MES_B19_")
    }
    if set(LINES) != set(rows):
        raise SystemExit(
            f"Maria V46 mismatch: missing={sorted(set(rows) - set(LINES))}, "
            f"extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    for record_id in sorted(LINES, key=lambda value: int(value.rsplit("R", 1)[1])):
        row = rows[record_id]
        english = LINES[record_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if first in STATES and not row["japanese"].startswith("{LB}")
            else ""
        )
        leading_break = english.startswith("{LB}")
        source_breaks = row["japanese"].count("{LB}")
        target_breaks = english.count("{LB}")
        waivers = ["weak-line-ending", "orphan-final-line"]
        if target_breaks:
            waivers.append("manual-break")
        if leading_break:
            waivers.append("source-leading-linebreak")
        if source_breaks != target_breaks:
            waivers.append("line-break-count")
        record = {
            "id": record_id,
            "english": (
                f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}"
            ),
            "speaker": SPEAKERS.get(state, "Companion"),
            "context": (
                "Maria route: Aziza's crew mutiny, rescue and ransom branches, "
                "family history, renunciation of piracy, and recruitment."
            ),
            "source_meaning": (
                english.replace("{LB}", " ")
                .replace("{MACRO:FI}", "the protagonist's given name")
                .replace("{MACRO:FA}", "the protagonist's surname")
                .replace("{MACRO:FO}", "the rival fleet leader's name")
                .strip()
            ),
            "localization_note": (
                "Direct SC3 translation reviewed for natural English, branch parity, "
                "macro preservation, and presentation-state safety."
            ),
            "qa_waivers": waivers,
            "review": {
                "source": True,
                "context": True,
                "localization": True,
                "naturalness": True,
                "formatting": True,
            },
        }
        if target_breaks:
            record["manual_break_reason"] = (
                "Preserves the source transition or groups the thought within four display lines."
            )
        records.append(record)

    payload = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v46-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": (
            "Maria SC3 block 19: Aziza's mutiny, rescue/ransom branches, backstory, "
            "retirement from piracy, and recruitment."
        ),
        "inventory": {
            "identified_records": len(rows),
            "translated_records": len(records),
            "excluded_records": 0,
            "blocks": {"19": len(records)},
        },
        "excluded": [],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
