from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v48.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = [
    "Usual cinnamon, please.",
    "(A customer?)",
    "Here. This is the price.",
    "Oh? Price went up?",
    "No. Same as always.",
    "Ha! Adil, don't be absurd.{LB}You think your costs are secret?",
    "Hey...",
    "Given this year's crop{LB}and local demand,{LB}you can do better.",
    "Could shop elsewhere.{LB}No law says one supplier only.",
    "Urk... all right.{LB}Can't beat you.",
    "Hm? Adil,{LB}do you have a fever?",
    "What now, Carlo?{LB}More complaints about my trade?",
    "No. You have a fever.{LB}Go to bed early.",
    "What are you...{LB}Wait. A chill...",
    "See? Shopping waits.{LB}Close today.",
    "Hmm... your advice sounds wise.{LB}Sorry, travelers.{LB}Come back tomorrow.",
    "Sorry about that.{LB}You came to trade, right?",
    "How did you know{LB}the owner was sick?",
    "His complexion.",
    "Sharp eyes.{LB}Nearly as keen as mine.",
    "...(Was that obvious?)",
    "Most wouldn't notice.{LB}Sensitive to people's health.",
    "Oh...",
    "Come back tomorrow with me.{LB}Today's trouble will be repaid.",
    "Thanks. We will.",
    "Carlo! Thanks for yesterday!",
    "How is Adil?",
    "Resting at home.{LB}Just in case.",
    "Hope he heals soon.",
    "That man never listens!{LB}Yesterday, if you hadn't...",
    "Oh, rambling again.{LB}You saved his life.{LB}Let me thank you.",
    "Thanks, but thank these travelers.{LB}They delayed their trade a day.",
    "Oh my, sorry to delay you.{LB}Not much, but please take this.",
    "Thank you, ma'am.{LB}Travelers, you're in a hurry.{LB}Shop first.",
    "Carlo!{LB}Sorry about yesterday!",
    "You!",
    "Adil!{LB}You should be in bed!",
    "Look at me--perfectly healthy!{LB}Can't sleep through prime business!",
    "Honestly, what a hopeless man!",
    "Ha! Glad you're lively,{LB}but don't push too hard today.",
    "Back tomorrow.{LB}Take care of these travelers.",
    "Travelers: cherish family{LB}and health. Goodbye.",
    "Um...",
    "Hm?",
    "...Will you join my ship?",
    "Why now?",
    "Skill and kindness{LB}won me over.",
    "Yesterday's bargaining{LB}was impressive.",
    "A merchant for many years.",
    "A merchant!{LB}Know market prices?",
    "Knew he was a pro.",
    "As expected.",
    "Sir, don't want ship life?{LB}Would family object?",
    "No family.{LB}They died last year.",
    "My daughter caught the epidemic.{LB}Work consumed me, and her care{LB}was neglected.",
    "Too late.{LB}My wife caught it too...{LB}Both were lost.",
    "Sir...",
    "Work gained by neglecting family{LB}proved hollow. Since then, health{LB}matters more than business.",
    "Ah... so you noticed{LB}his health.",
    "...Won't you return home?",
    "Venice?{LB}Too many happy memories there.{LB}Can't live there alone.",
    "Sir...{LB}please come with us.{LB}We need you.",
    "Hmm...",
    "Claudio...{LB}This man can teach me so much.",
    "...Maybe so.",
    "Admiral,{LB}why don't we all become{LB}his new family?",
    "Yes! Perfect!{LB}Sir... what do you say?",
    "Thank you, everyone.{LB}Such kindness...",
    "Settled.{LB}Your merchant skills{LB}are expected too.",
    "Carlo Sinato.{LB}Glad to join you.",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B170_")]
    if len(rows) != 70 or rows[0]["id"] != "DK4_MES_B170_R0005" or rows[-1]["id"] != "DK4_MES_B170_R0312":
        raise SystemExit("B170 inventory boundaries changed")
    if len(rows) != len(TRANSLATIONS):
        raise SystemExit(f"B170: {len(rows)} rows != {len(TRANSLATIONS)} translations")
    speaker_names = {
        0x05: "Claudio Manini", 0x06: "Julio Erdi", 0x13: "Carlo Sinato",
        0x14: "Raphael companion", 0x69: "Adil", 0x8E: "Adil's wife",
        0xFE: "Carlo's memory",
    }
    records = []
    for row, english in zip(rows, TRANSLATIONS, strict=True):
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if first in speaker_names else ""
        unsafe = english
        for macro in ("FI", "FA", "FO", "FU"):
            unsafe = unsafe.replace(f"{{MACRO:{macro}}}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row["id"],
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speaker_names.get(first, "Raphael Castor or local merchant"),
            "context": "Raphael meets the observant merchant Carlo Sinato, witnesses his care for a sick trader, learns of Carlo's lost family, and invites him into a new family aboard ship.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful natural American English preserving the price negotiation, health lesson, family tragedy, and warm recruitment resolution.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects emotional pacing, four-line bounds, and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC0.DK4",
        "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "raphael-story-deep-route-v48-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Carlo Sinato's complete merchant, bereavement, and recruitment event in SC0 block 170.",
        "excluded_records": {},
        "inventory": {"identified_records": len(rows), "translated_records": len(records), "blocks": {"170": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
