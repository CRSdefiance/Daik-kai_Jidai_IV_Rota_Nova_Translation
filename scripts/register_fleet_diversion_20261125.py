"""Register the two tested Lure Fleet revisions on the Seoul candidate."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_fleet_diversion_release_20261125 as checks
from scripts import reconcile_fleet_diversion_sources_20261125 as review
from scripts import register_seoul_reika_20261125 as parent
from scripts import replay_fleet_diversion_questions_20261125 as replay
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_fleet_diversion_replay_20261125 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text


draft, template = replay.draft, parent.template
PROFILE = "all-routes-fleet-diversion-v1-20261125"
CHECK = "registered_fleet_diversion_and_complete_parent_inverse"
WORK, ROM = replay.ROOT, replay.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_fleet_diversion_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF
STARTUP_CAPTURE, QA = checks.STARTUP_CAPTURE, checks.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_fleet_diversion.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_fleet_diversion_registered_20261125.md")
CHECKPOINT = "Registered two Lure Fleet questions that now read naturally on one line."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=replay.PROOF)))
build = SimpleNamespace(__file__=replay.__file__, NATIVE=draft.OUT)


def verify(previous, visual_sha):
    stored, live, native, patch = map(files.read, (replay.PROOF, gameplay.OUT, draft.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == native["candidate_sha256"] == stored["parent"]["sha256"]
    assert live["staged"] == stored and live["focused_fixture_gameplay"] and not live["ordinary_gameplay"]
    assert live["preflight"] == files.reference(draft.OUT) == stored["preflight"]
    assert stored["candidate"] == patch["candidate"] == files.reference(ROM) and stored["exact_parent_inverse"]
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert files.read(review.OUT)["candidate_sha256"] == previous["candidate_sha256"]
    assert native["all_placements_same_allocation"]
    visuals = [*native["native_previews"], live["sheet"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    original, target = (files.NdsImage.open(p) for p in (previous["candidate"], ROM))
    before, after = map(draft.native.files, (original, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert files.sha256(after[COMMON]).hexdigest() == stored["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    target.replace_file(COMMON, before[COMMON])
    assert files.sha256(target.rom.save()).hexdigest() == previous["candidate_sha256"]
    old_rows, new_rows = (parent.review.common_rows(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert {a.message_id for a, b in zip(old_rows, new_rows, strict=True) if a.text != b.text} == draft.DRAFTS.keys()
    ref = draft.review.source_ref
    holds = {row["message_ID"]: row for row in live["results"]}
    assert holds.keys() == draft.DRAFTS.keys()
    records = []
    for row in native["records"]:
        key = row["message_ID"]
        installed = ref(new_rows[key])
        assert row["installed_reference"] == ref(old_rows[key]) and row["proposed_reference"] == installed
        changed = key in holds
        if changed:
            hold = holds[key]
            assert hold["entirely_matching_frames"] == list(gameplay.COMPANIONS)
            assert hold["glyph_plane_matches_preflight"] and hold["nameplate_identical"] and hold["cancelled_without_payment"]
            assert hold["prior_preview"] == row["native_layouts"]
        records.append(row | dict(installed_reference=installed, registered_reference=installed | dict(candidate_sha256=candidate),
            decision="revision" if changed else "retention", review=dict.fromkeys(files.GATES, True)))
    assert len(records) == 6

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "original_arm9_and_protected_runtime_checks_pass",
    })
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(startup, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    inherited = files.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    for row in shared["records"]:
        key = row["message_ID"]
        assert key not in holds and old_rows[key].text == new_rows[key].text
        assert parent.review.PANELS.text_reference(old_rows[key]) == row["installed"]
        row["installed"] = parent.review.PANELS.text_reference(new_rows[key])
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate, visual_review=visuals,
        target_COMMON_sha256=stored["target_COMMON_sha256"], source_review=files.reference(draft.OUT),
        stored_proof=files.reference(replay.PROOF), gameplay=files.reference(gameplay.OUT),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_lisbon_purser_refit_predecessor=predecessor, seoul_reika_release=str(REVIEW)":
        "verified_seoul_reika_predecessor=predecessor, fleet_diversion_release=str(REVIEW)",
    "len(batches) == 1145 and len(checks) == 480": "len(batches) == 1146 and len(checks) == 481",
    "assert revised == ['COMMON_MESSAGE_991']": "assert revised == ['COMMON_MESSAGE_923', 'COMMON_MESSAGE_926']",
    "seoul_reika_release_proof": "fleet_diversion_release_proof",
    '"seoul_reika_pipeline"': '"fleet_diversion_pipeline"',
    "registered_manifest_entries=1146, passing_release_checks=481": "registered_manifest_entries=1147, passing_release_checks=482",
    "contextual_records_revisited=12, contextual_decisions_reused=0, previously_localized_records=12":
        "contextual_records_revisited=6, contextual_decisions_reused=0, previously_localized_records=6",
    "prose_revisions=1, justified_retentions=11": "prose_revisions=2, justified_retentions=4",
    "ordinary_Seoul_Tavern=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=22":
        "focused_Lure_Fleet_fixture=True, revised_gameplay_holds=2, native_pages=2, unchanged_gameplay_holds=14",
    "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=11":
        "prose_revisions=2, phrase_wrap_adjustments=2, punctuation_fields=0, texts_retained=4",
    "text_display_revisions=0, phrase_wrap_adjustments=1": "text_display_revisions=0, phrase_wrap_adjustments=2",
    '"seoul_reika_20261125"': '"fleet_diversion_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Lure Fleet testing candidate

Two crew adviser questions now fit on one line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Seoul Tavern candidate": "Preserve the registered Lure Fleet candidate",
    "1,146 entries and 481 passing checks": "1,147 entries and 482 passing checks",
    doc: '''    DOC.write_text(f"""# Lure Fleet dialogue registration

Two destination questions now fit on one line. Four other voices keep their wording. The exact clean Japanese, former and installed entries, and all five review gates are in the [registered review](../{REVIEW.as_posix()}).

The paired emulator test used an isolated eligibility fixture and a single RAM table entry to select each revised line. The ROM retains the original voice table. Both panels match their preflight glyph planes, 14 other frames match, and each run reaches the London confirmation and cancels without payment. [Paired capture](../{VERIFY.as_posix()}/{gameplay.SHEET.name}) · [Replay receipt](../{VERIFY.as_posix()}/{gameplay.OUT.name})

The cumulative candidate passed independent startup, 482 registered checks, 17 focused tests and exact clean-input reconstruction. The ordinary Missionary destination source, five archived COMMON display owners and unvisited practical scene variants remain open. [Testing package](../{PACKAGE.as_posix()}/README.md) · [Earlier source audit](editorial_fleet_diversion_current_20261125.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 16:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::register-fleet-diversion", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
