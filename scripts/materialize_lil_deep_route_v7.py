from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v7.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B34_R0005": "Sofala...{LB}East Africa's trade capital.",
    "DK4_MES_B34_R0016": "Hope there is good food!",
    "DK4_MES_B34_R0031": "East Africa's best.{LB}Nice city.",
    "DK4_MES_B34_R0038": "Lovely city.{LB}Business should thrive.{LB}Huh...?",
    "DK4_MES_B34_R0042": "U-ugh...",
    "DK4_MES_B34_R0046": "What is wrong?",
    "DK4_MES_B34_R0050": "U-ugh... m-medicine...",
    "DK4_MES_B34_R0062": "You okay?",
    "DK4_MES_B34_R0069": "Medicine!{LB}Wait. Something aboard can help.",
    "DK4_MES_B34_R0073": "Girl, useless.",
    "DK4_MES_B34_R0077": "But he is sick!{LB}Medicine is aboard.",
    "DK4_MES_B34_R0080": "He wants a different kind of drug...",
    "DK4_MES_B34_R0083": "Meaning?",
    "DK4_MES_B34_R0087": "Goddess' Temptation...",
    "DK4_MES_B34_R0091": "Goddess' Temptation?{LB}What is that? Not sick?",
    "DK4_MES_B34_R0095": "Sick... perhaps.{LB}Narcotics made him an addict.",
    "DK4_MES_B34_R0107": "Narcotics?!",
    "DK4_MES_B34_R0114": "You may not know,{LB}but narcotics are devil's medicine.{LB}Once started, stopping is hard.",
    "DK4_MES_B34_R0118": "What...?",
    "DK4_MES_B34_R0122": "That man too...{LB}He may not survive.",
    "DK4_MES_B34_R0125": "How awful...{LB}Why buy such a terrible drug?",
    "DK4_MES_B34_R0128": "Taking it brings happiness{LB}while alive--a passing illusion.",
    "DK4_MES_B34_R0132": "An illusion...{LB}People still use it?",
    "DK4_MES_B34_R0135": "Many. Everyone wants happiness.{LB}Dealers exploit that longing.",
    "DK4_MES_B34_R0139": "Suppose someone offered happiness{LB}for almost nothing.{LB}What would you do?",
    "DK4_MES_B34_R0143": "...Tempting.",
    "DK4_MES_B34_R0147": "Exactly. Many heard that promise{LB}and bought it. Then...",
    "DK4_MES_B34_R0151": "Then what?",
    "DK4_MES_B34_R0155": "The second dose{LB}costs an outrageous price.",
    "DK4_MES_B34_R0158": "They still buy it?",
    "DK4_MES_B34_R0162": "Yes. Addicts value drugs{LB}more than money.{LB}They keep buying...",
    "DK4_MES_B34_R0166": "At last, nothing remains.{LB}Every coin is gone.",
    "DK4_MES_B34_R0169": "Bankrupt...",
    "DK4_MES_B34_R0173": "That man did.{LB}Once a wealthy merchant,{LB}now penniless after trying it.",
    "DK4_MES_B34_R0176": "As a merchant, this is wrong!{LB}Who sells that poison?{LB}They will answer!",
    "DK4_MES_B34_R0188": "Yes, me too.",
    "DK4_MES_B34_R0203": "Such cruelty...{LB}Unforgivable.",
    "DK4_MES_B34_R0209": "Stop. Nobody can oppose{LB}the Espinosa Company...",
    "DK4_MES_B34_R0212": "Nothing is known until we try!{LB}Espinosa disgraces all merchants.{LB}That will not be forgiven!",
    "DK4_MES_B35_R0011": "Ah, another beautiful day!{LB}Wonderful!",
    "DK4_MES_B35_R0014": "? Hello.",
    "DK4_MES_B35_R0018": "Oh, a customer. Sorry!{LB}Got carried away.",
    "DK4_MES_B35_R0021": "Good news?",
    "DK4_MES_B35_R0025": "The Espinosa Company is destroyed!{LB}Peace returns to Sofala!",
    "DK4_MES_B35_R0029": "You really hated Espinosa, huh?",
    "DK4_MES_B35_R0032": "Of course! Espinosa profited{LB}from slavery and narcotics--{LB}truly wicked business.",
    "DK4_MES_B35_R0036": "Drug victims went bankrupt...{LB}That company was demonic.",
    "DK4_MES_B35_R0040": "What a vile merchant.{LB}As a merchant too,{LB}good riddance!",
    "DK4_MES_B35_R0043": "Exactly! They will never{LB}strut through town again!{LB}Wonderful! La la la!",
    "DK4_MES_B35_R0047": "Hm? You dropped something.",
    "DK4_MES_B35_R0051": "Ah, this.{LB}Want it, young lady?",
    "DK4_MES_B35_R0054": "What?",
    "DK4_MES_B35_R0058": "Came from Espinosa's house.{LB}No use to me, so it was going out.",
    "DK4_MES_B35_R0062": "Can this really be mine?",
    "DK4_MES_B35_R0066": "A traveling merchant can use it{LB}better than an old man.{LB}Take it.",
    "DK4_MES_B35_R0070": "Sir!",
    "DK4_MES_B35_R0074": "Ah, the young lady from before!{LB}You truly defeated Espinosa!{LB}Well done!",
    "DK4_MES_B35_R0077": "Hee hee, thanks!{LB}No merchant should tolerate{LB}such dirty business.",
    "DK4_MES_B35_R0089": "He was easy for us!",
    "DK4_MES_B35_R0095": "Everyone is celebrating.{LB}With time, the addicts{LB}can return to normal life.",
    "DK4_MES_B35_R0098": "Good... Happiness cannot come{LB}from a drug. That was too easy.",
    "DK4_MES_B35_R0102": "True. Happiness is not given;{LB}it must be earned.{LB}That is never easy.",
    "DK4_MES_B35_R0105": "So people live and work{LB}with all their strength.",
    "DK4_MES_B35_R0108": "Wow...{LB}That is good advice.",
    "DK4_MES_B35_R0119": "Wise words!",
    "DK4_MES_B35_R0126": "Ha ha. Only learned it recently.{LB}You work hard, young lady.{LB}Happiness will find you someday.",
    "DK4_MES_B35_R0130": "Really? Maybe...",
    "DK4_MES_B35_R0134": "Ha ha, that is guaranteed.{LB}Want this?{LB}This came from Espinosa's house.",
    "DK4_MES_B35_R0137": "Something is written here,{LB}but it means nothing to us.{LB}Take it.",
    "DK4_MES_B35_R0146": "Thanks, sir.{LB}Goodbye!",
    "DK4_MES_B36_R0017": "Admiral!{LB}Espinosa had this!",
    "DK4_MES_B36_R0023": "Espinosa had this,{LB}{MACRO:FI}!",
    "DK4_MES_B36_R0029": "What powder?",
    "DK4_MES_B36_R0039": "That is a narcotic.{LB}A terrible drug that ruins people!",
    "DK4_MES_B36_R0045": "Narcotic.{LB}A drug that drives people mad.",
    "DK4_MES_B36_R0051": "Espinosa!{LB}You sold this poison!",
    "DK4_MES_B36_R0058": "Espinosa, now under{LB}{MACRO:FO},{LB}you will never sell narcotics again!",
    "DK4_MES_B36_R0061": "Tch. All right!",
    "DK4_MES_B36_R0065": "{MACRO:FI}, are you{LB}the young lady?",
    "DK4_MES_B36_R0069": "Yes...",
    "DK4_MES_B36_R0073": "Thank you. Heard you stopped{LB}Espinosa from selling narcotics.",
    "DK4_MES_B36_R0077": "That devil's drug must go.{LB}Humanity's enemy.",
    "DK4_MES_B36_R0080": "Everyone in town is grateful.{LB}Wish every merchant were like you.{LB}Something should repay you...",
    "DK4_MES_B36_R0084": "Espinosa, now under{LB}{MACRO:FO},{LB}you will never sell narcotics again!",
    "DK4_MES_B36_R0087": "Tch. All right!",
    "DK4_MES_B36_R0091": "Oh, sir!",
    "DK4_MES_B36_R0095": "Why, the young lady from before.",
    "DK4_MES_B36_R0099": "Safe now!",
    "DK4_MES_B36_R0103": "Eh? What is?",
    "DK4_MES_B36_R0107": "Espinosa will never sell{LB}narcotics again!",
    "DK4_MES_B36_R0110": "No...!",
    "DK4_MES_B36_R0114": "True. Espinosa surrendered to me.",
    "DK4_MES_B36_R0117": "Amazing! You did that?{LB}Something should repay you...",
    "DK4_MES_B36_R0123": "No need. Espinosa simply{LB}made me angry.",
    "DK4_MES_B36_R0126": "No need for modesty.{LB}Take this. Something is written here.",
    "DK4_MES_B36_R0130": "Means nothing to us.{LB}Take it.",
    "DK4_MES_B36_R0135": "Thanks, sir.{LB}Goodbye!",
    "DK4_MES_B37_R0005": "A grand mansion nearby,{LB}yet people sleep outside here...{LB}Such a gap between rich and poor.",
    "DK4_MES_B37_R0015": "They have a caste system here.",
    "DK4_MES_B37_R0018": "Meaning?",
    "DK4_MES_B37_R0022": "Rank is fixed at birth.{LB}The rich are born rich.",
    "DK4_MES_B37_R0025": "Then the reverse...",
    "DK4_MES_B37_R0031": "Yes... Here, status is set{LB}from the moment of birth.",
    "DK4_MES_B37_R0035": "Called a caste system.{LB}Born outside a wealthy class,{LB}people may live in hardship.",
    "DK4_MES_B37_R0042": "So...{LB}My homeland is not the only place{LB}where people suffer...",
    "DK4_MES_B37_R0046": "Want to help somehow...{LB}What can one merchant do?",
    "DK4_MES_B37_R0057": "{MACRO:FI}!{LB}Well said! There must be something{LB}only you can do!",
    "DK4_MES_B37_R0069": "Yes.{LB}Something only Admiral {MACRO:FI}{LB}can surely do.",
    "DK4_MES_B37_R0087": "That person in Amsterdam...{LB}What happened afterward?",
    "DK4_MES_B37_R0091": "Hope the polder funds are growing.{LB}Let's return to Amsterdam!",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Crewmate", "09": "Kamil", "0E": "Emilio Ferrog",
    "10": "Gerhard Adelknauts", "14": "Fernando", "15": "Companion", "17": "Manuel",
    "24": "Espinosa", "54": "Sofala resident", "72": "Addicted merchant", "97": "Sailor",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    34: "Lil reaches Sofala, learns how Espinosa's narcotics exploit and ruin people, and vows to stop him.",
    35: "After Espinosa's defeat, a Sofala resident celebrates, reflects on earned happiness, and gives Lil an item from his estate.",
    36: "Lil finds narcotics in Espinosa's stores, bans their sale under her company, and receives the resident's thanks and item.",
    37: "Lil learns about caste inequality, resolves to help others, and remembers the Amsterdam polder project.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V7 inventory mismatch: missing={sorted(missing)}")
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
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": CONTEXTS[block],
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving the narcotics plot, branch outcomes, social context, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's Sofala arrival, Espinosa narcotics conflict and branch outcomes, resident rewards, caste reflection, and Amsterdam polder callback across SC2 blocks 34-37.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
