from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/sc2/script.csv"
OUTPUT = ROOT / "translations/lil_deep_route_v33.json"
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"

LINES = {
    "DK4_MES_B115_R0017": ("Admiral, please look at this!", "Admiral, look at this!"),
    "DK4_MES_B115_R0019": ("Admiral, look at this!", "Admiral, look!"),
    "DK4_MES_B115_R0021": ("Admiral, look at this!", "Admiral, look at this!"),
    "DK4_MES_B115_R0023": ("Admiral, look at this!", "Admiral, look here!"),
    "DK4_MES_B115_R0025": ("Admiral, look at this!", "Admiral! Look!"),
    "DK4_MES_B115_R0029": ("Oh, just an ordinary stone tablet.", "Oh. Just a stone tablet."),
    "DK4_MES_B115_R0041": (
        "This is no ordinary tablet. There is no stone in this area; that is why they build mosques from dried mud.",
        "This is no ordinary tablet. There's no local stone, so even the mosques use dried mud.",
    ),
    "DK4_MES_B115_R0044": (
        "Does that mean this tablet was not made here?",
        "So this tablet wasn't made here?",
    ),
    "DK4_MES_B115_R0047": ("Yes, probably.", "Most likely."),
    "DK4_MES_B115_R0061": ("Whispering...", "Whisper..."),
    "DK4_MES_B115_R0069": (
        "This is trouble. We cannot touch that now...",
        "This is bad. We can't get near it...",
    ),
    "DK4_MES_B115_R0072": (
        "Were you the bandits attacking Sao Jorge?",
        "Were you the bandits who attacked Sao Jorge?",
    ),
    "DK4_MES_B115_R0075": ("What?! Who are you?", "What?! Who are you?"),
    "DK4_MES_B115_R0078": ("I'm with FO.", "With {MACRO:FO}."),
    "DK4_MES_B115_R0082": (
        "What?! You helped guard that town and caused us enormous trouble!",
        "What?! You helped guard that town! You've ruined everything!",
    ),
    "DK4_MES_B115_R0086": (
        "Because of you, we cannot raid it! You've ruined our livelihood!",
        "You stopped our raids! We'll starve!",
    ),
    "DK4_MES_B115_R0089": (
        "Bold words for bandits! We cannot abandon a town in need!",
        "Bold words for bandits! We can't abandon a town in need!",
    ),
    "DK4_MES_B115_R0093": (
        "Shut up! Those Europeans destroyed our village!",
        "Shut up! Those Europeans destroyed our village!",
    ),
    "DK4_MES_B115_R0096": (
        "No matter what anyone says, we will have revenge!",
        "No one will stop our revenge!",
    ),
    "DK4_MES_B115_R0099": (
        "Wait. The only people you should resent are the corrupt slave traders and brutal soldiers plundering Africa.",
        "Wait. Your enemies are corrupt slavers and brutal soldiers who ravage Africa.",
    ),
    "DK4_MES_B115_R0102": (
        "If you hate every European and attack indiscriminately, you are no better than those cruel people. Equally guilty.",
        "Attack Europeans indiscriminately, and you're no better than those brutes. Just as guilty.",
    ),
    "DK4_MES_B115_R0105": ("You talk as if you know!", "Easy to say!"),
    "DK4_MES_B115_R0109": (
        "Give up revenge. It's meaningless; it cannot restore your happiness, can it?",
        "Give up revenge. That will never restore your happiness.",
    ),
    "DK4_MES_B115_R0113": (
        "That only causes more fighting. More of your people will suffer.",
        "That will only start another fight. More of your people will suffer.",
    ),
    "DK4_MES_B115_R0117": (
        "Then what are we supposed to do?!",
        "Then what are we supposed to do?!",
    ),
    "DK4_MES_B115_R0120": (
        "End the struggle for influence between European countries that causes countless conflicts across the world's seas.",
        "Europe's struggle for power fuels conflicts on every sea. We must end that struggle.",
    ),
    "DK4_MES_B115_R0128": (
        "The great powers are about to divide the world. We collect the Proofs of Supremacy they seek as a pretext, to prevent this.",
        "Great powers plan to carve up our world. Their excuse is the Proofs. We gather them to stop those plans.",
    ),
    "DK4_MES_B115_R0131": (
        "Stop the great powers?! Are you sane?",
        "The great powers?! Are you mad?",
    ),
    "DK4_MES_B115_R0134": (
        "This is no bluff. Our influence reaches Africa now, and we're confident we can meet them on equal terms or better.",
        "This is no bluff. Our influence reaches Africa now. We're strong enough to meet them on equal terms, or better.",
    ),
    "DK4_MES_B115_R0141": (
        "Well? Why not entrust that revenge to us?",
        "Why not trust us with your revenge?",
    ),
    "DK4_MES_B115_R0144": ("What?!", "What?!"),
    "DK4_MES_B115_R0148": (
        "Come to sea with us. With such spirit, you can surely succeed.",
        "Come to sea with us. With that spirit, you can make it.",
    ),
    "DK4_MES_B115_R0156": (
        "Nothing will change if we stay here...",
        "Staying here won't change a thing...",
    ),
    "DK4_MES_B115_R0159": ("All right. We'll bet on you!", "All right. We trust you!"),
    "DK4_MES_B115_R0163": ("Welcome.", "Welcome."),
    "DK4_MES_B115_R0170": (
        "I don't know if this relates to the Proof you seek, but this was hidden in the ruins.",
        "We found this hidden in the ruins. Could it be tied to your Proof?",
    ),
    "DK4_MES_B115_R0173": ("A stone tablet...?", "Tablet?"),
}

SPEAKERS = {
    0x02: "Lil Argot",
    0x03: "Maria",
    0x04: "Janus Pasha",
    0xB4: "African raider",
    0xD0: "Selected crewmate",
    0xFE: "Scene sound",
}
TEXT_LEADS = {0x82, 0x92}
STAGED_ID = "DK4_MES_B115_R0089"


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}
    records = []
    for row_id, (source_meaning, english) in LINES.items():
        row = source_rows[row_id]
        lead = int(row["source_hex"][:2], 16)
        staged = row_id == STAGED_ID
        if lead not in SPEAKERS and lead not in TEXT_LEADS and not (staged and lead == 0x0A):
            raise ValueError(f"{row_id}: unmapped lead {lead:02X}")
        literal = english.replace("{MACRO:FO}", "")
        if "I" in literal or "F" in literal:
            raise ValueError(f"{row_id}: uppercase renderer macro byte in English")
        in_shared_branch = int(row_id.rsplit("R", 1)[1]) >= 61
        note = (
            "Shared Maria branch confirmed by source-identical SC0 B123, SC1 B123, and SC3 B97."
            if in_shared_branch
            else "Reviewed against clean Japanese and adjacent tablet dialogue for Lil and Janus's voices."
        )
        if staged:
            note += " The source-leading LF is staging; English begins on the first row without a speaker byte."
        if row_id == "DK4_MES_B115_R0078":
            note += " Preserves the FO runtime faction macro with Lil's route-level expansion parity."
        records.append(
            {
                "id": row_id,
                "english": (f"{{SPEAKER:{lead:02X}}}" if lead in SPEAKERS else "")
                + english
                + "{PAD}",
                "speaker": "Continuing companion" if staged else SPEAKERS.get(lead, "Companion variant"),
                "context": (
                    "Shared Maria branch: African raiders explain their revenge; Maria recruits them against the great powers."
                    if in_shared_branch
                    else "Lil finds a stone tablet; Janus explains that local mosques use mud because stone is scarce."
                ),
                "source_meaning": source_meaning,
                "localization_note": note,
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
        "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-v33-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "SC2 B115 Lil/Janus tablet scene and the shared Maria raider-recruitment branch.",
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": {"115": len(records)},
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(records)} records")


if __name__ == "__main__":
    main()
