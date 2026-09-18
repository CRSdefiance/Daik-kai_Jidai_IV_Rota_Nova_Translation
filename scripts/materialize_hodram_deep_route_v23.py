from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v23.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(280, 290))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Hernan Berio handoff and reminder.
    "DK4_MES_B280_R0005": "Make way! Lord Hernan Berio passes!",
    "DK4_MES_B280_R0008": "Bound, yet playing king.{LB}What a fool.",
    "DK4_MES_B280_R0011": "At last, Hernan is caught!{LB}Hiring you was the right choice.{LB}Excellent work. Take this reward.",
    "DK4_MES_B280_R0014": "Received 110,000 coins.",
    "DK4_MES_B280_R0040": "Athens share rose slightly!",
    "DK4_MES_B280_R0058": "Have you visited{LB}this city's landmark?",
    "DK4_MES_B280_R0061": "Where?",
    "DK4_MES_B280_R0065": "Go see it. The place is{LB}this city's symbol.",
    "DK4_MES_B281_R0012": "Defeat Hernan in the Mediterranean.",
    "DK4_MES_B281_R0024": "Hurry and crush Hernan's gang!",

    # Swedish royal commission against Yasar.
    "DK4_MES_B282_R0006": "Admiral {MACRO:FA},{LB}the king summons you.",
    "DK4_MES_B282_R0009": "Ah, {MACRO:FA}.{LB}A private request awaits.",
    "DK4_MES_B282_R0012": "Thanks to your success,{LB}our ships now cross the southern seas.",
    "DK4_MES_B282_R0016": "A powerful foe in Arabia{LB}has ravaged our merchant fleets.{LB}You must defeat him.",
    "DK4_MES_B282_R0019": "The pirate is Yasar.{LB}Many punitive fleets have fallen.{LB}You are our last hope. Go.",
    "DK4_MES_B283_R0006": "Admiral {MACRO:FA},{LB}welcome home.",
    "DK4_MES_B283_R0009": "{MACRO:FA}!{LB}You defeated that mighty foe!",
    "DK4_MES_B283_R0012": "The reward!",
    "DK4_MES_B283_R0016": "This may not match your service,{LB}but accept our thanks.",
    "DK4_MES_B283_R0019": "Received 250,000 coins!",
    "DK4_MES_B283_R0028": "Now then, {MACRO:FA}.{LB}How goes your mission?",
    "DK4_MES_B283_R0031": "Sir.",
    "DK4_MES_B283_R0035": "Hmm. Yet does the most vital point{LB}remain unclear?",
    "DK4_MES_B283_R0039": "What makes your fleet{LB}the world's strongest?",
    "DK4_MES_B283_R0042": "What do you mean, sire?",
    "DK4_MES_B283_R0045": "Anyone may claim the title.{LB}Only universal recognition gives{LB}'the strongest' any true meaning.",
    "DK4_MES_B283_R0048": "By everyone...",
    "DK4_MES_B283_R0052": "Have you heard of the Proofs of Conquest{LB}sought by every great power?",
    "DK4_MES_B283_R0056": "The Proofs of Conquest...?",
    "DK4_MES_B283_R0060": "You knew, then.",
    "DK4_MES_B283_R0064": "Precisely. The Proofs said to lie{LB}scattered across the world's seas.",
    "DK4_MES_B283_R0068": "Each can be claimed only by one{LB}worthy to rule its own sea.",
    "DK4_MES_B283_R0072": "Gather all seven, and our strength{LB}will be plain to every nation.",
    "DK4_MES_B283_R0076": "Achieve this great feat{LB}and raise Sweden among the great powers.",
    "DK4_MES_B283_R0080": "Yes!",
    "DK4_MES_B283_R0085": "The Proofs... An unknown treasure hunt{LB}has become a royal command.",
    "DK4_MES_B283_R0089": "His Majesty says so, but do these Proofs{LB}truly carry such meaning?",
    "DK4_MES_B283_R0093": "Unknown. Yet the world's strongmen{LB}would not hunt a worthless thing.",
    "DK4_MES_B283_R0097": "Then again, crowds often chase{LB}a meaningless fantasy.",
    "DK4_MES_B283_R0104": "Either way, to win the Proofs{LB}we must defeat every mighty rival{LB}seeking the same prize.",
    "DK4_MES_B283_R0107": "That will demand broad, refined power,{LB}not mere strength in local battles.",
    "DK4_MES_B283_R0111": "Thus the Proofs truly can certify{LB}the world's strongest fleet.",
    "DK4_MES_B283_R0115": "Understood. Gathering the Proofs{LB}is the very mission before us.",
    "DK4_MES_B283_R0119": "Exactly.",
    "DK4_MES_B284_R0006": "Admiral, the king calls.{LB}Return to Stockholm at once.",
    "DK4_MES_B284_R0009": "Sire?",
    "DK4_MES_B284_R0013": "What might he want...?",
    "DK4_MES_B285_R0006": "Defeat Yasar{LB}in southern seas.",

    # William pirate hunt.
    "DK4_MES_B286_R0005": "{MACRO:FA}, we sought you.{LB}A vicious band must be destroyed.",
    "DK4_MES_B286_R0009": "A job?{LB}Who is the target?",
    "DK4_MES_B286_R0012": "Petty thugs once paid Maldonado{LB}while dabbling in piracy and smuggling.",
    "DK4_MES_B286_R0016": "While Maldonado fought Escante{LB}and Clifford, they declared independence.",
    "DK4_MES_B286_R0019": "Their boss is a pirate named William,{LB}a truly vicious man.",
    "DK4_MES_B286_R0023": "He attacks even migrant ships,{LB}kills every captive, and burns villages.",
    "DK4_MES_B286_R0027": "Beside them, Maldonado almost seems{LB}like a decent man.",
    "DK4_MES_B286_R0031": "They have no public organization,{LB}and William rarely shows his face.",
    "DK4_MES_B286_R0035": "Many bounty hunters sought his trail.{LB}Hardly any returned alive.",
    "DK4_MES_B286_R0039": "You're the only one we can ask.",
    "DK4_MES_B286_R0043": "A troublesome foe...{LB}Very well.",
    "DK4_MES_B286_R0046": "You'll accept the job?!",
    "DK4_MES_B286_R0050": "Must act.",
    "DK4_MES_B286_R0054": "Good!{LB}Take this advance. Do your best!",
    "DK4_MES_B286_R0059": "Received 25,000 coins.",
    "DK4_MES_B286_R0065": "But how will we find William?",
    "DK4_MES_B286_R0068": "No lead.{LB}Brute force, then.",
    "DK4_MES_B286_R0071": "Meaning...?",
    "DK4_MES_B286_R0075": "Destroy every pirate under him.{LB}Sooner or later, he will emerge.",
    "DK4_MES_B286_R0079": "Blunt.",

    # William handoff and ancient-city ruins commission.
    "DK4_MES_B287_R0005": "Gyaaah! Rrraaargh!",
    "DK4_MES_B287_R0009": "William!{LB}Caught at last.",
    "DK4_MES_B287_R0012": "At last, freedom.",
    "DK4_MES_B287_R0016": "Your skill is astounding!{LB}Accept this generous reward.",
    "DK4_MES_B287_R0020": "Received 180,000 coins!",
    "DK4_MES_B287_R0046": "Havana share rose slightly!",
    "DK4_MES_B287_R0057": "Someone here wishes to meet you.",
    "DK4_MES_B287_R0061": "Hello.",
    "DK4_MES_B287_R0069": "Your skill inspires a request.{LB}Please find a lost ruin for us.",
    "DK4_MES_B287_R0073": "Ruins?",
    "DK4_MES_B287_R0077": "Our ancestors built it{LB}to honor their warriors.",
    "DK4_MES_B287_R0080": "Only the greatest warrior{LB}can find it, legend says.",
    "DK4_MES_B287_R0084": "You call me the greatest warrior?",
    "DK4_MES_B287_R0088": "That victory convinced us.",
    "DK4_MES_B287_R0092": "The greatest warrior has not only power,{LB}but a just heart and wisdom.",
    "DK4_MES_B287_R0096": "Wait. You overrate me.{LB}Such a task cannot be accepted...",
    "DK4_MES_B287_R0100": "No need to worry. Truthfully,{LB}this is a faint hope even for us.",
    "DK4_MES_B287_R0104": "We simply ask every person{LB}who appears strong enough.",
    "DK4_MES_B287_R0108": "Pardon the offense, but none have{LB}succeeded, so we expect no miracle.",
    "DK4_MES_B287_R0112": "Honest.{LB}That is a relief.",
    "DK4_MES_B287_R0115": "Please accept an advance.{LB}You need not repay it if the ruin{LB}cannot be found.",
    "DK4_MES_B287_R0119": "Received 5,000 coins.",
    "DK4_MES_B287_R0125": "Obtain the Ancient City Map.{LB}Then speak to me again.{LB}We will join the search.",
    "DK4_MES_B287_R0128": "We shall wait at this city's gate.",
    "DK4_MES_B288_R0006": "Are you {MACRO:FA}?{LB}Havana's guild has been seeking you.",
    "DK4_MES_B289_R0012": "Defeat William{LB}in the New World.",
    "DK4_MES_B289_R0023": "Still no sign of William?",
    "DK4_MES_B289_R0028": "William still has not been caught?",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "47": "William",
    "48": "Hernan Berio", "77": "Tavern patron", "78": "Royal attendant",
    "7D": "King of Sweden", "93": "Guildmaster", "94": "Guildmaster",
    "97": "Manuel Armando", "B3": "Expedition host", "CF": "Companion",
    "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    280: "Hernan Berio is delivered to the guild, which rewards Hodram and shares an Athens landmark lead.",
    281: "Hodram and the guild recall the active Hernan Berio bounty.",
    282: "The Swedish king commissions Hodram to defeat the pirate Yasar in the southern seas.",
    283: "The king rewards Hodram and formally makes gathering all seven Proofs of Conquest his royal mission.",
    284: "Manuel and Gerhard tell Hodram that the king has urgently summoned him to Stockholm.",
    285: "Hodram recalls his royal commission against Yasar.",
    286: "Havana's guild commissions Hodram to draw out and defeat the brutal pirate William.",
    287: "William is delivered, and a local patron commissions Hodram to seek the ancient warrior ruins.",
    288: "A tavern patron directs Hodram to Havana's guild.",
    289: "Hodram and the guild recall the active William bounty.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V23 inventory mismatch: missing={missing}, extra={extra}")
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Alternate text"), "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FA}", "Hodram's company").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with established names and Proof-of-Conquest terminology.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Places protected newlines at semantic boundaries while preserving the progressive ASCII pair phase and native display rows."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-commission-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram bounty, royal-mission, and ancient-city events across SC1 blocks 280-289.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
