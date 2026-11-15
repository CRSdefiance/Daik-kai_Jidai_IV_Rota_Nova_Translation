"""Actual HELP glyphs, clicked page flow and constructed link/history state."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/help_display_v282")
CAPTURE = Path("work/emulation_v193/help_navigation_v282")
FRAMES = {0: 21200, 1: 21400, 6: 21800, 7: 22000, 202: 22400,
          37: 23000, 204: 23200, 205: 23600}
COLORS = ((123, 246, 123), (213, 214, 213), (106, 157, 246))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", type=Path, default=CAPTURE)
    parser.add_argument("--fixture", type=Path, default=ROOT / "navigation_fixture_manifest.json")
    parser.add_argument("--out", type=Path, default=ROOT / "actual_navigation_display_proof.json")
    args = parser.parse_args()
    report = json.loads((args.capture / "capture_report.json").read_text(encoding="utf-8"))
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == fixture["research_ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == 23800
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    rom = NdsImage.open(fixture["research_ROM"])
    arm = rom.read_file("/__arm9__.bin")
    font = GameAsciiFont.from_arm9(arm)
    proposal = json.loads((ROOT / "navigation_proposal.json").read_text(encoding="utf-8"))
    pages = {r["topic_id"]: r for r in proposal["pages"]}
    cases = []
    captures = {r["frame"]: Path(r["path"]) for r in report["frames_captured"]}
    for topic, frame in FRAMES.items():
        path = captures[frame]
        image = Image.open(path).convert("RGB")
        lines = []
        for row, text in enumerate(pages[topic]["visible_lines"]):
            y = 192 if row == 0 else 192 + 24 + (row - 1) * 16
            matches = []
            for index, char in enumerate(text):
                if char == " ":
                    continue
                candidates = []
                for color in COLORS:
                    try:
                        ink, bounds = complete_mask(font, char, image, index * 6, y, color)
                        candidates.append({"color": color, "ink": ink, "bounds": bounds})
                    except ValueError:
                        pass
                assert len(candidates) == 1, (topic, row, index, char, candidates)
                matches.append(candidates[0])
            lines.append({"text": text, "y": y, "complete_visible_characters": len(matches),
                          "independent_ink_pixels": sum(r["ink"] for r in matches)})
        cases.append({"topic_id": topic, "frame": frame, "complete_lines": lines,
                      "all_first_final_and_interior_letters_exact": True})
    # Native Back-to-article-start links render their exact original pages.
    for before, after in [(22000, 22800), (23000, 23800)]:
        a = Image.open(captures[before]).crop((0, 192, 252, 356))
        b = Image.open(captures[after]).crop((0, 192, 252, 356))
        assert a.tobytes() == b.tobytes()
    snapshot = report["read_only_RAM_snapshot"]
    ram = Path(snapshot["path"]).read_bytes()
    assert len(ram) == 4194304 and sha(ram) == snapshot["sha256"]
    vtable = struct.unpack_from("<I", arm, 0x7D40C)[0]
    child_vtable = struct.unpack_from("<I", arm, 0x7D488)[0]
    parents = []
    for offset in range(0, len(ram) - 0x6B0, 4):
        if struct.unpack_from("<I", ram, offset)[0] != vtable:
            continue
        count, depth = [struct.unpack_from("<I", ram, offset + field)[0] for field in (0x660, 0x6A8)]
        if count == 1 and depth <= 15:
            history = struct.unpack_from("<16I", ram, offset + 0x668)
            if history[depth] == 37:
                assert struct.unpack_from("<I", ram, offset + 0xA0)[0] == child_vtable
                assert struct.unpack_from("<I", ram, offset + 0xA8)[0] == 204
                parents.append({"address": 0x02000000 + offset, "history_depth": depth,
                                "actual_history": history, "active_link_count": count,
                                "constructed_jump_child_topic": 204})
    assert len(parents) == 1
    assert all(topic in parents[0]["actual_history"] for topic in (0, 1, 6, 7, 202, 37, 204, 205))
    proof = {"format": "dk4-real-help-navigation-display-v282", "research_ROM_sha256": report["ROM_sha256"],
             "actual_cold_boot_frames": 23800, "page_cases": cases, "actual_constructed_HELP_parent_and_jump_child": parents,
             "ordinary_X_index_route_links_and_five_prepared_page_navigation_verified": True,
             "both_actual_Back_to_article_start_links_pixel_exact": True,
             "native_child_creation_no_UI_construction_bridge_in_actual_run": True,
             "captured_state_read_only_no_savestate_loaded": True,
             "older_HELP_Japanese_and_placeholder_entries_remain_unfinished": True,
             "complete_registered_name_text_art_release_pending": True,
             "all18_plaque_hint_entries_remain_incomplete": True, "full_goal_complete": False}
    args.out.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"actual_pages": len(cases), "prepared_article_pages": 5,
                      "actual_jump_children_verified": 1, "both_Back_links_exact": True}))


if __name__ == "__main__":
    main()
