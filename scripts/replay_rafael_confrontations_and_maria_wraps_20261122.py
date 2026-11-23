"""Verify the new Maria phrase breaks and representative Rafael turns in initialized scenes."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import replay_camille_and_maria_reveals_20261122 as maria_template
from scripts import replay_rafael_diplomacy_and_friends_20261122 as rafael_template
from scripts import stage_rafael_confrontations_and_maria_wraps_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RAFAEL_ROOT = ROOT / "rafael"
ROM = RAFAEL_ROOT / "Rafael_Confrontations_FOCUSED_ONLY.nds"
REPORT = RAFAEL_ROOT / "capture/capture_report.json"
RAFAEL_LIVE = RAFAEL_ROOT / "verified_gameplay.json"
SEQUENCE = ((69, 22), (69, 26), (69, 154), (69, 166), (75, 123), (75, 137),
            (75, 202), (82, 125), (82, 140), (82, 172))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
rafael_scope = rafael_template.scope | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE)
rafael_source = checked_text(rafael_template.source, {
    'for group in proof["groups"]}': 'for group in proof["groups"] if group["file_path"] == "/data/SC0.DK4"}',
    'groups[64]["commands"][-1]': 'groups[82]["commands"][-1]',
    'Rafael_Diplomacy_And_Friends_FOCUSED_ONLY.nds': ROM.name,
})
exec(compile(rafael_source, __file__ + "::Rafael-cold-boot", "exec"), rafael_scope)
rafael_verify = FunctionType(rafael_template.verify.__code__,
    rafael_template.verify.__globals__ | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE))


MARIA_ROOT = ROOT / "maria"
MARIA_ROM = MARIA_ROOT / "Maria_Confrontation_Wraps_FOCUSED_ONLY.nds"
MARIA_LIVE = MARIA_ROOT / "verified_gameplay.json"
MARIA_REPORT = MARIA_ROOT / "after/capture_report.json"
MARIA_SAMPLE = tuple((36, i) for i in (31, 34, 37, 41, 45, 49, 52, 56))
maria_scope = maria_template.maria_scope | dict(
    stage=SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, parent=stage.parent,
                          review=SimpleNamespace(ARCHIVE="/data/SC3.DK4")),
    display=SimpleNamespace(PROOF=stage.NATIVE, display=stage.established.display),
    ROOT=MARIA_ROOT, ROM=MARIA_ROM, SETUP=MARIA_ROOT / "fixture_receipt.json",
    INPUTS=MARIA_ROOT / "inputs.json", LIVE=MARIA_LIVE, REPORT=MARIA_REPORT,
    PLAY_ORDER=tuple(f"DK4_MES_B{b}_R{i:04d}" for b, i in MARIA_SAMPLE),
)
for name in ("prepare", "capture"):
    fn = maria_template.maria_scope[name]
    maria_scope[name] = FunctionType(fn.__code__, maria_scope)
maria_verify = checked_text(maria_template.maria_verify, {
    'observations[:5]],\n                          "Aziza": [row["frame"] for row in observations[5:8]],\n                          "New World map": [row["frame"] for row in observations[8:]]':
        'observations]',
})
exec(compile(maria_verify, __file__ + "::Maria-body-masks", "exec"), maria_scope)


def combine():
    rafael, maria = map(base.load, (RAFAEL_LIVE, MARIA_LIVE))
    assert not LIVE.exists()
    assert rafael["candidate_sha256"] == maria["candidate_sha256"] == base.digest(stage.ROM)
    assert rafael["initialized_excerpts"] and maria["initialized_excerpts"]
    assert not rafael["natural_story_triggers_claimed"] and not maria["natural_story_triggers_claimed"]
    from PIL import Image
    from scripts import verify_story_literal_names_20261122 as visual

    path = "/data/SC3.DK4"
    named = {r["id"]: r["speaker"] for r in base.load(stage.review.REVIEW)["records"] if r["file_path"] == path}
    checked = {r["id"]: r for r in base.load(stage.NATIVE)["records"] if r["file_path"] == path}
    font = visual.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(native.ARM))
    observations = [r | {"file_path": "/data/SC0.DK4"} for r in rafael["observations"]]
    for row in maria["observations"]:
        ident = row["id"]
        hold = row["capture"]
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        with Image.open(hold["path"]) as image:
            visual.glyphs(font, image.convert("RGB"), named[ident], (16, 277), visual.LABEL_COLOR, 226)
        observations.append(row | dict(file_path=path, changed=bool(checked[ident]["layouts"]), speaker=named[ident]))
    assert len(observations) == len(SEQUENCE) + len(MARIA_SAMPLE)
    base.save(LIVE, dict(candidate_sha256=rafael["candidate_sha256"], initialized_excerpts=True,
        natural_story_triggers_claimed=False, observed_speech_pages=len(observations), observations=observations,
        sheets=rafael["sheets"] + maria["sheets"], rafael_report_sha256=rafael["report_sha256"],
        maria_report_sha256=maria["report_sha256"], rafael_return=rafael["return_frame"],
        maria_returns=list(maria["return_frames"].values()), hardware=False))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("rafael_replay", "rafael_verify", "maria_prepare", "maria_capture", "maria_verify", "combine"))
    action = cli.parse_args().action
    if action == "rafael_replay":
        rafael_scope["replay"]()
    elif action == "rafael_verify":
        rafael_verify()
    elif action == "combine":
        combine()
    else:
        if action == "maria_prepare":
            ROOT.mkdir(exist_ok=True)
        maria_scope[action.removeprefix("maria_")]()
