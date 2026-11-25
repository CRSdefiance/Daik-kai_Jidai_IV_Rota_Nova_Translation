"""Replay the rose handovers and matched convoy letters in initialized Lil and Maria."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_regional_proof_dialogue_20261118 as regional
from scripts import stage_all_routes_final_flagged_wraps_20261118 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, template = stage.base, stage.native, regional.template
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
L_ROOT, M_ROOT = ROOT / "lil", ROOT / "maria"
LIL_ROM = L_ROOT / "Lil_Rose_And_Convoy_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Rose_And_Convoy_RESEARCH_ONLY.nds"
LIL_SETUP, MARIA_SETUP = L_ROOT / "lil_fixture.json", M_ROOT / "maria_fixture.json"
LIL = ((239, (87, 91, 94)), (240, (115, 120)), (235, (41, 44, 47)))
MARIA = ((208, (43, 46, 49)), (213, (42, 45, 49, 102, 107)))


def prepare():
    prepare_route = FunctionType(regional.prepare.__code__, vars(regional) | globals())
    for route in ("lil", "maria"):
        prepare_route(route)


def capture(route):
    FunctionType(regional.capture.__code__, vars(regional) | globals())(route)


def observations(rows):
    assert len(rows) == 16
    for route in (2, 3):
        assert sum(r["route"] == route for r in rows) == 8
    for pair, phrase in (
        (("DK4_MES_B240_R0120", "DK4_MES_B213_R0107"), "to the governor's office!"),
        (("DK4_MES_B235_R0044", "DK4_MES_B208_R0043"), "The convoy managed to escape."),
        (("DK4_MES_B235_R0047", "DK4_MES_B208_R0046"), "with a scientific explanation"),
    ):
        panels = [r for r in rows if r["id"] in pair]
        assert len(panels) == 2 and all(r["page"] == 1 for r in panels)
        a, b = [stage.review.logical(bytes.fromhex(r["body_hex"]).decode("ascii")) for r in panels]
        assert a == b and phrase in a


def verify():
    earlier = base.load(stage.parent.display.PROOF)
    names = earlier["default_name_macros"]
    original, revised = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    assert all(original.read_file(asset) == revised.read_file(asset) for asset in display.ASSETS)
    source = checked_text(getsource(template.verify), {
        "    fe_paint = stage.stage.system.native_painter(lil_context())\n": "",
        '("lil", SETUP, ROM.parent / "capture/capture_report.json")':
            '("lil", LIL_SETUP, L_ROOT / "capture/capture_report.json")',
        '("maria", MARIA_SETUP, MARIA_ROM.parent / "live/capture/capture_report.json")':
            '("maria", MARIA_SETUP, M_ROOT / "live/capture/capture_report.json")',
        '            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")':
            '            body = display.prior.default_text(raw[6:raw.index(0, 6)], names[str(setup["route"])])',
        '''            if raw[5] == 254:
                physical = fe_paint(body)["physical"]
                planes = [bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])]
            else:
                planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''':
            '''            assert raw[5] < 207
            planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''',
        '''    assert len(observed) == 19
    assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)
    assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)''':
            "    observations(observed)",
        "actual_substitution_and_FE_receipt=True": "matched_rose_handover_and_convoy=True",
        "inventory_and_payment_accounting=False": "original_quest_effects=False",
    })
    env = vars(template) | globals() | {"names": names}
    exec(compile(source, __file__ + "::matching-initialized-exchanges", "exec"), env)
    env["verify"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture_lil", "capture_maria", "verify"))
    action = parser.parse_args().action
    if action.startswith("capture_"):
        capture(action.split("_", 1)[1])
    else:
        globals()[action]()
