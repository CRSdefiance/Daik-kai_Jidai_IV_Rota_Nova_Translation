"""Verify Lil's refit lesson and Maria's Basra exchange in original scene hosts."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from types import FunctionType, SimpleNamespace

from PIL import Image

from scripts import replay_current_story_wraps_20261122 as maria
from scripts import replay_tavern_and_proof_exchanges_20261122 as templates
from scripts import replay_fernando_parallel_routes_20261121 as cold
from scripts import stage_lil_lessons_and_maria_scenes_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "route2/Lil_Lessons_FOCUSED_ONLY.nds"
REPORT = ROOT / "route2/capture/capture_report.json"
LIVE = ROOT / "verified_gameplay.json"
SAMPLE = ((164, 5), (164, 25), (166, 5), (166, 20), (166, 52), (166, 68), (166, 106),
          (166, 109), (166, 112), (166, 169), (167, 68), (167, 71), (167, 88), (169, 156), (169, 160))
END = 4100 + len(SAMPLE) * 360
CASES = {2: dict(opening=22, prefix=56, end=END, input=cold.CASES[2]["input"], sample=SAMPLE)}
replay_lil = templates.scope | globals()
replay_lil["LIVE"] = ROOT / "lil_verified.json"
exec(compile(templates.replay_source, __file__ + "::Lil-original-opening-host", "exec"), replay_lil)
verify_source = checked_text(getsource(templates.verify), {
    'report, fixture, staged, native_pages, extra = map(base.load, (\n        REPORT, fixture_path, stage.PROOF, stage.NATIVE, stage.CHOICES_AND_PAGES))':
        'report, fixture, staged, native_pages = map(base.load, (REPORT, fixture_path, stage.PROOF, stage.NATIVE))',
    ' == extra["candidate_sha256"]': '',
    'if r["route"] == 1': 'if r["route"] == 2',
    'tavern_and_proofs_gameplay_': 'lil_ship_lessons_gameplay_',
    'focused Hodram replay': 'focused Lil replay',
})
exec(compile(verify_source, __file__ + "::Lil-body-and-labels", "exec"), replay_lil)


MARIA_ROOT = ROOT / "maria"
MARIA_ROM = MARIA_ROOT / "Maria_Basra_FOCUSED_ONLY.nds"
MARIA_LIVE, MARIA_REPORT = MARIA_ROOT / "verified_gameplay.json", MARIA_ROOT / "after/capture_report.json"
MARIA_SAMPLE = ((36, 37), (36, 41), (36, 45), (129, 16),
                (156, 72), (156, 75), (156, 79), (156, 82), (156, 86), (156, 90))
maria_scope = maria.scope | dict(stage=SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, parent=stage.parent,
    review=SimpleNamespace(ARCHIVE="/data/SC3.DK4")), display=SimpleNamespace(PROOF=stage.NATIVE, display=stage.established.display),
    ROOT=MARIA_ROOT, ROM=MARIA_ROM, SETUP=MARIA_ROOT / "fixture_receipt.json", INPUTS=MARIA_ROOT / "inputs.json",
    LIVE=MARIA_LIVE, REPORT=MARIA_REPORT, PLAY_ORDER=tuple(f"DK4_MES_B{b}_R{i:04d}" for b, i in MARIA_SAMPLE))
maria_scope["prepare"] = FunctionType(maria.scope["prepare"].__code__, maria_scope)
maria_scope["capture"] = FunctionType(maria.prior.capture.__code__, maria_scope)
maria_verify = checked_text(getsource(maria.prior.verify), {
    'for row in shown["records"]}': 'for row in shown["records"] if row["file_path"] == ARCHIVE}',
    'layout, = [entry for entry in record["layouts"] if entry["scope"] == "registered default"]': 'layout = record["layouts"][0]',
    '"mutiny": [row["frame"] for row in observations[:2]],': '"Maria and Lil": [row["frame"] for row in observations[:3]],',
    '"Aziza\'s father": [row["frame"] for row in observations[2:]]':
        '"Angelo": [observations[3]["frame"]],\n                          "Basra": [row["frame"] for row in observations[4:]]',
    'maria_B18_B20_gameplay_': 'maria_story_and_basra_gameplay_',
})
exec(compile(maria_verify, __file__ + "::Maria-body-masks", "exec"), maria_scope)


def verify_return_and_combine():
    assert not LIVE.exists()
    lil, m = map(base.load, (replay_lil["LIVE"], MARIA_LIVE))
    assert lil["candidate_sha256"] == m["candidate_sha256"] == base.digest(stage.ROM)
    assert lil["initialized_excerpts"] and m["initialized_excerpts"]
    assert not lil["natural_story_triggers_claimed"] and not m["natural_story_triggers_claimed"]
    path = "/data/SC3.DK4"
    named = {r["id"]: r["speaker"] for r in base.load(stage.review.REVIEW)["records"] if r["file_path"] == path}
    rows = {r["id"]: r for r in base.load(stage.NATIVE)["records"] if r["file_path"] == path}
    view = templates.visual
    font = view.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(native.ARM))
    maria_rows = []
    for row in m["observations"]:
        ident = row["id"]
        hold = row["capture"]
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        with Image.open(hold["path"]) as image:
            view.glyphs(font, image.convert("RGB"), named[ident], (16, 277), view.LABEL_COLOR, 226)
        maria_rows.append(row | dict(file_path=path, changed=bool(rows[ident]["layouts"]), speaker=named[ident]))
    observations = [r | {"file_path": "/data/SC2.DK4"} for r in lil["observations"]] + maria_rows
    assert len(observations) == len(SAMPLE) + len(MARIA_SAMPLE)
    base.save(LIVE, dict(candidate_sha256=lil["candidate_sha256"], initialized_excerpts=True, natural_story_triggers_claimed=False,
        observed_speech_pages=len(observations), observations=observations, sheets=lil["sheets"] + m["sheets"],
        lil_report_sha256=lil["report_sha256"], maria_report_sha256=m["report_sha256"],
        lil_return=lil["return_frame"], maria_returns=list(m["return_frames"].values()),
        lil_and_maria_panel_counts=dict(Counter(r["file_path"] for r in observations)), hardware=False))
    print(f"Verified {len(observations)} focused pages and labels across Lil's and Maria's routes.", flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("lil_replay", "lil_verify", "maria_prepare", "maria_capture", "maria_verify", "combine"))
    action = cli.parse_args().action
    if action == "lil_replay":
        replay_lil["replay"](2)
    elif action == "lil_verify":
        replay_lil["verify"]()
    elif action == "combine":
        verify_return_and_combine()
    else:
        if action == "maria_prepare":
            ROOT.mkdir(exist_ok=True)
        maria_scope[action.removeprefix("maria_")]()
