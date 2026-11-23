"""Replay selected stored speech commands after Rafael's original initialization."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_pereira_village_20261121 as precedent
from scripts import stage_rafael_east_asia_followup_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
prior = precedent.prior
ROOT = stage.ROOT / "focused_gameplay"
REPORT = ROOT / "capture/capture_report.json"
FOCUS = stage.ROOT / "company_replay"
FOCUS_REPORT = FOCUS / "capture/capture_report.json"
FOCUS_SEQUENCE = ((75, 132), (75, 198), (78, 5), (78, 9))
FINAL_SEQUENCE = ((73, 36), (74, 5), (75, 198), (79, 5))
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
SEQUENCE = (
    (71, 27), (71, 30), (71, 34),
    (72, 77), (72, 81), (72, 86), (72, 90), (72, 94),
    (73, 52), (73, 56), (73, 60), (73, 65), (73, 69),
    (74, 5),
    (75, 6), (75, 10), (75, 15), (75, 19), (75, 23), (75, 27), (75, 238),
    (76, 12), (77, 13), (78, 24), (78, 29), (79, 5), (80, 13),
)
INPUT = [(4000 + i * 300, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 255 for frame, _ in INPUT[:-1]), END - 1)


source = checked_text(precedent.source, {
    'terminal = groups[64]["commands"][-1]': 'terminal = groups[80]["commands"][-1]',
    '"Rafael_Pereira_Village_RESEARCH_ONLY.nds"': '"Rafael_East_Asia_Showdown_RESEARCH_ONLY.nds"',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::replay", "exec"), scope)


def company_settings(sequence=FOCUS_SEQUENCE):
    inputs = [(4000 + i * 300, "A") for i in range(len(sequence))]
    end = inputs[-1][0] + 720
    frames = (3900, *(frame + 255 for frame, _ in inputs[:-1]), end - 1)
    return dict(ROOT=FOCUS, REPORT=FOCUS_REPORT, SEQUENCE=sequence, INPUT=inputs, END=end, FRAMES=frames)


def replay_shorter_page():
    draft = base.load(stage.OUTPUT)
    plan = draft["plans"]["DK4_MES_B78_R0005"]
    row, = [r for r in draft["records"] if r["id"] == "DK4_MES_B78_R0005"]
    assert plan["expected_native_pages"] == 1 and bytes.fromhex(row["current_hex"]).count(10) >= 4
    replay = scope["replay"]
    FunctionType(replay.__code__, replay.__globals__ | company_settings())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "company", "visual", "startup", "patch"))
    check = parser.parse_args().check
    if check == "replay":
        scope["replay"]()
    elif check == "company":
        replay_shorter_page()
    elif check == "visual":
        replay = scope["replay"]
        FunctionType(replay.__code__, replay.__globals__ | company_settings(FINAL_SEQUENCE))()
    else:
        template = prior.prior.release_checks.template
        action = template.common.startup if check == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
