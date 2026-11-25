"""Replay the installed Aziza turns using the original initialized dialogue consumer."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_mosque_elysion_mikhail_20261122 as prior
from scripts import stage_aziza_shamshir_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "Aziza_Shamshir_FOCUSED_ONLY.nds"
REPORT = ROOT / "capture/capture_report.json"
LIVE = ROOT / "verified_gameplay.json"
SEQUENCE = tuple((26, i) for i in (41, 45, 60, 111, 192, 217, 228, 235, 271, 287, 310))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
scope = prior.rafael_scope | globals() | dict(prior=prior.rafael_scope["prior"])
source = checked_text(prior.rafael_source, {
    'groups[123]["commands"][-1]': 'groups[26]["commands"][-1]',
    prior.ROM.name: ROM.name,
})
exec(compile(source, __file__ + "::original-Rafael-host", "exec"), scope)
verify = FunctionType(prior.rafael_verify.__code__, prior.rafael_verify.__globals__ | globals())


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("capture", choices=("replay", "verify"))
    if parser.parse_args().capture == "replay":
        scope["replay"]()
    else:
        verify()
