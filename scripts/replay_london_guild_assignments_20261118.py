"""Replay Rafael's summons and riddle excerpts on the initialized Rafael route."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
import sys
from types import SimpleNamespace

from PIL import ImageDraw, Image

from scripts import headless_desmume_v193 as harness
from scripts import replay_rafael_final_wraps_20261114 as precedent
from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_london_guild_assignments_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "rafael_initialized"
ROM = ROOT / "Rafael_Ruins_Excerpts_RESEARCH_ONLY.nds"
FILE = "/data/SC0.DK4"
SETUP = ROOT / "fixture.json"
LIVE = ROOT / "verified.json"
LAST = 8401
EXCERPTS = ((294, (6,)), (296, (13, 17, 24, 122, 126, 145, 164, 186)),
            (298, (5, 14, 19, 23, 46, 60, 64)))


def prepare():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof["candidate_sha256"]
    draft = base.load(stage.review.OUTPUT)
    rows = {(r["block"], r["source_reference"]["record_index"]): r for r in draft["records"] if r["route"] == 0}
    image = base.NdsImage.open(stage.ROM)
    raw = image.read_file(FILE)
    bank = native.IlnkContainer.parse(raw)
    host = bank.blocks[44]
    inventory, _, _ = native.scoped_inventory()
    arm = image.read_file(native.ARM)
    selected, bytecode = [], []
    for n, indices in EXCERPTS:
        group = next(g for g in proof["groups"] if g["file_path"] == FILE and g["block"] == n)
        assert native.digest(bank.blocks[n]) == group["after"]
        for ident in indices:
            row = rows[n, ident]
            cmd = next(c for c in group["commands"] if c["record_ids"] == [row["id"]])
            assert cmd["word"] == 0x4000
            body = bytes.fromhex(cmd["stored"])
            at = cmd["stored_offset"]
            assert bank.blocks[n][at:at + len(body)] == body
            bytecode.append(body)
            selected.append(dict(id=row["id"], block=n, source_record_index=ident, stored_offset=at,
                                 stored_command_hex=body.hex()))
    value = bytearray(host[:40] + b"".join(bytecode) + bytes(4))
    pack_into("<H", value, 4, len(value) - 8)
    fixture = bytes(value) + bytes(-len(value) % 4)
    commands, speeches = inventory(arm, fixture)
    assert len(commands) == 11 + len(bytecode) and commands[-1]["word"] == 0
    assert [c["whole_command_hex"] for c in speeches] == [v.hex() for v in bytecode]
    ROOT.mkdir()
    bank.blocks[44] = fixture
    image.replace_file(FILE, bank.to_bytes())
    image.save(ROM)
    image.replace_file(FILE, raw)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    original = base.load(precedent.stage.CAPTURE)
    inputs = original["scripted_input_schedule"] + [
        dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 8101, 250)]
    path = ROOT / "inputs.json"
    base.save(path, inputs)
    base.save(SETUP, dict(candidate_sha256=proof["candidate_sha256"], fixture=str(ROM),
        fixture_sha256=base.digest(ROM), original_excerpt_commands_preserved=True,
        exact_ROM_inverse=True, initialized_Rafael=True, natural_activation=False,
        original_prefix_sha256=native.digest(host[:40]), selected=selected,
        inputs=str(path), inputs_sha256=base.digest(path)))


def capture():
    fixture = base.load(SETUP)
    assert base.digest(ROM) == fixture["fixture_sha256"]
    assert base.digest(fixture["inputs"]) == fixture["inputs_sha256"]
    argv = sys.argv
    try:
        sys.argv = [argv[0], "--rom", str(ROM), "--out", str(ROOT / "capture"), "--frames", str(LAST),
                    "--inputs-json", fixture["inputs"], "--capture-every", "999999",
                    "--capture-at", *map(str, range(3650, LAST, 25))]
        harness.main()
    finally:
        sys.argv = argv


def verify():
    assert not LIVE.exists()
    setup = base.load(SETUP)
    report_path = ROOT / "capture/capture_report.json"
    report = base.load(report_path)
    assert report["ROM_sha256"] == setup["fixture_sha256"] == base.digest(ROM)
    assert stage.base.digest(stage.ROM) == setup["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and report["scripted_input_schedule"] == base.load(setup["inputs"])
    asset = base.NdsImage.open(stage.ROM)
    arm, font = [asset.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT")]
    _, paint = stage.stage.progressive.layout.prior.precedent.planners(arm)
    photos = quest.prior.TOOL.photos(report)
    masks = [(n, quest.prior.TOOL.body_masks(im)) for n, (_, im) in sorted(photos.items())]
    observed, cursor = [], 3650
    for row in setup["selected"]:
        raw = bytes.fromhex(row["stored_command_hex"])
        body = raw[6:raw.index(0, 6)]  # The selector may be 00.
        body = body.replace(b"FI", b"Rafael").replace(b"FA", b"Castor")
        raster = paint(arm, font, body)
        for page in raster["pages"]:
            wanted = quest.prior.TOOL.prior.masks(bytes.fromhex(page["native_plane_hex"]))
            n = next((n for n, bits in masks if n > cursor and bits == wanted), None)
            assert n is not None, (row["id"], page["page"], body)
            observed.append(dict(id=row["id"], frame=n, page=page["page"], capture=photos[n][0], body_hex=body.hex()))
            cursor = n
    images = []
    for first in range(0, len(observed), 8):
        part = observed[first:first + 8]
        sheet = Image.new("RGB", (1024, 404 * ((len(part) + 1) // 2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(part):
            x, y = i % 2 * 512, i // 2 * 404
            draw.text((x + 4, y + 2), f"{row['id']}   frame {row['frame']}", fill="white")
            bottom = photos[row["frame"]][1].crop((0, 192, 256, 384))
            sheet.paste(bottom.resize((512, 384), Image.Resampling.NEAREST), (x, y + 16))
        path = ROOT / f"live_{first // 8 + 1}.png"
        sheet.save(path)
        images.append(dict(path=str(path), sha256=base.digest(path)))
    save = dict(candidate_sha256=setup["candidate_sha256"], fixture_sha256=setup["fixture_sha256"],
        initialized_Rafael=True, natural_activation=False, hardware=False, exact_original_commands=True,
        actual_Castor_and_Rafael_macro_glyphs=True, holds=observed, sheets=images,
        evidence={str(path): base.digest(path) for path in (report_path, SETUP)})
    base.save(LIVE, save)
    print(f"Matched {len(observed)} native body planes in order, including both captain name substitutions.", flush=True)


def startup():
    previous = base.load(stage.parent.RELEASE)
    boot = quest.inherited.boot
    snapshot = base.load(previous["own_registered_startup"])["read_only_snapshot"]["path"]
    prior = Path(snapshot).parent.parent
    context = SimpleNamespace(ROOT=stage.ROOT, ROM=stage.ROM, STORED=stage.PROOF, base=base)
    source = checked_text(getsource(boot.main), {
        'stage.parent.stage.ROOT/"startup_retry"': "PREVIOUS_CAPTURE",
        'stored["previous_sha256"]': 'stored["predecessor_sha256"]',
    })
    env = vars(boot) | dict(stage=context, PREVIOUS_CAPTURE=prior)
    exec(compile(source, __file__ + "::registered-startup", "exec"), env)
    env["main"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    globals()[parser.parse_args().action]()
