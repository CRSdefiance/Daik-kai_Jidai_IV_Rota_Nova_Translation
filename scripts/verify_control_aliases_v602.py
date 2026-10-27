"""Verify current English masks and discovered archive-copy synchronization."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.compact_font import layout
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.frame_buttons_v165 import atlas_indices
from scripts.probe_button_prompt_native import call, machine
from scripts.scan_graphic_template_aliases_v602 import ROOT, TEMPLATES


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    proof_paths = [ROOT / n for n in ("decoded_template_alias_proof.json", "embedded_control_alias_proof.json")]
    loose, embedded = [read(p) for p in proof_paths]
    assert loose["script_sha256"] == sha(Path("scripts/scan_graphic_template_aliases_v602.py").read_bytes())
    assert embedded["script_sha256"] == sha(Path("scripts/scan_embedded_control_aliases_v602.py").read_bytes())
    assert embedded["loose_template_proof_sha256"] == sha(proof_paths[0].read_bytes())
    assert loose["stats"]["PXL_files"] == 660 and loose["stats"]["FLS_textures"] == 261
    assert loose["stats"]["decoded_domains"] == 1313 and loose["stats"]["distinct_indexed_textures_shape_searched"] == 879
    assert len(loose["matches"]) == 7 and not loose["matches_outside_declared_crops"]
    assert len(embedded["matches"]) == 5 and embedded["stats"]["embedded_blocks_visited"] == 57
    assert all(m["path"] == "/GRP/CMMNIMG.DK4" and m["block"] == 5 and m["compared_bits"] == 0
               for m in embedded["matches"])
    rom = NdsImage.open(loose["candidate"])
    assert sha(rom.source.read_bytes()) == loose["candidate_sha256"] == embedded["candidate_sha256"]
    clean, historical = NdsImage.open("work/clean.nds"), NdsImage.open("out/all_routes_combined_v573_candidate.nds")
    for path in ("/_pxl/__frame.pxl", "/_pxl/kakutei.pxl"):
        assert rom.read_file(path) == historical.read_file(path)
    atlas = PxlImage.from_bytes(rom.read_file("/_pxl/__frame.pxl"))
    source_atlas = PxlImage.from_bytes(clean.read_file("/_pxl/__frame.pxl"))
    archive = atlas_indices(rom.read_file("/GRP/CMMNIMG.DK4"))
    batch = read("translations/frame_action_buttons_graphics_v7.json")
    cases = []
    sheet = Image.new("RGB", (1030, 530), (35, 43, 50))
    draw = ImageDraw.Draw(sheet)
    for x, text in ((5, "Original loose crop"), (345, "Current loose crop"),
                    (685, "Embedded INDEX mask; native palette unproved")):
        draw.text((x, 8), text, fill="white")
    for number, match in enumerate(embedded["matches"]):
        name = match["template"]
        source_box = next(box for template, _, box in TEMPLATES if template == name)
        left, top, right, bottom = source_box
        target_box = match["box"]
        assert target_box == [left + 256, top, right + 256, bottom]
        english = name.replace("_", " ")
        row = next(r for r in batch["records"] if r["text"] == english and r.get("font_face") == "compact-en-7px-v1")
        box = row.get("draw_box", row["box"])
        l, t, r, b = box
        mask, _, _ = layout(english, tuple(box), word_space_width=row.get("compact_word_space_width", 2), font_face=row["font_face"])
        expected = {(l + x, t + y) for y in range(b - t) for x in range(r - l) if mask.getpixel((x, y))}
        actual = {(x, y) for y in range(top, bottom) for x in range(left, right) if atlas.indices[y * 256 + x] == 9}
        assert actual == expected
        assert all(atlas.indices[y * 256 + x] in (0, 9) for y in range(top, bottom) for x in range(left, right))
        current_crop = bytes(atlas.indices[y * 256 + x] for y in range(top, bottom) for x in range(left, right))
        copied_crop = bytes(archive[y * 512 + x + 256] for y in range(top, bottom) for x in range(left, right))
        assert current_crop == copied_crop
        cases.append({"English": english, "source_box": list(source_box), "embedded_box": target_box,
                      "current_complete_compact_font_ink_pixels": len(expected),
                      "whole_loose_embedded_index_crop_exact": True, "palette_or_native_consumer_equivalence_not_inferred": True})
        draw.text((5, 43 + number * 94), english, fill="white")
        for x, image in ((5, source_atlas.render().crop(source_box).convert("RGB")),
                         (345, atlas.render().crop(source_box).convert("RGB"))):
            sheet.paste(image.resize((image.width * 5, image.height * 5), Image.Resampling.NEAREST), (x, 63 + number * 94))
        index_mask = Image.new("RGB", (right - left, bottom - top))
        index_mask.putdata([(255, 255, 255) if value == 9 else (0, 0, 0) for value in copied_crop])
        sheet.paste(index_mask.resize((index_mask.width * 5, index_mask.height * 5), Image.Resampling.NEAREST), (685, 63 + number * 94))
    assert sum(c["current_complete_compact_font_ink_pixels"] for c in cases) == 307
    sheet_path = ROOT / "source_current_embedded_index_review.png"
    sheet.save(sheet_path)
    confirm = PxlImage.from_bytes(rom.read_file("/_pxl/kakutei.pxl"))
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    ink = {(6 + n * 5 + x, 3 + y) for n, char in enumerate("Confirm") for y in range(2, 11)
           for x in range(5) if font.decode(char).getpixel((x, y))}
    assert len(ink) == 86
    assert ink == {(x, y) for y in range(20) for x in range(48) if confirm.indices[y * 48 + x] == 13}
    u = machine(rom.read_file("/__arm9__.bin"))
    call(u, 0x10E190, (), instruction_limit=1000000)
    name_pointer = struct.unpack("<I", u.mem_read(0x023139C0 + 12, 4))[0]
    assert bytes(u.mem_read(name_pointer, 64)).split(b"\0")[0] == b"_pxl/kakutei.pxl"
    assert sha(rom.source.read_bytes()) == loose["candidate_sha256"]
    save(ROOT / "current_control_copy_proof.json", {"candidate": str(rom.source), "candidate_sha256": loose["candidate_sha256"],
        "source_alias_proofs": {str(p): sha(p.read_bytes()) for p in proof_paths},
        "all921_PXL_FLS_entries_1313_palette_domains_and879_indexed_shapes_examined": True,
        "all57_embedded_blocks_visited_31_legacy_packets_and3_external_pairs_decoded": True,
        "five_automatically_detected_embedded_index_aliases": cases,
        "all307_current_miniature_ink_pixels_and_complete_embedded_crops_exact": True,
        "Confirm_complete86_point_English_mask_and_original_initialized_filename_exact": True,
        "both_control_atlases_byte_identical_to_prior_native_V573": True,
        "no_additional_exact_Confirm_template_alias_found_in_declared_decoders": True,
        "comparison_sheet": str(sheet_path), "comparison_sheet_sha256": sha(sheet_path.read_bytes()),
        "comparison_sheet_is_source_index_analysis_not_native_screenshot": True,
        "limits": "No new ordinary parent, native palette/alpha, rescaled/recolored/partial alias, arbitrary runtime composition or raw/headerless-block clearance is claimed.",
        "production_ROM_patch_or_graphics_changed": False, "all18_plaques_incomplete_and22_historical_objects_retained": True,
        "full_goal_complete": False, "script_sha256": sha(Path(__file__).read_bytes())})
    print("V602:921 entries/1313 color domains/879 indexed shapes;57 blocks;5 embedded controls synchronized;307 mini/86 Confirm ink points;ordinary parents remain open.")


if __name__ == "__main__":
    main()
