"""Register the Amsterdam Guild crystal pitch after its ordinary replay."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import stage_amsterdam_guild_crystal_20261125 as build
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_seoul_tavern_accept_20261125 as seoul
from scripts.source_locked_derivation_v5118 import checked_text


parent, review, gameplay = build.current, build.draft.review, build
template = parent.template
PROFILE = "all-routes-amsterdam-guild-crystal-v1-20261125"
CHECK = "registered_amsterdam_guild_crystal_and_complete_parent_inverse"
WORK, ROM = build.ROOT, build.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_amsterdam_guild_crystal_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in (
    "registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"
))
PATCH, REBUILT, PATCH_PROOF = build.PATCH, build.REBUILT, build.PATCH_PROOF
STARTUP_CAPTURE, QA = build.STARTUP_CAPTURE, build.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_amsterdam_guild_crystal.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_amsterdam_guild_crystal_registered_20261125.md")
CHECKPOINT = "Registered the Amsterdam Guildmaster's clearer crimson-crystal pitch."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))
GUILD_LINES = {62, 1071, 1073, 1074, build.KEY}


def verify(previous, visual_sha):
    stored, live, native, patch, original = map(files.read, (build.STORED, build.OUT, build.NATIVE, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == stored["parent"]["sha256"] == live["parent"]["sha256"]
    assert stored["candidate"] == live["candidate"] == patch["candidate"] == files.reference(ROM)
    assert stored["proposal"] == live["proposal"] == files.reference(build.NATIVE)
    assert original["ordinary_gameplay"] and live["ordinary_gameplay"] and stored["exact_parent_inverse"]
    assert native["source_review"] == files.reference(review.OUT) and native["candidate_sha256"] == original["candidate_sha256"]
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert live["revised_hold"]["frame"] == build.HOLD and len(live["exact_companion_frames"]) == 16
    visuals = [*native["native_previews"], live["sheet"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    clean, predecessor, image = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(build.archive_tools.files, (predecessor, image))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    common_hash = files.sha256(after[COMMON]).hexdigest()
    assert common_hash == stored["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    image.replace_file(COMMON, before[COMMON])
    assert files.sha256(image.rom.save()).hexdigest() == previous["candidate_sha256"]
    source = build.archive_tools.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    old, new = (review.panels.common_rows(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert {a.message_id for a, b in zip(old, new, strict=True) if a != b} == {build.KEY}
    proposed, = native["records"]
    assert tuple(native["native_layouts"][-1]["lines"]) == build.draft.LINES

    def exact(entry):
        return review.panels.text_reference(entry) | {"exact_hex": entry.text.hex()}

    records = []
    for row in original["records"]:
        key = row["message_ID"]
        if key not in GUILD_LINES:
            continue
        assert row["source_reference"] == exact(source[key]) and row["installed_reference"] == exact(old[key])
        installed = exact(new[key])
        if key == build.KEY:
            assert proposed["source_reference"] == row["source_reference"] and proposed["proposed_reference"] == installed
            row = row | dict(english=proposed["english"], localization_note=proposed["localization_note"], decision="revision",
                review=dict.fromkeys(files.GATES, True), verified_revised_hold=live["revised_hold"], lines=build.draft.LINES)
        records.append(row | dict(installed_reference=installed, registered_reference=installed | dict(candidate_sha256=candidate)))
    assert len(records) == 5 and sum(row["decision"] == "retention" for row in records) == 4
    map_hold = live["retained_map_pitch"]
    assert map_hold["source_review"] == files.reference(build.MAP_REVIEW) and map_hold["frame"] == build.MAP_HOLD
    map_row, = [r for r in files.read(build.MAP_REVIEW)["records"] if r["id"] == "ARM9_GUILD_TREASURE_PITCH"]
    assert map_row["decision"] == "retention" and all(map_row["review"].values())
    map_ref = map_row["installed_reference"]
    records.append(map_row | dict(
        context="Amsterdam Guild. The Guildmaster pitches the treasure map before describing the crimson crystal.",
        current_reference=map_ref | dict(candidate_sha256=previous["candidate_sha256"]),
        installed_reference=map_ref | dict(candidate_sha256=candidate),
        registered_reference=map_ref | dict(candidate_sha256=candidate), verified_amsterdam_hold=map_hold))

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    startup = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "crystal_pitch_and_startup_arm9_unchanged",
    })
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(startup, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    for row in shared["records"]:
        key = row["message_ID"]
        assert old[key] == new[key] and seoul.PANELS.text_reference(new[key]) == row["installed"]
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        visual_review=visuals, target_COMMON_sha256=common_hash, source_review=files.reference(review.OUT),
        gameplay=files.reference(build.OUT), stored_proof=files.reference(build.STORED),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_london_square_rumor_predecessor=predecessor, amsterdam_hodram_wraps_release=str(REVIEW)":
        "verified_amsterdam_hodram_wraps_predecessor=predecessor, amsterdam_guild_crystal_release=str(REVIEW)",
    "len(batches) == 1150 and len(checks) == 485": "len(batches) == 1151 and len(checks) == 486",
    "assert revised == [f'DK4_MES_B{block}_R{number:04d}' for block, number in build.DRAFTS]":
        "assert revised == ['COMMON_MESSAGE_3661']",
    "snapshot_scope=[STORY]": "snapshot_scope=[COMMON]",
    "amsterdam_hodram_wraps_release_proof": "amsterdam_guild_crystal_release_proof",
    '"amsterdam_hodram_wraps_pipeline"': '"amsterdam_guild_crystal_pipeline"',
    "gameplay.OUT, review.OUT, review.APOLOGY_OUT, build.OUT, gift.OUT, *(":
        "gameplay.OUT, review.OUT, build.NATIVE, build.MAP_REVIEW, *(",
    "registered_manifest_entries=1151, passing_release_checks=486, changed_components=1, changed_internal_files=[STORY]":
        "registered_manifest_entries=1152, passing_release_checks=487, changed_components=1, changed_internal_files=[COMMON]",
    'target_SC1_sha256=outcome["target_SC1_sha256"]': 'target_COMMON_sha256=outcome["target_COMMON_sha256"]',
    "contextual_records_revisited=48, contextual_decisions_reused=44, previously_localized_records=48":
        "contextual_records_revisited=6, contextual_decisions_reused=5, previously_localized_records=6",
    "prose_revisions=4, justified_retentions=44, text_display_revisions=0, phrase_wrap_adjustments=4":
        "prose_revisions=1, justified_retentions=5, text_display_revisions=0, phrase_wrap_adjustments=1",
    'ordinary_Hodram_Amsterdam=True, revised_gameplay_holds=4, native_pages=4, unchanged_gameplay_holds=len(stage.read(gameplay.OUT)["exact_companion_frames"])':
        'ordinary_Amsterdam_Guild=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=16',
    "prose_revisions=4, phrase_wrap_adjustments=4, punctuation_fields=0, texts_retained=44":
        "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=5",
    '"amsterdam_hodram_wraps_20261125"': '"amsterdam_guild_crystal_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Amsterdam Guild crystal pitch testing candidate

The Guildmaster's crimson-crystal pitch keeps the description and its condition together across three lines. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Amsterdam story reflows": "Preserve the registered Amsterdam Guild crystal pitch",
    "1,151 entries and 486 passing checks": "1,152 entries and 487 passing checks",
    doc: '''    DOC.write_text(f"""# Amsterdam Guild crystal pitch

The Guildmaster now describes the crimson crystal in three complete lines and keeps the star pattern as hearsay. The revised native page replayed in ordinary gameplay. All sixteen other sampled screens match pixel for pixel. Five Guild lines retain their wording, including the treasure map pitch. [Exact installed decisions and paired replay](../{REVIEW.as_posix()})

Independent startup, 487 release checks, 17 focused tests and exact clean-input reconstruction passed. The five archived message owners, ordinary Missionary trigger, and further practical scene coverage remain open. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-Amsterdam-Guild", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
