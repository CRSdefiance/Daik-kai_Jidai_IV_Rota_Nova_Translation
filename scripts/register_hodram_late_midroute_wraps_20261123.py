"""Register the verified Hodram wrap follow-ups and exact clean-input patch."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_remaining_wraps_20261123 as parent
from scripts import stage_hodram_late_midroute_wraps_20261123 as stage
from scripts import verify_hodram_late_midroute_wraps_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-hodram-late-midroute-wraps-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Hodram_Late_Midroute_Wraps_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_hodram_late_midroute_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_late_midroute_wraps_registered_20261123.md")
DISPLAY, EVIDENCE, FE = stage.NATIVE, stage.ROOT, stage.FE_PROOF
GLYPHS, CHOICE, ROLES = live.GLYPHS, live.CHOICES, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram's late midroute wraps, including Cesare's ship lesson and the Silla Gold Crown exchanges."
RUNS = ("route1", *live.RUNS)
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, choice, roles = map(base.load, (FE, CHOICE, ROLES))
    assert all(evidence["candidate_sha256"] == candidate for evidence in (modal, choice, roles))
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 50
    panels = {row["id"]: row for row in records if row["kind"] == "system"}
    for panel in modal["records"]:
        row = panels.pop(panel["id"])
        ref = row["registered_reference"]
        assert row["decision"] == "retention" and not panel["second_page"]
        assert ref["command_offset"] == panel["stored_offset"]
        assert ref["exact_command_hex"] == panel["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
    assert not panels
    assert choice["stored_tables_exact"] and len(choice["choices"]) == len(played["original_menu_choices"]) == 2
    payload = banks[stage.ARCHIVE].blocks[167]
    draft = {row["id"]: row for row in base.load(stage.REVIEW)["retained_choice_labels"]}
    branches = {row["slot"]: row for row in played["original_menu_choices"]}
    archive_hash = base.load(stage.PROOF)["archive_hashes"][stage.ARCHIVE]
    captions = []
    for label in choice["choices"]:
        row, observed = draft.pop(label["id"]), branches.pop(label["slot"])
        assert observed["original_branch_executed"] and label["block"] == observed["block"] == 167
        assert row["english"] == label["caption"] == observed["caption"]
        original, offset = row["current_reference"], label["offset"]
        at = offset - original["offset"] + original["command_offset"]
        raw, body = (bytes.fromhex(original[k]) for k in ("exact_command_hex", "exact_body_hex"))
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
    return dict(retained_modal_pages=50, retained_choice_labels=captions, retained_supporting_roles=24,
        modal_proof_sha256=base.digest(FE), choice_proof_sha256=base.digest(CHOICE), role_proof_sha256=base.digest(ROLES))


scene_checks = parent.verify_source[parent.verify_source.index('    lucia, ='):parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 20': 'observed_count() == 39',
    'native_count() == 19': 'native_count() == 25',
    'live.scope["report_path"](int(run))': 'live.report(run)',
    'archives = {"/data/SC0.DK4"}': 'archives = {stage.ARCHIVE}',
    'len(records) == 335': 'len(records) == 494',
    'len(changed) == 19': 'len(changed) == 25',
    'for r in changed) == 18': 'for r in changed) == 24',
    'set(manuscript["wrap_leads_covered"]) ==': 'set(manuscript["wrap_leads_covered"]) <=',
    scene_checks:'''    lesson, = [row for row in changed if row["id"] == "DK4_MES_B167_R0145"]
    assert lesson["display_proof"]["layouts"][0]["lines"][-1] == "but you'll need more sail handlers."
''',
    'stage.checkpoint.QUEUE': 'stage.paired.QUEUE',
    'wording_revisions=18': 'wording_revisions=24',
    'justified_retentions=316, choice_label_retentions=0': 'justified_retentions=469, choice_label_retentions=2',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    'len(batches) == 1082 and len(checks) == 417': 'len(batches) == 1083 and len(checks) == 418',
    'assert len(checks) == 418': 'assert len(checks) == 419',
    'verified_rafael_mediterranean_followups_predecessor': 'verified_active_predecessor',
    'previously_localized_records=335, contextual_records_revisited=335, contextual_decisions_reused=316':
        'previously_localized_records=496, contextual_records_revisited=496, contextual_decisions_reused=471',
    'prior_records_reviewed=335, contextual_decisions_reused=316': 'prior_records_reviewed=496, contextual_decisions_reused=471',
    'justified_retentions=316, retained_choice_labels=0': 'justified_retentions=469, retained_choice_labels=2',
    'prose_revisions=18': 'prose_revisions=24',
    'focused_initialized_Rafael=True, default_substitution_panels=0, retained_modal_pages=4, revised_modal_pages=0, native_choice_outcomes=0':
        'focused_initialized_Hodram=True, default_substitution_panels=1, retained_modal_pages=50, revised_modal_pages=0, native_choice_outcomes=2',
    'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, ROLES': 'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES',
    'DISPLAY, GLYPHS, FE, ROLES, args.visual_review': 'DISPLAY, GLYPHS, FE, CHOICE, ROLES, args.visual_review',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram's late midroute wrap follow-ups

The [testing ROM](../../{ROM.as_posix()}) includes the revised Hodram exchanges and Cesare's ship lesson. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_remaining_wraps", "hodram_late_midroute_wraps").replace(
    "verified_active_predecessor", "verified_rafael_remaining_wraps_predecessor")

pins = parent.commit[parent.commit.index("    excerpt_rom = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    excerpt_rom = live.route_rom(1)
    choice_rom = live.choice_paths(167)[1]
    earlier = [excerpt_rom, choice_rom]
    assert base.digest(excerpt_rom) == base.load(excerpt_rom.with_name("fixture.json"))["fixture_sha256"]
    assert base.digest(choice_rom) == base.load(live.choice_paths(167)[2])["rom_sha256"]
''',
    'Preserve the remaining Rafael wrap candidate, predecessor and focused ROMs':
        'Preserve the Hodram wrap candidate, predecessor and focused ROMs',
    old_doc:'''    DOC.write_text(f"""# Hodram's late midroute wrap follow-ups

Fifteen complete exchanges reconcile 496 clean and installed texts. Twenty-four wording changes and one wrap-only change address 20 scan leads and five nearby wording issues. The ledger carries forward 469 speech or panel decisions and two retained choice captions. [Exact review](../{REVIEW.as_posix()})

All 25 revised pages, 50 retained speakerless commands and 24 names or roles passed native checks. Focused emulator replays verified 39 holds and both original outcomes of Cesare's ship lesson. Ordinary scene activation and handheld display remain open for these scenes. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_remaining_wraps", "hodram_late_midroute_wraps")

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
