"""Replay representative changed commands through the initialized original Maria scene host."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_maria_B18_B20_20261122 as prior
from scripts import stage_current_story_wraps_20261122 as writer
from scripts.source_locked_derivation_v5118 import checked_text


ARCHIVE = "/data/SC3.DK4"
stage = SimpleNamespace(ROM=writer.ROM, PROOF=writer.PROOF, parent=writer.parent,
                        review=SimpleNamespace(ARCHIVE=ARCHIVE))
display = SimpleNamespace(PROOF=writer.NATIVE, display=writer.display)
ROOT = writer.ROOT / "focused_gameplay"
ROM = ROOT / "Early_Story_Wraps_Maria_FOCUSED_ONLY.nds"
SETUP, INPUTS = ROOT / "fixture_receipt.json", ROOT / "inputs.json"
LIVE, REPORT = ROOT / "verified_gameplay.json", ROOT / "after/capture_report.json"
PLAY_ORDER = tuple(f"DK4_MES_B{block}_R{ordinal:04d}" for block, ordinal in (
    (135, 325), (135, 328), (135, 332), (18, 64), (31, 42), (31, 71)))
FRAME_COUNT = 8851
RETURN_FRAMES = (3900, 8400, 8600)


scope = vars(prior) | globals()
for function, replacements in (
    (prior.prepare, {
        'for g in proof["groups"] for cmd':
            'for g in proof["groups"] if g["file_path"] == ARCHIVE for cmd',
    }),
    (prior.verify, {
        'for row in shown["records"]}':
            'for row in shown["records"] if row["file_path"] == ARCHIVE}',
        'layout, = [entry for entry in record["layouts"] if entry["scope"] == "registered default"]':
            'layout = record["layouts"][0]',
        '"mutiny": [row["frame"] for row in observations[:2]],':
            '"ship-buying lesson": [row["frame"] for row in observations[:3]],',
        '"Aziza\'s father": [row["frame"] for row in observations[2:]]':
            '"battle and retreat excerpts": [row["frame"] for row in observations[3:]]',
        'maria_B18_B20_gameplay_': 'early_story_wraps_gameplay_',
    }),
):
    source = checked_text(getsource(function), replacements)
    exec(compile(source, __file__ + "::initialized-history", "exec"), scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "verify"))
    action = cli.parse_args().action
    if action == "capture":
        FunctionType(prior.capture.__code__, scope)()
    else:
        scope[action]()
