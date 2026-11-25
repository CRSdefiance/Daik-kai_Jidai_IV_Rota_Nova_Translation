"""Register the source-reviewed and replayed London Square rumor."""

from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile as copy_rom
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_lisbon_guild_bargaining_20261125 as common_workflow
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_london_square_rumor_20261125 as runtime
from scripts import verify_london_square_rumor_replay_20261125 as gameplay
from scripts import verify_seoul_tavern_accept_20261125 as seoul
from scripts.source_locked_derivation_v5118 import checked_text


parent, review = runtime.current, runtime.review
template = parent.template
PROFILE = "all-routes-london-square-rumor-v1-20261125"
CHECK = "registered_london_square_rumor_and_complete_parent_inverse"
WORK = runtime.ROOT
DELIVERY = Path(".codex-release-work/london_square_rumor_delivery_20261125").resolve()
ROM = DELIVERY / "London_Square_Rumor.nds"
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_london_square_rumor_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                   "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = runtime.PATCH, runtime.REBUILT, runtime.PATCH_PROOF
STARTUP_CAPTURE, QA = runtime.STARTUP_CAPTURE, runtime.QA
STARTUP = DELIVERY / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = DELIVERY / "release_stack_london_square_rumor.json.gz", DELIVERY / "ledger_after.json.gz"
DOC = Path("docs/editorial_london_square_rumor_registered_20261125.md")
CHECKPOINT = "Registered the clearer Clifford rumor seen in London Square."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=runtime.STAGED)))
build = SimpleNamespace(__file__=runtime.__file__, NATIVE=runtime.NATIVE)


def verify(previous, visual_sha):
    staged, played, native, patch, original = map(files.read, (runtime.STAGED, gameplay.OUT, runtime.NATIVE, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == staged["parent"]["sha256"] == original["candidate_sha256"] == native["candidate_sha256"]
    assert played["candidate"] == staged["candidate"] == patch["candidate"] == files.reference(runtime.ROM)
    assert staged["candidate"]["sha256"] == candidate
    assert staged["proposal"] == played["preflight"] == files.reference(runtime.NATIVE)
    assert played["source_review"] == native["source_review"] == files.reference(review.OUT)
    assert staged["exact_parent_inverse"] and patch["byte_exact"] and played["ordinary_gameplay"] and original["ordinary_gameplay"]
    assert patch["patch"] == files.reference(PATCH) and patch["rebuilt"] == files.reference(REBUILT)
    assert files.digest(REBUILT) == candidate and patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    assert set(played["exact_companion_frames"]) == set(runtime.FRAMES) - runtime.CHANGED
    assert {r["frame"] for r in played["revised_holds"]} == runtime.CHANGED
    visuals = [*native["native_previews"], *original["sheets"], played["sheet"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    predecessor, target = (files.NdsImage.open(path) for path in (previous["candidate"], ROM))
    before, after = map(runtime.town.files, (predecessor, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert files.sha256(after[COMMON]).hexdigest() == staged["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    target.replace_file(COMMON, before[COMMON])
    assert files.sha256(target.rom.save()).hexdigest() == previous["candidate_sha256"]
    old, new = (review.panels.common_rows(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert {a.message_id for a, b in zip(old, new, strict=True) if a != b} == {runtime.KEY}
    draft, = native["records"]
    assert tuple(draft["native_layouts"][-1]["lines"]) == runtime.LINES

    def exact(row):
        return review.panels.text_reference(row) | {"exact_hex": row.text.hex()}

    records = []
    for row in original["records"]:
        key = row["message_ID"]
        assert row["installed_reference"] == exact(old[key])
        installed = exact(new[key])
        if key == runtime.KEY:
            assert draft["source_reference"] == row["source_reference"] and draft["proposed_reference"] == installed
            row = row | dict(english=draft["english"], localization_note=draft["localization_note"], decision="revision",
                review=dict.fromkeys(files.GATES, True), verified_revised_holds=played["revised_holds"], lines=runtime.LINES)
        records.append(row | dict(installed_reference=installed, registered_reference=installed | dict(candidate_sha256=candidate)))
    assert len(records) == 16 and sum(row["decision"] == "retention" for row in records) == 15
    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_Square_rumor_and_startup_arm9_unchanged",
    })
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(startup, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    inherited = files.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    for row in shared["records"]:
        key = row["message_ID"]
        assert old[key] == new[key] and seoul.PANELS.text_reference(new[key]) == row["installed"]
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate, visual_review=visuals,
        target_COMMON_sha256=staged["target_COMMON_sha256"], source_review=files.reference(review.OUT),
        stored_proof=files.reference(runtime.STAGED), gameplay=files.reference(gameplay.OUT),
        verified_candidate_delivery=files.reference(ROM),
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = common_workflow.prepare[
    common_workflow.prepare.index('    (PACKAGE / "README.md")'):common_workflow.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = common_workflow.finish[common_workflow.finish.index("    DOC.write_text"):common_workflow.finish.index("    prefix =")]
prepare = checked_text(common_workflow.prepare, {
    "verified_fleet_diversion_predecessor=predecessor, lisbon_guild_bargaining_release=str(REVIEW)":
        "verified_levelup_numerals_predecessor=predecessor, london_square_rumor_release=str(REVIEW)",
    "len(batches) == 1147 and len(checks) == 482": "len(batches) == 1149 and len(checks) == 484",
    "assert revised == ['COMMON_MESSAGE_1080', 'COMMON_MESSAGE_1092']": "assert revised == ['COMMON_MESSAGE_709']",
    "lisbon_guild_bargaining_release_proof": "london_square_rumor_release_proof",
    '"lisbon_guild_bargaining_pipeline"': '"london_square_rumor_pipeline"',
    "registered_manifest_entries=1148, passing_release_checks=483": "registered_manifest_entries=1150, passing_release_checks=485",
    "contextual_records_revisited=11, contextual_decisions_reused=0, previously_localized_records=11":
        "contextual_records_revisited=16, contextual_decisions_reused=0, previously_localized_records=16",
    "prose_revisions=2, justified_retentions=9, text_display_revisions=0, phrase_wrap_adjustments=2":
        "prose_revisions=1, justified_retentions=15, text_display_revisions=0, phrase_wrap_adjustments=1",
    "ordinary_Lisbon_Guild=True, revised_gameplay_holds=2, native_pages=2, unchanged_gameplay_holds=23":
        f"ordinary_London_Tavern_and_Square=True, revised_gameplay_holds=2, native_pages=1, unchanged_gameplay_holds={len(runtime.FRAMES) - len(runtime.CHANGED)}",
    "prose_revisions=2, phrase_wrap_adjustments=2, punctuation_fields=0, texts_retained=9":
        "prose_revisions=1, phrase_wrap_adjustments=1, punctuation_fields=0, texts_retained=15",
    '"lisbon_guild_bargaining_20261125"': '"london_square_rumor_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# London Square rumor testing candidate

The Shopkeeper's rumor about Clifford now keeps three complete thoughts together. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(common_workflow.finish, {
    "Preserve the registered Lisbon Guild bargaining candidate": "Preserve the registered London Square rumor candidate",
    "1,148 entries and 483 passing checks": "1,150 entries and 485 passing checks",
    doc: '''    DOC.write_text(f"""# London Tavern and Square checkpoint

Ordinary play tested both replies to Manuel's 303-gold offer. Accepting deducted exactly 303 gold, and declining left the balance at 40,351. Marie's tease after declining the second drink and the patron's Clifford rumor displayed in full. Food, Spice, Gem and Textile Shop visits sampled four responses, including two natural draws of the local story about Clifford's knighthood. [Source, installed text and ordinary inputs](../{VERIFY.as_posix()}/{review.OUT.name})

Clifford's pirate past, current naval rank and reported knighthood now each occupy a complete line. Both original holds replayed with the exact new glyphs and Shopkeeper name. Fifteen companion texts retain their wording. [Paired panels](../{VERIFY.as_posix()}/{gameplay.SHEET.name}) · [Registered record ledger](../{REVIEW.as_posix()})

Independent startup, 485 release checks, 17 focused tests and exact clean-input reconstruction passed. Marie's gift, the other Tavern rumors and Square Trends details remain unvisited in this replay. Continue the five archived COMMON display owners, the ordinary Missionary destination trigger, and further practical town and random coverage. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-London-Square", "exec"), scope)
    if not args.finish_only:
        DELIVERY.mkdir(exist_ok=True)
        tested = files.read(runtime.STAGED)["candidate"]
        assert files.reference(runtime.ROM) == tested
        if not ROM.exists():
            copy_rom(runtime.ROM, ROM)
        assert files.digest(ROM) == tested["sha256"]
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
