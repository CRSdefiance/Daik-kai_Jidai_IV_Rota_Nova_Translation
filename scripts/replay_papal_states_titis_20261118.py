"""Replay selected original Papal States and Titis commands after route initialization."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_late_trade_exchanges_20261118 as maria
from scripts import replay_story_phrase_continuity_20261118 as rafael
from scripts import stage_papal_states_titis_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
ROOT = stage.ROOT / "initialized_replays"
LIVE = ROOT / "replay.json"
R_ROOT, M_ROOT = ROOT / "rafael", ROOT / "maria"
ROM = R_ROOT / "Rafael_Papal_Titis_Excerpts_RESEARCH_ONLY.nds"
MARIA_ROM = M_ROOT / "Maria_Papal_Titis_Excerpts_RESEARCH_ONLY.nds"
SETUP, MARIA_SETUP = R_ROOT / "rafael_fixture.json", M_ROOT / "maria_fixture.json"
RAFAEL = ((246, (9, 12, 19, 26, 29, 33, 47)), (262, (7, 10, 13)))
MARIA = ((207, (28, 32, 36)), (222, (6, 9, 12)))


def prepare():
    FunctionType(rafael.prepare.__code__, vars(rafael) | globals())("rafael")
    clone = FunctionType(maria.prepare_excerpts.__code__, vars(maria) | {"stage": stage})
    setup = clone(3, 33, 34, MARIA, MARIA_ROM)
    original = maria.maria.quest.prior.precedent
    unlock = base.load(original.HISTORICAL)
    unlock.update(production_ROM=str(MARIA_ROM), production_ROM_sha256=base.digest(MARIA_ROM),
                  current_test_scope="Initialized Maria Papal States and Titis excerpts with the existing system-only unlock.")
    path = M_ROOT / "existing_system_only_unlock.json"
    base.save(path, unlock)
    original.validate_fixture(path)
    base.save(MARIA_SETUP, setup | {"unlock": str(path)})


def capture_rafael():
    FunctionType(rafael.capture.__code__, vars(rafael) | globals())("rafael")


def capture_maria():
    scope = vars(maria.maria) | {"ROOT": M_ROOT, "ROM": MARIA_ROM, "FIXTURE": MARIA_SETUP}
    FunctionType(maria.maria.capture.__code__, scope)("live", [(n, "A") for n in range(4200, 6301, 350)], 6451)


def verify():
    assert not LIVE.exists()
    source = getsource(maria.verify)
    # Rafael's preparation performs the same whole-ROM inverse under a different receipt key.
    source = checked_text(source, {
        "    fe_paint = stage.stage.system.native_painter(lil_context())\n": "",
        '("lil", SETUP, ROM.parent / "capture/capture_report.json")':
            '("rafael", SETUP, R_ROOT / "capture/capture_report.json")',
        'label == "lil"': 'label == "rafael"',
        'route=setup["route"]': 'route=setup.get("route", setup.get("initialized_route"))',
        'setup["whole_source_ROM_inverse"]': 'setup.get("whole_source_ROM_inverse", setup.get("exact_ROM_inverse"))',
        '            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")':
            '            given = b"Rafael" if label == "rafael" else b"Maria"\n'
            '            body = raw[6:raw.index(0, 6)].replace(b"FI", given)',
        '''            if raw[5] == 254:
                physical = fe_paint(body)["physical"]
                planes = [bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])]
            else:
                planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''':
            '''            assert raw[5] < 207
            planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''',
        'assert len(observed) == 19': 'assert len(observed) == 16',
        'assert any(b"Argot Co." in bytes.fromhex(row["body_hex"]) for row in observed)':
            'assert any(b"Rafael!" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B262_R0007" for row in observed)',
        'assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)':
            'assert any(b"Maria!" in bytes.fromhex(row["body_hex"]) and row["id"] == "DK4_MES_B222_R0006" for row in observed)',
        "initialized_Lil_and_Maria=True": "initialized_Rafael_and_Maria=True",
        "actual_substitution_and_FE_receipt=True": "actual_given_name_substitutions=True",
        "inventory_and_payment_accounting=False": "quest_and_trade_effects=False",
        "initialized Lil and Maria": "initialized Rafael and Maria",
    })
    env = vars(maria) | globals()
    exec(compile(source, __file__ + "::native-glyph-masks", "exec"), env)
    env["verify"]()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("prepare", "capture_rafael", "capture_maria", "verify"))
    globals()[cli.parse_args().action]()

