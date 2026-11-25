"""Exercise the revised story commands in the existing initialized Rafael replay."""

from argparse import ArgumentParser
from hashlib import sha256
from inspect import getsource

from PIL import Image

from scripts import replay_rafael_pereira_village_20261121 as earlier
from scripts import stage_rafael_diplomacy_and_friends_20261122 as stage
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as screenshot
from scripts import verify_story_literal_names_20261122 as visual
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "Rafael_Diplomacy_And_Friends_FOCUSED_ONLY.nds"
REPORT = ROOT / "capture/capture_report.json"
LIVE = ROOT / "verified_gameplay.json"
SEQUENCE = ((60, 201), (60, 205), (60, 208),
            (63, 22), (63, 25), (63, 30), (63, 34),
            (64, 352), (64, 355), (64, 358))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
source = checked_text(earlier.source, {"Rafael_Pereira_Village_RESEARCH_ONLY.nds": ROM.name})
scope = earlier.scope | globals()
exec(compile(source, __file__ + "::original-Rafael-scene-host", "exec"), scope)


def verify():
    assert not LIVE.exists()
    fixture_path = ROOT / "fixture.json"
    report, fixture, stored, native_proof = map(base.load, (REPORT, fixture_path, stage.PROOF, stage.NATIVE))
    candidate = base.digest(stage.ROM)
    assert fixture["candidate_sha256"] == stored["candidate_sha256"] == native_proof["candidate_sha256"] == candidate
    assert report["ROM_sha256"] == base.digest(ROM) == fixture["fixture_ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded")
    assert fixture["exact_candidate_inverse"] and not fixture["natural_activation"]
    assert fixture["original_speech_commands_copied_byte_exact"] and fixture["original_scene_branches_unexecuted"]
    assert report["scripted_input_schedule"] == base.load(ROOT / "inputs.json")
    rows = {r["id"]: r for r in native_proof["records"]}
    named = {r["id"]: r["speaker"] for r in base.load(stage.review.REVIEW)["records"]}
    holds = {r["frame"]: r for r in report["frames_captured"]}
    paint = stage.established.display
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    renderer = paint.clipped_renderer(ctx)
    game_font = visual.GameAsciiFont.from_arm9(ctx.arm)
    pages, pictures = [], []
    for (block, ordinal), command, frame in zip(SEQUENCE, fixture["copied"], FRAMES[:-1], strict=True):
        ident = f"DK4_MES_B{block}_R{ordinal:04d}"
        assert command["ids"] == [ident]
        row = rows[ident]
        assert command["hex"] == row["exact_command_hex"]
        if row["layouts"]:
            page, = row["layouts"][0]["pages"]
        else:
            body = bytes.fromhex(row["body_hex"])[1:]
            assert all(token not in body for token in (b"FI", b"FA", b"FO", b"FU"))
            render = renderer(ctx.arm, font, body)
            assert render["complete_consumed_bytes"] == len(body)
            page, = render["pages"]
        plane = bytes.fromhex(page["native_plane_hex"])
        hold = holds[frame]
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        with Image.open(hold["path"]) as opened:
            image = opened.convert("RGB")
        assert screenshot.mask_check(plane, 216, image), (ident, frame)
        speaker = named[ident]
        visual.glyphs(game_font, image, speaker, (16, 277), visual.LABEL_COLOR, 226)
        pages.append(dict(id=ident, candidate_body_hex=row["body_hex"], capture=hold, speaker=speaker,
                          plane_sha256=sha256(plane).hexdigest(), changed=bool(row["layouts"])))
        pictures.append((f"{ident} / {speaker}", image))
    assert len(pages) == len(SEQUENCE)
    closing = holds[FRAMES[-1]]
    assert base.digest(closing["path"]) == closing["PNG_sha256"]
    with Image.open(closing["path"]) as opened:
        pictures.append(("Return to normal scene handling", opened.convert("RGB")))
    sheets = []
    for start in range(0, len(pictures), 6):
        path, digest = visual.make_sheet(ROOT / f"rafael_story_gameplay_{start // 6 + 1}.png", pictures[start:start+6])
        sheets.append(dict(path=path, sha256=digest))
    base.save(LIVE, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_story_triggers_claimed=False,
        observed_speech_pages=len(pages), observations=pages, return_frame=closing, sheets=sheets,
        report_sha256=base.digest(REPORT), fixture_sha256=base.digest(fixture_path), hardware=False))
    print(f"Verified {len(pages)} exact body masks and speaker labels in the focused Rafael replay.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    if cli.parse_args().action == "replay":
        scope["replay"]()
    else:
        verify()
