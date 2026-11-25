"""Replay focused settlement, rescue, menu, and recruitment dialogue checks."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_hodram_B71_B80_20261122 as previous
from scripts import verify_hodram_B81_B89_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (81,39),(81,47),(81,78),
    (82,5),(82,12),(82,24),(82,41),(82,45),
    (83,12),
    (84,48),(84,56),(84,109),(84,141),(84,150),(84,169),
    (85,18),(85,47),(85,80),(85,129),(85,136),
    (86,47),(86,100),(86,103),(86,110),(86,113),(86,116),(86,119),(86,139),(86,145),
    (86,191),(86,295),(86,307),(86,322),
    (87,27),(87,"302"),(87,42),(87,66),(87,87),(87,93),(87,98),(87,101),
    (88,8),(88,19),(88,89),(88,93),(88,125),(88,169),(88,221),
    (89,28),(89,51),(89,67),(89,80),
)
test_name = ["DK4_MES_B86_R0110", "DK4_MES_B86_R0113", "DK4_MES_B86_R0116"]
ELLIPSIS_ID = "DK4_MES_B87_R0101"

match_panel = type(previous.match_panel)(previous.match_panel.__code__,
    previous.match_panel.__globals__ | {"display": display, "ELLIPSIS_ID": ELLIPSIS_ID})
producer = checked_text(previous.producer, {
    '"Hodram_B71_B80_FOCUSED_ONLY.nds"': '"Hodram_B81_B89_FOCUSED_ONLY.nds"',
})
page_check = previous.check[previous.check.index("    turn_results = []"):
                            previous.check.index("    final, image =")]
check = checked_text(previous.check, {
    '    assert not menus':
        '''    assert [m["highlight"] for m in menus] == [0, 1]
    assert all(m["block"] == 87 and m["record_ids"] == ["SC1_B87_CHOICE_302_0", "SC1_B87_CHOICE_302_1"]
               for m in menus)''',
    page_check: '''    names_observed = [h["id"] for h in holds if h["id"] in
        {"DK4_MES_B84_R0169", "DK4_MES_B85_R0129", "DK4_MES_B87_R0087", "DK4_MES_B88_R0221"}]
    assert len(names_observed) == 4
''',
    'len(holds) == len(expected_speech) + 2': 'len(holds) == len(expected_speech)',
    'exact_two_page_transitions=turn_results,': 'exact_name_introductions=names_observed,',
    'hodram_B71_B80_gameplay_': 'hodram_B81_B89_gameplay_',
    'sum(h["system_FE"] for h in holds) == 4': 'sum(h["system_FE"] for h in holds) == 5',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-rescue-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
