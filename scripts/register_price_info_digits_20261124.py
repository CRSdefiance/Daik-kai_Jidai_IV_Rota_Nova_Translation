"""Register the single Price Info numeral call after native and paired gameplay checks."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_lisbon_roster_galley_20261124 as parent
from scripts import stage_price_info_digits_20261124 as build
from scripts import verify_price_info_digits_replay_20261124 as gameplay
from scripts import stage_cartridge_title_20261123 as files
from scripts.source_locked_derivation_v5118 import checked_text


review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-price-info-digits-v1-20261124"
CHECK = "registered_price_info_fee_digits_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_price_info_digits_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_price_info_digits.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_price_info_digits_registered_20261124.md")
CHECKPOINT = "Registered regular fee digits in the Market Info map quote."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def verify(previous, visual_sha):
    packet, stored, live, patch = map(files.read, (build.OUT, build.STORED, gameplay.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert candidate == files.digest(REBUILT) == stored["candidate_sha256"] == live["candidate_sha256"] == packet["candidate_sha256"]
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert previous["candidate_sha256"] == packet["inherited_candidate_sha256"] == live["predecessor_sha256"] == stored["predecessor_sha256"]
    assert files.digest(files.CLEAN) == patch["clean_input_sha256"] == previous["clean_input_sha256"]
    assert stored["source_preflight"] == files.reference(build.OUT) and stored["whole_parent_inverse"]
    assert live["ordinary_gameplay"] and gameplay.observed.END in live["unchanged_frames"]
    assert live["quote"]["previous"]["cp932_full_width_amount"] and not live["quote"]["revised"]["cp932_full_width_amount"]
    assert live["quote"]["previous"]["exact_source_font_plane"] and live["quote"]["revised"]["exact_source_font_plane"]
    assert len(packet["number_cases"]) == 32 and packet["fee_range"] == [0, 50, 200]
    visible = [files.reference(gameplay.SHEET)]
    assert live["sheets"] == visible and files.sha256(visible[0]["sha256"].encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    old, new = map(files.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(parent.parent.parent.parent.trend.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    edit, = stored["instruction_changes"]
    assert edit["address"] == build.CALL
    at = build.CALL - build.BASE
    assert arm[at:at + 4].hex() == edit["after_hex"]
    assert before[ARM][at:at + 4].hex() == edit["before_hex"]
    assert arm[:at] + bytes.fromhex(edit["before_hex"]) + arm[at + 4:] == before[ARM]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    new.replace_file(ARM, before[ARM])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    startup = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Price_Info_fee_call_keeps_registered_pool_startup_exact",
    })
    exec(compile(startup, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    table = gameplay.panels.common_rows(after[COMMON], arm)
    assert all(gameplay.panels.text_reference(table[row["message_ID"]]) == row["installed"] for row in shared["records"])
    row, = packet["records"]
    outcome = dict(translation_policy=packet["translation_policy"], target_locale=packet["target_locale"],
        encoder=packet["encoder"], review_gates=packet["review_gates"],
        records=[row | dict(registered_reference=row["installed_reference"] | dict(candidate_sha256=candidate))],
        candidate_sha256=candidate, target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visible, stored_proof=files.reference(build.STORED), gameplay=files.reference(gameplay.OUT),
        fee_formatter_case_count=32, source_credit_added=0, shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_village_article_wraps_predecessor=predecessor, lisbon_roster_galley_release=str(REVIEW)":
        "verified_lisbon_roster_galley_predecessor=predecessor, price_info_digits_release=str(REVIEW)",
    "len(batches) == 1136 and len(checks) == 471": "len(batches) == 1137 and len(checks) == 472",
    'assert revised == [build.FIELD_ID, f"COMMON_MESSAGE_{build.KEY}"]': "assert revised == [build.FIELD]",
    "snapshot_scope=[ARM, COMMON]": "snapshot_scope=ARM",
    "lisbon_roster_galley_release_proof=stage.reference(stage.PROOF)": "price_info_digits_release_proof=stage.reference(stage.PROOF)",
    '"lisbon_roster_galley_pipeline"': '"price_info_digits_pipeline"',
    "registered_manifest_entries=1137, passing_release_checks=472, changed_components=2, changed_internal_files=[ARM, COMMON]":
        "registered_manifest_entries=1138, passing_release_checks=473, changed_components=1, changed_internal_files=[ARM]",
    "contextual_records_revisited=2, contextual_decisions_reused=0, previously_localized_records=2":
        "contextual_records_revisited=1, contextual_decisions_reused=0, previously_localized_records=1",
    "text_display_revisions=2, phrase_wrap_adjustments=1": "text_display_revisions=1, phrase_wrap_adjustments=0",
    "ordinary_Lisbon_crew_and_trade=True, revised_gameplay_holds=3, native_pages=1, roster_native_cases=55":
        "ordinary_Syracuse_investment_and_map=True, revised_gameplay_holds=1, native_pages=1, fee_formatter_cases=32",
    "prose_revisions=0, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=0":
        "prose_revisions=0, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=0",
    '"lisbon_roster_galley_20261124"': '"price_info_digits_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Price Info testing candidate

Market Info uses regular digits for its map quote. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Lisbon roster and Galley candidate": "Preserve the registered Price Info digits candidate",
    "1,137 entries and 472 passing checks": "1,138 entries and 473 passing checks",
    doc: '''    DOC.write_text(f"""# Regular digits in the Price Info quote

The Market Info map now displays **Syracuse: 0 coins** in the regular font. The single corrected call uses the installed ASCII numeral helper. The currency text, town substitution and fees of 0, 50 and 200 coins carry forward. Thirty-two exact native quote tests covered all formatter ring slots. [Exact source and register bindings](../{REVIEW.as_posix()})

Ordinary Syracuse play covered withdrawing an investment, paying 36,898 gold, and returning with too little gold for a second investment. Six lines retain their wording after eight complete dialogue checks. The paired candidate replay verified the revised local quote and matched all other sampled screens. [Quote comparison](../{VERIFY.as_posix()}/price_info_digits_paired.png) · [Ordinary investment evidence](../translations/editorial_checkpoints/shared_display_20261123/syracuse_investment_current_20261124.json)

The cumulative candidate passed its startup, 473 release checks, 17 focused tests and byte-exact clean-input reconstruction. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::Price-Info-digit-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
