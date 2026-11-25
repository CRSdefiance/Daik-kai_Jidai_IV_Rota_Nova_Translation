"""Register Julio's two verified bargaining replies as a cumulative candidate."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_lisbon_guild_bargaining_release_20261125 as checks
from scripts import preflight_lisbon_guild_bargaining_20261125 as draft
from scripts import register_fleet_diversion_20261125 as parent
from scripts import replay_lisbon_guild_bargaining_20261125 as replay
from scripts import stage_cartridge_title_20261123 as files
from scripts import verify_lisbon_guild_bargaining_replay_20261125 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text


review, template = draft.review, parent.template
PROFILE = "all-routes-lisbon-guild-bargaining-v1-20261125"
CHECK = "registered_lisbon_guild_bargaining_and_complete_parent_inverse"
WORK, ROM = replay.ROOT, replay.ROM
ARM, COMMON, STORY = parent.ARM, parent.COMMON, parent.STORY
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261125_lisbon_guild_bargaining_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in ("registered_review.json", "registered_release_verification.json",
                                                   "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF = checks.PATCH, checks.REBUILT, checks.PATCH_PROOF
STARTUP_CAPTURE, QA = checks.STARTUP_CAPTURE, checks.QA
STARTUP = WORK / "own_startup_verification.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_lisbon_guild_bargaining.json.gz", WORK / "ledger_after.json.gz"
DOC = Path("docs/editorial_lisbon_guild_bargaining_registered_20261125.md")
CHECKPOINT = "Registered Julio's clearer purchase and sale bargaining lines."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=replay.STAGED)))
build = SimpleNamespace(__file__=replay.__file__, NATIVE=draft.OUT)


def verify(previous, visual_sha):
    staged, played, native, patch, original = map(files.read, (replay.STAGED, gameplay.OUT, draft.OUT, PATCH_PROOF, review.OUT))
    candidate = files.digest(ROM)
    assert previous["candidate_sha256"] == native["candidate_sha256"] == original["candidate_sha256"] == staged["parent"]["sha256"]
    assert staged["exact_parent_inverse"] and native["all_placements_same_allocation"]
    assert played["ordinary_gameplay"] and original["ordinary_gameplay"]
    assert played["proposal"] == staged["proposal"] == files.reference(draft.OUT)
    assert played["baseline"] == files.reference(review.OUT)
    assert played["candidate"] == staged["candidate"] == patch["candidate"] == files.reference(ROM)
    assert patch["byte_exact"] and patch["patch"] == files.reference(PATCH)
    assert patch["rebuilt"] == files.reference(REBUILT) and files.digest(REBUILT) == candidate
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == files.digest(files.CLEAN)
    visuals = [*native["native_previews"], *original["sheets"], played["sheet"]]
    assert all(files.digest(row["path"]) == row["sha256"] for row in visuals)
    assert files.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha
    assert len(played["exact_companion_frames"]) == 23 and list(played["observed_wallets"].values()) == [26995, 17195, 25395]

    predecessor, target = (files.NdsImage.open(path) for path in (previous["candidate"], ROM))
    before, after = map(draft.native.files, (predecessor, target))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {COMMON}
    arm = after[ARM]
    assert files.sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert files.sha256(after[COMMON]).hexdigest() == staged["target_COMMON_sha256"] == native["proposed_COMMON_sha256"]
    target.replace_file(COMMON, before[COMMON])
    assert files.sha256(target.rom.save()).hexdigest() == previous["candidate_sha256"]
    old, new = (review.panels.common_rows(archive, arm) for archive in (before[COMMON], after[COMMON]))
    assert {a.message_id for a, b in zip(old, new, strict=True) if a.text != b.text} == draft.DRAFTS.keys()
    drafts = {row["message_ID"]: row for row in native["records"]}
    holds = {row["message_ID"]: row for row in played["revised_holds"]}
    assert holds.keys() == drafts.keys() == draft.DRAFTS.keys()

    def exact(row):
        return review.panels.text_reference(row) | {"exact_hex": row.text.hex()}

    records = []
    for row in original["records"]:
        key = row["message_ID"]
        if key == review.GROWTH:
            assert row["review"]["formatting"] is False and old[key].text == new[key].text
            continue
        installed = exact(new[key])
        assert row["installed_reference"] == exact(old[key])
        if key in drafts:
            revision, hold = drafts[key], holds[key]
            assert revision["source_reference"] == row["source_reference"] and revision["proposed_reference"] == installed
            assert hold["proposed_lines"] == revision["native_layouts"][-1]["lines"]
            row = row | dict(english=revision["english"], localization_note=revision["localization_note"],
                decision="revision", verified_revised_hold=hold, review=dict.fromkeys(files.GATES, True))
        records.append(row | dict(file_path=COMMON, installed_reference=installed,
                                  registered_reference=installed | dict(candidate_sha256=candidate)))
    assert len(records) == 11 and sum(row["decision"] == "retention" for row in records) == 9

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(name, "0")) for name in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    startup = checked_text(template.previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "original_arm9_and_protected_runtime_checks_pass",
    })
    scope = template.previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    exec(compile(startup, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)
    inherited = files.read(parent.REVIEW)
    shared = inherited["shared_consumer_binding"]
    assert shared["candidate_sha256"] == previous["candidate_sha256"] and len(shared["records"]) == 276
    for row in shared["records"]:
        key = row["message_ID"]
        assert key not in holds and old[key].text == new[key].text
        assert parent.parent.review.PANELS.text_reference(old[key]) == row["installed"]
        row["installed"] = parent.parent.review.PANELS.text_reference(new[key])
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate, visual_review=visuals,
        target_COMMON_sha256=staged["target_COMMON_sha256"], source_review=files.reference(review.OUT),
        stored_proof=files.reference(replay.STAGED), gameplay=files.reference(gameplay.OUT),
        separate_growth_glyph_lead=original["stat_growth_glyph_lead"],
        shared_consumer_binding=shared | {"candidate_sha256": candidate},
        retained_four_route_census_sha256=inherited["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=inherited["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_seoul_reika_predecessor=predecessor, fleet_diversion_release=str(REVIEW)":
        "verified_fleet_diversion_predecessor=predecessor, lisbon_guild_bargaining_release=str(REVIEW)",
    "len(batches) == 1146 and len(checks) == 481": "len(batches) == 1147 and len(checks) == 482",
    "assert revised == ['COMMON_MESSAGE_923', 'COMMON_MESSAGE_926']": "assert revised == ['COMMON_MESSAGE_1080', 'COMMON_MESSAGE_1092']",
    "fleet_diversion_release_proof": "lisbon_guild_bargaining_release_proof",
    '"fleet_diversion_pipeline"': '"lisbon_guild_bargaining_pipeline"',
    "registered_manifest_entries=1147, passing_release_checks=482": "registered_manifest_entries=1148, passing_release_checks=483",
    "contextual_records_revisited=6, contextual_decisions_reused=0, previously_localized_records=6":
        "contextual_records_revisited=11, contextual_decisions_reused=0, previously_localized_records=11",
    "prose_revisions=2, justified_retentions=4": "prose_revisions=2, justified_retentions=9",
    "focused_Lure_Fleet_fixture=True, revised_gameplay_holds=2, native_pages=2, unchanged_gameplay_holds=14":
        "ordinary_Lisbon_Guild=True, revised_gameplay_holds=2, native_pages=2, unchanged_gameplay_holds=23",
    "prose_revisions=2, phrase_wrap_adjustments=2, punctuation_fields=0, texts_retained=4":
        "prose_revisions=2, phrase_wrap_adjustments=2, punctuation_fields=0, texts_retained=9",
    '"fleet_diversion_20261125"': '"lisbon_guild_bargaining_20261125"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Lisbon Guild bargaining testing candidate

Julio's questions read in complete phrases while the Guildmaster's prices keep regular digits. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate}.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Lure Fleet candidate": "Preserve the registered Lisbon Guild bargaining candidate",
    "1,147 entries and 482 passing checks": "1,148 entries and 483 passing checks",
    doc: '''    DOC.write_text(f"""# Lisbon Guild bargaining registration

In ordinary Lisbon play, Julio's purchase and sale replies keep both questions intact. The Guildmaster still charged 9,800 for the book and paid 8,200 on resale. Nine companion texts retain their wording. The two revised pages and 23 matching companion screens passed. [Paired capture](../{VERIFY.as_posix()}/{gameplay.SHEET.name}) · [Exact source and installed review](../{REVIEW.as_posix()})

The cumulative candidate passed independent startup, 483 registered checks, 17 focused tests and exact clean-input reconstruction. The separate full-width stat gain in COMMON 336, five archived display owners and ordinary Missionary trigger remain open. [Testing package](../{PACKAGE.as_posix()}/README.md) · [Ordinary exchange and glyph finding](editorial_lisbon_guild_bargaining_current_20261125.md)
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
    exec(compile(prepare + "\n" + finish, __file__ + "::register-lisbon-guild-bargaining", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
