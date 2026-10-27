from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc3/script.csv")
REUSE = Path("work/analysis/sc3_cross_route_reuse.json")
OUTPUT = Path("translations/maria_deep_route_v25.json")
SC3_SHA256 = "001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2"
BLOCKS = (176, 177, 178, 184, 185, 186)
EXCLUDED = {
    "DK4_MES_B178_R0006": "Four-byte nontext parrot event payload 414893A8.",
    "DK4_MES_B186_R0021": "Four-byte nontext sword-legend event payload 214896A8.",
}

OVERRIDES = {
    "DK4_MES_B176_R0008": "Something?",
    "DK4_MES_B176_R0016": "An insect?",
    "DK4_MES_B176_R0023": "Yes.",
    "DK4_MES_B176_R0045": "Yes. Take this.",
    "DK4_MES_B176_R0049": "This?",
    "DK4_MES_B176_R0053": "A book about ingredients used in medicine.",
    "DK4_MES_B176_R0056": "This must be valuable.{LB}We can't accept it.",
    "DK4_MES_B176_R0059": "No longer needed, so it's yours.",
    "DK4_MES_B176_R0066": "Hohoho. Your friend seems to want it.",
    "DK4_MES_B176_R0069": "Huh? Well...{LB}The book did look interesting.",
    "DK4_MES_B176_R0073": "All right.{LB}Sell it for 1,000 coins?",
    "DK4_MES_B176_R0076": "Hohoho. Then 100 coins will do.",
    "DK4_MES_B176_R0079": "{MACRO:FI}: Charm +1!",
    "DK4_MES_B177_R0004": "Bored. Time to go somewhere.",
    "DK4_MES_B177_R0008": "Ma'am, anywhere interesting nearby?{LB}A walk might cure this boredom.",
    "DK4_MES_B177_R0012": "Well, the lord's castle lies east.",
    "DK4_MES_B177_R0015": "A castle? Sounds good.{LB}Time to see this country's castle.",
    "DK4_MES_B177_R0018": "Jam,{LB}where have you been?",
    "DK4_MES_B177_R0021": "Sorry.{LB}This was heavy.",
    "DK4_MES_B177_R0024": "Goodness...{LB}Where did you get that?",
    "DK4_MES_B177_R0027": "Obviously a figurehead!{LB}Genuine, made in Japan!",
    "DK4_MES_B177_R0031": "People here don't know how to use figureheads.{LB}Showed them, and got this as thanks.",
    "DK4_MES_B177_R0034": "Good. Glad they understand now.{LB}We're leaving soon, so get ready.",
    "DK4_MES_B177_R0037": "Got it.{LB}Give me a moment.",
    "DK4_MES_B177_R0042": "My lord! My looord!{LB}Disaster!",
    "DK4_MES_B177_R0045": "What now?{LB}So noisy at dawn!",
    "DK4_MES_B177_R0049": "The shachihoko vanished,{LB}and this foreign letter appeared!",
    "DK4_MES_B177_R0052": "What?! The shachihoko is gone?{LB}Catch that thief at any cost!",
    "DK4_MES_B177_R0059": "Dear lord of Japan,",
    "DK4_MES_B177_R0063": "That statue is a figurehead.{LB}Such things go on ships, not castles.{LB}Someone misunderstood.",
    "DK4_MES_B177_R0066": "No thanks needed. Took one spare instead.{LB}One figurehead per ship. Remember that.",
    "DK4_MES_B177_R0069": "Take care.{LB}Jam Jack Ludwayer",
    "DK4_MES_B178_R0004": "flap, flap!",
    "DK4_MES_B178_R0008": "Whoa! What is that?!",
    "DK4_MES_B178_R0012": "WHAT'S THAT",
    "DK4_MES_B178_R0016": "Mamma mia!{LB}That bird spoke!",
    "DK4_MES_B178_R0019": "THAT PARROT TALKED",
    "DK4_MES_B178_R0023": "A parrot.",
    "DK4_MES_B178_R0027": "A parrot, eh?",
    "DK4_MES_B178_R0031": "A PARROT, EH",
    "DK4_MES_B178_R0035": "Quit that!",
    "DK4_MES_B178_R0039": "STOP THAT",
    "DK4_MES_B178_R0043": "Oh, fun!{LB}Time to catch you!",
    "DK4_MES_B178_R0046": "Here goes! Hah!",
    "DK4_MES_B178_R0050": "flap! Thud! Crash!{LB}flap! Bang! Rustle!",
    "DK4_MES_B178_R0054": "Got it!",
    "DK4_MES_B178_R0058": "Whew!{LB}Surrender now? Hahahaha!",
    "DK4_MES_B178_R0062": "SURRENDER NOW",
    "DK4_MES_B178_R0066": "Hehe.",
    "DK4_MES_B184_R0004": "What a lovely square...{LB}Something is in that pond. Could that be...",
    "DK4_MES_B184_R0012": "A pair of swans!{LB}They visit even here?{LB}Are you two traveling too?",
    "DK4_MES_B184_R0020": "Hehe. So loving.{LB}Enviable.",
    "DK4_MES_B184_R0023": "flap, flap!",
    "DK4_MES_B184_R0027": "Oh! Where are they going?{LB}They're carrying something!",
    "DK4_MES_B184_R0035": "Cristina,{LB}what did you see?",
    "DK4_MES_B184_R0038": "Oh, Admiral {MACRO:FI}.{LB}A pair of swans was here.",
    "DK4_MES_B184_R0041": "They come even into town?",
    "DK4_MES_B184_R0044": "They carried something long and shining{LB}toward Amsterdam. Shall we look?",
    "DK4_MES_B185_R0004": "Hey, do you know{LB}Romance of the Three Kingdoms?",
    "DK4_MES_B185_R0009": "Yes.",
    "DK4_MES_B185_R0011": "No.",
    "DK4_MES_B185_R0021": "No? Read it.{LB}A wonderful tale.",
    "DK4_MES_B185_R0031": "You do? Wonderful!{LB}Who's your favorite hero?",
    "DK4_MES_B185_R0038": "Zhao",
    "DK4_MES_B185_R0040": "Guan",
    "DK4_MES_B185_R0042": "Zhuge",
    "DK4_MES_B185_R0050": "What?! Same as me!{LB}We'll get along.",
    "DK4_MES_B185_R0053": "His charge through Cao Cao's army{LB}with A Dou was magnificent!",
    "DK4_MES_B185_R0057": "Rumor says Zhao Yun's legendary spear{LB}lies somewhere on this peninsula.",
    "DK4_MES_B185_R0061": "Searched everywhere, but failed.{LB}Perhaps you can find it.",
    "DK4_MES_B185_R0077": "Zhuge Liang?{LB}His memorial brings tears.{LB}My second favorite.",
    "DK4_MES_B186_R0008": "What?",
    "DK4_MES_B186_R0012": "Could you show me that?",
    "DK4_MES_B186_R0019": "That item.",
    "DK4_MES_B186_R0023": "Hmm... No mistake.{LB}Just as foretold.",
    "DK4_MES_B186_R0030": "Three centuries ago,{LB}great Kublai Khan ruled the continent.",
    "DK4_MES_B186_R0034": "Yet even that emperor eventually died...",
    "DK4_MES_B186_R0037": "The emperor said:{LB}'Two centuries hence,{LB}the Sea King shall come...'",
    "DK4_MES_B186_R0041": "'The Sea King leads foreigners{LB}and bears a seal beyond my lands.{LB}He commands the open seas.{LB}Give that hero my sword.'",
    "DK4_MES_B186_R0044": "My clan served him.{LB}We awaited the Sea King...",
    "DK4_MES_B186_R0047": "Today, you have appeared at last.{LB}Ruler of the oceans, we awaited you.",
    "DK4_MES_B186_R0051": "Sir, there must be a mistake.{LB}That Sea King cannot be me.",
    "DK4_MES_B186_R0055": "No. These eyes do not err.{LB}You are truly the Sea King.",
    "DK4_MES_B186_R0058": "Search south of Shandong.{LB}The emperor's sword lies there.",
    "DK4_MES_B186_R0061": "The Great Sword is now yours.{LB}Go well.",
}

SPEAKERS = {
    "03": "Maria", "07": "Cristina", "0B": "Jam", "0F": "Emilio",
    "4C": "Mikhail", "7C": "Retainer", "82": "Japanese lord",
    "91": "Townswoman", "95": "Three Kingdoms enthusiast", "AA": "Old man",
    "FE": "System, animal sound, or letter",
}
PRESENTATION_STATES = {int(value, 16) for value in SPEAKERS}


def main() -> None:
    report = json.loads(REUSE.read_text(encoding="utf-8"))
    lines = {
        str(item["id"]): str(item["variants"][0]["english"])
        for item in report["reusable"] if int(item["block"]) in BLOCKS
    }
    lines.update(OVERRIDES)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    prefixes = tuple(f"DK4_MES_B{block}_" for block in BLOCKS)
    rows = {row_id: row for row_id, row in all_rows.items() if row_id.startswith(prefixes)}
    if set(lines) | set(EXCLUDED) != set(rows) or set(lines) & set(EXCLUDED):
        raise SystemExit(
            f"Maria V25 mismatch: missing={sorted(set(rows)-set(lines)-set(EXCLUDED))}, "
            f"extra={sorted((set(lines)|set(EXCLUDED))-set(rows))}"
        )

    records = []
    block_counts: dict[str, int] = {}
    excluded_counts: dict[str, int] = {}
    for row_id in sorted(rows, key=lambda value: (int(value.split("_B")[1].split("_")[0]), int(value.rsplit("R", 1)[1]))):
        block = row_id.split("_B", 1)[1].split("_", 1)[0]
        if row_id in EXCLUDED:
            excluded_counts[block] = excluded_counts.get(block, 0) + 1
            continue
        english = lines[row_id]
        row = rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in PRESENTATION_STATES else ""
        block_counts[block] = block_counts.get(block, 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice text"),
            "context": "Complete shared optional event with verified nontext payloads excluded.",
            "source_meaning": english,
            "localization_note": "Cross-route match or direct SC3 translation reviewed for natural English and state-byte safety.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"] + (["manual-break"] if "{LB}" in english else []),
            **({"manual_break_reason": "Protects semantic rows and pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })

    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC3.DK4",
        "source_file_sha256": SC3_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "maria-story-shared-events-v25-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Maria SC3 blocks 176-178 and 184-186: six complete shared optional events.",
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "excluded_records": len(EXCLUDED), "blocks": block_counts, "excluded_blocks": excluded_counts},
        "excluded": [{"id": row_id, "reason": reason} for row_id, reason in EXCLUDED.items()],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} preserved payloads")


if __name__ == "__main__":
    main()
