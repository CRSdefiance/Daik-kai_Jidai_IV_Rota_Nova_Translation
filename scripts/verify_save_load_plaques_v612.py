"""Complete Save/Load source frames, actual resource/getter/pixels and normal load."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.save_load_plaques import DONOR, FILE, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, report, save

ROOT = Path("work/analysis/save_load_plaques_v612")
ROM = Path("out/all_routes_combined_v612_candidate.nds")
PARENT = Path("out/all_routes_combined_v611_candidate.nds")
CAP = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ACTIVE = (6200, 7400, 7800, 8200, 8600, 9000, 9400, 9800, 10200, 10600,
          11000, 11400, 11800, 12200, 12600, 13000, 13400, 13800)
PREVIEWS = (11000, 11400, 11800, 12200, 12600, 13000)
SAVE_SHA = "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"


def snapshot(run, frame):
    rows = run.get("read_only_capture_RAM_snapshots", []) + run.get("read_only_pause_RAM_snapshots", [])
    row = next(r for r in rows if r["frame"] == frame)
    raw = Path(row["path"]).read_bytes()
    assert row["read_only_export"] and len(raw) == 0x400000 and sha(raw) == row["sha256"]
    return raw


def main():
    parent, rom, clean = [NdsImage.open(p) for p in (PARENT, ROM, "work/clean.nds")]
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == [FILE]
    expected, transform = apply_release(parent, clean, "translations/save_load_plaques_v1.json")
    assert expected[FILE] == new[FILE] and len(transform["records"]) == 2
    manifest, previous, stack = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json")), read("translations/release_stack.json")
    digest = sha(ROM.read_bytes())
    assert manifest["candidate_sha256"] == digest and manifest["profile"] == "all-routes-unified-v612"
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["base_sha256"] == stack["canonical_baseline"]["sha256"] == sha(Path(manifest["base_rom"]).read_bytes())
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == previous["required_batches"] and len(stack["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    atlas, original, donor = [PxlImage.from_bytes(d) for d in (new[FILE], clean.read_file(FILE), clean.read_file(DONOR))]
    assert atlas.source[:atlas.pixels_offset] == original.source[:original.pixels_offset]
    font = GameAsciiFont.from_arm9(new["/__arm9__.bin"])
    all_owned, masks = set(), []
    for row in transform["records"]:
        l, t, r, b = row["original_and_final_plaque_box"]
        text = row["English"]
        x0, y0 = l + (40 - len(text) * 5) // 2, t + 2
        ink = {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(text)
               for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        actual = {(x, y) for y in range(t + 2, b - 2) for x in range(l + 2, r - 2)
                  if atlas.indices[y * 256 + x] == 1}
        assert ink == actual and len(ink) == row["complete_native_font_ink"]
        negatives = []
        for i in (0, len(text) - 1):
            end = {(x0 + i * 5 + x, y0 + y) for y in range(11) for x in range(6)
                   if font.decode(text[i]).getpixel((x, y))}
            assert end and actual - end != ink
            negatives.append(len(end))
        for y in range(t, b):
            for x in range(l, r):
                if l + 2 <= x < r - 2 and t + 2 <= y < b - 2:
                    if (x, y) not in ink:
                        rgb = donor.palette[donor.indices[(62 + y - t - 2) * 256 + 3 + x - l - 2]]
                        mapped = min((i for i in range(256) if i != 1), key=lambda i: sum((atlas.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
                        assert atlas.indices[y * 256 + x] == mapped
                else:
                    assert atlas.indices[y * 256 + x] == original.indices[y * 256 + x]
        rl, rt, rr, rb = row["restore_box"]
        all_owned.update((x, y) for y in range(rt, rb) for x in range(rl, rr))
        assert all(atlas.indices[y * 256 + x] == original.indices[y * 256 + x]
                   for y in range(rt, rb) for x in range(rl, rr) if not (l <= x < r and t <= y < b))
        masks.append({"English": text, "Japanese": row["Japanese"], "complete_ink_points": len(ink),
                      "first_final_erasure_negative_points": negatives, "frame_source_geometry_exact": [l, t, r, b]})
    make_xdelta(Path("work/clean.nds"), ROM, ROM.with_suffix(".xdelta"))
    apply_xdelta(Path("work/clean.nds"), ROM.with_suffix(".xdelta"), ROOT / "patch_reconstructed.nds")
    assert (ROOT / "patch_reconstructed.nds").read_bytes() == ROM.read_bytes()
    runs, shots, receipts = {}, {}, {}
    for key, path, name in (("old", PARENT, "initial"), ("new", ROM, "current"), ("original", Path("work/clean.nds"), "original")):
        run, frames, receipt = report("save_load_plaques_v612_" + name, 14200, sha(path.read_bytes()))
        assert run["battery_save_preloaded"]["source_sha256"] == SAVE_SHA
        assert sha(Path(run["battery_save_preloaded"]["source"]).read_bytes()) == SAVE_SHA
        assert not any(v for k, v in run.items() if k.startswith("synthetic_"))
        assert run["scripted_input_schedule"] == read(ROOT / "complete_inputs.json")
        runs[key], shots[key], receipts[key] = run, frames, receipt
    assert all(r["core_options"] == runs["old"]["core_options"] for r in runs.values())
    assert shots["old"].keys() == shots["new"].keys() == shots["original"].keys()
    # Original live resource construction, then original getter on each captured
    # actual bitmap view. No supplied cache/header bridge or changed code.
    u = machine(new["/__arm9__.bin"])
    clean_machine = machine(clean.read_file("/__arm9__.bin"))
    assert bytes(u.mem_read(0x0210FA44, 36)) == bytes(clean_machine.mem_read(0x0210FA44, 36))
    u.emu_start(0x0210FA44, 0x0210FA68, count=100)
    assert u.reg_read(UC_ARM_REG_PC) == 0x0210FA68
    owner = u.reg_read(UC_ARM_REG_R0)
    assert owner == 0x02312CDC
    filename = struct.unpack("<I", u.mem_read(owner + 12, 4))[0]
    assert bytes(u.mem_read(filename, 24)).split(b"\0")[0] == b"_pxl/saveloadinfo.pxl"
    # The source constructor initializes a halfword, and the original draw
    # adapters read a halfword. Load mode retains nonzero allocation padding
    # above it; treating all four bytes as a flag was an invalid host assumption.
    for address, opcode in ((0x020D40A0, "b412c6e1"), (0x020D3A5C, "b422d2e1"), (0x020D3C5C, "b422d2e1")):
        assert bytes(u.mem_read(address, 4)) == bytes(clean_machine.mem_read(address, 4)) == bytes.fromhex(opcode)
    bindings, pairs = [], []
    for frame in sorted(shots["new"]):
        before, after = [Image.open(shots[key][frame]["path"]).convert("RGB") for key in ("old", "new")]
        original_shot = Image.open(shots["original"][frame]["path"]).convert("RGB")
        active = frame in ACTIVE
        for y in range(384):
            for x in range(256):
                expected_colour = native5(before.getpixel((x, y)))
                if active and (x, y) in all_owned:
                    expected_colour = native5(atlas.palette[atlas.indices[y * 256 + x]])
                    assert native5(original_shot.getpixel((x, y))) == native5(original.palette[original.indices[y * 256 + x]])
                assert native5(after.getpixel((x, y))) == expected_colour, (frame, x, y)
        if active:
            for key, resource in (("new", new[FILE]), ("original", clean.read_file(FILE))):
                raw = snapshot(runs[key], frame)
                views = []
                for off in range(0x170000, len(raw) - 48, 4):
                    words = struct.unpack_from("<12I", raw, off)
                    if (words[3] == owner and words[7:9] == (0, 0)
                            and words[9] & 0xFFFF == 0 and words[10:12] == (256, 192)):
                        views.append((0x02000000 + off, words))
                assert views, (frame, key, "No actual Save/Load view")
                native = machine(new["/__arm9__.bin"] if key == "new" else clean.read_file("/__arm9__.bin"))
                native.mem_write(0x02000000, raw)
                for address, words in views:
                    call(native, 0xD4170, (address,))
                    header = native.reg_read(UC_ARM_REG_R0)
                    assert bytes(native.mem_read(header, len(resource))) == resource
                    bindings.append({"frame": frame, "variant": key, "view": address, "words": list(words),
                                     "original_resource_owner": owner, "resident_header": header,
                                     "original_flags_halfword": words[9] & 0xFFFF, "retained_upper_padding_halfword": words[9] >> 16,
                                     "entire_named_PXL_sha256": sha(resource), "whole_original_resource_getter_no_bridge": True})
        pairs.append({"frame": frame, "whole_both_screen_native5_pixels_exact": 98304,
                      "active_save_load": active, "complete_restoration_pixels": len(all_owned) if active else 0,
                      "both_source_rims_and_all_English_letters_verified": active})
    # The selected first save is actually loaded through Yes. Original control
    # and V612 must reach identical Stockholm gameplay with the same inputs.
    assert shots["old"][14200]["PNG_sha256"] == shots["new"][14200]["PNG_sha256"]
    market, market_shots, market_receipt = report("save_load_plaques_v612_market", 24100, digest)
    prior, prior_shots, prior_receipt = report("regional_plaques_v611_market", 24100, sha(PARENT.read_bytes()))
    assert market["scripted_input_schedule"] == prior["scripted_input_schedule"] and market["core_options"] == prior["core_options"]
    assert not market.get("battery_save_preloaded") and not any(v for k, v in market.items() if k.startswith("synthetic_"))
    assert market_shots.keys() == prior_shots.keys() and len(market_shots) == 19
    assert all(market_shots[f]["PNG_sha256"] == prior_shots[f]["PNG_sha256"] for f in market_shots)
    preservation = read(ROOT / "preservation_proof.json")
    assert preservation["candidate_sha256"] == digest and preservation["current921_format_palette_extent_checks"]
    assert preservation["all57_embedded_block_extents_exact"]
    sheet = Image.new("RGB", (1000, 310), "#263238")
    draw = ImageDraw.Draw(sheet)
    for col, name in enumerate(("Actual original Japanese", "Actual V611", "Actual V612")):
        draw.text((col * 330 + 8, 8), name, fill="white")
    for n, row in enumerate(transform["records"]):
        l, t, r, b = row["restore_box"]
        draw.text((8, 35 + n * 130), row["English"], fill="#e7d9aa")
        for col, key in enumerate(("original", "old", "new")):
            crop = Image.open(shots[key][6200]["path"]).crop((l - 2, t - 2, r + 2, b + 2)).convert("RGB")
            sheet.paste(crop.resize((crop.width * 5, crop.height * 5), Image.Resampling.NEAREST), (col * 330 + 8, 55 + n * 130))
    sheet.save(ROOT / "actual_source_current_repair_5x.png")
    proof = {"candidate": str(ROM), "candidate_sha256": digest, "profile": manifest["profile"],
             "base": manifest["base_rom"], "base_sha256": manifest["base_sha256"], "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()),
             "exact_clean_patch_reconstruction": True, "only_changed_file_from_V611": FILE,
             "all_code_pool_layout_other_art_and_translations_exact_V611": True,
             "all470_batches114_accepted_layers_retained": True, "transform": transform,
             "independent_complete_font_masks": masks, "all_complete_native_composite_pairs": pairs,
             "native_original_and_current_getter_bindings": bindings, "whole_composite_pixel_positions": len(pairs) * 98304,
             "complete_active_restoration_pixels": len(ACTIVE) * len(all_owned), "all_six_actual_load_previews": list(PREVIEWS),
             "ordinary_Save_Load_cancel_and_existing_slot_load_on_isolated_copy": True,
             "all19_ordinary_market_regression_frames_exact": True, "reports": receipts,
             "market_reports": {"current": market_receipt, "parent": prior_receipt},
             "preservation_proof_sha256": sha((ROOT / "preservation_proof.json").read_bytes()),
             "source_and_copy_save_history_not_new_earned_progress": True,
             "original_halfword_flag_constructor_and_both_draw_read_opcodes_verified": True,
             "inherited_V611_regional_plaques_native_context_still_open": True,
             "all18_original_plaques_remain_incomplete_all22_historical_objects_retained": True,
             "experimental": True, "canonical_promoted": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    save(ROOT / "release_proof.json", proof)
    print(f"V612: two original-frame plaques in{len(ACTIVE)} normal Save/Load states; six previews and actual load; all{len(pairs)} whole screen pairs,19 market frames,full native resource and exact patch pass.")


if __name__ == "__main__":
    main()
