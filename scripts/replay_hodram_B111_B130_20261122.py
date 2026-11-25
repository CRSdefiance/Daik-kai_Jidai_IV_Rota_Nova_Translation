"""Replay the sailing controls, riddles, crew styles and linked conversation turns."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B91_B110_20261122 as previous
from scripts import verify_hodram_B111_B130_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (111,19),(112,5),(112,17),(113,37),
    (114,21),(114,136),(114,"782"),(114,191),(114,197),(114,204),
    (115,32),(115,54),(115,62),(115,65),(115,92),(115,182),
    (116,6),(116,20),(117,16),(117,27),
    (118,18),(118,22),(118,"372"),(118,94),(118,98),
    (119,36),(119,"336"),(119,100),
    (120,25),(120,36),(120,46),(121,42),(121,49),(121,114),(121,118),(121,121),
    (122,42),(123,65),(123,89),(123,92),(123,124),(123,127),(123,138),(123,142),(124,22),
    (125,"style54"),(125,32),(125,"style450"),
    (126,13),(126,17),(126,26),(126,38),(127,5),(127,49),(127,53),(127,57),(127,61),(127,64),
    (129,5),(129,69),(129,77),(129,80),(129,105),(130,20),(130,31),
)
test_name = ["DK4_MES_B127_R0053", "DK4_MES_B127_R0057", "DK4_MES_B127_R0061"]
PAGE_TURN = ("DK4_MES_B123_R0124", "DK4_MES_B123_R0127")
DIOGO_TURN = ("DK4_MES_B129_R0077", "DK4_MES_B129_R0080")
MENU_BLOCKS = (114, 118, 119)
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B91_B110_FOCUSED_ONLY.nds"': '"Hodram_B111_B130_FOCUSED_ONLY.nds"',
})
s = previous.check
menu_check = s[s.index('    assert [m["highlight"]'):s.index("    transition_ids = test_name")]
turns = s[s.index("    turns = {}"):s.index("    final, image =")]
scope_test = s[s.index("    assert len(holds)"):s.index("    paths = (fixture_file")]
check = checked_text(s, {
    menu_check: '''    assert [(m["block"], m["highlight"]) for m in menus] == [
        (block, slot) for block in MENU_BLOCKS for slot in range(3)]
''',
    turns: '''    turns = {}
    for pair in (PAGE_TURN, DIOGO_TURN):
        observed_turn = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in pair]
        ids, pages, frames = zip(*observed_turn)
        assert ids[-1] == pair[1] and all(i == pair[0] for i in ids[:-1])
        expected = native_rows[pair[0]]["layouts"][0]["page_sha256"]
        assert pages == (*range(1,len(expected)+1),1)
        assert [t-frames[0] for t in frames] == list(range(0,300*len(pages),300))
        turns[pair[0]] = observed_turn
    assert any(h["id"] == "DK4_MES_B126_R0013" for h in holds)
    assert any(h["id"] == "DK4_MES_B115_R0065" for h in holds)
''',
    'display.DYNAMIC_ROLE.get(ident, (None, row["speaker"]))[1]': 'row["speaker"]',
    'hodram_B91_B110_gameplay_': 'hodram_B111_B130_gameplay_',
    scope_test: '''    assert len(holds) == sum(r["type"] == "speech" for r in fixture["requested_holds"])
    styles = [h["id"] for h in holds if "_STYLE_" in h["id"]]
    assert len(styles) == 2 and all(i.startswith("SC1_B125_STYLE_") for i in styles)
    assert sum(h["system_FE"] for h in holds) == 13
    observed = speech_ids | {k for m in menus for k in m["record_ids"]}
''',
    'dynamic_nameplates=sorted(display.DYNAMIC_ROLE),': 'observed_style_owners=styles,',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::riddles-and-sail-controls", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

