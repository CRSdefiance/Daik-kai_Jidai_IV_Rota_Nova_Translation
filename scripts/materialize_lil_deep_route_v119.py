from __future__ import annotations

import csv
import json

from scripts.materialize_lil_deep_route_v107 import ROOT, SC2_SHA256

LINES = {
    (317, 6): "Welcome!",
    (317, 10): "{MACRO:FI}, heard of the Goryeo Celadon Burner? They say it's in East Asia.",
    (317, 14): "They say it makes readings much more accurate. Ah, how lovely to try it...",
    (317, 31): "Hmm.",
    (317, 35): "Oh, right!",
    (317, 39): "Pirates have been rampaging nearby lately. Better make sure your equipment is ready.",
    (317, 44): "Really? ...Thanks. We'll be careful.",
    (317, 47): "See you!",
    (318, 6): "Oh, welcome!",
    (318, 10): "Your burner made my readings much more accurate! Let me tell your fortune as thanks.",
    (318, 14): "Sit here.",
    (318, 26): "Deep inland from this city, ruins lie in the desert. What you seek must be there.",
    (319, 5): "Hey, little girl! Working hard?",
    (319, 8): "Hey, mister! As leader of {MACRO:FO}, being called a little girl is a bit much!",
    (319, 11): "Ha ha, sorry! Still, even a leader should be careful. Wandering here is dangerous for a young girl.",
    (319, 14): "Why?",
    (319, 18): "Gold and ivory are prized local goods. Profitable luxuries, but supplies are scarce.",
    (319, 22): "Greedy types like Silveira buy up the supplies. So others have started trading in different things.",
    (319, 26): "What things?",
    (319, 30): "Slaves, drugs, poaching... Anything goes. Some people have always ignored the law for easy money.",
    (319, 39): "You mean Espinosa...",
    (319, 50): "No worries! The Espinosa Company is already gone!",
    (319, 61): "Leave it to us! We'll bring down the Espinosa Company!",
    (319, 66): "Don't worry! We've taught Espinosa a lesson!",
    (319, 75): "No... Someone else will replace Espinosa when he's gone.",
    (319, 79): "What? So no matter what we do, the bad guys won't go away?",
    (319, 86): "Others will seek the same wicked profits after Espinosa. This region has a deeper problem.",
    (319, 90): "A cheap, profitable good suited to this land would help...",
    (319, 93): "What?",
    (319, 97): "Gold and ivory cost a lot and are scarce. You need capital to start trading. Only a few can afford it.",
    (319, 100): "But if goods were cheap, anyone could enter the market and trade honestly.",
    (319, 104): "Make honest trade easy and profitable, and people won't need to risk dangerous ventures.",
    (319, 108): "Ah... So honest trade could spare people from selling drugs?",
    (319, 112): "...A new, profitable good...",
    (319, 115): "Seeds for tropical crops, perhaps. They say the New World has many new crops we've never seen.",
}
STATES = {0x02, 0x68, 0xCC}


def main() -> None:
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = {r["id"]: r for r in csv.DictReader(stream)}
    expected = {i for i in source if 317 <= int(i.split("_B")[1].split("_")[0]) <= 319}
    assert expected == {f"DK4_MES_B{b}_R{n:04d}" for b, n in LINES}
    records = []
    for (b, n), text in LINES.items():
        row_id = f"DK4_MES_B{b}_R{n:04d}"
        raw = bytes.fromhex(source[row_id]["source_hex"])
        safe = text
        for macro in ("FI", "FO"):
            assert raw.count(macro.encode()) == text.count(f"{{MACRO:{macro}}}"), row_id
            safe = safe.replace(f"{{MACRO:{macro}}}", "")
        assert "I" not in safe and "F" not in safe, row_id
        state = raw[0] in STATES
        records.append({"id": row_id, "english": (f"{{SPEAKER:{raw[0]:02X}}}" if state else "") + text + "{PAD}", "speaker": "Lil" if raw[0] == 2 else "Fortune teller or local man", "context": "Goryeo burner divination and pirate warning; African luxury monopolies, illegal trade and tropical crops as an alternative.", "source_meaning": text, "source_japanese": raw[int(state):].decode("shift_jis", errors="replace"), "localization_note": "Natural English retains the established Goryeo Celadon Burner dialogue alias, East Asia, desert ruins, Silveira/Espinosa names, all three Espinosa outcomes, market entry costs, affordable profitable crops and New World seed lead. FI/FO and genuine states preserved.", "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")}})
    batch = {"format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC2.DK4", "source_file_sha256": SC2_SHA256, "encoder": "dialogue-fixed-v1", "dialogue_profile": "lil-story-deep-route-v119-live", "translation_policy": "natural-dialogue-v2", "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"], "scope": "Complete B317-B319 fortune teller and affordable trade scene.", "inventory": {"identified_records": len(expected), "translated_records": len(records), "blocks": {str(b): sum(bb == b for bb, _ in LINES) for b in range(317, 320)}}, "excluded_records": {}, "records": records}
    (ROOT / "translations/lil_deep_route_v119.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote Lil V119: {len(records)} records")


if __name__ == "__main__":
    main()
