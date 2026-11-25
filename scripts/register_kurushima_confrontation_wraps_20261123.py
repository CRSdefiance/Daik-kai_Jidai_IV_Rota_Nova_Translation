"""Register the source-reviewed Kurushima confrontation after native and live checks."""

from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_kurushima_confrontation_wraps_20261123 as played
from scripts import register_cartridge_title_20261123 as template
from scripts import register_nagasaki_dream_20261123 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_kurushima_confrontation_wraps_20261123 as build
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_moonlit_violin_20261121 import bytes_for


PROFILE = "all-routes-kurushima-confrontation-wraps-v1-20261123"
CHECK = "registered_kurushima_confrontation_native_pages_and_complete_parent_inverse"
STORY, COMMON, ARM = build.STORY, build.COMMON, build.ARM
WORK, ROM = build.ROOT, build.ROM
PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE = build.PATCH, build.PATCH_PROOF, build.REBUILT, build.STARTUP_CAPTURE
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_kurushima_confrontation_wraps_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
PLAN = VERIFY / "registration_mutation_plan.json"
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = WORK / "release_stack_kurushima_confrontation.json.gz", WORK / "ledger_after.json.gz"
STARTUP, QA = WORK / "own_startup_verification.json", WORK / "qa_passed.xml"
DOC = Path("docs/editorial_kurushima_confrontation_wraps_registered_20261123.md")
CHECKPOINT = "Registered two wording edits and one wrap fix in Maria's confrontation with Kurushima."
SHEET, PREVIEW = played.SHEET, played.PREVIEW
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, SHEET=SHEET, PROOF=build.STORED)))


def verify(previous, visual_sha):
    stored, live, native, patch = map(stage.read, (build.STORED, played.PAIRED, played.NATIVE, PATCH_PROOF))
    candidate = stage.digest(ROM)
    assert candidate == stored["candidate"]["sha256"] == live["candidate_sha256"] == native["candidate_sha256"] == stage.digest(REBUILT)
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and stage.reference(PATCH) == patch["patch"]
    assert patch["clean_input_sha256"] == previous["clean_input_sha256"] == stored["clean"]["sha256"] == stage.digest(stage.CLEAN)
    assert previous["candidate_sha256"] == stored["previous"]["sha256"] == live["previous_sha256"]
    assert stored["whole_parent_inverse"] and stage.reference(played.review.OUT) == stored["source_review"]
    assert stage.reference(played.NATIVE) == live["native"] and stage.reference(build.STORED) == native["stored"]
    assert live["ordinary_replay"] and live["sea_return_exact"] and len(live["identical_control_frames"]) == 12
    assert len(live["revised_pages"]) == 3 and native["complete_native_pages"] == 6
    assert stage.reference(played.BEFORE) == live["baseline"] and stage.reference(played.AFTER) == live["replay"]
    visuals = [stage.reference(SHEET), stage.reference(PREVIEW)]
    assert visuals == [live["visual"], native["visual"]]
    assert stage.sha256("".join(row["sha256"] for row in visuals).encode("ascii")).hexdigest() == visual_sha

    old, new = map(stage.NdsImage.open, (previous["candidate"], ROM))
    before, after = map(build.native.files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {STORY}
    assert stage.sha256(after[ARM]).hexdigest() == previous["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert stage.sha256(after[COMMON]).hexdigest() == previous["target_COMMON_sha256"] == stored["target_COMMON_sha256"]
    assert stage.sha256(after[STORY]).hexdigest() == stored["target_SC3_sha256"]
    assert template.right_bound(after[ARM], previous["right_bound_configuration"])["matched_repair_spans"] == 8
    archives = [build.IlnkContainer.parse(data[STORY]).blocks for data in (before, after)]
    assert [i for i, (a, b) in enumerate(zip(*archives, strict=True)) if a != b] == [build.BLOCK]
    block = archives[1][build.BLOCK]
    assert stage.sha256(block).hexdigest() == stored["target_block_sha256"]
    new.replace_file(STORY, before[STORY])
    assert bytes(new.rom.save()) == Path(previous["candidate"]).read_bytes()

    suite, = template.ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "one_Kurushima_block_and_startup_arm9_unchanged",
    })
    exec(compile(source, __file__ + "::startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, after[ARM])

    commands = {ident: r for r in stored["commands"] for ident in r["record_ids"]}
    rendered = {r["id"]: r for r in native["records"]}
    witnessed = {r["id"]: r for r in live["revised_pages"]}
    assert len(commands) == 8 and set(rendered) == set(witnessed) == set(stored["changed_ids"])
    records = []
    for row in stored["records"]:
        ident = row["id"]
        command = commands[ident]
        data = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert block[at:at + len(data)] == data
        assert row["source_reference"]["complete_command_hex"] == command["source"]
        assert row["current_reference"]["complete_command_hex"] == command["current"]
        assert " ".join(bytes_for(data).decode("ascii").split()) == row["english"]
        display = rendered.get(ident)
        if display:
            assert row["decision"] == "revision"
            first = display["layouts"][0]
            assert first["lines"] == witnessed[ident]["lines"]
            assert stage.sha256(bytes.fromhex(first["pages"][0]["native_plane_hex"])).hexdigest() == witnessed[ident]["full_native_plane_sha256"]
        else:
            assert row["decision"] == "retention" and command["current"] == command["stored"]
        installed = dict(file_path=STORY, block=build.BLOCK, command_offset=at, complete_command_hex=data.hex(),
            candidate_sha256=candidate, archive_sha256=stored["target_SC3_sha256"], block_sha256=stored["target_block_sha256"])
        records.append(row | dict(registered_reference=installed, previous_registered_gameplay=row["gameplay_hold"],
            gameplay_hold=witnessed.get(ident), installed_native_layouts=display, review=dict.fromkeys(files.GATES, True)))
    prior = stage.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = common_rows(after[COMMON], after[ARM])
    assert all(played.panels.text_reference(common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    outcome = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(files.GATES), records=records, source_credit_added=0, candidate_sha256=candidate,
        target_SC3_sha256=stored["target_SC3_sha256"], source_review=stage.reference(played.review.OUT),
        visual_review=visuals, stored_proof=stage.reference(build.STORED), gameplay=stage.reference(played.PAIRED),
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(outcome)
    return outcome


readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_missionary_destination_predecessor=predecessor, nagasaki_dream_release=str(REVIEW)":
        "verified_nagasaki_dream_predecessor=predecessor, kurushima_confrontation_release=str(REVIEW)",
    "len(batches) == 1115 and len(checks) == 450": "len(batches) == 1116 and len(checks) == 451",
    "assert len(revised) == 4 and all(ident in records[STORY] for ident in revised)":
        "assert len(revised) == 3\n        records[STORY].extend(ident for ident in revised if ident not in records[STORY])",
    "nagasaki_dream_release_proof": "kurushima_confrontation_release_proof",
    '"nagasaki_dream_pipeline"': '"kurushima_confrontation_pipeline"',
    "stage.PROOF, played.REPORT, PREVIEW": "stage.PROOF, played.PAIRED, played.NATIVE, PREVIEW",
    "registered_manifest_entries=1116, passing_release_checks=451": "registered_manifest_entries=1117, passing_release_checks=452",
    "contextual_records_revisited=17, contextual_decisions_reused=13, previously_localized_records=17":
        "contextual_records_revisited=8, contextual_decisions_reused=5, previously_localized_records=8",
    "prose_revisions=4, justified_retentions=13, text_display_revisions=4, wrap_only_revisions=0":
        "prose_revisions=2, justified_retentions=5, text_display_revisions=3, wrap_only_revisions=1",
    "ordinary_Nagasaki_dream=True, revised_gameplay_holds=3, conditional_Angelo_panels_observed=False":
        "ordinary_Kurushima_confrontation=True, revised_gameplay_holds=3, native_pages=6",
    "prose_revisions=4, texts_retained=13": "prose_revisions=2, wrap_only_revisions=1, texts_retained=5",
    '"nagasaki_dream_20261123"': '"kurushima_confrontation_wraps_20261123"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Kurushima confrontation testing candidate

Maria's confrontation with Kurushima has two wording edits and a wrap fix. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})
finish = checked_text(parent.finish, {
    "Preserve the registered Nagasaki dream candidate": "Preserve the registered Kurushima confrontation candidate",
    "1,116 entries and 451 passing checks": "1,117 entries and 452 passing checks",
    doc: '''    DOC.write_text(f"""# Maria’s confrontation with Kurushima

Yukihisa's full question about a proud samurai now stays together. Kurushima's sarcastic dismissal keeps its wording, with one beat per line. Kurushima's surrender offer addresses Maria directly and keeps her choice and the threat to everyone else clear. The four-row offer now takes three lines. The other five turns retain their wording. [Exact Japanese, prior and installed records](../{REVIEW.as_posix()})

Ordinary gameplay reached all eight story pages after departing Nagasaki on the existing Maria save. The staged replay verified all three updated pages and nameplates, and twelve control frames matched exactly, including the return to sea. Six stored pages passed offline native checks, including the default name and the one-, fifteen- and sixteen-cell variants of the offer. [Paired gameplay](../{VERIFY.as_posix()}/{SHEET.name}) · [Native pages](../{VERIFY.as_posix()}/{PREVIEW.name})

The cumulative build passed 452 release checks, its own startup and 17 focused tests. The clean-input patch reconstructs the full candidate byte for byte. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})


if __name__ == "__main__":
    cli = template.ArgumentParser(description=__doc__)
    cli.add_argument("--visual-sha256")
    cli.add_argument("--finish-only", action="store_true")
    args = cli.parse_args()
    assert args.finish_only or args.visual_sha256
    scope = vars(template) | vars(parent) | globals()
    exec(compile(prepare + "\n" + finish, __file__ + "::kurushima-confrontation-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
