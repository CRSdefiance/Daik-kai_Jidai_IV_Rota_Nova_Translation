"""Play representative original town quest branches from the initialized Maria entry."""

from argparse import ArgumentParser
import sys
from struct import pack_into, unpack_from
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import replay_alexandria_cooking_20261114 as prior
from scripts import replay_embedded_story_roles_20261115 as inherited
from scripts import stage_town_quest_exchanges_20261115 as stage

base, native = stage.base, stage.native
FILE = "/data/SC3.DK4"
CASES = {"book": ("book", 170, (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19)),
         "prophecy": ("prophecy", 186, (*range(14), 15, 16, 17)),
         "sextant": ("sextant_request", 299, tuple(range(9)))}
LAST = 13251
CAPTURES = (*range(4350, 11951, 25), 12500, 13100)


def folder(case):
    return stage.ROOT / ("replay_" + case)


def inputs(case):
    base_inputs = base.load(prior.precedent.stage.CAPTURE)["scripted_input_schedule"]
    if case != "book":
        actions = [(frame, "A") for frame in range(4200, 11901, 325)]
    else:
        actions = ([(frame, "A") for frame in range(4200, 6151, 325)]
                   + [(6380, "DOWN"), (6520, "DOWN")]
                   + [(frame, "A") for frame in range(6800, 11901, 325)])
    return base_inputs + [dict(start=frame, duration=16, buttons=[button]) for frame, button in actions]


def prepare(case):
    group, block, selected = CASES[case]
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged["candidate_sha256"]
    image = base.NdsImage.open(stage.ROM)
    arm, archive = (image.read_file(path) for path in (native.ARM, FILE))
    bank = native.IlnkContainer.parse(archive)
    host, guest = bank.blocks[33], bank.blocks[block]
    inventory, _, _ = native.scoped_inventory()
    host_commands, host_speech = inventory(arm, host)
    host_end = host_speech[-1]["offset"] + host_speech[-1]["native_extent"]
    cleanup = [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] >= host_end]
    assert cleanup[0] == "4062" and cleanup[-1] == "00000000"
    prefix = [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] < 34]
    assert len(prefix) == 7
    guest_end = 8 + unpack_from("<H", guest, 4)[0]
    guest_commands, _ = inventory(arm, guest)
    assert guest_commands[-1]["whole_command_hex"] == "00000000"
    body = bytearray(host[:34] + guest[8:guest_end - 4] + bytes.fromhex("".join(cleanup)))
    pack_into("<H", body, 4, len(body) - 8)
    inserted = bytes(body) + bytes(-len(body) % 4)
    commands, _ = inventory(arm, inserted)
    assert [r["whole_command_hex"] for r in commands] == (
        prefix + [r["whole_command_hex"] for r in guest_commands[:-1]] + cleanup)

    root = folder(case)
    root.mkdir()
    target = root / f"{case}_initialized_RESEARCH_ONLY.nds"
    bank.blocks[33] = inserted
    image.replace_file(FILE, bank.to_bytes())
    image.save(target)
    bank.blocks[33] = host
    assert bank.to_bytes() == archive
    image.replace_file(FILE, archive)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    unlock_path = root / "existing_system_only_unlock.json"
    unlock = base.load(prior.precedent.HISTORICAL)
    unlock.update(production_ROM=str(target), production_ROM_sha256=base.digest(target),
                  current_test_scope=f"Complete {group} from the initialized Maria entry.")
    base.save(unlock_path, unlock)
    prior.precedent.validate_fixture(unlock_path)
    base.save(root / "inputs.json", inputs(case))

    _, paint = native.layout.prior.precedent.planners(arm)
    font = image.read_file("/GRP/KANJI.FNT")
    rows = [r for r in base.load(stage.MANUSCRIPT)["records"]
            if r["file_path"] == FILE and r["block"] == block]
    planes = []
    for row in rows:
        if row["turn"] not in selected:
            continue
        raw = bytes.fromhex(row["staged_reference"]["raw_hex"])
        assert raw[0] != 254
        pages = row["after_native"]["pages"] if row["decision"] == "revision" else paint(arm, font, raw[1:])["pages"]
        for pg in pages:
            planes.append(dict(id=row["id"], kind=row["kind"], turn=row["turn"], page=pg["page"],
                               plane=pg["native_plane_hex"]))
    base.save(root / "fixture.json", dict(reference_ROM_sha256=staged["candidate_sha256"],
        fixture=str(target), fixture_sha256=base.digest(target), unlock=str(unlock_path),
        original_scene_commands_exact=True, whole_source_ROM_inverse=True, expected_pages=planes))


def capture(case):
    root = folder(case)
    fixture = base.load(root / "fixture.json")
    assert base.digest(fixture["fixture"]) == fixture["fixture_sha256"]
    unlock = prior.precedent.validate_fixture(fixture["unlock"])
    existing_argv = sys.argv
    try:
        sys.argv = [existing_argv[0], "--rom", fixture["fixture"], "--out", str(root / "capture"),
                    "--frames", str(LAST), "--inputs-json", str(root / "inputs.json"), "--touchscreen",
                    "--battery-save", unlock["fixture_save"], "--allow-gallery-fixtures",
                    "--gallery-save-fixture-manifest", fixture["unlock"], "--capture-every", "999999",
                    "--capture-at", *map(str, CAPTURES)]
        prior.precedent.harness.main()
    finally:
        sys.argv = existing_argv


def verify(case):
    root = folder(case)
    fixture = base.load(root / "fixture.json")
    report_path = root / "capture/capture_report.json"
    report = base.load(report_path)
    prior.precedent.validate_capture(report)
    assert report["ROM_sha256"] == fixture["fixture_sha256"]
    assert report["frames"] == LAST and report["scripted_input_schedule"] == inputs(case)
    photos = prior.TOOL.photos(report)
    masks = [(n, prior.TOOL.body_masks(image)) for n, (_, image) in sorted(photos.items())]
    observed, cursor = [], 4350
    for row in fixture["expected_pages"]:
        expected = prior.TOOL.prior.masks(bytes.fromhex(row["plane"]))
        found = next((n for n, bits in masks if n > cursor and bits == expected), None)
        assert found is not None, (case, row["id"], row["turn"], row["page"], cursor)
        cursor = found
        observed.append(dict(id=row["id"], turn=row["turn"], page=row["page"], frame=cursor))
    extra = (6300, 6450, 6650) if case == "book" else ()
    extra += (12500, 13100)
    sample_frames = sorted(set(extra) | {r["frame"] for r in observed})
    sheets = []
    for first in range(0, len(sample_frames), 8):
        frames = sample_frames[first:first+8]
        image = Image.new("RGB", (1024, 398 * ((len(frames)+1)//2)), "#263238")
        draw = ImageDraw.Draw(image)
        for i, frame in enumerate(frames):
            x, y = i % 2 * 512, i // 2 * 398
            draw.text((x + 5, y + 3), f"{case}   frame {frame}", fill="white")
            picture = photos[frame][1].crop((0,192,256,384))
            image.paste(picture.resize((512,384),Image.Resampling.NEAREST),(x,y+13))
        path = root / f"live_{len(sheets)+1}.png"
        image.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    base.save(root / "verified.json", dict(candidate_sha256=fixture["reference_ROM_sha256"], scenario=case,
        initialized_emulator=True, natural_activation=False, hardware=False, complete_holds=observed,
        report=str(report_path), sheets=sheets, supporting_frames=[photos[n][0] for n in sample_frames],
        evidence={str(path):base.digest(path) for path in (report_path, root/"fixture.json", root/"inputs.json")}))
    print(case, len(observed), "complete page holds")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify", "startup"))
    parser.add_argument("case", choices=CASES, nargs="?")
    args = parser.parse_args()
    if args.action == "startup":
        FunctionType(inherited.startup.__code__, vars(inherited) | {"stage": stage})()
    else:
        if args.case is None:
            parser.error("Choose a quest scenario.")
        globals()[args.action](args.case)
