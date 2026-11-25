"""Build the Osaka edits over the current registered release and replay both scenes."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import register_kurushima_surrender_20261122 as parent
from scripts import replay_hodram_early_confrontations_20261119 as hodram
from scripts import replay_maria_opening_wraps_20261114 as maria
from scripts import review_osaka_glass_followup_20261122 as review
from scripts import stage_rafael_deck_tutorial_followup_20261122 as established
from scripts import verify_seville_square_gameplay_20261121 as comparison
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL, validate_capture, validate_fixture
from scripts.replay_lil_ceramics_wrap_20261111 import photos


base, native = parent.base, parent.native
ROOT = review.ROOT / "staged"
BINDING = review.ROOT / "successor_binding.json"
ROM = ROOT / "Osaka_Glass_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
LIVE = ROOT / "focused_gameplay.json"
CASES = {1: (192, hodram.ENTRY, 2680, 300), 3: (161, 33, 4200, 325)}
SPEAKERS = {130: "Daimyo", 150: "Guildmaster"}


def stage():
    assert not ROOT.exists()
    previous, binding, manuscript, proof = map(base.load, (parent.RELEASE, BINDING, review.REVIEW, review.PROOF))
    digest = base.digest(parent.ROM)
    assert digest == previous["candidate_sha256"] == binding["candidate_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert base.digest(review.PROOF) == binding["stored_and_native_proof_sha256"]
    assert base.digest(review.REVIEW) == binding["draft_sha256"] == proof["manuscript_sha256"]
    assert binding["visually_reviewed_two_native_previews"] and base.digest(review.SHEET) == proof["sheet_sha256"]
    image = base.NdsImage.open(parent.ROM)
    before = native.files(image)

    for path, bound in binding["unchanged_osaka_blocks"].items():
        bank = native.IlnkContainer.parse(before[path])
        assert native.digest(bank.blocks[bound["block"]]) == bound["exact_current_sha256"]

    changed = {}
    for entry in proof["compiled_blocks"]:
        path, index = entry["file_path"], entry["block"]
        rows = [r for r in manuscript["records"] if (r["file_path"], r["block"]) == (path, index)]
        bank = native.IlnkContainer.parse(before[path])
        old, new = bank.blocks[index], bytes.fromhex(entry["compiled_block_hex"])
        assert native.digest(new) == entry["compiled_block_sha256"]
        assert native.digest(old) == binding["unchanged_osaka_blocks"][path]["exact_current_sha256"]
        altered = [cmd for cmd in entry["command_map"] if cmd["stored"] != cmd["current"]]
        assert [cmd["record_ids"] for cmd in altered] == [[r["id"] for r in rows if r["decision"] == "revision"]]
        bank.blocks[index] = new
        archive = bank.to_bytes()
        reread = native.IlnkContainer.parse(archive)
        assert reread.blocks[index] == new
        bank.blocks[index] = old
        assert bank.to_bytes() == before[path]
        assert [i for i, (a, b) in enumerate(zip(bank.blocks, reread.blocks, strict=True)) if a != b] == [index]
        image.replace_file(path, archive)
        changed[path] = dict(block=index, before=native.digest(before[path]), after=native.digest(archive),
                             target_block=native.digest(new), commands=entry["command_map"])

    after = native.files(image)
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == set(changed) == {"/data/SC1.DK4", "/data/SC3.DK4"}
    assert native.digest(after[native.ARM]) == previous["target_ARM9_sha256"]
    candidate = bytes(image.rom.save())
    for path in changed:
        image.replace_file(path, before[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=digest,
                           changed=changed, whole_parent_inverse=True, reviewed_manuscript_sha256=base.digest(review.REVIEW),
                           offline_proof_sha256=base.digest(review.PROOF), scope_binding_sha256=base.digest(BINDING)))


def capture(route):
    index, host_index, first, interval = CASES[route]
    folder = ROOT / f"route{route}"
    assert not folder.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof["candidate_sha256"]
    image = base.NdsImage.open(ROM)
    path = f"/data/SC{route}.DK4"
    original = image.read_file(path)
    bank = native.IlnkContainer.parse(original)
    arm = image.read_file(native.ARM)
    entry, scene = bank.blocks[host_index], bank.blocks[index]
    assert native.digest(scene) == proof["changed"][path]["target_block"]
    inventory, _, _ = native.scoped_inventory()
    commands, speeches = inventory(arm, scene)
    assert len(speeches) == 11
    assert [c["word"] for c in commands if c["word"] != 0x4000] == [0xA000, 0xC200, 0]
    if route == 1:
        host = base.load(hodram.HISTORICAL)
        prelude = b"".join(bytes.fromhex(r["whole_command_hex"]) for r in host["original_initializers"])
        initial = base.load(Path("work/analysis/papal_trade_route_runs_v7625/route1/ordinary_NewGame_inputs.json"))
        assert sum(e["buttons"] == ["RIGHT"] for e in initial) == 1
    else:
        clean_entry = native.IlnkContainer.parse(base.NdsImage.open(native.CLEAN).read_file(path)).blocks[host_index]
        prelude = clean_entry[8:34]
        assert len([c for c in inventory(arm, entry)[0] if c["offset"] < 34]) == 7
        original_unlock = base.load(maria.stage.CAPTURE)
        validate_capture(original_unlock)
        initial = original_unlock["scripted_input_schedule"]

    assert entry[8:8+len(prelude)] == prelude
    end = 8 + unpack_from("<H", scene, 4)[0]
    fixture = bytearray(entry[:8] + prelude + scene[8:end])
    pack_into("<H", fixture, 4, len(fixture) - 8)
    fixture += bytes(-len(fixture) % 4)
    inserted, _ = inventory(arm, bytes(fixture))
    assert [(c["offset"],c["whole_command_hex"]) for c in inserted if c["offset"] >= 8+len(prelude)] == [
        (c["offset"] + len(prelude),c["whole_command_hex"]) for c in commands]
    bank.blocks[host_index] = bytes(fixture)
    image.replace_file(path, bank.to_bytes())
    folder.mkdir()
    rom = folder / f"Osaka_Route{route}_FOCUSED_ONLY.nds"
    image.save(rom)
    image.replace_file(path, original)
    assert bytes(image.rom.save()) == ROM.read_bytes()

    advance = [dict(start=f, duration=16, buttons=["A"]) for f in range(first, first+13*interval,interval)]
    frames = sorted(set(range(first-60, first+13*interval, 50)) |
                    {first + i*interval + 220 for i in range(12)})
    end = first + 13*interval + 60
    inputs = folder / "inputs.json"
    base.save(inputs, initial + advance)
    extra = []
    if route == 3:
        unlock = base.load(HISTORICAL)
        unlock.update(production_ROM=str(rom), production_ROM_sha256=base.digest(rom),
                      current_test_scope="Original Osaka scene commands replayed in an initialized Maria route.")
        manifest = folder / "unlock.json"
        base.save(manifest, unlock)
        validate_fixture(manifest)
        extra = ["--battery-save", unlock["fixture_save"], "--allow-gallery-fixtures",
                 "--gallery-save-fixture-manifest", str(manifest), "--touchscreen"]
    base.save(folder / "fixture.json", dict(rom=str(rom), sha256=base.digest(rom), end=end, route=route,
        host=host_index, original_block=index, candidate_sha256=proof["candidate_sha256"], exact_candidate_inverse=True,
        original_scene_commands=commands, ordinary_Osaka_trigger=False))
    import sys
    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(folder / "capture"), "--frames", str(end),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999", "--capture-at",
                *map(str, frames), *extra]
    harness.main()


def verify():
    assert not LIVE.exists()
    proof, draft = map(base.load, (PROOF, review.REVIEW))
    candidate = base.digest(ROM)
    assert candidate == proof["candidate_sha256"]
    image = base.NdsImage.open(ROM)
    arm, font = (image.read_file(name) for name in (native.ARM, "/GRP/KANJI.FNT"))
    context = SimpleNamespace(image=image, arm=arm)
    town = comparison.town
    draw, draw_fe = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = comparison.GameAsciiFont.from_arm9(arm)
    cases, sheets = {}, {}
    for route, (index, _, _, _) in CASES.items():
        folder = ROOT / f"route{route}"
        capture_file = folder / "capture/capture_report.json"
        capture_report, fixture = map(base.load,(capture_file, folder / "fixture.json"))
        assert capture_report["ROM_sha256"] == fixture["sha256"] == base.digest(fixture["rom"])
        assert fixture["candidate_sha256"] == candidate and fixture["exact_candidate_inverse"]
        assert capture_report["frames"] == fixture["end"]
        assert capture_report["scripted_input_schedule"] == base.load(folder / "inputs.json")
        assert capture_report["cold_boot"] and not capture_report["savestate_loaded"] and not capture_report["callback_errors"]
        if route == 3:
            validate_capture(capture_report)
        else:
            assert not capture_report.get("battery_save_preloaded")
            assert not any(v for k,v in capture_report.items() if k.startswith("synthetic_"))
        rows = [r for r in draft["records"] if r["route"] == route]
        archive = f"/data/SC{route}.DK4"
        record_commands = {r["record_ids"][0]:r for r in proof["changed"][archive]["commands"] if r["record_ids"]}
        sightings, panels = [], []
        cursor = 0
        samples = photos(capture_report)
        for row in rows:
            command = bytes.fromhex(record_commands[row["id"]]["stored"])
            selector = row["source_selector"]
            assert selector == command[5]
            body = command[6:command.index(0, 6)]
            if selector == 254:
                result = draw_fe(body)
                plane, width = result["physical"], 228
            else:
                result = draw(arm, font, body)
                page, = result["pages"]
                assert page["native_independent_plane_equal"]
                plane, width = bytes.fromhex(page["native_plane_hex"]), 216
            assert result["complete_consumed_bytes"] == len(body)
            for frame, (receipt, shot) in sorted(samples.items()):
                if frame > cursor + 120 and comparison.previous.mask_check(plane,width,shot):
                    break
            else:
                raise AssertionError((route,row["id"],cursor))
            cursor = frame
            label = None
            if selector != 254:
                label = SPEAKERS[selector]
                comparison.previous.complete_mask(name_font, label, shot, 16, 277, town.INKS[1])
            sightings.append(dict(id=row["id"], frame=frame, capture=receipt,
                                  complete_native_body_mask_sha256=native.digest(plane), nameplate=label))
            panels.append((row["id"],shot))
        end_frame, (end_receipt, end_image) = max(samples.items())
        assert end_frame > cursor + 200
        assert not comparison.previous.mask_check(plane, width, end_image)
        panels.append(("After final page", end_image))
        canvas = Image.new("RGB",(1024, 242*((len(panels)+1)//2)), "#243139")
        labels = ImageDraw.Draw(canvas)
        for n,(tag,panel) in enumerate(panels):
            x,y = 512*(n%2),242*(n//2)
            labels.text((x+4,y+3),tag,fill="white")
            canvas.paste(panel.convert("RGB").crop((0,272,256,384)).resize((512,224),
                        Image.Resampling.NEAREST),(x,y+16))
        sheet = folder / "scenes.png"
        canvas.save(sheet)
        sheets[str(sheet)]=base.digest(sheet)
        cases[route]=dict(sightings=sightings, end_capture=end_receipt, end_frame=end_frame,
                         capture=str(capture_file), capture_sha256=base.digest(capture_file))
    base.save(LIVE,dict(candidate_sha256=candidate, cases=cases, sheets=sheets, initialized_scenes=True,
                       original_scene_commands=True, natural_Osaka_trigger=False, hardware=False))


def run():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup", "hodram", "maria", "verify"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        method = getattr(established, action)
        FunctionType(method.__code__, method.__globals__ | globals())()
    elif action in ("hodram", "maria"):
        capture(1 if action == "hodram" else 3)
    else:
        globals()[action]()


if __name__ == "__main__":
    run()

