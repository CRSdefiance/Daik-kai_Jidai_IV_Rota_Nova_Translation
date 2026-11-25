"""Replay the lesson, recruitment, Proofs and pirate transitions."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B151_B160_20261122 as previous
from scripts import verify_hodram_B171_B180_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (171,5),(171,"154"),(171,68),(171,105),(171,109),
    (172,20),(172,59),(172,74),(172,78),(172,98),(172,122),(172,126),(172,129),
    (172,228),(172,233),(172,244),(172,254),(172,329),(172,333),(172,336),(172,339),
    (173,44),(173,51),(173,58),(173,117),(173,121),(173,135),(173,138),(173,141),
    (174,46),(174,68),(174,72),(174,93),(174,117),(174,138),
    (175,18),(175,29),(175,56),(175,62),(175,97),(175,109),(175,128),
    (176,15),(176,56),(176,59),(176,73),(177,24),(177,39),
    (178,42),(178,63),(178,74),(178,90),
    (179,10),(179,17),(179,39),(179,47),(179,65),(179,68),(179,72),(179,80),(179,99),
    (180,27),(180,35),(180,38),
)
test_name = ["DK4_MES_B172_R0122", "DK4_MES_B172_R0126", "DK4_MES_B172_R0129"]
PAGE_TURN = ("DK4_MES_B173_R0138", "DK4_MES_B173_R0141")
PIRATE_TURN = ("DK4_MES_B179_R0065", "DK4_MES_B179_R0068")
MENU_BLOCKS = (171,)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B151_B160_FOCUSED_ONLY.nds"': '"Hodram_B171_B180_FOCUSED_ONLY.nds"',
})
check = checked_text(previous.check, {
    '{"DK4_MES_B156_R0188","DK4_MES_B156_R0256","DK4_MES_B159_R0069","DK4_MES_B160_R0219"}':
        '{writer.FLEET_PANEL,"DK4_MES_B172_R0336","DK4_MES_B175_R0029","DK4_MES_B180_R0038"}',
    'hodram_B151_B160_gameplay_': 'hodram_B171_B180_gameplay_',
    '(PAGE_TURN, CARLO_TURN)': '(PAGE_TURN, PIRATE_TURN)',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::proofs-yifa-and-pirate", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

