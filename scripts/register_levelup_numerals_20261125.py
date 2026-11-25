"""Register the verified stat-gain numeral correction as a cumulative candidate."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_levelup_numerals_release_20261125 as checks
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_levelup_numerals_20261125 as runtime
from scripts import verify_levelup_numerals_20261125 as gameplay
from scripts import verify_seoul_tavern_accept_20261125 as seoul
from scripts.source_locked_derivation_v5118 import checked_text


parent = runtime.current
template, review = parent.template, parent.review
PROFILE = "all-routes-levelup-numerals-v1-20261125"
CHECK = "registered_levelup_numeral_and_complete_parent_inverse"
WORK, ROM = runtime.ROOT, runtime.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_levelup_numerals_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                   "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF
STARTUP_CAPTURE, QA = checks.STARTUP_CAPTURE, checks.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_levelup_numerals.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_levelup_numerals_registered_20261125.md")
CHECKPOINT = "Registered matching font and numeral width in the level-up notices."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=runtime.PROOF)))
build = SimpleNamespace(__file__=runtime.__file__, NATIVE=gameplay.NATIVE)
FORMAT_RECORD = "ARM9_0207E524_COMMON_336_STAT_GAIN_NUMERAL"


def verify(previous, visual_sha):
    staged, played, native, patch, original = map(files.read, (runtime.PROOF, gameplay.OUT, build.NATIVE, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == staged["parent"]["sha256"]
    assert staged["exact_parent_inverse"] and native["stat_gain_template_unchanged"]
    assert played["ordinary_gameplay"] and original["ordinary_gameplay"] and not native["ordinary_gameplay"]
    assert played["parent"] == native["parent"] == staged["parent"]
    assert played["candidate"] == staged["candidate"] == native["candidate"] == patch["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    visuals = [played["sheet"], *native["native_previews"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert len(played["exact_companion_frames"]) == 24 and native["native_pages"] == 9
    assert native["original_four_plus_two_pagination_preserved"]

    clean, predecessor, target = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(gameplay.native.files, (predecessor, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    arm, edit = runtime.proposed_arm9(clean.read_file(ARM), before[ARM])
    assert arm == after[ARM] and edit == staged["edit"]
    assert files.sha256(arm).hexdigest() == staged["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert files.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"] == staged["target_COMMON_sha256"]
    target.replace_file(ARM, before[ARM])
    assert files.sha256(target.rom.save()).hexdigest() == previous["candidate_sha256"]
    row, = [r for r in original["records"] if r["message_ID"] == 336]
    assert row["source_reference"] == native["clean_reference"] and row["current_reference"] == native["installed_reference"]
    assert row["decision"] == "wording retained, glyph revision needed" and row["review"]["formatting"] is False
    record = row | dict(file_path=COMMON, decision="retention", review=dict.fromkeys(files.GATES, True),
        localization_note="The stat comes first, followed by the exact increase. The exclamation matches the Japanese notice. The live amount now uses the same digit style as the surrounding dialogue.",
        registered_reference=row["installed_reference"] | dict(candidate_sha256=candidate),
        revised_runtime_call=edit, verified_live_numeral=files.reference(gameplay.OUT))

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "single_stat_gain_formatter_call_preserves_startup_extent",
    })
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(startup, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    inherited = files.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    rows = review.panels.common_rows(after[COMMON], arm)
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    assert all(seoul.PANELS.text_reference(rows[row["message_ID"]]) == row["installed"] for row in shared["records"])
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=[record], source_credit_added=0, candidate_sha256=candidate, visual_review=visuals,
        target_COMMON_sha256=staged["target_COMMON_sha256"], target_ARM9_sha256=staged["target_ARM9_sha256"],
        exact_ARM9_edit=edit, source_review=files.reference(review.OUT), stored_proof=files.reference(runtime.PROOF),
        native_validation=files.reference(build.NATIVE), gameplay=files.reference(gameplay.OUT),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
record_update = parent.prepare[parent.prepare.index('        revised = [row["id"]'):parent.prepare.index('        update = dict(profile=')]
prepare = checked_text(parent.prepare, {
    "verified_fleet_diversion_predecessor=predecessor, lisbon_guild_bargaining_release=str(REVIEW)":
        "verified_lisbon_guild_bargaining_predecessor=predecessor, levelup_numerals_release=str(REVIEW)",
    "len(batches) == 1147 and len(checks) == 482": "len(batches) == 1148 and len(checks) == 483",
    record_update: '''        assert all(row["decision"] == "retention" for row in outcome["records"])
        revised = [FORMAT_RECORD]
        if FORMAT_RECORD not in records[ARM]:
            records[ARM].append(FORMAT_RECORD)
''',
    "snapshot_scope=[COMMON]": "snapshot_scope=[ARM]",
    "lisbon_guild_bargaining_release_proof": "levelup_numerals_release_proof",
    '"lisbon_guild_bargaining_pipeline"': '"levelup_numerals_pipeline"',
    "registered_manifest_entries=1148, passing_release_checks=483, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1149, passing_release_checks=484, changed_components=1, changed_internal_files=[ARM]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"]':
        'target_COMMON_sha256=outcome["target_COMMON_sha256"], target_ARM9_sha256=outcome["target_ARM9_sha256"]',
    "contextual_records_revisited=11, contextual_decisions_reused=0, previously_localized_records=11":
        "contextual_records_revisited=1, contextual_decisions_reused=1, previously_localized_records=1",
    "prose_revisions=2, justified_retentions=9, text_display_revisions=0, phrase_wrap_adjustments=2":
        "prose_revisions=0, justified_retentions=1, text_display_revisions=1, phrase_wrap_adjustments=0",
    "ordinary_Lisbon_Guild=True, revised_gameplay_holds=2, native_pages=2, unchanged_gameplay_holds=23":
        "ordinary_Lisbon_Guild=True, revised_gameplay_holds=1, native_pages=9, unchanged_gameplay_holds=24",
    "prose_revisions=2, phrase_wrap_adjustments=2, punctuation_fields=0, texts_retained=9":
        "prose_revisions=0, phrase_wrap_adjustments=0, punctuation_fields=0, texts_retained=1, text_display_revisions=1",
    '"lisbon_guild_bargaining_20261125"': '"levelup_numerals_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Level-up numeral testing candidate

Stat gains use the same dialogue digits as other numeric notices. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Lisbon Guild bargaining candidate": "Preserve the registered level-up numeral candidate",
    "1,148 entries and 483 passing checks": "1,149 entries and 484 passing checks",
    doc: '''    DOC.write_text(f"""# Level-up numeral registration

Ordinary Lisbon play showed Julio's “Luck increased by 2!” with a regular dialogue digit and full punctuation. Twenty-four companion frames match the predecessor pixel for pixel. The wording and original stat and amount arguments are preserved. [Paired capture](../{VERIFY.as_posix()}/{gameplay.SHEET.name}) · [Exact source and installed review](../{REVIEW.as_posix()})

Six native cases cover nine pages, including four-plus-two pagination and supplied multi-digit stress values. Independent startup, 484 registered checks, 17 focused tests, and exact clean-input reconstruction passed. Continue the archived COMMON display owners, practical town and random coverage, and the ordinary Missionary destination trigger. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-levelup-numerals", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
