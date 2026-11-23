"""Register the verified Gerhard recruitment and sea-battle tutorial."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_gerhard_tutorial_gameplay_20261121 as live
from scripts import register_rafael_spain_london_20261121 as parent
from scripts import review_rafael_gerhard_nameplates_20261121 as names
from scripts import verify_rafael_gerhard_tutorial_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-gerhard-tutorial-v1-20261121"
ROOT = Path("out/rafael_gerhard_tutorial_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Gerhard_Tutorial_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_gerhard_tutorial_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_gerhard_tutorial_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 131 Gerhard recruitment and sea-battle tutorial records. The registered candidate has "
              "74 wording revisions, three wrap-only fixes and 54 justified retentions.")
startup_check = FunctionType(parent.startup_check.__code__, parent.startup_check.__globals__ |
    {"checked_report": FunctionType(parent.report_reader.__code__, parent.report_reader.__globals__ |
                                    {"STARTUP_CAPTURE": STARTUP_CAPTURE})})


def pages_saved():
    changes = base.load(display.PROOF)["pagination_changes"]
    return sum(row["previous_pages"] - row["current_pages"] for row in changes)


def verify(registry, previous, viewed):
    stored, draft, rendered, playback, name_check = map(base.load,
        (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF, names.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"] == name_check["candidate_sha256"]
    assert stored["predecessor_sha256"] == draft["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF) and rendered["offline_native_only"]
    assert rendered["revised_speech_pages"] == 76 and rendered["FE_panels"] == 12
    assert sorted(m["count"] for m in rendered["menus"]) == [2, 3]
    assert len(playback["holds"]) == 29 and len(playback["menus"]) == 4 and len(playback["exact_sampled_page_turn"]) == 3
    assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]
    assert not playback["natural_activation"] and not playback["hardware_verified"]
    assert len(name_check["records"]) == 6 and all(len(row["native_getters"]) == 2 for row in name_check["records"])
    assert viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]}
    assert all(base.digest(path) == sha for path, sha in (viewed | playback["evidence"]).items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, parent_files, final = map(native.files, (clean, before, after))
    path = stage.PATH
    assert parent_files.keys() == final.keys() and {p for p in final if final[p] != parent_files[p]} == {path}
    old, new = [native.IlnkContainer.parse(raw).blocks for raw in (parent_files[path], final[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [84]
    group, = stored["groups"]
    assert group["block"] == 84 and group["file_path"] == path
    assert native.digest(old[84]) == group["before"] and native.digest(new[84]) == group["after"]
    assert stored["original_installed_commands"] == 219 and stored["original_clean_commands"] == 217
    assert stored["branch_targets_preserved"] == 20 and stored["preserved_FE_continuations"] == 2
    after.replace_file(path, parent_files[path])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    after.replace_file(path, final[path])
    assert bytes(after.rom.save()) == stage.ROM.read_bytes()
    arm = final[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(final["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(source, final)
    assert controls == stored["checked_story_format_guard"]
    FunctionType(startup_check.__code__, startup_check.__globals__ |
                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})(previous, candidate, arm)

    entries = {r["id"]: r for r in rendered["records"]}
    observed = set(playback["observed_ids"])
    archive_sha256 = native.digest(final[path])
    assert len(entries) == len(draft["records"]) == 131
    for row in draft["records"]:
        ident, selector = row["id"], row["source_selector"]
        proof = entries.pop(ident)
        refs = []
        for command in proof["stored_pages"]:
            raw, at = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert new[84][at:at + len(raw)] == raw
            if selector is None:
                index, = row["native_slots"]
                _, header = count_and_base(raw)
                position = header + unpack_from("<H", raw, 2 + index * 2)[0]
                value = labels(raw)[index]
                assert value.decode("ascii") == row["english"]
            else:
                position, value = 5, raw[5:raw.index(0, 6)]
                assert value[0] == selector
            refs.append(dict(command_offset=at, offset=at + position, exact_stored_hex=value.hex(), exact_command_hex=raw.hex()))
        row.update(registered_reference=dict(file_path=path, block=84, archive_sha256=archive_sha256,
            block_sha256=group["after"], candidate_sha256=candidate, installed_pages=refs, **refs[0]),
            observed_in_initialized_excerpt=ident in observed, native_formatting_evidence=proof)
        row["review"]["formatting"] = True
    assert not entries and draft["findings"] == {"retention": 54, "wording": 74, "wrap": 3}
    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,
        new_contextual_credit=0, checked_story_format_guard=controls, shared_payload_and_lookup_exact=True,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],
        native_preview_evidence=str(display.PROOF), initialized_replay_evidence=str(live.PROOF),
        scoped_nameplate_review={"path": str(names.PROOF), "sha256": base.digest(names.PROOF)})
    validate_natural_dialogue_batch(draft)
    return stored, draft, {path: archive_sha256}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_east_asia_showdown_predecessor": "verified_rafael_spain_london_predecessor",
    "len(batches) == 1001 and len(checks) == 336": "len(batches) == 1002 and len(checks) == 337",
    "display.PROOF, names.PROOF, PAGINATION, args.visual_review": "display.PROOF, names.PROOF, args.visual_review",
    "three_original_command_maps_and_FE_preambles_preserved=True": "B84_command_map_FE_continuations_and_choice_slots_preserved=True",
    "previously_localized_records=199, new_contextual_records=0, prose_revisions=105":
        "previously_localized_records=131, new_contextual_records=0, prose_revisions=74",
    "wrap_only_revisions=5, justified_retentions=89": "wrap_only_revisions=3, justified_retentions=54",
    "choice_label_revisions=0": "choice_label_revisions=3",
    "pagination_fixes=2": "pagination_fixes=pages_saved()",
    "initialized_Rafael_bullfight_and_rescue_excerpts=True": "initialized_Rafael_gerhard_excerpt=True",
    "native_revised_pages=110, observed_holds=43, contextual_nameplate_retentions=15, reclaimed_page_turns=2":
        "native_revised_pages=76, observed_holds=29, contextual_nameplate_retentions=6, reclaimed_page_turns=pages_saved(), actual_menu_samples=4",
    "prior_records_reviewed=199, observed_Rafael_panels=43, native_pages=110":
        "prior_records_reviewed=131, observed_Rafael_panels=29, native_pages=76",
    "prose_revisions=105, justified_retentions=89, wrap_only_revisions=5":
        "prose_revisions=74, justified_retentions=54, wrap_only_revisions=3",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's Gerhard recruitment and sea-battle tutorial

The [testing ROM](../../{ROM.as_posix()}) includes the reviewed B84 dialogue, menus and lesson panels. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_spain_london", "rafael_gerhard_tutorial").replace(
    "verified_rafael_gerhard_tutorial_predecessor", "verified_rafael_spain_london_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    'for tag in ("spanish_london_staged_v1", "spanish_london_staged_v2")':
        'for tag in ("gerhard_staged_v1", "gerhard_staged_v2")',
    '    for path in (ROM, stage.ROM, parent.ROM, *earlier_builds,':
        '''    earlier_fixture = stage.ROOT.with_name("gerhard_staged_v2") / "focused_gameplay/Rafael_Gerhard_Tutorial_RESEARCH_ONLY.nds"
    for path in (ROM, stage.ROM, parent.ROM, *earlier_builds, earlier_fixture,''',
    "Preserve the Spain and London candidate, predecessor, staged ROM and focused fixture":
        "Preserve the Gerhard tutorial candidate, predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's Gerhard recruitment and sea-battle tutorial

The review covers 131 records. There are 74 wording revisions, three wrap-only fixes and 54 justified retentions. The alternative recruitment caption now expresses why Rafael wants Gerhard aboard. Both training branches use the same combat instructions and the installed Aim, Gun Battery, Swords, Quarters and Boarding Leader terms. Six names and role labels were reviewed and kept. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Native and visual checks cover 76 revised speech pages, all 12 speakerless panels and all five choice captions. The two original menus keep their result slots. Focused emulator replays verified 29 speech pages, both menus and the transition between the two naval instruction panels and Gerhard's next reply. The controller moved the selection in both menus. The fixture sequenced the sampled replies. Natural story branches and hardware remain untested. [Native and emulator evidence](../{VERIFY.as_posix()})

The scene keeps all 219 installed commands, both source-owned FE continuations and 20 original branch targets. The revised progressive dialogue has {pages_saved()} fewer page turns. Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 131 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_spain_london", "rafael_gerhard_tutorial")
scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
