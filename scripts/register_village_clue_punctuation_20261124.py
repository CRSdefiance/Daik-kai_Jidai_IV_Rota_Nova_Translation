"""Register the fixed-pool village clue punctuation and phrase wraps."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_narvik_lookout_20261124 as parent
from scripts import stage_cartridge_title_20261123 as files
from scripts import stage_village_clue_punctuation_20261124 as build
from scripts import verify_village_clue_replay_20261124 as gameplay
from scripts.source_locked_derivation_v5118 import checked_text


review, template = build, parent.template
ARM, COMMON, ROM = build.ARM, build.COMMON, build.ROM
PROFILE = "all-routes-village-clue-punctuation-v1-20261124"
CHECK = "registered_village_clue_punctuation_and_complete_parent_inverse"
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261124_village_clue_punctuation_candidate")
VERIFY, MANIFEST = PACKAGE / "verification", ROM.with_suffix(".manifest.json")
REVIEW, RELEASE, PLAN = (VERIFY / name for name in (
    "registered_review.json", "registered_release_verification.json", "registration_mutation_plan.json"))
PATCH, REBUILT, PATCH_PROOF, STARTUP_CAPTURE = build.PATCH, build.REBUILT, build.PATCH_PROOF, build.STARTUP_CAPTURE
REGISTRY_BEFORE, LEDGER_BEFORE = parent.REGISTRY_NEXT, parent.LEDGER_NEXT
REGISTRY_NEXT, LEDGER_NEXT = build.ROOT / "release_stack_village_clue_punctuation.json.gz", build.ROOT / "ledger_after.json.gz"
STARTUP, QA = build.ROOT / "own_startup_verification.json", build.ROOT / "qa_passed.xml"
DOC = Path("docs/editorial_village_clue_punctuation_registered_20261124.md")
CHECKPOINT = "Registered punctuation and phrase wrapping across the 24 Promised Words clues."
stage = SimpleNamespace(**(vars(files) | dict(ROM=ROM, PARENT_RELEASE=parent.RELEASE, PROOF=build.STORED)))


def verify(previous, visual_sha):
    packet, stored, live, patch = map(files.read, (build.OUT, build.STORED, gameplay.OUT, PATCH_PROOF))
    candidate = files.digest(ROM)
    assert candidate == files.digest(REBUILT) == stored["candidate_sha256"] == live["candidate_sha256"]
    assert patch["byte_exact"] and patch["candidate"]["sha256"] == candidate and patch["patch"] == files.reference(PATCH)
    assert previous["candidate_sha256"] == packet["candidate_sha256"] == live["predecessor_sha256"] == stored["predecessor_sha256"]
    assert files.digest(files.CLEAN) == patch["clean_input_sha256"] == previous["clean_input_sha256"] == packet["source_sha256"]
    assert stored["source_preflight"] == files.reference(build.OUT) and stored["whole_parent_inverse"]
    assert live["position_only_focused_gameplay"] and live["same_message_requests"] and live["same_ship_writes"]
    assert live["changed"]["frame"] == gameplay.RESULT and len(live["unchanged_frames"]) == 48
    native = packet["native_cases"]
    assert [row["index"] for row in native] == list(range(24))
    assert all(row["page_count"] == 1 and row["portrait"]["buffer_canaries_intact"] for row in native)
    assert sum(len(row["messages"]) for row in packet["visuals"]) == 24
    declared = live["sheets"] + packet["visuals"]
    visible = [files.reference(row["path"]) for row in declared]
    assert [r["sha256"] for r in visible] == [r["sha256"] for r in declared]
    assert files.sha256("".join(row["sha256"] for row in visible).encode("ascii")).hexdigest() == visual_sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, old, new = map(files.NdsImage.open, (files.CLEAN, previous["candidate"], ROM))
    before, after = (parent.trend.files(image) for image in (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM}
    arm, clean_arm = after[ARM], clean.read_file(ARM)
    assert files.sha256(arm).hexdigest() == stored["target_ARM9_sha256"]
    assert files.sha256(after[COMMON]).hexdigest() == stored["target_COMMON_sha256"] == previous["target_COMMON_sha256"]
    assert template.right_bound(arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert build.cache_plan(arm) == build.cache_plan(before[ARM])
    code = build.MainCodeFile(arm, build.BASE)
    deployed = bytes(code.sections[3].data)
    for edit in stored["changed_pool_spans"]:
        start, size = edit["pool_offset"], edit["extent"]
        assert deployed[start:start + size].hex() == edit["after_hex"]
        code.sections[3].data[start:start + size] = bytes.fromhex(edit["before_hex"])
    assert bytes(code.save()) == before[ARM]
    new.replace_file(ARM, before[ARM])
    assert files.sha256(new.rom.save()).hexdigest() == previous["candidate_sha256"]

    records = []
    old_pool = bytes(code.sections[3].data)
    for row in packet["records"]:
        src, old_ref, ref = (row[k] for k in ("source_reference", "current_reference", "installed_reference"))
        at, ptr, source_ptr = ref["ARM9_file_offset"], ref["native_text_address"], src["native_text_address"]
        assert unpack_from("<I", clean_arm, at)[0] == source_ptr and unpack_from("<I", arm, at)[0] == ptr
        assert build.cstring(clean_arm, source_ptr - build.BASE).hex() == src["exact_hex"]
        assert build.cstring(old_pool, ptr - build.POOL).hex() == old_ref["exact_hex"]
        assert build.cstring(deployed, ptr - build.POOL).hex() == ref["exact_hex"]
        records.append(row | dict(registered_reference=ref | dict(candidate_sha256=candidate)))
    assert len(records) == 54 and sum(r["decision"] == "revision" for r in records) == 25
    wraps = sum([len(line.strip()) for line in row["previous"].splitlines()] !=
                [len(line.strip()) for line in row["proposed"].splitlines()] for row in native)
    assert wraps == 18

    inherited = template.previous
    scope = inherited.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    source = checked_text(inherited.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "Village_clue_pool_copy_and_startup_extent_preserved",
    })
    exec(compile(source, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](previous, candidate, arm)

    prior = files.read(parent.REVIEW)
    shared = prior["shared_consumer_binding"]
    assert len(shared["records"]) == 276 and shared["candidate_sha256"] == previous["candidate_sha256"]
    common = parent.build.panels.common_rows(after[COMMON], arm)
    assert all(parent.build.panels.text_reference(common[row["message_ID"]]) == row["installed"] for row in shared["records"])
    result = dict(translation_policy=packet["translation_policy"], target_locale=packet["target_locale"],
        encoder=packet["encoder"], review_gates=packet["review_gates"], records=records, candidate_sha256=candidate,
        target_ARM9_sha256=stored["target_ARM9_sha256"], target_COMMON_sha256=stored["target_COMMON_sha256"],
        visual_review=visible, stored_proof=files.reference(build.STORED), gameplay=files.reference(gameplay.OUT),
        native_clues=24, punctuation_fields=25, phrase_wrap_adjustments=wraps, source_credit_added=0,
        shared_consumer_binding=shared | dict(candidate_sha256=candidate),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"], full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


start = parent.prepare.index('        revised = [row["id"]')
update = parent.prepare[start:parent.prepare.index("        update = dict(profile=", start)]
readme = parent.prepare[parent.prepare.index('    (PACKAGE / "README.md")'):parent.prepare.index('    stage.write(PACKAGE / "checksums.json"')]
doc = parent.finish[parent.finish.index("    DOC.write_text"):parent.finish.index("    prefix =")]
prepare = checked_text(parent.prepare, {
    "verified_tripoli_hodram_warning_predecessor=predecessor, narvik_lookout_release=str(REVIEW)":
        "verified_narvik_lookout_predecessor=predecessor, village_clue_punctuation_release=str(REVIEW)",
    "len(batches) == 1133 and len(checks) == 468": "len(batches) == 1134 and len(checks) == 469",
    update: '''        revised = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert len(revised) == 25 and len(outcome["records"]) == 54
        records[ARM].extend(ident for ident in revised if ident not in records[ARM])
''',
    "snapshot_scope=COMMON": "snapshot_scope=ARM",
    "narvik_lookout_release_proof=stage.reference(stage.PROOF)": "village_clue_punctuation_release_proof=stage.reference(stage.PROOF)",
    '"narvik_lookout_pipeline"': '"village_clue_punctuation_pipeline"',
    "stage.PROOF, build.PAIRED, review.OUT": "stage.PROOF, gameplay.OUT, review.OUT",
    "registered_manifest_entries=1134, passing_release_checks=469, changed_components=1, changed_internal_files=[COMMON]":
        "registered_manifest_entries=1135, passing_release_checks=470, changed_components=1, changed_internal_files=[ARM]",
    "contextual_records_revisited=18, contextual_decisions_reused=17, previously_localized_records=18":
        "contextual_records_revisited=54, contextual_decisions_reused=29, previously_localized_records=54",
    "prose_revisions=1, justified_retentions=17, text_display_revisions=1, wrap_only_revisions=0":
        "prose_revisions=0, justified_retentions=29, text_display_revisions=24, phrase_wrap_adjustments=18, punctuation_fields=25",
    'ordinary_Copenhagen_departure=True, position_only_Narvik=True, revised_gameplay_holds=1, native_pages=1, unchanged_gameplay_holds=len(stage.read(build.PAIRED)["unchanged_frames"])':
        'position_only_Narvik=True, revised_gameplay_holds=1, native_pages=24, unchanged_gameplay_holds=len(stage.read(gameplay.OUT)["unchanged_frames"])',
    "prose_revisions=1, wrap_only_revisions=0, texts_retained=17":
        "prose_revisions=0, phrase_wrap_adjustments=18, punctuation_fields=25, texts_retained=29",
    '"narvik_lookout_20261124"': '"village_clue_punctuation_20261124"',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Promised Words clue testing candidate

The 24 quotations use American punctuation, and 18 keep more of the clue phrase together. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}`.
""", encoding="utf-8")
''',
})

finish = checked_text(parent.finish, {
    "Preserve the registered Narvik lookout candidate": "Preserve the registered village-clue candidate",
    "1,134 entries and 469 passing checks": "1,135 entries and 470 passing checks",
    doc: '''    DOC.write_text(f"""# Promised Words clues across all 24 villages

The clue now closes with American quotation punctuation. Eighteen layouts also keep related words together, including **stone statues** and **covered with sandstone**. All 24 stock answers and five surrounding messages retain their wording. [Exact Japanese, current text and registered review](../{REVIEW.as_posix()})

The original consumer selected, formatted and rendered every revised clue. All 24 fit on one page and retain their complete opening and closing glyphs. At Narvik, the paired position-only replay reached the clue after the typed Svartisen answer. Its full text and Charles Rochefort's nameplate passed, and 48 surrounding frames matched. [Native previews](../{VERIFY.as_posix()}/portrait_sheet_01.png) [Paired replay](../{VERIFY.as_posix()}/paired_village_clue_replay_1_20261123.png)

The candidate passed 470 release checks, its own startup, all 17 focused tests and byte-exact reconstruction from the clean input. [Testing package](../{PACKAGE.as_posix()}/README.md)
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
    while hasattr(lineage[-1], "parent") and lineage[-1].parent is not lineage[-1] and len(lineage) < 14:
        lineage.append(lineage[-1].parent)
    scope = vars(template).copy()
    for module in reversed(lineage):
        scope.update(vars(module))
    scope.update(globals())
    exec(compile(prepare + "\n" + finish, __file__ + "::village-clue-registration", "exec"), scope)
    if not args.finish_only:
        scope["prepare"](args.visual_sha256)
    scope["finish"]()
