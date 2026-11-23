"""Verify representative tavern and Proof pages with their original speaker labels."""

from argparse import ArgumentParser
from inspect import getsource

from PIL import Image

from scripts import replay_fernando_parallel_routes_20261121 as precedent
from scripts import stage_tavern_and_proof_exchanges_20261122 as stage
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as screen
from scripts import verify_story_literal_names_20261122 as visual
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "route1/Tavern_And_Proof_Exchanges_FOCUSED_ONLY.nds"
REPORT = ROOT / "route1/capture/capture_report.json"
LIVE = ROOT / "verified_gameplay.json"
PATH = "/data/SC1.DK4"
SAMPLE = ((169, 16), (169, 20), (169, 24), (169, 96), (169, 104), (169, 108), (169, 111), (169, 114), (169, 117),
          (170, 184), (170, 188), (173, 135), (173, 138), (173, 141), (174, 117))
END = 4100 + len(SAMPLE) * 360
CASES = {1: dict(opening=42, prefix=42, end=END, input=precedent.CASES[1]["input"], sample=SAMPLE)}
replay_source = checked_text(getsource(precedent.replay), {
    '    group, = [g for g in stored["groups"] if g["route"] == route]\n'
    '    assert group["file_path"] == path and group["block"] == case["block"]':
        '    groups = {g["block"]: g for g in stored["groups"] if g["route"] == route}\n'
        '    assert all(g["file_path"] == path for g in groups.values())',
    '    init, block = (archive.blocks[i] for i in (case["opening"], case["block"]))\n'
    '    assert native.digest(block) == group["after"]':
        '    init = archive.blocks[case["opening"]]\n'
        '    assert all(native.digest(archive.blocks[n]) == g["after"] for n, g in groups.items())',
    '    draft = base.load(stage.review.OUTPUT)\n'
    '    indices = {row["id"]: row["source_record_index"] for row in draft["records"] if row["route"] == route}\n'
    '    selected = {indices[c["record_ids"][0]]: c for c in group["commands"] if c["record_ids"]}':
        '    selected = {ident: c for g in groups.values() for c in g["commands"] for ident in c["record_ids"]}',
    '    for index in case["sample"]:\n        command = selected[index]':
        '    for number, ordinal in case["sample"]:\n'
        '        block = archive.blocks[number]\n'
        '        command = selected[f"DK4_MES_B{number}_R{ordinal:04d}"]',
    'block=case["block"]))': 'block=number))',
    '    end = group["commands"][-1]': '    end = groups[SAMPLE[-1][0]]["commands"][-1]',
    'folder / f"Fernando_SC{route}_RESEARCH_ONLY.nds"': 'ROM',
    'natural_activation=False, source_block=case["block"], original_opening_block=case["opening"]':
        'natural_activation=False, source_blocks=sorted(groups), original_opening_block=case["opening"]',
})
scope = vars(precedent) | globals()
exec(compile(replay_source, __file__ + "::Hodram-initialized-replay", "exec"), scope)


def verify():
    assert not LIVE.exists()
    fixture_path = ROM.with_name("fixture.json")
    report, fixture, staged, native_pages, extra = map(base.load, (
        REPORT, fixture_path, stage.PROOF, stage.NATIVE, stage.CHOICES_AND_PAGES))
    candidate = base.digest(stage.ROM)
    assert candidate == fixture["candidate_sha256"] == staged["candidate_sha256"] == native_pages["candidate_sha256"] == extra["candidate_sha256"]
    assert report["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == END
    assert fixture["exact_candidate_inverse"] and not fixture["natural_activation"]
    assert report["scripted_input_schedule"] == base.load(ROM.with_name("inputs.json"))
    shots = {}
    for hold in report["frames_captured"]:
        if hold["frame"] < 3900 or hold["frame"] > END - 1:
            continue
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        with Image.open(hold["path"]) as opened:
            shots[hold["frame"]] = hold, opened.convert("RGB")
    records = {r["id"]: r for r in native_pages["records"] if r["route"] == 1}
    speakers = {r["id"]: r["speaker"] for r in base.load(stage.review.REVIEW)["records"] if r["route"] == 1}
    display = stage.established.display
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    painter = display.clipped_renderer(ctx)
    name_font = visual.GameAsciiFont.from_arm9(ctx.arm)
    pages, pictures, cursor = [], [], 3800
    for (block, ordinal), copied in zip(SAMPLE, fixture["copied_native_commands"], strict=True):
        ident = f"DK4_MES_B{block}_R{ordinal:04d}"
        row = records[ident]
        assert copied["ids"] == [ident] and copied["command_sha256"] == native.digest(bytes.fromhex(row["exact_command_hex"]))
        if row["layouts"]:
            page, = row["layouts"][0]["pages"]
        else:
            raw = bytes.fromhex(row["body_hex"])[1:]
            assert not any(token in raw for token in (b"FI", b"FA", b"FO", b"FU"))
            result = painter(ctx.arm, font, raw)
            assert result["complete_consumed_bytes"] == len(raw)
            page, = result["pages"]
        plane = bytes.fromhex(page["native_plane_hex"])
        choices = ((frame, hold, img) for frame, (hold, img) in shots.items() if frame > cursor + 140)
        for frame, hold, image in choices:
            if screen.mask_check(plane, 216, image):
                break
        else:
            raise AssertionError((ident, cursor))
        cursor = frame
        speaker = speakers[ident]
        visual.glyphs(name_font, image, speaker, (16, 277), visual.LABEL_COLOR, 226)
        pages.append(dict(id=ident, changed=bool(row["layouts"]), capture=hold, speaker=speaker, plane_sha256=native.digest(plane)))
        pictures.append((f"{ident} / {speaker}", image))
    exit_hold, exit_screen = shots[END-1]
    assert cursor < END - 1
    pictures.append(("Original story host exit", exit_screen))
    sheets = []
    for i in range(0, len(pictures), 6):
        path, sha = visual.make_sheet(ROOT / f"tavern_and_proofs_gameplay_{1 + i // 6}.png", pictures[i:i+6])
        sheets.append(dict(path=path, sha256=sha))
    base.save(LIVE, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_story_triggers_claimed=False,
        observed_speech_pages=len(pages), observations=pages, return_frame=exit_hold, sheets=sheets,
        report_sha256=base.digest(REPORT), fixture_sha256=base.digest(fixture_path), hardware=False))
    print(f"Verified {len(pages)} body masks and speaker labels in the focused Hodram replay.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    if cli.parse_args().action == "replay":
        scope["replay"](1)
    else:
        verify()
