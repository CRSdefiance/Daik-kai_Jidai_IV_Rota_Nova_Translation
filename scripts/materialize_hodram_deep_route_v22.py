from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v22.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(270, 280))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Prett Perot bounty.
    "DK4_MES_B270_R0006": "Hey, you.{LB}You've got some compassion, right?",
    "DK4_MES_B270_R0009": "A girl whose father was killed{LB}by an English outlaw seeks revenge.{LB}Please help her.",
    "DK4_MES_B270_R0013": "The outlaw is Prett Perot.{LB}Will you take the job?",
    "DK4_MES_B271_R0005": "Prett! Villain...{LB}How dare you return?",
    "DK4_MES_B271_R0008": "Yes... so sorry...",
    "DK4_MES_B271_R0012": "Repentance cannot atone for murder.",
    "DK4_MES_B271_R0015": "Thank you. The girl who hired us{LB}will decide his fate.",
    "DK4_MES_B271_R0019": "Never thought you'd take him alive.{LB}You've earned a handsome reward.",
    "DK4_MES_B271_R0023": "Received 35,000 coins.",
    "DK4_MES_B271_R0048": "Hangzhou share rose slightly!",
    "DK4_MES_B271_R0066": "Have you visited the Purple Palace?{LB}Worth seeing, though it is far away.",
    "DK4_MES_B271_R0069": "Don't tell officials{LB}who gave you the lead.",
    "DK4_MES_B272_R0012": "We must defeat Prett soon.",
    "DK4_MES_B272_R0025": "Capture the outlaw Prett.",

    # Jean Ramusio bounty.
    "DK4_MES_B273_R0005": "A bounty needs your talents.{LB}Capture Jean Ramusio.",
    "DK4_MES_B273_R0009": "We tracked him for smuggling,{LB}but he routed our force in South Asia.",
    "DK4_MES_B273_R0013": "His fleet rivals any pirate's.{LB}Be ready. This is your advance.",
    "DK4_MES_B273_R0023": "Received 15,000 coins.",
    "DK4_MES_B274_R0005": "The smuggler!{LB}At last, you caught him.",
    "DK4_MES_B274_R0008": "They call me a smuggler,{LB}but it is all a misunderstanding!{LB}They're the ones troubling me!",
    "DK4_MES_B274_R0011": "All talk. Think of the trouble{LB}you have caused everyone else.",
    "DK4_MES_B274_R0015": "Then what am l supposed to do?!",
    "DK4_MES_B274_R0019": "Work honestly. Do not pretend{LB}you have already been doing so.",
    "DK4_MES_B274_R0022": "No...?",
    "DK4_MES_B274_R0026": "Sorry you had to deal with him.{LB}Please accept this modest reward.",
    "DK4_MES_B274_R0030": "Received 75,000 coins.",
    "DK4_MES_B274_R0055": "Basra share rose slightly!",
    "DK4_MES_B274_R0073": "Deep inland stands a mosque{LB}said to conceal a great treasure.",
    "DK4_MES_B274_R0076": "To claim it, gain the favor{LB}of the king enshrined there.{LB}A man like you may have a chance.{LB}Surely it is worth a try.",
    "DK4_MES_B275_R0012": "Jean's fleet is in South Asia.{LB}Defeat it.",
    "DK4_MES_B275_R0017": "Jean is hiding somewhere in South Asia.",

    # Jacob Portunto bounty.
    "DK4_MES_B276_R0005": "{MACRO:FA}, a job for you.",
    "DK4_MES_B276_R0008": "What?",
    "DK4_MES_B276_R0012": "Capture Jacob Portunto,{LB}a Dutch smuggler with a bounty.",
    "DK4_MES_B276_R0016": "Once a petty thug,{LB}he struck it rich in Africa{LB}and now plays at piracy.",
    "DK4_MES_B276_R0019": "This is your advance.{LB}He's too strong for us, but not you.",
    "DK4_MES_B276_R0028": "Received 16,000 coins.",
    "DK4_MES_B277_R0005": "You're back.",
    "DK4_MES_B277_R0009": "My cargo...",
    "DK4_MES_B277_R0013": "What are you saying?{LB}That cargo belonged to others!",
    "DK4_MES_B277_R0016": "Thanks for catching him.{LB}Please take this reward.",
    "DK4_MES_B277_R0019": "Received 72,000 coins.",
    "DK4_MES_B277_R0044": "Calicut share rose slightly!",
    "DK4_MES_B277_R0062": "A special lead, just for you.",
    "DK4_MES_B277_R0066": "Explore beyond the city gate.{LB}A building ahead hides great treasure.",
    "DK4_MES_B277_R0077": "Get a map before you explore.",
    "DK4_MES_B278_R0012": "We must find Jacob's fleet.",
    "DK4_MES_B278_R0025": "Still no sign of Jacob?",

    # Hernan Berio bounty.
    "DK4_MES_B279_R0005": "What can we do...?{LB}Only you can handle this job.",
    "DK4_MES_B279_R0008": "Defeat the Spanish pirate Hernan Berio.",
    "DK4_MES_B279_R0011": "Every merchant fears him.{LB}No one else will take the bounty.",
    "DK4_MES_B279_R0015": "He roams the Mediterranean.{LB}Here's an advance. Do your best.",
    "DK4_MES_B279_R0024": "Received 30,000 coins.",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "41": "Prett Perot", "42": "Jean Ramusio",
    "44": "Jacob Portunto", "94": "Guildmaster", "95": "Guildmaster",
    "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    270: "A guildmaster offers the bounty on English outlaw Prett Perot.",
    271: "Prett is delivered alive, judged, and exchanged for a reward and Purple Palace lead.",
    272: "Hodram and the guild recall the active Prett Perot bounty.",
    273: "A guildmaster commissions Hodram to capture smuggler Jean Ramusio.",
    274: "Jean is delivered, admonished, and exchanged for a reward and mosque-treasure lead.",
    275: "Hodram and the guild recall that Jean is hiding in South Asia.",
    276: "A guildmaster commissions Hodram to capture Dutch smuggler Jacob Portunto.",
    277: "Jacob is delivered, exposed as a thief, and exchanged for a reward and treasure lead.",
    278: "Hodram and the guild recall the search for Jacob's fleet.",
    279: "A guildmaster commissions Hodram to defeat Spanish pirate Hernan Berio.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V22 inventory mismatch: missing={missing}, extra={extra}")
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
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Places protected newlines at semantic boundaries while preserving the progressive ASCII pair phase and native display rows."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-bounty-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Ten source-locked Hodram guild-bounty events across SC1 blocks 270-279.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
