"""Register the verified Pereira, scabbard, inn and village dialogue batch."""

from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_rafael_pereira_village_gameplay_20261121 as live
from scripts import register_rafael_spain_20261121 as parent
from scripts import verify_rafael_pereira_village_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage = live.stage
base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-pereira-village-v1-20261121"
ROOT = Path("out/rafael_pereira_village_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Pereira_Village_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_rafael_pereira_village_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_pereira_village_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = live.replay.STARTUP_CAPTURE
CHECKPOINT = ("Reviewed 197 records across four complete Rafael exchanges. The registered build has 96 wording revisions, "
              "14 wrap-only fixes and 87 justified retentions.")


def verify(registry, previous, viewed):
    stored, draft, rendered, playback = map(base.load, (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["predecessor_sha256"] == draft["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.OUTPUT) and stored["whole_parent_inverse"]
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF) and rendered["offline_native_only"]
    assert rendered["revised_pages"] == 110
    assert len(playback["holds"]) == 23 and len(playback["offline_only"]) == 93
    reward, = [row for row in playback["holds"] if row["system_FE"]]
    assert reward["id"] == "DK4_MES_B61_R0113"
    assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]
    assert not playback["natural_activation"] and not playback["hardware_verified"]
    assert viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]}
    assert all(base.digest(path) == sha for path, sha in (viewed | playback["evidence"]).items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, parent_files, final = map(native.files, (clean, before, after))
    path = "/data/SC0.DK4"
    groups = {g["block"]: g for g in stored["groups"]}
    numbers = list(stage.review.BLOCKS[0])
    assert sorted(groups) == numbers and all(g["file_path"] == path for g in groups.values())
    assert parent_files.keys() == final.keys() and {p for p in final if final[p] != parent_files[p]} == {path}
    old, new = [native.IlnkContainer.parse(raw).blocks for raw in (parent_files[path], final[path])]
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == numbers
    assert all(native.digest(old[n]) == groups[n]["before"] and native.digest(new[n]) == groups[n]["after"] for n in numbers)
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
    assert len(draft["records"]) == len(results) == 197 and len(observed) == 23
    for row in draft["records"]:
        ident, block = row["id"], row["block"]
        result = results.pop(ident)
        raw, at = bytes.fromhex(result["stored_command_hex"]), result["stored_offset"]
        value = raw[5:raw.index(0, 6)]
        assert new[block][at:at + len(raw)] == raw and row["decision"] == result["decision"]
        assert value[0] == row["source_selector"]
        row.update(registered_reference=dict(file_path=path, block=block, command_offset=at, offset=at + 5,
            exact_stored_hex=value.hex(), exact_command_hex=raw.hex(), archive_sha256=archive_sha256,
            block_sha256=groups[block]["after"], candidate_sha256=candidate),
            observed_in_initialized_excerpt=ident in observed, native_formatting_evidence=result)
        row["review"]["formatting"] = True
    assert not results and draft["decisions"] == {"revision": 110, "retention": 87}
    assert draft["findings"] == {"prose and wrap": 96, "wrap": 14, "retention": 87}
    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,
        review_gates=sorted(REQUIRED_REVIEW_GATES), checked_story_format_guard=controls,
        new_contextual_credit=0, shared_payload_and_lookup_exact=True, native_preview_evidence=str(display.PROOF),
        initialized_replay_evidence=str(live.PROOF), shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, {path: archive_sha256}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                      parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build, {
    "verified_rafael_north_sea_africa_predecessor": "verified_rafael_spain_predecessor",
    "len(batches) == 997 and len(checks) == 332": "len(batches) == 998 and len(checks) == 333",
    "original_Spain_command_map_and_choice_indices_preserved=True": "four_original_command_maps_preserved=True",
    "previously_localized_records=103, new_contextual_records=0, prose_revisions=49":
        "previously_localized_records=197, new_contextual_records=0, prose_revisions=96",
    "wrap_only_revisions=6, justified_retentions=46": "wrap_only_revisions=14, justified_retentions=87",
    "choice_label_revisions=2": "choice_label_revisions=0",
    "pagination_fixes=len(RECLAIMED)": "pagination_fixes=0",
    "initialized_Rafael_menu_and_pagination_excerpt=True": "initialized_Rafael_dialogue_and_funds_excerpt=True",
    "native_revised_pages=56, observed_holds=8, native_menu_captions=4, natural_activation=False":
        "native_revised_pages=110, observed_holds=23, retained_FE_notice=True, natural_activation=False",
    "prior_records_reviewed=103, observed_Rafael_panels=8, native_pages=56":
        "prior_records_reviewed=197, observed_Rafael_panels=23, native_pages=110",
    "prose_revisions=49, justified_retentions=46, wrap_only_revisions=6":
        "prose_revisions=96, justified_retentions=87, wrap_only_revisions=14",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's farewell, scabbard, inn and village exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the four revised exchanges. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_spain", "rafael_pereira_village").replace(
    "verified_rafael_pereira_village_predecessor", "verified_rafael_spain_predecessor")

notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '''    earlier = stage.ROOT.with_name("staged_v1")
    for path in (ROM, stage.ROM, parent.ROM, earlier / stage.ROM.name,
                 earlier / "focused_gameplay/Rafael_Spain_Choices_RESEARCH_ONLY.nds",
                 *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):''':
    '''    first_fixture = stage.ROOT / "focused_gameplay/Rafael_Pereira_Village_RESEARCH_ONLY.nds"
    for path in (ROM, stage.ROM, parent.ROM, first_fixture,
                 *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):''',
    "Preserve the Spain sequence testing ROM, its predecessor, staged ROM and focused fixture":
        "Preserve the village candidate, its predecessor, staged ROM and focused fixtures",
    notes: '''    DOC.write_text(f"""# Rafael's farewell, scabbard, inn and village exchanges

The review covers 197 records. There are 96 wording revisions, 14 wrap-only fixes and 87 justified retentions. Pereira keeps his bluff humor, and the donation notice keeps the exact 500,000 amount. The scabbard remains a possible clue. In the inn, Rafael's private use of Eirene and the displayed Arcadius name reflect the original exchange. Charlotte's account preserves her Romani identity, the false promises made to her family and the prejudice directed at her community. [Exact source and registered decisions](../{REVIEW.as_posix()})

All 110 revised speech pages passed native glyph and bounds checks and direct visual review. An initialized emulator excerpt verified 23 panels across the four exchanges, including the retained donation notice and a return to Lisbon. Seventeen revised panels were observed in that excerpt. The natural scenes and hardware remain unverified. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 focused tests and exact clean-input reconstruction passed. These 197 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_spain", "rafael_pereira_village")

scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
