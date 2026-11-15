"""Prepare source-reviewed native COMMON names and complete HELP articles.

No ROM or registered release is changed. COMMON identities are global message
IDs, since the old physical block/record coordinates were reblocked earlier.
HELP sections describe article structure, not manually positioned line breaks.
"""

import json
from dataclasses import asdict
from pathlib import Path

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.mesfile import export_mesfile_rows

OUT = Path("work/analysis/confirmed_name_common_v228")
COMMON_PATH = "/COMMON/MESFILE.DK4"
HELP_PATH = "/COMMON/HELP.DK4"
CURRENT = Path("out/all_routes_combined_v218_candidate.nds")
CURRENT_SHA = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"

TEXT = {
    1360: (
        "... (I don't understand the words.)",
        "An aside admits not understanding the words.",
        "The source does not qualify this as partial language proficiency. Preserve the quiet aside without inventing a language or cause.",
    ),
    1361: (
        "Yes, that's a lovely sound.",
        "A warm, affirmative response praises the sound or timbre.",
        "Retain the musical approval without inventing the tune, performer or listener. The source note symbol conveys tone rather than an instruction.",
    ),
    1362: (
        "...That's quite well done...",
        "A reserved comment approves of the quality of the work or performance.",
        "Keep the restrained approval and surrounding hesitation. Do not infer a specific activity from the packed record's neighboring messages.",
    ),
    1363: (
        "Zzz... Honestly, Camille... Zzz...",
        "A sleeping voice mutters a mildly exasperated address to Camille between snores.",
        "Honestly conveys the mild exasperation of んもう naturally. Keep the snores and settled Camille spelling without inventing a relationship or dream event.",
    ),
    1683: (
        "I can't keep relying on Camille forever...",
        "The speaker reflects that continuing to rely on Camille indefinitely is not good.",
        "Restore the self-reflection as a complete natural sentence. The trailing hesitation remains; no new outcome or responsibility is invented.",
    ),
    1830: (
        "Am I going to die...? Camille...",
        "The speaker wonders whether they are going to die and addresses Camille.",
        "Restore the uncertainty expressed by かな. The previous Dying fragment made this sound like a definite report. Preserve the hesitant address, not an invented farewell.",
    ),
}

HELP = {
    "DK4_MES_B07_R0000": [
        ("heading", "Rafael Castor"),
        ("paragraph", "A young Portuguese sailor inspired by the many explorers who set out from Lisbon. He starts with many companions, making his route an accessible choice for new players."),
        ("paragraph", "Home port: Lisbon (Mediterranean)."),
        ("advantage", "Military investment costs 20 percent less."),
        ("advantage", "Discovering ruins or items grants twice the usual Influence."),
    ],
    "DK4_MES_B37_R0000": [
        ("heading", "Military Investment (Palace / Governor's Office)"),
        ("paragraph", "Invest in a city's defenses, from 1 to 20 units at a time. Each unit costs gold equal to 50 percent of the city's Arms rating, or 40 percent for Rafael."),
        ("paragraph", "Investment raises the city's Arms rating. Your market share also rises if the city's total market share is below 100 percent or a faction you are at war with owns a share."),
        ("paragraph", "A higher Arms rating makes the city less likely to surrender when attacked and allows you to buy better ships and cannons."),
    ],
}


def native_lock(entry):
    return {key: value for key, value in asdict(entry).items() if key != "text"} | {
        "text_hex": entry.text.hex().upper(),
        "text_sha256": sha(entry.text),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError("Reviewed current ROM identity differs")
    current, clean = NdsImage.open(CURRENT), NdsImage.open("work/clean.nds")
    source = common_message_entries(clean.read_file(COMMON_PATH), clean.read_file("/__arm9__.bin"))
    actual = common_message_entries(current.read_file(COMMON_PATH), current.read_file("/__arm9__.bin"), clean=False)
    records, audits = [], []
    for message_id, (english, gloss, note) in TEXT.items():
        original, selected = source[message_id], actual[message_id]
        encoded_text = english.replace("I", "Ｉ").replace("F", "Ｆ")
        audit = audit_native_common_entry(b" " * len(encoded_text.encode("cp932")), encoded_text + "{PAD}")
        records.append({
            "id": f"COMMON_MESSAGE_{message_id:04d}", "message_id": message_id,
            "source_hex": original.text.hex().upper(),
            "japanese": original.text.decode("cp932"),
            "english": encoded_text + "{PAD}", "readable_english": english,
            "speaker": "Context-dependent companion voice; fixed actor not established by the message table",
            "context": (
                "Native messages 1360-1363 are four separate ambient responses in one clean owner, not one dialogue paragraph. "
                "1683 is a shared battle reflection; 1830 is a shared critical-health reaction. "
                "Neighboring entries are response variants and do not establish a continuous conversation. "
                "Preserve each global message identity and do not infer kinship or actor identity from adjacency."
            ),
            "source_meaning": gloss, "localization_note": note + " Reserved uppercase I/F use the existing safe full-width glyph encoding; translators add no layout spaces or line breaks.",
            "clean_native_lock": native_lock(original), "current_native_lock": native_lock(selected),
            "clean_native_neighbors": [
                {"message_id": e.message_id, "japanese": e.text.decode("cp932")}
                for e in source[max(0, message_id - 1):message_id + 2]
            ],
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
        })
        audits.append({"message_id": message_id, "audit": audit})
    manuscript = {
        "format": "dk4-common-entry-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-fixed-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "status": "editorially-reviewed-native-allocation-and-preview-review-pending",
        "parent_ROM": CURRENT.as_posix(), "parent_ROM_sha256": CURRENT_SHA,
        "parent_common_sha256": sha(current.read_file(COMMON_PATH)),
        "records": records,
    }
    Path("translations/confirmed_name_common_manuscript_v1.json").write_text(
        json.dumps(manuscript, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source_help = {r["id"]: r for r in export_mesfile_rows(clean.read_file(HELP_PATH), HELP_PATH, include_non_japanese=True)}
    current_help = {r["id"]: r for r in export_mesfile_rows(current.read_file(HELP_PATH), HELP_PATH, include_non_japanese=True)}
    articles = []
    for record_id, sections in HELP.items():
        old = current_help[record_id]
        source_row = source_help[record_id]
        articles.append({
            "id": record_id, "file_path": HELP_PATH, "japanese": source_row["japanese"],
            "source_hex": source_row["source_hex"], "current_source_hex": old["source_hex"],
            "clean_article_neighbors": [
                {"id": neighbor, "japanese": source_help[neighbor]["japanese"]}
                for neighbor in list(source_help)[max(0, list(source_help).index(record_id) - 1):list(source_help).index(record_id) + 2]
            ],
            "sections": [{"role": role, "english": text} for role, text in sections],
            "source_meaning": (
                "Rafael's biography, Lisbon/Mediterranean home, accessible starting companions, military-cost discount and doubled Influence gain."
                if "B07" in record_id else
                "Palace/Governor's Office military investments: 1-20 units, gold cost 50 percent of Arms (Rafael 40), raised Arms, market-share conditions, surrender resistance and better ships/cannons."
            ),
            "localization_note": (
                "Heading and advantage sections remain separate semantic roles; the renderer/formatter owns wrapping. "
                "Restore omitted geography, gameplay conditions and uncertainty. Keep percent spelled out to preserve printf safety. "
                "Do not shorten complete prose to the old allocation or flatten structural headings into a run-on paragraph."
            ),
            "current_allocation_bytes": len(bytes.fromhex(old["source_hex"])),
            "logical_prose_bytes_before_layout": sum(len(text.encode("ascii")) for _, text in sections),
            "requires_reviewed_help_allocation_and_native_article_consumer": True,
            "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False},
        })
    help_payload = {
        "format": "dk4-structured-help-editorial-manuscript-v1", "not_a_release_batch": True,
        "target_locale": "en-US", "parent_ROM_sha256": CURRENT_SHA,
        "source_file_sha256": sha(clean.read_file(HELP_PATH)),
        "current_file_sha256": sha(current.read_file(HELP_PATH)), "records": articles,
    }
    Path("translations/confirmed_name_help_manuscript_v1.json").write_text(
        json.dumps(help_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"format": "dk4-confirmed-name-common-editorial-review-v228", "common_audits": audits,
              "native_entry_ids": list(TEXT), "HELP_articles": len(articles),
              "old_COMMON_physical_record_coordinates_rejected_as_identities": True,
              "packed_B16_owner_preserved_as_four_separate_entries": True,
              "source_context_localization_naturalness_review_complete": True,
              "formatting_native_consumer_and_release_pending": True, "playable_ROM_modified": False}
    (OUT / "editorial_review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"COMMON_entries": len(records), "HELP_articles": len(articles),
                      "layout_issues": [a for a in audits if a["audit"]["issues"]], "playable_ROM_modified": False}))


if __name__ == "__main__":
    main()
