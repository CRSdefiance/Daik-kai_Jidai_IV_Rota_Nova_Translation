"""Check each revised Rafael body in its original progressive or FE consumer."""

from inspect import getsource

from scripts import stage_rafael_mosque_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"

source = getsource(previous.main)
old_setup = source[source.index("    previous = base.load(PRIOR)"):source.index("    image =")]
old_reuse = source[source.index("                qualified ="):source.index("                try:")]
source = checked_text(source, {
    old_setup: "",
    old_reuse: "",
    "rendered, styles, pictures, reused = [], [], [], []": "rendered, styles, pictures = [], [], []",
    "assert len(rendered) == 40 and len(styles) == 1": "assert len(rendered) == 27 and not styles",
    '        reused_records=reused, prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n'
    '        previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],\n': "",
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::Rafael-checked-native-layout", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
