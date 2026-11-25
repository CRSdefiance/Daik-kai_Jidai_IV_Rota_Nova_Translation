"""Verify the compiled desert and incense burner pages in their native consumers."""

from scripts import stage_desert_censer_20261118 as build
from scripts import verify_sakura_expeditions_macao_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR_ROOT = build.ROOT.with_name("research_v1")
PRIOR = PRIOR_ROOT / ROOT.name / PROOF.name
source = checked_text(precedent.source, {
    "assert len(rendered) == 129 and len(styles) == 17": "assert len(rendered) == 142 and len(styles) == 38",
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::stored-native-layout", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
