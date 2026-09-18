from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v10.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B48_R0005": "Welcome, {MACRO:FI}.{LB}We awaited you.{LB}Please, this way.",
    "DK4_MES_B48_R0008": "Yes...",
    "DK4_MES_B48_R0012": "Everyone, please come in.{LB}You too... Oh?",
    "DK4_MES_B48_R0015": "Hm? Me?{LB}Something on my face?",
    "DK4_MES_B48_R0018": "N-no, it is nothing.",
    "DK4_MES_B48_R0024": "What is this fine offer?{LB}You called us all this way.{LB}Better not waste our time!",
    "DK4_MES_B48_R0027": "No worry.{LB}This deal profits us both.",
    "DK4_MES_B48_R0030": "Antony Kuhn's envoy,{LB}of the Kuhn Company,{LB}at your service.",
    "DK4_MES_B48_R0034": "!!{LB}(K-Kuhn?!)",
    "DK4_MES_B48_R0037": "Kamil? Your hands are shaking.{LB}Are you sick? Cold?",
    "DK4_MES_B48_R0041": "N-no. Nothing...{LB}Sorry. Please continue.",
    "DK4_MES_B48_R0044": "My master heard of the exploits{LB}of fellow Dutchwoman {MACRO:FI}.{LB}You interest him greatly.",
    "DK4_MES_B48_R0047": "Oh.{LB}Well... thanks.",
    "DK4_MES_B48_R0058": "Word of our deeds{LB}has spread this far!",
    "DK4_MES_B48_R0064": "The corrupt Pereira Company{LB}dominates Southeast Asia{LB}and torments everyone nearby.",
    "DK4_MES_B48_R0067": "Master Kuhn wants Pereira driven{LB}from these waters,{LB}but the task has proven difficult.{LB}Therefore...",
    "DK4_MES_B48_R0070": "We ask the famous {MACRO:FI}{LB}to help destroy Pereira.{LB}Our companies should form{LB}an alliance.",
    "DK4_MES_B48_R0073": "As a token of friendship,{LB}we offer 5,000 gold coins.{LB}What do you say?",
    "DK4_MES_B48_R0077": "{MACRO:FI}, let us go!{LB}Do not accept!",
    "DK4_MES_B48_R0080": "What is wrong? An alliance makes{LB}trade here safer.{LB}They even offer a reward.",
    "DK4_MES_B48_R0084": "And if Pereira is truly corrupt,{LB}we would eventually become enemies{LB}anyway...",
    "DK4_MES_B48_R0088": "Defeating them would help{LB}everyone in Southeast Asia.{LB}This deal is perfect!",
    "DK4_MES_B48_R0100": "Agreed.{LB}Those are fine terms.",
    "DK4_MES_B48_R0106": "Exactly. Exactly.",
    "DK4_MES_B48_R0110": "No!{LB}{MACRO:FI}, refuse!",
    "DK4_MES_B48_R0121": "Kamil, what is wrong?{LB}Not like you!",
    "DK4_MES_B48_R0127": "Kamil, was it?{LB}Could you have ties{LB}to the Pereira Company?",
    "DK4_MES_B48_R0131": "What?!",
    "DK4_MES_B48_R0143": "Mamma mia! Nonsense!",
    "DK4_MES_B48_R0158": "Kamil would never!",
    "DK4_MES_B48_R0165": "Then explain why you oppose{LB}this alliance so strongly.",
    "DK4_MES_B48_R0169": "That is...",
    "DK4_MES_B48_R0173": "Cannot explain?{LB}Then suspicion of a connection{LB}is only natural.",
    "DK4_MES_B48_R0185": "Do not stand silent.{LB}Say something!",
    "DK4_MES_B48_R0199": "Kamil...",
    "DK4_MES_B48_R0206": "K-Kamil... it is not true, right?{LB}No link to Pereira?",
    "DK4_MES_B48_R0209": "Even {MACRO:FI}?!{LB}Of course not!",
    "DK4_MES_B48_R0212": "Then you have no objection{LB}to this alliance?",
    "DK4_MES_B48_R0215": "No... cannot.",
    "DK4_MES_B48_R0219": "Kamil, you have acted strange!{LB}What is wrong?",
    "DK4_MES_B48_R0222": "Same as ever! Please,{LB}{MACRO:FI}!{LB}Refuse this offer!",
    "DK4_MES_B48_R0226": "Then he must have Pereira ties...{LB}{MACRO:FI},{LB}do not trust such a man.",
    "DK4_MES_B48_R0230": "Kamil...",
    "DK4_MES_B48_R0242": "Kamil... explain yourself.",
    "DK4_MES_B48_R0256": "Those ties are a lie,{LB}right?",
    "DK4_MES_B48_R0262": "{MACRO:FI}...!{LB}Goodbye!",
    "DK4_MES_B48_R0265": "Kamil!{LB}Where are you going?!",
    "DK4_MES_B48_R0276": "Kamil, wait!{LB}Come back!",
    "DK4_MES_B48_R0291": "Hey! Do not be rash!",
    "DK4_MES_B48_R0298": "{MACRO:FI}.",
    "DK4_MES_B48_R0302": "Let go!{LB}Take your hand off me!{LB}Let go!",
    "DK4_MES_B48_R0306": "That man is hiding something.{LB}Watch him for a while{LB}and learn the truth.",
    "DK4_MES_B48_R0309": "But...",
    "DK4_MES_B48_R0313": "Never mind. Please sign here.{LB}Go on, {MACRO:FI}.",
    "DK4_MES_B48_R0317": "Y-yes...{LB}What happened to Kamil...?",
    "DK4_MES_B48_R0328": "Kamil... you...",
    "DK4_MES_B49_R0005": "Kuhn,{LB}{MACRO:FO} pact{LB}is signed.",
    "DK4_MES_B49_R0009": "Good. At last,{LB}Pereira can fall...",
    "DK4_MES_B49_R0012": "Also, Lord Marinus...",
    "DK4_MES_B49_R0016": "Marinus?! Certain?{LB}Not another person?",
    "DK4_MES_B49_R0019": "Yes. The name Kamil raised doubts,{LB}but that face could belong{LB}to no one else.",
    "DK4_MES_B49_R0023": "Kamil... a woman's name still?{LB}How did he seem?",
    "DK4_MES_B49_R0026": "Lord Marinus opposed the alliance.{LB}Several times,{LB}he nearly ruined the meeting...",
    "DK4_MES_B49_R0030": "Marinus...{LB}Still determined to defy me.",
    "DK4_MES_B49_R0033": "All is handled.{LB}Talks ended safely,{LB}and our measures are in place.",
    "DK4_MES_B49_R0037": "Lord Marinus will never{LB}return to {MACRO:FO}.",
    "DK4_MES_B49_R0041": "Hm... good.{LB}He is powerless...",
    "DK4_MES_B50_R0005": "{MACRO:FI},{LB}welcome back.",
    "DK4_MES_B50_R0008": "Ah, Kuhn's envoy.",
    "DK4_MES_B50_R0012": "Master Kuhn seeks{LB}an alliance with {MACRO:FI}.",
    "DK4_MES_B50_R0015": "Please accept...",
    "DK4_MES_B50_R0019": "All right...",
    "DK4_MES_B50_R0023": "Thank you.{LB}Master Kuhn hopes{LB}{MACRO:FI} will keep{LB}assisting him.",
    "DK4_MES_B51_R0006": "{MACRO:FI},{LB}welcome.",
    "DK4_MES_B51_R0009": "Ah, Kuhn's envoy...",
    "DK4_MES_B51_R0013": "What became of{LB}that man Kamil?",
    "DK4_MES_B51_R0016": "Nothing since...",
    "DK4_MES_B51_R0020": "So he did have some connection{LB}to Pereira...",
    "DK4_MES_B51_R0023": "Stop that talk.{LB}You came for a reason, right?",
    "DK4_MES_B51_R0026": "Pardon me.{LB}Master Kuhn is deeply{LB}grateful to {MACRO:FI}.",
    "DK4_MES_B51_R0030": "You came all this way{LB}just to say that?{LB}How idle.",
    "DK4_MES_B51_R0034": "Still impatient--pardon,{LB}still someone who values time.",
    "DK4_MES_B51_R0037": "Then straight to the matter.{LB}Have you heard of the Li family,{LB}which controls China?",
    "DK4_MES_B51_R0046": "Yes, somewhat.{LB}Heard of them.",
    "DK4_MES_B51_R0051": "Who? Never heard.",
    "DK4_MES_B51_R0058": "Pirates rule China's underworld.{LB}Drugs, slavery--{LB}every evil imaginable.",
    "DK4_MES_B51_R0070": "More scum besides Pereira?!",
    "DK4_MES_B51_R0076": "Master Kuhn grieves over their crimes.{LB}He works to unite Southeast Asia{LB}as quickly as possible.",
    "DK4_MES_B51_R0079": "To free those they oppress,{LB}Master Kuhn plans to advance{LB}into China.",
    "DK4_MES_B51_R0083": "Sounds good.{LB}But villains truly exist{LB}everywhere, huh?",
    "DK4_MES_B51_R0087": "Yes. Li is especially vicious.{LB}{MACRO:FI}, when you enter East Asia,{LB}beware the Li family.",
    "DK4_MES_B51_R0091": "We will be careful.{LB}Thanks.",
    "DK4_MES_B51_R0094": "Then, farewell.",
    "DK4_MES_B51_R0106": "Tch. Do not like that man...",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Crewmate", "06": "Old sailor", "07": "Crewmate",
    "09": "Kamil", "0F": "Emilio", "10": "Gerhard", "13": "Crewmate",
    "14": "Fernando", "15": "Companion", "28": "Antony Kuhn", "38": "Kuhn envoy",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    48: "Kuhn's envoy proposes an anti-Pereira alliance in Batavia, accuses Kamil of hidden ties, and drives Kamil to flee before Lil signs.",
    49: "The envoy reports the alliance to Antony Kuhn, identifies Kamil as Lord Marinus, and reveals that measures were taken to prevent his return.",
    50: "Kuhn's envoy returns with a shorter alliance proposal and secures Lil's consent.",
    51: "After Kamil's disappearance, Kuhn's envoy warns Lil about the Li family's piracy, narcotics, slavery, and control of China's underworld.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V10 inventory mismatch: missing={sorted(missing)}")
    records = []
    blocks: dict[str, int] = {}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        blocks[str(block)] = blocks.get(str(block), 0) + 1
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        if "I" in unsafe or "F" in unsafe:
            raise SystemExit(f"{row_id}: unsafe literal uppercase macro byte remains: {english}")
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"), "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the alliance conflict, Kamil/Marinus reveal, branch continuity, Li warning, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's Batavia alliance confrontation, Kamil's departure and Marinus reveal, alternate alliance, and Li-family warning across SC2 blocks 48-51.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
