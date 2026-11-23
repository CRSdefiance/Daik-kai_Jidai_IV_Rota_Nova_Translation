"""Observe the exact revised dialogue in initialized Rafael and Hodram excerpts."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
import sys
from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import headless_desmume_v193 as harness
from scripts import replay_late_trade_exchanges_20261118 as earlier
from scripts import verify_moonlit_violin_20261121 as offline


build = offline.build
base, native = build.base, build.native
ROOT = build.ROOT / "playback"
PROOF = ROOT / "verified.json"
CONFIG = {
    "rafael": (0, 44, 40, 51, (6, 18, 24, 37, 46, 50, 59, 63, 67, 71)),
    "hodram": (1, 42, 42, 143, (17, 23, 30, 71, 75, 84, 87, 92, 96, 100, 104)),
}
INPUT_REPORT = {
    "rafael": Path("work/company_name_dialogue_20261121/rafael_name_context/capture_report.json"),
    "hodram": Path("work/company_name_dialogue_20261121/hodram_name_context/capture_report.json"),
}
FIRST, LAST, STEP = 3400, 7301, 20


def prepare(name):
    route, host, prefix, scene, selected = CONFIG[name]
    folder = ROOT / name
    assert not folder.exists()
    stored = base.load(build.PROOF)
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    image = base.NdsImage.open(build.ROM)
    path = f"/data/SC{route}.DK4"
    archive, arm = (image.read_file(p) for p in (path, native.ARM))
    bank = native.IlnkContainer.parse(archive)
    entry = bank.blocks[host]
    scan, _, _ = native.scoped_inventory()
    commands, speeches = scan(arm, entry)
    assert speeches[0]["offset"] == prefix
    group, = [g for g in stored["groups"] if g["route"] == route and g["block"] == scene]
    assert native.digest(bank.blocks[scene]) == group["after"]
    by_id = {ids[0]: cmd for cmd in group["commands"] if (ids := cmd["record_ids"])}
    records = []
    for index in selected:
        ident = f"DK4_MES_B{scene}_R{index:04}"
        row = by_id[ident]
        at, raw = row["stored_offset"], bytes.fromhex(row["stored"])
        assert bank.blocks[scene][at:at+len(raw)] == raw and row["word"] == 0x4000
        records.append(dict(id=ident, stored_hex=raw.hex(), original_offset=at))
    fixture = bytearray(entry[:prefix] + b"".join(bytes.fromhex(r["stored_hex"]) for r in records) + bytes(4))
    pack_into("<H", fixture, 4, len(fixture)-8)
    fixture.extend(bytes(-len(fixture) % 4))
    new_commands, new_speeches = scan(arm, fixture)
    prefix_controls = [c["whole_command_hex"] for c in commands if c["offset"] < prefix]
    assert [c["whole_command_hex"] for c in new_commands[:len(prefix_controls)]] == prefix_controls
    assert [c["whole_command_hex"] for c in new_speeches] == [r["stored_hex"] for r in records]
    folder.mkdir(parents=True)
    rom = folder / f"{name}_RESEARCH_ONLY.nds"
    bank.blocks[host] = bytes(fixture)
    image.replace_file(path, bank.to_bytes())
    image.save(rom)
    bank.blocks[host] = entry
    assert bank.to_bytes() == archive
    image.replace_file(path, archive)
    assert bytes(image.rom.save()) == build.ROM.read_bytes()
    plan = folder / "inputs.json"
    inputs = base.load(INPUT_REPORT[name])["scripted_input_schedule"]
    inputs.extend(dict(start=n, duration=8, buttons=["A"]) for n in range(3800, LAST-110, 275))
    base.save(plan, inputs)
    base.save(folder / "fixture.json", dict(candidate_sha256=stored["candidate_sha256"],
        fixture_sha256=base.digest(rom), fixture=str(rom), plan=str(plan), plan_sha256=base.digest(plan),
        initialized_route=route, host_block=host, excerpt_block=scene, selected=records,
        exact_prefix_and_dialogue_commands=True, parent_ROM_inverse=True, natural_activation=False))


def capture(name):
    folder = ROOT / name
    setup = base.load(folder / "fixture.json")
    assert base.digest(setup["fixture"]) == setup["fixture_sha256"]
    assert base.digest(setup["plan"]) == setup["plan_sha256"]
    sys.argv = [harness.__file__, "--rom", setup["fixture"], "--out", str(folder / "capture"),
        "--frames", str(LAST), "--inputs-json", setup["plan"], "--capture-every", "999999",
        "--capture-at", *map(str, range(FIRST, LAST, STEP))]
    harness.main()


def verify():
    assert not PROOF.exists()
    target = base.NdsImage.open(build.ROM)
    candidate = base.digest(build.ROM)
    checks = base.load(offline.PROOF)
    assert checks["candidate_sha256"] == candidate
    arm, font = (target.read_file(a) for a in (native.ARM, "/GRP/KANJI.FNT"))
    paint = offline.display.clipped_renderer(SimpleNamespace(arm=arm))
    tool = earlier.precedent.quest.prior.TOOL
    evidence, holds, sheets = {}, [], []
    for name in CONFIG:
        folder = ROOT / name
        fixture, log = folder / "fixture.json", folder / "capture/capture_report.json"
        setup, report = map(base.load, (fixture, log))
        assert setup["candidate_sha256"] == candidate and setup["parent_ROM_inverse"]
        assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(setup["fixture"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not report.get("battery_save_preloaded") and report["frames"] == LAST
        assert report["scripted_input_schedule"] == base.load(setup["plan"])
        photos = tool.photos(report)
        masks = [(n, tool.body_masks(pic)) for n, (_, pic) in sorted(photos.items()) if n >= FIRST]
        found, cursor = [], FIRST-1
        for row in setup["selected"]:
            raw = bytes.fromhex(row["stored_hex"])
            body = offline.display.prior.default_text(offline.bytes_for(raw), offline.NAMES)
            for page in paint(arm, font, body)["pages"]:
                wanted = tool.prior.masks(bytes.fromhex(page["native_plane_hex"]))
                at = next((n for n, actual in masks if n > cursor and actual == wanted), None)
                assert at is not None, (name, row["id"], cursor, body)
                found.append(row | dict(route=setup["initialized_route"], frame=at, capture=photos[at][0]))
                cursor = at
        holds.extend(found)
        revised = {r["id"] for r in checks["records"] if r["decision"] == "revision"}
        focused = [r for r in found if r["id"] in revised]
        sheet = Image.new("RGB", (768, 212*((len(focused)+2)//3)), "#242833")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(focused):
            x, y = 256*(i%3), 212*(i//3)
            draw.text((x+5, y+3), f"{row['id']}  {row['frame']}", fill="white")
            sheet.paste(photos[row["frame"]][1].crop((0, 192, 256, 384)), (x, y+19))
        screenshot = folder / f"{name}_verified_revisions.png"
        sheet.save(screenshot)
        sheets.append(dict(path=str(screenshot), sha256=base.digest(screenshot)))
        evidence.update({str(p): base.digest(p) for p in (fixture, log, setup["fixture"], setup["plan"])})
    assert revised <= {r["id"] for r in holds}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        hardware_verified=False, exact_native_glyph_matches=True, holds=holds, sheets=sheets, evidence=evidence))
    print(f"Emulator matched {len(holds)} complete dialogue panels across Rafael and Hodram.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "verify"))
    cli.add_argument("name", choices=tuple(CONFIG), nargs="?")
    args = cli.parse_args()
    if args.action == "verify":
        verify()
    else:
        globals()[args.action](args.name)
