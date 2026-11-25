"""Play revised Hodram and Lil dialogue and verify both original Lil choices."""

from argparse import ArgumentParser
from inspect import getsource
from struct import pack_into
from types import FunctionType
import sys

from PIL import Image

from scripts import replay_fernando_parallel_routes_20261121 as cold
from scripts import replay_rafael_proof_and_financing_20261122 as menu
from scripts import replay_tavern_and_proof_exchanges_20261122 as excerpt
from scripts import stage_hodram_and_lil_followups_20261122 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as checks
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
INPUTS = {route: cold.CASES[route]["input"] for route in (1, 2)}
CHOICE_ROOT = ROOT / "choice"
CHOICE_ROM = CHOICE_ROOT / "SC2_Lil_Original_Choice_FOCUSED_ONLY.nds"
CHOICE_RECEIPT = CHOICE_ROOT / "fixture.json"
HOLDS = (3900, 4300, 4630, 4970, 5350, 5740)
BRANCHES = {"accept": (164, 167), "refuse": (194, 197)}
SAMPLES = {
    1: ((17, 68), (17, 91), (17, 211), (17, 269), (85, 57), (85, 64), (85, 123)),
    2: ((26, 23), (26, 35), (26, 80), (26, 90), (26, 98), (26, 101), (26, 104),
        (26, 196), (26, 397), (26, 445), (133, 5), (133, 29), (133, 96), (133, 190), (133, 213)),
}


def route_config(route):
    sample = SAMPLES[route]
    host = cold.CASES[route]
    return dict(opening=host["opening"], prefix=host["prefix"], end=4100 + len(sample) * 360,
                input=INPUTS[route], sample=sample)


def route_rom(route):
    return ROOT / f"route{route}" / f"SC{route}_Hodram_And_Lil_FOCUSED_ONLY.nds"


def report(run):
    return ROOT / run / "capture/capture_report.json"


def replay(route):
    scope = excerpt.scope | globals() | dict(
        CASES={route: route_config(route)}, SAMPLE=SAMPLES[route], ROM=route_rom(route))
    exec(compile(excerpt.replay_source, __file__ + "::route-replay", "exec"), scope)
    scope["replay"](route)


def formatting():
    glyphs = FunctionType(checks.check_glyphs.__code__, checks.check_glyphs.__globals__ | dict(stage=stage, OUTPUT=GLYPHS))
    glyphs()
    modal_source = checked_text(getsource(checks.check_modal), {
        'assert len(records) == 10 and sum(r["second_page"] for r in records) == 2':
            'assert len(records) == 4 and not any(r["second_page"] for r in records)',
        'Verified all ten modal pages, including both original two-page Maria sequences.':
            'Verified all four original Lil notices with the native modal consumer.',
    })
    scope = vars(checks) | globals() | dict(display=checks.display)
    exec(compile(modal_source, __file__ + "::original-notices", "exec"), scope)
    scope["check_modal"]()


def display_context():
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    paint = stage.established.display.clipped_renderer(ctx)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    names = menu.gameplay.GameAsciiFont.from_arm9(ctx.arm)
    return ctx, paint, font, names


def panel_mask(row, pages, modal, ctx, paint, font):
    if exact := modal.get((row["route"], row["id"])):
        assert not exact["second_page"]
        return 228, bytes.fromhex(exact["physical_plane_hex"])
    view = pages[row["route"], row["id"]]
    if view["layouts"]:
        page, = view["layouts"][0]["pages"]
    else:
        raw = bytes.fromhex(view["body_hex"])[1:]
        assert not any(token in raw for token in (b"FI", b"FA", b"FO", b"FU"))
        result = paint(ctx.arm, font, raw)
        assert result["complete_consumed_bytes"] == len(raw)
        page, = result["pages"]
    return 216, bytes.fromhex(page["native_plane_hex"])


def verify_excerpts():
    proof, layout, source, fe = map(base.load, (stage.PROOF, stage.NATIVE, stage.REVIEW, stage.FE_PROOF))
    candidate = base.digest(stage.ROM)
    assert proof["candidate_sha256"] == layout["candidate_sha256"] == fe["candidate_sha256"] == candidate
    ctx, paint, font, names = display_context()
    pages = {(row["route"], row["id"]): row for row in layout["records"]}
    owners = {(row["route"], row["id"]): row for row in source["records"]}
    modals = {(row["route"], row["id"]): row for row in fe["records"]}
    observations, pictures, reports, exits = [], [], {}, {}
    for route, sample in SAMPLES.items():
        run = f"route{route}"
        rom = route_rom(route)
        fixture = base.load(rom.with_name("fixture.json"))
        capture = base.load(report(run))
        assert fixture["candidate_sha256"] == candidate and fixture["exact_candidate_inverse"]
        assert not fixture["natural_activation"]
        verify_capture(capture, rom, fixture["fixture_sha256"], rom.with_name("inputs.json"))
        shots = {}
        for hold in capture["frames_captured"]:
            assert base.digest(hold["path"]) == hold["PNG_sha256"]
            with Image.open(hold["path"]) as image:
                shots[hold["frame"]] = hold, image.convert("RGB")
        assert capture["frames"] == route_config(route)["end"]
        cursor = 3800
        for (block, ordinal), command in zip(sample, fixture["copied_native_commands"], strict=True):
            ident = record_id(block, ordinal)
            row = owners[route, ident]
            width, plane = panel_mask(row, pages, modals, ctx, paint, font)
            assert command["ids"] == [ident]
            assert command["command_sha256"] == native.digest(bytes.fromhex(pages[route, ident]["exact_command_hex"]))
            for frame, (hold, image) in shots.items():
                if frame > cursor + 140 and menu.gameplay.mask_check(plane, width, image):
                    break
            else:
                raise AssertionError((route, ident, cursor))
            cursor = frame
            if width == 216:
                menu.gameplay.glyphs(names, image, row["speaker"], (16, 277), menu.gameplay.LABEL_COLOR, 226)
            observations.append(observation(row, run, hold, command["original_offset"]))
            pictures.append((f"SC{route} {ident} / {row['speaker']}", image))
        end = route_config(route)["end"] - 1
        hold, image = shots[end]
        assert cursor < end
        exits[run] = hold
        pictures.append((f"SC{route} / original opening host exit", image))
        reports[run] = base.digest(report(run))
    return observations, pictures, reports, exits


def observation(row, run, hold, offset):
    return dict(file_path=row["file_path"], id=row["id"], run=run, capture=hold,
                stored_offset=offset, speaker=row["speaker"], exact_complete_body_mask=True)


def record_id(block, ordinal):
    return f"DK4_MES_B{block}_R{ordinal:04d}"


def verify_capture(capture, rom, digest, inputs):
    assert capture["ROM_sha256"] == digest == base.digest(rom)
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not capture.get("battery_save_preloaded")
    assert capture["scripted_input_schedule"] == base.load(inputs)


def prepare_choice():
    proof = base.load(stage.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM) and proof["whole_parent_inverse"]
    group, = [row for row in proof["groups"] if (row["route"], row["block"]) == (2, 133)]
    if CHOICE_RECEIPT.exists():
        receipt = base.load(CHOICE_RECEIPT)
        assert receipt["candidate_sha256"] == proof["candidate_sha256"] and receipt["exact_inverse"]
        assert receipt["rom_sha256"] == base.digest(CHOICE_ROM)
        return
    path = group["file_path"]
    image, predecessor = map(base.NdsImage.open, (stage.ROM, stage.parent.ROM))
    original = image.read_file(path)
    archive = native.IlnkContainer.parse(original)
    config = route_config(2)
    opening, prefix = config["opening"], config["prefix"]
    host, event = archive.blocks[opening], archive.blocks[133]
    assert native.digest(event) == group["after"]
    assert native.IlnkContainer.parse(predecessor.read_file(path)).blocks[opening] == host
    inventory, _, _ = native.scoped_inventory()
    arm = image.read_file(native.ARM)
    assert next(c["offset"] for c in inventory(arm, host)[0] if c["word"] == 0x4000) == prefix
    commands = group["commands"]
    first = next(i for i, c in enumerate(commands) if record_id(133, 145) in c["record_ids"])
    start = commands[first]["stored_offset"]
    last = menu.stage.paired.logical_end(event)
    payload = bytearray(host[:prefix] + event[start:last])
    pack_into("<H", payload, 4, len(payload) - 8)
    body = bytes(payload) + bytes(-len(payload) % 4)
    installed = {c["offset"]: c for c in inventory(arm, body)[0]}
    shift = prefix - start
    assert len([c for c in installed.values() if c["word"] == 0x2100]) == 1
    relative_branches = []
    for row in commands[first:]:
        at = row["stored_offset"]
        cmd = installed[at + shift]
        extent = cmd["native_extent"]
        assert cmd["whole_command_hex"] == event[at:at + extent].hex()
        if "target_command_index" in row:
            target = commands[row["target_command_index"]]["stored_offset"]
            assert menu.stage.paired.jump(bytes.fromhex(row["stored"]), at + shift) == target + shift
            assert target + shift in installed
            relative_branches.append(dict(original_offset=at, target=target, fixture_offset=at+shift, fixture_target=target+shift))
    archive.blocks[opening] = body
    image.replace_file(path, archive.to_bytes())
    CHOICE_ROOT.mkdir(parents=True)
    image.save(CHOICE_ROM)
    image.replace_file(path, original)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    base.save(CHOICE_RECEIPT, dict(candidate_sha256=proof["candidate_sha256"], rom=str(CHOICE_ROM),
        rom_sha256=base.digest(CHOICE_ROM), exact_inverse=True, natural_activation=False,
        initialization_block=opening, exact_contiguous_suffix_source_block=133, original_start=start,
        original_end=last, preserved_relative_branches=relative_branches))


def play_choice(run):
    fixture = base.load(CHOICE_RECEIPT)
    assert fixture["rom_sha256"] == base.digest(CHOICE_ROM)
    steps = [(4000, "A"), (4340, "A"), (5050, "A"), (5440, "A")]
    if run == "refuse":
        steps.insert(2, (4770, "DOWN"))
    out = report(run).parent
    out.parent.mkdir(exist_ok=True)
    schedule = base.load(INPUTS[2]) + [dict(start=f, duration=5, buttons=[button]) for f, button in steps]
    inputs = out.parent / "inputs.json"
    base.save(inputs, schedule)
    harness = menu.precedent.HARNESS
    sys.argv = [harness.__file__, "--rom", str(CHOICE_ROM), "--out", str(out),
        "--frames", str(HOLDS[-1] + 120), "--inputs-json", str(inputs), "--press-start", "-1",
        "--capture-every", "999999", "--capture-at", *map(str, HOLDS)]
    harness.main()


def verify_choice():
    proof, draft, fixture, layouts = map(base.load, (stage.PROOF, stage.REVIEW, CHOICE_RECEIPT, stage.NATIVE))
    candidate = proof["candidate_sha256"]
    assert fixture["candidate_sha256"] == layouts["candidate_sha256"] == candidate == base.digest(stage.ROM)
    assert fixture["exact_inverse"] and not fixture["natural_activation"]
    group, = [r for r in proof["groups"] if (r["route"], r["block"]) == (2, 133)]
    file_path = group["file_path"]
    image = base.NdsImage.open(stage.ROM)
    arc = image.read_file(file_path)
    bank = native.IlnkContainer.parse(arc).blocks[133]
    choice, = [c for c in group["commands"] if c["word"] == 0x2100]
    raw, start = bytes.fromhex(choice["stored"]), choice["stored_offset"]
    assert choice["current"] == choice["stored"] and bank[start:start+len(raw)] == raw
    captions = []
    for row in draft["retained_choice_labels"]:
        ref = row["current_reference"]
        offset = start + ref["offset"] - ref["command_offset"]
        body = bytes.fromhex(ref["exact_body_hex"])
        assert raw.hex() == ref["exact_command_hex"] and bank[offset:offset+len(body)+1] == body+b"\x00"
        assert body.decode("ascii") == row["english"]
        registered = dict(file_path=file_path, block=133, candidate_sha256=candidate,
            archive_sha256=native.digest(arc), block_sha256=group["after"], command_offset=start,
            offset=offset, exact_command_hex=raw.hex(), exact_body_hex=body.hex())
        captions.append(row | dict(registered_reference=registered, review=row["review"] | dict(formatting=True)))

    ctx, paint, font, names = display_context()
    pages = {(r["route"], r["id"]): r for r in layouts["records"]}
    owners = {r["id"]: r for r in draft["records"] if (r["route"], r["block"]) == (2, 133)}
    commands = {ident: c for c in group["commands"] for ident in c["record_ids"]}
    labels = [r["english"] for r in captions]
    observations, pictures, reports, choices = [], [], {}, []
    for selected, (run, responses) in enumerate(BRANCHES.items()):
        capture = base.load(report(run))
        verify_capture(capture, CHOICE_ROM, fixture["rom_sha256"], report(run).parent.parent / "inputs.json")
        reports[run] = base.digest(report(run))
        menu_frames = []
        for frame in (4630, 4970):
            hold, image = menu.gameplay.screen(capture, frame)
            menu_frames.append(dict(capture=hold, labels=menu.gameplay.captions(names, image, labels)))
            pictures.append((f"Lil / {run} choice at frame {frame}", image))
        first, last = [[r["background"] for r in moment["labels"]] for moment in menu_frames]
        assert first[0] == menu.gameplay.MENU_HIGHLIGHT and first[1] != menu.gameplay.MENU_HIGHLIGHT
        assert last == (first[::-1] if selected else first)
        for ordinal, frame in zip((145, 148, *responses), (3900, 4300, 5350, 5740), strict=True):
            ident = record_id(133, ordinal)
            row = owners[ident]
            hold, image = menu.gameplay.screen(capture, frame)
            width, plane = panel_mask(row, pages, {}, ctx, paint, font)
            assert menu.gameplay.mask_check(plane, width, image), (run, ident, frame)
            menu.gameplay.glyphs(names, image, row["speaker"], (16, 277), menu.gameplay.LABEL_COLOR, 226)
            observations.append(observation(row, run, hold, commands[ident]["stored_offset"]))
            if ordinal in responses:
                pictures.append((f"Lil / {ident} / {row['speaker']}", image))
        choices.append(dict(run=run, selected=selected, caption=labels[selected],
            response=record_id(133, responses[0]), original_branch_executed=True, observations=menu_frames))
    base.save(stage.CHOICE_PROOF, dict(candidate_sha256=candidate, captions=captions,
        exact_retained_choice_object=raw.hex(), original_choice_consumer=True,
        preserved_relative_branches=fixture["preserved_relative_branches"], both_branches_observed=True))
    return observations, pictures, reports, choices


def verify():
    observations, pictures, reports, exits = verify_excerpts()
    branch_observations, branch_pictures, branch_reports, choices = verify_choice()
    observations.extend(branch_observations)
    pictures.extend(branch_pictures)
    reports.update(branch_reports)
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, sha = menu.gameplay.make_sheet(ROOT / f"hodram_and_lil_gameplay_{1 + offset // 6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=sha))
    base.save(LIVE, dict(candidate_sha256=base.digest(stage.ROM), observed_speech_pages=len(observations),
        observations=observations, report_sha256=reports, return_frames=exits, original_menu_choices=choices,
        sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} dialogue and notice holds, both original Lil branches, and both host exits.", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("hodram", "lil", "formatting", "prepare_choice", "verify", *BRANCHES))
    case = parser.parse_args().case
    if case == "formatting":
        formatting()
    elif case == "prepare_choice":
        prepare_choice()
    elif case in BRANCHES:
        play_choice(case)
    elif case == "verify":
        verify()
    else:
        replay(1 if case == "hodram" else 2)
