"""Exercise selected Rafael dialogue, a choice menu and FE notices in an initialized replay."""

import sys
from argparse import ArgumentParser
from struct import pack_into
from types import SimpleNamespace

from scripts import check_rafael_gerhard_tutorial_gameplay_20261121 as prior
from scripts import verify_rafael_followup_encounters_20261121 as display


stage, base, native = display.stage, display.base, display.native
town, menu, panel = prior.town, display.prior.menu, prior.panel.panel
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
PATH = display.PATH

# The scene excerpts preserve exact installed speech and menu objects. The
# refusal reply after B91's menu is sequenced in the fixture.
SELECTED = (
    (85, 5), (85, 40), (85, 48),
    (86, 5), (86, 75), (86, 129), (86, 143), (86, 205), (86, 248), (86, 280),
    (87, 32), (87, 97), (87, 133), (87, 162), (87, 217),
    (88, 52), (88, 82), (88, 103),
    (90, 32), (90, 40),
    (91, 14), (91, "menu"), (91, 98), (91, 101), (91, 109), (91, 112),
    (92, 5), (92, 57), (92, 61),
    (93, 5), (93, 9), (93, 64), (93, 73),
    (95, 29), (97, 47), (97, 77), (97, 80), (100, 21), (100, 38),
)


def replay():
    assert not ROOT.exists()
    stage_report = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == stage_report["candidate_sha256"] and stage_report["whole_parent_inverse"]
    image = base.NdsImage.open(stage.ROM)
    archive = image.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    opening = bank.blocks[44]
    driver = prior.replay
    prelude = bytes.fromhex(base.load(driver.spain.OLD_FIXTURE)["original_prelude"])
    assert opening[8:40] == prelude and len(prelude) == 32
    groups = {group["block"]: group for group in stage_report["groups"]}
    compiled, copied, logical = [], [], bytearray(opening[:40])
    for block, index in SELECTED:
        group = groups[block]
        owner = bank.blocks[block]
        assert native.digest(owner) == group["after"] and opening[:4] == owner[:4] and opening[6:8] == owner[6:8]
        if index == "menu":
            command, = [c for c in group["commands"] if c["word"] == 0x2100]
            plan = None
        else:
            ident = f"DK4_MES_B{block}_R{index:04d}"
            command, = [c for c in group["commands"] if c["record_ids"] == [ident]]
            assert command["word"] == 0x4000
            plan = group["plans"].get(ident)
        raw, at = bytes.fromhex(command["stored"]), command["stored_offset"]
        assert owner[at:at + len(raw)] == raw
        copied.append(dict(block=block, ids=command["record_ids"], fixture_offset=len(logical), actual_block_offset=at,
                           word=command["word"], hex=raw.hex()))
        compiled.append(command | {"stored_offset": len(logical), "plan": plan})
        logical.extend(raw)
    end = groups[91]["commands"][-1]
    assert end["word"] == 0
    logical.extend(bytes.fromhex(end["stored"]))
    pack_into("<H", logical, 4, len(logical) - 8)
    body = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = native.scoped_inventory()
    parsed, _ = inventory(image.read_file(native.ARM), body)
    indexed = {row["offset"]: row["whole_command_hex"] for row in parsed}
    assert all(indexed[row["fixture_offset"]] == row["hex"] for row in copied)
    bank.blocks[44] = body
    image.replace_file(PATH, bank.to_bytes())
    ROOT.mkdir(parents=True)
    rom = ROOT / "Rafael_Followup_Encounters_RESEARCH_ONLY.nds"
    image.save(rom)
    inverse = base.NdsImage.open(rom)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    events, requests, frames = driver.make_schedule(compiled)
    inputs = ROOT / "inputs.json"
    base.save(inputs, base.load(driver.original.INPUTS) + events)
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(rom), fixture_ROM_sha256=base.digest(rom),
        original_prelude=prelude.hex(), copied=copied, requested_holds=requests, end=frames, exact_candidate_inverse=True,
        original_story_branches_unexecuted=True, natural_activation=False))
    holds = [frame for q in requests for frame in q["holds"]] + [frames - 1]
    harness = driver.original.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(REPORT.parent), "--frames", str(frames),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, holds)]
    harness.main()


def check():
    assert not PROOF.exists()
    fixture_file, inputs = [ROOT / name for name in ("fixture.json", "inputs.json")]
    fixture, report, native_report, draft = map(base.load, (fixture_file, REPORT, display.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == native_report["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["original_story_branches_unexecuted"] and not fixture["natural_activation"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == fixture["end"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)
    game = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(game.read_file(PATH)).blocks
    assert bank[44][8:40].hex() == fixture["original_prelude"]
    arm, font = [game.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT")]
    native_ctx = SimpleNamespace(image=game, arm=arm)
    paint, fe = town.clipped_renderer(native_ctx), town.current_fe_painter(native_ctx)
    _, paint_menu, _ = menu.adapters(arm)
    name_font = panel.GameAsciiFont.from_arm9(arm)
    captures = {shot["frame"]: shot for shot in report["frames_captured"] if shot["path"].endswith("_cold_boot.png")}
    copied = {row["fixture_offset"]: row for row in fixture["copied"]}
    for row in copied.values():
        raw, where = bytes.fromhex(row["hex"]), row["actual_block_offset"]
        assert bank[row["block"]][where:where + len(raw)] == raw
    rows = {r["id"]: r for r in draft["records"]}
    native_rows = {r["id"]: r for r in native_report["records"]}
    menus_at = {(m["block"], m["stored_command_offset"]): m for m in native_report["menus"]}
    holds, menus, pictures = [], [], []
    for req in fixture["requested_holds"]:
        item = copied[req["offset"]]
        if req["type"] == "menu":
            observed, image = prior.menu_frame(arm, paint_menu, menus_at[item["block"], item["actual_block_offset"]], req, captures)
            menus.append(observed)
            pictures.append((f"B91 miracle choice, selected {observed['highlight'] + 1}", image))
            continue
        ident, = item["ids"]
        row, checked = rows[ident], native_rows[ident]
        page = req["page"]
        frame, = req["holds"]
        captured, image = town.read_frame(captures, frame)
        system = row["source_selector"] == 254
        assert checked["stored_pages"][0]["stored"] == item["hex"]
        if system:
            expected, = checked["system"]
            plane = fe(bytes.fromhex(expected["expanded_hex"]))["physical"]
            assert native.digest(plane) == expected["plane_sha256"]
        else:
            if checked.get("layouts"):
                expected = checked["layouts"][0]
                assert expected["scope"] == "registered default"
                body = bytes.fromhex(expected["expanded_hex"])
            else:
                current = bytes.fromhex(row["current_hex"])[1:].decode("ascii")
                body = stage.review.TOKEN.sub(lambda m: native_report["default_names"][m[0]], current).encode("ascii")
            view = paint(arm, font, body)
            assert view["complete_consumed_bytes"] == len(body)
            plane = bytes.fromhex(view["pages"][page - 1]["native_plane_hex"])
            if checked.get("layouts"):
                assert native.digest(plane) == expected["page_sha256"][page - 1]
            panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])
        assert panel.mask_check(plane, 228 if system else 216, image), (ident, page, frame)
        holds.append(dict(id=ident, page=page, frame=frame, speaker=row["speaker"], decision=row["decision"],
                          system_FE=system, observed=captured))
        pictures.append((f"{ident} page {page}", image))
    assert [m["highlight"] for m in menus] == [0, 1]
    transition_ids = ["DK4_MES_B91_R0101", "DK4_MES_B91_R0109", "DK4_MES_B91_R0112", "DK4_MES_B92_R0005"]
    turn = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in transition_ids]
    assert [h[0] for h in turn] == transition_ids
    assert [h[2] for h in turn] == list(range(turn[0][2], turn[0][2] + 1200, 300))
    final, image = town.read_frame(captures, fixture["end"] - 1)
    pictures.append(("Return after the focused excerpts", image))
    sheets = []
    for i in range(0, len(pictures), 6):
        path = ROOT / f"rafael_encounters_gameplay_{i // 6 + 1}.png"
        town.sheet(pictures[i:i + 6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    miracle_menu, = [m for m in native_report["menus"] if m["block"] == 91]
    observed = {r["id"] for r in holds} | set(miracle_menu["record_ids"])
    paths = (fixture_file, inputs, REPORT, display.PROOF, fixture["fixture_ROM"])
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, menus=menus, observed_ids=sorted(observed),
        original_story_branches_unvisited=True, exact_sampled_page_turn=turn, final_hold=final, sheets=sheets,
        evidence={str(path): base.digest(path) for path in paths},
        offline_only=[r["id"] for r in draft["records"] if r["id"] not in observed]))
    print(f"Verified {len(holds)} speech pages and two miracle menu highlights.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    (replay if parser.parse_args().action == "replay" else check)()

