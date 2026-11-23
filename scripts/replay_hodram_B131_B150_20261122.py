"""Replay the crew lessons, Sera's introduction, and selected discoveries."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B111_B130_20261122 as previous
from scripts import verify_hodram_B131_B150_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (131,41),(131,54),(131,57),(131,61),
    (132,53),(132,68),(132,96),(132,"1532"),(132,145),(132,159),(132,174),
    (133,"style10"),(134,"134"),(134,28),(135,"124"),(135,35),(135,39),
    (136,"130"),(136,31),(136,35),(136,38),(136,44),
    (137,21),(137,32),(137,35),(137,39),(137,58),(137,74),
    (138,12),(138,23),(138,38),(139,7),
    (140,9),(140,87),(140,90),(140,"2334"),(140,123),(140,136),(141,40),
    (142,5),(142,8),(142,11),(142,27),(142,159),(142,182),(142,186),
    (142,213),(142,217),(142,220),(142,223),(142,226),(142,230),(142,243),(142,246),(142,250),(142,253),
    (143,30),(143,33),(143,37),(143,75),(143,79),(143,87),(143,96),
    (144,15),(145,29),(146,17),(147,20),(148,103),(149,78),(150,72),(150,89),
)
test_name = ["DK4_MES_B142_R0220", "DK4_MES_B142_R0223", "DK4_MES_B142_R0226"]
PAGE_TURN = ("DK4_MES_B142_R0008", "DK4_MES_B142_R0011")
SERA_NAME = ("DK4_MES_B142_R0246", "DK4_MES_B142_R0250")
MENU_BLOCKS = (132,134,135,136,140)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B111_B130_FOCUSED_ONLY.nds"': '"Hodram_B131_B150_FOCUSED_ONLY.nds"',
})
s = previous.check
turns = s[s.index("    turns = {}"):s.index("    final, image =")]
check = checked_text(s, {
    'for block in MENU_BLOCKS for slot in range(3)': 'for block in MENU_BLOCKS for slot in range(2)',
    turns: '''    turns = {}
    for pair in (PAGE_TURN, SERA_NAME):
        observed_turn = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in pair]
        ids, pages, frames = zip(*observed_turn)
        assert ids[-1] == pair[1] and all(i == pair[0] for i in ids[:-1])
        expected = native_rows[pair[0]]["layouts"][0]["page_sha256"]
        assert pages == (*range(1,len(expected)+1),1)
        assert [t-frames[0] for t in frames] == list(range(0,300*len(pages),300))
        turns[pair[0]] = observed_turn
    sampled = {h["id"] for h in holds}
    assert {"DK4_MES_B143_R0033","DK4_MES_B143_R0079","DK4_MES_B143_R0087","DK4_MES_B137_R0074"} <= sampled
''',
    'hodram_B111_B130_gameplay_': 'hodram_B131_B150_gameplay_',
    'assert len(styles) == 2 and all(i.startswith("SC1_B125_STYLE_") for i in styles)':
        'assert len(styles) == 1 and styles[0].startswith("SC1_B133_STYLE_10_")',
    'assert sum(h["system_FE"] for h in holds) == 13':
        'assert sum(h["system_FE"] for h in holds) == sum(rows[i]["source_selector"] == 254 for i in speech_ids)',
})
scope = previous.scope | globals()
for source in (producer,check):
    exec(compile(source,__file__+"::lessons-and-Sera", "exec"),scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay","check"))
    scope[parser.parse_args().action]()

