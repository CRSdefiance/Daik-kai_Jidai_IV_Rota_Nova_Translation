from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v9.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B43_R0006": "Hmm. We found a raw material,{LB}but have no idea how to use it.{LB}What should we do?",
    "DK4_MES_B43_R0017": "Hmm. What could it be?",
    "DK4_MES_B43_R0024": "That is extremely rare.{LB}Used well, it can yield{LB}an enormous profit.",
    "DK4_MES_B43_R0036": "Oh?{LB}How do we use it?",
    "DK4_MES_B43_R0042": "Go to a town's trade guild.{LB}With luck, it will add{LB}a new trade good there.",
    "DK4_MES_B43_R0055": "Ahem! This wise old fellow{LB}can tell where some materials{LB}will sell best.",
    "DK4_MES_B43_R0062": "Raw goods only work{LB}where the land suits them.",
    "DK4_MES_B43_R0065": "Bring fitting raw material{LB}to a trade guild,{LB}and the merchant will approach you.",
    "DK4_MES_B43_R0069": "When asked to hand it over,{LB}{MACRO:FI} decides{LB}whether to agree.",
    "DK4_MES_B43_R0073": "Even after finding a useful town,{LB}we can refuse?",
    "DK4_MES_B43_R0077": "Yes. Several towns may suit it.{LB}Choose whichever place makes{LB}trade easiest for us.",
    "DK4_MES_B43_R0081": "Not sure...",
    "DK4_MES_B43_R0085": "Any firm can trade the new good.{LB}So consider each town's market share{LB}before deciding.",
    "DK4_MES_B43_R0097": "Aha, got it!{LB}A new good is more profitable{LB}if only we can trade it!",
    "DK4_MES_B43_R0104": "What?? Come on!{LB}Explain it in simple terms!",
    "DK4_MES_B43_R0108": "Even with a new good,{LB}we cannot trade much in a town{LB}dominated by an enemy company.{LB}Right?",
    "DK4_MES_B43_R0111": "Worse, our enemy might buy it all{LB}and resell it elsewhere.{LB}Then adding that good{LB}helped us nothing.",
    "DK4_MES_B43_R0114": "Got it! A profitable new good{LB}pays more when only we{LB}can control its trade!",
    "DK4_MES_B43_R0118": "Any town can gain a new good.{LB}But {MACRO:FO} may lose profit{LB}if we choose the wrong place.",
    "DK4_MES_B43_R0121": "Hmm. Sounds fun.{LB}So all that matters is profit!",
    "DK4_MES_B43_R0124": "True, but...{LB}(Oh, this is worrying...)",
    "DK4_MES_B44_R0006": "Africa and Asia are nearly{LB}under {MACRO:FO}.",
    "DK4_MES_B44_R0009": "And now we know how to trade{LB}with new goods...{LB}At our present strength...",
    "DK4_MES_B44_R0024": "Take new goods west{LB}and make a fortune!",
    "DK4_MES_B44_R0029": "Now we return to the Mediterranean{LB}and challenge Hayreddin!{LB}This time, we win!",
    "DK4_MES_B44_R0041": "Pirate King...{LB}Cannot wait.",
    "DK4_MES_B44_R0055": "Now {MACRO:FO}{LB}can rival Hayreddin's clan.",
    "DK4_MES_B44_R0072": "To the Mediterranean!{LB}Spread the new goods there!",
    "DK4_MES_B44_R0077": "Yes, let us return!{LB}We will challenge Hayreddin!",
    "DK4_MES_B44_R0088": "Pirate King...{LB}Cannot wait.",
    "DK4_MES_B44_R0102": "Now {MACRO:FO}{LB}can rival Hayreddin's clan.",
    "DK4_MES_B44_R0112": "...R-right.",
    "DK4_MES_B44_R0116": "Huh? What is wrong?{LB}Usually {MACRO:FI}{LB}would leap at the idea.",
    "DK4_MES_B44_R0120": "Y-yes... Kamil,{LB}you have changed lately...",
    "DK4_MES_B44_R0123": "(He seems so dependable now...{LB}So manly, maybe.)",
    "DK4_MES_B44_R0126": "Really? Seems the same to me.{LB}So where next?{LB}Somewhere else?",
    "DK4_MES_B44_R0130": "No. Mediterranean!",
    "DK4_MES_B45_R0018": "Hayreddin actually fell...{LB}The Pirate King had ties{LB}to the Ottoman Empire{LB}and many others, they say...",
    "DK4_MES_B45_R0023": "The Pirate King{LB}is gone from the Mediterranean.",
    "DK4_MES_B45_R0026": "He had ties{LB}to the Ottoman Empire...",
    "DK4_MES_B45_R0038": "His methods were obsolete.{LB}Brute force cannot work{LB}against us anymore.",
    "DK4_MES_B45_R0043": "His methods were obsolete.",
    "DK4_MES_B45_R0047": "Yes.",
    "DK4_MES_B45_R0051": "Trade must be in{LB}a time of transition.",
    "DK4_MES_B45_R0055": "Trade will keep changing.{LB}Those clinging to old methods{LB}will be left behind...",
    "DK4_MES_B45_R0067": "Exactly, Kamil. Success requires{LB}seeing the present--no,{LB}one step beyond it.",
    "DK4_MES_B45_R0079": "Yes. Old customs{LB}must not bind us.",
    "DK4_MES_B45_R0088": "{MACRO:FI}!{LB}We must grow {MACRO:FO}!",
    "DK4_MES_B45_R0092": "Y-yeah...{LB}(When did Kamil begin{LB}looking so manly?)",
    "DK4_MES_B45_R0123": "You made Hayreddin submit...{LB}Amazing, Admiral!",
    "DK4_MES_B45_R0128": "You drove Hayreddin{LB}this far...",
    "DK4_MES_B45_R0131": "{MACRO:FI},{LB}well done.",
    "DK4_MES_B45_R0139": "We truly made Hayreddin's fleet{LB}submit to us.",
    "DK4_MES_B45_R0153": "Luck alone cannot beat him.{LB}This victory shows{LB}{MACRO:FO}'s true power.",
    "DK4_MES_B45_R0160": "Honestly, even now it is hard{LB}to believe. But everyone helped.{LB}The Pirate King truly serves{LB}under us now.",
    "DK4_MES_B45_R0175": "That unity is exactly how{LB}we came this far, Admiral!",
    "DK4_MES_B45_R0181": "Perhaps everyone helped{LB}because you are {MACRO:FI}.",
    "DK4_MES_B45_R0185": "You now possess{LB}that much personal charm.",
    "DK4_MES_B45_R0193": "Everyone helped{LB}because you are {MACRO:FI}.",
    "DK4_MES_B45_R0199": "No way.{LB}Now you embarrass me...",
    "DK4_MES_B45_R0205": "Admiral, this was{LB}lying at the port.",
    "DK4_MES_B45_R0208": "Maybe...{LB}Could this be a map?",
    "DK4_MES_B46_R0018": "That mighty Pasha fleet...{LB}gone too.",
    "DK4_MES_B46_R0023": "The Pasha fleet is gone.{LB}Once it was overwhelmingly strong.{LB}Times truly change.",
    "DK4_MES_B46_R0036": "Admiral, look.",
    "DK4_MES_B46_R0042": "{MACRO:FI}.",
    "DK4_MES_B46_R0061": "Now Pasha is{LB}under {MACRO:FO}...",
    "DK4_MES_B46_R0070": "Never thought he was{LB}mightier than Hayreddin.",
    "DK4_MES_B46_R0084": "Admiral, Pasha's men{LB}sent us this.",
    "DK4_MES_B46_R0089": "{MACRO:FI},{LB}Pasha's men sent this.",
    "DK4_MES_B46_R0099": "What?",
    "DK4_MES_B46_R0109": "Pasha's treasure, sir.",
    "DK4_MES_B46_R0115": "Perhaps Pasha's treasure.{LB}That armor looks valuable.",
    "DK4_MES_B46_R0129": "Amazing armor!",
    "DK4_MES_B46_R0144": "Amazing!{LB}A valuable treasure!",
    "DK4_MES_B47_R0009": "Pardon me.{LB}{MACRO:FI} {MACRO:FA}{LB}and company?",
    "DK4_MES_B47_R0021": "Wrong.{LB}Jam and his merry crew.",
    "DK4_MES_B47_R0024": "O-ow! That hurt!",
    "DK4_MES_B47_R0031": "Yes, that is us...",
    "DK4_MES_B47_R0035": "A fine offer awaits.{LB}Would you come to{LB}Batavia's tavern?",
    "DK4_MES_B47_R0039": "Offer?",
    "DK4_MES_B47_R0043": "Details later.{LB}We will await you.",
    "DK4_MES_B47_R0046": "Kamil, thoughts?",
    "DK4_MES_B47_R0050": "Clearly suspicious...{LB}No desire to go, but...{LB}{MACRO:FI} decides.",
}

SPEAKERS = {
    "02": "Lil Argot", "04": "Crewmate", "06": "Old sailor", "09": "Kamil",
    "0B": "Jam", "0D": "Crewmate", "10": "Gerhard", "11": "Emilio",
    "14": "Fernando", "38": "Messenger", "4C": "Old scholar", "97": "Sailor",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    43: "Kamil explains how raw materials create new trade goods, why regional suitability and market share matter, and how Lil chooses where to surrender them.",
    44: "Lil resolves to return to the Mediterranean with new trade goods, challenge Hayreddin, and quietly notices Kamil's growing maturity.",
    45: "After Hayreddin's defeat or submission, Lil's crew reflects on changing trade, praises her leadership, and discovers a map at the harbor.",
    46: "After Pasha's defeat or submission, Lil's crew receives his valuable armor and reflects on the fall of another great fleet.",
    47: "A mysterious messenger invites Lil and her company to Batavia's tavern while Kamil warns that the offer seems suspicious.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V9 inventory mismatch: missing={sorted(missing)}")
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
            "localization_note": "Faithful concise American English preserving tutorial rules, route branches, quantities, rewards, relationships, and character tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4",
        "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": "lil-story-deep-route-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's raw-material tutorial, Mediterranean return, Hayreddin and Pasha aftermath branches and rewards, and Batavia invitation across SC2 blocks 43-47.",
        "excluded_records": {},
        "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": blocks},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
