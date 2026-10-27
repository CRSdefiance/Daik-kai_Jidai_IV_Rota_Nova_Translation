"""Preserve complete reviewed HELP prose and links in native ten-row pages."""

import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/help_consumers_v281")
WIDTH = 41  # Native42-cell rows retain room for an invisible final pair guard.
LINK = re.compile(r"\[\[([0-9]+)\|([^\]]+)\]\]")


def words(text):
    result = []
    for part in re.split(r"(\[\[[0-9]+\|[^\]]+\]\])", text):
        match = LINK.fullmatch(part)
        if match:
            result.append({"label": match[2], "id": int(match[1])})
        else:
            punctuation = re.match(r"^[.,;:!?]+", part)
            if punctuation and result and isinstance(result[-1], dict):
                result[-1]["label"] += punctuation[0]
                part = part[len(punctuation[0]):]
            result.extend(part.split())
    return result


def wrap(text):
    rows, line, length = [], [], 0
    for token in words(text):
        width = len(token["label"] if isinstance(token, dict) else token)
        assert width <= WIDTH
        if length + bool(line) + width > WIDTH:
            rows.append(line)
            line, length = [], 0
        length += bool(line) + width
        line.append(token)
    if line:
        rows.append(line)
    return rows


def encoded_line(tokens):
    result, plain = bytearray(), ""
    visible, links = [], []
    for index, token in enumerate(tokens):
        separator = " " if index else ""
        if isinstance(token, str):
            plain += separator + token
            visible.append(separator + token)
        else:
            plain += separator
            label = token["label"]
            visible.append(separator + label)
            if len(plain) % 2:
                assert plain.endswith(" ")
                plain = plain[:-1]
                label = " " + label
            result.extend(plain.encode("ascii"))
            plain = ""
            assert token["id"] != 203 and 0 <= token["id"] <= 255
            result.extend(b"{" + label.encode("ascii") + b":" + bytes([token["id"]]) + b"}")
            links.append({"label": label, "id": token["id"], "navigation": token.get("navigation", False)})
    if len(plain) % 2:
        plain += " "
    result.extend(plain.encode("ascii"))
    assert len("".join(visible)) <= WIDTH
    return bytes(result), "".join(visible), links


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open("out/all_routes_combined_v275_candidate.nds")
    raw = current.read_file("/COMMON/HELP.DK4")
    container = IlnkContainer.parse(raw)
    old = [bytes(b) for b in container.blocks]
    assert len(old) == 202
    manuscript = json.loads(Path("translations/confirmed_name_help_manuscript_v1.json").read_text(encoding="utf-8"))
    next_id = 202
    pages, articles = [], []
    for article in manuscript["records"]:
        original_id = int(article["id"].split("_B")[1].split("_")[0])
        title = article["sections"][0]["english"]
        groups = [wrap(title)]
        benefit = 0
        source_links = []
        for section in article["sections"][1:]:
            text = section["english"]
            if original_id == 7:
                text = text.replace("Military investment", "[[37|Military investment]]")
                text = text.replace("Influence", "[[184|Influence]]")
            else:
                text = text.replace("city's total market share", "city's total [[150|market share]]")
                text = text.replace("at war", "[[187|at war]]")
            if section["role"] == "advantage":
                benefit += 1
                text = f"[Benefit {benefit}] " + text
            groups.append(wrap(text))
        queue = list(groups)
        batches = []
        first = True
        while queue:
            heading = [] if first else wrap(("Rafael Castor" if original_id == 7 else "Military Investment") + " (continued)")
            content = list(heading)
            while queue and len(content) + len(queue[0]) <= 9:
                content.extend(queue.pop(0))
            if len(content) == len(heading) and queue:
                # A larger semantic section may span pages, but its prose and
                # word boundaries remain complete.
                take = 9 - len(content)
                content.extend(queue[0][:take])
                queue[0] = queue[0][take:]
            batches.append(content)
            first = False
        ids = [original_id]
        for _ in batches[1:]:
            if next_id == 203:
                next_id += 1
            ids.append(next_id)
            next_id += 1
        for i, batch in enumerate(batches):
            semantic_batch = batch if i == 0 else batch[len(wrap(("Rafael Castor" if original_id == 7 else "Military Investment") + " (continued)")):]
            semantic_lines = [encoded_line(line)[1] for line in semantic_batch]
            nav_id = ids[i + 1] if i + 1 < len(ids) else original_id
            if len(ids) > 1:
                batch.append([{"label": "Continue reading" if i + 1 < len(ids) else "Back to article start", "id": nav_id, "navigation": True}])
            assert len(batch) <= 10
            data, text_lines, link_rows = bytearray(), [], []
            for row_number, line in enumerate(batch):
                encoded, visible, links = encoded_line(line)
                data.extend(encoded + b"\n")
                text_lines.append(visible)
                for link in links:
                    link_rows.append({**link, "row": row_number})
                    if not link["navigation"]:
                        source_links.append(link["id"])
            data.extend(b"\0")
            assert len(data) < 1024
            while len(container.blocks) <= ids[i]:
                container.blocks.append(b"\0")
            container.blocks[ids[i]] = bytes(data)
            pages.append({"topic_id": ids[i], "source_article_id": original_id,
                          "page_number": i + 1, "page_count": len(ids), "visible_lines": text_lines,
                          "semantic_content_lines": semantic_lines,
                          "links": link_rows, "encoded_hex": data.hex(), "bytes": len(data)})
        assert source_links == ([37, 184] if original_id == 7 else [150, 187])
        original_words = []
        benefit_number = 0
        for section in article["sections"]:
            text = section["english"]
            if section["role"] == "advantage":
                benefit_number += 1
                text = f"[Benefit {benefit_number}] " + text
            original_words.append(text)
        rendered_words = " ".join(line for page in pages if page["source_article_id"] == original_id
                                  for line in page["semantic_content_lines"])
        assert rendered_words == " ".join(original_words)
        articles.append({"source_article_id": original_id, "topic_pages": ids,
                         "all_reviewed_sections_words_and_original_cross_reference_IDs_retained": True})
    for index, block in enumerate(old):
        if index not in (7, 37):
            assert container.blocks[index] == block
    assert container.blocks[203] == b"\0"  # Native history sentinel is never a topic.
    saved = container.to_bytes()
    assert IlnkContainer.parse(saved).blocks == container.blocks
    (ROOT / "help_research_only.bin").write_bytes(saved)
    proof = {"format": "dk4-structured-help-page-proposal-v281", "source_HELP_sha256": sha(raw),
             "target_HELP_sha256": sha(saved), "native_original_topic_count": len(old),
             "target_topic_count": len(container.blocks), "articles": articles, "pages": pages,
             "all200_unrelated_original_blocks_exact": True, "native203_history_sentinel_preserved": True,
             "native_ascii_pair_control_boundaries_encoded_without_visible_extra_spaces": True,
             "native_parser_loader_complete_pixels_navigation_and_actual_display_pending": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "page_proposal.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "topics": len(container.blocks), "max_page_bytes": max(p["bytes"] for p in pages),
                      "articles": articles}))


if __name__ == "__main__":
    main()
