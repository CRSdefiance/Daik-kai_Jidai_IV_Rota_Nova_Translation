"""Check every revised Sakura, forest and Macao page with its native display consumer."""

from inspect import getsource

from scripts import stage_sakura_expeditions_macao_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR_ROOT = build.ROOT.with_name("research_v1")
PRIOR = PRIOR_ROOT / ROOT.name / PROOF.name

source = getsource(previous.main)
old_setup = source[source.index("    previous = base.load(PRIOR)"):source.index("    image =")]
old_reuse = source[source.index("                qualified ="):source.index("                try:")]
source = checked_text(source, {
    old_setup: """    previous = base.load(PRIOR)
    prior_stage_path = PRIOR_ROOT / build.PROOF.name
    prior_stage = base.load(prior_stage_path)
    assert previous["stage_proof_sha256"] == base.digest(prior_stage_path)
    assert prior_stage["predecessor_sha256"] == proof["predecessor_sha256"]
    assert previous["candidate_sha256"] == base.digest(PRIOR_ROOT / build.ROM.name)
    prior_image = base.NdsImage.open(PRIOR_ROOT / build.ROM.name)
    reusable = {(r["file_path"], r["id"]): r for r in previous["checked_records"]}
""",
    old_reuse: """                qualified = reusable.get((path, ident))
                if qualified and qualified.get("stored_hex", qualified.get("target_hex")) == value.hex():
                    rendered.append(qualified)
                    reused.append([path, ident])
                    continue
""",
    '    _, paint = inherited.early.prior.precedent.planners(ctx.arm)':
        """    assert all(image.read_file(resource) == prior_image.read_file(resource)
               for resource in (native.ARM, "/GRP/KANJI.FNT", "/COMMON/MESFILE.DK4"))
    _, paint = inherited.early.prior.precedent.planners(ctx.arm)""",
    "assert len(rendered) == 40 and len(styles) == 1": "assert len(rendered) == 129 and len(styles) == 17",
    '        reused_records=reused, prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n'
    '        previous_sheets=previous["previous_sheets"] + previous["contact_sheets"],\n':
        '        reused_records=reused, previous_sheets=previous["contact_sheets"],\n'
        '        prior_proof=dict(path=str(PRIOR), sha256=base.digest(PRIOR)),\n',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::source-bound-original-renderers", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()

