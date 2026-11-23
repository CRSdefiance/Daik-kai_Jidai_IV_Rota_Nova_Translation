"""Register the tested late Hodram dialogue batch and clean-input patch."""

from pathlib import Path
from types import FunctionType

from scripts import register_hodram_late_midroute_wraps_20261123 as parent
from scripts import stage_hodram_late_story_wraps_20261123 as stage
from scripts import verify_hodram_late_story_wraps_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-hodram-late-story-wraps-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Hodram_Late_Story_Wraps_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_hodram_late_story_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_late_story_wraps_registered_20261123.md")
DISPLAY, EVIDENCE, FE = stage.NATIVE, stage.ROOT, stage.FE_PROOF
GLYPHS, CHOICE, ROLES, STYLES = live.GLYPHS, live.CHOICES, live.ROLES, live.STYLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram's town rumors, bargaining scenes, and late story wrap follow-ups."
RUNS = ("route1", *live.RUNS)
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, choice, roles, styles = map(base.load, (FE, CHOICE, ROLES, STYLES))
    assert all(evidence["candidate_sha256"] == candidate for evidence in (modal, choice, roles, styles))
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 17
    panels = {row["id"]:row for row in records if row["kind"] == "system"}
    for panel in modal["records"]:
        row = panels.pop(panel["id"])
        ref = row["registered_reference"]
        assert row["decision"] == "retention" and not panel["second_page"]
        assert ref["command_offset"] == panel["stored_offset"]
        assert ref["exact_command_hex"] == panel["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
    assert not panels
    assert choice["stored_tables_exact"] and len(choice["choices"]) == 22 and len(played["original_menu_choices"]) == 3
    draft = {row["id"]:row for row in base.load(stage.REVIEW)["retained_choice_labels"]}
    branches = {row["slot"]:row for row in played["original_menu_choices"]}
    archive_hash = base.load(stage.PROOF)["archive_hashes"][stage.ARCHIVE]
    captions = []
    for label in choice["choices"]:
        row = draft.pop(label["id"])
        block = label["block"]
        payload = banks[stage.ARCHIVE].blocks[block]
        observed = None
        if block == 216 and label["command_word"] == 0x2200:
            observed = branches.pop(label["slot"])
            assert observed["original_branch_executed"] and observed["block"] == block
            assert label["caption"] == observed["caption"]
        assert row["english"] == label["caption"]
        original, offset = row["current_reference"], label["offset"]
        at = offset - original["offset"] + original["command_offset"]
        raw, body = (bytes.fromhex(original[key]) for key in ("exact_command_hex", "exact_body_hex"))
        assert raw.hex() == label["exact_command_hex"] and payload[at:at+len(raw)] == raw
        assert payload[offset:offset+len(body)+1] == body + b"\x00"
        ref = original | dict(candidate_sha256=candidate, archive_sha256=archive_hash,
            block_sha256=native.digest(payload), command_offset=at, offset=offset)
        captions.append(row | dict(registered_reference=ref, observed_focused=observed,
            review=row["review"] | {"formatting":True}))
    assert not draft and not branches
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    assert {row["actor_ID"] for row in roles["records"]} == live.NOTES.keys()
    assert all(all(row["review"].values()) for row in roles["records"])
    assert styles["stored_table_exact"] and len(styles["records"]) == 7
    assert all(all(row["review"].values()) for row in styles["records"])
    return dict(retained_modal_pages=17, retained_choice_labels=captions, retained_supporting_roles=25,
        retained_style_variants=styles["records"], modal_proof_sha256=base.digest(FE), choice_proof_sha256=base.digest(CHOICE),
        role_proof_sha256=base.digest(ROLES), style_proof_sha256=base.digest(STYLES))


scene_check = parent.verify_source[parent.verify_source.index('    lesson, ='):parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 39': 'observed_count() == 31',
    'native_count() == 25': 'native_count() == 22',
    'len(records) == 494': 'len(records) == 259',
    'len(changed) == 25': 'len(changed) == 22',
    'for r in changed) == 24': 'for r in changed) == 22',
    'for r in changed) == 1': 'for r in changed) == 0',
    'set(manuscript["wrap_leads_covered"]) <=': 'set(manuscript["wrap_leads_covered"]) ==',
    scene_check:'''    signature, = [row for row in changed if row["id"] == "DK4_MES_B218_R0068"]
    assert signature["display_proof"]["layouts"][0]["lines"][-1] == "Janus Pasar"
''',
    'wording_revisions=24, wrap_only_revisions=1': 'wording_revisions=22, wrap_only_revisions=0',
    'justified_retentions=469, choice_label_retentions=2': 'justified_retentions=237, choice_label_retentions=22',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    'len(batches) == 1083 and len(checks) == 418': 'len(batches) == 1084 and len(checks) == 419',
    'assert len(checks) == 419': 'assert len(checks) == 420',
    'verified_rafael_remaining_wraps_predecessor': 'verified_active_predecessor',
    'previously_localized_records=496, contextual_records_revisited=496, contextual_decisions_reused=471':
        'previously_localized_records=288, contextual_records_revisited=288, contextual_decisions_reused=266',
    'prior_records_reviewed=496, contextual_decisions_reused=471': 'prior_records_reviewed=288, contextual_decisions_reused=266',
    'justified_retentions=469, retained_choice_labels=2': 'justified_retentions=237, retained_choice_labels=22, retained_style_variants=7',
    'prose_revisions=24': 'prose_revisions=22',
    'wrap_only_revisions=1': 'wrap_only_revisions=0',
    'retained_modal_pages=50, revised_modal_pages=0, native_choice_outcomes=2':
        'retained_modal_pages=17, revised_modal_pages=0, native_choice_outcomes=3',
    'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES':
        'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES, STYLES',
    'DISPLAY, GLYPHS, FE, CHOICE, ROLES, args.visual_review': 'DISPLAY, GLYPHS, FE, CHOICE, ROLES, STYLES, args.visual_review',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram's late story wrap follow-ups

The [testing ROM](../../{ROM.as_posix()}) includes the revised late Hodram exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_late_midroute_wraps", "hodram_late_story_wraps").replace(
    "verified_active_predecessor", "verified_hodram_late_midroute_wraps_predecessor")

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'live.choice_paths(167)': 'live.choice_paths(216)',
    old_doc:'''    DOC.write_text(f"""# Hodram's late story wrap follow-ups

Seventeen complete exchanges reconcile 288 exact source and installed texts. Twenty-two wording revisions address the 22 scan leads. The ledger records 237 speech or panel retentions, 22 retained choice captions and seven original personality variants. [Exact review](../{REVIEW.as_posix()})

All 22 revised pages, 17 speakerless commands and 25 names or roles passed native checks. Focused emulator replays verified 31 holds, all three original commander-choice outcomes and the retained two-page Zhuge Liang response. Other conditional outcomes and ordinary scene activation remain unvisited. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_late_midroute_wraps", "hodram_late_story_wraps")

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
