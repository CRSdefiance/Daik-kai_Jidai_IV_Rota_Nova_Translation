"""Check every revised cave paragraph through its native text consumer."""

from inspect import getsource

from scripts import stage_jungle_caves_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR = build.ROOT.with_name("research_v1") / ROOT.name / PROOF.name


source = getsource(previous.main)
verification = checked_text(source, {
    "assert len(rendered) == 40 and len(styles) == 1": "assert len(rendered) == 78 and len(styles) == 19",
    'previous_sheets=previous["previous_sheets"] + previous["contact_sheets"]':
        'previous_sheets=previous["contact_sheets"]',
})
env = vars(previous) | globals()
exec(compile(verification, __file__ + "::same-native-proof-with-cave-scope", "exec"), env)

if __name__ == "__main__":
    env["main"]()
