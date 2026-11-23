"""Cold-boot focused Maria excerpts using the staged commands and original host exit."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import replay_maria_B18_B20_20261122 as prior
from scripts import stage_maria_tutorial_followup_20261122 as writer
from scripts import verify_maria_tutorial_followup_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage=SimpleNamespace(ROM=writer.ROM,PROOF=writer.PROOF,parent=writer.parent,review=SimpleNamespace(ARCHIVE=writer.ARCHIVE))
ROOT=writer.ROOT/"focused_gameplay"
ROM=ROOT/"Maria_Tutorial_Followup_FOCUSED_ONLY.nds"
SETUP,INPUTS=ROOT/"fixture_receipt.json",ROOT/"inputs.json"
LIVE,REPORT=ROOT/"verified_gameplay.json",ROOT/"after/capture_report.json"
SELECTED=((135,325),(135,328),(135,332),(135,335),(135,348),(136,139),(136,143),(136,146),(138,113),(138,116),(138,119),(138,125))
PLAY_ORDER=tuple(f"DK4_MES_B{block}_R{index:04d}" for block,index in SELECTED)
FRAME_COUNT=9301
RETURN_FRAMES=(3900,8850,9100)
scope=vars(prior)|globals()
for function,changes in (
    (prior.prepare,{'range(4200,8101,325)':'range(4200,8701,325)'}),
    (prior.capture,{"'range(4450, 8301, 125)'":"'range(4450, 8826, 125)'"}),
    (prior.verify,{
        "4450 <= frame <= 8300":"4450 <= frame <= 8825",
        'page_transitions={"mutiny": [row["frame"] for row in observations[:2]],\n'
        '                          "Aziza\'s father": [row["frame"] for row in observations[2:]]}':
            'page_transitions={"Cesare advice": [row["frame"] for row in observations[:5]],\n'
            '                          "Fernando": [row["frame"] for row in observations[5:8]],\n'
            '                          "Manuel advice and decline": [row["frame"] for row in observations[8:]]}',
        "maria_B18_B20_gameplay_":"maria_tutorial_followup_gameplay_",
    }),
):
    source=checked_text(getsource(function),changes)
    exec(compile(source,__file__+"::initialized-Maria-followup","exec"),scope)

if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","capture","verify"))
    scope[parser.parse_args().action]()

