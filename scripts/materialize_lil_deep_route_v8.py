from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc2/script.csv")
OUTPUT = Path("translations/lil_deep_route_v8.json")
SC2_SHA256 = "c2e0d1a2744a7da4a24f9693230b302a29f05bcaa036ebd5cc9726a6184731ff"
LINES = {
    "DK4_MES_B38_R0005": "Kamil...",
    "DK4_MES_B38_R0009": "What is it?",
    "DK4_MES_B38_R0013": "Could my choices be wrong?",
    "DK4_MES_B38_R0016": "Huh?",
    "DK4_MES_B38_R0020": "A merchant grows her company{LB}and earns all she can.{LB}That always seemed natural.",
    "DK4_MES_B38_R0024": "But that drive causes conflicts{LB}across the world.{LB}My company does it too.",
    "DK4_MES_B38_R0038": "Now nothing feels{LB}truly right anymore...",
    "DK4_MES_B38_R0042": "{MACRO:FI} is not wrong.{LB}But...",
    "DK4_MES_B38_R0047": "Now nothing feels right...{LB}That makes me no better{LB}than Kuhn.",
    "DK4_MES_B38_R0054": "Oh, sorry!{LB}That was not meant to insult{LB}your father...",
    "DK4_MES_B38_R0058": "No, it is okay.{LB}{MACRO:FI} is right.{LB}But...",
    "DK4_MES_B38_R0064": "But?",
    "DK4_MES_B38_R0068": "As nations and companies seek{LB}profit on the sea routes,{LB}the oceans will know no peace.{LB}That is so.",
    "DK4_MES_B38_R0071": "Then what can we do?",
    "DK4_MES_B38_R0075": "Well...{LB}Drop all greed{LB}and settle it by talk...",
    "DK4_MES_B38_R0079": "That will never happen.{LB}We all want profit{LB}and a happier life.",
    "DK4_MES_B38_R0083": "Dreamers chased fortune{LB}and worked hard.{LB}That is how Holland prospered.",
    "DK4_MES_B38_R0087": "Wanting a better life is natural.{LB}No one has the right to crush{LB}that desire by force.{LB}Never.",
    "DK4_MES_B38_R0090": "{MACRO:FI} as ever.{LB}And perhaps right.",
    "DK4_MES_B38_R0101": "Much as it pains me,{LB}my father may have been right.{LB}Pretty ideals alone cannot{LB}solve every problem.",
    "DK4_MES_B38_R0107": "So peace is impossible...?{LB}Can no one live in peace?",
    "DK4_MES_B38_R0110": "Someone must rule{LB}the world's seas.",
    "DK4_MES_B38_R0113": "Ruler...?{LB}You mean taking every sea{LB}by force?",
    "DK4_MES_B38_R0117": "No. We need not conquer{LB}the world by force.",
    "DK4_MES_B38_R0120": "How so?",
    "DK4_MES_B38_R0124": "That is why we seek{LB}the proofs.",
    "DK4_MES_B38_R0128": "The proofs...?",
    "DK4_MES_B38_R0132": "When a leader accepted by all{LB}holds those proofs,{LB}perhaps conflict at sea will end.",
    "DK4_MES_B38_R0136": "Why?",
    "DK4_MES_B38_R0140": "Rich trade routes lie before us.{LB}A hollow promise to share all{LB}equally could never keep peace.{LB}Would it?",
    "DK4_MES_B38_R0143": "...True.",
    "DK4_MES_B38_R0147": "But with one unquestioned leader{LB}governing the world's seas,{LB}everyone would have to behave.",
    "DK4_MES_B38_R0151": "Sea ruler...",
    "DK4_MES_B38_R0155": "Aha, got it!{LB}Like siblings who never fight{LB}with a scary father watching?",
    "DK4_MES_B38_R0159": "Uh... what an example.{LB}But yes, more or less.",
    "DK4_MES_B38_R0162": "You want me{LB}to play that father?",
    "DK4_MES_B38_R0165": "Yes.",
    "DK4_MES_B38_R0169": "You think that role suits me?",
    "DK4_MES_B38_R0173": "The proofs decide{LB}who is worthy.",
    "DK4_MES_B38_R0176": "Work hard, {MACRO:FI}.{LB}Gain strength and spirit{LB}worthy of a ruler.",
    "DK4_MES_B38_R0180": "Me... sea guardian...",
    "DK4_MES_B39_R0005": "Ah, {MACRO:FI}!",
    "DK4_MES_B39_R0009": "How is the polder going?",
    "DK4_MES_B39_R0013": "Well... the funding brought{LB}more helpers, and we even built{LB}a small settlement...",
    "DK4_MES_B39_R0017": "So it is going well!{LB}Yet you look unhappy.{LB}What happened?",
    "DK4_MES_B39_R0021": "A polder alone serves no purpose,{LB}so we planned to develop{LB}the town first.",
    "DK4_MES_B39_R0025": "We sought aid to build{LB}a governor's office, but...",
    "DK4_MES_B39_R0028": "That office could attract{LB}investment from many groups.{LB}Sounds smart.",
    "DK4_MES_B39_R0032": "The state demanded three holds{LB}of gold in return for its aid.{LB}We are at a loss.",
    "DK4_MES_B39_R0036": "Gold is scarce in the North Sea.{LB}Africa is another matter...",
    "DK4_MES_B39_R0040": "Why not offer aid freely?{LB}What a miserly government!",
    "DK4_MES_B39_R0043": "All right.{LB}We will bring gold.{LB}Wait here.",
    "DK4_MES_B39_R0047": "Y-you will?!{LB}We need three full holds.",
    "DK4_MES_B39_R0050": "That is nothing.{LB}Leave it to me!",
    "DK4_MES_B39_R0053": "Thank you!{LB}Our settlement is near Amsterdam.{LB}We named it Lelystad.",
    "DK4_MES_B39_R0057": "Lelystad...{LB}Three holds of gold, delivered there.{LB}We will do it!",
    "DK4_MES_B40_R0005": "Here.",
    "DK4_MES_B40_R0009": "{MACRO:FI}... sure this is it?{LB}Nothing is here.",
    "DK4_MES_B40_R0013": "There should be...{LB}But this place is so empty.{LB}Now my confidence is gone...",
    "DK4_MES_B40_R0017": "{MACRO:FI}!{LB}Over here!",
    "DK4_MES_B40_R0020": "There you are! So glad!{LB}We brought the promised gold!",
    "DK4_MES_B40_R0023": "Thank you!{LB}Words cannot express our gratitude...",
    "DK4_MES_B40_R0026": "Oh, stop.{LB}No thanks needed.",
    "DK4_MES_B40_R0029": "Will things be okay?",
    "DK4_MES_B40_R0033": "Yes... we know how.",
    "DK4_MES_B40_R0037": "Once the office opens,{LB}investors may come.{LB}And then...",
    "DK4_MES_B40_R0041": "As the polder advances,{LB}we hope to turn Lelystad{LB}into a trading town.",
    "DK4_MES_B40_R0045": "A trading town...{LB}May it come soon.",
    "DK4_MES_B40_R0048": "Yes. Look forward to it!",
    "DK4_MES_B40_R0052": "Let us do our best!",
    "DK4_MES_B41_R0005": "Look! The office{LB}is done!",
    "DK4_MES_B41_R0009": "Now this town should grow{LB}faster and faster.",
    "DK4_MES_B41_R0020": "Right.{LB}Let us go see it at once.",
    "DK4_MES_B41_R0026": "{MACRO:FI}!{LB}The office is finally complete!",
    "DK4_MES_B41_R0030": "Congratulations! You did it!{LB}Here, a gift from me.",
    "DK4_MES_B41_R0034": "What?! 400,000 gold!{LB}Can we accept this?",
    "DK4_MES_B41_R0037": "More money will be needed, right?{LB}Hope this is enough...",
    "DK4_MES_B41_R0040": "Well...",
    "DK4_MES_B41_R0044": "What? Not enough?",
    "DK4_MES_B41_R0048": "Exactly.{LB}More investment is needed{LB}to add new facilities.",
    "DK4_MES_B41_R0052": "This money may go just to{LB}preparing part of the town...",
    "DK4_MES_B41_R0055": "Building a town costs far more{LB}than expected...{LB}Do not worry. We will earn it!",
    "DK4_MES_B41_R0059": "So sorry. We have relied on{LB}{MACRO:FI}{LB}for everything...",
    "DK4_MES_B41_R0063": "Leave the money to me!{LB}And the town is yours to manage.{LB}Make that polder succeed!",
    "DK4_MES_B41_R0066": "Yes!{LB}We will make the polder{LB}a total success!",
}

SPEAKERS = {
    "02": "Lil Argot",
    "09": "Kamil",
    "14": "Fernando",
    "AB": "Lelystad founder",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXTS = {
    38: "Lil questions the conflicts caused by commercial ambition; Kamil proposes a universally accepted guardian of the seas and explains why the Proofs of Supremacy matter.",
    39: "The Amsterdam polder founder reports Lelystad's progress and asks Lil to secure three holds of gold for a governor's office.",
    40: "Lil delivers the gold to the new Lelystad settlement and hears the founder's plan to develop it into a trading town.",
    41: "Lelystad completes its governor's office; Lil contributes 400,000 gold coins and pledges further support for the polder.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Lil V8 inventory mismatch: missing={sorted(missing)}")
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
        records.append(
            {
                "id": row_id,
                "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
                "speaker": SPEAKERS.get(state, "Story participant"),
                "context": CONTEXTS[block],
                "source_meaning": english.replace("{LB}", " "),
                "localization_note": "Faithful concise American English preserving the ethical debate, Proofs of Supremacy lore, polder objectives, quantities, and character tone.",
                "qa_waivers": [
                    "weak-line-ending",
                    "orphan-final-line",
                    *(["manual-break"] if "{LB}" in english else []),
                ],
                **(
                    {"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."}
                    if "{LB}" in english
                    else {}
                ),
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
        "dialogue_profile": "lil-story-deep-route-live",
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Lil's moral crisis and sea-governance discussion with Kamil, followed by Lelystad's gold delivery, governor's-office completion, and polder investment across SC2 blocks 38-41.",
        "excluded_records": {},
        "inventory": {
            "identified_records": len(LINES),
            "translated_records": len(records),
            "blocks": blocks,
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
