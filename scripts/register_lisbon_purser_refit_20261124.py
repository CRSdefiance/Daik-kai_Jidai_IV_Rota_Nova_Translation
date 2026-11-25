"""Register the verified Lisbon Purser Refit wording as the next cumulative candidate."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import preflight_lisbon_purser_refit_20261124 as draft
from scripts import register_ceuta_contract_refusal_20261124 as parent
from scripts import replay_lisbon_purser_refit_20261124 as replay
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_lisbon_purser_refit_replay_20261124 as gameplay
from scripts import verify_lisbon_stock_quota_20261124 as review
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
PROFILE = "all-routes-lisbon-purser-refit-v1-20261124"
CHECK = "registered_lisbon_purser_refit_and_complete_parent_inverse"
WORK, ROM = replay.ROOT, replay.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_lisbon_purser_refit_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                    "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = (WORK / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = WORK / "startup/capture/capture_report.json"
QA, STARTUP = WORK / "qa_passed.xml", WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_lisbon_purser_refit.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_lisbon_purser_refit_registered_20261124.md")
CHECKPOINT = "Registered the Lisbon Purser Refit help with clearer stock-buying wording."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=replay.STAGED)))
build = SimpleNamespace(__file__=replay.__file__, NATIVE=draft.OUT)


def verify(previous, visual_sha):
    stored, packet, live, native, patch = map(files.read, (replay.STAGED, review.OUT, gameplay.OUT, draft.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == packet["candidate_sha256"] == native["candidate_sha256"]
    assert stored["candidate_sha256"] == candidate and stored["exact_parent_inverse"]
    assert live["candidate"] == patch["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert native["exact_allocation_inverse"] and len(live["matching_navigation_frames"]) == 20
    assert live["source_review"] == files.reference(draft.OUT)
    native_font = files.read(native["native_proof"]["path"])
    assert files.reference(native["native_proof"]["path"]) == native["native_proof"]
    font_record, = native_font["records"]
    assert font_record["complete_independent_font_plane_equal"] and font_record["text_and_pixel_guards_and_ABI_preserved"]
    assert font_record["lines"] == live["lines"]
    visuals = [native["sheet"], live["sheet"], *packet["contact_sheets"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    parent_rom, staged = map(files.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(parent.draft.native.files, (parent_rom, staged))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(after[COMMON]).hexdigest() == stored["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    staged.replace_file(COMMON, before[COMMON])
    assert files.sha256(staged.rom.save()).hexdigest() == previous["candidate_sha256"]
    parser = review.scope.base.common_rows
    old_rows, new_rows = (parser(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert [a.message_id for a, b in zip(old_rows, new_rows, strict=True) if a.text != b.text] == [draft.KEY]
    ref = review.scope.source_ref
    original = packet["proposed_revision"]
    revised = native["record"]
    assert original["source_reference"] == revised["source_reference"]
    assert original["installed_reference"] == revised["current_reference"] == ref(old_rows[draft.KEY])
    assert revised["proposed_reference"] == ref(new_rows[draft.KEY])
    records = []
    for row in (*packet["records"], original):
        key = row["message_ID"]
        installed = ref(new_rows[key])
        assert row["installed_reference"] == ref(old_rows[key])
        current = row | dict(installed_reference=installed, registered_reference=installed | dict(candidate_sha256=candidate))
        if key == draft.KEY:
            current.update(english=draft.ENGLISH, localization_note=revised["localization_note"], decision="revision",
                           new_native_layout=font_record, verified_revised_hold=files.reference(gameplay.OUT),
                           review=dict.fromkeys(files.GATES, True))
        records.append(current)
    assert len(records) == 26
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
        old_ref, new_ref = (review.panels.text_reference(entries[key]) for entries in (old_rows, new_rows))
        assert key != draft.KEY and old_ref == row["installed"] and old_rows[key].text == new_rows[key].text
        row["installed"] = new_ref
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
    "verified_claudio_opening_wrap_predecessor=predecessor, ceuta_contract_refusal_release=str(REVIEW)":
        "verified_ceuta_contract_refusal_predecessor=predecessor, lisbon_purser_refit_release=str(REVIEW)",
    "len(batches) == 1143 and len(checks) == 478": "len(batches) == 1144 and len(checks) == 479",
    "assert revised == ['COMMON_MESSAGE_761']": "assert revised == ['COMMON_MESSAGE_1255']",
    "ceuta_contract_refusal_release_proof": "lisbon_purser_refit_release_proof",
    '"ceuta_contract_refusal_pipeline"': '"lisbon_purser_refit_pipeline"',
    "registered_manifest_entries=1144, passing_release_checks=479": "registered_manifest_entries=1145, passing_release_checks=480",
    "contextual_records_revisited=17, contextual_decisions_reused=0, previously_localized_records=17":
        "contextual_records_revisited=26, contextual_decisions_reused=0, previously_localized_records=26",
    "prose_revisions=1, justified_retentions=16": "prose_revisions=1, justified_retentions=25",
    "ordinary_Ceuta_town=True, revised_gameplay_holds=1, native_pages=2, unchanged_gameplay_holds=6":
        "focused_Lisbon_Refit=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=20",
    "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=16":
        "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=25",
    '"ceuta_contract_refusal_20261124"': '"lisbon_purser_refit_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Lisbon Purser Refit testing candidate

Refit Help describes the Purser's two abilities in plain language. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Ceuta Market refusal candidate": "Preserve the registered Lisbon Purser Refit candidate",
    "1,144 entries and 479 passing checks": "1,145 entries and 480 passing checks",
    doc: '''    DOC.write_text(f"""# Lisbon Purser Refit help registration

The Refit panel now reads **“A purser can bargain and buy out local stock.”** The revised phrase matches the Trade Help and the observed extra-stock purchase. It fits the original COMMON allocation. The revised hold passed native text and visual checks, and 20 companion screens matched the parent. [Paired capture](../{VERIFY.as_posix()}/{gameplay.OUT.with_suffix(".png").name}) · [Exact source and installed text](../{REVIEW.as_posix()})

The cumulative candidate passed independent startup, 480 registered checks, 17 focused tests and byte-for-byte reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md) · [Lisbon stock-quota checkpoint](editorial_lisbon_stock_quota_current_20261124.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-lisbon-purser", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
