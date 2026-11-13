"""Restore every remaining blank-owned native group in B15/B16."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    1198: ("%s, %s attacked %s and failed miserably. Serves them right!", "Addresses the first substituted name; the second substituted party attacked the third but failed badly. The speaker gloats that it serves them right."),
    1199: ("Oh, are you leaving already?", "An informal surprised question asking whether the player is departing already."),
    1202: ("Come, let us sing a song of joy.", "A ceremonial invitation to sing a song of joy; no specific named composition is supplied by the source."),
    1203: ("Kneel there. Now... ahem.", "A formal instruction to kneel at that spot, followed by a pause and throat clearing."),
    1209: ("Huh???", "A puzzled, surprised reaction with three question marks."),
    1210: ("Then help with the preparations at once.", "An instruction to promptly help with the preparations."),
    1211: ("Help?", "A brief questioning repetition of help."),
    1212: ("Help, you say?", "A more forceful questioning repetition of the instruction to help."),
    1216: ("...", "A silent pause; this packed neighbor remains an independent message."),
    1217: ("(Ugh, what is this all about?)", "An exasperated internal aside wondering what is going on."),
    1218: ("God is always watching what you do.", "A religious speaker says God always observes the person's actions."),
    1226: ("Pilgrims, are you? Line up there and offer your prayers one at a time.", "Recognizes the visitors as pilgrims and instructs them to line up at that spot and offer prayers in order."),
    1227: ("Then join the circle of dancers.", "A formal suggestion that the visitors join the dancing circle."),
    1233: ("What?!", "A surprised reaction."),
    1234: ("What did you say?!", "An indignant or forcefully surprised reaction."),
    1235: ("Whaaat?!", "A prolonged surprised cry."),
    1236: ("...I guess it can't be helped...", "A pause followed by resigned acceptance that nothing can be done about it."),
    1238: ("(Stomach growls...)", "Parenthetical stomach-growling sound; surrounding reactions concern hunger."),
    1239: ("(Stomach growls...)", "A separate voice's identical parenthetical stomach-growling sound."),
    1240: ("(I'm so hungry...)", "A parenthetical, drawn-out expression of hunger."),
    1242: ("We'll climb the sacred mountain to collect holy water. Is that all right?", "Explains that the group will climb the sacred peak to draw holy water, and asks for agreement."),
    1243: ("Follow me, then. Stay close so you don't get separated.", "Asks the visitors to follow the speaker and avoid being separated from the group."),
    1249: ("A ship's doctor can cure ailments affecting crew members and sailors.", "Having a ship's doctor allows treatment of health problems affecting officers/crew characters and sailors."),
    1250: ("A chief cook saves water and food, and keeps sailors from tiring so easily.", "Having a chief cook conserves water and food and makes sailors less prone to fatigue."),
    1251: ("Crew members assigned here feel refreshed and help keep sailors from tiring.", "Crew characters placed here feel mentally refreshed and also make sailors less prone to fatigue."),
    1252: ("An animal keeper helps your food last longer.", "Having an animal keeper slows the depletion of food."),
    1253: ("A missionary eases sailors' discontent and lets you distribute trade goods in the square.", "Having a missionary resolves sailors' dissatisfaction and enables distribution of trade goods in the public square."),
    1254: ("A strategist lets you plan schemes at the tavern.", "Having a strategist enables planning of schemes at the tavern."),
    1285: ("Lateen sails perform well in headwinds. You can't mount a square sail behind a lateen sail.", "Lateen/triangular sails are strong against headwinds; a square sail cannot be fitted behind a triangular sail. Fresh source translation also replaces the historical donor's unguarded line breaks."),
    1290: ("Admiral, there's a town in sight!", "A polite crew voice reports that a town is visible."),
    1291: ("Admiral, I can see a town!", "An informal youthful crew voice reports a visible town."),
    1292: ("Admiral, I see a town!", "An informal crew voice reports a visible town."),
    1293: ("Admiral, we've got a town in sight!", "A rough, emphatic crew voice reports a visible town."),
    1294: ("Admiral, that looks like a town.", "An older crew voice says that the sight appears to be a town, preserving uncertainty."),
    1299: ("Admiral! %s's fleet is in battle! Shall we help them?", "Reports the substituted party's fleet is engaged in battle and asks the admiral whether to assist."),
    1300: ("Admiral! %s's fleet is fighting! Should we help?", "An informal voice reports the substituted party's fleet is fighting and asks whether to assist."),
    1301: ("Admiral! %s's fleet is in a fight! Want to lend a hand?", "A rough voice reports the substituted party's fleet is fighting and asks whether to lend assistance."),
    1303: ("Admiral! %s's fleet is fighting! Should we give them a hand?", "A youthful voice reports the substituted party's fleet is fighting and asks whether to help."),
    1304: ("%s's fleet is in battle. Shall we lend them a hand?", "An older, polite voice reports the substituted party's fleet is engaged in battle and asks whether to assist; no admiral address in the source."),
    1305: ("Admiral, %s has attacked us!", "A crew report that the substituted party has attacked the speaker's side."),
    1316: ("Admiral, I can see a village!", "An informal voice reports a visible village."),
    1317: ("Admiral, it's a village!", "A rough crew voice identifies the sight as a village."),
    1318: ("Admiral, there's a village.", "An older crew voice identifies the sight as a village."),
    1319: ("Hey, look! There's a village!", "A youthful voice eagerly points out a village; the source does not address the admiral."),
    1350: ("I gave the villagers %s gold coins to thank them for their help.", "A polite report of giving the villagers the substituted number of gold coins in thanks for their assistance."),
    1351: ("They helped us, so I gave the villagers %s gold coins.", "An informal report of giving the villagers the substituted number of gold coins because they helped the party."),
    1352: ("I gave the villagers %s gold coins as thanks for looking after us.", "An informal report of giving the villagers the substituted number of gold coins in thanks for their care/assistance."),
    1353: ("They helped us out, so I handed the villagers %s gold coins as thanks.", "A rough voice reports giving the villagers the substituted number of gold coins as thanks for help."),
    1356: ("I gave the villagers %s gold coins in gratitude for their help.", "An older, polite report of giving the villagers the substituted number of gold coins in gratitude for assistance."),
    1357: ("I cook very well. I'm sure it'll taste good.", "The speaker says they are very good at cooking and expresses confidence the food will be delicious. Simple sentences retain the source's straightforward delivery."),
    1360: ("... (I can't really understand the words.)", "A pause and parenthetical thought that the speaker does not understand the language/words well."),
    1361: ("Yes, that's a lovely sound.", "An approving comment on the pleasing musical tone."),
    1362: ("...That's rather well done...", "A reserved, approving comment that the performance or work is quite good."),
    1363: ("Zzz... Oh, come on, Kamil... Zzz...", "A sleeping voice mutters a mildly exasperated address to Kamil between snores. Existing route spelling is Kamil."),
}


REVISIONS = {
    1285: "Lateen sails handle headwinds well. You can't mount a square sail behind them.",
    1210: "Then start helping us prepare now.",
    1242: "We'll climb the sacred peak and collect holy water. Do you agree?",
    1250: "A chief cook saves water and food and reduces sailor fatigue.",
    1351: "To thank the villagers for helping us, I gave them %s gold coins.",
    1353: "The villagers helped us out, so I gave them %s gold coins as thanks.",
    1360: "... (I don't know this language very well.)",
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    pending = json.loads(Path("work/analysis/common_blank_remaining_v110_source_entries.json").read_text(encoding="utf-8"))
    required = {row["message_id"] for row in pending if row["block"] in {15, 16}} | {1285}
    if required != PROSE.keys():
        raise ValueError("Cover every native neighbor of every missing B15/B16 group")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        english = REVISIONS.get(message_id, english)
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Ceremonial speaker, crew voice or report narrator",
            "context": f"Independent native message {message_id}, COMMON B{source.block} R{source.record_index}; ceremony/reaction, room help, sighting, battle, village or performance report. Every packed neighbor and voice variant is separate.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source prose retains brief reactions, silent pauses, stomach sounds, hesitation, ceremony, holy water, safety instructions, conditional role benefits, town versus village, uncertainty, help questions, gratitude and gold amounts. Gender and fixed identities are not invented for voice variants. Substitution order is source-locked. Stomach growls express the sound's meaning naturally; Kamil uses established spelling. Reserved I/F use existing full-width Latin glyphs. Native repack and all exact-font previews require review.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    Path("translations/common_blank_b15_b16_manuscript_v1.json").write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B15/B16 entries; formatting pending")


if __name__ == "__main__":
    main()
