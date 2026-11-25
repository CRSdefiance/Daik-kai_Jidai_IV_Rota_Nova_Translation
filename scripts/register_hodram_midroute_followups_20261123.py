"""Register the cumulative Hodram dialogue, tutorial, and choice follow-ups."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_midroute_exchanges_20261122 as prior
from scripts import replay_hodram_midroute_followups_20261123 as live
from scripts import review_hodram_midroute_nameplates_20261123 as labels
from scripts import stage_hodram_midroute_followups_20261123 as stage
from scripts import verify_hodram_midroute_followups_20261123 as checked
from scripts.source_locked_derivation_v5118 import checked_text

base, native = prior.base, prior.native
parent = stage.active
PROFILE = "all-routes-hodram-midroute-followups-v1-20261123"
ROOT = stage.BATCH.parent / "registered"
WORK = stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Hodram_Midroute_Followups_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261123_hodram_midroute_followups_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_hodram_midroute_followups_registered_20261123.md")
DISPLAY, EVIDENCE = stage.NATIVE, stage.ROOT
GLYPHS, FE, CHOICE, ROLES, STYLES = checked.GLYPHS, stage.FE_PROOF, checked.CHOICES, labels.PROOF, checked.STYLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 13 Hodram exchanges, including the resupply lesson, trade lesson, and Escante's proposal."
RUNS = ("route1", *live.RUNS)
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())

controls = checked_text(getsource(prior.retained_controls), {
    'modal["complete_stored_page_count"] == 17': 'modal["complete_stored_page_count"] == 10',
    'ident == "DK4_MES_B118_R0125"': 'ident in ("DK4_MES_B135_R0035", "DK4_MES_B136_R0038")',
    'len(choices["choices"]) == 5': 'len(choices["choices"]) == 8',
    'file_path = "/data/SC0.DK4"': 'file_path = "/data/SC1.DK4"',
    '    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=16, revised_modal_pages=1,':
        '    style = base.load(STYLES)\n'
        '    assert style["candidate_sha256"] == candidate and style["stored_table_exact"]\n'
        '    assert style["current_native_body_rendering"] and len(style["records"]) == 5\n'
        '    for row in style["records"]:\n'
        '        ref = row["registered_reference"]\n'
        '        raw = bytes.fromhex(ref["exact_command_hex"])\n'
        '        start = ref["command_offset"]\n'
        '        assert all(row["review"].values()) and archive.blocks[123][start:start + len(raw)] == raw\n'
        '    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=8, revised_modal_pages=2,\n'
        '        style_proof_sha256=base.digest(STYLES), original_style_variants=style["records"],',
})

verify_source = checked_text(prior.verify_source, {
    'observed_count() == 50': 'observed_count() == 47',
    'native_count() == 32': 'native_count() == 23',
    'archives = {"/data/SC0.DK4"}': 'archives = {"/data/SC1.DK4"}',
    'len(records) == 275': 'len(records) == 293',
    'len(changed) == 31': 'len(changed) == 25',
    'sum(r["change_class"] == "prose" for r in changed) == 30': 'all(r["change_class"] == "prose" for r in changed)',
    '    assert [r["id"] for r in changed if r["change_class"] == "wrap_only"] == ["DK4_MES_B118_R0125"]\n': '',
    'wording_revisions=30, wrap_only_revisions=1': 'wording_revisions=25, wrap_only_revisions=0',
    'justified_retentions=244, choice_label_retentions=5': 'justified_retentions=268, choice_label_retentions=8',
    'base.load(FE)["sheets"]': 'base.load(FE)["sheets"] + base.load(STYLES)["sheets"]',
})

readme = prior.main[prior.main.index('    (PACKAGE / "README.md").write_text'):prior.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(prior.main, {
    "len(batches) == 1076 and len(checks) == 411": "len(batches) == 1077 and len(checks) == 412",
    "previously_localized_records=280, contextual_records_revisited=280":
        "previously_localized_records=306, contextual_records_revisited=306",
    "prior_records_reviewed=280": "prior_records_reviewed=306",
    "justified_retentions=244, retained_choice_labels=5":
        "justified_retentions=268, retained_choice_labels=8, retained_style_variants=5",
    "prose_revisions=30": "prose_revisions=25",
    "wrap_only_revisions=1": "wrap_only_revisions=0",
    "focused_initialized_Rafael=True, default_substitution_panels=2, retained_modal_pages=16, revised_modal_pages=1, native_choice_outcomes=5":
        "focused_initialized_Hodram=True, default_substitution_panels=1, retained_modal_pages=8, revised_modal_pages=2, native_choice_outcomes=8",
    "verified_hodram_early_and_midroute_predecessor": "verified_rafael_midroute_predecessor",
    "FE, CHOICE, ROLES)": "FE, CHOICE, ROLES, STYLES)",
    "FE, CHOICE, ROLES, args.visual_review,": "FE, CHOICE, ROLES, STYLES, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram's midroute follow-ups

The [testing ROM](../../{ROM.as_posix()}) includes the revised dialogue and both updated tutorial panels. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_midroute_exchanges", "hodram_midroute_followups").replace(
    '"hodram_midroute_followups_20261122", entry', '"hodram_midroute_followups_20261123", entry').replace(
    '"hodram_midroute_followups_20261122", 1', '"hodram_midroute_followups_20261123", 1')

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    '    excerpt_rom = Path(base.load(live.excerpt_scope["receipt"](0))["rom"])':
        '    excerpt_rom = live.route_rom(1)\n'
        '    prototype = stage.BATCH.parent / "first_staging" / "staged" / stage.ROM.name\n'
        '    prototype_receipt = base.load(prototype.with_name(stage.PROOF.name))\n'
        '    assert prototype_receipt["whole_parent_inverse"]\n'
        '    assert base.digest(prototype) == prototype_receipt["candidate_sha256"] != candidate',
    'earlier = [excerpt_rom,': 'earlier = [prototype, excerpt_rom,',
    'Preserve the Rafael midroute candidate, predecessor and focused ROMs':
        'Preserve Hodram midroute testing and prototype ROMs, predecessor and focused ROMs',
    '2026-11-22': '2026-11-23',
    old_doc:'''    DOC.write_text(f"""# Hodram's midroute follow-ups

The clean-Japanese review covers 306 texts in 13 complete exchanges. Twenty-five revisions address 17 flagged wraps and related wording or layout issues. The ledger records 268 prose or modal retentions, eight choice captions, five physical style variants and the exact fields for 18 names and roles. [Exact review](../{REVIEW.as_posix()})

All 23 changed progressive pages and 10 modal panels passed native checks, including the maximum-width Spirit notice. Focused emulator tests verified 47 displays and all eight original menu outcomes. The five retained style bodies and their eight slot assignments were checked offline. Ordinary story activation and handheld testing remain open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_midroute_exchanges", "hodram_midroute_followups")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for source in (controls, verify_source, main, commit):
    exec(compile(source, __file__ + "::signed-off-registration", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
