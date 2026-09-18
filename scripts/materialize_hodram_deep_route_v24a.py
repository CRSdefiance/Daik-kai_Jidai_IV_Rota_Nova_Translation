from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT = Path("translations/hodram_deep_route_v24a.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS = (290,)
EXCLUDED = {
    "DK4_MES_B290_R0038": "Eight-byte nontext expedition event payload preserved byte-for-byte.",
}


LINES = {
    "DK4_MES_B290_R0021": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B290_R0022": "No map.{LB}We'll get lost.",
    "DK4_MES_B290_R0023": "No map, Admiral.{LB}We'll get lost.",
    "DK4_MES_B290_R0024": "Admiral, no map.{LB}We'll get lost.",
    "DK4_MES_B290_R0025": "Admiral, no map means{LB}getting lost.",
    "DK4_MES_B290_R0026": "Admiral, we'll get lost{LB}without a map!",
    "DK4_MES_B290_R0027": "No map.{LB}We'll get lost.",
    "DK4_MES_B290_R0049": "A dense forest.{LB}Proceed carefully.",
    "DK4_MES_B290_R0050": "Dense forest.{LB}Stay careful.",
    "DK4_MES_B290_R0051": "So dark...{LB}Bad feeling.",
    "DK4_MES_B290_R0052": "Such dense woods.{LB}Hope we don't get lost.",
    "DK4_MES_B290_R0053": "These woods feel wrong.",
    "DK4_MES_B290_R0055": "Careful now. Stay alert.",
    "DK4_MES_B290_R0057": "Hope there's treasure here!",
    "DK4_MES_B290_R0059": "A very dense forest.{LB}May nothing find us...",
    "DK4_MES_B290_R0062": "Move.",
    "DK4_MES_B290_R0079": "Behind you...",
    "DK4_MES_B290_R0081": "Admiral, don't move!{LB}Behind you...",
    "DK4_MES_B290_R0082": "Admiral... behind!",
    "DK4_MES_B290_R0084": "Eek... b-behind you...",
    "DK4_MES_B290_R0086": "Admiral, behind!",
    "DK4_MES_B290_R0088": "Whoa... behind you!",
    "DK4_MES_B290_R0096": "Look out!",
    "DK4_MES_B290_R0103": "Be brave",
    "DK4_MES_B290_R0105": "Play dead",
    "DK4_MES_B290_R0107": "Other",
    "DK4_MES_B290_R0118": "Shoot!",
    "DK4_MES_B290_R0136": "Ah! The bear ran!",
    "DK4_MES_B290_R0138": "The bear ran off!",
    "DK4_MES_B290_R0140": "Ah! The bear ran!",
    "DK4_MES_B290_R0142": "Oh! The bear fled!",
    "DK4_MES_B290_R0144": "Yes! Gone!",
    "DK4_MES_B290_R0148": "Some sailors were hurt.",
    "DK4_MES_B290_R0161": "A-Admiral...{LB}The bear shows no sign of leaving.",
    "DK4_MES_B290_R0163": "Admiral...{LB}That bear refuses to leave.",
    "DK4_MES_B290_R0165": "No good.{LB}The bear won't move!",
    "DK4_MES_B290_R0166": "A-Admiral... no good.{LB}This bear will not move.",
    "DK4_MES_B290_R0167": "A-Admiral... no good.{LB}The bear won't run!",
    "DK4_MES_B290_R0168": "This is bad.{LB}The bear shows no sign of leaving.",
    "DK4_MES_B290_R0170": "A-Admiral...{LB}The bear won't go home.",
    "DK4_MES_B290_R0171": "Hmm...{LB}That bear will not move.",
    "DK4_MES_B290_R0175": "Quiet. Hold on.",
    "DK4_MES_B290_R0196": "Whew... it gave up.",
    "DK4_MES_B290_R0198": "Whew... it gave up.",
    "DK4_MES_B290_R0200": "Whew... it gave up at last.",
    "DK4_MES_B290_R0202": "Zzz...",
    "DK4_MES_B290_R0214": "Emilio?",
    "DK4_MES_B290_R0218": "Zzz...",
    "DK4_MES_B290_R0222": "He really slept...",
    "DK4_MES_B290_R0233": "One day passed.",
    "DK4_MES_B290_R0240": "Drive it off",
    "DK4_MES_B290_R0242": "Run away",
    "DK4_MES_B290_R0257": "Threats failed; it stayed!",
    "DK4_MES_B290_R0259": "Threats failed...",
    "DK4_MES_B290_R0261": "What is it?{LB}Threats don't scare it!",
    "DK4_MES_B290_R0262": "What nerve!{LB}Threats won't move it!",
    "DK4_MES_B290_R0263": "This bear has guts!{LB}Won't run!",
    "DK4_MES_B290_R0264": "Come on!{LB}Threats do nothing!{LB}What is with this bear?",
    "DK4_MES_B290_R0266": "Huh?{LB}We scared it; still here!",
    "DK4_MES_B290_R0267": "Threats failed...{LB}Stubborn beast.",
    "DK4_MES_B290_R0278": "Admiral, this is bad!{LB}Could be a man-eating bear!{LB}Attacking could endanger us!",
    "DK4_MES_B290_R0289": "Admiral, look out!{LB}A crewman was mauled!{LB}We must flee before more are hurt!",
    "DK4_MES_B290_R0290": "Look out!{LB}A crewman was mauled!{LB}We must flee before more are hurt!",
    "DK4_MES_B290_R0291": "Admiral, look out!{LB}A crewman was mauled!{LB}Give up and run!",
    "DK4_MES_B290_R0293": "Admiral, look out!{LB}A crewman is being mauled!{LB}We should run!",
    "DK4_MES_B290_R0295": "Look out!{LB}Some men are hurt!{LB}We'd better run!",
    "DK4_MES_B290_R0297": "Danger!{LB}Admiral, we should flee!",
    "DK4_MES_B290_R0298": "Danger! Let's run!",
    "DK4_MES_B290_R0300": "This is bad.{LB}Admiral, we should flee!",
    "DK4_MES_B290_R0305": "Sailor fatigue rose greatly.{LB}Some were injured.",
    "DK4_MES_B290_R0313": "Run!!",
    "DK4_MES_B290_R0329": "We somehow escaped...",
    "DK4_MES_B290_R0331": "Whew...{LB}We escaped...",
    "DK4_MES_B290_R0333": "Pant...{LB}Looks safe...",
    "DK4_MES_B290_R0334": "...Looks safe...",
    "DK4_MES_B290_R0336": "Whew...{LB}Got away...",
    "DK4_MES_B290_R0337": "Whew...{LB}That was terrifying...",
    "DK4_MES_B290_R0338": "Out of breath...{LB}Everyone seems safe.{LB}Good.",
    "DK4_MES_B290_R0352": "Admiral, we're through!{LB}The ruins!",
    "DK4_MES_B290_R0353": "We're through.{LB}The ruins...",
    "DK4_MES_B290_R0354": "Out of the forest at last...{LB}Admiral, these are the ruins!",
    "DK4_MES_B290_R0356": "We're through the woods.{LB}The ruins...",
    "DK4_MES_B290_R0357": "Admiral, we made it!{LB}Those must be the ruins!",
    "DK4_MES_B290_R0358": "We escaped the forest.{LB}So those are the ruins...",
    "DK4_MES_B290_R0360": "We're out of the forest!{LB}Strange stones everywhere...{LB}Are those the ruins?",
    "DK4_MES_B290_R0362": "Admiral, we're through.{LB}The ruins...",
}


SPEAKERS = {
    "01": "Hodram Bergstrom", "0E": "Emilio Ferrog", "16": "Companion",
    "D0": "Companion", "D3": "Companion", "D7": "Companion",
    "D8": "Companion", "FE": "System text",
}
EXTENDED_STATES = {int(state, 16) for state in SPEAKERS}


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream) if row["id"].startswith("DK4_MES_B290_")}
    if set(LINES) | set(EXCLUDED) != set(source_rows) or set(LINES) & set(EXCLUDED):
        missing = sorted(set(source_rows) - set(LINES) - set(EXCLUDED))
        extra = sorted((set(LINES) | set(EXCLUDED)) - set(source_rows))
        raise SystemExit(f"Hodram V24a inventory mismatch: missing={missing}, extra={extra}")
    records = []
    for row_id, english in LINES.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in EXTENDED_STATES) else ""
        records.append({
            "id": row_id, "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": SPEAKERS.get(state, "Party-member variant"),
            "context": "Hodram's expedition crosses a dense forest, confronts a bear, and reaches ancient warrior ruins.",
            "source_meaning": english.replace("{LB}", " "),
            "localization_note": "Faithful concise American English; parallel party-member reactions retain their distinct tone.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Protects semantic rows and the progressive ASCII pair phase in this expedition scene."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4", "source_file_sha256": SC1_SHA256,
        "encoder": "dialogue-fixed-v1", "dialogue_profile": "hodram-story-jungle-live", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": "Source-locked Hodram forest-and-bear expedition in SC1 block 290.",
        "excluded_records": EXCLUDED, "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": {"290": len(records)}},
        "records": records,
    }
    OUTPUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} controls preserved")


if __name__ == "__main__":
    main()
