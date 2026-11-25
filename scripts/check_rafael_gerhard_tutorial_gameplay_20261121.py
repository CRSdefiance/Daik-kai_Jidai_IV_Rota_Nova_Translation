"""Check both actual menu highlights, the battle-instruction pages and the next speaker."""

from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as panel
from scripts import replay_rafael_gerhard_tutorial_20261121 as replay
from scripts import verify_rafael_gerhard_tutorial_20261121 as display
from scripts.check_hodram_B91_B110_actual_pixels import match


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay.json"


def menu_frame(arm, paint, menu, request, captures):
    vm = menu["native_vm_cases"][-1]
    width = vm["minimum_width_units"] * 6
    x, y = vm["native_menu_rectangle"][:2]
    masks = []
    for i, label in enumerate(vm["labels"]):
        plane, _ = paint(arm, label.encode("ascii"), 1, width, (0, i * 12))
        assert native.digest(plane) == menu["planes"][i * 2]["plane_sha256"]
        masks.append({(index % width, index // width) for index, ink in enumerate(plane) if ink})
    for frame in request["holds"]:
        captured, image = town.read_frame(captures, frame)
        highlighted = []
        for index, ink in enumerate(masks):
            px, py = x + 16, 192 + y + 16 + index * 20
            assert match(image, ink, (8, 8, 8), [px], [py]) == [px, py]
            background = {image.getpixel((a, b)) for a in range(px, px + width)
                          for b in range(py - 4, py + 16) if (a - px, b - py) not in ink}
            assert background in ({(205, 198, 180)}, {(0, 165, 172)}), (menu["source_command_offset"], frame, index, background)
            if background == {(0, 165, 172)}:
                highlighted.append(index)
        if highlighted == [request["slot"]]:
            return dict(command_offset=menu["source_command_offset"], frame=frame, highlight=request["slot"],
                        captions=vm["labels"], observed=captured, exact_complete_glyphs=True), image
        assert not highlighted, (menu["source_command_offset"], frame, highlighted, request["slot"])
    raise AssertionError((menu["source_command_offset"], request["holds"], request["slot"]))


def main():
    assert not PROOF.exists()
    fixture_path, inputs = [replay.ROOT / name for name in ("fixture.json", "inputs.json")]
    fixture, report, checked, draft = map(base.load, (fixture_path, replay.REPORT, display.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == checked["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["original_story_branches_unexecuted"]
    assert fixture["sampled_branch_reply_commands_are_sequenced_in_fixture"] and not fixture["natural_activation"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == fixture["end"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)
    image = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(image.read_file(replay.PATH)).blocks
    assert bank[44][8:40].hex() == fixture["original_prelude"]
    copied = {row["actual_block_offset"]: row for row in fixture["copied"]}
    assert all(bank[84][at:at + len(bytes.fromhex(x["hex"]))].hex() == x["hex"] for at, x in copied.items())
    arm, font = (image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    ctx = SimpleNamespace(image=image, arm=arm)
    paint, fe = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    _, paint_menu, _ = display.menu.adapters(arm)
    name_font = panel.panel.GameAsciiFont.from_arm9(arm)
    captures = {x["frame"]: x for x in report["frames_captured"] if x["path"].endswith("_cold_boot.png")}
    native_menus = {menu["stored_command_offset"]: menu for menu in checked["menus"]}
    native_rows = {r["id"]: r for r in checked["records"]}
    rows = {r["id"]: r for r in draft["records"]}
    holds, menus, pictures = [], [], []
    for request in fixture["requested_holds"]:
        at = request["offset"]
        if request["type"] == "menu":
            observation, frame = menu_frame(arm, paint_menu, native_menus[at], request, captures)
            menus.append(observation)
            pictures.append((f"Menu {observation['command_offset']}, selected {observation['highlight'] + 1}", frame))
            continue
        ident, = copied[at]["ids"]
        row, result = rows[ident], native_rows[ident]
        frame, = request["holds"]
        captured, image = town.read_frame(captures, frame)
        system = row["source_selector"] == 254
        if system:
            index, = [i for i, p in enumerate(result["stored_pages"]) if p["stored_offset"] == at]
            expected = result["system"][index]
            plane = fe(bytes.fromhex(expected["expanded_hex"]))["physical"]
            assert native.digest(plane) == expected["plane_sha256"]
            number = index + 1
        else:
            number = request["page"]
            if row["decision"] == "revision":
                layout = result["layouts"][0]
                assert layout["scope"] == "registered default"
                raw = bytes.fromhex(layout["expanded_hex"])
            else:
                raw = stage.review.TOKEN.sub(lambda m: checked["default_names"][m[0]],
                                              bytes.fromhex(row["current_hex"])[1:].decode("ascii")).encode("ascii")
            rendered = paint(arm, font, raw)
            assert rendered["complete_consumed_bytes"] == len(raw)
            plane = bytes.fromhex(rendered["pages"][number - 1]["native_plane_hex"])
            if row["decision"] == "revision":
                assert native.digest(plane) == layout["page_sha256"][number - 1]
        assert panel.panel.mask_check(plane, 228 if system else 216, image), (ident, number, frame)
        if not system:
            panel.panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])
        holds.append(dict(id=ident, page=number, frame=frame, speaker=row["speaker"], decision=row["decision"],
                          system_FE=system, observed=captured))
        pictures.append((f"{ident} page {number}", image))
    assert [(m["command_offset"], m["highlight"]) for m in menus] == [(3114, 0), (3114, 1), (5298, 0), (5298, 1)]
    turn = [(r["id"], r["page"], r["frame"]) for r in holds if r["id"] in ("DK4_MES_B84_R0539", "DK4_MES_B84_R0542")]
    assert [(i, p) for i, p, _ in turn] == [("DK4_MES_B84_R0539", 1), ("DK4_MES_B84_R0539", 2), ("DK4_MES_B84_R0542", 1)]
    assert [f for _, _, f in turn] == list(range(turn[0][2], turn[0][2] + 900, 300))
    final, image = town.read_frame(captures, fixture["end"] - 1)
    pictures.append(("Return after the focused tutorial excerpt", image))
    sheets = []
    for i in range(0, len(pictures), 6):
        path = replay.ROOT / f"gerhard_gameplay_{i // 6 + 1}.png"
        town.sheet(pictures[i:i + 6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    ids = {row["id"] for row in holds} | {ident for m in checked["menus"] for ident in m["record_ids"]}
    evidence = {str(path): base.digest(path) for path in (fixture_path, inputs, replay.REPORT, display.PROOF, fixture["fixture_ROM"])}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, menus=menus, observed_ids=sorted(ids),
        original_story_branches_unvisited=True, exact_sampled_page_turn=turn, final_hold=final,
        sheets=sheets, evidence=evidence,
        offline_only=[r["id"] for r in draft["records"] if r["decision"] == "revision" and r["id"] not in ids]))
    print(f"Verified {len(holds)} speech pages and both live menus, including the two-panel tutorial transition.")


if __name__ == "__main__":
    main()
