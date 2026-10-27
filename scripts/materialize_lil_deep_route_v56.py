from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v56.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    5: ("The Li elder confirms Lil's full name.", "{MACRO:FI} {MACRO:FA}?"),
    9: ("Lil confirms it.", "Yes."),
    13: ("The elder has heard about Lil and asks her to follow.", "Heard about you. Come with me."),
    18: ("A mysterious woman welcomes Lil to her house.", "Welcome to my home."),
    21: (
        "The elder questions the woman's trust in Westerners, including Hodram and now Lil.",
        "Admiral, you baffle me. Hodram, now this girl... Why do you put so much faith in Westerners?",
    ),
    24: ("The woman says her judgment is sound and Lil deserves their trust.", "Trust me. She deserves our trust."),
    28: ("The woman admits that Lil seems somewhat reckless.", "A little reckless, perhaps."),
    31: ("The elder finds the woman's unusual confidence in Lil surprising.", "You trust her that much? That's rare for you."),
    35: (
        "Lil demands to know why she was summoned so far when she has little time to spare.",
        "Hey! You brought us all this way. What do you want? We're busy!",
    ),
    47: ("Fernando also demands an explanation.", "Yeah! Get to the point."),
    53: ("The woman acknowledges their impatience.", "Of course."),
    56: ("The woman says she summoned Lil to discuss Kuhn.", "We brought you here because of Kuhn."),
    60: ("Lil asks why Kuhn has come up.", "Kuhn? Why bring him up?"),
    63: ("The woman says plainly that Kuhn is exploiting Lil.", "To be blunt, Kuhn is using you."),
    75: ("Christina is shocked by the claim.", "Using us? That's absurd!"),
    90: ("Al angrily objects to the woman's accusation.", "What's she saying?"),
    97: ("The woman warns Lil that Kuhn will harm her and urges her to cut ties.", "He'll hurt you eventually. Cut ties with him now."),
    101: ("Lil asks what the woman means.", "What do you mean?"),
    105: ("Lil defends Kuhn as a trusted ally who has worked with her until now.", "Kuhn's our ally! We've trusted each other all this time!"),
    117: ("Carlo agrees with Lil.", "Yes!"),
    124: ("Lil rejects a stranger's right to accuse her ally.", "Who are you to lecture me?"),
    127: ("Lil demands that the woman finally identify herself.", "Who are you? Tell us your name!"),
    131: ("The woman introduces herself as Maria Huamei Li.", "Yes, of course. Maria Huamei Li."),
    134: ("Lil recognizes the Li surname.", "Li? You mean..."),
    146: ("Gerhard is astonished that this is the head of the Li family.", "So this woman heads the Li family..."),
    158: ("Lil asks if Maria belongs to the Li family she knows of.", "The Li family?"),
    162: ("Maria confirms it and says she came to warn Lil.", "Yes. And you must hear my warning."),
    165: ("Lil questions the warning.", "What?"),
    170: ("Lil accuses the Li family of sending assassins to kill her.", "The Li family! You sent killers after me. Cowards!"),
    174: ("Maria is confused by the accusation about assassins.", "Assassins? What do you mean?"),
    186: ("Christina cannot believe Maria would deny the attack.", "After that, you deny it?"),
    192: ("Lil says a Li assassin attacked and badly injured her.", "Don't play dumb! Your killer attacked me. The wounds were real!"),
    204: ("Carlo calls the attack a dirty trick.", "That's right. A dirty trick!"),
    211: ("Maria asks why Lil believes the assassin worked for her.", "Why assume the killer was my man?"),
    215: ("Lil says the fleeing assassin dropped the Li family crest.", "He dropped the Li crest as he fled. Some fool!"),
    219: ("Maria attributes the planted crest and attack to Kuhn.", "Kuhn did this. That villain would stoop to it."),
    222: ("Lil condemns Maria for blaming Kuhn for her own act.", "Blaming Kuhn for your own deed? That's low!"),
    229: ("Maria says Lil does not know Kuhn's true nature.", "You don't know the real Kuhn."),
    232: ("Lil praises Kuhn as a merchant trying to help Southeast Asians.", "He wants to help Southeast Asia! He's a fine merchant!"),
    244: ("Janus says they are working together toward a noble goal.", "Yes! Our noble goal takes hard work!"),
    251: ("Maria says that is only Kuhn's public image and asks what he has done for townspeople.", "That's for show. What has he done for the townspeople?"),
    255: ("Maria says life has grown harder under Kuhn's control.", "Life under Kuhn has only grown harder for them."),
    259: ("Lil insists this is a lie she would have heard about.", "That's a lie! We'd have heard."),
    262: ("Maria says Kuhn uses wealth and power to manipulate information.", "He uses money and power to control the news."),
    266: ("Lil struggles to accept Maria's account.", "No... You're lying. You have to be!"),
    269: ("Maria says Kuhn first expands his power by cooperating with people like Lil.", "He starts by working with people like you to gain power..."),
    273: ("Kuhn later disposes of those allies and keeps the enlarged territory.", "Then he gets rid of them, keeping the territory they helped him win."),
    285: ("Ian realizes Kuhn may have trapped their group.", "So we've been set up...?"),
    292: ("Lil demands proof and refuses to believe Kuhn is evil without it.", "This is all nonsense! Show me proof that Kuhn is evil! You have none. We won't believe you!"),
    295: ("Maria addresses Lil by name and warns that Kuhn eliminates his allies.", "{MACRO:FI}! Your life is in danger! Kuhn gets rid of allies when he's done with them!"),
    298: ("Lil realizes she may be Kuhn's next target.", "Then... could he come after me?"),
    309: ("Manuel recognizes the gravity of the situation.", "Oh dear... this is serious!"),
    315: ("Maria says Lil may resist the truth but will eventually see it.", "You may not want to believe me. But it's true. You'll see."),
    319: ("Lil is shaken by the thought that Kuhn is a villain.", "Kuhn... evil?"),
    323: ("Maria suggests seeking Kuhn's son if Lil wants proof.", "Still unsure? Then find Kuhn's son."),
    327: ("Lil asks whether Kuhn has a son.", "Kuhn has a son?"),
    331: ("Maria says Kuhn disowned his son and urges Lil to learn why.", "He disowned his son. Learn why."),
    335: ("Lil lacks a lead on where to begin looking.", "But where...?"),
    339: ("Maria tells Lil to go to Batavia.", "Go to Batavia."),
    342: ("Lil agrees to investigate in Batavia while remaining wary of Maria.", "Batavia, then. Still not sure about you, but we'll go."),
    346: ("Lil asks if the meeting is over and says she is leaving.", "That's all? Then we're leaving."),
    363: ("Fernando says they must go see the truth for themselves.", "We have to go and see the truth ourselves."),
    371: ("Julian says they must go see the truth for themselves.", "We have to go and see the truth ourselves."),
    377: ("The elder hopes Lil will finally recognize the truth.", "Hope that opens her eyes..."),
    380: ("Maria trusts Lil's intelligence and expects her to uncover the truth.", "She's wiser than we thought. She'll find the truth."),
    384: ("Maria believes Lil and Hodram may be keys to saving Asia.", "She and Hodram may help save Asia."),
    388: ("The elder agrees.", "Yes."),
    392: ("Maria quietly encourages Lil by full name.", "{MACRO:FI} {MACRO:FA}... Stay strong."),
}

SPEAKERS = {
    0x02: "Lil Argot", 0x03: "Maria Huamei Li", 0x04: "Janus Pasha",
    0x07: "Christina", 0x0F: "Carlo", 0x10: "Gerhard",
    0x11: "Al", 0x14: "Fernando Dias", 0x15: "Ian Dukov",
    0x17: "Manuel Almeida", 0x1A: "Julian", 0xFE: "Mysterious woman",
}
EXCLUDED = {"DK4_MES_B147_R0129": "Opaque four-byte reveal event payload (21 46 83 80)."}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    expected = {row_id for row_id in source_rows if row_id.startswith("DK4_MES_B147_")}
    authored = {f"DK4_MES_B147_R{number:04d}" for number in LINES}
    if authored | EXCLUDED.keys() != expected or authored & EXCLUDED.keys():
        raise ValueError(f"B147 coverage mismatch: missing {expected - authored - EXCLUDED.keys()}")
    if source_rows["DK4_MES_B147_R0129"]["source_hex"].upper() != "21468380":
        raise ValueError("B147 R0129 reveal event payload changed")
    records = []
    for number, (source_meaning, english) in LINES.items():
        row_id = f"DK4_MES_B147_R{number:04d}"
        lead = int(source_rows[row_id]["source_hex"][:2], 16)
        if lead == 0x0A:
            # R0021's 108-byte allocation would pad into a blank fifth page
            # with the inherited leading break. Its English fills three safe
            # rows when the source-only blank row is omitted.
            prefix, speaker = ("" if number == 21 else "{LB}"), "Li elder"
        elif lead in SPEAKERS:
            prefix, speaker = f"{{SPEAKER:{lead:02X}}}", SPEAKERS[lead]
        else:
            raise ValueError(f"{row_id}: unexpected presentation lead {lead:02X}")
        literal = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: unsafe literal uppercase renderer byte")
        record = {
            "id": row_id,
            "english": f"{prefix}{english}{{PAD}}",
            "speaker": speaker,
            "context": (
                "At a Li family house, Maria reveals herself to Lil and warns that Antony Kuhn is using her. "
                "Lil blames Li for an earlier assassination attempt, then learns Kuhn may have framed her. "
                "Maria directs Lil to investigate Kuhn's disowned son in Batavia."
            ),
            "source_meaning": source_meaning,
            "localization_note": (
                "Natural English from clean B147 Japanese; preserves exact FI/FA names, alternate companion "
                "reactions, the Li/Kuhn accusation sequence and the Batavia lead. Five source-leading "
                "elder breaks are retained; R0021 omits its blank first row to avoid a padding-created empty page. "
                "The reveal event stays unchanged."
            ),
            "review": {gate: True for gate in ("source", "context", "localization", "naturalness", "formatting")},
        }
        if lead == 0x0A and number != 21:
            record["qa_waivers"] = ["manual-break", "source-leading-linebreak"]
            record["manual_break_reason"] = (
                "The clean source begins with a structural 0A continuation byte; "
                "preserving it protects the inherited entry position."
            )
        if number == 388:
            record["qa_waivers"].append("orphan-final-line")
        records.append(record)
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "All 68 text records in B147; preserves one opaque Maria reveal control.",
        "inventory": {"identified_records": 69, "translated_records": len(records), "blocks": {"147": 68}},
        "excluded_records": EXCLUDED,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records, {len(EXCLUDED)} control excluded")


if __name__ == "__main__":
    main()
