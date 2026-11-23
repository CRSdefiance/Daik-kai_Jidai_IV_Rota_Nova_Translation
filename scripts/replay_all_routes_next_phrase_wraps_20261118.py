"""Verify the shared Aziza dialogue in initialized Lil and Maria excerpts."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_rafael_early_phrase_wraps_20261118 as service
from scripts import replay_regional_proof_dialogue_20261118 as prior
from scripts import stage_all_routes_next_phrase_wraps_20261118 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
template = prior.template
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
L_ROOT, M_ROOT = ROOT / "lil", ROOT / "maria"
LIL_ROM = L_ROOT / "Lil_Aziza_Phrase_Excerpts_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Aziza_Phrase_Excerpts_RESEARCH_ONLY.nds"
LIL_SETUP, MARIA_SETUP = L_ROOT / "lil_fixture.json", M_ROOT / "maria_fixture.json"
LIL = ((12, (53, 60, 64)), (63, (62, 65, 69)))
MARIA = ((19, (40, 59, 63)), (31, (18, 21, 25, 42)))


def prepare(route):
    FunctionType(prior.prepare.__code__, vars(prior) | globals())(route)


def capture(route):
    FunctionType(prior.capture.__code__, vars(prior) | globals())(route)


def patch():
    FunctionType(service.patch.__code__, vars(service) | {"stage": stage})()


def startup():
    FunctionType(service.startup.__code__, vars(service) | {"stage": stage})()


def verify():
    proof = base.load(display.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM)
    names = proof["default_name_macros"]
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
        'assert len(observed) == 19': 'assert len(observed) == 13',
        'assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)':
            '''for route, record in ((2, "DK4_MES_B12_R0060"), (3, "DK4_MES_B19_R0059")):
        row, = [r for r in observed if r["route"] == route and r["id"] == record]
        body = bytes.fromhex(row["body_hex"])
        assert names[str(route)]["FO"].encode("ascii") in body and b"Bloodstained Shamshir" in body and b".." not in body''',
        'assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)':
            'assert any(b"Maria warned me:" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B31_R0042" for row in observed)',
        "actual_substitution_and_FE_receipt=True": "actual_company_names_and_shared_accusation=True",
        "inventory_and_payment_accounting=False": "original_quest_effects=False",
    })
    scope = vars(template) | globals() | {"names": names}
    exec(compile(source, __file__ + "::actual-company-name-glyphs", "exec"), scope)
    scope["verify"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "patch", "startup", "verify"))
    cli.add_argument("route", nargs="?", choices=("lil", "maria"))
    args = cli.parse_args()
    if args.action in ("prepare", "capture"):
        assert args.route
        globals()[args.action](args.route)
    else:
        globals()[args.action]()
