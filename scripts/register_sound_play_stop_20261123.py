"""Register the verified Sound Setup labels over the Pirate affiliation release."""

from inspect import getsource
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_reference
from scripts import register_pirate_affiliation_20261123 as parent
from scripts import stage_sound_play_stop_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_sound_play_stop_20261123 import OUTPUT as DISPLAY


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = parent.ARM, parent.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-sound-play-stop-v1-20261123"
EVIDENCE = stage.ROOT
ROOT, WORK = EVIDENCE.parent / "registered", EVIDENCE.parent / "registration"
ROM = ROOT / "Translation_DS_Sound_Play_Stop_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_sound_play_stop_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_sound_play_stop_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = stage.STARTUP_CAPTURE
REBUILT, RESEARCH_PATCH = stage.REBUILT, stage.PATCH
CHECKPOINT = "Registered the Sound Setup Stop label and verified the original Play and Stop controls."
guard_spec = parent.guard_spec
link_snapshot = parent.link_snapshot
startup_source = checked_text(getsource(startup_reference.startup_proof), {
    "original_ARM9_and_overlay_preserved=True": "only_sound_stop_slot_changed=True, original_overlay_preserved=True",
})
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["exact_play_and_stop_glyphs"])


def observed_count():
    return len(base.load(DISPLAY)["all_full_frame_differences"])


def verify(registry, previous, viewed):
    stored, display = map(base.load, (stage.PROOF, DISPLAY))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == display["candidate_sha256"] == base.digest(REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == display["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["exact_parent_inverse"] and display["ordinary_controller_replay"]
    assert viewed == {display["sheet"]["path"]: display["sheet"]["sha256"]}
    assert all(base.digest(p) == h for p, h in (viewed | display["evidence"]).items())
    assert sum(value is not None for value in display["all_full_frame_differences"].values()) == 9
    assert len(display["retired_Japanese_glyph_residue"]) == 6
    assert all(len(dots) == 3 for dots in display["retired_Japanese_glyph_residue"].values())
    assert native_count() == 9 and observed_count() == 12
    assert [(row["english"], row["decision"]) for row in display["records"]] == [("Stop", "revision"), ("Play", "retention")]
    assert [row | {"review": row["review"] | {"formatting": True}} for row in stored["records"]] == display["records"]
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    clean, old, new = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    lo, hi = stage.SLOT, stage.SLOT + stage.SIZE
    assert source[ARM][lo:hi] == before[ARM][lo:hi] == stage.STOP_JAPANESE
    assert before[ARM][hi:hi + stage.SIZE] == stage.PLAY_ENGLISH
    assert after[ARM] == before[ARM][:lo] + stage.STOP_ENGLISH + before[ARM][hi:]
    assert stage.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    hashes = {p: native.digest(after[p]) for p in (ARM, COMMON, *routes.ROUTES)}
    assert hashes[ARM] == stored["target_ARM9_sha256"] and hashes[COMMON] == previous["target_COMMON_sha256"]
    new.replace_file(ARM, before[ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = parent.parent.parent.bind_registered_story_percent_guard(guard)(source, after)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_scope["startup_proof"](previous, candidate, after[ARM])

    earlier = base.load(parent.REVIEW)
    binding = earlier["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == earlier["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == earlier["retained_editorial_coverage_sha256"]
    census = base.load(routes.OUT)
    assert all(hashes[p] == census["routes"][p]["installed_archive_sha256"] for p in routes.ROUTES)
    result = display | dict(visual_review=viewed, registered_consumer="Sound Setup footer action",
        checked_story_format_guard=checks, shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), new_reviewed_UI_slots=1,
        justified_retentions=1, full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


old_copy = parent.build[parent.build.index("    for source in (stage.PROOF"):parent.build.index("        filename = ")]
old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'parent.WORK / "release_stack_with_online_card_copy.json"': 'parent.WORK / "release_stack_with_pirate_affiliation.json"',
    'verified_online_card_copy_predecessor': 'verified_pirate_affiliation_predecessor',
    'len(batches) == 1098 and len(checks) == 433': 'len(batches) == 1099 and len(checks) == 434',
    'assert len(checks) == 434\n': 'assert len(checks) == 435\n',
    'reviewed_UI_labels=1': 'reviewed_UI_labels=2',
    'previously_localized_records=0, contextual_records_revisited=1, contextual_decisions_reused=0':
        'previously_localized_records=1, contextual_records_revisited=2, contextual_decisions_reused=1',
    'justified_retentions=0': 'justified_retentions=1',
    'focused_battle_nameplate_fixture=True': 'ordinary_sound_setup=True',
    'contextual_decisions_reused=0, observed_focused_battle_nameplate_holds':
        'contextual_decisions_reused=1, observed_sound_setup_holds',
    '(PLAYBACK, DISPLAY)': '(DISPLAY,)',
    old_copy: '''    for source in (stage.PROOF, STARTUP, QA, DISPLAY, routes.OUT, audit.OUT, args.visual_review,
                   *(Path(p) for p in base.load(args.visual_review))):
''',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Sound Setup Play and Stop testing candidate

The [testing ROM](../../{ROM.as_posix()}) displays the English Play and Stop actions in Sound Setup. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
}).replace("pirate_affiliation", "sound_play_stop").replace(
    "verified_sound_play_stop_predecessor", "verified_pirate_affiliation_predecessor").replace(
    'parent.WORK / "release_stack_with_sound_play_stop.json"', 'parent.WORK / "release_stack_with_pirate_affiliation.json"')

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    "Preserve the Pirate affiliation candidate and its predecessor": "Preserve the Sound Setup candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Sound Setup Play and Stop

Sound Setup now shows **Stop** while a BGM track is playing and retains **Play** for starting a track or previewing a sound effect. The four text bytes fit the original eight-byte slot. Ordinary title-menu replays checked both playback states, changing the track, the SFX preview action and the return to Options and title. The English label also removes three leftover Japanese glyph pixels that persisted after leaving Stop. [Exact review and captures](../{REVIEW.as_posix()})

The candidate's startup, 24 protected name getter checks, 17 repository tests and exact clean-input patch reconstruction passed. Audio output and handheld display were outside this check. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("pirate_affiliation", "sound_play_stop")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
