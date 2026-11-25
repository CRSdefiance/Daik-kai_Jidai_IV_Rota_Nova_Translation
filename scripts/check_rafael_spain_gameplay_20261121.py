"""Check the live menus and both pages of Pereira's instruction in the fixture."""

from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as panel
from scripts import replay_rafael_spain_20261121 as replay
from scripts import verify_rafael_spain_20261121 as display
from scripts.check_hodram_B91_B110_actual_pixels import match


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay.json"
MENU_FRAMES = {768: (4380, 4550, 4680), 1852: (5360, 5560)}
SPEECH = [(3900, 71, 1), (4208, 75, 1), (4940, 177, 1), (5170, 182, 1),
          (5950, 474, 1), (6230, 486, 1), (6530, 486, 2), (6830, 489, 1)]


def verify_menu(receipt, arm, paint, pictures, captures):
    vm = receipt["captions"]["stored"]
    width = vm["minimum_width_units"] * 6
    x, y = vm["native_menu_rectangle"][:2]
    source = receipt["source_command_offset"]
    expected = (None, 1, 0) if source == 768 else (0, 1)
    masks = []
    for index, label in enumerate(vm["labels"]):
        plane, _ = paint(arm, label.encode("ascii"), 1, width, (0, index * 12))
        expected_plane = receipt["planes"][index * 2]
        assert expected_plane["style"] == 1 and native.digest(plane) == expected_plane["plane_sha256"]
        masks.append({(i % width, i // width) for i, ink in enumerate(plane) if ink})
    samples = []
    for frame, selected in zip(MENU_FRAMES[source], expected, strict=True):
        image = pictures[frame]
        highlights = []
        for index, ink in enumerate(masks):
            px, py = x + 16, 192 + y + 16 + index * 20
            assert match(image, ink, (8, 8, 8), [px], [py]) == [px, py]
            background = {image.getpixel((a, b)) for a in range(px, px + width)
                          for b in range(py - 4, py + 16) if (a - px, b - py) not in ink}
            assert background in ({(205, 198, 180)}, {(0, 165, 172)}), (source, frame, index, background)
            if background == {(0, 165, 172)}:
                highlights.append(index)
        assert highlights == ([] if selected is None else [selected]), (source, frame, highlights, selected)
        samples.append(dict(command_offset=source, frame=frame, highlight=selected, captions=vm["labels"],
                            observed=captures[frame], full_glyph_masks_and_background_exact=True))
    return samples


def main():
    assert not PROOF.exists()
    fixture_path = replay.ROOT / "fixture.json"
    inputs = replay.ROOT / "inputs.json"
    fixture, report, checked, draft = map(base.load, (fixture_path, replay.REPORT, display.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == checked["candidate_sha256"] == fixture["candidate_sha256"]
    assert candidate == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["original_menu_objects_copied_byte_exact"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == replay.END
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)
    rom = base.NdsImage.open(stage.ROM)
    block = native.IlnkContainer.parse(rom.read_file(replay.PATH)).blocks[60]
    assert all(block[x["actual_block_offset"]:][:len(bytes.fromhex(x["hex"]))].hex() == x["hex"]
               for x in fixture["copied"])
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = panel.panel.GameAsciiFont.from_arm9(arm)
    captures = {x["frame"]: x for x in report["frames_captured"] if x["path"].endswith("_cold_boot.png")}
    pictures = {f: town.read_frame(captures, f)[1] for f in replay.FRAMES}
    _, menu_painter, _ = display.menu.adapters(arm)
    menus = [sample for menu in checked["menus"] for sample in verify_menu(menu, arm, menu_painter, pictures, captures)]
    rows = {row["id"]: row for row in draft["records"]}
    proof = {row["id"]: row for row in checked["records"]}
    holds = []
    for frame, index, page in SPEECH:
        ident = f"DK4_MES_B60_R{index:04d}"
        layout = proof[ident]["layouts"][0]
        rendered = paint(arm, font, bytes.fromhex(layout["expanded_hex"]))["pages"][page - 1]
        native_body = bytes.fromhex(rendered["native_plane_hex"])
        assert native.digest(native_body) == layout["pages"][page - 1]
        assert panel.panel.mask_check(native_body, 216, pictures[frame]), (ident, page, frame)
        speaker = rows[ident]["speaker"]
        panel.panel.complete_mask(name_font, speaker, pictures[frame], 16, 277, town.INKS[1])
        holds.append(dict(id=ident, frame=frame, page=page, speaker=speaker, observed=captures[frame]))
    last = captures[replay.FRAMES[-1]]
    frames = [(r["frame"], f"{r['id']} page {r['page']}") for r in holds]
    frames += [(r["frame"], f"Menu {r['command_offset']}, " +
                (f"choice {r['highlight'] + 1}" if r["highlight"] is not None else "cursor blink")) for r in menus]
    frames.append((last["frame"], "After the fixture"))
    sheets = []
    ordered = [(label, pictures[frame]) for frame, label in sorted(frames)]
    for i in range(0, len(ordered), 6):
        path = replay.ROOT / f"spain_gameplay_{i // 6 + 1}.png"
        town.sheet(ordered[i:i + 6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    on_screen = {r["id"] for r in holds}
    on_screen |= {ident for m in checked["menus"] for ident in m["record_ids"]}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, menus=menus, final_hold=last,
        both_pages_and_next_speech_observed=True, original_story_branches_unvisited=True,
        observed_ids=sorted(on_screen),
        offline_only=[r["id"] for r in rows.values() if r["decision"] == "revision" and r["id"] not in on_screen],
        sheets=sheets, evidence={str(path): base.digest(path) for path in
                                 (fixture_path, replay.REPORT, inputs, display.PROOF, fixture["fixture_ROM"])}))
    print("Verified both live menu highlights, eight complete speech pages including the page turn, and the next speech.")


if __name__ == "__main__":
    main()
