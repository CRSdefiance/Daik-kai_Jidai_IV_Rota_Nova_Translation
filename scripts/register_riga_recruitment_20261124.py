"""Register Riga once the native, replay, startup and patch checks pass."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_price_info_digits_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_riga_recruitment_20261124 as build
from scripts import verify_riga_recruitment_replay_20261124 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text

review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-riga-recruitment-v1-20261124"
CHECK = "registered_riga_recruitment_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_riga_recruitment_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / path for path in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_riga_recruitment.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
STORED = build.ROOT / "stored_proof.json"
DOC = Path("docs/editorial_riga_recruitment_registered_20261124.md")
CHECKPOINT = "Registered more natural recruitment questions and regular digits in the crew assignment warnings."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=STORED)))


def verify(previous, visual_sha):
    packet, live, patch = map(files.read, (build.OUT, gameplay.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert candidate == files.digest(REBUILT) == live["candidate_sha256"] == packet["candidate_sha256"]
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert previous["candidate_sha256"] == packet["predecessor_sha256"] == live["predecessor_sha256"]
    assert files.digest(files.CLEAN) == patch["clean_input_sha256"] == previous["clean_input_sha256"]
    assert live["ordinary_gameplay"] and gameplay.baseline.END in live["unchanged_frames"]
    assert {r["frame"]: (r["message_id"], r["count"]) for r in live["revised"]} == gameplay.CHANGED
    assert packet["native_pages"] == 180 and len(packet["regular_digit_cases"]) == 64
    assert len(packet["sheets"]) == 9 and all(files.digest(r["path"]) == r["sha256"] for r in packet["sheets"])
    visual = [files.reference(r["path"]) for r in packet["sheets"]] + [files.reference(gameplay.SHEET)]
    assert visual[-1:] == live["sheets"]
    assert files.sha256("".join(r["sha256"] for r in visual).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    old, new = map(files.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(parent.parent.parent.parent.parent.trend.files, (old, new))
    assert before.keys() == after.keys() and {key for key in before if before[key] != after[key]} == {ARM, COMMON}
    arm, common = after[ARM], after[COMMON]
    assert files.sha256(arm).hexdigest() == packet["target_ARM9_sha256"]
    assert files.sha256(common).hexdigest() == packet["target_COMMON_sha256"]
    undo = bytearray(arm)
    assert packet["exact_parent_reserialize"] and tuple(r["address"] for r in packet["instruction_changes"]) == build.CALLS
    for row in packet["instruction_changes"]:
        at = row["address"] - build.BASE
        assert arm[at:at + 4].hex() == row["after_hex"] and before[ARM][at:at + 4].hex() == row["before_hex"]
        undo[at:at + 4] = bytes.fromhex(row["before_hex"])
    assert undo == before[ARM]
    old_rows = build.recruit.catalogue(before[ARM], before[COMMON])
    new_rows = build.recruit.catalogue(arm, common)
    altered = {r["message_id"] for r in packet["records"] if r["wording_decision"] == "revision"}
    assert altered == {key for key, (draft, _) in build.DRAFTS.items() if draft}
    assert {b.message_id for a, b in zip(old_rows, new_rows, strict=True) if a != b} == altered
    reverted, _, _ = build.owned_deployment(common, arm, new_rows, {key: old_rows[key].text for key in altered})
    assert bytes(reverted) == before[COMMON]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    new.replace_file(ARM, before[ARM])
    new.replace_file(COMMON, reverted)
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]
    files.write(STORED, dict(candidate_sha256=candidate, predecessor_sha256=previous["candidate_sha256"],
        whole_parent_inverse=True, target_ARM9_sha256=packet["target_ARM9_sha256"],
        target_COMMON_sha256=packet["target_COMMON_sha256"], proof=files.reference(build.OUT),
        instruction_changes=packet["instruction_changes"], changed_COMMON=sorted(altered)))

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Riga_number_and_dialogue_changes_preserve_startup",
    })
    exec(compile(source, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    ref = gameplay.panels.text_reference
    for row in shared["records"]:
        key = row["message_ID"]
        assert ref(old_rows[key]) == row["installed"]
        assert ref(new_rows[key]) == row["installed"] or key in altered
    records = [r | dict(review=dict.fromkeys(files.GATES, True),
                        registered_reference=r["installed_reference"] | dict(candidate_sha256=candidate))
               for r in packet["records"]]
    bindings = [r | dict(installed=ref(new_rows[r["message_ID"]])) for r in shared["records"]]
    outcome = dict(translation_policy=packet["translation_policy"], target_locale=packet["target_locale"],
        encoder=packet["encoder"], review_gates=packet["review_gates"], records=records,
        candidate_sha256=candidate, target_ARM9_sha256=packet["target_ARM9_sha256"],
        target_COMMON_sha256=packet["target_COMMON_sha256"], visual_review=visual, native=files.reference(build.OUT),
        stored_proof=files.reference(STORED), gameplay=files.reference(gameplay.OUT), source_credit_added=0,
        shared_consumer_binding=shared | dict(candidate_sha256=candidate, records=bindings),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_lisbon_roster_galley_predecessor=predecessor, price_info_digits_release=str(REVIEW)":
        "verified_price_info_digits_predecessor=predecessor, riga_recruitment_release=str(REVIEW)",
    "len(batches) == 1137 and len(checks) == 472": "len(batches) == 1138 and len(checks) == 473",
    'revised = [row["id"] for row in outcome["records"]]\n        assert revised == [build.FIELD]':
        'revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]\n        assert len(revised) == 10',
    "snapshot_scope=ARM, revised_records": "snapshot_scope=[ARM, COMMON], revised_records",
    "price_info_digits_release_proof=stage.reference(stage.PROOF)": "riga_recruitment_release_proof=stage.reference(stage.PROOF)",
    '"price_info_digits_pipeline"': '"riga_recruitment_pipeline"',
    "registered_manifest_entries=1138, passing_release_checks=473, changed_components=1, changed_internal_files=[ARM]":
        "registered_manifest_entries=1139, passing_release_checks=474, changed_components=2, changed_internal_files=[ARM, COMMON]",
    "contextual_records_revisited=1, contextual_decisions_reused=0, previously_localized_records=1":
        "contextual_records_revisited=12, contextual_decisions_reused=0, previously_localized_records=12",
    "prose_revisions=0, justified_retentions=0, text_display_revisions=1, phrase_wrap_adjustments=0":
        "prose_revisions=9, justified_retentions=3, text_display_revisions=5, phrase_wrap_adjustments=4",
    "ordinary_Syracuse_investment_and_map=True, revised_gameplay_holds=1, native_pages=1, fee_formatter_cases=32":
        "ordinary_Riga_recruitment=True, revised_gameplay_holds=3, native_pages=180, number_call_cases=64",
    "prose_revisions=0, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=0":
        "prose_revisions=9, phrase_wrap_adjustments=4, punctuation_fields=0, texts_retained=3",
    '"price_info_digits_20261124"': '"riga_recruitment_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Riga recruitment testing candidate

The Tavern uses more natural recruitment questions, and crew assignment uses regular digits. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Price Info digits candidate": "Preserve the registered Riga recruitment candidate",
    "1,138 entries and 473 passing checks": "1,139 entries and 474 passing checks",
    doc: '''    DOC.write_text(f"""# Riga recruitment and crew assignment

Five spare-berth questions now avoid repeating “more.” Four assignment questions keep the complete sailor phrase on one row. All five warnings use regular digits. Three existing wordings remain, including one warning that needed a font change. [Clean and installed records](../{REVIEW.as_posix()})

Ordinary play verified Gerhard's follow-up for 49 spare berths and both unassigned-sailor warnings, with 120 and 15 in the regular font. All other sampled screens matched, including the return to assignment after declining. Other officer variants were checked offline. [Paired gameplay](../{VERIFY.as_posix()}/riga_recruitment_paired.png)

The candidate passed startup, 474 release checks, 17 focused tests, and byte-exact clean-input reconstruction. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    for item in reversed(lineage):
        scope.update(vars(item))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Riga-recruitment-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()