"""Cold-boot exact excerpts to test page turns, FE staging and the return to port."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import replay_rafael_followup_encounters_20261121 as template
from scripts import replay_rafael_ruins_and_proof_20261121 as pacing
from scripts import verify_rafael_B161_B169_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, PATH = display.stage, display.base, display.native, display.PATH
ROOT = stage.ROOT / "focused_gameplay"
REPORT, PROOF = ROOT / "capture/capture_report.json", ROOT / "verified_gameplay.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
SELECTED = (
    (161, 25), (161, 62), (165, 16), (166, 69), (166, 72), (166, 85),
    (166, 196), (166, 205), (166, 208), (166, 245), (166, 249), (166, 253), (166, 261), (166, 265),
    (166, 526), (166, 538), (166, 629), (166, 787), (166, 791), (166, 794), (166, 797), (166, 908), (166, 912),
    (167, 5), (167, 180), (168, 214), (169, 110), (169, 291),
)


def match_panel(plane, system, image, ident):
    if ident == "DK4_MES_B166_R0265":
        crop = image.crop((16, 296, 244, 360)).get_flattened_data()
        assert len(crop) == len(plane) and set(plane) == {0, 14, 15}
        return bytes(v == 15 for v in plane) == bytes(v == (0, 8, 0) for v in crop) and (
            bytes(v == 14 for v in plane) == bytes(v == (197, 198, 197) for v in crop))
    return template.panel.mask_check(plane, 228 if system else 216, image)


producer = checked_text(pacing.producer, {
    'groups[120]["commands"]': 'groups[169]["commands"]',
    '"Rafael_Ruins_And_Proof_RESEARCH_ONLY.nds"': '"Rafael_B161_B169_FOCUSED_ONLY.nds"',
})
check = checked_text(getsource(template.check), {
    ' == base.digest(stage.ROOT / "clean_rebuilt.nds")': '',
    'panel.mask_check(plane, 228 if system else 216, image)': 'match_panel(plane, system, image, ident)',
    '    assert [m["highlight"] for m in menus] == [0, 1]': '    assert not menus',
    '["DK4_MES_B91_R0101", "DK4_MES_B91_R0109", "DK4_MES_B91_R0112", "DK4_MES_B92_R0005"]':
        '["DK4_MES_B165_R0016", "DK4_MES_B166_R0069", "DK4_MES_B166_R0072"]',
    '    assert [h[0] for h in turn] == transition_ids':
        '    assert [h[0] for h in turn] == [transition_ids[0], *transition_ids]\n'
        '    assert [h[1] for h in turn] == [1, 2, 1, 1]',
    'rafael_encounters_gameplay_': 'rafael_B161_B169_gameplay_',
    '''    miracle_menu, = [m for m in native_report["menus"] if m["block"] == 91]
    observed = {r["id"] for r in holds} | set(miracle_menu["record_ids"])''':
        '''    observed = {r["id"] for r in holds}
    assert len(holds) == len(SELECTED) + 1
    assert observed == {f"DK4_MES_B{block}_R{index:04d}" for block, index in SELECTED}''',
    ' and two miracle menu highlights': ' across the focused excerpts',
})
scope = vars(template) | globals() | dict(
    stage=SimpleNamespace(PROOF=stage.PROOF, ROM=stage.ROM, ROOT=stage.ROOT, OUTPUT=stage.MANUSCRIPT,
                          review=SimpleNamespace(TOKEN=stage.TOKEN)),
    schedule=pacing.schedule,
)
for script in (producer, check):
    exec(compile(script, __file__ + "::focused-native-excerpts", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "check"))
    scope[parser.parse_args().action]()
