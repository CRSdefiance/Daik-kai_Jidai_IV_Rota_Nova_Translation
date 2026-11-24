"""Register the Tavern reflow and repaired region argument with paired gameplay."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_maria_captured_ship_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_istanbul_tavern_rumor_20261124 as build
from scripts.source_locked_derivation_v5118 import checked_text


review = build.review
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-istanbul-tavern-rumor-v1-20261124"
CHECK = "registered_istanbul_tavern_rumor_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_istanbul_tavern_rumor_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_istanbul_tavern_rumor.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_istanbul_tavern_rumor_registered_20261124.md")
CHECKPOINT = "Registered the Istanbul Tavern rumor reflow and restored the Indian Ocean substitution."
SHEET = build.SHEET
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))
template = parent.template


def verify(previous, visual_sha):
    stored, live, rebuilt, preflight = map(files.read, (build.STORED, build.PAIRED, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert candidate == stored["candidate_sha256"] == live["candidate_sha256"] == files.digest(REBUILT)
    assert rebuilt["byte_exact"] and rebuilt["candidate"]["sha256"] == candidate and rebuilt["patch"] == files.reference(PATCH)
    assert files.digest(files.CLEAN) == rebuilt["clean_input_sha256"] == previous["clean_input_sha256"]
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == live["predecessor_sha256"] == preflight["candidate_sha256"]
    assert stored["whole_parent_inverse"] and stored["changed_message"] == review.KEY
    assert live["ordinary_saved_game"] and live["source_preflight"] == stored["source_preflight"] == files.reference(review.OUT)
    assert live["tavern"]["frame"] == review.HOLD and live["guild"]["frame"] == build.LONDON_HOLD
    assert build.END in live["tavern"]["unchanged_frames"] and build.LONDON_END in live["guild"]["unchanged_frames"]
    assert live["tavern"]["before"] == files.reference(build.BEFORE) and live["tavern"]["after"] == files.reference(build.AFTER)
    for label, member in (("parent", "before"), ("candidate", "after")):
        assert live["guild"][member] == files.reference(build.london_report(label))
    native = preflight["native"]
    assert native["tested_cases"] == 242 and native["other_rumor_region_cases"] == 121
    assert tuple(native["proposed"]) == review.REGIONS and native["previous"][3] == "reasure."
    visual = [files.reference(SHEET), *(files.reference(row["path"]) for row in preflight["proposed_sheets"])]
    assert live["sheets"] == visual[:1]
    assert [row["sha256"] for row in visual[1:]] == [row["sha256"] for row in preflight["proposed_sheets"]]
    assert files.sha256("".join(row["sha256"] for row in visual).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, old, image = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    old_arm, arm = (item.read_file(ARM) for item in (old, image))
    before, installed = (item.read_file(COMMON) for item in (old, image))
    assert files.sha256(old_arm).hexdigest() == previous["target_ARM9_sha256"] == preflight["current_ARM9_sha256"]
    assert files.sha256(arm).hexdigest() == stored["target_ARM9_sha256"] == preflight["proposed_ARM9_sha256"]
    assert files.sha256(before).hexdigest() == previous["target_COMMON_sha256"]
    assert files.sha256(installed).hexdigest() == stored["target_COMMON_sha256"] == preflight["proposed_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"]) == template.right_bound(old_arm, previous["right_bound_configuration"])
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    expected, edits, pitch, _, _ = review.proposed_arm(clean.read_file(ARM), old_arm)
    assert arm == expected and edits == stored["exact_ARM9_edits"] == preflight["exact_ARM9_edits"]
    image.replace_file(ARM, old_arm)
    image.replace_file(COMMON, before)
    assert files.sha256(image.rom.save()).hexdigest() == previous["candidate_sha256"]
    del image, old
    former, current = (review.athens.common_rows(raw, main) for raw, main in ((before, old_arm), (installed, arm)))
    assert [b.message_id for a, b in zip(former, current, strict=True) if a != b] == [review.KEY]
    jp = review.guild.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    del clean
    records = []
    for row in preflight["records"]:
        if "message_ID" in row:
            key = row["message_ID"]
            assert row["source_reference"] == review.exact_entry(jp[key])
            assert row["current_reference"] == review.exact_entry(former[key])
            assert row["proposed_reference"] == review.exact_entry(current[key])
        else:
            assert row["id"] == "ARM9_GUILD_TREASURE_PITCH" and row["proposed_reference"]["exact_hex"] == pitch.hex()
        records.append(row | dict(registered_reference=row["proposed_reference"] | dict(candidate_sha256=candidate)))

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Tavern_text_edits_preserve_startup_extent",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    snapshot = files.read(STARTUP)["read_only_snapshot"]
    with Path(snapshot["path"]).open("rb") as data:
        for row in edits:
            expected = bytes.fromhex(row["installed_hex"])
            data.seek(row["offset"])
            assert data.read(len(expected)) == expected

    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    assert all(build.panels.text_reference(current[row["message_ID"]]) == row["installed"] for row in shared["records"])
    outcome = dict(translation_policy=preflight["translation_policy"], target_locale=preflight["target_locale"],
        encoder=preflight["encoder"], review_gates=preflight["review_gates"], records=records,
        candidate_sha256=candidate, target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visual, stored_proof=files.reference(build.STORED), gameplay=files.reference(build.PAIRED),
        native_rumor_cases=native["tested_cases"], region_provider=preflight["region_provider"],
        source_credit_added=0, shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


start = parent.prepare.index('        revised = [row["id"]')
old_update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_tunis_palace_refusal_predecessor=predecessor, maria_captured_ship_release=str(REVIEW)":
        "verified_maria_captured_ship_predecessor=predecessor, istanbul_tavern_rumor_release=str(REVIEW)",
    "len(batches) == 1129 and len(checks) == 464": "len(batches) == 1130 and len(checks) == 465",
    old_update: '''        revised = [row for row in outcome["records"] if row["decision"] == "revision"]
        assert [row["id"] for row in revised] == [f"COMMON_MESSAGE_{review.KEY}", "ARM9_GUILD_TREASURE_PITCH"]
        assert len(outcome["records"]) == 13
        for row in revised:
            if row["id"] not in records[row["file_path"]]:
                records[row["file_path"]].append(row["id"])
        records[ARM].append("ARM9_TAVERN_INDIAN_OCEAN_ARGUMENT")
''',
    "snapshot_scope=COMMON": "snapshot_scope=[ARM, COMMON]",
    "maria_captured_ship_release_proof=stage.reference(stage.PROOF)": "istanbul_tavern_rumor_release_proof=stage.reference(stage.PROOF)",
    '"maria_captured_ship_pipeline"': '"istanbul_tavern_rumor_pipeline"',
    "registered_manifest_entries=1130, passing_release_checks=465, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1131, passing_release_checks=466, changed_components=2, changed_internal_files=[ARM, COMMON]",
    "contextual_records_revisited=7, contextual_decisions_reused=6, previously_localized_records=7":
        "contextual_records_revisited=13, contextual_decisions_reused=11, previously_localized_records=13",
    "prose_revisions=1, justified_retentions=6, text_display_revisions=1":
        "prose_revisions=2, justified_retentions=11, text_display_revisions=3",
    'ordinary_Maria_Nagasaki_duel=True, revised_gameplay_holds=1, native_pages=29, unchanged_gameplay_holds=len(stage.read(build.PAIRED)["unchanged_frames"])':
        'ordinary_Istanbul_Tavern_and_London_Guild=True, revised_gameplay_holds=2, native_pages=8, '
        'unchanged_gameplay_holds=sum(len(stage.read(build.PAIRED)[label]["unchanged_frames"]) for label in ("tavern", "guild"))',
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=6": "prose_revisions=2, wrap_only_revisions=0, texts_retained=11",
    '"maria_captured_ship_20261124"': '"istanbul_tavern_rumor_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Istanbul Tavern rumor testing candidate

The patron keeps the rare treasure and the item name together. Tavern rumors restore the Indian Ocean phrase and the Guildmaster still offers his old map. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Maria captured-ship candidate": "Preserve the registered Istanbul Tavern rumor candidate",
    "1,130 entries and 465 passing checks": "1,131 entries and 466 passing checks",
    doc: '''    DOC.write_text(f"""# Istanbul Tavern rumor and Indian Ocean substitution

After Hodram buys a round, the patron thanks him and offers a tip about the rare treasure. The revised rumor keeps every item and region name together across all 242 native cases. **They say** preserves the hearsay. Eleven surrounding Tavern records retain their wording. [Exact records and review gates](../{REVIEW.as_posix()})

The region provider returned **reasure.** instead of **the Indian Ocean** because its pointer landed in the Guild map pitch. The Guildmaster now says **I have an old map**. The two-line offer and all seven region phrases fit in their existing allocations. Both rumor consumers passed offline checks. Ordinary paired gameplay verified the Black Rapier rumor and the London Guild's map pitch, with all other sampled holds matching. Indian Ocean variants were verified offline. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name})

The candidate passed 466 release checks, its own cold boot, 17 focused regression tests and byte-exact reconstruction from the clean input. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 10:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::Istanbul-Tavern-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
