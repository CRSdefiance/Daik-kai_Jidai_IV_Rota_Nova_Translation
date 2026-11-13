"""Restore source HELP index/World/character links removed by older placeholders."""

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_help_pages_v281 import encoded_line, wrap

ROOT = Path("work/analysis/help_display_v282")
DEFINITIONS = {
    0: ("Help Index", ["[[1|The World of Uncharted Waters IV]]", "[[11|Town Commands]]",
                       "[[82|Commands at Sea]]", "[[103|Shared Commands]]", "[[143|Data Guide]]",
                       "[!] marks helpful tips worth knowing."]),
    1: ("The World of Uncharted Waters IV", ["An overview of Uncharted Waters IV and the goals of the game.",
                                           "[[2|Game Overview]]", "[[3|Game Goals]]",
                                           "[[6|Choosing a Captain]]", "[[10|Game Over]]"]),
    6: ("Choosing a Captain", ["At first, you can choose from three captains.",
                              "Each captain has different benefits and a different level of difficulty.",
                              "[[7|Rafael Castor]]", "[[8|Lil Argot]]", "[[9|Hodram Joakim Bergstrom]]"]),
}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open("work/clean.nds")
    clean = IlnkContainer.parse(source.read_file("/COMMON/HELP.DK4"))
    raw = Path("work/analysis/help_consumers_v281/help_research_only.bin").read_bytes()
    container = IlnkContainer.parse(raw)
    before = list(container.blocks)
    pages, records = [], []
    for topic, (heading, sections) in DEFINITIONS.items():
        lines = wrap(heading)
        for text in sections:
            lines.extend(wrap(text))
        assert len(lines) <= 10
        encoded, visible, links = bytearray(), [], []
        for row, line in enumerate(lines):
            data, text, refs = encoded_line(line)
            encoded.extend(data + b"\n")
            visible.append(text)
            links.extend({**ref, "row": row} for ref in refs)
        encoded.extend(b"\0")
        source_ids = []
        source_bytes = clean.blocks[topic]
        cursor = 0
        while cursor < len(source_bytes) and source_bytes[cursor]:
            first = source_bytes[cursor]
            if 0x81 <= first <= 0x9F or 0xE0 <= first <= 0xFC:
                cursor += 2
            elif first == 123:
                colon = source_bytes.index(b":", cursor)
                assert source_bytes[colon + 2] == 125
                source_ids.append(source_bytes[colon + 1])
                cursor = colon + 3
            else:
                cursor += 1
        assert [link["id"] for link in links] == source_ids
        container.blocks[topic] = bytes(encoded)
        pages.append({"topic_id": topic, "source_article_id": topic, "page_number": 1, "page_count": 1,
                      "visible_lines": visible, "links": links, "encoded_hex": encoded.hex(), "bytes": len(encoded)})
        records.append({"topic_id": topic, "source_hex": clean.blocks[topic].hex(),
                        "source_Japanese": clean.blocks[topic].split(b"\0")[0].decode("cp932", errors="replace"),
                        "heading": heading, "sections": sections,
                        "source_meaning": "Preserve original HELP navigation, topic links, overview and initial three-captain/difficulty-benefits explanation.",
                        "review": {"source": True, "context": True, "localization": True, "naturalness": True, "formatting": False}})
    for topic, (left, right) in enumerate(zip(before, container.blocks, strict=True)):
        if topic not in DEFINITIONS:
            assert left == right
    saved = container.to_bytes()
    (ROOT / "help_navigation_research_only.bin").write_bytes(saved)
    previous = json.loads(Path("work/analysis/help_consumers_v281/page_proposal.json").read_text(encoding="utf-8"))
    proposal = {**previous, "format": "dk4-help-navigation-proposal-v282", "source_prior_HELP_sha256": sha(raw),
                "target_HELP_sha256": sha(saved), "source_reviewed_navigation_records": records,
                "pages": previous["pages"] + pages, "only_extra_topics0_1_6_changed": True}
    (ROOT / "navigation_proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Source-faithful navigation topics0/1/6 regenerated; other prepared/original topics exact.")


if __name__ == "__main__":
    main()
