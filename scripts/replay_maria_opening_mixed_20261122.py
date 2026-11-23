"""Replay Maria's opening exchanges in the established initialized host."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import replay_maria_B18_B20_20261122 as prior
from scripts import stage_maria_opening_hodram_wraps_20261122 as writer
from scripts import verify_maria_opening_hodram_wraps_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(ROM=writer.ROM, PROOF=writer.PROOF, parent=writer.parent,
                        review=SimpleNamespace(ARCHIVE=writer.review.maria.ARCHIVE))
ROOT = writer.ROOT/"maria_gameplay"
ROM = ROOT/"Maria_Opening_FOCUSED_ONLY.nds"
SETUP, INPUTS = ROOT/"fixture_receipt.json", ROOT/"inputs.json"
LIVE, REPORT = ROOT/"verified_gameplay.json", ROOT/"after/capture_report.json"
SELECTED = (
    (3,26),(3,32),(3,35),(3,39),
    (4,41),(4,45),(4,97),(4,101),(4,105),
    (5,19),(5,25),(5,28),(5,35),
    (12,9),(12,12),(12,16),
    (14,5),(14,9),(14,12),
)
PLAY_ORDER = tuple(f"DK4_MES_B{b}_R{i:04d}" for b,i in SELECTED)
FRAME_COUNT=12051
RETURN_FRAMES=(3900, 11650, 11900)
scope = vars(prior)|globals()
for f, changes in (
    (prior.prepare, {'range(4200,8101,325)':'range(4200,11351,325)'}),
    (prior.capture, {"'range(4450, 8301, 125)'":" 'range(4450, 11526, 125)'"}),
    (prior.verify, {
        "4450 <= frame <= 8300":"4450 <= frame <= 11525",
        'for row in shown["records"]}':'for row in shown["records"] if row["route"]==3}',
        'page_transitions={"mutiny": [row["frame"] for row in observations[:2]],\n                          "Aziza\'s father": [row["frame"] for row in observations[2:]]}':
            'page_transitions={"Kurushima": [row["frame"] for row in observations[:4]],\n                          "Lil": [row["frame"] for row in observations[-3:]]}',
        "maria_B18_B20_gameplay_":"maria_opening_gameplay_",
    }),
):
    validated = checked_text(getsource(f),changes)
    exec(compile(validated,__file__+"::initialized-Maria-opening-excerpts","exec"),scope)


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","capture","verify"))
    scope[parser.parse_args().action]()

