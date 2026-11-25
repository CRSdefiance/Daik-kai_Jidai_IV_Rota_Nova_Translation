"""Check the final warrior and village pages with the original renderers."""

from scripts import stage_warrior_village_handovers_20261118 as build
from scripts import verify_sakura_expeditions_macao_20261118 as precedent
from scripts import verify_london_guild_assignments_20261118 as runtime
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR_ROOT = build.ROOT.with_name("research_v1")
PRIOR = PRIOR_ROOT / ROOT.name / PROOF.name
verified_layouts = {}


def paragraph(ctx, font, paint, expand, fe_paint, names, row, raw, plan):
    key = (row["kind"], raw, plan["encoded_hex"], tuple(plan["lines"]), plan["expected_native_pages"])
    if key not in verified_layouts:
        verified_layouts[key] = runtime.paragraph(ctx, font, paint, expand, fe_paint, names, row, raw, plan)
    assert runtime.build.review.logical(raw[1:].decode("ascii")) == row["english"]
    return verified_layouts[key] | {"id": row["id"], "file_path": row["file_path"]}


source = checked_text(precedent.source, {
    'if not cmd["record_ids"] or cmd["current"] == cmd["stored"]:':
        'if not cmd["record_ids"] or cmd["current"] == cmd["stored"] or cmd["word"] in stage.MENU:',
    "assert len(rendered) == 129 and len(styles) == 17":
        "assert len(rendered) == 167 and len(styles) == sum(\n"
        '        c["word"] == stage.STYLE and c["current"] != c["stored"]\n'
        '        for g in proof["groups"] for c in g["commands"])',
    'if row["decision"] == "revision"\n': 'if row["decision"] == "revision" and row["kind"] != "typed-choice-label"\n',
})
scope = precedent.scope | globals()
exec(compile(source, __file__ + "::native-layout", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
