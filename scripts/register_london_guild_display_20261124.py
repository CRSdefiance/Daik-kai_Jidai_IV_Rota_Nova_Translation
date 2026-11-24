"""Register the three London Guild revisions and their exact display evidence."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_london_guild_release_20261124 as checks
from scripts import register_yard_numerals_20261124 as parent
from scripts import replay_london_guild_display_20261124 as replay
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_london_guild_display_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-london-guild-display-v1-20261124"
CHECK = "registered_london_guild_display_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_london_guild_display_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = (build.ROOT / name for name in ("release_stack_london_guild_display.json.gz", "ledger_after.json.gz"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF, checks.STARTUP_CAPTURE
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_london_guild_display_registered_20261124.md")
CHECKPOINT = "Registered the London Guild's map pitch, buy quote, and empty sale reply."
SHEET = replay.OUT.with_name("london_guild_paired_1_20261123.png")
PREVIEW = build.OUT.with_suffix("") / "portrait_sheet_01.png"
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.OUT)))
template = parent.template


def verify(previous, visual_sha):
    stored, live, rebuilt = map(files.read, (build.OUT, replay.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert stored["candidate"] == files.reference(ROM) and live["candidate_sha256"] == candidate
    assert stored["predecessor"]["sha256"] == live["predecessor_sha256"] == previous["candidate_sha256"]
    assert stored["whole_parent_inverse"] and live["ordinary_gameplay"]
    assert rebuilt["byte_exact"] and rebuilt["candidate"]["sha256"] == files.digest(REBUILT) == candidate
    assert rebuilt["patch"] == files.reference(PATCH) and rebuilt["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert len(live["revised"]) == 4 and len(live["unchanged_frames"]) == 18
    assert [r["frame"] for r in live["revised"]] == sorted(replay.CHANGED)
    assert all(files.reference(row["path"]) == row for row in live["evidence"])
    visual = list(map(files.reference, (SHEET, PREVIEW)))
    actual, = stored["sheets"]
    assert live["sheets"] == visual[:1] and Path(actual["path"]) == PREVIEW and actual["sha256"] == visual[1]["sha256"]
    assert files.sha256("".join(row["sha256"] for row in visual).encode("ascii")).hexdigest() == visual_sha
    assert len(stored["quote_cases"]) == 201 and stored["price_domain"] == [90, 420000]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    restored, image = map(files.NdsImage.open, (previous["candidate"], ROM))
    old_arm, arm = (item.read_file(ARM) for item in (restored, image))
    old_common, common = (item.read_file(COMMON) for item in (restored, image))
    assert files.sha256(old_arm).hexdigest() == previous["target_ARM9_sha256"] and files.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert files.sha256(old_common).hexdigest() == previous["target_COMMON_sha256"] and files.sha256(common).hexdigest() == stored["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    right_bound = template.right_bound(arm, previous["right_bound_configuration"])
    assert right_bound == template.right_bound(old_arm, previous["right_bound_configuration"])
    restored_edit = bytearray(arm)
    for row in stored["exact_ARM9_edits"]:
        offset = row["offset"]
        a, b = (bytes.fromhex(row[k]) for k in ("previous_hex", "installed_hex"))
        assert len(a) == len(b) and old_arm[offset:offset + len(a)] == a and arm[offset:offset + len(b)] == b
        restored_edit[offset:offset + len(a)] = a
    assert restored_edit == old_arm
    image.replace_file(ARM, old_arm)
    image.replace_file(COMMON, old_common)
    assert bytes(image.rom.save()) == Path(previous["candidate"]).read_bytes()
    old_rows, new_rows = (build.native.yard.common_rows(a, b) for a, b in ((old_common, old_arm), (common, arm)))
    assert [b.message_id for a, b in zip(old_rows, new_rows, strict=True) if a != b] == sorted(build.EDIT)
    assert all(build.exact_row(new_rows[r["message_ID"]]) == r["staged_reference"] for r in stored["records"] if "message_ID" in r)

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Guild_literal_and_price_call_preserve_startup_extent",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(build.text_reference(new_rows[row["message_ID"]]) == row["installed"] for row in shared["records"])
    records = [row | {"registered_reference": row["staged_reference"] | {"candidate_sha256": candidate}}
               for row in stored["records"] + live["retentions"]]
    outcome = dict(translation_policy=stored["translation_policy"], target_locale=stored["target_locale"],
        encoder=stored["encoder"], review_gates=stored["review_gates"], records=records,
        candidate_sha256=candidate, predecessor_sha256=previous["candidate_sha256"],
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visual, stored_proof=files.reference(build.OUT), gameplay=files.reference(replay.OUT),
        native_price_cases=len(stored["quote_cases"]), source_credit_added=0,
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


old_record_update = parent.prepare[parent.prepare.index('        assert all(row["decision"] == "retention"'):parent.prepare.index('        update = dict(profile=')]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_nagasaki_yard_reflow_predecessor=predecessor, yard_numerals_release=str(REVIEW)":
        "verified_yard_numerals_predecessor=predecessor, london_guild_display_release=str(REVIEW)",
    "len(batches) == 1124 and len(checks) == 459": "len(batches) == 1125 and len(checks) == 460",
    "assert ARM in paths and ARM in records and CHECK not in checks": "assert {ARM, COMMON} <= set(paths) and {ARM, COMMON} <= records.keys() and CHECK not in checks",
    old_record_update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert len(revised) == 3
        for row in outcome["records"]:
            if row["decision"] == "revision" and row["id"] not in records[row["file_path"]]:
                records[row["file_path"]].append(row["id"])
        records[ARM].append("ARM9_GUILD_BUY_NUMERAL_BRANCH")
''',
    "snapshot_scope=ARM": "snapshot_scope=[ARM, COMMON]",
    'yard_numerals_release_proof=stage.reference(stage.PROOF), native_patch=outcome["native_patch_module"], visual_review=outcome["visual_review"]':
        'london_guild_display_release_proof=stage.reference(stage.PROOF), visual_review=outcome["visual_review"]',
    '"yard_numerals_pipeline"': '"london_guild_display_pipeline"',
    "stage.SHEET, stage.PROOF, build.PAIRED, PREVIEW, native.OUT": "stage.SHEET, stage.PROOF, replay.OUT, PREVIEW",
    "registered_manifest_entries=1125, passing_release_checks=460, changed_components=1, changed_internal_files=[ARM]":
        "registered_manifest_entries=1126, passing_release_checks=461, changed_components=2, changed_internal_files=[ARM, COMMON]",
    "contextual_records_revisited=13, contextual_decisions_reused=13, previously_localized_records=13":
        "contextual_records_revisited=7, contextual_decisions_reused=4, previously_localized_records=7",
    "prose_revisions=0, justified_retentions=13, text_display_revisions=13":
        "prose_revisions=3, justified_retentions=4, text_display_revisions=3",
    "ordinary_Nagasaki_Yard=True, revised_gameplay_holds=2, native_pages=15, unchanged_gameplay_holds=53":
        "ordinary_London_Guild=True, revised_gameplay_holds=4, native_pages=6, unchanged_gameplay_holds=18",
    "prose_revisions=0, wrap_only_revisions=0, texts_retained=13": "prose_revisions=3, wrap_only_revisions=0, texts_retained=4",
    '"yard_numerals_20261124"': '"london_guild_display_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# London Guild testing candidate

The old map pitch, buy quote and sale refusal use complete, readable lines. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Yard numeral candidate": "Preserve the registered London Guild candidate",
    "1,125 entries and 460 passing checks": "1,126 entries and 461 passing checks",
    doc: '''    DOC.write_text(f"""# London Guild dialogue and prices

The Guildmaster's old map pitch restores that he has the map and presents the rumor in two complete lines. The purchase question keeps the displayed amount together with the buy decision and uses regular dialogue digits. The empty sale reply reads in one line. Four companion turns retain their wording. [Exact records and five review gates](../{REVIEW.as_posix()})

Ordinary London play verified the revised pitch, the 11,000-coin Loom quote, the 3,000-coin map quote and the empty sale reply. Eighteen companion frames match pixel for pixel. The player declined the Loom, bought the map for the original 3,000 coins, found nothing eligible to sell and returned to London. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [Native previews](../{VERIFY.as_posix()}/{PREVIEW.name})

The candidate passed 201 native price layouts, six startup holds, 461 release checks and 17 focused repository tests. Its clean-input patch reconstructs the complete ROM. A successful sale and the insufficient-funds response remain unvisited in this replay. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent.parent.parent.parent.parent) | vars(parent.parent.parent.parent) | vars(parent.parent.parent) | vars(parent.parent) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::London-Guild-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
