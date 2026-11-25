"""Register the one-slot Pirate label over the exact Online Card Copy release."""

from inspect import getsource
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_reference
from scripts import register_online_card_copy_20261123 as parent
from scripts import stage_pirate_affiliation_20261123 as stage
from scripts.probe_pirate_affiliation_20261123 import ENGLISH, JAPANESE, SLOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_pirate_panel_emulator_20261123 import REPORT as DISPLAY, STORED as PLAYBACK


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = parent.ARM, parent.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-pirate-affiliation-v1-20261123"
EVIDENCE = stage.ROOT
ROOT, WORK = EVIDENCE.parent / "registered", EVIDENCE.parent / "registration"
ROM = ROOT / "Translation_DS_Pirate_Affiliation_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_pirate_affiliation_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_pirate_affiliation_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = stage.STARTUP_CAPTURE
REBUILT, RESEARCH_PATCH = stage.REBUILT, stage.PATCH
CHECKPOINT = "Registered the Pirate affiliation label in the alternate battle panel."
guard_spec = parent.guard_spec
link_snapshot = parent.link_snapshot
startup_source = checked_text(getsource(startup_reference.startup_proof), {
    "original_ARM9_and_overlay_preserved=True": "only_pirate_affiliation_slot_changed=True, original_overlay_preserved=True",
})
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return 1


def observed_count():
    return 9


def verify(registry, previous, viewed):
    stored, displayed, playback = map(base.load, (stage.PROOF, DISPLAY, PLAYBACK))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == playback["candidate_sha256"] == base.digest(REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == displayed["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["exact_parent_inverse"] and displayed["complete_English_pixels_per_hold"] == 70
    assert not playback["label_overridden_in_memory"] and len(playback["exact_English_frame_matches"]) == 11
    assert viewed == {displayed["sheet"]["path"]: displayed["sheet"]["sha256"]}
    assert all(base.digest(p) == h for p, h in (viewed | stored["evidence"]).items())
    assert playback["display_receipt"]["sha256"] == base.digest(DISPLAY)
    assert playback["stored_proof"]["sha256"] == base.digest(stage.PROOF)
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    clean, old, new = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    end = SLOT + len(ENGLISH)
    assert source[ARM][SLOT:end] == before[ARM][SLOT:end] == JAPANESE
    assert after[ARM] == before[ARM][:SLOT] + ENGLISH + before[ARM][end:]
    assert stage.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    hashes = {path: native.digest(after[path]) for path in (ARM, COMMON, *routes.ROUTES)}
    assert hashes[ARM] == stored["target_ARM9_sha256"] and hashes[COMMON] == previous["target_COMMON_sha256"]
    new.replace_file(ARM, before[ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = parent.parent.bind_registered_story_percent_guard(guard)(source, after)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, after[ARM])

    previous_review = base.load(parent.REVIEW)
    binding = previous_review["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == previous_review["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == previous_review["retained_editorial_coverage_sha256"]
    route = base.load(routes.OUT)
    assert all(hashes[path] == route["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    result = dict(candidate_sha256=candidate, records=stored["records"], visual_review=viewed,
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=displayed["review_gates"], registered_consumer="Alternate battle affiliation nameplate",
        checked_story_format_guard=checks, shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), new_reviewed_UI_slots=1,
        focused_emulator_fixture=True, ordinary_battle_activation_or_exit_observed=False, hardware=False,
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


old_copy = parent.build[parent.build.index("    for source in (stage.PROOF"):parent.build.index("        filename = ")]
old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'parent.WORK / "release_stack_with_ending_credit_spacing.json"': 'parent.WORK / "release_stack_with_online_card_copy.json"',
    'verified_ending_credit_spacing_predecessor': 'verified_online_card_copy_predecessor',
    'len(batches) == 1097 and len(checks) == 432': 'len(batches) == 1098 and len(checks) == 433',
    'assert len(checks) == 433\n': 'assert len(checks) == 434\n',
    'changed_components=2': 'changed_components=1',
    'reviewed_UI_labels=0': 'reviewed_UI_labels=1',
    'previously_localized_records=2, contextual_records_revisited=2': 'previously_localized_records=0, contextual_records_revisited=1',
    'new_contextual_records=0, prose_revisions=2, spacing_revisions=0': 'new_contextual_records=1, prose_revisions=0, spacing_revisions=0',
    'text_display_revisions=2': 'text_display_revisions=1',
    'ordinary_online_guide=True': 'focused_battle_nameplate_fixture=True',
    'prior_records_reviewed=2, contextual_decisions_reused=0, observed_online_guide_holds':
        'new_reviewed_UI_slots=1, contextual_decisions_reused=0, observed_focused_battle_nameplate_holds',
    'prose_revisions=2, spacing_revisions=0, punctuation_glyph_corrections=0':
        'prose_revisions=0, spacing_revisions=0, punctuation_glyph_corrections=0, ui_label_revisions=1',
    '(playback.OUT, DISPLAY)': '(PLAYBACK, DISPLAY)',
    old_copy: '''    for source in (stage.PROOF, STARTUP, QA, PLAYBACK, DISPLAY, routes.OUT, audit.OUT, args.visual_review,
                   *(Path(p) for p in base.load(args.visual_review))):
''',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Pirate affiliation testing candidate

The [testing ROM](../../{ROM.as_posix()}) displays Pirate on the alternate battle nameplate. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("online_card_copy", "pirate_affiliation").replace(
    "verified_pirate_affiliation_predecessor", "verified_online_card_copy_predecessor").replace(
    'parent.WORK / "release_stack_with_pirate_affiliation.json"', 'parent.WORK / "release_stack_with_online_card_copy.json"')

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Online card wording candidate and its predecessor": "Preserve the Pirate affiliation candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Pirate affiliation label

The alternate battle nameplate displays **Pirate**. The six text bytes fit the original eight-byte slot. All nine visible panel holds show the complete label. A focused cold boot also matched the English fixture using the stored candidate bytes. Ordinary battle activation and exit remain unvisited. [Exact source and installed review](../{REVIEW.as_posix()})

The candidate's startup, both original name getters for each of the 12 protected actors, 17 repository checks and exact clean-input reconstruction passed. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("online_card_copy", "pirate_affiliation")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
