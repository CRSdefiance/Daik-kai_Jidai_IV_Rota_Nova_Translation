"""Replay the repaired opening turns and representative Maria B21–32 exchanges."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import replay_maria_B18_B20_20261122 as prior
from scripts import stage_maria_B21_B32_20261122 as writer
from scripts import verify_maria_B21_B32_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage=SimpleNamespace(ROM=writer.ROM,PROOF=writer.PROOF,parent=writer.parent,
                      review=SimpleNamespace(ARCHIVE=writer.review.ARCHIVE))
ROOT=writer.ROOT/"focused_gameplay"
ROM=ROOT/"Maria_B21_B32_FOCUSED_ONLY.nds"
SETUP,INPUTS=ROOT/"fixture_receipt.json",ROOT/"inputs.json"
LIVE,REPORT=ROOT/"verified_gameplay.json",ROOT/"after/capture_report.json"
SELECTED=(
    (0,8),(0,12),(14,5),(14,9),(14,12),(17,34),
    (27,23),(27,34),(27,44),
    (29,88),(29,91),(29,94),(29,97),(29,100),(29,103),(29,115),(29,119),
    (30,20),(30,27),
    (31,8),(31,11),(31,15),(31,18),(31,21),(31,42),(31,49),(31,52),(31,56),
)
PLAY_ORDER=tuple(f"DK4_MES_B{block}_R{index:04d}" for block,index in SELECTED)
FRAME_COUNT=14701
RETURN_FRAMES=(3900,14250,14500)
scope=vars(prior)|globals()
for function,changes in (
    (prior.prepare,{'range(4200,8101,325)':'range(4200,13951,325)'}),
    (prior.capture,{"'range(4450, 8301, 125)'":"'range(4450, 14226, 125)'"}),
    (prior.verify,{
        "4450 <= frame <= 8300":"4450 <= frame <= 14225",
        'page_transitions={"mutiny": [row["frame"] for row in observations[:2]],\n                          "Aziza\'s father": [row["frame"] for row in observations[2:]]}':
            'page_transitions={"Maria and Lil": [row["frame"] for row in observations[9:17]],\n                          "Kuhn impostor fleet": [row["frame"] for row in observations[19:]]}',
        "maria_B18_B20_gameplay_":"maria_B21_B32_gameplay_",
    }),
):
    source=checked_text(getsource(function),changes)
    exec(compile(source,__file__+"::initialized-Maria-alliances","exec"),scope)


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","capture","verify"))
    scope[parser.parse_args().action]()

