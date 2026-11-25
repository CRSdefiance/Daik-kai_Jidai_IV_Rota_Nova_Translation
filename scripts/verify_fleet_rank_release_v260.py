"""Full inheritance and actual numbered-fleet rank/crop evidence."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.fleet_rank_labels import ROOT
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v260_candidate.nds")
CAPTURE = Path("work/emulation_v193/fleet_rank_v260")
ORIGINAL = Path("work/emulation_v193/live_map_v260")


def main():
    prior = Path("out/all_routes_combined_v258_candidate.nds")
    assert (ROOT / "v258_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    arm = b.read_file("/__arm9__.bin")
    assert arm == (ROOT / "research_arm9.bin").read_bytes()
    m = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    normalize = lambda rows: [r.replace("\\", "/") for r in rows]
    assert normalize(m["batches"]) == normalize(old["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old["required_batches"]
    for path, records in old["changed_records"].items():
        assert set(records) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest and m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    before = json.loads((ORIGINAL / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == 34000 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == before["scripted_input_schedule"]
    prior_frames = {row["frame"]: row for row in before["frames_captured"] if "cold_boot" in row["path"]}
    identical = []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if "cold_boot" in row["path"] and row["frame"] < 34000:
            assert row["PNG_sha256"] == prior_frames[row["frame"]]["PNG_sha256"]
            identical.append(row["frame"])
    image = Image.open(CAPTURE / "frame_034000_final.png").convert("RGB")
    source = Image.open(ORIGINAL / "frame_034000_final.png").convert("RGB")
    mapping = struct.unpack_from("<3340H", arm, 0x125EC4)
    font = b.read_file("/GRP/KANJI.FNT")
    index = mapping.index(int.from_bytes("１".encode("cp932"), "big"))
    cell = font[index * 22:(index + 1) * 22]
    expected = {(84 + x, 60 + y) for y in range(11) for x in range(11)
                if cell[y * 2 + x // 8] & (0x80 >> (x % 8))}
    ascii_font = GameAsciiFont.from_arm9(arm)
    for n, ch in enumerate(" Fleet Admiral"):
        glyph = ascii_font.decode(ch)
        expected |= {(96 + n * 6 + x, 60 + y) for y in range(11) for x in range(6) if glyph.getpixel((x, y))}
    actual = {(x, y) for y in range(60, 71) for x in range(84, 240) if image.getpixel((x, y)) == (230, 230, 230)}
    assert actual == expected and len(actual) == 165
    delta = [(x, y) for y in range(384) for x in range(256) if source.getpixel((x, y)) != image.getpixel((x, y))]
    assert delta and all(132 <= x < 210 and 60 <= y < 73 for x, y in delta)
    assert image.crop((0, 208, 256, 384)).tobytes() == source.crop((0, 208, 256, 384)).tobytes()
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(file).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert not audit["full_plaque_audit_complete"] and len(audit["ongoing_plaque_inventory"]) == 18
        assert all(not row["fully_completed"] for row in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    sheet = Image.new("RGB", (1024, 808), "#333333")
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), "V258: untranslated rank", fill="white")
    draw.text((520, 8), "V260: numbered fleet + Admiral", fill="white")
    sheet.paste(source.resize((512, 768), Image.Resampling.NEAREST), (0, 32))
    sheet.paste(image.resize((512, 768), Image.Resampling.NEAREST), (512, 32))
    sheet.save(ROOT / "rank_review.png")
    proof = {"format": "dk4-fleet-rank-live-v260", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_batches_prior_stages_records_files_art_routes_ARM7_overlays_retained": True,
             "exact_full_V258_reproduction": True, "exact_clean_patch_reconstruction": True,
             "cold_boot_ordinary_input_no_savestate_or_RAM_injection": True, "complete_rank_text": "１ Fleet Admiral",
             "complete_native_fullwidth_digit_and_ASCII_rank_ink_pixels": 165,
             "only_rank_suffix_region_pixels_changed": len(delta), "entire_actual_map_and_controls_unchanged": True,
             "unchanged_whole_frames": identical, "actual_route_map_and_fleet_view_reached": True,
             "actual_displayed_map_rectangle": [6, 208, 250, 368],
             "map_blue_palette_source_parent_or_seamap_copy_equivalence_not_proved": True,
             "native45_formatter_cases_passed_but_two_other_parent_displays_pending": True,
             "all18_plaque_entries_and_variants_incomplete": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"], "complete_actual_rank_pixels": 165, "unchanged_frames": len(identical)}))


if __name__ == "__main__":
    main()
