"""Restore all native neighbors of B0's blank departure/supply messages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

PROSE = {
    30: ("Admiral, it looks like some of our ships need repairs.", "The speaker cautiously reports to the admiral that some ships appear to require repairs."),
    31: ("Hold on! Some ships need repairs before we set sail.", "The speaker asks the player to wait: some ships must be repaired before departure."),
    32: ("Admiral, let's repair the ships before we sail. It's too risky like this!", "An informal speaker urges repairs before departure and warns that the current state is dangerous."),
    33: ("Admiral, repairs must come before we set sail.", "An older-sounding speaker states that ship repairs take priority over departure."),
    34: ("Admiral! I don't want to drown! Let's get the ships fixed first!", "A childlike speaker calls to the admiral, fears drowning, and asks to repair the ships first."),
    35: ("Admiral, we should repair the ships before departing.", "A polite older-sounding speaker says ship repairs must precede departure."),
    37: ("Admiral, at this rate we'll run out of supplies in no time...", "An informal speaker warns the admiral that the current supplies will soon be exhausted."),
    38: ("We'll soon run out of supplies, Admiral...", "The speaker observes that the current supplies will soon run out."),
    41: ("Goodness... With so few supplies, we'll run out in no time.", "A politely emphatic speaker warns that the limited supplies will quickly be exhausted."),
    42: ("Admiral, I'm not sure these supplies will be enough...", "The speaker tentatively expresses unease about whether the supplies are sufficient."),
    43: ("Admiral, aren't we just a bit short on supplies?", "An informal speaker asks whether the available supplies are somewhat insufficient."),
    44: ("Admiral, I'm a little worried about having so few supplies...", "A polite speaker expresses concern about the limited amount of supplies."),
    45: ("Admiral, aren't we a little short on supplies?", "The speaker asks the admiral whether the supplies are a little insufficient."),
    46: ("Admiral, aren't we taking too few supplies?", "An older-sounding speaker asks whether the quantity of supplies is excessively small."),
    47: ("Admiral! Will I have enough to eat? Aren't we a little short on supplies?", "A childlike speaker worries about their own meals and asks whether the supplies are too few."),
    48: ("Hmm... We seem to be short on supplies.", "A polite speaker reflects that the amount of supplies appears small."),
    92: ("The fleets under our command have sent income and expense reports. Would you like to hear them?", "Income and expense reports have arrived from subordinate fleets; the player is asked whether to hear them."),
    93: ("The city of %s has opened fire on %s's fleet.", "The substituted city is bombarding the substituted faction or person's fleet, in that argument order."),
    95: ("In %s, %s sold large amounts of %s and expanded their market share!", "In the substituted city, the substituted person or faction sold large quantities of the substituted commodity and increased market share. Argument order is city, person/faction, commodity."),
    96: ("%s's market share has fallen!", "The substituted person or faction's market share has decreased, presented as unwelcome news."),
    98: ("You haven't acquired any items.", "No items have yet been obtained."),
    99: ("You haven't discovered any ruins.", "No ruins have yet been discovered."),
    100: ("Choose three skills you excel at.", "The player is asked to select three skills in which they are proficient."),
}


def main() -> None:
    clean = NdsImage.open("work/clean.nds")
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))
    inventory = json.loads(Path("work/analysis/common_native_v103.json").read_text(encoding="utf-8"))
    owners = {(entry["block"], entry["record"]) for entry in inventory["blank_native_messages"] if entry["block"] == 0}
    required = {entry.message_id for entry in entries if (entry.block, entry.record_index) in owners}
    if required != PROSE.keys():
        raise ValueError("B0 manuscript must cover every native neighbor of every blank record")
    records = []
    for message_id, (english, gloss) in PROSE.items():
        source = entries[message_id]
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "block": source.block, "record": source.record_index,
            "source_hex": source.text.hex().upper(), "japanese": source.text.decode("cp932"),
            "english": english.replace("I", "Ｉ").replace("F", "Ｆ") + "{PAD}",
            "source_meaning": gloss, "speaker": "Shared crew response or status narrator",
            "context": f"Independent native message {message_id}, COMMON B0 R{source.record_index}; departure safety, supplies, fleet reports or status/skill selection. Packed neighbors are separate messages.",
            "previous_japanese": entries[message_id - 1].text.decode("cp932"),
            "next_japanese": entries[message_id + 1].text.decode("cp932"),
            "localization_note": "Fresh clean-source localization retains repairs, danger, supplies, uncertainty, individual tone, financial report details and ordered substitutions. No relationship is inferred from age or manner of address. Reserved capital I/F use existing full-width Latin glyphs. Layout must use full native mapping rather than shorten meaning.",
            "review": {"source": True, "context": True, "localization": True,
                       "naturalness": True, "formatting": False},
        })
    path = Path("translations/common_blank_b0_manuscript_v1.json")
    path.write_text(json.dumps({
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "draft-awaiting-native-repack-and-formatting-review", "records": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(records)} source-reviewed B0 entries; formatting remains pending")


if __name__ == "__main__":
    main()
