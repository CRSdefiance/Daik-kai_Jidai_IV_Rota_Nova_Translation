"""Register the source-reviewed Tunis shop advice with cumulative proofs."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_cartridge_title_20261123 as template
from scripts import register_guild_trade_numerals_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_tunis_shop_advice_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


review, trend = build.review, build.trend
ARM, COMMON, ROM = trend.ARM, trend.COMMON, build.ROM
PROFILE = "all-routes-tunis-shop-advice-v1-20261124"
CHECK = "registered_tunis_shop_advice_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_tunis_shop_advice_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_tunis_shop_advice.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_tunis_shop_advice_registered_20261124.md")
CHECKPOINT = "Registered the Tunis Shopkeeper's courteous Market advice."
SHEET = build.PAIRED.with_name("paired_tunis_shop_advice_1_20261123.png")
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def visuals(preflight):
    return [files.reference(SHEET), *(files.reference(row["path"]) for row in preflight["proposed_sheets"])]


def verify(previous, visual_sha):
    stored, live, patch, preflight = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert files.digest(files.CLEAN) == patch["clean_input_sha256"] == previous["clean_input_sha256"]
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == live["predecessor_sha256"] == preflight["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_message"] == review.KEY
    assert stored["source_preflight"] == files.reference(review.OUT)
    assert live["before"] == files.reference(build.BEFORE) and live["after"] == files.reference(build.AFTER)
    assert live["stored"] == files.reference(build.STORED) and live["ordinary_saved_game"]
    assert [row["frame"] for row in live["dialogue_holds"]] == [5800, 7800, 8600, 9400]
    assert build.END in live["unchanged_frames"]
    assert {row["frame"] for row in live["shop_selection_blinks"]} == build.MENU_BLINKS.keys()
    visible = visuals(preflight)
    assert visible[0] == live["sheets"][0]
    assert visible[1:] == [dict(path=Path(row["path"]).as_posix(), sha256=row["sha256"])
                           for row in preflight["proposed_sheets"]]
    assert len(preflight["native_proposed_cases"]) == 124
    assert files.sha256("".join(row["sha256"] for row in visible).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, old, image = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    arm, before, installed = image.read_file(ARM), old.read_file(COMMON), image.read_file(COMMON)
    assert arm == old.read_file(ARM) and files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(installed).hexdigest() == preflight["proposed_COMMON_sha256"] == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    allocator = trend.digest(arm[trend.DIRECTORY_OFFSET:trend.TABLE_OFFSET])
    former, current = (trend.owned_entries(raw, arm, allocator) for raw in (before, installed))
    assert {a.message_id for a, b in zip(former, current, strict=True) if a.text != b.text} == {review.KEY}
    image.replace_file(COMMON, before)
    assert bytes(image.rom.save()) == Path(previous["candidate"]).read_bytes()

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "tunis_advice_keeps_ARM9_and_startup_extent_exact",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    jp = trend.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    text_ref = build.panels.text_reference
    records = []
    for row in preflight["records"]:
        key = row["message_ID"]
        assert jp[key].text.hex() == row["source_hex"] and former[key].text.hex() == row["current_hex"]
        assert current[key].text.hex() == row["proposed_hex"]
        assert text_ref(current[key]) == row["proposed_reference"]
        records.append(row | dict(message_id=key, review=dict.fromkeys(files.GATES, True),
            registered_reference=text_ref(current[key]) | dict(exact_stored_hex=current[key].text.hex(), candidate_sha256=candidate)))
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(text_ref(current[row["message_ID"]]) == row["installed"] for row in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, candidate_sha256=candidate,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visible, stored_proof=files.reference(build.STORED), gameplay=files.reference(build.PAIRED),
        native_goods_cases=124, source_credit_added=0, shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


start = parent.prepare.index('        revised = [row["id"]')
record_update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
start = parent.prepare.index('    (PACKAGE / "README.md")')
readme = parent.prepare[start:parent.prepare.index('    stage.write(PACKAGE / "checksums.json"', start)]
prepare = checked_text(parent.prepare, {
    "verified_london_guild_display_predecessor=predecessor, guild_trade_numerals_release=str(REVIEW)":
        "verified_guild_trade_numerals_predecessor=predecessor, tunis_shop_advice_release=str(REVIEW)",
    "len(batches) == 1126 and len(checks) == 461": "len(batches) == 1127 and len(checks) == 462",
    record_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert revised == [f"COMMON_MESSAGE_{review.KEY}"] and len(outcome["records"]) == 4
        records[COMMON].extend(ident for ident in revised if ident not in records[COMMON])
''',
    "snapshot_scope=[ARM, COMMON]": "snapshot_scope=COMMON",
    "guild_trade_numerals_release_proof=stage.reference(stage.PROOF)": "tunis_shop_advice_release_proof=stage.reference(stage.PROOF)",
    '"guild_trade_numerals_pipeline"': '"tunis_shop_advice_pipeline"',
    "stage.SHEET, stage.PROOF, replay.OUT, PREVIEW": '''stage.SHEET, stage.PROOF, build.PAIRED, review.OUT,
        *(Path(row["path"]) for row in outcome["visual_review"][1:])''',
    "registered_manifest_entries=1127, passing_release_checks=462, changed_components=2, changed_internal_files=[ARM, COMMON]":
        "registered_manifest_entries=1128, passing_release_checks=463, changed_components=1, changed_internal_files=[COMMON]",
    "contextual_records_revisited=9, contextual_decisions_reused=5, previously_localized_records=9":
        "contextual_records_revisited=4, contextual_decisions_reused=3, previously_localized_records=4",
    "prose_revisions=4, justified_retentions=5, text_display_revisions=4": "prose_revisions=1, justified_retentions=3, text_display_revisions=1",
    "ordinary_Seoul_Guild=True, revised_gameplay_holds=2, native_pages=12, unchanged_gameplay_holds=28":
        'ordinary_Tunis_Square=True, revised_gameplay_holds=4, native_pages=124, unchanged_gameplay_holds=len(stage.read(build.PAIRED)["unchanged_frames"])',
    "prose_revisions=4, wrap_only_revisions=0, texts_retained=5": "prose_revisions=1, wrap_only_revisions=0, texts_retained=3",
    '"guild_trade_numerals_20261124"': '"tunis_shop_advice_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Tunis shop advice testing candidate

The shopkeeper politely asks sailors to sell the named goods at the Market soon. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
start = parent.finish.index("    DOC.write_text")
doc = parent.finish[start:parent.finish.index("    prefix =", start)]
finish = checked_text(parent.finish, {
    "Preserve the registered Guild trade numeral candidate": "Preserve the registered Tunis shop advice candidate",
    "1,127 entries and 462 passing checks": "1,128 entries and 463 passing checks",
    doc: '''    DOC.write_text(f"""# Tunis Delicacy Shop advice

The shopkeeper now says, **If you brought Whale Meat, please sell your stock at the Market soon.** The revised conditional keeps the original urgency and restores the courteous request. The two separate sales comments and the tentative forecast retain their wording. All 124 goods substitutions preserve the full goods name and fit on one page. [Review and five gates](../{REVIEW.as_posix()})

Normal controls from an existing Tunis save reached all three Delicacy Shops. The four revised holds have complete body and nameplate glyphs. The alternate forecast and the return to the town match the predecessor. The other goods substitutions were verified offline. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The candidate passed 463 release checks, its own startup, 17 focused regression tests and byte-exact clean-input reconstruction. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 7:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Tunis-shop-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
