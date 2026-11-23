"""Register the two verified PXL text revisions over the ending-credit release."""

from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_ending_credit_spacing_20261123 as parent
from scripts import replay_online_card_copy_20261123 as playback
from scripts import stage_online_card_copy_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = parent.ARM, parent.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-online-card-copy-v1-20261123"
EVIDENCE = stage.ROOT
ROOT, WORK = EVIDENCE / "registered", EVIDENCE / "registration"
ROM = ROOT / "Translation_DS_Online_Card_Copy_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_online_card_copy_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_online_card_copy_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = playback.STARTUP_CAPTURE
REBUILT, RESEARCH_PATCH, DISPLAY = playback.REBUILT, playback.PATCH, stage.review.OUT
CHECKPOINT = "Registered the Online ship and world card wording corrections."
guard_spec = parent.guard_spec
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["records"])


def observed_count():
    return sum(1 + len(r["same_revised_text_with_other_slides"]) for r in base.load(playback.OUT)["records"].values())


def verify(registry, previous, viewed):
    stored, played, earlier = map(base.load, (stage.PROOF, playback.OUT, parent.REVIEW))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == base.digest(parent.ROM)
    assert base.digest(native.CLEAN) == stored["clean_sha256"] == previous["clean_input_sha256"]
    assert stored["exact_parent_inverse"] and played["ordinary_controller_replay"] and not played["COMMON_requests"]
    assert played["exact_unchanged_neighbor"] and played["exact_title_return"]
    assert viewed == {played["sheet"]["path"]: played["sheet"]["sha256"],
        stored["preview"]["path"]: stored["preview"]["sha256"]}
    assert all(base.digest(path) == digest for path, digest in (viewed | played["evidence"] | stored["evidence"]).items())
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    clean, first, last = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, first, last))
    assert before.keys() == after.keys()
    changes = {p for p in before if before[p] != after[p]}
    assert len(changes) == 2 and changes == set(stored["changed_files"]) == played["records"].keys()
    hashes = {p: native.digest(after[p]) for p in changes | {ARM, COMMON}}
    assert hashes[ARM] == previous["target_ARM9_sha256"] and hashes[COMMON] == previous["target_COMMON_sha256"]
    rows = []
    for row in stored["records"]:
        path, manifest = row["file_path"], Path(row["manuscript"])
        assert base.digest(manifest) == row["manuscript_sha256"]
        expected, keys = stage.apply_pxl_label_batches([manifest], source[path])
        assert keys == [row["id"]] and expected == after[path]
        assert native.digest(before[path]) == row["current_reference"]["file_sha256"]
        assert hashes[path] == row["installed_reference"]["file_sha256"]
        live = played["records"][path]
        assert live["exact_RGB_outside_changed_text_art"] and not live["two_pages"]
        rows.append(row | dict(review=dict(row["review"], formatting=True), observed=live))
    assert len(rows) == native_count() == 2 and observed_count() == 5
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = parent.bind_registered_story_percent_guard(guard)(source, after)
    assert checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, after[ARM])
    binding = earlier["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == earlier["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == earlier["retained_editorial_coverage_sha256"]
    route = base.load(routes.OUT)
    assert all(native.digest(after[path]) == route["routes"][path]["installed_archive_sha256"] for path in routes.ROUTES)
    result = dict(candidate_sha256=candidate, records=rows, visual_review=viewed,
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(rows[0]["review"]), registered_consumer="Online guide PXL cards",
        checked_story_format_guard=checks, shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT),
        retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), full_editorial_goal_complete=False,
        ordinary_online_menu_controller_replay=True, hardware=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


old_copy = parent.build[parent.build.index("    for source in (stage.PROOF"):parent.build.index("        filename = ")]
old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'parent.WORK / "release_stack_with_tavern_drink_reply.json"': 'parent.WORK / "release_stack_with_ending_credit_spacing.json"',
    'verified_tavern_drink_reply_predecessor': 'verified_ending_credit_spacing_predecessor',
    'len(batches) == 1096 and len(checks) == 431': 'len(batches) == 1097 and len(checks) == 432',
    'assert len(checks) == 432\n': 'assert len(checks) == 433\n',
    'changed_components=4': 'changed_components=2',
    'previously_localized_records=0, contextual_records_revisited=4': 'previously_localized_records=2, contextual_records_revisited=2',
    'new_contextual_records=0, prose_revisions=0, spacing_revisions=4': 'new_contextual_records=0, prose_revisions=2, spacing_revisions=0',
    'text_display_revisions=4': 'text_display_revisions=2',
    'focused_four_ending_movies=True': 'ordinary_online_guide=True',
    'prior_records_reviewed=4, contextual_decisions_reused=0, observed_focused_credit_holds':
        'prior_records_reviewed=2, contextual_decisions_reused=0, observed_online_guide_holds',
    'prose_revisions=0, spacing_revisions=4, punctuation_glyph_corrections=0':
        'prose_revisions=2, spacing_revisions=0, punctuation_glyph_corrections=0',
    old_copy: '''    for source in (stage.PROOF, STARTUP, QA, playback.OUT, routes.OUT, audit.OUT, args.visual_review,
                   *(Path(p) for p in base.load(args.visual_review)),
                   *(Path(row["manuscript"]) for row in stored["records"])):
''',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Online guide card testing candidate

The [testing ROM](../../{ROM.as_posix()}) restores ship types, the number of sails, and the Leaning Tower of Pisa on the Online guide cards. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("ending_credit_spacing", "online_card_copy").replace(
    'verified_online_card_copy_predecessor', 'verified_ending_credit_spacing_predecessor').replace(
    'parent.WORK / "release_stack_with_online_card_copy.json"', 'parent.WORK / "release_stack_with_ending_credit_spacing.json"')

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the ending credit spacing candidate and its predecessor": "Preserve the Online card wording candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Online guide card wording

The ship card now mentions the different ship types and the number of sails. The world card names the Leaning Tower of Pisa. Both cards keep their own original PXL slots, screen position, colors and draw path. [Exact source and installed review](../{REVIEW.as_posix()})

An ordinary title replay verified both revised cards and their rotating images, the exact previous card and the return to the title. The full clean-input reconstruction and registered startup passed. Handheld testing remains open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("ending_credit_spacing", "online_card_copy")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
