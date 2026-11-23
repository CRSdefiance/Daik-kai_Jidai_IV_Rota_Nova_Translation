"""Register the cumulative ROM with both reviewed violin encounters."""

from argparse import ArgumentParser
from contextlib import contextmanager
from gzip import GzipFile
from json import dumps, loads
from mmap import ACCESS_READ, mmap
from os import fsync
from pathlib import Path
import re
from shutil import copyfile, copyfileobj
from types import FunctionType
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts.finish_ruin_statue_registration_20261118 import update_ledger_in_place
from scripts import register_amsterdam_tavern_editorial_20261120 as startup_check
from scripts import replay_moonlit_violin_20261121 as live
from scripts import stage_moonlit_violin_20261121 as stage
from scripts import verify_moonlit_violin_20261121 as display


base, native, parent = stage.base, stage.native, stage.parent
workflow = parent.workflow
PROFILE = "all-routes-moonlit-violin-v1-20261121"
ROOT = Path("out/moonlit_violin_registered_20261121")
ROM = ROOT / "Translation_DS_Moonlit_Violin_20261121_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261121_moonlit_violin_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_moonlit_violin_registered_20261121.md")
EVIDENCE = stage.ROOT
STARTUP, QA = EVIDENCE / "own_startup_verification.json", EVIDENCE / "qa_passed.xml"
STARTUP_CAPTURE = EVIDENCE / "startup/capture/capture_report.json"
CHECKPOINT = "Reviewed both versions of the moonlit violin encounter. Registered five dialogue edits and 32 justified retentions."


def verify(registry, previous, viewed):
    stored, draft, rendered, playback = map(base.load, (stage.PROOF, stage.review.OUTPUT, display.PROOF, live.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["predecessor_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.review.OUTPUT)
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert draft["decisions"] == {"revision": 5, "retention": 32} and stored["whole_parent_inverse"]
    assert playback["initialized_excerpts"] and playback["exact_native_glyph_matches"]
    assert not playback["natural_activation"] and not playback["hardware_verified"]
    assert rendered["newly_rendered_pages"] == 5 and not rendered["actual_gameplay"]
    assert len(playback["holds"]) == 21 and {h["route"] for h in playback["holds"]} == {0, 1}
    assert viewed == {s["path"]: s["sha256"] for s in rendered["sheets"] + playback["sheets"]} and len(viewed) == 3
    for path, sha in (viewed | playback["evidence"]).items():
        assert base.digest(path) == sha
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean, previous_rom, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    source, before, after = map(native.files, (clean, previous_rom, target))
    groups = {g["file_path"]: g for g in stored["groups"]}
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == groups.keys() == {"/data/SC0.DK4", "/data/SC1.DK4"}
    archives, blocks = {}, {}
    for path, group in groups.items():
        old, new = [native.IlnkContainer.parse(data).blocks for data in (before[path], after[path])]
        number = group["block"]
        assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [number]
        assert native.digest(old[number]) == group["before"] and native.digest(new[number]) == group["after"]
        archives[path], blocks[path] = native.digest(after[path]), new[number]
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    for path in groups:
        target.replace_file(path, after[path])
    assert bytes(target.rom.save()) == stage.ROM.read_bytes()
    arm = after[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(after[stage.review.shared.COMMON]) == previous["target_COMMON_sha256"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(source, after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    assert stage.review.bind_movie(clean, target, (source[native.ARM], arm))["sha256"] == draft["artwork"]["sha256"]

    startup = startup_check.startup_proof
    FunctionType(startup.__code__, startup.__globals__ | {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})(
        previous, candidate, arm)
    checked = {(r["file_path"], r["id"]): r for r in rendered["records"]}
    seen = {r["id"] for r in playback["holds"]}
    assert len(checked) == len(draft["records"]) == 37
    for row in draft["records"]:
        path, ident = row["file_path"], row["id"]
        result = checked[path, ident]
        raw, at = bytes.fromhex(result["stored_command_hex"]), result["stored_offset"]
        assert blocks[path][at:at+len(raw)] == raw
        assert row["decision"] == result["decision"]
        if row["decision"] == "revision":
            assert ident in seen and result["native_pages"] == 1
        row["review"]["formatting"] = True
        row["registered_reference"] = dict(file_path=path, block=row["block"], offset=at,
            exact_command_hex=raw.hex(), archive_sha256=archives[path],
            block_sha256=groups[path]["after"], candidate_sha256=candidate)
        row["observed_in_initialized_excerpt"] = ident in seen
        row["native_formatting_evidence"] = result
    draft.update(candidate_sha256=candidate, status="registered", direct_visual_review=viewed,
        checked_story_format_guard=controls, new_contextual_credit=0, shared_payload_and_lookup_exact=True,
        native_preview_evidence=str(display.PROOF), excerpt_evidence=str(live.PROOF),
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"])
    validate_natural_dialogue_batch(draft)
    return stored, draft, archives


@contextmanager
def mapped(path):
    with path.open("rb") as file, mmap(file.fileno(), 0, access=ACCESS_READ) as data:
        yield data


def field(data, key, depth, start=0, end=None):
    # These release files use a fixed indentation and CRLF, with escaped newlines in string values.
    indent = b" " * depth
    end = len(data) if end is None else end
    pattern = rb'^' + indent + rb'"' + re.escape(key.encode("ascii")) + rb'": '
    match = re.compile(pattern, re.M).search(data, start, end)
    assert match is not None, key
    boundary = re.compile(rb'^(' + indent + rb'"| {0,' + str(depth-1).encode() + rb'}\})', re.M)
    following = boundary.search(data, match.end(), end)
    stop = following.start() if following else end
    assert data[stop-2:stop] == b"\r\n"
    value_end = stop - 2 - int(data[stop-3:stop-2] == b",")
    return match.start(), match.end(), value_end, stop


def value(data, key, depth, start=0, end=None):
    _, first, last, _ = field(data, key, depth, start, end)
    return loads(data[first:last])


def encoding(key, data, indent, step):
    line = " " * indent + dumps(key) + ": "
    raw = dumps(data, ensure_ascii=False, indent=step).replace("\n", "\r\n" + " " * indent)
    return (line + raw).encode()


def replace_value(data, key, new, depth):
    first, _, last, _ = field(data, key, depth)
    return first, last, encoding(key, new, depth, depth)


def added_field(data, key, new, indent, step, start=0, end=None):
    end = len(data) if end is None else end
    close = data.rfind(b"\r\n" + b" " * (indent-step) + b"}", start, end)
    assert close > start and data[close-1:close] not in (b"{", b",")
    return close, close, b",\r\n" + encoding(key, new, indent, step)


def write_update(data, path, edits):
    old = 0
    with path.open("xb") as file:
        for start, stop, replacement in sorted(edits):
            assert old <= start <= stop <= len(data)
            for pos in range(old, start, 1 << 20):
                file.write(data[pos:min(pos+(1 << 20), start)])
            file.write(replacement)
            old = stop
        for pos in range(old, len(data), 1 << 20):
            file.write(data[pos:min(pos+(1 << 20), len(data))])


def archive(path, destination):
    with path.open("rb") as source, destination.open("xb") as raw:
        with GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            copyfileobj(source, compressed, 1 << 20)


def copy_in_place(source, destination):
    with source.open("rb") as stream, destination.open("r+b") as target:
        assert base.digest(source) != base.digest(destination)
        copyfileobj(stream, target, 1 << 20)
        target.truncate()
        target.flush()
        fsync(target.fileno())
    assert base.digest(source) == base.digest(destination)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-review", type=Path, required=True)
    parser.add_argument("--finish", action="store_true", help="Finish a prepared transaction after an interrupted write.")
    args = parser.parse_args()
    if args.finish:
        commit(base.load(VERIFY / "registration_mutation_plan.json"))
        return
    snapshot = dict(registry_before=base.digest(base.REGISTRY), ledger_before=base.digest(base.LEDGER),
                    main_sha256=base.digest(base.PROMOTED))
    previous = base.load(parent.RELEASE)
    assert snapshot["registry_before"] == previous["registry_sha256"]
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    registry_backup = ROOT / "release_stack_before_moonlit_violin.json"
    registry_next = ROOT / "release_stack_with_moonlit_violin.json"
    ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"
    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC, ledger_backup, ledger_next))
    with mapped(base.REGISTRY) as data:
        assert len(value(data, "accepted_layers", 2)) == 114
        _, profiles, before_close, _ = field(data, "profiles", 2)
        profile = value(data, previous["profile"], 4, profiles, before_close)
    _, draft, archives = verify({"profiles": {previous["profile"]: profile}}, previous, base.load(args.visual_review))
    candidate = draft["candidate_sha256"]

    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    copyfile(base.REGISTRY, registry_backup)
    copyfile(base.LEDGER, ledger_backup)
    predecessor = {k: previous[k] for k in
        ("profile", "candidate", "candidate_sha256", "manifest", "manifest_sha256", "registry_sha256")}
    predecessor["registry"] = str(registry_backup)
    profile.update(verified_search_forage_wrap_predecessor=predecessor, moonlit_violin_release=str(REVIEW))
    with mapped(base.REGISTRY) as data:
        write_update(data, registry_next, [added_field(data, PROFILE, profile, 4, 2, profiles, before_close)])
    registry_sha = base.digest(registry_next)
    with mapped(registry_next) as data:
        assert value(data, PROFILE, 4) == profile
    for src, target in ((EVIDENCE / "translation.xdelta", PATCH), (EVIDENCE / "clean_rebuilt.nds", ROM)):
        copyfile(src, target)
        assert base.digest(src) == base.digest(target)
    assert base.digest(ROM) == candidate
    for source in (stage.PROOF, STARTUP, QA, live.PROOF, display.PROOF, args.visual_review,
                   *(Path(p) for p in base.load(args.visual_review))):
        copyfile(source, VERIFY / source.name)
        assert base.digest(source) == base.digest(VERIFY / source.name)
    base.save(REVIEW, draft)
    with mapped(parent.MANIFEST) as data:
        assert value(data, "candidate_sha256", 2) == previous["candidate_sha256"]
        assert value(data, "release_stack_sha256", 2) == snapshot["registry_before"]
        batches, checks, changed = (value(data, k, 2) for k in ("batches", "checks", "changed_records"))
        assert len(batches) == 979 and len(checks) == 314 and all(checks.values())
        batches.append(str(REVIEW))
        checks["registered_moonlit_violin_and_complete_parent_inverse"] = True
        for r in draft["records"]:
            if r["decision"] == "revision" and r["id"] not in changed[r["file_path"]]:
                changed[r["file_path"]].append(r["id"])
        changes = dict(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=candidate,
            release_stack_sha256=registry_sha, batches=batches, checks=checks, changed_records=changed)
        node = dict(predecessor=predecessor, registered_review=str(REVIEW), registered_review_sha256=base.digest(REVIEW),
            registration_driver_sha256=base.digest(__file__), stored_proof_sha256=base.digest(stage.PROOF),
            native_and_emulator_evidence_sha256=base.digest(live.PROOF), complete_parent_inverse=True,
            original_name_substitution_order=True, archive_hashes=archives, source_movie_preserved=True,
            target_ARM9_sha256=previous["target_ARM9_sha256"])
        edits = [replace_value(data, key, new, 2) for key, new in changes.items()]
        write_update(data, MANIFEST, [*edits, added_field(data, "moonlit_violin_pipeline", node, 2, 2)])
    with mapped(MANIFEST) as data:
        assert all(value(data, k, 2) == val for k, val in changes.items())
        assert value(data, "moonlit_violin_pipeline", 2) == node
    startup = VERIFY / STARTUP.name
    release = previous | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=candidate, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=registry_sha, predecessor=predecessor, registered_manifest_entries=len(batches),
        passing_release_checks=len(checks), own_registered_startup=str(startup),
        own_registered_startup_sha256=base.digest(startup), changed_internal_files=sorted(archives),
        changed_components=2, repository_tests=17, legacy_fixture_tests_skipped=0, reviewed_UI_labels=0,
        previously_localized_records=37, new_contextual_records=0, prose_revisions=4, spacing_revisions=0,
        wrap_only_revisions=0, justified_retentions=32, name_label_revisions=0, text_display_revisions=1,
        pagination_fixes=0, name_consistency_revisions=0,
        actual_verification_scope=dict(own_startup=True, initialized_Rafael_and_Hodram_excerpts=True,
            native_revised_pages=5, observed_panels=21, natural_activation=False, hardware=False),
        **{f"target_SC{i}_sha256": archives.get(f"/data/SC{i}.DK4", previous[f"target_SC{i}_sha256"]) for i in range(4)})
    base.save(RELEASE, release)
    base.save(PACKAGE / "release_manifest.json", release | {"user_acceptance_pending": True})
    archive(MANIFEST, PACKAGE / "build_manifest.json.gz")
    archive(registry_next, PACKAGE / "build_release_stack.json.gz")
    archive(ledger_backup, ROOT / "editorial_ledger_before.json.gz")

    with mapped(base.LEDGER) as data:
        assert value(data, "records_editorially_completed", 1) == 27700
        assert not value(data, "full_goal_complete", 1)
        _, start, stop, _ = field(data, base.CONTEXT, 1)
        credited = {(r["file_path"], r["id"]) for r in value(data, "integrated_record_keys", 2, start, stop)}
        assert len(credited) == 27700 and all((r["file_path"], r["id"]) in credited for r in draft["records"])
        pending = value(data, "pending_shared_consumer_checkpoint_20261114", 1)
        current = value(data, "current_integrated_candidate", 1)
        assert pending["remaining_total"] == 276 and pending["candidate_sha256"] == current["sha256"] == previous["candidate_sha256"]
        pending.update(candidate_sha256=candidate, latest_unchanged_record_binding=str(REVIEW))
        current.update(path=str(ROM), sha256=candidate, profile=PROFILE, patch=str(PATCH),
            patch_sha256=release["patch_sha256"], manifest=str(MANIFEST), manifest_sha256=release["manifest_sha256"],
            registered_release_verification=str(RELEASE),
            **{f"SC{i}_sha256": release[f"target_SC{i}_sha256"] for i in range(4)})
        changes = dict(pending_shared_consumer_checkpoint_20261114=pending, current_integrated_candidate=current,
                       latest_checkpoint=CHECKPOINT)
        entry = dict(registered_candidate_sha256=candidate, registered_review=str(REVIEW), registered_release=str(RELEASE),
            prior_records_reviewed=37, actual_Rafael_and_Hodram_panels=21, offline_pages=5, new_contextual_credit=0,
            prose_revisions=4, justified_retentions=32, text_display_revisions=1)
        edits = [replace_value(data, key, new, 1) for key, new in changes.items()]
        write_update(data, ledger_next, [*edits, added_field(data, "moonlit_violin_20261121", entry, 1, 1)])
    with mapped(ledger_next) as data:
        assert all(value(data, k, 1) == new for k, new in changes.items())
        assert value(data, "moonlit_violin_20261121", 1) == entry
    assert base.digest(registry_backup) == snapshot["registry_before"] == base.digest(base.REGISTRY)
    assert base.digest(ledger_backup) == snapshot["ledger_before"] == base.digest(base.LEDGER)
    base.save(VERIFY / "registration_mutation_plan.json", snapshot | dict(
        registry_after=registry_sha, ledger_after=base.digest(ledger_next)))
    (PACKAGE / "README.md").write_text(f"""# Moonlit violin testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes both reviewed versions of the encounter. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte.
""", encoding="utf-8")
    base.save(PACKAGE / "checksums.json", workflow.package_checksums(PACKAGE))
    commit(base.load(VERIFY / "registration_mutation_plan.json"))


def commit(plan):
    registry_backup = ROOT / "release_stack_before_moonlit_violin.json"
    registry_next = ROOT / "release_stack_with_moonlit_violin.json"
    ledger_backup, ledger_next = ROOT / "ledger_before.json", ROOT / "ledger_after.json"
    assert not DOC.exists()
    assert plan["registry_before"] == base.digest(base.REGISTRY) == base.digest(registry_backup)
    assert plan["ledger_before"] == base.digest(base.LEDGER) == base.digest(ledger_backup)
    assert plan["main_sha256"] == base.digest(base.PROMOTED)
    assert plan["registry_after"] == base.digest(registry_next)
    assert plan["ledger_after"] == base.digest(ledger_next)
    release = base.load(RELEASE)
    candidate = release["candidate_sha256"]
    assert candidate == base.digest(ROM) == base.digest(stage.ROM)
    assert base.digest(PATCH) == release["patch_sha256"] and base.digest(MANIFEST) == release["manifest_sha256"]
    assert base.load(PACKAGE / "checksums.json") == workflow.package_checksums(PACKAGE)
    try:
        copy_in_place(registry_next, base.REGISTRY)
        update_ledger_in_place(ledger_backup.read_bytes(), ledger_next.read_bytes())
    except (OSError, AssertionError):
        for before, actual in ((registry_backup, base.REGISTRY), (ledger_backup, base.LEDGER)):
            if base.digest(before) != base.digest(actual):
                copy_in_place(before, actual)
        raise
    assert base.digest(base.PROMOTED) == plan["main_sha256"]
    pin_path = Path("translations/rom_retention_pins.json")
    pins = base.load(pin_path)
    for path in (ROM, stage.ROM, parent.ROM, *(Path(p) for p in base.load(live.PROOF)["evidence"] if p.endswith(".nds"))):
        absolute = str(path.resolve())
        if all(pin["path"] != absolute for pin in pins):
            pins.append(dict(path=absolute, reason=f"Preserve the violin candidate or replay ROM {base.digest(path)}"))
    base.replace_checked(pin_path, (dumps(pins, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n").encode())
    DOC.write_text(f"""# The moonlit violin encounter

Reviewed all 37 records across Rafael’s and Hodram’s versions. Rafael’s opening now uses two lines and trails off before the violin appears. In both accounts Hodram wonders privately whether Sera knows Rafael. The crewmate’s question fits Hodram looking for Sera, and Rafael’s smile follows the scene’s other action cues. The other 32 records have individual reasons for retention. [Exact source, prior and registered dialogue](../{REVIEW.as_posix()})

Five revised pages passed native bounds and visual review. Initialized emulator excerpts displayed 21 complete panels, including the revised dialogue and Sera’s player-name substitutions. The natural trigger was outside the replay. The original story commands still select the same violin movie. The stored COMMON 3410 label has an artwork association and its independent display path remains unverified.

Six startup holds, 24 protected name getters, and 17 focused tests passed. [Cumulative testing ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
    prefix = f"# Current editorial checkpoint - 2026-11-21\n\n{CHECKPOINT} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md", "translation_progress.md", "build_continuity_protocol.md"):
        path = DOC.with_name(name)
        base.replace_checked(path, prefix + path.read_bytes())
    print(f"Registered {candidate} with {release['registered_manifest_entries']} entries, 114 accepted layers and "
          f"{release['passing_release_checks']} passing checks.", flush=True)


if __name__ == "__main__":
    main()


