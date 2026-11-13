"""Prepare source-owned village names/menu labels and a scoped name correction."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/village_ui_v609")
MANUSCRIPT = Path("translations/village_ui_manuscript_v1.json")
NAMES = ["Inuvik", "Hawaii", "Rio de Janeiro", "Churchill", "Valparaiso", "Nome", "Cape Cod",
         "Montevideo", "Hekla", "Karibib", "Forel", "Tahiti", "Dikson", "Azores", "Santa Barbara",
         "Narvik", "Leveque", "Callao", "Ezo", "Perth", "Guam", "Tiksi", "Korf", "Wanganui"]
MENU = [("補給", "Resupply", 0x1478F0), ("宿泊", "Stay", 0x1478E8),
        ("船修理", "Repair Ship", 0x147918), ("水夫募集", "Recruit Sailors", 0x147940),
        ("出港", "Set Sail", 0x1478F8), ("約束の言葉", "Promised Words", 0x147A24)]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source_rom = NdsImage.open("work/clean.nds")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    current = NdsImage.open("out/all_routes_combined_v608_candidate.nds")
    source, baked = [r.read_file("/__arm9__.bin") for r in (source_rom, canonical)]
    rows = []

    def add(ident, english, japanese, gloss, context, **extra):
        rows.append({"id": ident, "english": english, "Japanese": japanese,
            "source_meaning": gloss, "context": context, "speaker": "Village UI / place-name label",
            "localization_note": "Use established English geographic spelling when identified; preserve the game's historical/unqualified labels. ASCII accent folding follows the existing UI font. No new story facts or place categories.",
            "review": {k: True for k in ("source", "context", "localization", "naturalness", "formatting")}, **extra})

    records = json.loads(Path("work/analysis/village_location_v606/original_village_records.json").read_text(encoding="utf-8"))["records"]
    for record, english in zip(records, NAMES, strict=True):
        index, pointer = record["id"], record["name_pointer"]
        field = 0x15AFB0 + index * 44
        encoded = record["source_name"].encode("cp932") + b"\0"
        assert struct.unpack_from("<I", source, field)[0] == pointer
        assert struct.unpack_from("<I", baked, field)[0] == pointer
        assert source[pointer - 0x02000000:pointer - 0x02000000 + len(encoded)] == encoded
        assert baked[pointer - 0x02000000:pointer - 0x02000000 + len(encoded)] == encoded
        point = list(struct.unpack_from("<2i", source, field + 4))
        add(f"VILLAGE_NAME_{index}", english, record["source_name"],
            "The original place name " + record["source_name"] + ".",
            f"Village {index}; original 44-byte descriptor copied into the 52-byte native village model. Discovery/docking substitute its name getter.",
            kind="name", index=index, pointer_field=field, source_pointer=pointer, source_hex=encoded.hex(),
            original_map_point=point)
    for index, (japanese, english, offset) in enumerate(MENU):
        field = 0x119248 + index * 16
        encoded = japanese.encode("cp932") + b"\0"
        assert struct.unpack_from("<I", source, field)[0] == 0x02000000 + offset
        assert source[offset:offset + len(encoded)] == baked[offset:offset + len(encoded)] == encoded
        gloss = ["Replenish supplies.", "Stay at the lodging; no fixed duration is added to the label.",
                 "Repair the ship.", "Recruit sailors.", "Depart the village by sea.",
                 "Enter the promised words."][index]
        add(f"VILLAGE_MENU_{index}", english, japanese, gloss,
            "Original village dock menu; preserve the six action IDs, ordering and callbacks.",
            kind="menu", index=index, pointer_field=field, source_pointer=0x02000000 + offset,
            source_hex=encoded.hex())
    original_blocks, baked_blocks, current_blocks = [IlnkContainer.parse(r.read_file("/data/SC2.DK4")).blocks
                                                    for r in (source_rom, canonical, current)]
    for block, record in ((247, 9), (248, 12), (248, 18)):
        source_row = original_blocks[block].split(b"\0")[record]
        baked_row = baked_blocks[block].split(b"\0")[record]
        current_row = current_blocks[block].split(b"\0")[record]
        assert source_row == baked_row and "レバキュー".encode("cp932") in source_row
        assert current_row.count(b"Lebaque") == 1 and current_row[0] == source_row[0]
        parts = original_blocks[block].split(b"\0")
        add(f"VILLAGE_ROUTE_NAME_B{block}_R{record}", "Leveque", source_row[1:].decode("cp932"),
            "This occurrence names レバキュー, the village east across the Indian Ocean / south of Southeast Asia.",
            "Existing translated Lil survey dialogue. Correct only the seven-byte proper name; retain every existing speaker/layout byte and all other prose. This is not a new paragraph translation or approval of older wording.",
            kind="route-name", file_path="/data/SC2.DK4", block=block, record=record,
            source_hex=source_row.hex(), canonical_hex=baked_row.hex(), current_hex=current_row.hex(),
            neighboring_source_hex=[p.hex() for p in parts[max(0, record - 1):record + 2]])
    packet = {"format": "dk4-village-ui-manuscript-v1", "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US", "encoder": "dialogue-relocatable-v1",
        "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
        "records": rows,
        "name_notes": {
            "Cape Cod": "Geographic adaptation of コッド using the Atlantic-coast position and Champlain clue; the NPS documents Champlain's Cape Cod exploration.",
            "Forel": "Source-faithful spelling. Southeastern Greenland at the game's N65 W39 is not Cape Farewell (about N60 W44); do not rename it. Mont Forel supports a regional spelling but does not prove the fictional village's identity.",
            "Leveque": "Original village/quest position near S16 E122 matches Cape Leveque. Retain unqualified village label Leveque, and correct the prior unsupported Lebaque spelling in three active story occurrences.",
            "Korf": "Bering Sea/Kamchatka village at the source location; not Corfu in Greece.",
            "Wanganui": "Retain the game's historical spelling; Wanganui and Whanganui are recognized alternative city names. Do not substitute a modern spelling just because the district later changed.",
            "Ezo": "Retain the original historical name rather than replacing it with Hokkaido."},
        "references": ["https://www.inuvik.ca/discovering-inuvik/about-inuvik/",
            "https://www.nps.gov/caco/learn/historyculture/samuel-de-champlain.htm",
            "https://www.bom.gov.au/climate/averages/tables/cw_003004_Info.shtml",
            "https://www.amsa.gov.au/amsa-heritage-strategy-2022-2025/heritage-places-1-3",
            "https://eng.geus.dk/media/13684/nr18_001-126.pdf",
            "https://www.linz.govt.nz/consultations/whanganui",
            "https://ns.kamlib.ru/upload/medialibrary/439/vnkwjocij3gn40nt74i5ah7qzb3rcso2/adm-ter-ustr.pdf"],
        "geographic_identification_is_inference_from_source_name_location_and_clue": True}
    validate_natural_dialogue_batch(packet)
    save(MANUSCRIPT, packet)
    save(ROOT / "source_packet_proof.json", {"manuscript_sha256": sha(MANUSCRIPT.read_bytes()),
        "records": len(rows), "UI_names_and_labels": 30, "same_width_story_name_corrections": 3})
    print("Prepared 24 place names,6 original menu labels and3 scoped seven-byte story name corrections.")


if __name__ == "__main__":
    main()
