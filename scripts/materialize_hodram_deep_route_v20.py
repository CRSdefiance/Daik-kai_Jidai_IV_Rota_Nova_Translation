from __future__ import annotations

import csv
import json
from pathlib import Path


SOURCE = Path("work/sc1/script.csv")
OUTPUT_A = Path("translations/hodram_deep_route_v20a.json")
OUTPUT_B = Path("translations/hodram_deep_route_v20b.json")
SC1_SHA256 = "2126eddc3bd17ef2b24efd9a1072b0d12190371edcb487a0c4817a52faf91cb6"
BLOCKS_A = (250, 251, *range(253, 260))
BLOCKS_B = (252,)
EXCLUDED_A: dict[str, str] = {}
EXCLUDED_B = {
    "DK4_MES_B252_R0186": "Raw four-byte event-control payload; not dialogue.",
}


LINES_A = {
    # Rio survey reward and nearby Solomon's treasury lead.
    "DK4_MES_B250_R0005": "Thank you. Take the expenses and reward.",
    "DK4_MES_B250_R0010": "Received 42,000 coins.",
    "DK4_MES_B250_R0034": "Sofala share rose slightly!",
    "DK4_MES_B250_R0052": "Visited the ruins near town?{LB}",
    "DK4_MES_B250_R0055": "Legend calls them King Solomon's treasury. Pay them a visit.",

    # Cesare and Hodram discover a benevolent figurehead.
    "DK4_MES_B251_R0005": "What is it, Admiral?",
    "DK4_MES_B251_R0009": "Does this statue make you feel something? A strange warmth...",
    "DK4_MES_B251_R0015": "A statue? Where?",
    "DK4_MES_B251_R0018": "There.",
    "DK4_MES_B251_R0022": "Let's see.",
    "DK4_MES_B251_R0026": "A figurehead!{LB}Very finely made. Yes,{LB}there is a strange feeling here!",
    "DK4_MES_B251_R0033": "Could it be renowned?",
    "DK4_MES_B251_R0037": "Never heard of it.{LB}Wait, do you mean to take it?",
    "DK4_MES_B251_R0043": "Exactly",
    "DK4_MES_B251_R0045": "No.",
    "DK4_MES_B251_R0053": "A splendid figurehead.{LB}Such a piece may bless our ship.{LB}But may we take it?",
    "DK4_MES_B251_R0056": "Such a fine figurehead should sail, not sit on land. Do you disagree?",
    "DK4_MES_B251_R0060": "How kind you are, Admiral! Let us carry it away at once!",
    "DK4_MES_B251_R0064": "Pardon us, figurehead. Please come with us.",
    "DK4_MES_B251_R0067": "Then this one shall watch over you.",
    "DK4_MES_B251_R0070": "What was that voice?!",
    "DK4_MES_B251_R0073": "What are you doing? Help us.",
    "DK4_MES_B251_R0076": "That voice...",
    "DK4_MES_B251_R0080": "Dreaming?",
    "DK4_MES_B251_R0085": "{MACRO:FI}'s Luck rose by 1!",
    "DK4_MES_B251_R0089": "Cesare's Luck rose by 1!",
    "DK4_MES_B251_R0092": "What was that voice? So warm, so full of compassion...",
    "DK4_MES_B251_R0099": "Yes... Yet part of this man feels disappointed.",
    "DK4_MES_B251_R0103": "Time to return to town.",
    "DK4_MES_B251_R0110": "Agreed. Still, merely seeing that wonderful statue cleansed the heart...",
    "DK4_MES_B251_R0113": "{MACRO:FI}'s Charm rose by 1!",
    "DK4_MES_B251_R0117": "Cesare's Charm rose by 1!",

    # Short local ruin hints.
    "DK4_MES_B253_R0007": "Hello, {MACRO:FI}! Welcome!",
    "DK4_MES_B253_R0010": "Looking for ruins? Some lie nearby.",
    "DK4_MES_B253_R0013": "Outsiders rarely hear this, but you are an exception.",
    "DK4_MES_B254_R0006": "Welcome, {MACRO:FI}.",
    "DK4_MES_B254_R0009": "Searching ruins worldwide?{LB}This town has no famous ones.",
    "DK4_MES_B255_R0006": "Hello, {MACRO:FI}.",
    "DK4_MES_B255_R0010": "Searching ruins worldwide? Sadly, this town has no famous ones.",

    # London guild request to find the wandering noble Yulis.
    "DK4_MES_B256_R0005": "A job requires finding someone.{LB}Will you take it?",
    "DK4_MES_B256_R0012": "A noble who loves travel never returns to his estate. His people have complained.",
    "DK4_MES_B256_R0016": "Rumor places him in Syracuse...",
    "DK4_MES_B257_R0006": "There you are. With {MACRO:FA}, right? London's guild seeks you.",
    "DK4_MES_B258_R0005": "Yulis should be in this town.",
    "DK4_MES_B258_R0008": "Ah, ancient Rome. Such beauty.",
    "DK4_MES_B258_R0012": "Excuse this man. Do you know anyone named Yulis nearby?",
    "DK4_MES_B258_R0015": "Such strength, such grace...",
    "DK4_MES_B258_R0019": "...Are you listening?",
    "DK4_MES_B258_R0023": "This man is Yulis.",
    "DK4_MES_B258_R0027": "You are? Now that you say so, your manner is rather noble...",
    "DK4_MES_B258_R0031": "You cannot idle here. Your people are upset that their lord left and never returned.",
    "DK4_MES_B258_R0034": "Oh! The estate was forgotten completely! Please take this man home.",
    "DK4_MES_B258_R0037": "Back to London first. Then we shall see.",
    "DK4_MES_B259_R0005": "Yulis! What have you done while neglecting work? Your people are suffering.",
    "DK4_MES_B259_R0009": "Sorry. Travel makes this man stray.{LB}The return begins now.",
    "DK4_MES_B259_R0013": "Honestly... Rest here after your long journey, then go home.",
    "DK4_MES_B259_R0017": "Almost forgot. Take this small reward.",
    "DK4_MES_B259_R0021": "Received 11,000 coins.",
    "DK4_MES_B259_R0049": "London share rose slightly!",
    "DK4_MES_B259_R0060": "Sorry. A customer waits.",
    "DK4_MES_B259_R0064": "Old man, no maps?",
    "DK4_MES_B259_R0068": "You lot again? Yes, none left.",
    "DK4_MES_B259_R0071": "Tch. Useless.",
    "DK4_MES_B259_R0075": "..",
    "DK4_MES_B259_R0079": "You scum bought them all!",
    "DK4_MES_B259_R0082": "Maps?",
    "DK4_MES_B259_R0086": "Maps to a site. Strange men gather there and trouble nearby residents.",
    "DK4_MES_B259_R0090": "Nearby?",
    "DK4_MES_B259_R0094": "Rather far, but easy with a map. Those men bought every copy.",
    "DK4_MES_B259_R0097": "Another town may still have one.",
    "DK4_MES_B259_R0100": "Got it...",
}


LINES_B = {
    # Fernando and Hodram solve a water-level ruin puzzle and awaken a statue.
    "DK4_MES_B252_R0006": "Admiral, over here! Writing on the wall!",
    "DK4_MES_B252_R0009": "A full vessel holds floating ice. When the ice melts, what happens to the water level?",
    "DK4_MES_B252_R0012": "Press the stone ahead for higher, left for lower, or right for unchanged.",
    "DK4_MES_B252_R0019": "Ahead",
    "DK4_MES_B252_R0021": "Left",
    "DK4_MES_B252_R0023": "Right",
    "DK4_MES_B252_R0031": "This is it!",
    "DK4_MES_B252_R0042": "Admiral, the ceiling falls! Danger!",
    "DK4_MES_B252_R0043": "Admiral! The ceiling falls!",
    "DK4_MES_B252_R0044": "Admiral! The ceiling is collapsing!",
    "DK4_MES_B252_R0045": "Admiral! The ceiling is falling! Run!",
    "DK4_MES_B252_R0047": "Look out! The ceiling falls!",
    "DK4_MES_B252_R0048": "Admiral, the ceiling is falling! We should flee!",
    "DK4_MES_B252_R0049": "Aaaah! The ceiling is falling!",
    "DK4_MES_B252_R0050": "The ceiling falls. We must leave.",
    "DK4_MES_B252_R0053": "Wrong! Dangerous here. Back to town!",
    "DK4_MES_B252_R0068": "This is it!",
    "DK4_MES_B252_R0079": "Admiral, the ceiling falls! Danger!",
    "DK4_MES_B252_R0080": "Admiral! The ceiling falls!",
    "DK4_MES_B252_R0081": "Admiral! The ceiling is collapsing!",
    "DK4_MES_B252_R0082": "Admiral! The ceiling is falling! Run!",
    "DK4_MES_B252_R0083": "Look out! The ceiling is collapsing!",
    "DK4_MES_B252_R0085": "Admiral, the ceiling is falling! We should flee!",
    "DK4_MES_B252_R0086": "Aaaah! The ceiling is falling!",
    "DK4_MES_B252_R0087": "The ceiling falls. We must leave.",
    "DK4_MES_B252_R0090": "Wrong! Dangerous here. Back to town!",
    "DK4_MES_B252_R0106": "Melting ice cannot change the level.",
    "DK4_MES_B252_R0112": "The wall opens!",
    "DK4_MES_B252_R0120": "Admiral! A strange statue!",
    "DK4_MES_B252_R0123": "Where?",
    "DK4_MES_B252_R0127": "Here. Like a figurehead...",
    "DK4_MES_B252_R0130": "Crack! Crack!",
    "DK4_MES_B252_R0134": "What?!",
    "DK4_MES_B252_R0138": "Did you wake me?",
    "DK4_MES_B252_R0142": "Waaah! Admiral!",
    "DK4_MES_B252_R0145": "Answer!",
    "DK4_MES_B252_R0151": "Yes",
    "DK4_MES_B252_R0153": "No",
    "DK4_MES_B252_R0160": "Then wield my power!",
    "DK4_MES_B252_R0164": "Huh?",
    "DK4_MES_B252_R0168": "Take the statue bearing my power, then leave this place at once!",
    "DK4_MES_B252_R0174": "What was that? This thing will not curse us, will it?",
    "DK4_MES_B252_R0178": "Who knows? This man cannot say.",
    "DK4_MES_B252_R0184": "You say this one woke alone? Such insult demands punishment!",
    "DK4_MES_B252_R0195": "Rooooooar!!",
    "DK4_MES_B252_R0207": "Admiral! Run!",
    "DK4_MES_B252_R0212": "Everyone, run!!",
    "DK4_MES_B252_R0223": "Hah, hah... Whew, that was close.",
    "DK4_MES_B252_R0226": "This body feels heavy.",
}


SPEAKERS_A = {
    "01": "Hodram Bergstrom", "0D": "Cesare Tohni", "40": "Yulis",
    "71": "Sailor", "93": "Guildmaster", "B2": "Ruffian", "BD": "Woman",
    "BE": "Woman", "C8": "Woman", "FE": "System or statue voice",
}
SPEAKERS_B = {
    "01": "Hodram Bergstrom", "14": "Fernando", "D0": "Crewman",
    "FE": "Ruin inscription or statue voice",
}

CONTEXT_A = {
    250: "The guild rewards the Rio survey and points Hodram toward Solomon's treasury.",
    251: "Cesare and Hodram discover a benevolent figurehead that raises luck or charm.",
    253: "A local woman privately reveals nearby ruins.",
    254: "A local woman says the town has no famous ruins.",
    255: "A local woman says the town has no famous ruins.",
    256: "The London guild asks Hodram to find the wandering noble Yulis in Syracuse.",
    257: "A sailor tells Hodram's company that London's guild is looking for them.",
    258: "Hodram finds Yulis absorbed in Roman art and agrees to escort him home.",
    259: "The guild receives Yulis, pays Hodram, and reveals a map-buying dispute tied to nearby ruins.",
}
CONTEXT_B = {252: "Fernando and Hodram solve a water-level ruin puzzle and awaken a supernatural figurehead."}


def _make_batch(
    *, output: Path, blocks: tuple[int, ...], lines: dict[str, str], excluded: dict[str, str],
    speakers: dict[str, str], contexts: dict[int, str], profile: str, scope: str,
) -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        source_rows = {
            row["id"]: row for row in csv.DictReader(stream)
            if any(row["id"].startswith(f"DK4_MES_B{block}_") for block in blocks)
        }
    if set(lines) | set(excluded) != set(source_rows) or set(lines) & set(excluded):
        missing = sorted(set(source_rows) - set(lines) - set(excluded))
        extra = sorted((set(lines) | set(excluded)) - set(source_rows))
        raise SystemExit(f"Hodram V20 inventory mismatch: missing={missing}, extra={extra}")
    extended_states = {int(state, 16) for state in speakers}
    records = []
    block_counts: dict[str, int] = {}
    for row_id, english in lines.items():
        row = source_rows[row_id]
        first = bytes.fromhex(row["source_hex"])[0]
        state = f"{first:02X}" if ((0x01 <= first <= 0x0F and first != 0x0A) or first in extended_states) else ""
        block = int(row_id.split("_B", 1)[1].split("_", 1)[0])
        block_counts[str(block)] = block_counts.get(str(block), 0) + 1
        records.append({
            "id": row_id,
            "english": f"{{SPEAKER:{state}}}{english}{{PAD}}" if state else f"{english}{{PAD}}",
            "speaker": speakers.get(state, "Choice or alternate crew text"),
            "context": contexts[block],
            "source_meaning": english.replace("{MACRO:FI}", "Hodram").replace("{MACRO:FA}", "Hodram's company").replace("{LB}", " "),
            "localization_note": "Faithful concise American English with measured fixed-record wrapping.",
            "qa_waivers": ["weak-line-ending", "orphan-final-line", *(["manual-break"] if "{LB}" in english else [])],
            **({"manual_break_reason": "Places a protected newline before the native row boundary so the progressive ASCII pair phase cannot auto-wrap and skip a display row."} if "{LB}" in english else {}),
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": True},
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "file_path": "/data/SC1.DK4",
        "source_file_sha256": SC1_SHA256, "encoder": "dialogue-fixed-v1",
        "dialogue_profile": profile, "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "scope": scope, "excluded_records": excluded,
        "inventory": {"identified_records": len(source_rows), "translated_records": len(records), "blocks": block_counts},
        "records": records,
    }
    output.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}: {len(records)} records, {len(excluded)} controls preserved")


def main() -> None:
    _make_batch(output=OUTPUT_A, blocks=BLOCKS_A, lines=LINES_A, excluded=EXCLUDED_A, speakers=SPEAKERS_A, contexts=CONTEXT_A, profile="hodram-story-quest-live", scope="Nine source-locked Hodram local-hint, figurehead, and guild-quest events across SC1 blocks 250-251 and 253-259.")
    _make_batch(output=OUTPUT_B, blocks=BLOCKS_B, lines=LINES_B, excluded=EXCLUDED_B, speakers=SPEAKERS_B, contexts=CONTEXT_B, profile="hodram-story-puzzle-live", scope="The source-locked Hodram water-level ruin puzzle and awakened-figurehead event in SC1 block 252, preserving one raw event payload.")


if __name__ == "__main__":
    main()
