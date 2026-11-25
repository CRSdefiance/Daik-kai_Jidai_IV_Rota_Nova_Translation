"""Verify Rafael's revised panels and both original preparation choices."""

from argparse import ArgumentParser
from struct import pack_into
import sys

from scripts import check_rafael_B84_training_gameplay_20261122 as gameplay
from scripts import replay_rafael_B84_training_20261122 as precedent
from scripts import stage_rafael_proof_and_financing_20261122 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RUNS = ("speech", "ask", "alone")
MENU_HOLDS = (3900, 4300, 4630, 4970, 5350)
ARCHIVE = stage.paired.ARCHIVE


def report(name):
    return ROOT / name / "capture/capture_report.json"


def exact_fixture(kind):
    folder = ROOT / kind
    proof = base.load(stage.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM) and proof["whole_parent_inverse"]
    receipt = folder / "fixture.json"
    if receipt.exists():
        previous = base.load(receipt)
        assert previous["candidate_sha256"] == proof["candidate_sha256"] and previous["exact_inverse"]
        assert base.digest(previous["rom"]) == previous["rom_sha256"]
        return
    image = base.NdsImage.open(stage.ROM)
    original = image.read_file(ARCHIVE)
    archive = native.IlnkContainer.parse(original)
    host = archive.blocks[44]
    expected = base.load(precedent.prior.rafael_scope["OLD_FIXTURE"])["original_prelude"]
    assert host[8:40].hex() == expected
    payload = bytearray(host[:40])
    by_block = {g["block"]: g for g in proof["groups"]}
    if kind == "speech":
        selected = [(g["block"], c) for g in proof["groups"] for c in g["commands"]
            if any(ident in g["plans"] and not ident.endswith("R0449") or ident.endswith("R0264")
                   for ident in c["record_ids"])]
        assert len(selected) == 16
        selected.append((44, by_block[44]["commands"][-1]))
    else:
        commands = by_block[44]["commands"]
        first = next(i for i, c in enumerate(commands) if "DK4_MES_B44_R0446" in c["record_ids"])
        selected = [(44, c) for c in commands[first:]]
        assert sum(c["word"] == 0x2100 for _, c in selected) == 1
    sequence = []
    for block, command in selected:
        at, raw = command["stored_offset"], bytes.fromhex(command["stored"])
        assert archive.blocks[block][at:at + len(raw)] == raw
        sequence.append(command | dict(block=block, fixture_offset=len(payload)))
        payload.extend(raw)
    pack_into("<H", payload, 4, len(payload) - 8)
    compiled = bytes(payload) + bytes(-len(payload)%4)
    assert len(compiled) < 0x2400
    inventory, _, _ = native.scoped_inventory()
    parsed, _ = inventory(image.read_file(native.ARM), compiled)
    found = {c["offset"]: c for c in parsed}
    for row in sequence:
        cmd = found[row["fixture_offset"]]
        expected = row["stored"]
        if row["word"] == 0x0100 and kind == "choice":
            at = row["stored_offset"]
            expected = host[at:at+cmd["native_extent"]].hex()
        assert cmd["word"] == row["word"] and cmd["whole_command_hex"] == expected, (kind, row["word"], row["stored_offset"])
    if kind == "choice":
        shift = sequence[0]["fixture_offset"] - sequence[0]["stored_offset"]
        candidate_rows = by_block[44]["commands"]
        assert all(row["fixture_offset"]-row["stored_offset"] == shift for row in sequence)
        for row in sequence:
            if "target_command_index" in row:
                target = candidate_rows[row["target_command_index"]]["stored_offset"] + shift
                assert target in found or target == stage.paired.logical_end(compiled)
                assert stage.paired.jump(bytes.fromhex(row["stored"]), row["fixture_offset"]) == target
    folder.mkdir(parents=True)
    archive.blocks[44] = compiled
    image.replace_file(ARCHIVE, archive.to_bytes())
    path = folder / f"Rafael_Proof_And_Financing_{kind}_FOCUSED_ONLY.nds"
    image.save(path)
    image.replace_file(ARCHIVE, original)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    base.save(receipt, dict(candidate_sha256=proof["candidate_sha256"], rom=str(path),
        rom_sha256=base.digest(path), exact_inverse=True, original_menu_suffix=kind=="choice",
        commands=sequence, natural_story_activation=False))


def play(name):
    kind = "speech" if name == "speech" else "choice"
    fixture = base.load(ROOT / kind / "fixture.json")
    assert base.digest(fixture["rom"]) == fixture["rom_sha256"]
    if name == "speech":
        steps = [(4000 + 370*i, "A") for i in range(len(fixture["commands"])-1)]
        holds = (3900, *(f+300 for f, _ in steps))
    else:
        steps = [(4000, "A"), (4340, "A"), (5050, "A")]
        if name == "alone":
            steps.insert(2, (4770, "DOWN"))
        if name == "ask":
            steps.append((5440, "A"))
        holds = (*MENU_HOLDS, 5740) if name == "ask" else MENU_HOLDS
    folder = ROOT / name
    folder.mkdir(exist_ok=True)
    schedule = base.load(precedent.BOOT.INPUTS) + [
        dict(start=f, duration=5, buttons=[button]) for f, button in steps]
    inputs = folder / "inputs.json"
    base.save(inputs, schedule)
    base.save(folder / "holds.json", holds)
    harness = precedent.HARNESS
    sys.argv = [harness.__file__, "--rom", fixture["rom"], "--out", str(report(name).parent),
        "--frames", str(holds[-1]+120), "--inputs-json", str(inputs), "--press-start", "-1",
        "--capture-every", "999999", "--capture-at", *map(str, holds)]
    harness.main()


def verify():
    assert not LIVE.exists()
    native_report, modal, choice, review, proof = map(
        base.load, (stage.NATIVE, stage.FE_PROOF, stage.CHOICE_PROOF, stage.REVIEW, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert all(value["candidate_sha256"]==candidate for value in (native_report, modal, choice, proof))
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    paint = gameplay.display.clipped_renderer(ctx)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    names = gameplay.GameAsciiFont.from_arm9(ctx.arm)
    expected = {row["id"]: row for row in native_report["records"]}
    speakers = {row["id"]: row["speaker"] for row in review["records"]}
    commands = {ident: cmd for g in proof["groups"] for cmd in g["commands"] for ident in cmd["record_ids"]}
    observations, menu_observations, pictures, reports = [], [], [], {}

    def check_panel(data, ident, frame, run):
        hold, image = gameplay.screen(data, frame)
        if ident == modal["owner"]:
            width, plane = 228, modal["physical_plane_hex"]
            caption = "Original 30,000 gold notice"
        else:
            check = expected[ident]
            if check["layouts"]:
                page, = check["layouts"][0]["pages"]
            else:
                raw = bytes.fromhex(check["body_hex"])[1:]
                assert not any(v in raw for v in (b"FI", b"FA", b"FO", b"FU"))
                rendered = paint(ctx.arm, font, raw)
                assert rendered["complete_consumed_bytes"] == len(raw)
                page, = rendered["pages"]
            width, plane = 216, page["native_plane_hex"]
            label = speakers[ident]
            gameplay.glyphs(names, image, label, (16,277), gameplay.LABEL_COLOR, 226)
            caption = f"{ident} / {label}"
        assert gameplay.mask_check(bytes.fromhex(plane), width, image), (run, ident, frame)
        observations.append(dict(file_path=ARCHIVE, id=ident, run=run, capture=hold,
            stored_offset=commands[ident]["stored_offset"], exact_complete_body_mask=True))
        pictures.append((caption, image))

    for name in RUNS:
        key = "speech" if name == "speech" else "choice"
        fixture, data = map(base.load, (ROOT/key/"fixture.json", report(name)))
        assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"]
        assert data["ROM_sha256"] == fixture["rom_sha256"] == base.digest(fixture["rom"])
        assert data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
        assert not data.get("battery_save_preloaded")
        assert data["scripted_input_schedule"] == base.load(ROOT/name/"inputs.json")
        holds = base.load(ROOT/name/"holds.json")
        reports[name] = base.digest(report(name))
        if name == "speech":
            for row, frame in zip(fixture["commands"][:-1], holds[:-1], strict=True):
                ident, = row["record_ids"]
                check_panel(data, ident, frame, name)
            exit_frame, image = gameplay.screen(data, holds[-1])
            pictures.append(("Return to port", image))
            continue
        check_panel(data, "DK4_MES_B44_R0449", 4300, name)
        captions = [row["english"] for row in choice["captions"]]
        frames = []
        for frame in (4630, 4970):
            hold, image = gameplay.screen(data, frame)
            visible = gameplay.captions(names, image, captions)
            frames.append(dict(capture=hold, labels=visible))
            pictures.append((f"{name.capitalize()} choice at frame {frame}", image))
        first, last = ([r["background"] for r in s["labels"]] for s in frames)
        assert first[0] == gameplay.MENU_HIGHLIGHT and first[1] != gameplay.MENU_HIGHLIGHT
        selected = int(name == "alone")
        assert last == (first[::-1] if selected else first)
        response = "DK4_MES_B44_R0479" if selected else "DK4_MES_B44_R0464"
        check_panel(data, response, 5350, name)
        if not selected:
            check_panel(data, "DK4_MES_B44_R0469", 5740, name)
        menu_observations.append(dict(run=name, selected=selected, caption=captions[selected], response=response,
            original_branch_executed=True, observations=frames))
    assert len(observations) == 21 and len(menu_observations) == 2
    sheets = []
    for i in range(0, len(pictures), 6):
        path, sha = gameplay.make_sheet(ROOT / f"financing_gameplay_{i//6+1}.png", pictures[i:i+6])
        sheets.append(dict(path=path, sha256=sha))
    base.save(LIVE, dict(candidate_sha256=candidate, report_sha256=reports, observations=observations,
        observed_speech_pages=len(observations), original_menu_choices=menu_observations, return_frame=exit_frame,
        sheets=sheets, initialized_excerpts=True, natural_story_triggers_claimed=False, hardware=False))
    print("Verified 21 native dialogue and modal holds, both selection highlights, and both original responses.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("fixtures", *RUNS, "verify"))
    action = cli.parse_args().action
    if action == "fixtures":
        for kind in ("speech", "choice"):
            exact_fixture(kind)
    elif action == "verify":
        verify()
    else:
        play(action)
