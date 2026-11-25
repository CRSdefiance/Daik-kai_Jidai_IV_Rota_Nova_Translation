"""Register the single-slot Tavern revision and its ordinary gameplay evidence."""

from pathlib import Path

from scripts import audit_current_editorial_coverage_20261123 as audit
from scripts import register_regional_rumor_wrap_followups_20261123 as parent
from scripts import stage_tavern_nearby_town_wrap_20261123 as stage
from scripts import verify_tavern_nearby_town_wrap_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes = stage.ARM, stage.COMMON, parent.routes
PROFILE = "all-routes-tavern-nearby-town-wrap-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Tavern_Nearby_Town_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_tavern_nearby_town_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_tavern_nearby_town_wrap_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL, DISCOVERY = EVIDENCE / "visual_review.json", stage.observed.OUT
CHECKPOINT = "Registered the Tavern’s nearby-town hint after ordinary Tunis and Syracuse replays."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_source = checked_text(parent.prior.startup_source, {
    "original_ARM9_and_overlay_preserved=False, only_COMMON_directory_and_offset_fields_changed=True":
        "original_ARM9_and_overlay_preserved=True, only_COMMON_dialogue_slot_changed=True",
})
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["native_town_cases"])


def observed_count():
    return base.load(live.LIVE)["revised_holds"]


def verify(registry, previous, viewed):
    stored, played = map(base.load, (stage.PROOF, live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == played["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and set(stored["allocations"]) == {str(stage.KEY)}
    assert stored["allocations"][str(stage.KEY)]["new_null_fields"] == 0
    assert viewed == base.load(VISUAL) == stored["sheets"] | played["sheets"]
    assert all(base.digest(p) == digest for evidence in (viewed, played["evidence"]) for p, digest in evidence.items())
    assert played["ordinary_battery_save_gameplay"] and played["revised_holds"] == 2 and played["menu_transitions"] == 4
    assert played["retained_holds"] == 8 and not played["revised_offline_only_records"]
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    clean, old, target = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(stage.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    first, final = map(native.files, (old, target))
    assert first.keys() == final.keys() and {path for path in first if first[path] != final[path]} == {COMMON}
    hashes = {path: native.digest(final[path]) for path in (ARM, COMMON)}
    assert hashes[ARM] == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert hashes[COMMON] == stored["target_COMMON_sha256"]
    target.replace_file(COMMON, first[COMMON])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean), final)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, final[ARM])

    prior_review = base.load(parent.REVIEW)
    prior_binding = prior_review["shared_consumer_binding"]
    get_entries = stage.observed.prior.shared.paired.prior.entries
    installed = get_entries(base.NdsImage.open(stage.ROM))
    earlier = get_entries(old)
    assert {before.message_id for before, after in zip(earlier, installed, strict=True) if before != after} == {stage.KEY}
    assert len(prior_binding["records"]) == 276
    shared_rows = []
    for row in prior_binding["records"]:
        key = row["message_ID"]
        assert installed[key] == earlier[key]
        reference = stage.town.reference(installed[key])
        assert reference == row["installed"]
        shared_rows.append(dict(message_ID=key, before=reference, installed=reference, exact_body_retained=True))
    shared_binding = dict(candidate_sha256=candidate, records=shared_rows, all_stored_bodies_preserved=True,
        changed_locations=[], earlier_binding_sha256=base.digest(parent.REVIEW), display_ownership_open=True)
    assert base.digest(routes.OUT) == prior_review["retained_four_route_census_sha256"]
    route = base.load(routes.OUT)
    assert all(native.digest(final[path]) == route["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    assert base.load(audit.OUT)["candidate_sha256"] == previous["candidate_sha256"]
    assert stored["inherited_observations_sha256"] == base.digest(DISCOVERY)

    rows = stored["records"]
    assert len(rows) == 9 and all(all(row["review"].values()) for row in rows)
    revised, = [row for row in rows if row["decision"] == "revision"]
    assert revised["message_ID"] == stage.KEY and revised["installed_hex"] == installed[stage.KEY].text.hex()
    assert all(case["complete_native_body"] for case in stored["native_town_cases"])
    assert len({case["town"] for case in stored["native_town_cases"]}) == 90
    revised["observed_changed_pages"] = [row for row in played["observed"]["tunis"] if row["message_ID"] == stage.KEY]
    result = dict(candidate_sha256=candidate, records=rows, checked_story_format_guard=checks,
        ordinary_tavern_dialogue=played, visual_review=viewed, prior_records_reviewed=9, wording_revisions=1,
        justified_retentions=8, native_town_variants=90, shared_consumer_binding=shared_binding,
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), full_editorial_goal_complete=False, hardware=False)
    return stored, result, hashes


def renamed(source):
    return source.replace("regional_rumor_wrap_followups", "tavern_nearby_town_wrap")


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    "len(batches) == 1088 and len(checks) == 423": "len(batches) == 1089 and len(checks) == 424",
    "assert len(checks) == 424\n": "assert len(checks) == 425\n",
    'parent.WORK / "release_stack_with_hodram_b261_b310_wrap_fixes.json"':
        'parent.WORK / "release_stack_with_regional_rumor_wrap_followups.json"',
    "verified_hodram_b261_b310_wrap_fixes_predecessor": "verified_regional_rumor_wrap_followups_predecessor",
    'source_bound_square_rumor_storage': 'source_bound_tavern_storage',
    'changed_internal_files=sorted(archives),\n        changed_components=2':
        'changed_internal_files=[COMMON],\n        changed_components=1',
    'previously_localized_records=21, contextual_records_revisited=21, contextual_decisions_reused=19':
        'previously_localized_records=9, contextual_records_revisited=9, contextual_decisions_reused=8',
    'prior_records_reviewed=21, contextual_decisions_reused=19, observed_ordinary_regional_rumors':
        'prior_records_reviewed=9, contextual_decisions_reused=8, observed_ordinary_tavern_holds',
    'prose_revisions=2, spacing_revisions=0': 'prose_revisions=1, spacing_revisions=0',
    'prose_revisions=2, punctuation_glyph_corrections=0': 'prose_revisions=1, punctuation_glyph_corrections=0',
    'justified_retentions=19, name_label_revisions=0, text_display_revisions=2':
        'justified_retentions=8, name_label_revisions=0, text_display_revisions=1',
    'justified_retentions=19, wrap_only_revisions=0': 'justified_retentions=8, wrap_only_revisions=0',
    'ordinary_Valencia_and_Syracuse=True': 'ordinary_Tunis_and_Syracuse=True',
    'DISCOVERY, routes.OUT, args.visual_review': 'DISCOVERY, routes.OUT, audit.OUT, args.visual_review',
    '    for src, target in ((EVIDENCE / "translation.xdelta", PATCH), (EVIDENCE / "clean_rebuilt.nds", ROM)):\n'
    '        copyfile(src, target)\n        assert base.digest(src) == base.digest(target)':
        '    copyfile(stage.PATCH, PATCH)\n'
        '    assert base.digest(stage.PATCH) == base.digest(PATCH)\n'
        '    link_snapshot(stage.REBUILT, ROM, candidate)',
    'changed_component_hashes=archives': 'changed_component_hashes={COMMON: archives[COMMON]}',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tavern nearby-town wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reflowed Tavern question. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    'Preserve the regional rumor candidate and its predecessor': 'Preserve the Tavern candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Tavern nearby-town hint

The barkeep now asks “Have you heard of a nearby town called %s?” The native formatter keeps the place name and question mark together across all 90 stock towns. The review retains eight alternate or surrounding lines with individual reasons. [Exact source and installed review](../{REVIEW.as_posix()})

Both ordinary Tunis holds show the complete revised question. Syracuse verifies two alternate people, towns and roles. Both ports preserve the drink menu and its return transition. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
