from __future__ import annotations

import csv
import json
from pathlib import Path

SOURCE = Path("work/sc1/script.csv")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"

BATCHES = {
    135: {
        "output": Path("translations/hodram_stockholm_dock_natural_v2_sc1_b135.json"),
        "scope": "Hodram's first Stockholm dock resupply tutorial (SC1 block 135)",
        "records": {
            "DK4_MES_B135_R0005": ("01", "Hodram Bergstrom", "Manuel, ready to depart?", "Hodram asks Manuel whether departure preparations are complete."),
            "DK4_MES_B135_R0009": ("17", "Manuel", "Not yet, Admiral. We're about to resupply. Your orders?", "Manuel says he is about to load supplies and asks the admiral for instructions."),
            "DK4_MES_B135_R0015": (None, "Hodram Bergstrom", "All right.", "Hodram agrees to direct the resupply operation."),
            "DK4_MES_B135_R0017": (None, "Hodram Bergstrom", "You handle it.", "Hodram delegates the resupply operation to Manuel."),
            "DK4_MES_B135_R0024": ("01", "Hodram Bergstrom", "That hardly requires an order.", "Hodram observes that resupply hardly requires detailed instructions."),
            "DK4_MES_B135_R0028": ("17", "Manuel", "True. Once we request supplies, the crew handles the rest.", "Manuel agrees and says the crew handles everything once told to resupply."),
            "DK4_MES_B135_R0032": ("FE", "Tutorial narration", "Always resupply before sailing. Running out of food and water can destroy the whole fleet.", "The tutorial warns that running out of food and water at sea can wipe out the fleet."),
            "DK4_MES_B135_R0035": ("FE", "Tutorial narration", "We usually fill the hold. Limited funds mean a smaller load.", "The tutorial says resupply normally fills capacity, but limited funds restrict the purchase."),
            "DK4_MES_B135_R0039": ("FE", "Tutorial narration", "To change the water and food ratio, decline supplies and set it again.", "The tutorial says to refuse the initial resupply and configure it again to change the water-to-food ratio."),
            "DK4_MES_B135_R0045": ("17", "Manuel", "Yes, yes. Right away.", "Manuel acknowledges the order and says he will begin immediately."),
        },
    },
    136: {
        "output": Path("translations/hodram_stockholm_market_natural_v2_sc1_b136.json"),
        "scope": "Hodram's first Stockholm trading-post tutorial (SC1 block 136)",
        "records": {
            "DK4_MES_B136_R0005": ("01", "Hodram Bergstrom", "Charles, how was the haul?", "Hodram asks Charles how the captured goods turned out."),
            "DK4_MES_B136_R0009": ("12", "Charles", "Quite well. We're selling it now. Any orders?", "Charles says the haul was good, that it is being sold, and asks for instructions."),
            "DK4_MES_B136_R0015": (None, "Hodram Bergstrom", "All right.", "Hodram agrees to direct the sale."),
            "DK4_MES_B136_R0017": (None, "Hodram Bergstrom", "Don't sell it.", "Hodram orders Charles not to sell the captured goods."),
            "DK4_MES_B136_R0024": ("FE", "Tutorial narration", "Choose Trade, then select the goods to buy or sell.", "The tutorial says to choose Trade and then select the trade goods to purchase or sell."),
            "DK4_MES_B136_R0027": ("FE", "Tutorial narration", "Buy only when cargo space is free. With a full hold, sell goods first to make room.", "The tutorial says goods can be bought only with an empty cargo hold and instructs the player to sell cargo first when necessary."),
            "DK4_MES_B136_R0031": ("FE", "Tutorial narration", "To sell, choose the goods with the D-pad and press A.", "The tutorial explains how to select goods for sale with the directional pad and confirm with A."),
            "DK4_MES_B136_R0035": ("FE", "Tutorial narration", "To buy, choose a local specialty and press A. The selected goods go into the hold.", "The tutorial explains how to select a local specialty to buy and confirms that it enters the cargo hold."),
            "DK4_MES_B136_R0038": ("FE", "Tutorial narration", "After choosing each ship's goods, press X: Done. That completes the trade.", "The tutorial says to press X Done after selecting every ship's purchases and sales, completing the transaction."),
            "DK4_MES_B136_R0044": ("12", "Charles", "Understood. We'll leave it aboard.", "Charles accepts the order not to sell and says the cargo will remain aboard."),
        },
    },
}


def context_for(block: int, row_id: str) -> str:
    if block == 135:
        if row_id.endswith(("R0015", "R0017")):
            return "The player chooses whether Hodram or Manuel will handle the first Stockholm resupply."
        return "Hodram and Manuel review resupply during the first visit to Stockholm's dock."
    if row_id.endswith(("R0015", "R0017")):
        return "The player chooses whether to proceed with selling the captured goods at Stockholm's trading post."
    return "Hodram and Charles review captured cargo and the trading controls at Stockholm's trading post."


def localization_note(row_id: str) -> str:
    if row_id.endswith("R0015"):
        return "A natural affirmative that exactly fills the choice record's ten-byte allocation."
    if row_id.endswith("R0017"):
        return "A concise natural choice that exactly fills the source record's fourteen-byte allocation."
    return "Natural American localization from the clean Japanese; source line breaks are layout evidence and are not copied."


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {row["id"]: row for row in csv.DictReader(stream)}

    for block, spec in BATCHES.items():
        expected = {
            row_id for row_id in source_rows if row_id.startswith(f"DK4_MES_B{block}_")
        }
        authored = set(spec["records"])
        if expected != authored:
            raise SystemExit(
                f"B{block} inventory mismatch: missing={sorted(expected-authored)}, extra={sorted(authored-expected)}"
            )
        records = []
        for row_id, (state, speaker, english, meaning) in spec["records"].items():
            prefix = f"{{SPEAKER:{state}}}" if state else ""
            records.append({
                "id": row_id,
                "english": f"{prefix}{english}{{PAD}}",
                "speaker": speaker,
                "context": context_for(block, row_id),
                "source_meaning": meaning,
                "localization_note": localization_note(row_id),
                "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
            })
        batch = {
            "format": "dk4-ilnk-translation-batch-v1",
            "file_path": "/data/SC1.DK4",
            "source_file_sha256": SC1_SHA256,
            "encoder": "dialogue-fixed-v1",
            "dialogue_profile": "hodram-story-probe",
            "translation_policy": "natural-dialogue-v2",
            "target_locale": "en-US",
            "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
            "scope": spec["scope"],
            "profile_note": "Fixed-allocation companion layer to the existing Hodram opening probe; only already-mapped SC1 presentation states are retained.",
            "inventory": {"block": block, "identified_records": len(records), "translated_records": len(records)},
            "records": records,
        }
        spec["output"].write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {spec['output']}: {len(records)} records")


if __name__ == "__main__":
    main()
