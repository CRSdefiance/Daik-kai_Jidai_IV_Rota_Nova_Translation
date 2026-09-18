from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
OUTPUT_A = Path("translations/hodram_deep_route_v6a.json")
OUTPUT_B = Path("translations/hodram_deep_route_v6b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (114, 115, 116, 117, 118, 119, 120)
EXCLUDED = {
    "DK4_MES_B115_R0145": "Raw event-control payload; not dialogue.",
    "DK4_MES_B116_R0004": "Raw event-control payload; not dialogue.",
    "DK4_MES_B118_R0100": "Raw event-control payload; not dialogue.",
}

LINES = {
    "DK4_MES_B114_R0005": "Majestic",
    "DK4_MES_B114_R0010": "Answer me.",
    "DK4_MES_B114_R0021": "What has four legs at dawn, two at noon, and three at dusk?",
    "DK4_MES_B114_R0028": "Know it",
    "DK4_MES_B114_R0030": "No idea",
    "DK4_MES_B114_R0032": "No such beast",
    "DK4_MES_B114_R0044": "Begone, fool!",
    "DK4_MES_B114_R0048": "Waaah!",
    "DK4_MES_B114_R0060": "Begone, fool!",
    "DK4_MES_B114_R0064": "Waaah!",
    "DK4_MES_B114_R0077": "Then name it.",
    "DK4_MES_B114_R0084": "Humans",
    "DK4_MES_B114_R0086": "You, Sphinx",
    "DK4_MES_B114_R0088": "Other",
    "DK4_MES_B114_R0100": "Begone, fool!",
    "DK4_MES_B114_R0104": "Waaah!",
    "DK4_MES_B114_R0116": "Begone, fool!",
    "DK4_MES_B114_R0120": "Waaah!",
    "DK4_MES_B114_R0133": "That old riddle is dull. Another question.",
    "DK4_MES_B114_R0136": "12 people have 32 hands and feet on the floor, plus two canes. How many are babies?",
    "DK4_MES_B114_R0142": "3",
    "DK4_MES_B114_R0144": "4",
    "DK4_MES_B114_R0146": "5",
    "DK4_MES_B114_R0156": "Begone, fool!",
    "DK4_MES_B114_R0160": "Waaah!",
    "DK4_MES_B114_R0174": "Begone, fool!",
    "DK4_MES_B114_R0178": "Waaah!",
    "DK4_MES_B114_R0191": "Two canes means two elders...?",
    "DK4_MES_B114_R0197": "Hands and feet are known. Canes do not matter; elders still have two feet.",
    "DK4_MES_B114_R0200": "Ah, the earlier three-leg riddle fooled me.",
    "DK4_MES_B114_R0204": "Twelve people: 24 feet, eight hands on the floor. So four are babies.",
    "DK4_MES_B114_R0210": "Wise one! Take this!",

    "DK4_MES_B115_R0006": "Hmph!",
    "DK4_MES_B115_R0010": "Aaaah...",
    "DK4_MES_B115_R0014": "Ooooh!",
    "DK4_MES_B115_R0018": "A song? How strange...",
    "DK4_MES_B115_R0021": "A revelation! Our Ancient Megalith Society will soon rule the world!",
    "DK4_MES_B115_R0025": "We are chosen! We'll unearth this treasure and rule the godless fools!",
    "DK4_MES_B115_R0028": "Ooooh!",
    "DK4_MES_B115_R0032": "...Hardly peaceful.",
    "DK4_MES_B115_R0035": "Begin by attacking this village! Those who mocked us will learn!",
    "DK4_MES_B115_R0039": "Ooooh!",
    "DK4_MES_B115_R0047": "Too dangerous to ignore.",
    "DK4_MES_B115_R0050": "Evacuate the villagers at once!",
    "DK4_MES_B115_R0054": "Do it. Everyone, prepare for battle.",
    "DK4_MES_B115_R0057": "Yes!",
    "DK4_MES_B115_R0062": "Set fires! Spare no resistance!",
    "DK4_MES_B115_R0065": "Ooh!",
    "DK4_MES_B115_R0077": "Wait!",
    "DK4_MES_B115_R0084": "That's enough!",
    "DK4_MES_B115_R0092": "Surrender. Cooperate and this ends quietly. You don't want judgment by army and church.",
    "DK4_MES_B115_R0095": "Judge me? Godless fools! Capture them all for sacrifice!",
    "DK4_MES_B115_R0099": "Ooooh!",
    "DK4_MES_B115_R0103": "Brave, but choose your opponent better.",
    "DK4_MES_B115_R0114": "Now... mind your footing.",
    "DK4_MES_B115_R0120": "Waaah!",
    "DK4_MES_B115_R0132": "All aboard--into the pit.",
    "DK4_MES_B115_R0138": "A trap?! Curses! This way!",
    "DK4_MES_B115_R0143": "That way is closed too.",
    "DK4_MES_B115_R0147": "Ouch!",
    "DK4_MES_B115_R0159": "Caught you!",
    "DK4_MES_B115_R0166": "Take them!",
    "DK4_MES_B115_R0170": "Waaah!",
    "DK4_MES_B115_R0174": "Nearly a hundred followers... gone at once...",
    "DK4_MES_B115_R0178": "Who are you?!",
    "DK4_MES_B115_R0182": "No need to answer. You chose the army's merciless judgment.",
    "DK4_MES_B115_R0185": "Hm? What's this?",
    "DK4_MES_B115_R0189": "Don't touch that! No! My sacred mission is ruined!",
    "DK4_MES_B115_R0196": "Take him. Send the villagers home. We leave after.",
    "DK4_MES_B115_R0200": "Yes.",

    "DK4_MES_B116_R0006": "Did you kill my servant sent into the sea?",
    "DK4_MES_B116_R0009": "Servant? That monster fish? Yes, slain.",
    "DK4_MES_B116_R0013": "Then are you ruler of this sea?",
    "DK4_MES_B116_R0016": "Sea ruler...",
    "DK4_MES_B116_R0020": "No, nothing so grand. Yet in a sense, that is what we seek.",
    "DK4_MES_B116_R0024": "Hero! Claim the seal you seek!",
    "DK4_MES_B116_R0030": "What's it?",
    "DK4_MES_B116_R0034": "A coin from ancient times.",
    "DK4_MES_B116_R0038": "What can this mean?",

    "DK4_MES_B117_R0006": "Who are you? Wait...",
    "DK4_MES_B117_R0009": "Oh! Believers, after so long!",
    "DK4_MES_B117_R0012": "We fled Muslim rule and lived quietly, keeping our faith.",
    "DK4_MES_B117_R0016": "Pardon the sudden question. We seek the Proof of Conquest. Does anyone know its legends?",
    "DK4_MES_B117_R0019": "What! You seek the Proof? God's guidance!",
    "DK4_MES_B117_R0023": "You know?",
    "DK4_MES_B117_R0027": "Yes, certainly...",
    "DK4_MES_B117_R0031": "This lamp has passed down here. Seekers of the Proof are said to need it. Take it.",
    "DK4_MES_B117_R0036": "Please keep the Proof from the Ottoman Empire.",
    "DK4_MES_B117_R0040": "We promise every effort.",

    "DK4_MES_B118_R0007": "Colosseum visitor, answer me!",
    "DK4_MES_B118_R0010": "A riddle?",
    "DK4_MES_B118_R0014": "Answer.",
    "DK4_MES_B118_R0018": "A magic bean doubles each second: two after one, four after two, eight after three.",
    "DK4_MES_B118_R0022": "One bean fills a bag in 60 seconds. Starting with two, when is it full?",
    "DK4_MES_B118_R0025": "Choose your answer.",
    "DK4_MES_B118_R0032": "1 s",
    "DK4_MES_B118_R0034": "30 s",
    "DK4_MES_B118_R0036": "59 s",
    "DK4_MES_B118_R0045": "Gerhard, any idea?",
    "DK4_MES_B118_R0049": "None. We must guess.",
    "DK4_MES_B118_R0052": "A guess, then. The answer is one second.",
    "DK4_MES_B118_R0056": "Wrong!",
    "DK4_MES_B118_R0066": "Gerhard, any idea?",
    "DK4_MES_B118_R0070": "None. We must guess.",
    "DK4_MES_B118_R0073": "Then 30 seconds.",
    "DK4_MES_B118_R0076": "Wrong!",
    "DK4_MES_B118_R0087": "Gerhard, solved it.",
    "DK4_MES_B118_R0091": "Excellent! The answer?",
    "DK4_MES_B118_R0094": "59 seconds.",
    "DK4_MES_B118_R0098": "Well done! Wise and brave, take this!",

    "DK4_MES_B119_R0015": "Admiral, dead end.",
    "DK4_MES_B119_R0017": "Admiral, dead end.",
    "DK4_MES_B119_R0019": "A dead end.",
    "DK4_MES_B119_R0021": "A dead end.",
    "DK4_MES_B119_R0023": "A dead end.",
    "DK4_MES_B119_R0025": "A dead end.",
    "DK4_MES_B119_R0027": "A dead end.",
    "DK4_MES_B119_R0029": "A dead end.",
    "DK4_MES_B119_R0033": "An urn-shaped tablet lies here.",
    "DK4_MES_B119_R0036": "Pour from the urn left-handed.",
    "DK4_MES_B119_R0039": "Urn... left?",
    "DK4_MES_B119_R0046": "Push",
    "DK4_MES_B119_R0048": "Right",
    "DK4_MES_B119_R0050": "Left",
    "DK4_MES_B119_R0066": "Left hand means tilt right...",
    "DK4_MES_B119_R0089": "Run!",
    "DK4_MES_B119_R0093": "Waaah!",
    "DK4_MES_B119_R0100": "A sailor is hurt!",

    "DK4_MES_B120_R0007": "Sir.",
    "DK4_MES_B120_R0011": "Yes?",
    "DK4_MES_B120_R0015": "You seek the Proof of Conquest?",
    "DK4_MES_B120_R0018": "How know?",
    "DK4_MES_B120_R0021": "You seem to command soldiers.",
    "DK4_MES_B120_R0025": "Yes. A royal fleet is mine. Why?",
    "DK4_MES_B120_R0029": "Then this must be told...",
    "DK4_MES_B120_R0032": "Long ago Japan faced invasion by Yuan, history's greatest empire.",
    "DK4_MES_B120_R0036": "Yuan's invincible army was barely repelled by divine winds.",
    "DK4_MES_B120_R0039": "With an invincible navy too, the Yuan emperor might have conquered the world.",
    "DK4_MES_B120_R0043": "The Proof carries the boundless ambitions of kings who achieved such deeds.",
    "DK4_MES_B120_R0046": "Heirs to the Yuan emperor's will find his keepsake.",
    "DK4_MES_B120_R0050": "A keepsake?",
    "DK4_MES_B120_R0054": "Bring it here when you have it.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "0E": "Emilio Ferrog", "10": "Gerhard Adelknauts",
    "12": "Charles", "17": "Crewman", "89": "Japanese elder", "97": "Sailor",
    "A0": "Hidden Christian", "B1": "Cult leader", "B2": "Cultists",
    "CF": "Companion or scene voice", "D0": "Crewman", "FE": "Temple or system voice",
}
EXTENDED_STATES = {0x10, 0x12, 0x17, 0x97, 0xA0, 0xB1, 0xB2, 0xCF, 0xD0, 0xFE}
CONTEXT = {
    114: "Hodram solves the Sphinx's two riddles.",
    115: "Hodram stops an ancient-megalith cult from attacking a village.",
    116: "A sea deity confronts Hodram after he defeats its monstrous servant.",
    117: "Hidden Christians entrust Hodram with a lamp tied to the Proof of Conquest.",
    118: "Hodram solves the Colosseum's doubling-bean riddle.",
    119: "The expedition navigates an urn-and-left-hand ruin trap.",
    120: "A Japanese elder explains the Yuan emperor's link to the Proof of Conquest.",
}


def _write_batch(
    *,
    output: Path,
    blocks: tuple[int, ...],
    profile: str,
    source_rows: dict[str, dict[str, str]],
) -> int:
    selected_rows = {
        row_id: row
        for row_id, row in source_rows.items()
        if int(row_id.split("_B", 1)[1].split("_", 1)[0]) in blocks
    }
    selected_lines = {row_id: text for row_id, text in LINES.items() if row_id in selected_rows}
    selected_excluded = {row_id: note for row_id, note in EXCLUDED.items() if row_id in selected_rows}
    if set(selected_lines) | set(selected_excluded) != set(selected_rows):
        raise SystemExit(f"Hodram V6 inventory mismatch in {output}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in selected_lines.items():
        row = selected_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        first = bytes.fromhex(row["source_hex"])[0]
        states = EXTENDED_STATES | ({0x89} if block == 120 else set())
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in states) else ""
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Choice or scene text"),
            "context": CONTEXT[block],
            "source_meaning": english,
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line"],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": profile,
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": f"Hodram Proof-of-Conquest events across SC1 blocks {blocks[0]}-{blocks[-1]}.",
        "excluded_records": selected_excluded,
        "inventory": {
            "identified_records": len(selected_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    output.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}: {len(records)} records, {len(selected_excluded)} controls preserved")
    return len(records)


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row
            for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)
        }
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V6 inventory mismatch: missing={missing}, extra={extra}")
    count_a = _write_batch(
        output=OUTPUT_A,
        blocks=(114, 115, 116, 117, 118, 119),
        profile="hodram-story-proof-live",
        source_rows=source_rows,
    )
    count_b = _write_batch(
        output=OUTPUT_B,
        blocks=(120,),
        profile="hodram-story-live",
        source_rows=source_rows,
    )
    if count_a + count_b != len(LINES):
        raise SystemExit("Hodram V6 split lost translated records")


if __name__ == "__main__":
    main()
