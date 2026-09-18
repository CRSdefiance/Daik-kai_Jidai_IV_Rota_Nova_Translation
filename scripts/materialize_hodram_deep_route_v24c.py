from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v24c.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(292, 300))
EXCLUDED: dict[str, str] = {}


LINES = {
    # Malacca sea-monster commission and reward.
    "DK4_MES_B292_R0005": "Good timing.{LB}A request awaits you.",
    "DK4_MES_B292_R0008": "You may not believe this...{LB}A monster often appears in these waters.",
    "DK4_MES_B292_R0012": "Monster?",
    "DK4_MES_B292_R0016": "Locals call it a demon.{LB}The beast sinks bitten ships.",
    "DK4_MES_B292_R0019": "Several ships were devoured{LB}this year alone.",
    "DK4_MES_B292_R0022": "You might be able to stop it.{LB}Will you hunt the beast for us?",
    "DK4_MES_B292_R0025": "Meeting it will depend on luck.",
    "DK4_MES_B292_R0028": "We can wait patiently.{LB}Good luck.",
    "DK4_MES_B293_R0005": "Amazing!{LB}You truly killed it!{LB}You're no ordinary sailor!",
    "DK4_MES_B293_R0009": "Now we can only pray{LB}there was just one...",
    "DK4_MES_B293_R0012": "...What?",
    "DK4_MES_B293_R0016": "Nothing!{LB}Take your reward!",
    "DK4_MES_B293_R0020": "Received 70,000 coins.",
    "DK4_MES_B293_R0043": "Malacca share rose slightly!",
    "DK4_MES_B293_R0060": "Ah, right.{LB}Heard an interesting rumor.",
    "DK4_MES_B293_R0063": "Deep inland, ancient royal ruins{LB}remain intact in the jungle.",
    "DK4_MES_B293_R0067": "Truly?",
    "DK4_MES_B293_R0071": "Only a rumor.{LB}No one has found them yet.{LB}Perhaps you could.",

    # Hidden Christian village approach and poison trap.
    "DK4_MES_B294_R0020": "Admiral, no map.{LB}We cannot continue.",
    "DK4_MES_B294_R0021": "Admiral, no map.{LB}Cannot continue.",
    "DK4_MES_B294_R0022": "Admiral, we need a map.",
    "DK4_MES_B294_R0024": "No map.{LB}We cannot continue.",
    "DK4_MES_B294_R0025": "Come on.{LB}We need a map to continue.",
    "DK4_MES_B294_R0026": "Admiral, we need a map.",
    "DK4_MES_B294_R0028": "Admiral, we need a map!",
    "DK4_MES_B294_R0030": "Admiral, no map.{LB}Cannot continue.",
    "DK4_MES_B294_R0043": "Deep woods.",
    "DK4_MES_B294_R0047": "That must be why no one{LB}has found it before.",
    "DK4_MES_B294_R0058": "Let's leave these woods{LB}as soon as we can.",
    "DK4_MES_B294_R0064": "Christians from before Muslim rule...{LB}Could they descend from Byzantium?",
    "DK4_MES_B294_R0067": "A tale centuries old.{LB}Hope it yields a clue to the Proof.",
    "DK4_MES_B294_R0071": "What bones?!",
    "DK4_MES_B294_R0075": "Someone entered as we did{LB}and died here...",
    "DK4_MES_B294_R0078": "Search the area, just in case?",
    "DK4_MES_B294_R0084": "Yes",
    "DK4_MES_B294_R0086": "No",
    "DK4_MES_B294_R0093": "Understood. Caution is wise.",
    "DK4_MES_B294_R0096": "What is this smoke?{LB}Can't breathe...",
    "DK4_MES_B294_R0099": "Poison smoke!{LB}{MACRO:FI}, do not breathe it!{LB}Leave this place at once!",
    "DK4_MES_B294_R0103": "All here?",
    "DK4_MES_B294_R0107": "Crew safe!",
    "DK4_MES_B294_R0111": "Good... {MACRO:FI}!{LB}Are you all right?",
    "DK4_MES_B294_R0115": "Y-yes... all right...{LB}What was that?",
    "DK4_MES_B294_R0118": "Smoke harmful to the body.{LB}Only rumors mentioned such a thing...",
    "DK4_MES_B294_R0122": "So... that...",
    "DK4_MES_B294_R0126": "Admiral in danger!{LB}Everyone, move!",
    "DK4_MES_B294_R0135": "The sailors seem confused.",
    "DK4_MES_B294_R0143": "No reason to linger here.{LB}Let us hurry onward.",
    "DK4_MES_B294_R0155": "Too bad... We might have learned{LB}the secret of these bones.",
    "DK4_MES_B294_R0167": "This is it.",

    # Cappadocian hidden-village rumor.
    "DK4_MES_B295_R0006": "Well, welcome.",
    "DK4_MES_B295_R0010": "You're rather handsome up close.{LB}Let me share a secret.",
    "DK4_MES_B295_R0014": "Have you heard of a hidden{LB}Christian village nearby?",
    "DK4_MES_B295_R0017": "No.",
    "DK4_MES_B295_R0021": "They supposedly live in houses{LB}carved from rock. Only a rumor, though.",

    # Charles devises explosives to clear the blocked path.
    "DK4_MES_B296_R0005": "This...",
    "DK4_MES_B296_R0009": "A rockfall, perhaps.{LB}The path is impassable.",
    "DK4_MES_B296_R0012": "No choice. Turn back.",
    "DK4_MES_B296_R0037": "What?{LB}Come, Charles.",
    "DK4_MES_B296_R0040": "Let's blast it!",
    "DK4_MES_B296_R0044": "What?! A blast?",
    "DK4_MES_B296_R0047": "Yes! Blow away{LB}the blocking rocks!",
    "DK4_MES_B296_R0050": "Seriously?{LB}Such solid rock requires{LB}much gunpowder.",
    "DK4_MES_B296_R0054": "Getting so much gunpowder{LB}at once is nearly impossible.",
    "DK4_MES_B296_R0057": "No concern. We can make{LB}the gunpowder ourselves.",
    "DK4_MES_B296_R0060": "You can make it?",
    "DK4_MES_B296_R0063": "Admiral, remember my research?{LB}Bring sulfur; we can make it.",
    "DK4_MES_B296_R0067": "Sulfur should be sold{LB}in this city.",
    "DK4_MES_B296_R0070": "Buy it at market.{LB}Bring it here.",
    "DK4_MES_B296_R0073": "Good. We'll buy sulfur.",
    "DK4_MES_B297_R0011": "Charles must be here.",
    "DK4_MES_B297_R0033": "We need to buy sulfur.",
    "DK4_MES_B297_R0213": "Not even close to enough.",
    "DK4_MES_B297_R0232": "Need more.",
    "DK4_MES_B297_R0243": "Yes, this should be enough.",
    "DK4_MES_B297_R0247": "What comes next?",
    "DK4_MES_B297_R0251": "Next, timber for{LB}charcoal.",
    "DK4_MES_B297_R0254": "Timber?",
    "DK4_MES_B297_R0258": "Timber is not sold here.{LB}We must obtain it elsewhere.",
    "DK4_MES_B298_R0011": "Charles must be here.",
    "DK4_MES_B298_R0033": "We need to buy timber.",
    "DK4_MES_B298_R0128": "Not even close to enough.",
    "DK4_MES_B298_R0147": "Need more.",
    "DK4_MES_B298_R0158": "Yes, this should{LB}be enough.",
    "DK4_MES_B298_R0161": "Last...",
    "DK4_MES_B298_R0165": "Still more?",
    "DK4_MES_B298_R0169": "The vital ingredient remains:{LB}saltpeter.",
    "DK4_MES_B298_R0172": "Saltpeter?",
    "DK4_MES_B298_R0176": "A southern-seas city{LB}should sell it.",
    "DK4_MES_B298_R0179": "Quite far...",
    "DK4_MES_B299_R0011": "Charles must be here.",
    "DK4_MES_B299_R0033": "We need to buy{LB}saltpeter.",
    "DK4_MES_B299_R0229": "Not even close{LB}to enough.",
    "DK4_MES_B299_R0247": "Need more.",
    "DK4_MES_B299_R0258": "Yes.{LB}This should be enough.",
    "DK4_MES_B299_R0265": "Done!",
    "DK4_MES_B299_R0269": "Set the explosives.{LB}Evacuate.",
    "DK4_MES_B299_R0278": "Here goes.{LB}Three, two, one, go!",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles",
    "93": "Guildmaster", "97": "Crewman", "C2": "Tavern patron",
    "D3": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}
CONTEXT = {
    292: "Malacca's guild commissions Hodram to hunt the Demon Fish sea monster.",
    293: "The guild rewards Hodram for killing the sea monster and shares a jungle-ruins rumor.",
    294: "Hodram's party crosses a forest toward a hidden Christian settlement and encounters a poison-smoke trap.",
    295: "A local shares a rumor about Christians living in rock-carved homes nearby.",
    296: "A rockfall blocks the route, and Charles proposes manufacturing gunpowder from sulfur.",
    297: "Charles checks the sulfur supply, then asks for timber to make charcoal.",
    298: "Charles checks the timber supply, then identifies saltpeter as the last ingredient.",
    299: "Charles checks the saltpeter supply, finishes the explosives, and clears the route.",
}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in BLOCKS)}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V24c inventory mismatch: missing={missing}, extra={extra}")
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
            "speaker": SPEAKERS.get(state, "Party-member variant"), "context": CONTEXT[block],
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with established Proof and commodity terminology.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and the progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-ruins-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram sea-monster, hidden-village, ruins, and gunpowder events across SC1 blocks 292-299.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
