"""Verify Maria's handover and Lil's map exchange in initialized emulator routes."""

from argparse import ArgumentParser
from inspect import getsource
import sys
from types import FunctionType

from scripts import replay_late_trade_exchanges_20261118 as template
from scripts import stage_regional_proof_dialogue_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
L_ROOT, M_ROOT = ROOT / "lil", ROOT / "maria"
LIL_ROM = L_ROOT / "Lil_Proof_Excerpts_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Proof_Excerpts_RESEARCH_ONLY.nds"
LIL_SETUP, MARIA_SETUP = L_ROOT / "lil_fixture.json", M_ROOT / "maria_fixture.json"
# Keep the new wording between exact neighboring responses.
LIL = ((145, (16, 19, 23)), (153, (26, 29, 33)))
MARIA = ((47, (129, 136, 140, 143, 147)), (298, (37, 41, 45)))


def prepare(name):
    clone = FunctionType(template.prepare_excerpts.__code__, vars(template) | {"stage": stage})
    if name == "lil":
        setup = clone(2, 22, 56, LIL, LIL_ROM)
        original = template.stage.ROOT / "lil_snapshot_inputs.json"
        inputs = base.load(original) + [
            dict(start=n, duration=5, buttons=["A"]) for n in range(3800, 5401, 250)
        ]
        path = L_ROOT / "inputs.json"
        base.save(path, inputs)
        base.save(LIL_SETUP, setup | dict(inputs=str(path), inputs_sha256=base.digest(path)))
    else:
        setup = clone(3, 33, 34, MARIA, MARIA_ROM)
        ref = template.maria.quest.prior.precedent
        unlock = base.load(ref.HISTORICAL)
        unlock.update(production_ROM=str(MARIA_ROM), production_ROM_sha256=base.digest(MARIA_ROM),
                      current_test_scope="Initialized Maria Proof dialogue excerpts with the existing system-only unlock.")
        path = M_ROOT / "existing_system_only_unlock.json"
        base.save(path, unlock)
        ref.validate_fixture(path)
        base.save(MARIA_SETUP, setup | dict(unlock=str(path)))


def capture(name):
    if name == "lil":
        setup = base.load(LIL_SETUP)
        assert base.digest(LIL_ROM) == setup["fixture_sha256"]
        assert base.digest(setup["inputs"]) == setup["inputs_sha256"]
        sys.argv = [sys.argv[0], "--rom", str(LIL_ROM), "--out", str(L_ROOT / "capture"),
                    "--frames", "5551", "--inputs-json", setup["inputs"], "--capture-every", "999999",
                    "--capture-at", *map(str, range(3650, 5551, 25))]
        template.harness.main()
    else:
        scope = vars(template.maria) | {"ROOT": M_ROOT, "ROM": MARIA_ROM, "FIXTURE": MARIA_SETUP}
        run = FunctionType(template.maria.capture.__code__, scope)
        run("live", [(n, "A") for n in range(4200, 7001, 350)], 7151)


def verify():
    assert not LIVE.exists()
    source = checked_text(getsource(template.verify), {
        "    fe_paint = stage.stage.system.native_painter(lil_context())\n": "",
        '("lil", SETUP, ROM.parent / "capture/capture_report.json")':
            '("lil", LIL_SETUP, L_ROOT / "capture/capture_report.json")',
        '("maria", MARIA_SETUP, MARIA_ROM.parent / "live/capture/capture_report.json")':
            '("maria", MARIA_SETUP, M_ROOT / "live/capture/capture_report.json")',
        '            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")':
            '            given = b"Lil" if label == "lil" else b"Maria"\n'
            '            body = raw[6:raw.index(0, 6)].replace(b"FI", given)',
        '''            if raw[5] == 254:
                physical = fe_paint(body)["physical"]
                planes = [bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])]
            else:
                planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''':
            '''            assert raw[5] < 207
            planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''',
        'assert len(observed) == 19': 'assert len(observed) == 14',
        'assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)':
            'assert any(b"Lil!" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B153_R0029" for row in observed)',
        'assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)':
            'assert any(b"Africa\'s Proof of Conquest" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B47_R0140" for row in observed)\n'
            '    assert any(b"Maria!" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B298_R0041" for row in observed)',
        "actual_substitution_and_FE_receipt=True": "actual_given_name_and_exact_quest_title=True",
        "inventory_and_payment_accounting=False": "item_inventory_and_quest_outcomes=False",
    })
    env = vars(template) | globals()
    exec(compile(source, __file__ + "::actual-Proof-and-name-glyph-masks", "exec"), env)
    env["verify"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture", "verify"))
    cli.add_argument("route", nargs="?", choices=("lil", "maria"))
    args = cli.parse_args()
    if args.action == "verify":
        verify()
    else:
        assert args.route
        globals()[args.action](args.route)
