"""Replay Rafael's revised panels and original name substitutions."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_athens_and_maria_crew_20261122 as prior
from scripts import stage_rafael_charlotte_and_maria_20261122 as stage
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts.source_locked_derivation_v5118 import checked_text


base, native, gameplay = stage.base, stage.native, prior.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
SAMPLE = {0: ((67, 143), (67, 148), (67, 165), (67, 202), (67, 245),
    (70, 18), (70, 50), (70, 87), (70, 174), (70, 178), (70, 190), (70, 193), (70, 214),
    (71, 39), (71, 63), (72, 62), (72, 67))}
RUNTIME_VALUES = {
    "DK4_MES_B67_R0148": {"FI": "Rafael"},
    "DK4_MES_B70_R0050": {"FI": "Rafael", "FA": "Castor"},
}
RUNS = ("0",)
scope = vars(prior) | globals()
for name in ("receipt", "report_path", "run_file", "play"):
    inherited = getattr(prior, name)
    scope[name] = FunctionType(inherited.__code__, scope)
fixture_source = checked_text(getsource(prior.fixture), {
    "Athens_And_Crew_FOCUSED_ONLY.nds": "Rafael_Charlotte_And_Maria_FOCUSED_ONLY.nds",
})
exec(compile(fixture_source, __file__ + "::focused-fixture", "exec"), scope)


def report(run):
    return scope["report_path"](int(run))


def formatting():
    FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()


def verify():
    proof, display, manuscript = map(base.load, (stage.PROOF, stage.NATIVE, stage.REVIEW))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] == display["candidate_sha256"]
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    renderer = stage.established.display.clipped_renderer(ctx)
    names = gameplay.GameAsciiFont.from_arm9(ctx.arm)
    fixture, data = map(base.load, (scope["receipt"](0), report("0")))
    assert fixture["candidate_sha256"] == candidate and fixture["exact_inverse"] and not fixture["natural_activation"]
    assert data["ROM_sha256"] == fixture["rom_sha256"] == base.digest(fixture["rom"])
    assert data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
    assert not data.get("battery_save_preloaded")
    assert data["scripted_input_schedule"] == base.load(scope["run_file"](0, "inputs"))
    holds = base.load(scope["run_file"](0, "holds"))
    by_id = {r["id"]: r for r in display["records"]}
    labels = {r["id"]: r["speaker"] for r in manuscript["records"]}
    pictures, observations = [], []
    for frame, command in zip(holds[:-1], fixture["commands"], strict=True):
        ident = command["id"]
        row = by_id[ident]
        assert command["exact_command_hex"] == row["exact_command_hex"]
        values = RUNTIME_VALUES.get(ident, {})
        if row["layouts"]:
            assert not values
            page, = row["layouts"][0]["pages"]
        else:
            body = bytes.fromhex(row["body_hex"])[1:]
            assert {token for token in ("FO", "FI", "FA", "FU") if token.encode() in body} == values.keys()
            for token, value in values.items():
                body = body.replace(token.encode("ascii"), value.encode("ascii"))
            rendered = renderer(ctx.arm, font, body)
            assert rendered["complete_consumed_bytes"] == len(body)
            page, = rendered["pages"]
        hold, image = gameplay.screen(data, frame)
        assert gameplay.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, image), (ident, frame)
        speaker = labels[ident]
        gameplay.glyphs(names, image, speaker, (16, 277), gameplay.LABEL_COLOR, 226)
        observations.append(dict(file_path=row["file_path"], id=ident, page=1, capture=hold, speaker=speaker,
            exact_complete_body_mask=True, default_substitutions=values, stored_offset=command["offset"]))
        pictures.append((f"{ident} / {speaker}", image))
    assert len(observations) == len(SAMPLE[0])
    assert {r["id"] for r in by_id.values() if r["layouts"]} <= {r["id"] for r in observations}
    exit_hold, image = gameplay.screen(data, holds[-1])
    pictures.append(("Rafael / host return to port", image))
    sheets = []
    for offset in range(0, len(pictures), 6):
        path, digest = gameplay.make_sheet(ROOT / f"rafael_charlotte_and_maria_gameplay_{1+offset//6}.png", pictures[offset:offset+6])
        sheets.append(dict(path=path, sha256=digest))
    base.save(LIVE, dict(candidate_sha256=candidate, observed_speech_pages=len(observations),
        observations=observations, report_sha256={"0": base.digest(report("0"))},
        return_frames={"0": exit_hold}, sheets=sheets, initialized_excerpts=True,
        natural_story_triggers_claimed=False, hardware=False))
    print(f"Verified {len(observations)} focused speech holds, default name substitutions, and the host exit.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "formatting", "verify"))
    action = cli.parse_args().action
    if action == "replay":
        scope["fixture"](0)
        scope["play"](0)
    else:
        globals()[action]()
