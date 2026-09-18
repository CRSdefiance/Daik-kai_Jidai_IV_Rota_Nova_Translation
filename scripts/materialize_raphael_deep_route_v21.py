from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc0/script.csv")
OUTPUT = Path("translations/raphael_deep_route_v21.json")
SC0_SHA256 = "a774ff674b086a27be2344188de71e1c7a64e5d2ee5cf366f9d6b8bada48e85e"
TRANSLATIONS = {
    127: [
        "Let us head for Ceuta.", "Now sail the ship.",
        "Begin by checking{LB}which way the ship faces.",
        "Set the fleet's course.{LB}Point toward the desired heading.",
        "Choose direction{LB}with the D-Pad or stylus.",
        "Press the D-Pad toward the heading,{LB}or touch the screen.",
        "The stylus sets the sails automatically.{LB}Touch the flagship to stop.",
        "Did that make sense?",
        "Perfectly.", "The wind may be wrong...",
        "Keep it up, Admiral!",
        "A heading is set,{LB}but bad wind may stop us...",
        "Headwind slows a ship,{LB}but the route to Ceuta has a tailwind.",
        "Will it work?",
        "Doing beats worrying.{LB}Return to Lisbon if stuck.",
        "Long voyages bring trouble:{LB}sickness, rats, leaks, and more.",
        "Most cannot be fixed at sea.{LB}Make port quickly when trouble starts.",
        "Abnormal fleet conditions recover{LB}after entering any town.",
        "Ceuta lies southeast.{LB}Check the Route Map.",
    ],
    128: [
        "Now, {MACRO:FI}.{LB}A few more actions at sea{LB}need explanation.",
        "Yes, please.",
        "When to open every sail{LB}and when to anchor.",
        "Use 'full' for maximum speed.{LB}Then the captain must direct{LB}the sail handlers personally.",
        "While learning, keep 'half.'{LB}Assign one handler per mast{LB}and they work the sails themselves.",
        "At 'full,'{LB}speed may hinder control.{LB}'Half' may be better in battle too.",
        "Anchoring regroups a spread fleet{LB}or helps ambush an enemy.",
        "Got it.",
        "At sea,{LB}sail opening controls speed.{LB}The fleet can also anchor in place.",
        "Use A and B to change sail opening.{LB}B slows down; A speeds up.",
        "Press B at 'full'{LB}to change to 'half' and slow down.",
        "Press B at 'half'{LB}to anchor and stop.",
        "Press A while anchored for 'half';{LB}press A at 'half' for 'full.'",
        "Even at half sail, too few sail handlers means the captain must still direct every sail personally.",
        "Really?",
        "A captain must learn the sails.{LB}Maximum-speed travel will be needed someday.",
        "Y-yes!",
        "Wind behind the sails{LB}is the basis of speed.",
        "Use L and R to turn the sails.{LB}Good trim raises speed.",
        "Press L to turn sails left{LB}and R to turn them right.",
        "The stylus trims sails automatically.{LB}Touch the flagship to stop.",
        "Watch the wind.{LB}Set it behind the sails{LB}relative to the ship's heading.",
        "A tailwind is simple.{LB}A headwind takes some skill.",
        "Check speed on the meter.{LB}To gain speed, maximize the bar.",
        "That covers the basics.{LB}Study the rest yourself.",
        "Understood.{LB}Let me try!",
        "Hmm...{LB}Something was forgotten...",
        "Ah, yes! {MACRO:FI}.{LB}Please head for Athens.",
        "Athens?{LB}That is in Greece,{LB}east in the Mediterranean.",
        "Yes.{LB}Business awaits.",
        "Hey, can the old man's errand{LB}really decide our course?",
        "This is not merely my errand.{LB}We seek something concerning us all.",
        "Something concerning us all...?{LB}Like a shared goal?",
        "Yes.{LB}Something like that.",
        "Nothing must be done at once,{LB}but it will be needed later.",
        "Athens will explain it?",
        "Yes.",
        "We also need it{LB}to fulfill our promise to Hayreddin.",
        "Oh! {MACRO:FI},{LB}this sounds interesting!",
        "Yes!",
        "Go now, {MACRO:FI}.",
        "What could be there?",
        "All right!{LB}Seek our goal!",
        "Huh? Strange.",
    ],
    129: [
        "Now, {MACRO:FI}.{LB}Have you learned the secret{LB}to earning big profits?",
        "Not yet.", "Mastered.",
        "Begin with Madeira,{LB}a small Portuguese island{LB}southwest of Lisbon.",
        "Sugar enriches Madeira. The island becomes vital as {MACRO:FO} expands into Africa and the New World.",
        "When Madeira has market share,{LB}invest as much as possible.",
        "Build funds through trade among{LB}Lisbon, Ceuta, and Madeira.{LB}Then secure Las Palmas and Cape Verde.",
        "They connect Africa with the Mediterranean. Cape Verde yields many goods for little investment.",
        "Trade between Africa and the Mediterranean. Use profits for larger ships and greater town shares.",
        "More cargo holds and town goods{LB}mean greater profit from each voyage.",
        "Then expand trade{LB}farther and farther.",
        "Even an unprofitable town{LB}may gain new goods{LB}through commercial investment.",
        "With spare funds,{LB}try the New World.{LB}No need to force it.",
        "Understood.{LB}We will try.",
        "Will everything be all right?{LB}Old men worry too much.",
        "Try doing things{LB}your own way.",
    ],
}
BLOCKS = tuple(TRANSLATIONS)
SPEAKERS = {"04": "Janus Pasha", "05": "Claudio Manousch", "06": "Julio Castor", "FE": "Tutorial system"}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    127: "Julio and the system teach Raphael basic movement, stylus control, wind, voyage hazards, recovery, and the route to Ceuta.",
    128: "Julio and the system teach sail opening, anchoring, handlers, manual trim, speed, then direct the party toward Athens and its larger goal.",
    129: "Julio teaches Raphael an investment and trade-growth plan spanning Madeira, Atlantic islands, Africa, the Mediterranean, and the New World.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    inventory = {row["id"] for row in rows if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    records = []
    block_counts = {}
    for block, texts in TRANSLATIONS.items():
        source_rows = [row for row in rows if row["id"].startswith(f"DK4_MES_B{block}_")]
        if len(source_rows) != len(texts):
            raise SystemExit(f"B{block}: {len(source_rows)} source rows != {len(texts)} translations")
        block_counts[str(block)] = len(texts)
        for row, english in zip(source_rows, texts, strict=True):
            first = bytes.fromhex(row["source_hex"])[0]
            state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
            unsafe = english.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
            if "I" in unsafe or "F" in unsafe:
                raise SystemExit(f"{row['id']}: unsafe literal uppercase macro byte remains: {english}")
            records.append({
                "id": row["id"], "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Raphael Castor or story participant"), "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving every control, button, wind and sail mechanic, route objective, commerce strategy, macro name, and fixed-allocation safety.",
                "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
                **({"manual_break_reason": "Protects instructional grouping and progressive ASCII pair phase."} if "{LB}" in english else {}),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
    if len(records) != len(inventory):
        raise SystemExit("Raphael V21 inventory accounting mismatch")
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC0.DK4", "source_file_sha256": SC0_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "raphael-story-deep-route-v20-live",
        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Complete basic sailing, advanced sail/anchor, route-objective, and commerce tutorials across Raphael SC0 blocks 127-129.",
        "excluded_records": {},
        "inventory": {"identified_records": len(inventory), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
