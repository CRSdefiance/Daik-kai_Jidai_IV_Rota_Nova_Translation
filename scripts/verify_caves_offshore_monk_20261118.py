"""Validate the final text through the native progressive and modal renderers."""

from scripts import stage_caves_offshore_monk_20261118 as build
from scripts import verify_sakura_expeditions_macao_20261118 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR_ROOT = build.ROOT.with_name("research_v3")
PRIOR = PRIOR_ROOT / ROOT.name / PROOF.name
source = checked_text(precedent.source, {
    'previous_sheets=previous["contact_sheets"],':
        'previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],',
    'if not cmd["record_ids"] or cmd["current"] == cmd["stored"]:':
        'if not cmd["record_ids"] or cmd["current"] == cmd["stored"] or cmd["word"] in stage.MENU:',
    "assert len(rendered) == 129 and len(styles) == 17":
        "assert len(rendered) == 158 and len(styles) == sum(\n"
        '        c["word"] == stage.STYLE and c["current"] != c["stored"]\n'
        '        for g in proof["groups"] for c in g["commands"])',
    'if row["decision"] == "revision"\n': 'if row["decision"] == "revision" and row["kind"] != "typed-choice-label"\n',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::native-wrap-and-glyphs", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
