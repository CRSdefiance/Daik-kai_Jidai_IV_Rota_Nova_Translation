from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/hodram_natural_v2_sc2_b66_blocked.json")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"

LINES = {
    "DK4_MES_B66_R0012": "Now that Kuhn Trading, Southeast Asia's largest organization, is gone, we can trade freely here.",
    "DK4_MES_B66_R0016": "All right, let's get to work!",
    "DK4_MES_B66_R0033": "With Kuhn Trading under us, we can trade freely throughout Southeast Asia.",
    "DK4_MES_B66_R0046": "(So you're {MACRO:FI}...",
    "DK4_MES_B66_R0050": "Who are you?!",
    "DK4_MES_B66_R0054": "(Antony Kuhn...",
    "DK4_MES_B66_R0058": "You're Kuhn...",
    "DK4_MES_B66_R0064": "({MACRO:FI}... was it?",
    "DK4_MES_B66_R0067": "You...!",
    "DK4_MES_B66_R0074": "(What happened to Marinus?",
    "DK4_MES_B66_R0078": "Marinus?",
    "DK4_MES_B66_R0088": "No one by that name is with us.",
    "DK4_MES_B66_R0092": "(I see... You don't know.",
    "DK4_MES_B66_R0096": "What are you talking about?",
    "DK4_MES_B66_R0102": "That's Kamil's real name? Kamil already left us.",
    "DK4_MES_B66_R0105": "You know more than I do, don't you? You're his father, right?",
    "DK4_MES_B66_R0109": "(You know how Kamil and I are related?",
    "DK4_MES_B66_R0113": "More or less.",
    "DK4_MES_B66_R0117": "(I see...",
    "DK4_MES_B66_R0124": "(No. Forgive me. I'll be going.",
    "DK4_MES_B66_R0128": "Father!",
    "DK4_MES_B66_R0132": "Kamil...",
    "DK4_MES_B66_R0144": "Kamil, you bastard! Where have you been?!",
    "DK4_MES_B66_R0158": "You're back! I'm so happy!",
    "DK4_MES_B66_R0169": "Kamil, are you all right now?",
    "DK4_MES_B66_R0173": "Yes.",
    "DK4_MES_B66_R0177": "Then I'll be going.",
    "DK4_MES_B66_R0181": "Hodram, thank you for everything!",
    "DK4_MES_B66_R0184": "Don't mention it.",
    "DK4_MES_B66_R0188": "Kamil, where have you been?!",
    "DK4_MES_B66_R0198": "And why did you call him 'Father'? What's going on?!",
    "DK4_MES_B66_R0203": "I looked for you...",
    "DK4_MES_B66_R0211": "Kamil, I owe you an apology. You're really Kuhn's...",
    "DK4_MES_B66_R0217": "Yes... Overijssel is my mother's surname. My real name is Marinus Kuhn. Antony Kuhn is my father.",
    "DK4_MES_B66_R0226": "Marinus Kuhn... Kuhn is Kamil's father...",
    "DK4_MES_B66_R0229": "Yes. Kamil has been my nickname since I was little.",
    "DK4_MES_B66_R0237": "My father was a good man once. When he met my mother, he was only a small-time trader.",
    "DK4_MES_B66_R0241": "They were poor, but Mother said they were happy together every day.",
    "DK4_MES_B66_R0244": "But when Kuhn Trading reached the Spice Islands, the money poured in. Once Father became rich, he changed...",
    "DK4_MES_B66_R0248": "Greed blinded him. Profit became all that mattered, and no method was too dirty...",
    "DK4_MES_B66_R0252": "Mother and I couldn't bear what he'd become.",
    "DK4_MES_B66_R0255": "Kamil...",
    "DK4_MES_B66_R0259": "Everyone around us feared Father. Even our neighbors began avoiding Mother and me...",
    "DK4_MES_B66_R0263": "Mother decided we couldn't live there anymore, so she took me back to the Netherlands.",
    "DK4_MES_B66_R0267": "{MACRO:FI}... I never meant to tell anyone about Father. I especially didn't want you to know.",
    "DK4_MES_B66_R0270": "That's why I opposed you back then... I'm sorry.",
    "DK4_MES_B66_R0280": "Oh... So that's why you were so against it back then...",
    "DK4_MES_B66_R0283": "I didn't know, but I still doubted you... I'm so sorry, Kamil.",
    "DK4_MES_B66_R0289": "No... You were suffering too, Kamil...",
    "DK4_MES_B66_R0295": "Say, {MACRO:FI}... will you let me sail aboard your ship again?",
    "DK4_MES_B66_R0298": "Of course! Things were a mess without you. You'll have to work twice as hard to make up for it!",
    "DK4_MES_B66_R0302": "You haven't changed at all, {MACRO:FI}. You're still such a slave driver.",
    "DK4_MES_B66_R0306": "Well, excuse me!",
    "DK4_MES_B66_R0310": "Ha ha. But that's what makes you {MACRO:FI}.",
    "DK4_MES_B66_R0313": "Kamil... (I'm so glad you came back!)",
    "DK4_MES_B66_R0317": "Hey, Father.",
    "DK4_MES_B66_R0321": "(What is it?",
    "DK4_MES_B66_R0325": "You understand now, don't you? You can make money honestly, just like before.",
    "DK4_MES_B66_R0328": "(Hmph. Perhaps. But I have my own way of doing things.",
    "DK4_MES_B66_R0331": "Father!",
    "DK4_MES_B66_R0335": "(I'll rebuild from scratch. I haven't given up yet.",
    "DK4_MES_B66_R0342": "(...Marinus. Take this. I have no use for it now.",
    "DK4_MES_B66_R0345": "What is it?",
    "DK4_MES_B66_R0349": "(Something I acquired when I was young.",
    "DK4_MES_B66_R0355": "Father... can't you become the kind man you used to be?",
    "DK4_MES_B66_R0359": "(That's impossible.",
    "DK4_MES_B66_R0363": "Why? You and Mother could start over, just like before!",
    "DK4_MES_B66_R0366": "(...Is your mother well?",
    "DK4_MES_B66_R0370": "Yes.",
    "DK4_MES_B66_R0374": "(...Take care of her.",
    "DK4_MES_B66_R0378": "That's not fair! You could go see Mother yourself!",
    "DK4_MES_B66_R0381": "(Adults have their own reasons. Goodbye.",
}

SPEAKERS = {
    "01": "Hodram Bergstrom",
    "02": "Lil Argot",
    "09": "Kamil",
    "0E": "Emilio",
    "14": "Fernando",
    "28": "Antony Kuhn",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = {
            row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B66_")
        }
    if set(rows) != set(LINES):
        raise SystemExit(
            f"B66 inventory mismatch: missing={sorted(set(rows) - set(LINES))}, extra={sorted(set(LINES) - set(rows))}"
        )

    records = []
    for row_id, english in LINES.items():
        source = bytes.fromhex(rows[row_id]["source_hex"])
        prefix = f"{source[0]:02X}"
        records.append(
            {
                "id": row_id,
                "draft_english": f"{english}{{PAD}}",
                "speaker": SPEAKERS[prefix],
                "context": "After Kuhn Trading falls, Lil encounters Antony Kuhn; Kamil returns, reveals his identity as Marinus Kuhn, reconciles with Lil, and confronts his father.",
                "source_meaning": english.replace("{MACRO:FI}", "Lil"),
                "localization_note": "Localized from the clean Japanese as natural American dialogue; manual source wrapping is intentionally discarded.",
                "source_prefix_hex": prefix,
                "source_length": len(source),
                "blocker": "SC2 block 66 speaker/portrait state and cross-route FI expansion are unmapped; byte 0x28 may be a literal thought marker rather than presentation state; this editorial draft is not encodable.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": False,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "route_owner": "Lil Argot",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "draft_status": "source-first-editorial-draft-blocked-unmapped-sc2-b66-control-state",
        "profile_note": "Non-buildable Lil-route draft retained under a historical Hodram filename. SC2 block 66 control state and runtime FI expansion must be mapped before formatting or insertion. The leading 0x28 on Antony's lines may be a literal thought marker, not presentation state.",
        "inventory": {
            "identified_records": 72,
            "translated_drafts": 72,
            "encodable_records": 0,
            "blocked_records": 72,
            "missing_records": 0,
            "blocks": {"66": 72},
        },
        "records": [],
        "blocked_records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} blocked source-first drafts")


if __name__ == "__main__":
    main()
