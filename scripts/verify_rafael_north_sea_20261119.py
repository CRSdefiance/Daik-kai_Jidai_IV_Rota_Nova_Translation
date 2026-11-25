"""Verify the native North Sea pages and check both revised name substitutions."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import audit_ceuta_lesson_20261119 as startup_audit
from scripts import replay_rafael_first_voyage_debrief_20261119 as boot
from scripts import stage_rafael_north_sea_20261119 as build
from scripts import verify_rafael_first_voyage_debrief_20261119 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"
STARTUP = build.ROOT / "startup_fixture"
STARTUP_PROOF = build.ROOT / "own_startup_verification.json"


def native_display():
    source = checked_text(getsource(previous.main), {
        '{"/data/SC0.DK4": [44, 47]}': '{"/data/SC0.DK4": [49, 50, 52]}',
        'len(checked) == 39 and len(retained) == 93': 'len(checked) == 18 and len(retained) == 94',
        '{f"DK4_MES_B44_R{i:04}" for i in (17, 152, 308, 316, 327)}':
            '{"DK4_MES_B49_R0388", "DK4_MES_B52_R0005"}',
        "Checked 39 revised pages, five macro records and 93 exact retentions.":
            "Checked 18 revised pages, two macro records and 94 exact retentions.",
    })
    scope = vars(previous) | globals()
    exec(compile(source, __file__ + "::north-sea-native-display", "exec"), scope)
    scope["main"]()


def startup():
    run = boot.startup_template.startup
    FunctionType(run.__code__, vars(boot.startup_template) | globals())()


def startup_proof():
    scope = vars(startup_audit) | dict(build=build, play=SimpleNamespace(STARTUP=STARTUP), STARTUP=STARTUP_PROOF)
    FunctionType(startup_audit.startup.__code__, scope)()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("native_display", "startup", "startup_proof"))
    globals()[parser.parse_args().action]()
