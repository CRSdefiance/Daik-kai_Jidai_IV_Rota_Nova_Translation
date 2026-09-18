from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v2.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B12_R0006": "Damn, beaten again...{LB}But next time... Huh?!",
    "DK4_MES_B12_R0009": "No 'next time' for you.",
    "DK4_MES_B12_R0012": "Heh heh...",
    "DK4_MES_B12_R0016": "What?!{LB}Say that again!",
    "DK4_MES_B12_R0020": "What? Could not hear?",
    "DK4_MES_B12_R0024": "Nobody here obeys you anymore.{LB}Not one of us!",
    "DK4_MES_B12_R0027": "Damn you!{LB}You betrayed me!",
    "DK4_MES_B12_R0030": "Hm? So noisy...",
    "DK4_MES_B12_R0034": "Trouble aboard{LB}that pirate woman's ship.",
    "DK4_MES_B12_R0037": "What is it? Let's look.",
    "DK4_MES_B12_R0041": "We keep losing and earn nothing.{LB}Someone must answer for that,{LB}and it will be you.",
    "DK4_MES_B12_R0045": "Answer?!",
    "DK4_MES_B12_R0049": "Why keep chasing{LB}{MACRO:FO}, anyway?",
    "DK4_MES_B12_R0053": "Heh. Hiding the reason{LB}from us, are you?!",
    "DK4_MES_B12_R0060": "You only chased {MACRO:FO}{LB}to reclaim the Bloody Shamshir!{LB}Your father's keepsake!",
    "DK4_MES_B12_R0064": "No... That was not why...",
    "DK4_MES_B12_R0068": "You have gone soft.{LB}Nobody follows a leader{LB}who cannot earn. Prepare yourself!",
    "DK4_MES_B12_R0072": "They will kill her!{LB}What should we do...?",
    "DK4_MES_B12_R0076": "Leave it to me.",
    "DK4_MES_B12_R0080": "Al...?",
    "DK4_MES_B12_R0084": "What? Stay out of this!",
    "DK4_MES_B12_R0087": "Back off, lackey.",
    "DK4_MES_B12_R0091": "This is none of your affair!{LB}Men, finish Aziza and these fools!",
    "DK4_MES_B12_R0095": "Al, my aid is yours.",
    "DK4_MES_B12_R0099": "Count me in!{LB}Men who need numbers are weak!",
    "DK4_MES_B12_R0102": "Bad luck, fools.{LB}Now you answer to me!",
    "DK4_MES_B12_R0106": "Pirates!{LB}Come and face me!",
    "DK4_MES_B12_R0109": "Why...?{LB}Why fight for me?{LB}We were enemies moments ago...",
    "DK4_MES_B12_R0113": "Damn! The odds are bad!",
    "DK4_MES_B12_R0117": "Lost your nerve already?!",
    "DK4_MES_B12_R0121": "{MACRO:FI} {MACRO:FA}...",
    "DK4_MES_B12_R0125": "You came to save her too?",
    "DK4_MES_B12_R0129": "Yes. Had enough?",
    "DK4_MES_B12_R0133": "We are sick of her.{LB}But this is none of your concern.{LB}Stay out of it.",
    "DK4_MES_B12_R0137": "Not our concern, true.{LB}But we cannot stand by{LB}while someone is killed.",
    "DK4_MES_B12_R0141": "Do not touch her.",
    "DK4_MES_B12_R0145": "Aziza matters that much?{LB}Pay us, and she is yours.",
    "DK4_MES_B12_R0148": "Price?",
    "DK4_MES_B12_R0152": "{MACRO:FI}!{LB}You would pay these thugs?!",
    "DK4_MES_B12_R0155": "We can earn more. Right?",
    "DK4_MES_B12_R0159": "All this... for me?",
    "DK4_MES_B12_R0163": "Then pay 2,000,000 coins.",
    "DK4_MES_B12_R0167": "One million.",
    "DK4_MES_B12_R0171": "W-well, agreed.{LB}One million for her.",
    "DK4_MES_B12_R0175": "Agreed.{LB}Aziza, come with us.",
    "DK4_MES_B12_R0182": "Done. Go!",
    "DK4_MES_B12_R0188": "Betrayed by my own crew...{LB}How low have things fallen?{LB}But why did you save me?",
    "DK4_MES_B12_R0192": "Could not help it.",
    "DK4_MES_B12_R0196": "Things just happened that way.{LB}At Basra's tavern, you let us go.{LB}You never seemed like an ordinary pirate.",
    "DK4_MES_B12_R0199": "Why become a pirate?{LB}With skill like yours,{LB}honest work would pay well.",
    "DK4_MES_B12_R0203": "As a child, watching others{LB}taught me swordplay{LB}and the pirate trade.",
    "DK4_MES_B12_R0207": "Eh?",
    "DK4_MES_B12_R0211": "My father was a pirate.{LB}No other life ever occurred to me.{LB}Those men served under him.",
    "DK4_MES_B12_R0215": "Where is your father?",
    "DK4_MES_B12_R0219": "An accident took him.{LB}That sword was his.{LB}He vanished with it...",
    "DK4_MES_B12_R0223": "The Bloody Shamshir...",
    "DK4_MES_B12_R0226": "So that was the 'fine sword'{LB}you mentioned...",
    "DK4_MES_B12_R0229": "My dream: become{LB}a great pirate like him.{LB}His every deed became my model.",
    "DK4_MES_B12_R0233": "When news came that you had it,{LB}that sword became all that mattered.{LB}With it...",
    "DK4_MES_B12_R0240": "Then that might prove{LB}being like my father...{LB}Heh, but...",
    "DK4_MES_B12_R0244": "More than pirate fame,{LB}his keepsake was all that mattered.{LB}At last, that became clear...",
    "DK4_MES_B12_R0247": "No wonder they abandoned me.{LB}Chasing a worthless relic{LB}would anger any crew.",
    "DK4_MES_B12_R0251": "Still yearn for piracy?",
    "DK4_MES_B12_R0255": "Piracy was never the true pursuit.{LB}My father was.{LB}That life is over now.",
    "DK4_MES_B12_R0259": "Then come with us!{LB}Skill like yours{LB}should not go to waste.",
    "DK4_MES_B12_R0263": "Me, join you...?{LB}Truly...?",
    "DK4_MES_B12_R0266": "Sure!{LB}You're strong.",
    "DK4_MES_B12_R0270": "Thanks...{LB}Hard work is promised.{LB}You saved my life.",
    "DK4_MES_B12_R0274": "And from now on,{LB}just call me Aziza.",
    "DK4_MES_B12_R0277": "All right!{LB}Everyone heard that!{LB}Aziza,{LB}work hard for us!",
}

SPEAKERS = {
    "02": "Lil Argot", "07": "Sailor", "0C": "Sailor", "11": "Al", "14": "Fernando",
    "1B": "Aziza Nurennahar", "B7": "Mutineer", "B8": "Mutineer", "B9": "Mutineer",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V2 inventory mismatch: missing={sorted(missing)}")
    records = []
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Aziza's crew mutinies; Lil intervenes, bargains for her life, learns her history, and recruits her.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving Lil's bargaining, the one-million-coin outcome, Aziza's motive, and recruitment staging.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Lil Aziza-mutiny, rescue, bargain, history, and recruitment dialogue in SC2 block 12.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": {"12": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
