"""Stage and verify the captured-ship reply on Maria's ordinary Nagasaki route."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_maria_captured_ship_20261124 as review
from scripts import stage_tunis_palace_refusal_20261124 as palace
from scripts import stage_tunis_shop_advice_20261124 as shared
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read, reference, write


trend, panels, KEY, END = review.trend, review.panels, review.KEY, review.END
played = SimpleNamespace(ROOT=review.played.ROOT, RELEASE=review.played.prior.RELEASE, replay=review.played.prior.replay)
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_maria_captured_ship")
ROM, STORED = ROOT / "Maria_Captured_Ship_STAGED.nds", ROOT / "stored_proof.json"
BEFORE, AFTER = played.ROOT / "capture/capture_report.json", ROOT / "replay/capture/capture_report.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PAIRED, SHEET = ROOT / "paired_gameplay.json", ROOT / "paired_maria_captured_ship_1_20261123.png"


def scope():
    return vars(shared) | vars(palace) | globals()


def stage():
    assert ROOT.parent.exists()
    source = checked_text(getsource(shared.stage), {"== 124": '== len(proof["native_cases"]) == 30'})
    bindings = scope()
    exec(compile(source, __file__ + "::source-locked-COMMON-stage", "exec"), bindings)
    bindings["stage"]()


def verify(stored):
    source = checked_text(getsource(palace.verify), {
        'row["label"] == "Proposed"': 'row["label"] == "Proposed" and row["name"] == "War Ironclad"',
        "review.REVISED_HOLDS": "(review.RESULT_FRAME,)",
        'panels.nameplate(font, "Guard", b)': 'panels.nameplate(font, "Sailor", b)',
        'panels.nameplate(font, "Guard", a)': 'panels.nameplate(font, "Sailor", a)',
        "len(changed) == 2 and {8600, 9400, 14600, 15400, 15800, END}": "len(changed) == 1 and {10400, 17100, 19100, 19500, 19900, END}",
        "paired_tunis_palace_refusal": "paired_maria_captured_ship",
        "both revised Guard holds": "the revised captured-ship hold",
    })
    bindings = scope()
    exec(compile(source, __file__ + "::paired-captured-ship", "exec"), bindings)
    bindings["verify"](stored)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action == "verify":
        verify(read(STORED))
    else:
        function = shared.replay if action == "replay" else shared.release_check
        arguments = [read(STORED)] if action == "replay" else [read(STORED), action]
        FunctionType(function.__code__, scope())(*arguments)
