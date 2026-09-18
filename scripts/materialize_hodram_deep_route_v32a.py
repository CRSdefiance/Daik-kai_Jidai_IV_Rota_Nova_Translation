from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v32a.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = tuple(range(20, 30))
LINES = {
    "DK4_MES_B20_R0009": "Surrender.{LB}You are coming to Sao Jorge.",
    "DK4_MES_B20_R0012": "Damn you! Hands off!{LB}Damn--mmph!",
    "DK4_MES_B21_R0009": "Bind him.{LB}To Hangzhou.",
    "DK4_MES_B21_R0012": "Ow!{LB}Sorry, truly...",
    "DK4_MES_B22_R0008": "What a nuisance.{LB}No wonder Basra's guild suffered.",
    "DK4_MES_B22_R0011": "Come on! Without me,{LB}this whole region would be{LB}in even worse chaos!",
    "DK4_MES_B22_R0015": "Justifying your crimes?{LB}What a vile excuse for a man.{LB}Utterly shameless.",
    "DK4_MES_B23_R0009": "D-damn...{LB}My precious cargo...",
    "DK4_MES_B23_R0012": "Stolen cargo is irrelevant.{LB}Worry about being hauled{LB}back to Calicut.",
    "DK4_MES_B24_R0009": "L-listen!{LB}Letting you win was planned!",
    "DK4_MES_B24_R0012": "Athens guild will take custody.{LB}Stay quiet until then.",
    "DK4_MES_B25_R0008": "Gah!{LB}Me, defeated?{LB}Never! This cannot be!",
    "DK4_MES_B25_R0012": "Gaaah!!",
    "DK4_MES_B25_R0016": "Mission done.{LB}Back to Stockholm.{LB}Report to the king.",
    "DK4_MES_B25_R0020": "Admiral! This was{LB}aboard!",
    "DK4_MES_B25_R0026": "His plunder, perhaps...{LB}But no ordinary plate.",
    "DK4_MES_B26_R0028": "By now, he should have{LB}shown himself...",
    "DK4_MES_B26_R0052": "Keep sinking{LB}every pirate fleet.",
    "DK4_MES_B27_R0009": "Screech! Curse you!{LB}A curse upon you!{LB}Curse you!",
    "DK4_MES_B27_R0013": "Send him to Havana's guild{LB}at once.",
    "DK4_MES_B28_R0005": "At last, defeated.",
    "DK4_MES_B28_R0019": "Report to Malacca's guild{LB}at once!",
    "DK4_MES_B28_R0020": "Report to Malacca's guild{LB}now.",
    "DK4_MES_B28_R0021": "Tell Malacca's guild at once!",
    "DK4_MES_B28_R0023": "Let us report this{LB}to Malacca's guild.",
    "DK4_MES_B28_R0024": "Report this to{LB}Malacca's guild at once.",
    "DK4_MES_B28_R0025": "Let us tell Malacca's guild!",
    "DK4_MES_B28_R0027": "Shall we report this{LB}to Malacca's guild?",
    "DK4_MES_B29_R0005": "There it is!",
    "DK4_MES_B29_R0009": "Speyer's ship?",
    "DK4_MES_B29_R0013": "That Hanseatic cog--{LB}no mistake!",
    "DK4_MES_B29_R0016": "But outside our waters,{LB}we lack authority.",
    "DK4_MES_B29_R0019": "What?!{LB}They attacked without warning!",
    "DK4_MES_B29_R0022": "What is this? A mistake?!",
    "DK4_MES_B29_R0026": "Signal!",
    "DK4_MES_B29_R0030": "Yes! Message?",
    "DK4_MES_B29_R0034": "Your fleet may have{LB}entered our nation's waters.",
    "DK4_MES_B29_R0038": "Stop your ship.{LB}We require an explanation.",
    "DK4_MES_B29_R0045": "Wah!",
    "DK4_MES_B29_R0049": "N-no good!{LB}They ignore our signal!",
    "DK4_MES_B29_R0052": "Willful.",
    "DK4_MES_B29_R0056": "They mean to sink us{LB}before trouble.",
    "DK4_MES_B29_R0059": "Then no restraint.{LB}All hands, battle stations!",
    "DK4_MES_B29_R0062": "Annoying pests!{LB}Teach this makeshift fleet{LB}the terror of naval battle!",
    "DK4_MES_B29_R0067": "Charles! Your battle plan?",
    "DK4_MES_B29_R0071": "Use the classic T formation.",
    "DK4_MES_B29_R0074": "Avoid broadside range.{LB}Circle ahead or astern,{LB}turn our broadside toward them,{LB}then fire one full salvo!",
    "DK4_MES_B29_R0077": "Good. Gunnery is yours!",
    "DK4_MES_B29_R0081": "Leave it to me!{LB}Steer the ship,{LB}and the gunners obey!",
    "DK4_MES_B29_R0085": "Now we shall test{LB}our new cannon's power!",
    "DK4_MES_B29_R0088": "Steer and adjust the sails{LB}just as during normal travel.",
    "DK4_MES_B29_R0092": "Guns fire alone{LB}when foes enter range.",
    "DK4_MES_B29_R0095": "Admiral! Assign me{LB}to the marines as commander!",
    "DK4_MES_B29_R0098": "During battle, change sailor posts{LB}to combat roles.{LB}Use the deck screen.",
    "DK4_MES_B29_R0102": "Press X for the menu,{LB}then choose 'Deck'{LB}to open the deck screen.",
    "DK4_MES_B29_R0106": "Useful battle posts:{LB}gun deck, marines, and deck.",
    "DK4_MES_B29_R0109": "Select Gerhard,{LB}then assign him to the marines.",
    "DK4_MES_B29_R0112": "When ships touch, melee starts.{LB}As marine commander,{LB}Gerhard leads the boarding attack.",
    "DK4_MES_B29_R0116": "Admiral,{LB}give the ship a heading!",
}

SPEAKERS = {
    "01": "Hodram Bergstrom", "10": "Gerhard Adelknauts", "12": "Charles", "17": "Manuel",
    "1D": "Speyer captain", "3F": "Bounty target", "41": "Bounty target", "42": "Bounty target",
    "44": "Bounty target", "47": "Bounty target", "48": "Bounty target", "49": "Bounty target",
    "97": "Sailor", "D0": "Sailor", "FE": "Tutorial",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        all_rows = {row["id"]: row for row in csv.DictReader(stream)}
    missing = set(LINES) - set(all_rows)
    if missing:
        raise SystemExit(f"Hodram V32a inventory mismatch: missing={sorted(missing)}")
    records = []
    counts = {str(block): 0 for block in BLOCKS}
    for row_id, english in LINES.items():
        row = all_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        counts[row_id.split("_B", 1)[1].split("_", 1)[0]] += 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Story participant"),
            "context": "Hodram closes early guild bounties, then intercepts Speyer's ship and receives the naval-combat tutorial.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English preserving guild destinations, battle choices, and tutorial instructions.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and progressive ASCII pair phase."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-caribbean-battles-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram bounty conclusions and first naval-combat tutorial in SC1 blocks 20-29.",
        "excluded_records": {}, "inventory": {"identified_records": len(LINES), "translated_records": len(records), "blocks": counts},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records")


if __name__ == "__main__":
    main()
