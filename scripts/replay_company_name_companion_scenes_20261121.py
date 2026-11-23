"""Play exact staged dialogue and the preserved speakerless sequence in initialized routes."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
import sys

from scripts import headless_desmume_v193 as harness
from scripts import stage_company_name_companion_scenes_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "replays"
CAPTURE_ROOT = stage.EVIDENCE_ROOT / "replays"
RAFAEL_INPUTS = Path("work/papal_states_titis_20261118/research_v1/rafael_snapshot_inputs.json")
MARIA_INPUTS = Path("work/item_gallery_wraps_20261121/startup/inputs.json")
UNLOCK = Path("work/analysis/gallery_v521/gallery-test-only.dsv")
CONFIG = {
    "rafael": (0, 44, 40, 10, 84, (89, 93, 97, 100, 103, 106, 110), 3800, 275, 6501),
    "maria": (3, 33, 34, 7, 116, (41, 44, 48, 51, 54, 102, 106, 110, 113), 4200, 350, 9401),
}


def prepare(name):
    route, host_number, prefix_length, prefix_count, scene, selection, begin, stride, frames = CONFIG[name]
    root = ROOT / name
    assert not root.exists()
    candidate = base.load(stage.PROOF)["candidate_sha256"]
    assert base.digest(stage.ROM) == candidate
    image = base.NdsImage.open(stage.ROM)
    path = f"/data/SC{route}.DK4"
    arm, archive = image.read_file(native.ARM), image.read_file(path)
    bank = native.IlnkContainer.parse(archive)
    scan, _, _ = native.scoped_inventory()
    entry = bank.blocks[host_number]
    commands, speech = scan(arm, entry)
    prefix = [c["word"] for c in commands if c["offset"] < prefix_length]
    assert len(prefix) == prefix_count and speech[0]["offset"] == prefix_length
    if route == 0:
        suffix = bytes(4)
    else:
        last = speech[-1]
        suffix = entry[last["offset"] + last["native_extent"]:stage.stage.logical_end(entry)]
        assert suffix[:2] == b"\x40\x62" and suffix[-4:] == bytes(4)
    records = {r["source_reference"]["record_index"]: r for r in base.load(stage.REVIEW)["records"] if r["route"] == route}
    selected, payloads = [], []
    for index in selection:
        row = records[index]
        for page, installed in enumerate(row["target_pages"], 1):
            command = bytes.fromhex(installed["exact_command_hex"])
            offset = installed["offset"]
            assert bank.blocks[scene][offset:offset + len(command)] == command
            selected.append(dict(id=row["id"], page=page, record_index=index, stored_hex=command.hex()))
            payloads.append(command)
    raw = bytearray(entry[:prefix_length] + b"".join(payloads) + suffix)
    pack_into("<H", raw, 4, len(raw)-8)
    raw.extend(bytes(-len(raw) % 4))
    parsed, stored = scan(arm, raw)
    assert [cmd["word"] for cmd in parsed[:len(prefix)]] == prefix
    assert [cmd["whole_command_hex"] for cmd in stored] == [p.hex() for p in payloads]
    root.mkdir(parents=True)
    rom = root / f"{name}_RESEARCH_ONLY.nds"
    bank.blocks[host_number] = bytes(raw)
    image.replace_file(path, bank.to_bytes())
    image.save(rom)
    bank.blocks[host_number] = entry
    assert bank.to_bytes() == archive
    image.replace_file(path, archive)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    spec = RAFAEL_INPUTS if route == 0 else MARIA_INPUTS
    inputs = [a for a in base.load(spec) if a["start"] < begin]
    inputs += [dict(start=n, duration=8, buttons=["A"]) for n in range(begin, frames-130, stride)]
    plan = root / "inputs.json"
    base.save(plan, inputs)
    base.save(root / "fixture.json", dict(candidate_sha256=candidate, fixture_sha256=base.digest(rom), fixture=str(rom),
        initialized_route=route, frames=frames, control_plan=str(plan), control_sha256=base.digest(plan), selected=selected,
        whole_parent_ROM_inverse=True, exact_individual_dialogue_and_FE_commands=True, natural_activation=False))


def capture(name):
    root = ROOT / name
    setup = base.load(root / "fixture.json")
    assert base.digest(setup["fixture"]) == setup["fixture_sha256"]
    assert base.digest(setup["control_plan"]) == setup["control_sha256"]
    end = setup["frames"]
    frames = range(3650 if name == "rafael" else 4075, end, 25)
    sys.argv = [harness.__file__, "--rom", setup["fixture"], "--out", str(CAPTURE_ROOT / name / "capture"),
        "--frames", str(end), "--inputs-json", setup["control_plan"], "--capture-every", "999999",
        "--capture-at", *map(str, frames)]
    if name == "maria":
        assert base.digest(UNLOCK) == "295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949"
        sys.argv.extend(("--battery-save", str(UNLOCK), "--touchscreen"))
    harness.main()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture"))
    cli.add_argument("name", choices=tuple(CONFIG))
    args = cli.parse_args()
    globals()[args.action](args.name)
