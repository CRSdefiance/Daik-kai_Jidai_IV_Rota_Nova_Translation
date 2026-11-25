"""Replay both initialized hosts and their original modal-page transitions."""

from argparse import ArgumentParser
from struct import pack_into
import sys

from scripts import check_rafael_B84_training_gameplay_20261122 as gameplay
from scripts import headless_desmume_v193 as harness
from scripts import replay_maria_opening_wraps_20261114 as maria_boot
from scripts import replay_rafael_B84_training_20261122 as rafael_boot
from scripts import stage_rafael_athens_and_maria_crew_20261122 as stage
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL, validate_capture, validate_fixture


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay_final.json"
SAMPLE = {
    0: ((47, 5), (47, 44), (47, 53), (47, 77), *((48, n) for n in (
        61, 71, 121, 125, 167, 262, 312, 427, 431, 435, 438))),
    3: tuple((116, n) for n in (15, 24, 30, 36, 41, 44, 48, 51, 58, 61, 68, 82)),
}


def receipt(route):
    return ROOT / f"route{route}" / "fixture.json"


def report_path(route):
    directory = "capture" if route == 0 else "capture_followthrough"
    return receipt(route).parent / directory / "capture_report.json"


def run_file(route, name):
    prefix = "" if route == 0 else "followthrough_"
    return receipt(route).parent / f"{prefix}{name}.json"


def fixture(route):
    folder = receipt(route).parent
    assert not folder.exists()
    stored = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert stored["candidate_sha256"] == candidate and stored["whole_parent_inverse"]
    bank_path = f"/data/SC{route}.DK4"
    host_id, prefix_end = (44, 40) if route == 0 else (33, 34)
    clean, image = map(base.NdsImage.open, (native.CLEAN, stage.ROM))
    original = image.read_file(bank_path)
    bank = native.IlnkContainer.parse(original)
    clean_host = native.IlnkContainer.parse(clean.read_file(bank_path)).blocks[host_id]
    host = bank.blocks[host_id]
    inventory, _, _ = native.scoped_inventory()
    arm, clean_arm = image.read_file(native.ARM), clean.read_file(native.ARM)
    init, _ = inventory(arm, host)
    clean_commands, clean_speeches = inventory(clean_arm, clean_host)
    assert host[:4] == clean_host[:4] and host[6:prefix_end] == clean_host[6:prefix_end]
    assert any(c["offset"] == prefix_end for c in init)
    original_tail = clean_speeches[-1]["offset"] + clean_speeches[-1]["native_extent"]
    control_tail = [c["whole_command_hex"] for c in clean_commands if c["offset"] >= original_tail]
    assert control_tail[-1] == "00000000"
    if route == 0:
        assert host[8:40] == bytes.fromhex(base.load(rafael_boot.prior.rafael_scope["OLD_FIXTURE"])["original_prelude"])
        control_tail = control_tail[-1:]
    else:
        assert control_tail[0] == "4062"
        assert sum(c["offset"] < prefix_end for c in init) == 7
        validate_capture(base.load(maria_boot.stage.CAPTURE))
    selected = {(g["block"], ident): c for g in stored["groups"] if g["route"] == route
                for c in g["commands"] for ident in c["record_ids"]}
    continuations = {c["retained_continuation_of"]: c for g in stored["groups"] if g["route"] == route
                     for c in g["commands"] if c.get("retained_continuation_of")}
    payload = bytearray(host[:prefix_end])
    commands = []
    for block, ordinal in SAMPLE[route]:
        ident = f"DK4_MES_B{block}_R{ordinal:04d}"
        sequence = [selected[block, ident]]
        if ident in continuations:
            sequence.append(continuations[ident])
        for number, command in enumerate(sequence, 1):
            raw, start = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert command["word"] == 0x4000 and bank.blocks[block][start:start + len(raw)] == raw
            commands.append(dict(id=ident, block=block, offset=start, page=number, exact_command_hex=raw.hex()))
            payload.extend(raw)
    payload.extend(b"".join(bytes.fromhex(c) for c in control_tail))
    pack_into("<H", payload, 4, len(payload) - 8)
    installed = bytes(payload) + bytes(-len(payload) % 4)
    assert len(installed) < 0x2400
    parsed, speeches = inventory(arm, installed)
    assert [c["whole_command_hex"] for c in speeches] == [r["exact_command_hex"] for r in commands]
    assert [c["whole_command_hex"] for c in parsed[-len(control_tail):]] == control_tail
    bank.blocks[host_id] = installed
    image.replace_file(bank_path, bank.to_bytes())
    folder.mkdir(parents=True)
    rom = folder / f"SC{route}_Athens_And_Crew_FOCUSED_ONLY.nds"
    image.save(rom)
    image.replace_file(bank_path, original)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    digest = base.digest(rom)
    config = dict(candidate_sha256=candidate, rom=str(rom), rom_sha256=digest, exact_inverse=True,
                  host_block=host_id, commands=commands, natural_activation=False)
    if route == 3:
        unlock_path = folder / "unlock_fixture.json"
        unlock = base.load(HISTORICAL)
        unlock.update(production_ROM=str(rom), production_ROM_sha256=digest,
                      current_test_scope="Focused Maria crew story and original consecutive modal pages.")
        base.save(unlock_path, unlock)
        validated = validate_fixture(unlock_path)
        config.update(unlock=str(unlock_path), unlock_sha256=base.digest(unlock_path), save=validated["fixture_save"])
    base.save(receipt(route), config)


def play(route):
    config = base.load(receipt(route))
    assert base.digest(config["rom"]) == config["rom_sha256"]
    first = 4000 if route == 0 else 4200
    steps = [first + i * 370 for i in range(len(config["commands"]) + (route == 3))]
    if route == 0:
        original = base.load(rafael_boot.BOOT.INPUTS)
    else:
        original = base.load(maria_boot.stage.CAPTURE)["scripted_input_schedule"]
    schedule = original + [dict(start=frame, duration=8, buttons=["A"]) for frame in steps]
    holds = [3900, *(f + 300 for f in steps)]
    if route == 3:
        holds = holds[1:]
    inputs = run_file(route, "inputs")
    base.save(inputs, schedule)
    base.save(run_file(route, "holds"), holds)
    options = ["--press-start", "-1"]
    if route == 3:
        assert base.digest(config["unlock"]) == config["unlock_sha256"]
        options = ["--battery-save", config["save"], "--allow-gallery-fixtures",
                   "--gallery-save-fixture-manifest", config["unlock"], "--touchscreen"]
    sys.argv = [harness.__file__, "--rom", config["rom"], "--out", str(report_path(route).parent),
                "--frames", str(holds[-1]+120), "--inputs-json", str(inputs), *options,
                "--capture-every", "999999", "--capture-at", *map(str, holds)]
    harness.main()


def verify():
    displayed, modal, source = map(base.load, (stage.NATIVE, stage.FE_PROOF, stage.REVIEW))
    candidate = base.digest(stage.ROM)
    assert displayed["candidate_sha256"] == modal["candidate_sha256"] == candidate
    names = gameplay.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(native.ARM))
    progressive = {(r["route"], r["id"]): r for r in displayed["records"] if r["layouts"]}
    system = {(r["route"], r["id"], 1 + r["second_page"]): r for r in modal["records"]}
    speakers = {(r["route"], r["id"]): r["speaker"] for r in source["records"]}
    pictures, observations, reports, exits = [], [], {}, {}
    for route in SAMPLE:
        config, report = map(base.load, (receipt(route), report_path(route)))
        assert candidate == config["candidate_sha256"] and config["exact_inverse"]
        assert report["ROM_sha256"] == config["rom_sha256"] == base.digest(config["rom"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["scripted_input_schedule"] == base.load(run_file(route, "inputs"))
        if route == 3:
            validate_capture(report)
        holds = base.load(run_file(route, "holds"))
        for frame, command in zip(holds[:-1], config["commands"], strict=True):
            hold, image = gameplay.screen(report, frame)
            ident, page = command["id"], command["page"]
            if check := system.get((route, ident, page)):
                assert command["exact_command_hex"] == check["exact_command_hex"]
                width, plane = 228, check["physical_plane_hex"]
                title = f"SC{route} {ident} / system page {page}"
            else:
                check = progressive[route, ident]
                assert command["exact_command_hex"] == check["exact_command_hex"]
                raster, = check["layouts"][0]["pages"]
                width, plane = 216, raster["native_plane_hex"]
                label = speakers[route, ident]
                gameplay.glyphs(names, image, label, (16,277), gameplay.LABEL_COLOR, 226)
                title = f"SC{route} {ident} / {label}"
            assert gameplay.mask_check(bytes.fromhex(plane), width, image), (route, ident, page, frame)
            observations.append(dict(file_path=f"/data/SC{route}.DK4", id=ident, page=page,
                capture=hold, system=width==228, exact_complete_body_mask=True))
            pictures.append((title, image))
        hold, image = gameplay.screen(report, holds[-1])
        host_transition = "return to port" if route == 0 else "original crew recruitment notice"
        exits[route] = hold | dict(observed_host_transition=host_transition)
        pictures.append((f"SC{route} / {host_transition}", image))
        reports[route] = base.digest(report_path(route))
    assert sum(row["system"] for row in observations) == 10
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, sha = gameplay.make_sheet(ROOT / f"athens_and_crew_verified_{offset//6+1}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=sha))
    base.save(LIVE, dict(candidate_sha256=candidate, observed_speech_pages=len(observations), observations=observations,
        report_sha256=reports, return_frames=exits, sheets=sheets, initialized_excerpts=True,
        natural_story_triggers_claimed=False, maria_existing_unlock_fixture=True, hardware=False))
    print(f"Verified {len(observations)} initialized panels and both original host transitions.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("rafael", "maria", "maria_followthrough", "verify"))
    action = cli.parse_args().action
    if action == "verify":
        verify()
    elif action == "maria_followthrough":
        play(3)
    else:
        route = 0 if action == "rafael" else 3
        fixture(route)
        play(route)
