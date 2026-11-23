"""Replay the three repaired Hodram wraps with their preceding and following speech."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B311_B324_20261122 as prior
from scripts import stage_maria_opening_hodram_wraps_20261122 as source
from scripts import verify_maria_opening_hodram_wraps_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = SimpleNamespace(ROM=source.ROM, PROOF=source.PROOF, logical_end=prior.writer.logical_end)
stage = SimpleNamespace(ROM=source.ROM, PROOF=source.PROOF, OUTPUT=source.MANUSCRIPT, ROOT=source.ROOT,
                        review=SimpleNamespace(TOKEN=source.review.hodram.writer.TOKEN))
ROOT=source.ROOT/"hodram_gameplay"
REPORT,PROOF=ROOT/"capture/capture_report.json",ROOT/"verified_gameplay.json"
SELECTED=((312,6),(312,10),(312,13),(312,16),(318,94),(318,109),(318,114),(318,117),(318,125),
          (324,133),(324,144),(324,148))
PAGE_TURN=("DK4_MES_B312_R0010","DK4_MES_B312_R0013")
SERA_NAME=("DK4_MES_B324_R0144","DK4_MES_B324_R0148")
test_name=["DK4_MES_B318_R0109","DK4_MES_B318_R0114","DK4_MES_B318_R0117"]
MENUS=STYLE_OBJECTS=()
producer=checked_text(prior.producer, {'"Hodram_B311_B324_FOCUSED_ONLY.nds"':'"Hodram_Wraps_FOCUSED_ONLY.nds"'})
check=checked_text(prior.check,{
    'for m in native_report["menus"]':'for m in native_report.get("menus",[])',
    'native_report["default_names"][m[0]]':'native_report["default_names"]["1"][m[0]]',
    'assert native.digest(plane) == expected["page_sha256"][page - 1]':
        'assert plane.hex() == expected["pages"][page - 1]["native_plane_hex"]',
    '["layouts"][0]["page_sha256"]':'["layouts"][0]["pages"]',
    '{"DK4_MES_B294_R0058", "DK4_MES_B301_R0021", "DK4_MES_B313_R0228", "DK4_MES_B318_R0109", "DK4_MES_B324_R0058"}':
        '{"DK4_MES_B312_R0010", "DK4_MES_B318_R0125", "DK4_MES_B324_R0144"}',
    "hodram_B311_B324_gameplay_":"hodram_wraps_gameplay_",
    'if r["id"] not in observed]))':'if r["route"]==1 and r["id"] not in observed]))',
})
scope=prior.scope|globals()
for program in (producer,check):
    exec(compile(program,__file__+"::Hodram-wrap-transitions","exec"),scope)


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("replay","check"))
    scope[parser.parse_args().action]()

