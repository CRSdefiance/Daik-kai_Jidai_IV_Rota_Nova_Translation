"""Check each stored town command and render every revised page."""

from inspect import getsource

from scripts import stage_seville_stockholm_trends_20261121 as build
from scripts import verify_hamburg_ceramics_cross_route_20261120 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = build.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


if __name__ == "__main__":
    program = checked_text(getsource(precedent.main), {"len(lookup) == 68": "len(lookup) == 72"})
    env = vars(precedent) | globals()
    exec(compile(program, __file__ + "::complete-stored-town-pages", "exec"), env)
    env["main"]()
