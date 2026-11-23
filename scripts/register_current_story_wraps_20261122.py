"""Register the verified four-route story wrap and dialogue checkpoint."""

from pathlib import Path
from xml.etree import ElementTree as ET

from scripts import register_square_rumor_wraps_20261122 as parent
from scripts import replay_current_story_wraps_20261122 as live
from scripts import stage_current_story_wraps_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-early-story-wraps-v1-20261122"
ROOT = parent.ROOT.with_name("early_story_wraps_registered_20261122")
ROM = ROOT / "Translation_DS_Early_Story_Wraps_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_early_story_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_early_story_wraps_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered 13 early story and tutorial revisions across all four routes."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_source = checked_text(parent.startup_source, {
    "original_ARM9_and_overlay_preserved=False, square_rumor_layout_and_COMMON_offsets_only=True":
        "original_ARM9_and_overlay_preserved=True, story_archives_only=True",
})
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return base.load(DISPLAY)["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def verify(registry, previous, viewed):
    proof, checked, played, manuscript = map(base.load, (stage.PROOF, DISPLAY, live.LIVE, stage.review.REVIEW))
    candidate = base.digest(stage.ROM)
    assert candidate == base.digest(stage.REBUILT) == proof["candidate_sha256"] == checked["candidate_sha256"] == played["candidate_sha256"]
    assert base.digest(parent.ROM) == previous["candidate_sha256"] == proof["predecessor_sha256"] == manuscript["candidate_sha256"]
    assert stage.PROOF.is_file() and checked["stage_sha256"] == base.digest(stage.PROOF)
    assert proof["draft_sha256"] == base.digest(stage.review.REVIEW)
    assert viewed == {s["path"]: s["sha256"] for s in checked["sheets"] + played["sheets"]}
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    assert played["initialized_excerpts"] and not played["natural_story_triggers_claimed"] and observed_count() == 6
    assert played["report_sha256"] == base.digest(live.REPORT)
    assert checked["offline_native_only"] and native_count() == 15
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, old, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == proof["clean_sha256"] == previous["clean_input_sha256"]
    a, b = map(native.files, (old, target))
    archives = {f"/data/SC{i}.DK4" for i in range(4)}
    assert a.keys() == b.keys() and {p for p in a if a[p] != b[p]} == archives == proof["archive_hashes"].keys()
    assert proof["archive_hashes"] == {p: native.digest(b[p]) for p in archives}
    assert native.digest(b[ARM]) == previous["target_ARM9_sha256"]
    assert native.digest(b[COMMON]) == previous["target_COMMON_sha256"]
    for path in archives:
        target.replace_file(path, a[path])
    assert proof["whole_parent_inverse"] and bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean), b)
    assert checks == proof["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous, candidate, b[ARM])

    refs = {(r["file_path"], r["id"]): r for r in checked["records"]}
    observed = {(live.ARCHIVE, r["id"]): r for r in played["observations"]}
    banks = {p: native.IlnkContainer.parse(b[p]) for p in archives}
    records = []
    for row in manuscript["records"]:
        path, ident, block = (row[k] for k in ("file_path", "id", "block"))
        display = refs.pop((path, ident), None)
        assert (row["decision"] == "revision") == bool(display and display["layouts"])
        ref = display or row["current_reference"]
        payload = banks[path].blocks[block]
        exact = bytes.fromhex(ref["exact_command_hex"])
        at = ref["command_offset"]
        assert payload[at:at+len(exact)] == exact
        registered = dict(candidate_sha256=candidate, command_offset=at, offset=at+5,
            archive_sha256=proof["archive_hashes"][path], block_sha256=native.digest(payload),
            file_path=path, block=block, exact_command_hex=exact.hex(), exact_body_hex=exact[6:exact.index(0,6)].hex())
        records.append(row | dict(registered_reference=registered, display_proof=display,
            review=row["review"] | {"formatting":True}, observed_focused=observed.pop((path, ident), None)))
    assert not refs and not observed and len(records) == 72 and all(all(r["review"].values()) for r in records)
    result = dict(candidate_sha256=candidate, records=records, translation_policy="natural-dialogue-v2",
        target_locale="en-US", visual_review=viewed, focused_gameplay=played, native_display_sha256=base.digest(DISPLAY),
        checked_story_format_guard=checks, contextual_review_sha256=base.digest(stage.review.REVIEW),
        heuristic_triage_sha256=base.digest(stage.review.TRIAGE), wording_revisions=2, wrap_only_revisions=11,
        justified_retentions=59, historical_source_credit=dict(by_census_id={}, direct_keys=0),
        full_editorial_goal_complete=False, hardware=False)
    return proof, result, {p: native.digest(b[p]) for p in archives | {ARM, COMMON}}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "len(batches) == 1054 and len(checks) == 389": "len(batches) == 1055 and len(checks) == 390",
    "(stage.PROOF, STARTUP, QA, live.LIVE, args.visual_review,": "(stage.PROOF, STARTUP, QA, live.LIVE, DISPLAY, args.visual_review,",
    "(live.LIVE, stage.PROOF)": "(live.LIVE, DISPLAY, stage.PROOF)",
    "source_bound_square_rumor_layout=stored['native_scope']": "source_bound_story_archives=stored['archive_hashes']",
    "changed_component_hashes=archives": "changed_component_hashes=stored['archive_hashes']",
    "changed_internal_files=sorted(archives)": "changed_internal_files=sorted(stored['archive_hashes'])",
    "changed_components=2": "changed_components=4",
    "previously_localized_records=2, contextual_records_revisited=2": "previously_localized_records=72, contextual_records_revisited=72",
    "prior_records_reviewed=2": "prior_records_reviewed=72",
    "wrap_only_revisions=2": "wrap_only_revisions=11",
    "justified_retentions=0": "justified_retentions=59",
    "prose_revisions=0": "prose_revisions=2",
    "text_display_revisions=2": "text_display_revisions=11",
    "focused_original_Square_rumor_selection=True": "focused_initialized_Maria_lesson_and_battle=True",
    "observed_focused_rumors": "observed_focused_dialogue",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Early story wraps testing candidate

The [testing ROM](../../{ROM.as_posix()}) carries 13 story and tutorial revisions across all four routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("square_rumor_wraps", "early_story_wraps").replace(
    "verified_square_shop_names_predecessor", "verified_square_rumor_wraps_predecessor")
doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "earlier = [stage.ROM]": "earlier = [live.ROM]",
    "Preserve the Square rumor wrap candidate, predecessor and staged ROM":
        "Preserve the early story wrap candidate, predecessor and unique focused ROM",
    doc:'''    DOC.write_text(f"""# Early story and tutorial wraps

The batch revisited 72 records in 11 exchanges and kept 59 with individual reasons. Eleven revisions fix line breaks. Two refine Gerhard's address to Manaus and Aziza's order to bring the ship around to the enemy's starboard quarter. [Source, installed text and all five review gates](../{REVIEW.as_posix()})

All 13 changed records passed native rendering and visual review, including default and maximum-width name substitutions. Six original dialogue commands played through an initialized Maria scene, covering the ship-buying lesson, a battle warning and a retreat. The other nine revised prompts were checked offline. Their individual story triggers remain unvisited in this build. Startup and 17 regressions passed. [Candidate and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)

The broader offline scan marked 423 possible wrap leads across 19,721 ASCII story bodies. The results are triage clues. Earlier credits carry forward, and the remaining shared, random, name and alternate-display scope stays active. [Current scan](../{stage.review.TRIAGE.as_posix()})
""",encoding="utf-8")
''',
}).replace("square_rumor_wraps", "early_story_wraps")
scope = parent.scope | globals()
for program in (build, commit):
    exec(compile(program, __file__ + "::register", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
