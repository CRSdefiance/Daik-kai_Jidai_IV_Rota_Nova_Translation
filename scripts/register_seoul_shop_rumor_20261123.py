"""Register the source-reviewed Seoul Food Shop reflow on the cumulative ROM."""

from pathlib import Path
from types import SimpleNamespace

from scripts import register_sea_inspection_prose_20261123 as prior
from scripts import prepare_riga_seoul_review_20261123 as review
from scripts.check_seoul_rumor_release_20261123 import PATCH, PATCH_PROOF, PLAY, REBUILT, SHEET, STARTUP_CAPTURE
from scripts.source_locked_derivation_v5118 import checked_text


template = prior.template
PROFILE = "all-routes-seoul-shop-rumor-v1-20261123"
CHECK = "registered_seoul_shop_rumor_and_complete_parent_inverse"
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261123_seoul_shop_rumor_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
ROM = review.ROM
MANIFEST = ROM.with_suffix(".manifest.json")
PLAN = VERIFY / "registration_mutation_plan.json"
STARTUP = review.STAGE / "own_startup_verification.json"
QA = review.STAGE / "qa_passed.xml"
DOC = Path("docs/editorial_seoul_shop_rumor_registered_20261123.md")
CHECKPOINT = "Registered the reflowed Hideyoshi and Kurushima reply in Seoul."
REGISTRY_BEFORE, LEDGER_BEFORE = prior.REGISTRY_NEXT, prior.LEDGER_NEXT
REGISTRY_NEXT = review.STAGE / "release_stack_with_seoul_shop_rumor.json.gz"
LEDGER_NEXT = review.STAGE / "ledger_after.json.gz"
VISUAL = review.STAGE / "visual_review.json"
PROOF = review.STAGE / "stored_proof.json"
stage = SimpleNamespace(**(vars(review) | dict(PARENT_RELEASE=prior.RELEASE, PROOF=PROOF, SHEET=SHEET)))


def verify(parent, visual_sha):
    stored, play, patch = map(stage.read, (PROOF, PLAY, PATCH_PROOF))
    candidate = stored["candidate"]["sha256"]
    assert candidate == play["candidate_sha256"] == patch["candidate_sha256"] == stage.digest(ROM) == stage.digest(REBUILT)
    assert stored["clean"]["sha256"] == patch["clean_input_sha256"] == parent["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert stored["predecessor"]["sha256"] == parent["candidate_sha256"] == stage.digest(parent["candidate"])
    assert patch["byte_exact"] and stage.digest(PATCH) == patch["patch"]["sha256"]
    assert len(play["ordinary_food_shop_repetitions"]) == 2 and len(play["matching_control_frames"]) == 9
    refs = [stored["preview"], play["sheet"]]
    assert all(stage.digest(row["path"]) == row["sha256"] for row in refs)
    visual = {row["path"]: row["sha256"] for row in refs}
    assert stage.digest_bytes("".join(visual.values()).encode("ascii")) == visual_sha
    stage.write(VISUAL, visual)
    clean, old, new = map(stage.NdsImage.open, (stage.CLEAN, parent["candidate"], ROM))
    arm = old.read_file(stage.ARM)
    assert stage.digest_bytes(arm) == stored["target_ARM9_sha256"] == parent["target_ARM9_sha256"]
    assert new.read_file(stage.ARM) == arm
    assert template.right_bound(arm, parent["right_bound_configuration"])["matched_repair_spans"] == 8
    assert all(stage.digest_bytes(new.read_file(f"/data/SC{i}.DK4")) == parent[f"target_SC{i}_sha256"] for i in range(4))
    common, updated = (image.read_file(stage.COMMON) for image in (old, new))
    assert stage.digest_bytes(updated) == stored["target_COMMON_sha256"]
    before, after = (stage.common_rows(raw, arm) for raw in (common, updated))
    assert {a.message_id for a,b in zip(before, after, strict=True) if a != b} == {stage.RUMOR}
    row, = stored["records"]
    source = stage.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))[stage.RUMOR]
    assert row["source_reference"] == stage.ref(source)
    assert row["current_reference"] == stage.ref(before[stage.RUMOR])
    assert row["staged_reference"] == stage.ref(after[stage.RUMOR])
    row["registered_reference"] = row["staged_reference"] | dict(candidate_sha256=candidate)
    new.replace_file(stage.COMMON, common)
    assert bytes(new.rom.save()) == old.source.read_bytes()
    stage.validate_natural_dialogue_batch(stored)
    historical = stage.read(prior.REVIEW)
    shared = historical["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == parent["candidate_sha256"]
    assert all(before[r["message_ID"]] == after[r["message_ID"]] for r in shared["records"])
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "seoul_shop_rumor_startup_and_ARM9_match_parent",
    })
    exec(compile(startup, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](parent, candidate, arm)
    return stored | dict(candidate_sha256=candidate, registered=True, actual_revised_ROM_replay_pending=False,
        observed=play, visual_review=visual, ordinary_town_review=stage.reference(stage.REPORT),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=historical["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=historical["retained_editorial_coverage_sha256"],
        new_source_credit=0, full_editorial_goal_complete=False)


old_doc = prior.finish[prior.finish.index("    DOC.write_text"):prior.finish.index("    prefix =")]
old_readme = prior.prepare[prior.prepare.index('    (PACKAGE / "README.md").write_text'):prior.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
prepare = checked_text(prior.prepare, {
    "verified_cartridge_title_predecessor=predecessor, sea_inspection_prose_release=str(REVIEW)":
        "verified_sea_inspection_predecessor=predecessor, seoul_shop_rumor_release=str(REVIEW)",
    "1103 and len(checks) == 438": "1104 and len(checks) == 439",
    "assert len(revised) == 4": "assert revised == ['COMMON_MESSAGE_726']",
    "Path(sea.__file__)": "Path(review.__file__)",
    '"sea_inspection_prose_pipeline"': '"seoul_shop_rumor_pipeline"',
    'PATCH_PROOF, PLAY, stage.SHEET, stage.PROOF, VISUAL, sea.PANEL_REPORT, sea.SHEET, sea.WORK / "portrait_sheet_01.png"':
        'PATCH_PROOF, PLAY, stage.SHEET, stage.PROOF, VISUAL, stage.REPORT, stage.STAGE / "seoul_rumor_before_after.png"',
    "registered_manifest_entries=1104, passing_release_checks=439": "registered_manifest_entries=1105, passing_release_checks=440",
    "contextual_records_revisited=9, contextual_decisions_reused=9, previously_localized_records=9":
        "contextual_records_revisited=15, contextual_decisions_reused=14, previously_localized_records=15",
    "prose_revisions=4, justified_retentions=5, text_display_revisions=4":
        "prose_revisions=1, justified_retentions=14, text_display_revisions=1",
    "focused_emulator_replays=2, offline_original_voice_cases=8": "paired_ordinary_shop_holds=2, matching_control_frames=9",
    "naturally_spawned_encounter=False, handheld=False": "ordinary_gameplay=True, handheld=False",
    'revisited_reactions=8, contextual_notice_retained=True, prose_revisions=4, new_contextual_credit=0':
        "ordinary_town_holds=26, distinct_reviewed_ids=15, prose_revisions=1, new_contextual_credit=0",
    '"sea_inspection_prose_20261123"': '"seoul_shop_rumor_20261123"',
    old_readme: '''    (PACKAGE / "README.md").write_text(f"""# Seoul Square testing candidate

The Seoul shopkeeper's reply about Hideyoshi and Kurushima now keeps the vow on one line. The [clean-input patch](translation.xdelta) reconstructs the ROM with SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(prior.finish, {
    "Preserve the registered sea-inspection prose candidate": "Preserve the registered Seoul shop rumor candidate",
    "1,104 entries and 439 passing checks": "1,105 entries and 440 passing checks",
    old_doc: '''    DOC.write_text(f"""# Seoul shopkeeper reply

The clean Japanese shopkeeper vows to drive off either Hideyoshi or Kurushima every time they come. The revised English keeps the defiant opening and the whole vow on separate complete lines. Both ordinary Food Shop visits showed the clean wrap, complete Shopkeeper nameplate and normal Square return. All nine control frames matched, including Yifa's recruitment return.

The cumulative ROM passed the clean-input round-trip, six startup comparisons, 24 protected getters, all eight ASCII right-bound spans and 17 focused tests. The Riga and Seoul ledger records 26 actual dialogue holds across 15 shared IDs. The existing editorial credit stays at 27,700. Other conditional variants and handheld display remain unobserved. [Registered review](../{REVIEW.as_posix()}) · [Paired playtesting](../{VERIFY.as_posix()}/ordinary_Seoul_comparison.png) · [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    scope = vars(template) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::release-transaction", "exec"), scope)
    parser = template.ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    assert args.finish_only or args.visual_sha256
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
