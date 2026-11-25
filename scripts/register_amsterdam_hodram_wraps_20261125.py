"""Register the four ordinary-tested Amsterdam story reflows."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import stage_amsterdam_hodram_wraps_20261125 as build
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_amsterdam_hodram_wraps_replay_20261125 as gameplay
from scripts import verify_amsterdam_london_gift_20261125 as gift
from scripts import verify_seoul_tavern_accept_20261125 as seoul
from scripts.source_locked_derivation_v5118 import checked_text


parent, review = build.parent, build.review
template = parent.template
PROFILE = "all-routes-amsterdam-hodram-wraps-v1-20261125"
CHECK = "registered_amsterdam_hodram_wraps_and_complete_parent_inverse"
WORK, ROM, STORY = build.ROOT, build.ROM, build.STORY
ARM, COMMON = parent.ARM, parent.COMMON
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_amsterdam_hodram_wraps_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                   "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = build.PATCH, build.REBUILT, build.PATCH_PROOF
STARTUP_CAPTURE, QA = build.STARTUP_CAPTURE, build.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_amsterdam_hodram_wraps.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_amsterdam_hodram_wraps_registered_20261125.md")
CHECKPOINT = "Registered four reflows in Hodram's Amsterdam exchanges."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, native, clean_patch, route = map(files.read, (build.STORED, gameplay.OUT, build.OUT, PATCH_PROOF, gift.OUT))
    source = [files.read(path) for path in (review.OUT, review.APOLOGY_OUT)]
    candidate = files.digest(ROM)
    assert route["ordinary_gameplay"] and route["paired_story_holds"] == 48
    assert previous["candidate_sha256"] == stored["parent"]["sha256"] == route["candidate_sha256"]
    assert stored["candidate"] == live["candidate"] == clean_patch["candidate"] == files.reference(ROM)
    assert stored["proposal"] == live["proposal"] == files.reference(build.OUT)
    assert stored["exact_parent_inverse"] and stored["unchanged_story_directory"] and live["ordinary_gameplay"]
    assert not any(stored["format_guard"]["source_bound_new_command_counts"].values())
    assert clean_patch["byte_exact"] and clean_patch["patch"] == files.reference(PATCH)
    assert clean_patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert clean_patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    visuals = [*native["native_previews"], *live["sheets"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert len(live["revised_holds"]) == len(build.DRAFTS) == 4

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {STORY}
    assert files.sha256(after[STORY]).hexdigest() == stored["target_archive_sha256"]
    assert files.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"]
    assert files.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    jp, old_blocks, blocks = (build.IlnkContainer.parse(raw).blocks for raw in (clean.read_file(STORY), before[STORY], after[STORY]))
    assert [i for i, (a, b) in enumerate(zip(old_blocks, blocks, strict=True)) if a != b] == stored["changed_blocks"] == [44, 137]
    new.replace_file(STORY, before[STORY])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]
    layouts, observed = ({r["id"]: r for r in rows} for rows in (native["records"], live["revised_holds"]))
    assert layouts.keys() == observed.keys()
    records = []
    for packet in source:
        assert packet["candidate_sha256"] == previous["candidate_sha256"]
        for row in packet["records"]:
            key, block = row["id"], row["block"]
            src, current = row["source_reference"], row["current_reference"]
            source_at, at = src["command_offset"], current["command_offset"]
            source_bytes, was = (bytes.fromhex(item["exact_command_hex"]) for item in (src, current))
            assert jp[block][source_at:source_at + len(source_bytes)] == source_bytes
            assert old_blocks[block][at:at + len(was)] == was
            data = bytes.fromhex(layouts[key]["exact_proposed_command_hex"]) if key in layouts else was
            assert blocks[block][at:at + len(data)] == data and len(data) == len(was)
            assert source_bytes[:6] == was[:6] == data[:6]
            installed = current | dict(exact_command_hex=data.hex(), block_sha256=files.sha256(blocks[block]).hexdigest(),
                                       archive_sha256=stored["target_archive_sha256"], candidate_sha256=candidate)
            result = row | dict(installed_reference=installed, registered_reference=installed)
            if key in layouts:
                draft = layouts[key]
                assert row["decision"] == "wrap revision needed" and draft["same_extent"]
                assert draft["native_preview_sha256"] == observed[key]["native_mask_sha256"]
                result.update(english=draft["english"], localization_note=draft["localization_note"], decision="revision",
                              review=dict.fromkeys(files.GATES, True), live_revision=observed[key])
            records.append(result)
    assert len(records) == 48 and sum(row["decision"] == "retention" for row in records) == 44

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    program = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "four_Hodram_wrap_commands_and_startup_arm9_unchanged",
    })
    startup = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(program, __file__ + "::startup", "exec"), startup)
    startup["startup_proof"](previous, candidate, after[ARM])
    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = review.panels.common_rows(after[COMMON], after[ARM])
    assert all(seoul.PANELS.text_reference(common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        visual_review=visuals, target_SC1_sha256=stored["target_archive_sha256"], source_reviews=native["source_reviews"],
        gameplay=files.reference(gameplay.OUT), ordinary_gift_gameplay=files.reference(gift.OUT), stored_proof=files.reference(build.STORED),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_levelup_numerals_predecessor=predecessor, london_square_rumor_release=str(REVIEW)":
        "verified_london_square_rumor_predecessor=predecessor, amsterdam_hodram_wraps_release=str(REVIEW)",
    "len(batches) == 1149 and len(checks) == 484": "len(batches) == 1150 and len(checks) == 485",
    "assert revised == ['COMMON_MESSAGE_709']":
        "assert revised == [f'DK4_MES_B{block}_R{number:04d}' for block, number in build.DRAFTS]",
    "snapshot_scope=[COMMON]": "snapshot_scope=[STORY]",
    "london_square_rumor_release_proof": "amsterdam_hodram_wraps_release_proof",
    '"london_square_rumor_pipeline"': '"amsterdam_hodram_wraps_pipeline"',
    "gameplay.OUT, review.OUT, build.NATIVE, *(": "gameplay.OUT, review.OUT, review.APOLOGY_OUT, build.OUT, gift.OUT, *(",
    "registered_manifest_entries=1150, passing_release_checks=485, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1151, passing_release_checks=486, changed_components=1, changed_internal_files=[STORY]",
    'target_COMMON_sha256=outcome["target_COMMON_sha256"]': 'target_SC1_sha256=outcome["target_SC1_sha256"]',
    "contextual_records_revisited=16, contextual_decisions_reused=0, previously_localized_records=16":
        "contextual_records_revisited=48, contextual_decisions_reused=44, previously_localized_records=48",
    "prose_revisions=1, justified_retentions=15, text_display_revisions=0, phrase_wrap_adjustments=1":
        "prose_revisions=4, justified_retentions=44, text_display_revisions=0, phrase_wrap_adjustments=4",
    'ordinary_London_Tavern_and_Square=True, revised_gameplay_holds=2, native_pages=1, unchanged_gameplay_holds=42':
        'ordinary_Hodram_Amsterdam=True, revised_gameplay_holds=4, native_pages=4, unchanged_gameplay_holds=len(stage.read(gameplay.OUT)["exact_companion_frames"])',
    "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=15":
        "prose_revisions=4, phrase_wrap_adjustments=4, punctuation_fields=0, texts_retained=44",
    '"london_square_rumor_20261125"': '"amsterdam_hodram_wraps_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Hodram's Amsterdam story testing candidate

Four revised panels keep Lil's challenge and Gerhard's recruiting advice in complete phrases. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered London Square rumor candidate": "Preserve the registered Amsterdam story reflows",
    "1,150 entries and 485 passing checks": "1,151 entries and 486 passing checks",
    doc: '''    DOC.write_text(f"""# Hodram's Amsterdam story reflows

The candidate revises Lil's challenge and complaint and Gerhard's Mediterranean recruiting lead. All four complete native panels replayed on the original ordinary voyage. Forty-four other speeches retain their wording. The Original dialogue commands, speaker controls and archive layout carry forward. [Exact installed decisions and paired replay](../{REVIEW.as_posix()})

Independent startup, 486 release checks, 17 focused tests and exact clean-input reconstruction passed. The same ordinary voyage obtained Rainbow Marbles and verified both London gift choices on the predecessor. The Guildmaster's crimson-crystal wrap remains open with the five archived message owners and ordinary Missionary trigger. [Voyage and gift evidence](editorial_amsterdam_voyage_and_london_gift_20261125.md) · [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-Amsterdam-story", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
