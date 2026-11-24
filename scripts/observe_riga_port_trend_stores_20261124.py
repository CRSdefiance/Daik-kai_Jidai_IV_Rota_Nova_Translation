"""Observe Riga trend and fleet stores using each instruction's actual registers."""

from inspect import getsource
from types import FunctionType

from scripts import observe_riga_port_trend_20261124 as earlier
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = earlier.ROOT.with_name("editorial_20261124_riga_port_trend_stores")


if __name__ == "__main__":
    recipe = checked_text(getsource(earlier.observe), {
        "value = (v[5] if pc == 0x020347A4 else v[6]) & 255":
            "opcode = v[1]\n     owner = v[4 + (opcode >> 16 & 15)]\n     value = v[4 + (opcode >> 12 & 15)] & 255",
        'kind="fleet_byte", caller_LR=v[18], owner=v[4], value=value':
            'kind="fleet_byte", caller_LR=v[18], owner=owner, value=value',
    })
    scope = vars(earlier) | dict(ROOT=ROOT, __file__=__file__)
    exec(compile(recipe, __file__ + "::native-fleet-store-registers", "exec"), scope)
    FunctionType(earlier.main.__code__, scope)()
