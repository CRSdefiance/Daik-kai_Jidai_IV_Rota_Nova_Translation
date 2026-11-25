"""Replay the alias reveal and the two prior Maria wrap findings in context."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import replay_lil_lessons_and_maria_scenes_20261122 as template
from scripts import stage_camille_and_maria_reveals_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "route2/Camille_Reveal_FOCUSED_ONLY.nds"
REPORT = ROOT / "route2/capture/capture_report.json"
LIVE = ROOT / "verified_gameplay.json"
SAMPLE = ((65, 140), (65, 144), (65, 153), (65, 198), (65, 207), (65, 249),
          (127, 50), (127, 53), (127, 57), (127, 77), (127, 81), (127, 85))
END = 4100 + len(SAMPLE) * 360
CASES = {2: template.CASES[2] | dict(end=END, sample=SAMPLE)}
replay_lil = template.replay_lil | globals()
replay_lil["LIVE"] = ROOT / "lil_verified.json"
for name in ("replay", "verify"):
    fn = template.replay_lil[name]
    replay_lil[name] = FunctionType(fn.__code__, replay_lil)


MARIA_ROOT = ROOT / "maria"
MARIA_ROM = MARIA_ROOT / "Maria_Reveals_FOCUSED_ONLY.nds"
MARIA_LIVE, MARIA_REPORT = MARIA_ROOT / "verified_gameplay.json", MARIA_ROOT / "after/capture_report.json"
MARIA_SAMPLE = ((36, 34), (36, 37), (36, 41), (36, 45), (36, 49),
                (19, 184), (19, 188), (19, 191), (126, 33), (126, 37))
maria_scope = template.maria_scope | dict(stage=SimpleNamespace(ROM=stage.ROM, PROOF=stage.PROOF, parent=stage.parent,
    review=SimpleNamespace(ARCHIVE="/data/SC3.DK4")), display=SimpleNamespace(PROOF=stage.NATIVE, display=stage.established.display),
    ROOT=MARIA_ROOT, ROM=MARIA_ROM, SETUP=MARIA_ROOT / "fixture_receipt.json", INPUTS=MARIA_ROOT / "inputs.json",
    LIVE=MARIA_LIVE, REPORT=MARIA_REPORT, PLAY_ORDER=tuple(f"DK4_MES_B{b}_R{i:04d}" for b, i in MARIA_SAMPLE))
for name in ("prepare", "capture"):
    fn = template.maria_scope[name]
    maria_scope[name] = FunctionType(fn.__code__, maria_scope)
maria_verify = checked_text(template.maria_verify, {
    'observations[:3]': 'observations[:5]',
    '"Angelo": [observations[3]["frame"]],': '"Aziza": [row["frame"] for row in observations[5:8]],',
    '"Basra": [row["frame"] for row in observations[4:]]': '"New World map": [row["frame"] for row in observations[8:]]',
    'maria_story_and_basra_gameplay_': 'maria_reveals_gameplay_',
})
exec(compile(maria_verify, __file__ + "::Maria-body-masks", "exec"), maria_scope)
combine = template.verify_return_and_combine
verify_return_and_combine = FunctionType(combine.__code__, combine.__globals__ | globals())


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
