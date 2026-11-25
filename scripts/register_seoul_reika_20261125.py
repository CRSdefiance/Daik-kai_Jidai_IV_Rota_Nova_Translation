"""Register Reika's verified Tavern reflow as a cumulative testing candidate."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_seoul_reika_release_20261125 as checks
from scripts import preflight_seoul_reika_20261125 as draft
from scripts import register_lisbon_purser_refit_20261124 as parent
from scripts import replay_seoul_reika_20261125 as replay
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_seoul_reika_replay_20261125 as gameplay
from scripts import verify_seoul_tavern_accept_20261125 as review
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
PROFILE = "all-routes-seoul-reika-v1-20261125"
CHECK = "registered_seoul_reika_and_complete_parent_inverse"
WORK, ROM = replay.ROOT, replay.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_seoul_reika_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF
STARTUP_CAPTURE, QA = checks.STARTUP_CAPTURE, checks.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_seoul_reika.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_seoul_reika_registered_20261125.md")
CHECKPOINT = "Registered Reika's reflow and verified both Seoul Tavern choices and the Pink Apron rumor."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=replay.STAGED)))
build = SimpleNamespace(__file__=replay.__file__, NATIVE=draft.OUT)


def verify(previous, visual_sha):
    stored, packet, live, native, patch = map(files.read, (replay.STAGED, review.OUT, gameplay.OUT, draft.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == packet["candidate_sha256"] == native["parent_candidate_sha256"]
    assert stored["candidate_sha256"] == candidate and stored["exact_parent_inverse"]
    assert live["candidate"] == patch["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert native["exact_allocation_inverse"] and len(live["matching_navigation_frames"]) == 22
    assert native["pages"][-1]["lines"] == live["lines"] and live["ordinary_gameplay"]
    assert live["source_review"] == files.reference(draft.OUT)
    visuals = [native["visual_review"], live["sheet"], *packet["sheets"]]
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
    old_rows, new_rows = (review.common_rows(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert [a.message_id for a, b in zip(old_rows, new_rows, strict=True) if a.text != b.text] == [draft.KEY]
    ref = review.review.source_ref
    records = []
    for row in packet["records"]:
        key = row["message_ID"]
        installed = ref(new_rows[key])
        assert row["installed_reference"] == ref(old_rows[key])
        context = ("Maria buys a round at the Seoul Tavern, and a grateful patron shares a treasure rumor."
                   if key in (855, 867, 870, 872, 874) else
                   "Maria orders drinks at the Seoul Tavern and sees both answers to Reika's invitation for another.")
        selected = row | dict(context=context, installed_reference=installed,
                              registered_reference=installed | dict(candidate_sha256=candidate))
        if key == draft.KEY:
            revised = native["record"]
            assert revised["source_reference"] == row["source_reference"] and revised["proposed_reference"] == installed
            selected.update(english=draft.ENGLISH, localization_note=revised["localization_note"], decision="revision",
                            new_native_layout=native["pages"][-1], verified_revised_hold=files.reference(gameplay.OUT),
                            review=dict.fromkeys(files.GATES, True))
        records.append(selected)
    assert len(records) == 12

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
        assert key != draft.KEY and old_rows[key].text == new_rows[key].text
        assert review.PANELS.text_reference(old_rows[key]) == row["installed"]
        row["installed"] = review.PANELS.text_reference(new_rows[key])
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate, visual_review=visuals,
        target_COMMON_sha256=stored["target_COMMON_sha256"], source_review=files.reference(review.OUT),
        stored_proof=files.reference(replay.STAGED), gameplay=files.reference(gameplay.OUT),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_ceuta_contract_refusal_predecessor=predecessor, lisbon_purser_refit_release=str(REVIEW)":
        "verified_lisbon_purser_refit_predecessor=predecessor, seoul_reika_release=str(REVIEW)",
    "len(batches) == 1144 and len(checks) == 479": "len(batches) == 1145 and len(checks) == 480",
    "assert revised == ['COMMON_MESSAGE_1255']": "assert revised == ['COMMON_MESSAGE_991']",
    "lisbon_purser_refit_release_proof": "seoul_reika_release_proof",
    '"lisbon_purser_refit_pipeline"': '"seoul_reika_pipeline"',
    "registered_manifest_entries=1145, passing_release_checks=480": "registered_manifest_entries=1146, passing_release_checks=481",
    "contextual_records_revisited=26, contextual_decisions_reused=0, previously_localized_records=26":
        "contextual_records_revisited=12, contextual_decisions_reused=0, previously_localized_records=12",
    "prose_revisions=1, justified_retentions=25": "prose_revisions=1, justified_retentions=11",
    "focused_Lisbon_Refit=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=20":
        "ordinary_Seoul_Tavern=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=22",
    "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=25":
        "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=11",
    '"lisbon_purser_refit_20261124"': '"seoul_reika_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Seoul Tavern testing candidate

Reika's reply keeps her reaction and wish in readable phrases. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Lisbon Purser Refit candidate": "Preserve the registered Seoul Tavern candidate",
    "Current editorial checkpoint - 2026-11-24": "Current editorial checkpoint - 2026-11-25",
    "1,145 entries and 480 passing checks": "1,146 entries and 481 passing checks",
    doc: '''    DOC.write_text(f"""# Seoul Tavern reply registration

Reika says **“Are you rich? I'm jealous! Hopefully I'll meet someone nice and be happy soon, too.”** The reflow keeps her initial reaction and the phrase about meeting someone intact. The revised page and Reika’s nameplate passed paired ordinary gameplay, with 22 other frames matching. [Paired capture](../{VERIFY.as_posix()}/{gameplay.OUT.with_suffix(".png").name}) · [Exact source and installed review](../{REVIEW.as_posix()})

The Seoul replay also verified both second-drink choices, a ten-coin and a five-coin charge, both outcomes of a 196-gold round, the Pink Apron rumor, and the return to town. Eleven other lines retain their wording. [Ordinary gameplay and other decisions](../{review.OUT.as_posix()})

The cumulative candidate passed independent startup, 481 registered checks, 17 focused tests, and byte-for-byte reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-seoul-reika", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
