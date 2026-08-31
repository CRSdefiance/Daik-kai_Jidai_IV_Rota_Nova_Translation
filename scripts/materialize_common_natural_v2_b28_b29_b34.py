from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "work/analysis/common_clean_inventory.json"
BASE = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
BATCH = ROOT / "translations/common_natural_v2_b28_b29_b34_safe.json"
BLOCKED = ROOT / "translations/common_natural_v2_b28_b29_b34_blocked.json"
AUDIT = ROOT / "work/analysis/common_b28_b29_b34_entry_audit.json"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"
COUNTS = {28: 82, 29: 62, 34: 72}

# Only records whose clean segment contains one independently addressable line
# are eligible.  The materialized result still has to pass shared-pair-live QA.
DRAFTS = {
    (28, 0): "%s is attacking us! It's the pirate %s!",
    (28, 6): "We won!",
    (28, 7): "We won!",
    (28, 8): "We did it! We won!",
    (28, 10): "Our fleet has been defeated...",
    (28, 11): "They took out our fleet...",
    (28, 12): "Our fleet has been defeated...",
    (28, 13): "Our fleet got beaten...",
    (28, 14): "We have retreated...",
    (28, 16): "Our fleet has retreated...",
    (28, 17): "Our fleet has retreated...",
    (28, 18): "Our fleet has retreated...",
    (28, 19): "Our fleet ran away...",
    (28, 20): "We'll put in at a nearby town and await orders.",
    (28, 21): "Let's put in at a nearby town for now.",
    (28, 22): "Let's put in at a nearby town for now.",
    (28, 23): "We'll put in at a nearby town for now.",
    (28, 24): "No choice. We'll put in at a nearby town.",
    (28, 26): "%s sank!",
    (28, 27): "%s sank!",
    (28, 28): "%s sank!",
    (28, 29): "%s sank!",
    (28, 30): "%s went down!",
    (28, 31): "%s has sunk!",
    (28, 32): "%s has no sailors left!",
    (28, 33): "There are no sailors aboard %s!",
    (28, 34): "%s has no sailors left!",
    (28, 35): "%s hasn't got a single sailor left!",
    (28, 36): "%s has no sailors left!",
    (28, 37): "%s has no sailors left!",
    (28, 38): "%s has no sailors left!",
    (28, 39): "Are you sure? I'll discard %s.",
    (28, 40): "Very well... I'll discard %s.",
    (28, 44): "The flagship is lost! Retreat to %s!",
    (28, 46): "Damn! This cannot end here. You will avenge me!",
    (28, 47): "Damn it! But I won't go down for nothing!",
    (28, 48): "They got me... Just you wait!",
    (28, 50): "I will not end here! You will regret this!",
    (28, 51): "I will avenge our commander's death.",
    (28, 52): "I will carry on our commander's wishes!",
    (28, 53): "I will avenge our commander!",
    (28, 54): "I will avenge our commander's death!",
    (28, 55): "I will avenge our commander!",
    (28, 56): "I will avenge our commander!",
    (28, 57): "I shall avenge our commander!",
    (28, 59): "Oh, we lost. I'd better find a new employer.",
    (28, 60): "This is bad. What am I going to do...?",
    (28, 62): "%s sent a personal letter?",
    (28, 63): "%s sent us a personal letter?",
    (28, 64): "%s sent a personal letter?",
    (28, 65): "%s sent us a personal letter?",
    (28, 66): "We have no reason to accept it. Send it back!",
    (28, 68): "Very well. I will accept it.",
    (28, 69): "Hmm... Fine, I'll accept it.",
    (28, 71): "Very well. Let us use this chance to strike %s.",
    (28, 74): "It would be unwise to oppose %s now. Decline politely.",
    (28, 76): "They ended the pact?! What is %s thinking?",
    (28, 79): "They want a ceasefire?",
    (28, 80): "They demand a ceasefire?",
    (29, 0): "Very well. We have no wish for pointless conflict either.",
    (29, 1): "All right. We don't want a pointless conflict either.",
    (29, 2): "Very well. We have no wish for pointless conflict either.",
    (29, 3): "All right. Pointless fighting does nobody any good.",
    (29, 4): "Outrageous! Tell them to prepare for death!",
    (29, 7): "What?! %s wants trouble? Prepare yourself!",
    (29, 9): "They want us to submit to %s?",
    (29, 10): "They demand that we submit to %s?",
    (29, 11): "They want us to submit to %s?",
    (29, 12): "They want us to submit to %s?",
    (29, 15): "A new product is available in %s?",
    (29, 16): "%s has a new product?",
    (29, 17): "There's a new product in %s?",
    (29, 18): "What, a new product in %s?",
    (29, 19): "An enemy merchant fleet appeared at %s?",
    (29, 20): "An enemy merchant fleet appeared at %s?",
    (29, 21): "What, an enemy merchant fleet at %s?",
    (29, 23): "Send a fleet at once!",
    (29, 24): "Let us send a fleet at once.",
    (29, 25): "Suspicious... It may be false. Ignore it.",
    (29, 26): "Can we trust that report? Fine, ignore it.",
    (29, 27): "That sounds false. Ignore it.",
    (29, 28): "They demand that we submit to %s?!",
    (29, 29): "They want us to submit to %s?!",
    (29, 30): "They demand that we submit to %s?!",
    (29, 31): "We show restraint, and they grow arrogant!",
    (29, 32): "What a joke! Absolutely not!",
    (29, 34): "This document is forged. Ignore it.",
    (29, 35): "This document is forged. Ignore it.",
    (29, 36): "I think this is forged. Ignore it.",
    (29, 37): "This is clearly forged. Ignore it.",
    (29, 38): "This document is forged. Ignore it.",
    (29, 39): "I hear %s is involved in smuggling.",
    (29, 40): "I hear %s is utterly ruthless.",
    (29, 41): "Hmm... Is %s unfit to trade with our town?",
    (29, 42): "%s, a smuggler? That must be a false rumor.",
    (29, 44): "You want my help? My fee will be %s gold.",
    (29, 45): "You can't pay? Then the deal is off.",
    (29, 47): "%s tried to spread rumors in %s, but we stopped it.",
    (29, 51): "%s tried to spread rumors in %s, so I took precautions.",
    (29, 52): "Choose at least one coin, or the game cannot continue.",
    (29, 53): "A New World crop whose fruit and seeds are a local staple.",
    (29, 54): "A New World vegetable whose ripe fruit turns bright red.",
    (29, 55): "A sweet, fragrant Southeast Asian fruit that turns yellow when ripe.",
    (29, 56): "A honeycomb packed with nutritious honey gathered by bees.",
    (29, 59): "A pungent New World pepper with round or oblong fruit.",
    (29, 60): "An East African tree with jasmine-scented flowers. Its roasted fruit makes a drink.",
    (34, 0): "Southeast Asia has the ideal climate for growing pepper.",
    (34, 2): "Growing cinnamon in the Mediterranean could make a fortune.",
    (34, 3): "If only this spice could be sold in Africa.",
    (34, 4): "The New World should be well suited to coffee production.",
    (34, 5): "Tea could probably be grown in Africa too.",
    (34, 7): "African ore could become a new product.",
    (34, 8): "Glass is precious in Africa and East Asia.",
    (34, 10): "Pearls might be found in East Asia too.",
    (34, 11): "China may still hold rare herbal medicines.",
    (34, 12): "Southeast Asia has rare fruit whose peel yields dye.",
    (34, 13): "This should be very useful during a rat outbreak.",
    (34, 14): "Every voyage should carry this against scurvy.",
    (34, 15): "No sailor can defy the weather. This will be useful.",
    (34, 16): "A marvel of Eastern medicine, especially against epidemics.",
    (34, 17): "Give this to a deckhand.",
    (34, 18): "Give this to a deckhand or boarding chief.",
    (34, 20): "Give this to a deckhand or boarding chief.",
    (34, 21): "Not worth its price, but it may look impressive.",
    (34, 22): "Give this to a deckhand.",
    (34, 23): "Give this to a deckhand or boarding chief.",
    (34, 24): "Give it to an officer, or wield it yourself.",
    (34, 25): "Give this to a deckhand or boarding chief.",
    (34, 26): "Give this to your boarding chief.",
    (34, 27): "Give this to your boarding chief.",
    (34, 28): "Entrust this to a reliable champion.",
    (34, 29): "Entrust this to a reliable champion.",
    (34, 30): "It is called Gentian. Only a mighty champion could master it.",
    (34, 31): "A fine item for a skilled boarding chief.",
    (34, 32): "Give this to a skilled boarding chief.",
    (34, 33): "Give this to your boarding chief.",
    (34, 34): "Give this to a deckhand for self-defense.",
    (34, 35): "Give this to a deckhand or boarding chief.",
    (34, 36): "A masterpiece fit for a trusted warrior.",
    (34, 37): "Give it to a companion, or wield it yourself.",
    (34, 38): "A splendid blade! I sense an unseen power within it.",
    (34, 39): "The legendary blade... I never thought I would see it.",
    (34, 41): "Even someone unsure of their skill can use this.",
    (34, 43): "Give this to a deckhand.",
    (34, 44): "Light, easy-to-use armor.",
    (34, 45): "Give this to your boarding chief.",
    (34, 46): "Give this to your boarding chief.",
    (34, 47): "Give this to a deckhand or boarding chief.",
    (34, 48): "Give this to a deckhand or boarding chief.",
    (34, 50): "Give this to a deckhand or boarding chief.",
    (34, 51): "Give such equipment to a confident fighter.",
    (34, 52): "Give such equipment to a confident fighter.",
    (34, 54): "One rarely encounters an item this fine.",
    (34, 55): "One rarely encounters an item this fine.",
    (34, 56): "Hmm... A truly splendid item.",
    (34, 57): "It holds an indescribable power.",
    (34, 58): "This is equipment fit for a true champion!",
    (34, 59): "It has the majesty of a conqueror. What a sight!",
    (34, 60): "This armor is worthy of the admiral.",
    (34, 61): "Give this to the sail handler.",
    (34, 62): "Give this to the mainmast sail handler.",
    (34, 63): "The lookout must know the ship's heading.",
    (34, 64): "The lookout must know the ship's exact heading.",
    (34, 65): "Deck work is dull. Poetry would be a good diversion.",
    (34, 66): "Deck work is dull. A story might be a good diversion.",
    (34, 67): "Deck work is dull. Pass the time with a funny tale.",
    (34, 68): "A chart's accuracy depends on the quality of the tools.",
}

PACKED = {
    (28, i) for i in (1, 2, 3, 4, 5, 9, 25, 41, 42, 43, 45, 49, 58, 61, 67, 70, 72, 73, 75, 77, 78)
} | {(29, i) for i in (5, 6, 8, 13, 14, 22, 33, 43, 46, 48, 49, 50, 57, 58)} | {
    (34, i) for i in (1, 6, 9, 19, 40, 42, 49, 53, 69, 70)
}
PADDING = {(28, 81), (29, 61), (34, 71)}


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    clean = {(int(r["block_index"]), int(r["segment_index"])): r for r in inventory["records"] if int(r["block_index"]) in COUNTS}
    expected = {(b, i) for b, count in COUNTS.items() for i in range(count)}
    if set(clean) != expected or set(DRAFTS) & (PACKED | PADDING):
        raise ValueError("block 28/29/34 classification mismatch")
    common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    if sha256(common).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted COMMON hash mismatch")
    accepted = {(r.block_index, r.segment_index): r for r in iter_mesfile_records(common, include_non_japanese=True) if r.block_index in COUNTS}
    safe, blocked, audit = [], [], []
    for key in sorted(expected):
        b, i = key
        row, base = clean[key], accepted[key]
        if len(base.raw_bytes) != int(row["source_length"]):
            raise ValueError(f"{key}: allocation mismatch")
        rid = f"DK4_MES_B{b:02d}_R{i:04d}"
        if key in DRAFTS:
            text = DRAFTS[key]
            safe.append({"id": rid, "english": text + "{PAD}", "speaker": "Fleet officer, adviser, or item appraiser", "context": "Shared naval, diplomacy, product, or appraisal message.", "source_meaning": text, "localization_note": "Natural American English faithful to the clean Japanese single-message segment.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
            classification, reason = "single-message", "One independently addressable message; still subject to renderer QA."
        else:
            classification = "padding-only" if key in PADDING else "packed-multiple-entry" if key in PACKED else "single-message-editorial-blocked"
            reason = "Padding-only segment." if key in PADDING else "Multiple messages share one allocation and interior entry offsets are unproven." if key in PACKED else "Single source message retained for a later reviewed translation pass."
            blocked.append({"id": rid, "source_length": row["source_length"], "source_hex": row["source_hex"], "japanese_markup": row["markup"], "classification": classification, "speaker": "Fleet officer, adviser, or item appraiser", "context": "Shared naval, diplomacy, product, or appraisal message.", "source_meaning": "Clean Japanese preserved in full.", "editorial_status": "source classified; translation pending" if classification != "padding-only" else "not translatable", "blocker": reason, "review": {"source": True, "context": True, "localization": False, "naturalness": False, "formatting": False}})
        audit.append({"id": rid, "block_index": b, "segment_index": i, "source_length": row["source_length"], "clean_source_hex": row["source_hex"], "accepted_source_hex": base.raw_bytes.hex().upper(), "japanese_markup": row["markup"], "classification": classification, "safe_to_replace": key in DRAFTS, "safety_reason": reason})
    BATCH.write_text(json.dumps({"format": "dk4-ilnk-translation-batch-v1", "file_path": "/COMMON/MESFILE.DK4", "source_file_sha256": SOURCE_HASH, "encoder": "dialogue-fixed-v1", "dialogue_profile": "shared-pair-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Source-safe single-entry records in COMMON blocks 28, 29, and 34", "blocked_records": [r["id"] for r in blocked], "records": safe}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BLOCKED.write_text(json.dumps({"format": "dk4-blocked-editorial-inventory-v1", "file_path": "/COMMON/MESFILE.DK4", "source_file_sha256": SOURCE_HASH, "blocks": [28, 29, 34], "buildable": False, "records": blocked}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {name: sum(r["classification"] == name for r in audit) for name in ("single-message", "packed-multiple-entry", "single-message-editorial-blocked", "padding-only")}
    AUDIT.write_text(json.dumps({"format": "dk4-common-entry-safety-audit-v1", "file_path": "/COMMON/MESFILE.DK4", "blocks": [28, 29, 34], "accepted_source_file_sha256": SOURCE_HASH, "classification_counts": counts, "records": audit}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote block 28/29/34 audit={len(audit)}, safe={len(safe)}, blocked={len(blocked)}")


if __name__ == "__main__":
    main()
