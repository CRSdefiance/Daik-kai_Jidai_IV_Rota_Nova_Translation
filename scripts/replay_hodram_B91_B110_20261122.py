"""Check representative treasure dialogue and the choice and panel transitions."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B61_B64_20261122 as panels
from scripts import replay_hodram_B81_B89_20261122 as previous
from scripts import verify_hodram_B91_B110_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup_touch/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (91,"112"),(91,27),(91,31),(91,72),(91,75),(91,78),(91,84),(91,87),(91,94),(91,103),(91,106),
    (92,22),(92,52),(93,5),(93,13),(93,17),(93,21),(93,33),(93,51),
    (95,26),(95,29),(97,35),(97,46),(97,74),(100,21),(100,27),
    (101,43),(101,60),(101,63),(102,26),(102,41),(103,21),(103,38),
    (104,13),(104,16),(105,37),(108,8),(108,20),(109,10),
    (110,15),(110,27),(110,47),(110,51),(110,59),(110,69),
)
test_name = ["DK4_MES_B93_R0013", "DK4_MES_B93_R0017", "DK4_MES_B93_R0021"]
PAGE_TURN = ("DK4_MES_B101_R0060", "DK4_MES_B101_R0063")
SHORTER_TURN = ("DK4_MES_B104_R0013", "DK4_MES_B104_R0016")
match_panel = panels.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B81_B89_FOCUSED_ONLY.nds"': '"Hodram_B91_B110_FOCUSED_ONLY.nds"',
})
original = previous.check
symbol_start = original.index('    symbols =')
symbol_end = original.index('    assert candidate == native_report')
page_start = original.index('                if ident in display.SYMBOLS')
page_end = original.index('            if checked.get("layouts"):', page_start)
names_start = original.index('    names_observed =')
names_end = original.index('    final, image =', names_start)
check = checked_text(original, {
    original[symbol_start:symbol_end]: "",
    original[page_start:page_end]: '''                current = stored.decode("ascii")
                body = stage.review.TOKEN.sub(lambda m: native_report["default_names"][m[0]], current).encode("ascii")
            view = paint(arm, font, body)
            assert view["complete_consumed_bytes"] == len(body)
            plane = bytes.fromhex(view["pages"][page - 1]["native_plane_hex"])
''',
    original[names_start:names_end]: '''    turns = {}
    for pair, expected in ((PAGE_TURN, [1, 2, 1]), (SHORTER_TURN, [1, 1])):
        observed_turn = [(h["id"], h["page"], h["frame"]) for h in holds if h["id"] in pair]
        assert [ident for ident, _, _ in observed_turn] == [pair[0]] * (len(expected) - 1) + [pair[1]]
        assert [page for _, page, _ in observed_turn] == expected
        assert [frame - observed_turn[0][2] for _, _, frame in observed_turn] == list(range(0, 300 * len(expected), 300))
        turns[pair[0]] = observed_turn
''',
    'display.CONTEXT_SHORT_NAMES.get(ident, (None, row["speaker"]))[1]':
        'display.DYNAMIC_ROLE.get(ident, (None, row["speaker"]))[1]',
    'm["block"] == 87 and m["record_ids"] == ["SC1_B87_CHOICE_302_0", "SC1_B87_CHOICE_302_1"]':
        'm["block"] == 91 and m["record_ids"] == ["SC1_B91_CHOICE_112_0", "SC1_B91_CHOICE_112_1"]',
    'len(holds) == len(expected_speech)': 'len(holds) == len(expected_speech) + 1',
    'exact_name_introductions=names_observed,': 'page_transitions=turns, dynamic_nameplates=sorted(display.DYNAMIC_ROLE),',
    'hodram_B81_B89_gameplay_': 'hodram_B91_B110_gameplay_',
    'display.SYMBOLS <= speech_ids and sum(h["system_FE"] for h in holds) == 5':
        'set(display.DYNAMIC_ROLE) <= speech_ids and sum(h["system_FE"] for h in holds) == 7',
    ', ELLIPSIS, display.OPAQUE)': ')',
    ' opaque_source_symbols=sorted(display.SYMBOLS),': '',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::Hodram-treasure-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

