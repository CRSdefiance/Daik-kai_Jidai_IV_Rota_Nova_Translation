"""Replay the registered-format London and Alexandria town scenes after initialization."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import replay_alexandria_cooking_20261114 as prior
from scripts import replay_embedded_story_roles_20261115 as inherited
from scripts import stage_town_trend_exchanges_20261115 as stage

base = stage.base
GUESTS = {155: ("London", 8), 159: ("Alexandria", 12)}
FILE = "/data/SC3.DK4"


def paths(block):
    root = stage.ROOT / GUESTS[block][0].lower()
    return root, root / "fixture_receipt.json", root / "inputs.json"


def prepare(block):
    root, setup, inputs = paths(block)
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged["candidate_sha256"]
    image = base.NdsImage.open(stage.ROM)
    arm, archive = (image.read_file(path) for path in (stage.ARM, FILE))
    bank = stage.IlnkContainer.parse(archive)
    host, guest = bank.blocks[33], bank.blocks[block]
    inventory, _, _ = stage.scoped_inventory()
    host_commands, host_speech = inventory(arm, host)
    host_end = host_speech[-1]["offset"] + host_speech[-1]["native_extent"]
    cleanup = [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] >= host_end]
    assert cleanup[0] == "4062" and cleanup[-1] == "00000000"
    prefix = [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] < 34]
    assert len(prefix) == 7

    guest_end = 8 + unpack_from("<H", guest, 4)[0]
    guest_commands, guest_speeches = inventory(arm, guest)
    assert len(guest_speeches) == GUESTS[block][1]
    assert guest[guest_end-6:guest_end] == bytes.fromhex("00c200000000")
    body = bytearray(host[:34] + guest[8:guest_end-4] + bytes.fromhex("".join(cleanup)))
    pack_into("<H", body, 4, len(body) - 8)
    replacement = bytes(body) + bytes(-len(body) % 4)
    commands, speeches = inventory(arm, replacement)
    assert [r["whole_command_hex"] for r in commands] == (
        prefix + [r["whole_command_hex"] for r in guest_commands[:-1]] + cleanup)
    assert [r["whole_command_hex"] for r in speeches] == [r["whole_command_hex"] for r in guest_speeches]

    root.mkdir()
    target = root / (GUESTS[block][0] + "_initialized_RESEARCH_ONLY.nds")
    bank.blocks[33] = replacement
    image.replace_file(FILE, bank.to_bytes())
    image.save(target)
    bank.blocks[33] = host
    assert bank.to_bytes() == archive
    image.replace_file(FILE, archive)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    manifest = root / "existing_system_only_unlock.json"
    unlock = base.load(prior.precedent.HISTORICAL)
    unlock.update(production_ROM=str(target), production_ROM_sha256=base.digest(target),
                  current_test_scope=f"Complete {GUESTS[block][0]} scene at initialized Maria entry.")
    base.save(manifest, unlock)
    prior.precedent.validate_fixture(manifest)
    schedule = base.load(prior.precedent.stage.CAPTURE)["scripted_input_schedule"] + [
        dict(start=frame, duration=16, buttons=["A"]) for frame in range(4200, 8501, 325)]
    base.save(inputs, schedule)

    _, paint = stage.layout.prior.precedent.planners(arm)
    font = image.read_file("/GRP/KANJI.FNT")
    review = base.load(stage.MANUSCRIPT)["records"]
    rows = [r for r in review if r["file_path"] == FILE and r["block"] == block]
    _, raw_records = stage.raw_speeches(arm, guest, inventory)
    planes = []
    for row, record in zip(rows, raw_records, strict=True):
        assert row["staged_reference"]["raw_hex"] == record["raw_hex"]
        raw = bytes.fromhex(record["raw_hex"])
        if raw[0] == 254:
            continue
        page, = paint(arm, font, raw[1:])["pages"]
        planes.append(dict(id=row["id"], selector=raw[0], plane=page["native_plane_hex"],
                           text=row["english"].split("}", 1)[1]))
    base.save(setup, dict(candidate_sha256=staged["candidate_sha256"],
        fixture_ROMs=dict(after=dict(path=str(target), sha256=base.digest(target), unlock=str(manifest), unlock_sha256=base.digest(manifest))),
        original_scene_commands=[r["whole_command_hex"] for r in guest_commands[:-1]],
        original_host_cleanup=cleanup, whole_checked_ROM_inverse_exact=True,
        progressive_targets=planes, market_notice_exact_hex=raw_records[-1]["raw_hex"]))


def capture(block):
    root, setup, inputs = paths(block)
    FunctionType(prior.capture.__code__, vars(prior) | dict(ROOT=root, SETUP=setup, INPUTS=inputs))()


def verify(block):
    root, setup, inputs = paths(block)
    receipt = base.load(setup)
    report_path = root / "after_verified/capture_report.json"
    report = base.load(report_path)
    prior.precedent.validate_capture(report)
    assert report["ROM_sha256"] == receipt["fixture_ROMs"]["after"]["sha256"]
    assert report["frames"] == prior.FRAME_COUNT and report["scripted_input_schedule"] == base.load(inputs)
    photos = prior.TOOL.photos(report)
    candidates = [(frame, item, prior.TOOL.body_masks(image)) for frame, (item, image) in sorted(photos.items())
                  if 4350 <= frame <= 8250]
    cursor = 4350
    shown = []
    for row in receipt["progressive_targets"]:
        expected = prior.TOOL.prior.masks(bytes.fromhex(row["plane"]))
        cursor, observed = next((frame, item) for frame, item, masks in candidates
                                if frame > cursor and masks == expected)
        shown.append(dict(id=row["id"], frame=cursor, selector=row["selector"], observed=observed))

    # Include multiple notice samples so the modal and its dismissal can be read directly.
    samples = [r["frame"] for r in shown] + [
        frame for frame in sorted(photos) if cursor + 325 <= frame <= cursor + 975 and frame % 100 == 0]
    samples.extend(prior.RETURN_FRAMES[-2:])
    boxes = [photos[frame][1].crop((0, 225, 256, 384)) for frame in samples]
    sheet = Image.new("RGB", (1024, 342 * ((len(samples) + 1) // 2)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, box) in enumerate(zip(samples, boxes, strict=True)):
        x, y = i % 2 * 512, i // 2 * 342
        draw.text((x + 5, y + 3), f"{GUESTS[block][0]}   Frame {frame}", fill="white")
        sheet.paste(box.resize((512, 318), Image.Resampling.NEAREST), (x, y + 20))
    sheet_path = root / "complete_exchange.png"
    sheet.save(sheet_path)
    base.save(root / "initialized_exchange.json", dict(candidate_sha256=receipt["candidate_sha256"],
        original_scene_execution_after_initialized_Maria_entry=True, natural_random_activation=False, hardware=False,
        progressive_holds=shown, game_notice_source_hex=receipt["market_notice_exact_hex"],
        captures=[dict(frame=frame, evidence=photos[frame][0]) for frame in samples],
        sheet=str(sheet_path), sheet_sha256=base.digest(sheet_path),
        evidence={str(path):base.digest(path) for path in (setup, inputs, report_path)}))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    parser.add_argument("block", type=int, choices=GUESTS, nargs="?")
    args = parser.parse_args()
    if args.action == "startup":
        FunctionType(inherited.startup.__code__, vars(inherited) | {"stage": stage})()
    else:
        if args.block is None:
            parser.error("Choose the London or Alexandria block.")
        globals()[args.action](args.block)
