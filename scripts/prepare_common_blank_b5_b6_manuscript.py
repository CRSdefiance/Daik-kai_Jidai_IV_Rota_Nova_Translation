"""Restore complete native B5/B6 report and crew-warning groups."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    345: ("And so their many legends will be passed down to each new generation...", "Leaving many legends behind, the subject will continue to be spoken of by subsequent new generations; an ending narration continuation."),
    346: ("%s refused to accept the letter.", "The substituted recipient refused receipt of the personal/diplomatic letter."),
    368: ("They seem to want closer relations.", "It appears the other party wishes to deepen friendly relations."),
    369: ("Someone's schemes seem to be harming our relations with %s!", "An unidentified person's plotting appears to be lowering friendship with the substituted party."),
    370: ("%s and %s have begun fighting!", "The first and second substituted parties have started fighting."),
    371: ("The plan seems to have failed.", "The plan appears to have failed."),
    373: ("Market share has fallen.", "Market share has declined."),
    374: ("The rumor wasn't taken seriously.", "The rumor was not believed or taken seriously."),
    375: ("In %s, a broker for %s received the letter.", "In the first substituted city, a broker/intermediary belonging to the second substituted party received the letter."),
    376: ("Will you pay?", "Asks whether the player will pay."),
    377: ("Seized %s's market share.", "The substituted party's market share was taken away."),
    407: ("Aaaah! Admiral, there are rats everywhere! Don't let them eat my food!", "A frightened, youthful speaker cries that there are many rats, addresses the admiral, and protests at the prospect of rats eating their food."),
    408: ("Admiral, the ship is infested with rats! Our food is in danger!", "An emphatic, formal crew warning: the ship is full of rats and the food supply is threatened."),
    514: ("Admiral, the sailors are growing restless. We'd best call at a port.", "An older, measured voice says sailor dissatisfaction is rising and recommends a temporary port call."),
    515: ("Admiral! The sailors are all in a bad mood. Let's put into port already. I'm scared!", "A youthful, frightened speaker says the sailors are all ill-tempered and urges a port call; they express fear."),
    516: ("I'm fed up! I'll make you head for port, even if I have to use force!", "An angry sailor has reached the limit of their patience and threatens to force the ship to head toward a town."),
    519: ("This is bad... The sailors are about to explode with anger. Admiral, what should we do?", "A worried, informal voice says the sailors' dissatisfaction is about to erupt and asks the admiral what to do."),
    520: ("Admiral, this is serious! The angry sailors are about to resort to force! What should we do?", "An alarmed, polite voice says angry sailors are about to use force and asks what to do."),
    534: ("...Admiral, let's put into port soon. There's no telling what will happen next.", "A hesitant crew voice urges an early call at some port; the next outcome is unknown."),
    535: ("...Admiral, we have to put into port. I feel sorry for the sailors.", "A hesitant, informal voice insists on a port call and expresses sympathy for the sailors."),
    539: ("What a relief... But everyone's still on edge. Admiral, we'd better put into port soon.", "Relief is tempered by the realization everyone is still irritable; advises the admiral to call at a port promptly."),
    540: ("They've calmed down this time, but there's no telling what will happen next. We'd best put into port soon.", "A measured, formal voice says the sailors quieted down this time, but next time is uncertain; recommends a prompt call at some port."),
}


REVISIONS = {
    345: "Its many legends will live on, passed down to each new generation...",
    375: "In %s, a broker acting for %s received the letter.",
    407: "Aaah! Admiral, so many rats! Don't eat my food!",
    408: "Admiral, rats are all over the ship! Our food is in danger!",
    515: "Admiral! The sailors are all grumpy. Let's go into port. I'm scared!",
    516: "I can't take this anymore! I'll force you to head for port!",
    520: "Admiral, this is serious! The angry sailors are about to use force! What should we do?",
    535: "...Admiral, we must put into port. I feel sorry for the sailors.",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v106_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {5, 6}}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B5/B6 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        if message_id == 345:
            gloss = "The Age of Discovery, identified in the previous message, leaves many legends and continues to be recounted to each succeeding generation; an ending narration continuation."
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Report narrator" if message_id < 407 else "Crew warning voice",
            "context": f"Independent native message {message_id}, COMMON B{source.block} R{source.record_index}; ending/report or rat/morale warning. Packed neighbors are separate messages, often voice variants.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source English retains uncertainty, recipients, argument order, threat, hunger/food danger, rising anger, fear, relief, sympathy and recommended timing. Port calls express the source town calls naturally in nautical context. Voice variants remain distinct without invented names or kinship. Ending narration retains its trailing pause. Reserved I/F use existing full-width Latin glyphs. Native repack and all previews require review.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b5_b6_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B5/B6 entries; formatting pending")


if __name__ == "__main__":
    main()
