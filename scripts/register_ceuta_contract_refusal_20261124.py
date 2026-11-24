"""Register the source-bound Ceuta Market refusal on the cumulative branch."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import preflight_ceuta_contract_refusal_20261124 as draft
from scripts import register_claudio_opening_wrap_20261124 as parent
from scripts import replay_ceuta_contract_refusal_20261124 as gameplay
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_ceuta_town_20261124 as review
from scripts.source_locked_derivation_v5118 import checked_text


template = parent.template
PROFILE = "all-routes-ceuta-contract-refusal-v1-20261124"
CHECK = "registered_ceuta_contract_refusal_and_complete_parent_inverse"
WORK, ROM = draft.ROOT, gameplay.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_ceuta_contract_refusal_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                  "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = (WORK / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = WORK / "startup/capture/capture_report.json"
QA, STARTUP = WORK / "qa_passed.xml", WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_ceuta_contract_refusal.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_ceuta_contract_refusal_registered_20261124.md")
CHECKPOINT = "Registered the Ceuta Market refusal with the complete return instruction."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=gameplay.STORED)))
build = SimpleNamespace(__file__=gameplay.__file__, NATIVE=draft.OUT)


def verify(previous, visual_sha):
    stored, packet, live, native, patch = map(files.read, (gameplay.STORED, review.OUT, gameplay.OUT, draft.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == packet["candidate_sha256"]
    assert stored["candidate"] == live["candidate"] == patch["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert stored["exact_complete_parent_inverse"] and stored["only_message"] == draft.KEY
    assert live["ordinary_gameplay"] and native["offline_only"] and len(live["matching_companion_frames"]) == 6
    assert len(native["both_substitutions"]) == 4
    visuals = [native["native_preview"], live["contact_sheet"], *packet["review_sheets"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    clean, parent_rom, staged = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(draft.native.files, (parent_rom, staged))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    assert files.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(after[COMMON]).hexdigest() == stored["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    staged.replace_file(COMMON, before[COMMON])
    assert files.sha256(staged.rom.save()).hexdigest() == previous["candidate_sha256"]
    clean_rows = draft.native.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    arm = after[ARM]
    old_rows, new_rows = (draft.native.owned_entries(archive, arm, draft.digest_range(arm)) for archive in (before[COMMON], after[COMMON]))
    assert [a.message_id for a, b in zip(old_rows, new_rows, strict=True) if a.text != b.text] == [draft.KEY]
    record, = native["records"]
    current_record, = packet["open_review"]
    assert record["source_reference"] == current_record["source_reference"]
    assert record["current_reference"] == current_record["current_reference"]
    records = []
    for row in (*packet["records"], current_record):
        key = row["message_ID"]
        source_ref = draft.evidence.source_ref(clean_rows[key])
        old_ref = draft.evidence.source_ref(old_rows[key])
        new_ref = draft.evidence.source_ref(new_rows[key])
        assert row["source_reference"] == source_ref and row["current_reference"] == old_ref
        selected = row | dict(registered_reference=new_ref | dict(candidate_sha256=candidate))
        if key == draft.KEY:
            assert new_ref == record["proposed_reference"]
            selected.update(english=record["english"], decision="revision", localization_note=record["localization_note"],
                installed_reference=new_ref, review=dict.fromkeys(files.GATES, True),
                proposed_native_cases=native["both_substitutions"], confirmed_live=files.reference(gameplay.OUT))
        else:
            assert old_rows[key].text == new_rows[key].text
            selected["installed_reference"] = new_ref
        records.append(selected)
    assert len(records) == 17 and sum(row["decision"] == "revision" for row in records) == 1

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    source = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "original_arm9_and_protected_runtime_checks_pass",
    })
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    inherited = files.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    for row in shared["records"]:
        key = row["message_ID"]
        old_ref, new_ref = (review.panels.text_reference(entries[key]) for entries in (old_rows, new_rows))
        assert old_ref == row["installed"] and key != draft.KEY and old_rows[key].text == new_rows[key].text
        row["installed"] = new_ref
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_COMMON_sha256=stored["target_COMMON_sha256"], source_review=files.reference(review.OUT),
        visual_review=visuals, stored_proof=files.reference(gameplay.STORED), gameplay=files.reference(gameplay.OUT),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_deck_skill_guidance_predecessor=predecessor, claudio_opening_wrap_release=str(REVIEW)":
        "verified_claudio_opening_wrap_predecessor=predecessor, ceuta_contract_refusal_release=str(REVIEW)",
    "len(batches) == 1142 and len(checks) == 477": "len(batches) == 1143 and len(checks) == 478",
    "assert revised == [review.WRAP_ID]": "assert revised == ['COMMON_MESSAGE_761']",
    "snapshot_scope=[STORY]": "snapshot_scope=[COMMON]",
    "claudio_opening_wrap_release_proof": "ceuta_contract_refusal_release_proof",
    '"claudio_opening_wrap_pipeline"': '"ceuta_contract_refusal_pipeline"',
    "registered_manifest_entries=1143, passing_release_checks=478, changed_components=1, changed_internal_files=[STORY]":
        "registered_manifest_entries=1144, passing_release_checks=479, changed_components=1, changed_internal_files=[COMMON]",
    'target_SC0_sha256=outcome["target_SC0_sha256"]': 'target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "contextual_records_revisited=5, contextual_decisions_reused=4, previously_localized_records=5":
        "contextual_records_revisited=17, contextual_decisions_reused=0, previously_localized_records=17",
    "prose_revisions=0, justified_retentions=4": "prose_revisions=1, justified_retentions=16",
    "ordinary_Rafael_New_Game=True, revised_gameplay_holds=1, native_pages=3, unchanged_gameplay_holds=10":
        "ordinary_Ceuta_town=True, revised_gameplay_holds=1, native_pages=2, unchanged_gameplay_holds=6",
    "prose_revisions=0, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=4":
        "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=16",
    '"claudio_opening_wrap_20261124"': '"ceuta_contract_refusal_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Ceuta Market refusal testing candidate

The Trader keeps the full facility name and the invitation to return on the final line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Claudio opening reflow candidate": "Preserve the registered Ceuta Market refusal candidate",
    "1,143 entries and 478 passing checks": "1,144 entries and 479 passing checks",
    doc: '''    DOC.write_text(f"""# Ceuta Market refusal and town dialogue

The Trader now says **“Sorry. Once you sign a contract at the Governor’s Office, come back.”** Both the Governor’s Office and Palace substitutions fit on two lines. The full facility names and the instruction to return remain intact. Ordinary paired play verified the revised page and complete Trader nameplate, with all six surrounding screens matching. [Exact source and installed text](../{REVIEW.as_posix()}) · [Paired gameplay](../{VERIFY.as_posix()}/{gameplay.OUT.with_suffix(".png").name})

The ordinary Ceuta visit verified 21 held panels across the Market, Tavern, Inn, Governor’s Office and Square. Sixteen other texts retain their wording, including the Madeira tip, the Black Rapier rumor and the Shopkeeper’s account of Admiral Albuquerque’s ancestor. The recorded visit includes the 5-gold drink, the 183-gold round and the 1-gold overnight stay. The Guard refused a trade contract because the city’s two shares already total 100 percent. [Ordinary gameplay and individual decisions](../{review.OUT.as_posix()})

The cumulative candidate passed independent startup, 479 registered checks, 17 focused tests and byte-for-byte reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    lineage = [parent]
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 16:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::register-ceuta-market", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
