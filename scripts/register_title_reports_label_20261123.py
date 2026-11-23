"""Register the title Options label and the paired confirmation evidence."""

from pathlib import Path

from scripts import register_square_and_market_reward_wraps_20261123 as parent
from scripts import stage_title_reports_label_20261123 as stage
from scripts import verify_title_reports_label_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-title-reports-label-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Title_Reports_Label_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_title_reports_label_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_title_reports_label_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = live.HISTORICAL
CHECKPOINT = "Registered the Reports label and verified the title Options controls."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_source = checked_text(parent.parent.startup_source, {
    "original_ARM9_and_overlay_preserved=True, only_COMMON_dialogue_slot_changed=True":
        "only_title_Options_label_changed=True",
})
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return 3


def observed_count():
    replay = base.load(live.LIVE)
    return len(replay["options_holds"]) + len(replay["toggle_holds"])


def verify(registry, previous, viewed):
    stored, replay = map(base.load, (stage.PROOF, live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == replay["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == replay["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and viewed == base.load(VISUAL) == replay["sheets"]
    assert all(base.digest(p) == sha for evidence in (viewed, replay["evidence"]) for p, sha in evidence.items())
    assert replay["ordinary_title_options"] and replay["sound_meters_restored"]
    assert len(replay["options_holds"]) == 10 and len(replay["toggle_holds"]) == 6
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    clean, old, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    first, final = map(native.files, (old, target))
    assert first.keys() == final.keys() and {path for path in first if first[path] != final[path]} == {ARM}
    hashes = {path: native.digest(final[path]) for path in (ARM, COMMON)}
    assert hashes[COMMON] == previous["target_COMMON_sha256"] == stored["target_COMMON_sha256"]
    assert hashes[ARM] == stored["target_ARM9_sha256"]
    arm, selections = stage.reviewed_slot(clean.read_file(ARM), first[ARM])
    assert arm == final[ARM] and selections == stored["native_title_menu_selections"]
    target.replace_file(ARM, first[ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean), final)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, arm)

    prior_review = base.load(parent.REVIEW)
    binding = prior_review["shared_consumer_binding"]
    read_entries = parent.parent.stage.observed.prior.shared.paired.prior.entries
    installed, predecessor = map(read_entries, (base.NdsImage.open(stage.ROM), old))
    assert installed == predecessor and len(installed) == 3668 and len(binding["records"]) == 276
    for row in binding["records"]:
        assert row["installed"] == stage.town.reference(installed[row["message_ID"]])
    shared_binding = binding | dict(candidate_sha256=candidate, earlier_binding_sha256=base.digest(parent.REVIEW))
    assert base.digest(routes.OUT) == prior_review["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == prior_review["retained_editorial_coverage_sha256"]
    route = base.load(routes.OUT)
    assert all(native.digest(final[path]) == route["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    revised = stored["record"] | dict(source_reference=selections[0][1], current_reference=selections[1][1],
        installed_reference=selections[2][1], review=dict.fromkeys(stage.town.GATES, True))
    revised["installed_reference"].update(candidate_sha256=candidate, ARM9_sha256=hashes[ARM])
    rows = [revised, *replay["prompt_retentions"]]
    assert len(rows) == 5 and all(all(row["review"].values()) for row in rows)
    return stored, dict(candidate_sha256=candidate, records=rows, checked_story_format_guard=checks,
        options_dialogue=replay, visual_review=viewed, prior_records_reviewed=5, label_revisions=1,
        justified_retentions=4, native_title_descriptors=3, shared_consumer_binding=shared_binding,
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), full_editorial_goal_complete=False, hardware=False), hashes


def renamed(source):
    return source.replace("square_and_market_reward_wraps", "title_reports_label")


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    'len(batches) == 1090 and len(checks) == 425': 'len(batches) == 1091 and len(checks) == 426',
    'assert len(checks) == 426\n': 'assert len(checks) == 427\n',
    'parent.WORK / "release_stack_with_tavern_nearby_town_wrap.json"':
        'parent.WORK / "release_stack_with_square_and_market_reward_wraps.json"',
    'verified_tavern_nearby_town_wrap_predecessor': 'verified_square_and_market_reward_wraps_predecessor',
    "source_bound_square_and_market_storage=stored['allocations']": "source_bound_title_options_slot=stored['record']",
    'changed_component_hashes={COMMON: archives[COMMON]}': 'changed_component_hashes={ARM: archives[ARM]}',
    'changed_internal_files=[COMMON]': 'changed_internal_files=[ARM]',
    'reviewed_UI_labels=0': 'reviewed_UI_labels=3',
    'previously_localized_records=27, contextual_records_revisited=27, contextual_decisions_reused=25':
        'previously_localized_records=5, contextual_records_revisited=5, contextual_decisions_reused=4',
    'prior_records_reviewed=27, contextual_decisions_reused=25, observed_focused_square_and_market_holds':
        'prior_records_reviewed=5, contextual_decisions_reused=4, observed_title_options_holds',
    'prose_revisions=2, spacing_revisions=0': 'prose_revisions=0, spacing_revisions=0',
    'prose_revisions=2, punctuation_glyph_corrections=0': 'prose_revisions=0, punctuation_glyph_corrections=0, ui_label_revisions=1',
    'justified_retentions=25, name_label_revisions=0, text_display_revisions=2':
        'justified_retentions=4, name_label_revisions=0, text_display_revisions=1',
    'justified_retentions=25, wrap_only_revisions=0': 'justified_retentions=4, wrap_only_revisions=0',
    'focused_square_and_market=True': 'ordinary_title_options=True',
    'live.LIVE, DISCOVERY, routes.OUT': 'live.LIVE, live.BASELINE_DRIVER, DISCOVERY, routes.OUT',
    'assert all((row["file_path"], aliases.get(row["id"], row["id"])) in credited for row in draft["records"])':
        'assert all(row["file_path"] == ARM for row in draft["records"])',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Title Options testing candidate

The [testing ROM](../../{ROM.as_posix()}) uses Reports in the title Options menu. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    'Preserve the Square and Market candidate and its predecessor': 'Preserve the title Options candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Title Options reports

The title Options menu now uses **Reports**, matching the confirmation and in-game label. The review retains Sound, Sailing Help and both confirmation templates with individual reasons. The original menu descriptor, choice order and setting handlers are unchanged. [Exact review](../{REVIEW.as_posix()})

Paired ordinary title replays verified the full label in ten menu holds. Six complete confirmation holds show both state orders and preserve cancellation. Twenty offline preference cases checked both choices and unrelated bits. The controls restored both volume meters and returned to the title. COMMON 102 and 330–333 still await evidence for any separate callers. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
