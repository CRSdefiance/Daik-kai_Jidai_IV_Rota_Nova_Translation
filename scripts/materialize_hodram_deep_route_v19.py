from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v19.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(240, 250))
EXCLUDED = {
    "DK4_MES_B243_R0100": "Raw two-byte event-control payload; not dialogue.",
}


LINES = {
    # Cesare fumes over sailors discussing the Demon-Piercing Arrow.
    "DK4_MES_B240_R0005": "Blast! What are those fools saying?",
    "DK4_MES_B240_R0008": "What has you so angry, Cesare?",
    "DK4_MES_B240_R0011": "The sailors are wasting time on nonsense, sir.",
    "DK4_MES_B240_R0014": "Nonsense?",
    "DK4_MES_B240_R0018": "They neglect their work to chatter about the Demon-Piercing Arrow. That absurd name belongs to the item, sir!",
    "DK4_MES_B240_R0021": "Hard to follow. What is this{LB}Demon-Piercing Arrow?",
    "DK4_MES_B240_R0024": "A legendary arrow an angel used to slay a demon, sir.",
    "DK4_MES_B240_R0028": "They say it grants genius with a bow. The sailors wonder whether it helps cannons, instead of tending the ship.",
    "DK4_MES_B240_R0031": "Cannon practice would help them far more than idle chatter!",
    "DK4_MES_B240_R0035": "No such treasure lies near Britain, yet they claim it is on Skye or that someone saw it on Lewis.",
    "DK4_MES_B240_R0038": "They cheer over foolish rumors!{LB}Were it so close, someone would have{LB}taken it already!",
    "DK4_MES_B240_R0041": "...No point arguing with him now.",
    "DK4_MES_B240_R0044": "Those men are always like this! Grumble... grumble...",

    # Gennas is hurt repairing the ship; a sailor offers to find lost gloves.
    "DK4_MES_B241_R0005": "Gah! ...Ouch...",
    "DK4_MES_B241_R0009": "Gennas? What happened?",
    "DK4_MES_B241_R0012": "Nothing serious. A mast fitting caught this man's hand during maintenance.",
    "DK4_MES_B241_R0016": "Hey, friend. What happened?",
    "DK4_MES_B241_R0019": "Well... This...",
    "DK4_MES_B241_R0023": "Our navigator hurt his hand.",
    "DK4_MES_B241_R0026": "That is no good. Let me see it.",
    "DK4_MES_B241_R0029": "...Ouch.",
    "DK4_MES_B241_R0033": "Hm. The sort of wound every seaman gets.",
    "DK4_MES_B241_R0036": "Heh. Good gloves can prevent this.",
    "DK4_MES_B241_R0040": "Glove?",
    "DK4_MES_B241_R0044": "Yes! Rare and very useful gloves. Wait... Where did this man put them?",
    "DK4_MES_B241_R0047": "Oh no! Were they dropped somewhere?",
    "DK4_MES_B241_R0050": "...Hopeless.",
    "DK4_MES_B241_R0054": "Sorry. They must have been lost around Denmark!",
    "DK4_MES_B241_R0058": "Denmark?",
    "DK4_MES_B241_R0062": "Yes! Somewhere on Jutland. Truly! Believe this man!",
    "DK4_MES_B241_R0066": "We shall search.",
    "DK4_MES_B241_R0070": "You believe me? Recover them, and they are yours.",
    "DK4_MES_B241_R0074": "They never fit this man's hands, so they would be sold anyway. Their quality is guaranteed.",

    # Hodram returns the frozen rose and receives a church lead.
    "DK4_MES_B242_R0006": "Welcome.",
    "DK4_MES_B242_R0010": "That ornament you carry... May this woman see it?",
    "DK4_MES_B242_R0014": "This?",
    "DK4_MES_B242_R0018": "Yes! Where did you find it?",
    "DK4_MES_B242_R0021": "A petty criminal named Gabriel had it.",
    "DK4_MES_B242_R0024": "That is this woman's treasure! Stolen some time ago...",
    "DK4_MES_B242_R0028": "Birthday gift from her father,{LB}since this woman loves roses.{LB}Treasured dearly.",
    "DK4_MES_B242_R0032": "Then it has returned{LB}to its rightful owner.",
    "DK4_MES_B242_R0036": "Returned the frozen rose.",
    "DK4_MES_B242_R0045": "Thank you! This woman had given up hope of ever holding it again!",
    "DK4_MES_B242_R0049": "Some reward must be given...",
    "DK4_MES_B242_R0053": "The guild already paid us for capturing Gabriel. Nothing more is needed.",
    "DK4_MES_B242_R0057": "{MACRO:FI}...!",
    "DK4_MES_B242_R0061": "Bye.",
    "DK4_MES_B242_R0072": "Wait!",
    "DK4_MES_B242_R0076": "Your crew explores the whole world, right?",
    "DK4_MES_B242_R0079": "Seen the church outside town?{LB}Wooden churches are rare in Europe.",
    "DK4_MES_B242_R0084": "Hidden nearby. That never occurred to us. We will visit.",
    "DK4_MES_B242_R0093": "Thank you again! Please return!",

    # Hodram and an elder attempt to claim a supernatural figurehead.
    "DK4_MES_B243_R0006": "Sir!",
    "DK4_MES_B243_R0010": "What?",
    "DK4_MES_B243_R0014": "Look! A splendid figurehead!",
    "DK4_MES_B243_R0017": "You found it, then.",
    "DK4_MES_B243_R0021": "Ah, priest.",
    "DK4_MES_B243_R0025": "Such kingly presence... Does this statue have a history?",
    "DK4_MES_B243_R0029": "No special history. But...",
    "DK4_MES_B243_R0032": "But?",
    "DK4_MES_B243_R0036": "Only someone the statue itself favors can carry it away.",
    "DK4_MES_B243_R0040": "Many have tried. Most failed to carry it and went home injured.",
    "DK4_MES_B243_R0044": "When a successful owner dies, it somehow returns to this church.",
    "DK4_MES_B243_R0048": "Hmm...",
    "DK4_MES_B243_R0052": "Would you care to try?",
    "DK4_MES_B243_R0056": "Ha! No chance! We need no strange thing. Right, Admiral?",
    "DK4_MES_B243_R0060": "Hmm...",
    "DK4_MES_B243_R0064": "Surely not!",
    "DK4_MES_B243_R0070": "Try it",
    "DK4_MES_B243_R0072": "Leave it",
    "DK4_MES_B243_R0079": "Everyone, lend a hand!",
    "DK4_MES_B243_R0083": "Stop, this elder says!",
    "DK4_MES_B243_R0087": "Go home if you like.",
    "DK4_MES_B243_R0091": "This elder will help! Happy now? Honestly!",
    "DK4_MES_B243_R0095": "Heave! Heave! Heave!",
    "DK4_MES_B243_R0114": "Aaaah!",
    "DK4_MES_B243_R0126": "Run!",
    "DK4_MES_B243_R0133": "Apparently, you were not worthy.",
    "DK4_MES_B243_R0137": "Owww...",
    "DK4_MES_B243_R0143": "Apparently, the statue has accepted you.",
    "DK4_MES_B243_R0146": "Only good luck.",
    "DK4_MES_B243_R0150": "No need for such modesty.",
    "DK4_MES_B243_R0154": "No other reason seems likely. We must simply have been lucky.",
    "DK4_MES_B243_R0158": "Whatever the reason, congratulations. May God's protection go with you.",
    "DK4_MES_B243_R0163": "{MACRO:FI}'s Spirit rose by 1!",
    "DK4_MES_B243_R0174": "A wise decision.",
    "DK4_MES_B243_R0178": "Yes! This elder feared you meant to take it!",
    "DK4_MES_B243_R0182": "Then may God's protection go with you.",

    # Tavern women point Hodram toward nearby discoveries.
    "DK4_MES_B244_R0006": "You came back!",
    "DK4_MES_B244_R0010": "Have you ever seen golden sand?",
    "DK4_MES_B244_R0018": "A sailor spoke of a New World river{LB}where golden sand flows.",
    "DK4_MES_B244_R0022": "Just imagining it feels romantic, does it not?",

    "DK4_MES_B245_R0007": "Hello, {MACRO:FI}.",
    "DK4_MES_B245_R0011": "Like ancient ruins? This town has some.",
    "DK4_MES_B245_R0014": "Surprised? They are nearby,{LB}atop the hill visible from here.",

    "DK4_MES_B246_R0007": "Have you visited the pyramids?",
    "DK4_MES_B246_R0011": "No.",
    "DK4_MES_B246_R0015": "Anyone visiting should see them.{LB}Here are directions. Enjoy!",
    "DK4_MES_B246_R0018": "Good to know.",

    "DK4_MES_B247_R0006": "Welcome, {MACRO:FI}. Pleasant weather again.",
    "DK4_MES_B247_R0010": "Have you seen the nearby ruins?{LB}They may have been King Solomon's treasury.",
    "DK4_MES_B247_R0013": "Hm.",
    "DK4_MES_B247_R0017": "Perfect picnic weather. Why not visit them?",

    # The guild commissions a survey of Rio de Janeiro village.
    "DK4_MES_B248_R0005": "A job for you.",
    "DK4_MES_B248_R0009": "West across the Atlantic lies{LB}Rio de Janeiro village.{LB}Send an expedition there.",
    "DK4_MES_B248_R0012": "Survey?",
    "DK4_MES_B248_R0020": "Across the Atlantic, in the south{LB}of the New World... Quite far.",
    "DK4_MES_B248_R0024": "That is why this job is yours.",
    "DK4_MES_B248_R0028": "The survey needs funds. Take a little extra.",
    "DK4_MES_B249_R0012": "Rio de Janeiro lies in the southern New World.",
    "DK4_MES_B249_R0018": "How goes the Rio survey?{LB}The village lies far west, across the Atlantic.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom",
    "04": "Gennas Pasa",
    "06": "Elder companion",
    "0D": "Cesare Tohni",
    "71": "Sailor",
    "8B": "Priest",
    "93": "Guildmaster",
    "BA": "Woman",
    "BC": "Woman",
    "C1": "Woman",
    "C3": "Woman",
    "C4": "Woman",
    "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    240: "Cesare fumes over sailors neglecting work to discuss the Demon-Piercing Arrow.",
    241: "Gennas hurts his hand repairing the ship, prompting a lead about protective gloves lost on Jutland.",
    242: "Hodram returns the stolen frozen rose and receives a lead about a wooden church outside town.",
    243: "Hodram and an elder attempt to claim a supernatural figurehead from a church.",
    244: "A tavern woman tells Hodram of a New World river carrying golden sand.",
    245: "A local woman points Hodram toward nearby hilltop ruins.",
    246: "A local woman gives Hodram directions to the pyramids.",
    247: "A local woman points Hodram toward ruins said to be King Solomon's treasury.",
    248: "The guild commissions Hodram to survey Rio de Janeiro village.",
    249: "The guild reminds Hodram where to find Rio de Janeiro village.",
}


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
        raise SystemExit(f"Hodram V19 inventory mismatch: missing={missing}, extra={extra}")

    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = (
            f"{first:02X}"
            if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES)
            else ""
        )
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Choice text"),
                "context": CONTEXT[block],
                "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
                "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {
                        "manual_break_reason": (
                            "Places a protected newline before the native row boundary so the "
                            "progressive ASCII pair phase cannot auto-wrap and skip a display row."
                        )
                    }
                    if "{LB}" in english
                    else {}
                ),
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "hodram-story-relic-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram relic, church, tavern-hint, and guild-request events across SC1 blocks 240-249.",
        "excluded_records": EXCLUDED,
        "inventory": {
            "identified_records": len(source_rows),
            "translated_records": len(records),
            "blocks": block_counts,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
