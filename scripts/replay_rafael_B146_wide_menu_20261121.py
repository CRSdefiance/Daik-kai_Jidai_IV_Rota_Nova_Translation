"""Observe the widest reviewed choice with both cursor positions in DeSmuME."""

from pathlib import Path
from struct import pack_into
import sys

from PIL import Image

from scripts import check_typed_story_menu_display_20261121 as offline
from scripts import headless_desmume_v193 as harness


base, native, current = offline.base, offline.native, offline.current
ROOT = offline.ROOT / "rafael_B146_emulator"
LOG = ROOT / "capture/capture_report.json"
SETUP = ROOT / "fixture.json"
FINAL = ROOT / "observed.json"
INITIAL = Path("work/company_name_dialogue_20261121/rafael_name_context/capture_report.json")
HISTORICAL = Path("work/analysis/Rafael557_tutorial_menu_pixels_v1_20261105/menu_actual_pixels.json")
FILE = "/data/SC0.DK4"
END = 5810


def prepare():
    assert not ROOT.exists()
    source_index, offline_proof = map(base.load, (offline.scout.OUTPUT, offline.PROOF))
    candidate = base.digest(current.ROM)
    assert source_index["candidate_sha256"] == offline_proof["candidate_sha256"] == candidate
    lead, = [r for r in source_index["leads"] if r["current"]["file_path"] == FILE and r["current"]["block"] == 146]
    image = base.NdsImage.open(current.ROM)
    archive, arm = (image.read_file(p) for p in (FILE, native.ARM))
    bank = native.IlnkContainer.parse(archive)
    host = bank.blocks[44]
    scan, _, _ = native.scoped_inventory()
    host_commands, speeches = scan(arm, host)
    prefix = speeches[0]["offset"]
    assert prefix == 40
    scene_commands, _ = scan(arm, bank.blocks[146])
    menu_offset = lead["current"]["command_offset"]
    context = [row for row in lead["context"]["current"] if row["word"] == "0x4000"]
    picked_offsets = sorted([row["command_offset"] for row in context] + [menu_offset])
    assert len(picked_offsets) == 5 and picked_offsets[3] == menu_offset
    selected = [c for c in scene_commands if c["offset"] in picked_offsets]
    menu = selected[3]
    assert menu["whole_command_hex"] == lead["current_object_hex"]
    fixture = bytearray(host[:prefix] + b"".join(bytes.fromhex(c["whole_command_hex"]) for c in selected) + bytes(4))
    pack_into("<H", fixture, 4, len(fixture) - 8)
    fixture.extend(bytes(-len(fixture) % 4))
    commands, _ = scan(arm, fixture)
    before = [c["whole_command_hex"] for c in host_commands if c["offset"] < prefix]
    assert [c["whole_command_hex"] for c in commands][:len(before)+len(selected)] == (
        before + [c["whole_command_hex"] for c in selected])
    ROOT.mkdir()
    rom = ROOT / "rafael_B146_menu_RESEARCH_ONLY.nds"
    bank.blocks[44] = bytes(fixture)
    image.replace_file(FILE, bank.to_bytes())
    image.save(rom)
    bank.blocks[44] = host
    assert bank.to_bytes() == archive
    image.replace_file(FILE, archive)
    assert bytes(image.rom.save()) == current.ROM.read_bytes()
    plan = ROOT / "inputs.json"
    inputs = [row for row in base.load(INITIAL)["scripted_input_schedule"] if row["start"] < 3000]
    inputs.extend(dict(start=frame, duration=8, buttons=[button])
                  for frame, button in ((3800, "A"), (4080, "A"), (4360, "A"), (4900, "DOWN"), (5400, "A")))
    base.save(plan, inputs)
    base.save(SETUP, dict(candidate_sha256=candidate, research_fixture=str(rom), fixture_sha256=base.digest(rom),
        inputs=str(plan), inputs_sha256=base.digest(plan), exact_ROM_inverse=True,
        initialized_Rafael_host=44, excerpt_block=146, exact_stored_commands=selected, natural_activation=False))


def capture():
    fixture = base.load(SETUP)
    assert base.digest(fixture["research_fixture"]) == fixture["fixture_sha256"]
    assert base.digest(fixture["inputs"]) == fixture["inputs_sha256"]
    sys.argv = [harness.__file__, "--rom", fixture["research_fixture"], "--out", str(LOG.parent),
        "--frames", str(END), "--inputs-json", fixture["inputs"], "--capture-every", "999999",
        "--capture-at", *map(str, range(3675, END, 55))]
    harness.main()


def verify():
    assert not FINAL.exists()
    proof, fixture, report = map(base.load, (offline.PROOF, SETUP, LOG))
    assert proof["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(current.ROM)
    assert report["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(fixture["research_fixture"])
    assert report["frames"] == END and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    assert report["scripted_input_schedule"] == base.load(fixture["inputs"])
    menu, = [case for case in proof["cases"] if case["key"] == "SC0_B146"]
    assert not menu["failures"]
    historic, = [s for s in base.load(HISTORICAL)["menu_samples"] if s["source_command_offset"] == 468
                 and s["visible_selected_option"] == 0]
    old_mask = []
    for row in historic["labels"]:
        plane, = [p for p in menu["paint"] if p["option"] == row["index"] and p["style"] == 1]
        pixels = Path(row["native_plane"]).read_bytes()
        assert base.digest(row["native_plane"]) == row["native_plane_sha256"] == plane["raster_sha256"]
        assert row["text"] == plane["text"]
        x, y = row["origin"]
        old_mask.append(((x, y, x + plane["logical_width_px"], y+plane["logical_height_px"]),
                         bytes(bool(v) for v in pixels)))

    selected = {}
    after = None
    ink, highlight, plain = (8, 8, 8), (0, 165, 172), (205, 198, 180)
    for frame in report["frames_captured"]:
        at = frame["frame"]
        if at < 4400:
            continue
        assert frame["PNG_sha256"] == base.digest(frame["path"])
        pic = Image.open(frame["path"]).convert("RGB")
        colors = [[*pic.crop(bounds).getdata()] for bounds, _ in old_mask]
        match = all(bytes(rgb == ink for rgb in color) == mask
                    for color, (_, mask) in zip(colors, old_mask, strict=True))
        if match:
            for index in range(2):
                if at < 4900 and index != 0 or at >= 5400 or 4900 <= at and index != 1:
                    continue
                fills = [{highlight, ink} if i == index else {plain, ink} for i in range(2)]
                if all(set(color) == expected for color, expected in zip(colors, fills, strict=True)):
                    selected.setdefault(index, frame)
        elif at > 5400 and after is None:
            after = frame
    assert set(selected) == {0, 1} and after
    base.save(FINAL, dict(candidate_sha256=proof["candidate_sha256"], fixture_sha256=fixture["fixture_sha256"],
        full_caption_ink_masks_match_current_native_painter=True, captured_cursor_states=selected,
        after_A=after, exact_complete_match_to_earlier_caption_proof=True,
        actual_gameplay_with_initialized_scene=True, original_story_branch_and_natural_activation=False,
        hardware_verified=False, evidence={str(p): base.digest(p) for p in (SETUP, LOG, offline.PROOF, HISTORICAL)}))
    print("Both full cursor states match all caption pixels:", {key: value["frame"] for key, value in selected.items()})
    print("Controller A leaves the menu:", after["frame"])


if __name__ == "__main__":
    action, = sys.argv[1:]
    {"prepare": prepare, "capture": capture, "verify": verify}[action]()

