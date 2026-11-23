"""Register the four verified ending-credit spacing corrections."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_tavern_drink_reply_20261123 as parent
from scripts import stage_ending_credit_spacing_20261123 as stage
from scripts import stage_rafael_deck_tutorial_followup_20261122 as release_tools
from scripts import verify_ending_credit_spacing_20261123 as playback
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = parent.ARM, parent.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-ending-credit-spacing-v1-20261123"
EVIDENCE = stage.ROOT
ROOT, WORK = EVIDENCE / "registered", EVIDENCE / "registration"
ROM = ROOT / "Translation_DS_Ending_Credit_Spacing_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_ending_credit_spacing_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_ending_credit_spacing_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
DISPLAY = stage.PROOF
REBUILT, RESEARCH_PATCH = EVIDENCE / "clean_rebuilt.nds", EVIDENCE / "translation.xdelta"
CHECKPOINT = "Registered the spacing correction in all four ending credit lines."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["records"])


def observed_count():
    return sum(len(row["exact_full_upper_credit_holds"]) for row in base.load(playback.OUT)["records"])


def verify(registry, previous, viewed):
    stored, played, earlier = map(base.load, (stage.PROOF, playback.OUT, parent.REVIEW))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["exact_parent_inverse"] and played["actual_focused_playback"] and not played["earned_route_completion"]
    assert viewed == {played["sheet"]["path"]: played["sheet"]["sha256"]}
    assert all(base.digest(path) == digest for path, digest in (viewed | played["evidence"]).items())
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, first, last = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, first, last))
    assert before.keys() == after.keys()
    captures = {row["id"]: row for row in played["records"]}
    changes = {path for path in before if before[path] != after[path]}
    assert changes == set(stored["changed_files"]) == {row["file_path"] for row in stored["records"]}
    hashes = {path: native.digest(after[path]) for path in changes | {ARM, COMMON}}
    assert hashes[ARM] == previous["target_ARM9_sha256"] and hashes[COMMON] == previous["target_COMMON_sha256"]
    rows = []
    for row in stored["records"]:
        path, index = row["file_path"], row["texture_index"]
        assert source[path] == before[path]
        expected, layout = stage.replace_credit(source[path], index)
        assert expected == after[path] and layout == row["layout"]
        assert hashes[path] == row["installed_reference"]["archive_sha256"]
        observed = captures[row["id"]]
        assert observed["texture_index"] == index and observed["first_opaque"]["original_gray_level"] == 31
        rows.append(row | dict(review=dict(row["review"], formatting=True), observed=observed))
    assert len(rows) == 4 and len(captures) == 4
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checked_source = bind_registered_story_percent_guard(guard)(source, after)
    assert checked_source["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, after[ARM])
    binding = earlier["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == earlier["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == earlier["retained_editorial_coverage_sha256"]
    route = base.load(routes.OUT)
    assert all(native.digest(after[path]) == route["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    result = dict(candidate_sha256=candidate, records=rows, visual_review=viewed,
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(rows[0]["review"]), registered_consumer="FLS fixed-slot bitmap credit",
        checked_story_format_guard=checked_source, shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT),
        retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), full_editorial_goal_complete=False,
        actual_focused_ending_playback=True, ordinary_earned_ending=False, hardware=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


retained_guard = 'assert all((row["file_path"], aliases.get(row["id"], row["id"])) in credited for row in draft["records"])'
copies_start = parent.build.index("    for source in (stage.PROOF")
copies_end = parent.build.index("        filename = ", copies_start)
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "parent.WORK / \"release_stack_with_cabin_square_wrap.json\"": 'parent.WORK / "release_stack_with_tavern_drink_reply.json"',
    "verified_cabin_square_predecessor": "verified_tavern_drink_reply_predecessor",
    "stage.PATCH": "RESEARCH_PATCH",
    "stage.REBUILT": "REBUILT",
    parent.build[copies_start:copies_end]: '''    for source in (stage.PROOF, STARTUP, QA, playback.OUT, routes.OUT, audit.OUT, args.visual_review,
                   *(Path(p) for p in base.load(args.visual_review))):
''',
    "len(batches) == 1095 and len(checks) == 430": "len(batches) == 1096 and len(checks) == 431",
    "assert len(checks) == 431\n": "assert len(checks) == 432\n",
    'if r["decision"] == "revision" and r["id"] not in changed[r["file_path"]]:':
        'if r["decision"] == "revision" and r["id"] not in changed.setdefault(r["file_path"], []):',
    "live.LIVE, DISPLAY": "playback.OUT, DISPLAY",
    "changed_component_hashes={COMMON: archives[COMMON]}, source_bound_tavern_drink_reply_storage=stored['allocations']":
        'changed_component_hashes={path: archives[path] for path in stored["changed_files"]}',
    "changed_internal_files=[COMMON],\n        changed_components=1":
        'changed_internal_files=stored["changed_files"],\n        changed_components=4',
    "previously_localized_records=11, contextual_records_revisited=11, contextual_decisions_reused=10":
        "previously_localized_records=0, contextual_records_revisited=4, contextual_decisions_reused=0",
    "prose_revisions=1, spacing_revisions=0": "prose_revisions=0, spacing_revisions=4",
    "prose_revisions=1, punctuation_glyph_corrections=0": "prose_revisions=0, spacing_revisions=4, punctuation_glyph_corrections=0",
    "text_display_revisions=1": "text_display_revisions=4",
    "justified_retentions=10": "justified_retentions=0",
    "ordinary_istanbul_tavern=True": "focused_four_ending_movies=True",
    "prior_records_reviewed=11, contextual_decisions_reused=10, observed_ordinary_istanbul_holds":
        "prior_records_reviewed=4, contextual_decisions_reused=0, observed_focused_credit_holds",
    retained_guard: 'assert {row["file_path"] for row in draft["records"]} == set(stored["changed_files"]) and not aliases',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Ending credit spacing testing candidate

The [testing ROM](../../{ROM.as_posix()}) corrects the credit line in all four endings. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("tavern_drink_reply", "ending_credit_spacing").replace(
    "verified_ending_credit_spacing_predecessor", "verified_tavern_drink_reply_predecessor").replace(
    'parent.WORK / "release_stack_with_ending_credit_spacing.json"',
    'parent.WORK / "release_stack_with_tavern_drink_reply.json"')

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Istanbul Tavern candidate and its predecessor":
        "Preserve the ending credit spacing candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Ending credit spacing

All four endings now read **Special Thanks: BRIDGE Inc.** The rendered correction moves the original glyphs for “Thanks” by one character cell. The original attribution, full lettering, card dimensions, palette, and position carry forward with the existing credit fades. [Exact source and installed review](../{REVIEW.as_posix()})

Four focused cold boots entered the original ending selector through its one-byte state fixture. Each verified the full credit through several fade states and the following ending-save prompt. Earned completion and handheld display remain open. The 276 stored shared display entries and the separate graphics artwork remain in scope. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("tavern_drink_reply", "ending_credit_spacing")

scope = parent.scope | globals()
for source_code in (build, commit):
    exec(compile(source_code, __file__ + "::registration", "exec"), scope)


def resume_verified_assets():
    """Continue after an interrupted manifest write using the sealed release inputs."""
    previous, stored, draft = map(base.load, (parent.RELEASE, stage.PROOF, REVIEW))
    candidate = stored["candidate_sha256"]
    assert candidate == draft["candidate_sha256"] == base.digest(ROM) == base.digest(stage.ROM)
    assert ROM.samefile(REBUILT)
    assert base.digest(PATCH) == base.digest(RESEARCH_PATCH)
    assert all(base.digest(path) == digest for path, digest in draft["visual_review"].items())
    validate_natural_dialogue_batch(draft)
    snapshots = dict(registry=base.REGISTRY, ledger=base.LEDGER, main=base.PROMOTED)
    snapshot = {key + ("_sha256" if key == "main" else "_before"): base.digest(path)
                for key, path in snapshots.items()}
    assert previous["registry_sha256"] == snapshot["registry_before"]
    registry_backup, registry_next = (
        WORK / f"release_stack_{form}_ending_credit_spacing.json" for form in ("before", "with"))
    ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"
    assert base.digest(registry_backup) == snapshot["registry_before"]
    assert base.digest(ledger_backup) == snapshot["ledger_before"]
    assert not any(path.exists() for path in (VERIFY / "registration_mutation_plan.json", ledger_next, DOC))
    with scope["mapped"](registry_next) as data:
        profile = scope["value"](data, PROFILE, 4)
    registry_sha = base.digest(registry_next)
    predecessor = profile["verified_tavern_drink_reply_predecessor"]
    assert predecessor["registry"] == str(registry_backup)
    assert all(previous[key] == value for key, value in predecessor.items() if key != "registry")
    archives = {row["file_path"]: row["installed_reference"]["archive_sha256"] for row in draft["records"]}
    archives.update({ARM: previous["target_ARM9_sha256"], COMMON: previous["target_COMMON_sha256"]})
    assert stored["changed_files"] == list(archives)[:4]
    assert all(base.digest(VERIFY / source.name) == base.digest(source)
               for source in (stage.PROOF, STARTUP, QA, playback.OUT, playback.SHEET))
    assert MANIFEST.exists()
    try:
        base.load(MANIFEST)
    except ValueError:
        moved = EVIDENCE / "interrupted_partial_manifest.json"
        assert not moved.exists()
        MANIFEST.rename(moved)
    else:
        raise ValueError("The prepared manifest is complete. Check its release transaction before resuming.")
    start = build.index("    with mapped(parent.MANIFEST) as data:")
    inputs = ("snapshot", "previous", "stored", "draft", "candidate", "archives", "predecessor",
              "registry_sha", "registry_backup", "registry_next", "ledger_backup", "ledger_next")
    header = "def finish(" + ", ".join(inputs) + "):\n"
    env = scope.copy()
    exec(compile(header + build[start:], __file__ + "::finish-verified-assets", "exec"), env)
    prepared = locals()
    env["finish"](*(prepared[key] for key in inputs))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2 and sys.argv[1] in ("patch", "startup"):
        step = getattr(release_tools, sys.argv[1])
        settings = dict(base=base, native=native, parent=parent, PROOF=stage.PROOF, ROM=stage.ROM,
            PATCH=RESEARCH_PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
        FunctionType(step.__code__, step.__globals__ | settings)()
    elif sys.argv[1:] == ["--resume-verified-assets"]:
        resume_verified_assets()
    else:
        scope["main"]()
