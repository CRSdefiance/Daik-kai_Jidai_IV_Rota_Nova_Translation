"""Register the verified B60 dialogue, menus and cumulative clean-input patch."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_spain_gameplay_20261121 as live
from scripts import register_rafael_north_sea_africa_20261121 as parent
from scripts import verify_rafael_spain_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-spain-v1-20261121"
ROOT = Path("out/rafael_spain_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Spain_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_spain_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_spain_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed all 103 records in Rafael's negotiations with Pereira. The registered build has 49 wording revisions, "
              "six wrap-only fixes, two revised choice captions and 46 justified retentions.")
RECLAIMED = {140, 208, 293, 399, 474}


def verify(registry, previous, viewed):
    stored, draft, rendered, playback = map(base.load, (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["predecessor_sha256"] == draft["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT) and stored["whole_parent_inverse"]
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF) and rendered["offline_native_only"]
    assert rendered["revised_pages"] == 56 and rendered["native_caption_count"] == 4
    assert len(playback["holds"]) == 8 and len(playback["menus"]) == 5 and len(playback["offline_only"]) == 48
    assert playback["both_pages_and_next_speech_observed"] and playback["exact_native_glyph_matches"]
    assert playback["initialized_excerpts"] and not playback["natural_activation"] and not playback["hardware_verified"]
    assert viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]}
    assert all(base.digest(path) == sha for path, sha in (viewed | playback["evidence"]).items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, parent_files, final = map(native.files, (clean, before, after))
    group, = stored["groups"]
    path, block = group["file_path"], group["block"]
    assert (path, block) == ("/data/SC0.DK4", 60)
    assert parent_files.keys() == final.keys() and {p for p in final if final[p] != parent_files[p]} == {path}
    old, new = [native.IlnkContainer.parse(raw).blocks for raw in (parent_files[path], final[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [60]
    assert native.digest(old[60]) == group["before"] and native.digest(new[60]) == group["after"]
    after.replace_file(path, parent_files[path])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    after.replace_file(path, final[path])
    assert bytes(after.rom.save()) == stage.ROM.read_bytes()
    arm = final[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(final["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(source, final)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup = parent.scope["startup_check"].startup_proof
    FunctionType(startup.__code__, startup.__globals__ |
                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})(previous, candidate, arm)

    results = {record["id"]: record for record in rendered["records"]}
    observed = set(playback["observed_ids"])
    archive_sha256 = native.digest(final[path])
    draw = display.display.clipped_renderer(SimpleNamespace(arm=arm, image=before))
    font = before.read_file("/GRP/KANJI.FNT")
    pagination = {}
    assert len(draft["records"]) == len(results) == 103 and len(observed) == 11
    for row in draft["records"]:
        ident = row["id"]
        result = results.pop(ident)
        raw, at = bytes.fromhex(result["stored_command_hex"]), result["stored_offset"]
        assert new[60][at:at + len(raw)] == raw and row["decision"] == result["decision"]
        if row["native_command_word"] == 0x2100:
            index, = row["native_slots"]
            count, base_offset = count_and_base(raw)
            assert count == 2
            value = labels(raw)[index]
            assert value == row["english"].encode("ascii") and result["native_caption"]
            offset = base_offset + unpack_from("<H", raw, 2 + 2 * index)[0]
        else:
            offset = 5
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"]
            if row["source_record_index"] in RECLAIMED:
                previous_body = bytes.fromhex(row["current_hex"])[1:]
                previous_display = draw(arm, font, previous_body)
                assert previous_display["complete_consumed_bytes"] == len(previous_body)
                assert len(previous_display["pages"]) == 2 and result["native_pages"] == 1
                pagination[ident] = {"previous_pages": 2, "registered_pages": 1}
        row.update(registered_reference=dict(file_path=path, block=60, command_offset=at, offset=at + offset,
            exact_stored_hex=value.hex(), exact_command_hex=raw.hex(), archive_sha256=archive_sha256,
            block_sha256=group["after"], candidate_sha256=candidate),
            observed_in_initialized_excerpt=ident in observed, native_formatting_evidence=result)
        row["review"]["formatting"] = True
    assert not results and draft["decisions"] == {"revision": 57, "retention": 46}
    assert len(pagination) == len(RECLAIMED)
    assert draft["findings"] == {"prose and wrap": 49, "choice caption": 2, "wrap": 6, "retention": 46}
    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,
        review_gates=sorted(REQUIRED_REVIEW_GATES), checked_story_format_guard=controls,
        new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),
        page_count_improvements=pagination,
        initialized_replay_evidence=str(live.PROOF), shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {path: archive_sha256}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_hodram_baltic_trade_predecessor": "verified_rafael_north_sea_africa_predecessor",
    "len(batches) == 996 and len(checks) == 331": "len(batches) == 997 and len(checks) == 332",
    "nine_original_exchange_command_maps_preserved=True": "original_Spain_command_map_and_choice_indices_preserved=True",
    "previously_localized_records=146, new_contextual_records=0, prose_revisions=34":
        "previously_localized_records=103, new_contextual_records=0, prose_revisions=49",
    "wrap_only_revisions=4, justified_retentions=108": "wrap_only_revisions=6, justified_retentions=46",
    "choice_label_revisions=0": "choice_label_revisions=2",
    "pagination_fixes=0": "pagination_fixes=len(RECLAIMED)",
    "initialized_Rafael_excerpts=True": "initialized_Rafael_menu_and_pagination_excerpt=True",
    "native_revised_pages=38, observed_holds=13, natural_activation=False":
        "native_revised_pages=56, observed_holds=8, native_menu_captions=4, natural_activation=False",
    "prior_records_reviewed=146, observed_Rafael_panels=13, native_pages=38":
        "prior_records_reviewed=103, observed_Rafael_panels=8, native_pages=56",
    'source.parent == rendered.ROOT': 'source.parent == display.ROOT',
    "prose_revisions=34, justified_retentions=108, wrap_only_revisions=4":
        "prose_revisions=49, justified_retentions=46, wrap_only_revisions=6",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's negotiations with Pereira

The [testing ROM](../../{ROM.as_posix()}) includes the revised dialogue and choices in Rafael's Spain sequence. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_north_sea_africa", "rafael_spain").replace(
    "verified_rafael_spain_predecessor", "verified_rafael_north_sea_africa_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '    for path in (ROM, stage.ROM, parent.ROM, *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):':
        '    earlier = stage.ROOT.with_name("staged_v1")\n'
        '    for path in (ROM, stage.ROM, parent.ROM, earlier / stage.ROM.name,\n'
        '                 earlier / "focused_gameplay/Rafael_Spain_Choices_RESEARCH_ONLY.nds",\n'
        '                 *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):',
    "Preserve the Rafael dialogue candidate, staged build, predecessor and focused emulator ROMs":
        "Preserve the Spain sequence testing ROM, its predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's negotiations with Pereira

The full 103-record exchange has 49 wording revisions, six wrap-only fixes, two revised choice captions and 46 justified retentions. Pereira tests Rafael's commitment before discussing the two strategies for Kuhn. Rafael preserves the reason for leaving Pereira in Southeast Asia in each branch, and the political warning still concerns the royal family's claim to the throne. Five speeches now fit on one page. Pereira's two-page warning about Valdes keeps the Proof of Conquest title together and turns the page after a complete question. [Exact source and registered decisions](../{REVIEW.as_posix()})

All 56 revised speech pages, six surname-width cases and four captions passed native checks and direct visual review. An initialized emulator excerpt showed both menus and their cursor movement, eight revised speech pages, the complete Valdes page turn, Rafael's reply, and the return to Lisbon. The native menu checks preserved both choice indices and cancellation. The original narrative branches and hardware remain unverified. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 103 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_north_sea_africa", "rafael_spain")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
