"""Replay the farewell panels, recruit exchanges and two dialogue transitions."""

from argparse import ArgumentParser
from types import SimpleNamespace

from scripts import replay_hodram_B131_B150_20261122 as previous
from scripts import verify_hodram_B151_B160_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


writer = display.stage
base, native, PATH = writer.base, writer.native, display.PATH
ROOT = writer.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = writer.ROOT / "startup/capture/capture_report.json"
stage = SimpleNamespace(PROOF=writer.PROOF, ROM=writer.ROM, ROOT=writer.ROOT, OUTPUT=writer.OUTPUT,
                        review=SimpleNamespace(TOKEN=writer.TOKEN))
SELECTED = (
    (151,5), (151,13), (151,20), (152,6), (153,9), (154,54), (155,30), (155,33), (155,36), (155,43),
    (156,14), (156,154), (156,157), (156,176), (156,180), (156,184), (156,188),
    (156,193), (156,197), (156,201), (156,210), (156,228), (156,252), (156,256), (156,260),
    (156,310), (156,314), (156,340), (156,344), (156,347),
    (157,34), (157,37), (157,80), (157,86), (157,106),
    (158,22), (158,42), (158,86), (158,115), (158,172), (158,178), (158,195), (158,201),
    (159,38), (159,51), (159,58), (159,69), (159,120), (159,149), (159,229),
    (160,5), (160,43), (160,52), (160,123), (160,148), (160,208), (160,211),
    (160,219), (160,222), (160,230), (160,233), (160,249), (160,260), (160,271),
)
test_name = ["DK4_MES_B156_R0193", "DK4_MES_B156_R0197", "DK4_MES_B156_R0201"]
PAGE_TURN = ("DK4_MES_B158_R0172", "DK4_MES_B158_R0178")
CARLO_TURN = ("DK4_MES_B160_R0230", "DK4_MES_B160_R0233")
MENU_BLOCKS = ()
match_panel = previous.match_panel
producer = checked_text(previous.producer, {
    '"Hodram_B131_B150_FOCUSED_ONLY.nds"': '"Hodram_B151_B160_FOCUSED_ONLY.nds"',
    '            plan = group["plans"].get(ident)': '''            plan = group["plans"].get(ident)
            if ident == PAGE_TURN[0]:
                assert plan is None
                raw = bytes.fromhex(command["stored"])
                body = raw[6:raw.index(0, 6)]
                ctx = SimpleNamespace(image=image, arm=image.read_file(native.ARM))
                count = len(town.clipped_renderer(ctx)(ctx.arm, image.read_file("/GRP/KANJI.FNT"), body)["pages"])
                assert count == 2
                plan = {"expected_native_pages": count}
'''.rstrip(),
})
check = checked_text(previous.check, {
    '{"DK4_MES_B143_R0033","DK4_MES_B143_R0079","DK4_MES_B143_R0087","DK4_MES_B137_R0074"}':
        '{"DK4_MES_B156_R0188","DK4_MES_B156_R0256","DK4_MES_B159_R0069","DK4_MES_B160_R0219"}',
    'hodram_B131_B150_gameplay_': 'hodram_B151_B160_gameplay_',
    '(PAGE_TURN, SERA_NAME)': '(PAGE_TURN, CARLO_TURN)',
    '        expected = native_rows[pair[0]]["layouts"][0]["page_sha256"]\n        assert pages == (*range(1,len(expected)+1),1)':
        '        assert pages == ((1, 2, 1) if pair == PAGE_TURN else (1, 1))',
    'assert len(styles) == 1 and styles[0].startswith("SC1_B133_STYLE_10_")': 'assert not styles',
})
scope = previous.scope | globals()
for source in (producer, check):
    exec(compile(source, __file__ + "::farewell-and-recruitment", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()

