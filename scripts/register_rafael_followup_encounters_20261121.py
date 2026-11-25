"""Register the verified Rafael follow-up encounters over the Gerhard tutorial candidate."""

from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_rafael_gerhard_tutorial_20261121 as parent
from scripts import replay_rafael_followup_encounters_20261121 as live
from scripts import verify_rafael_followup_encounters_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, workflow = live.stage, parent.base, parent.native, parent.workflow
PROFILE = "all-routes-rafael-followup-encounters-v1-20261121"
ROOT = parent.ROOT.with_name("rafael_followup_encounters_registered_20261121")
ROM = ROOT / "Translation_DS_Rafael_Followup_Encounters_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261121_rafael_followup_encounters_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_followup_encounters_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml", live.STARTUP_CAPTURE
names = SimpleNamespace(PROOF=display.NAMES)
CHECKPOINT = "Reviewed 261 Rafael records across 11 encounters, with 159 wording revisions, two wrap-only fixes and 100 justified retentions."


def pages_saved():
    return sum(r["previous_pages"] - r["current_pages"] for r in base.load(display.PROOF)["pagination_changes"])


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(live.PROOF)["holds"])


def verify(registry, previous, viewed):
    stored, draft, rendered, playback, name_check = map(base.load,
        (stage.PROOF, stage.OUTPUT, display.PROOF, live.PROOF, names.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"] == name_check["candidate_sha256"]
    assert stored["predecessor_sha256"] == draft["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF) and rendered["offline_native_only"]
    assert rendered["FE_panels"] == 7 and sorted(m["count"] for m in rendered["menus"]) == [2, 2, 2]
    assert len(playback["holds"]) >= 38 and len(playback["menus"]) == 2 and len(playback["exact_sampled_page_turn"]) == 4
    assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]
    assert not playback["natural_activation"] and not playback["hardware_verified"]
    assert len(name_check["records"]) == 20 and all(len(row["native_getters"]) == 2 for row in name_check["records"])
    assert viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]}
    assert all(base.digest(path) == sha for path, sha in (viewed | playback["evidence"]).items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    clean, before, after = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, parent_files, final = map(native.files, (clean, before, after))
    path = display.PATH
    assert parent_files.keys() == final.keys() and {p for p in final if final[p] != parent_files[p]} == {path}
    old, new = [native.IlnkContainer.parse(raw).blocks for raw in (parent_files[path], final[path])]
    blocks = [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
    assert blocks == list(stage.review.BLOCKS[0]) == stored["changed_blocks"][path]
    groups = {group["block"]: group for group in stored["groups"]}
    assert sum(len(group["commands"]) for group in groups.values()) == 435
    for n in blocks:
        group = groups[n]
        assert native.digest(old[n]) == group["before"] and native.digest(new[n]) == group["after"]
    after.replace_file(path, parent_files[path])
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    after.replace_file(path, final[path])
    assert bytes(after.rom.save()) == stage.ROM.read_bytes()
    arm = final[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(final["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(source, final)
    assert controls == stored["source25"]
    startup = parent.startup_check
    report_reader = startup.__globals__["checked_report"]
    checked = FunctionType(report_reader.__code__, report_reader.__globals__ | {"STARTUP_CAPTURE": STARTUP_CAPTURE})
    FunctionType(startup.__code__, startup.__globals__ |
                 {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE, "checked_report": checked})(previous, candidate, arm)

    entries = {r["id"]: r for r in rendered["records"]}
    observed = set(playback["observed_ids"])
    archive_sha256 = native.digest(final[path])
    assert len(entries) == len(draft["records"]) == 261
    for row in draft["records"]:
        ident, selector, block = row["id"], row["source_selector"], row["block"]
        proof = entries.pop(ident)
        command, = proof["stored_pages"]
        raw, at = bytes.fromhex(command["stored"]), command["stored_offset"]
        assert block == proof["block"] and new[block][at:at + len(raw)] == raw
        if selector is None:
            index, = row["native_slots"]
            _, header = count_and_base(raw)
            position = header + unpack_from("<H", raw, 2 + index * 2)[0]
            value = labels(raw)[index]
            assert value.decode("ascii") == row["english"]
        else:
            position, value = 5, raw[5:raw.index(0, 6)]
            assert value[0] == selector
        installed = dict(command_offset=at, offset=at + position, exact_stored_hex=value.hex(), exact_command_hex=raw.hex())
        row.update(registered_reference=dict(file_path=path, block=block, archive_sha256=archive_sha256,
            block_sha256=groups[block]["after"], candidate_sha256=candidate, **installed),
            observed_in_initialized_excerpt=ident in observed, native_formatting_evidence=proof)
        row["review"]["formatting"] = True
    assert not entries and draft["findings"] == {"wording": 159, "wrap": 2, "retention": 100}
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
    "verified_rafael_spain_london_predecessor": "verified_rafael_gerhard_tutorial_predecessor",
    "len(batches) == 1002 and len(checks) == 337": "len(batches) == 1003 and len(checks) == 338",
    "B84_command_map_FE_continuations_and_choice_slots_preserved=True": "original_command_maps_FE_and_choice_slots_preserved=True",
    "previously_localized_records=131, new_contextual_records=0, prose_revisions=74":
        "previously_localized_records=261, new_contextual_records=0, prose_revisions=159",
    "wrap_only_revisions=3, justified_retentions=54": "wrap_only_revisions=2, justified_retentions=100",
    "choice_label_revisions=3": "choice_label_revisions=0",
    "initialized_Rafael_gerhard_excerpt=True": "initialized_Rafael_followup_encounters=True",
    "native_revised_pages=76, observed_holds=29, contextual_nameplate_retentions=6":
        "native_revised_pages=native_count(), observed_holds=observed_count(), contextual_nameplate_retentions=20",
    "actual_menu_samples=4": "actual_menu_samples=2",
    "prior_records_reviewed=131, observed_Rafael_panels=29, native_pages=76":
        "prior_records_reviewed=261, observed_Rafael_panels=observed_count(), native_pages=native_count()",
    "prose_revisions=74, justified_retentions=54, wrap_only_revisions=3":
        "prose_revisions=159, justified_retentions=100, wrap_only_revisions=2",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael's follow-up encounters

The [testing ROM](../../{ROM.as_posix()}) includes 11 contextual scene reviews. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
''',
}).replace("rafael_gerhard_tutorial", "rafael_followup_encounters").replace(
    "verified_rafael_followup_encounters_predecessor", "verified_rafael_gerhard_tutorial_predecessor")
notes = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
pins = parent.commit[parent.commit.index("    earlier_builds ="):parent.commit.index("        absolute =")]
commit = checked_text(parent.commit, {
    pins: '''    earlier = stage.ROOT.with_name("staged_v1")
    earlier_proof = base.load(earlier / "focused_gameplay/verified_gameplay.json")
    prior_roms = [Path(p) for p in earlier_proof["evidence"] if p.endswith(".nds")]
    for path in (ROM, stage.ROM, parent.ROM, earlier / stage.ROM.name, *prior_roms,
                 *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):
''',
    "Preserve the Gerhard tutorial candidate, predecessor, staged ROM and focused fixture":
        "Preserve the Rafael encounters candidate, predecessor, staged ROM and focused fixture",
    notes: '''    DOC.write_text(f"""# Rafael's follow-up encounters

The review covers 261 records across 11 complete encounters. It includes 159 wording revisions, two wrap-only fixes and 100 justified retentions. The scenes cover Rafael's second visit to Gerhard, Charles and Yukihisa joining the crew, the Silla Gold Crown choices, Janus's fleet plans, the sailor with the Miracle Bullet Charm, Emilio's food encounters, and the Katzbalger, ninja and amber leads. All 20 speaking names and roles were retained with source and consumer references. [Exact Japanese and registered decisions](../{REVIEW.as_posix()})

Offline checks cover {native_count()} revised speech pages, all seven speakerless panels and all six captions in three retained menus. Focused emulator excerpts cover {observed_count()} speech pages, both highlights of the miracle menu and the steps through the Spirit notices to the next progressive panel. The fixture sequenced those exact installed commands. Original story activation, other choice paths and hardware remain untested. [Native and emulator evidence](../{VERIFY.as_posix()})

Six startup holds, 24 protected name getters, 17 repository tests and exact clean-input reconstruction passed. All scene command maps, original branch destinations and the ASCII right-bound correction are preserved. These 261 records already carried editorial credit. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
}).replace("rafael_gerhard_tutorial", "rafael_followup_encounters")
scope = parent.scope | globals()
for source in (build, commit):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

