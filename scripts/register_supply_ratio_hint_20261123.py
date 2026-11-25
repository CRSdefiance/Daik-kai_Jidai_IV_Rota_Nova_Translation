"""Register the verified Supply Ratio button hint over Sound Setup."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_sound_play_stop_20261123 as parent
from scripts.check_supply_ratio_release_inputs_20261123 import PATCH as RESEARCH_PATCH, PROOF, REBUILT, STARTUP_CAPTURE
from scripts.finish_sound_play_stop_20261123 import apply_snapshot
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_supply_ratio_hint_20261123 import ENGLISH, SLOT, SOURCE
from scripts.verify_supply_ratio_hint_20261123 import HOLDS, OUTPUT as DISPLAY, ROOT as EVIDENCE


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = parent.ARM, parent.COMMON, parent.routes, parent.audit
stage = SimpleNamespace(PROOF=PROOF, ROM=EVIDENCE / "Translation_DS_Supply_Ratio_Mix_STAGED.nds", native=native)
PROFILE = "all-routes-supply-ratio-hint-v1-20261123"
ROOT, WORK = EVIDENCE / "registered", EVIDENCE / "registration"
ROM = ROOT / "Translation_DS_Supply_Ratio_Hint_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_supply_ratio_hint_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_supply_ratio_hint_registered_20261123.md")
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
CHECKPOINT = "Registered Mix on the L/R Supply Ratio button hint."
guard_spec, link_snapshot, copy_in_place = parent.guard_spec, parent.link_snapshot, apply_snapshot
storage = base.load(parent.VERIFY / "generated_snapshot_storage.json")
REGISTRY_BACKUP, LEDGER_BACKUP = (Path(storage[k]) for k in ("registry_snapshot", "ledger_snapshot"))

startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_source = checked_text(parent.startup_source, {"only_sound_stop_slot_changed": "only_supply_ratio_hint_slot_changed"})
exec(compile(startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(HOLDS)


def observed_count():
    return len(base.load(DISPLAY)["observed_frames"])


def verify(registry, previous, viewed):
    stored, display = map(base.load, (stage.PROOF, DISPLAY))
    stored["changed_files"] = [stored["changed_file"]]
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == display["candidate_sha256"] == base.digest(REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == display["predecessor_sha256"] == base.digest(parent.ROM)
    assert storage["candidate_sha256"] == previous["candidate_sha256"] and stored["exact_parent_inverse"]
    assert viewed == {display["sheet"]["path"]: display["sheet"]["sha256"]}
    assert all(base.digest(p) == h for p, h in (viewed | display["evidence"]).items())
    assert display["focused_emulator_fixture"] and not display["fixture_changes_label"]
    assert native_count() == 4 and observed_count() == 12
    assert [key for key, item in display["observed_frames"].items() if item.get("font_checks")] == list(map(str, HOLDS))
    record, = display["records"]
    assert record == stored["record"] | {"review": stored["record"]["review"] | {"formatting": True}}
    assert record["english"] == "Mix" and record["decision"] == "revision"
    suite, = parent.scope["ET"].parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_input_sha256"]
    clean, old, new = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    end = SLOT + len(SOURCE)
    assert source[ARM][SLOT:end] == before[ARM][SLOT:end] == SOURCE
    assert after[ARM] == before[ARM][:SLOT] + ENGLISH + before[ARM][end:]
    assert parent.stage.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    hashes = {p: native.digest(after[p]) for p in (ARM, COMMON, *routes.ROUTES)}
    assert hashes[ARM] == stored["target_ARM9_sha256"] and hashes[COMMON] == previous["target_COMMON_sha256"]
    new.replace_file(ARM, before[ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = parent.parent.parent.parent.bind_registered_story_percent_guard(guard)(source, after)
    assert checks["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous, candidate, after[ARM])

    earlier = base.load(parent.REVIEW)
    binding = earlier["shared_consumer_binding"]
    assert len(binding["records"]) == 276 and binding["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(routes.OUT) == earlier["retained_four_route_census_sha256"]
    assert base.digest(audit.OUT) == earlier["retained_editorial_coverage_sha256"]
    census = base.load(routes.OUT)
    assert all(hashes[p] == census["routes"][p]["installed_archive_sha256"] for p in routes.ROUTES)
    result = display | dict(visual_review=viewed, registered_consumer="Supply Ratio L/R button hint",
        checked_story_format_guard=checks, shared_consumer_binding=binding | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=base.digest(routes.OUT), retained_editorial_coverage_sha256=base.digest(audit.OUT),
        historical_source_credit=dict(by_census_id={}, direct_keys=0), new_reviewed_UI_slots=1,
        justified_retentions=0, full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return stored, result, hashes


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    'registry_backup = WORK / "release_stack_before_sound_play_stop.json"': 'registry_backup = REGISTRY_BACKUP',
    'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"':
        'ledger_backup, ledger_next = LEDGER_BACKUP, WORK / "ledger_after.json"',
    '(ROOT, PACKAGE, DOC, registry_backup, registry_next, ledger_backup, ledger_next)':
        '(ROOT, PACKAGE, DOC, registry_next, ledger_next)',
    'link_snapshot(parent.WORK / "release_stack_with_pirate_affiliation.json", registry_backup, snapshot["registry_before"])':
        'assert snapshot["registry_before"] == storage["registry_sha256"] == base.digest(registry_backup)',
    'link_snapshot(parent.WORK / "ledger_after.json", ledger_backup, snapshot["ledger_before"])':
        'assert snapshot["ledger_before"] == storage["ledger_sha256"] == base.digest(ledger_backup)',
    'len(batches) == 1099 and len(checks) == 434': 'len(batches) == 1100 and len(checks) == 435',
    'assert len(checks) == 435\n': 'assert len(checks) == 436\n',
    'reviewed_UI_labels=2': 'reviewed_UI_labels=1',
    'previously_localized_records=1, contextual_records_revisited=2, contextual_decisions_reused=1':
        'previously_localized_records=0, contextual_records_revisited=1, contextual_decisions_reused=0',
    'justified_retentions=1': 'justified_retentions=0',
    'ordinary_sound_setup=True': 'focused_supply_ratio_fixture=True',
    'contextual_decisions_reused=1, observed_sound_setup_holds':
        'contextual_decisions_reused=0, observed_supply_ratio_holds',
    'verified_pirate_affiliation_predecessor': 'verified_sound_play_stop_predecessor',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Supply Ratio button hint testing candidate

The [testing ROM](../../{ROM.as_posix()}) displays **Mix** beside the L/R controls. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("sound_play_stop_release", "supply_ratio_hint_release").replace("registered_sound_play_stop_and", "registered_supply_ratio_hint_and").replace(
    "sound_play_stop_pipeline", "supply_ratio_hint_pipeline").replace(
    "release_stack_with_sound_play_stop.json", "release_stack_with_supply_ratio_hint.json").replace("sound_play_stop_20261123", "supply_ratio_hint_20261123")

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'registry_backup = WORK / "release_stack_before_sound_play_stop.json"': 'registry_backup = REGISTRY_BACKUP',
    'ledger_backup, ledger_next = WORK / "ledger_before.json", WORK / "ledger_after.json"':
        'ledger_backup, ledger_next = LEDGER_BACKUP, WORK / "ledger_after.json"',
    'update_ledger_in_place(ledger_backup.read_bytes(), ledger_next.read_bytes())': 'copy_in_place(ledger_next, base.LEDGER)',
    "Preserve the Sound Setup candidate and its predecessor": "Preserve the Supply Ratio candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Supply Ratio button hint

The Copenhagen Port Worker's water-and-food question opens the Supply Ratio panel. **Mix** names the setting beside L/R and uses the same wording as the question. The original hint `割合` was visible in the footer. The focused replay used the original buttons after a bounded supply fixture. Four displayed holds matched all three native English letters and the full Back and Select glyphs. Eight other whole frames matched the predecessor. [Source, display and controls](../{REVIEW.as_posix()})

Cold startup, 24 protected name getters, all 17 focused tests and exact clean-input reconstruction passed. Naturally earned shortages and handheld verification remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("release_stack_with_sound_play_stop.json", "release_stack_with_supply_ratio_hint.json")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
