"""Reconcile the eight registered deltas since the Kurushima editorial audit."""

from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import register_nagasaki_contract_wrap_20261124 as contract
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.seal_shared_text_source_v1 import reference as message_reference
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
OUT = ROOT / "editorial_acceptance_after_yard_20261124.json"
ANCHOR = ROOT / "editorial_acceptance_after_kurushima_20261123.json"
DRIVE = ROOT / "yard_numerals_drive_20261124.json"
LEDGER = Path("translations/editorial_review_current_v1.json")
ARCHIVED = ROOT / "archived_message_storage_20261124.json"
ARM, COMMON, HELP = "/__arm9__.bin", "/COMMON/MESFILE.DK4", "/COMMON/HELP.DK4"
SC0, SC1 = "/data/SC0.DK4", "/data/SC1.DK4"
CHAIN = (
    ("20261123_kurushima_confrontation_wraps", {}),
    ("20261123_rafael_prepare_alone", {SC0: (44,)}),
    ("20261124_athens_item_rumor", {COMMON: (828,)}),
    ("20261124_stockholm_recruiting", {SC1: (134,)}),
    ("20261124_tavern_buy_a_round", {ARM: (), HELP: (12, 14, 15)}),
    ("20261124_nagasaki_contract_wrap", {COMMON: (1157,)}),
    ("20261124_nagasaki_tavern_recruitment", {COMMON: (1045,)}),
    ("20261124_nagasaki_yard_reflow", {COMMON: (1264, 1285, 1287)}),
    ("20261124_yard_numerals", {ARM: ()}),
)


def load(step):
    package = Path("releases") / f"all_routes_editorial_{step}_candidate"
    sums = read(package / "checksums.json")
    paths = [package / "verification" / name for name in ("registered_release_verification.json", "registered_review.json")]
    assert all(digest(path) == sums[path.relative_to(package).as_posix()] for path in paths)
    release, review = map(read, paths)
    assert digest(release["candidate"]) == release["candidate_sha256"] == review["candidate_sha256"]
    for field in ("manifest", "patch", "own_registered_startup"):
        assert digest(release[field]) == release[f"{field}_sha256"]
    assert release["accepted_layers"] == 114 and release["experimental_not_promoted"]
    assert release["clean_input_patch_byte_exact"] and release["whole_parent_inverse_exact"] and not release["own_registered_startup_pending"]
    assert review["translation_policy"] == "natural-dialogue-v2" and review["target_locale"] == "en-US"
    assert all(set(row["review"]) == set(GATES) and all(row["review"].values()) for row in review["records"])
    return release, review, list(map(reference, paths)), NdsImage.open(release["candidate"])


def assets(image):
    return {**{path: raw for _, path, raw in image.iter_files()}, **dict(image.iter_components())}


def story_command(block, ref):
    assert sha256(block).hexdigest() == ref["block_sha256"]
    offset = ref["command_offset"]
    cmd = bytes.fromhex(ref.get("exact_command_hex", ""))
    if not cmd:
        body = bytes.fromhex(ref["exact_body_hex"])
        cmd = block[offset:offset + 6 + len(body) + 1]
        assert cmd[6:] == body + b"\0"
    assert block[offset:offset + len(cmd)] == cmd
    return cmd


def story_review(path, block_id, clean_raw, before_raw, after_raw, review, reference_to_review):
    clean, before, after = (IlnkContainer.parse(raw).blocks[block_id] for raw in (clean_raw, before_raw, after_raw))
    row, = [item for item in review["records"] if item["decision"] == "revision"]
    source, old, installed = (story_command(block, row[key]) for block, key in (
        (clean, "source_reference"), (before, "current_reference"), (after, "registered_reference")))
    assert source[:6] == old[:6] == installed[:6] and len(old) == len(installed) and installed.endswith(b"\0")
    rendered = installed[6:installed.index(0, 6)]
    assert " ".join(rendered.decode("ascii").split()) == row["english"]
    at = row["registered_reference"]["command_offset"]
    assert after[:at] + old + after[at + len(installed):] == before
    old_body = row["registered_reference"].get("exact_body_hex")
    correction = None
    if old_body is not None and old_body != rendered.hex():
        assert bytes.fromhex(old_body) == old[6:old.index(0, 6)]
        correction = dict(reference_field="registered_reference.exact_body_hex", archived_review=reference_to_review,
                          superseded_hex=old_body, corrected_hex=rendered.hex(), command_hex=installed.hex(), body_offset=at + 6)
    return dict(file=path, block=block_id, id=row["id"], source_command_hex=source.hex(), previous_command_hex=old.hex(),
                installed_command_hex=installed.hex(), installed_body_hex=rendered.hex(), factual_review=row["review"],
                reference_correction=correction)


def common_review(clean_rows, old, new, expected, review):
    old_rows, new_rows = (common_rows(data[COMMON], data[ARM]) for data in (old, new))
    assert len(old_rows) == len(new_rows) == 3668
    differences = [a.message_id for a, b in zip(old_rows, new_rows, strict=True) if a.text != b.text]
    assert differences == list(expected)
    rows = {int(r["id"].rsplit("_", 1)[1]): r for r in review["records"] if r["decision"] == "revision"}
    assert set(rows) == set(expected)
    verified = []
    for index in expected:
        row = rows[index]
        exact = (clean_rows[index], old_rows[index], new_rows[index])
        for bound, key in zip(exact, ("source_reference", "current_reference", "registered_reference"), strict=True):
            ref = row[key]
            assert all(ref[field] == value for field, value in message_reference(bound).items())
            if "exact_stored_hex" in ref:
                assert ref["exact_stored_hex"] == bound.text.hex()
        assert row["installed_hex"] == exact[-1].text.hex()
        verified.append(dict(message_ID=index, source=exact[0].text.hex(), previous=exact[1].text.hex(), installed=exact[2].text.hex()))
    return verified


def latest_manifest(release):
    assert digest(REGISTRY) == release["registry_sha256"]
    registry = read(REGISTRY)
    accepted = registry["accepted_layers"]
    assert len(accepted) == release["accepted_layers"] == 114
    del registry
    manifest = read(release["manifest"])
    assert manifest["candidate_sha256"] == release["candidate_sha256"] and manifest["release_stack_sha256"] == release["registry_sha256"]
    assert manifest["profile"] == release["profile"]
    assert len(manifest["batches"]) == release["registered_manifest_entries"] == 1125
    assert len(manifest["checks"]) == release["passing_release_checks"] == 460 and all(manifest["checks"].values())
    keys = {p.replace("\\", "/") for p in manifest["batches"]}
    assert all(row["status"] == "accepted" and (row.get("baked_into_baseline") is True or row["batch"].replace("\\", "/") in keys) for row in accepted)
    return dict(accepted_layers=len(accepted), listed_batches=len(keys), passing_checks=len(manifest["checks"]))


def arm_review(before, after, stored):
    if "changed_ARM9_slot" in stored:
        slot = stored["changed_ARM9_slot"]
        edits = [(slot["offset"], slot["prior_hex"], slot["target_hex"])]
    else:
        edits = [(r["address"] - 0x02000000, r["before_hex"], r["after_hex"]) for r in stored["instruction_changes"]]
        assert len(edits) == 9
    restored = bytearray(after)
    for offset, previous, installed in edits:
        a, b = map(bytes.fromhex, (previous, installed))
        assert len(a) == len(b) and before[offset:offset + len(a)] == a and after[offset:offset + len(b)] == b
        restored[offset:offset + len(a)] = a
    assert restored == before
    return dict(owned_changes=[dict(offset=offset, previous_hex=previous, installed_hex=installed)
                              for offset, previous, installed in edits])


def coverage(anchor, release, review, components):
    ledger = read(LEDGER)
    assert ledger["current_integrated_candidate"]["sha256"] == release["candidate_sha256"]
    assert ledger["full_goal_complete"] is False
    items = ledger["contextual_story_natural_dialogue_pass_v1871"]["integrated_record_keys"]
    historical = ledger["records_editorially_completed"]
    assert len(items) == len({(row["file_path"], row["id"]) for row in items}) == historical == anchor["historical_credit_count"] == 27700
    del ledger, items
    archived = read(ARCHIVED)
    assert archived["candidate_sha256"] == review["shared_consumer_binding"]["candidate_sha256"] == release["candidate_sha256"]
    current = common_rows(components[COMMON], components[ARM])
    records = review["shared_consumer_binding"]["records"]
    assert len(records) == anchor["shared_display"]["scoped_rows"] == 276
    assert all(r["exact_body_retained"] and r["installed"] == message_reference(current[r["message_ID"]]) for r in records)
    archived_keys = [284, 318, 750, 751, 752]
    assert all(archived["installed"]["archived_records"][str(key)]["exact_hex"] == current[key].text.hex() for key in archived_keys)
    return dict(historical_review_credits=historical, story_positions=anchor["previous_credited_story_positions"],
                priority_groups=anchor["priority_decisions"]["groups"], scopes_reused_outside_changed_blocks=[SC0 + " B44", SC1 + " B134"],
                shared_dispositions=276, open_archived_display_keys=archived_keys, exact_storage_proof=reference(ARCHIVED), ledger=reference(LEDGER))


def main():
    anchor = read(ANCHOR)
    prior, _, _, previous_image = load(CHAIN[0][0])
    assert prior["candidate_sha256"] == anchor["candidate_sha256"] and digest(CLEAN) == prior["clean_input_sha256"]
    clean = NdsImage.open(CLEAN)
    clean_rows = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    prior_files = assets(previous_image)
    results = []
    for step, scope in CHAIN[1:]:
        release, review, refs, image = load(step)
        assert list(sorted(scope)) == sorted(release["changed_internal_files"])
        assert release["clean_input_sha256"] == prior["clean_input_sha256"] and release["canonical_sha256"] == prior["canonical_sha256"]
        assert all(prior[key] == release["predecessor"][key] for key in ("candidate_sha256", "manifest_sha256", "registry_sha256"))
        assert release["passing_release_checks"] == prior["passing_release_checks"] + 1
        assert release["registered_manifest_entries"] == prior["registered_manifest_entries"] + 1
        current_files = assets(image)
        assert current_files.keys() == prior_files.keys() and {p for p in current_files if prior_files[p] != current_files[p]} == scope.keys()
        proofs = {}
        for path, ids in scope.items():
            if path == COMMON:
                proofs[path] = common_review(clean_rows, prior_files, current_files, ids, review)
            elif path == ARM:
                stored = Path(refs[1]["path"]).with_name("stored_proof.json")
                assert digest(stored) == review["stored_proof"]["sha256"]
                proofs[path] = arm_review(prior_files[path], current_files[path], read(stored))
            else:
                before, after = (IlnkContainer.parse(data[path]).blocks for data in (prior_files, current_files))
                assert [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b] == list(ids)
                proofs[path] = dict(changed_blocks=ids)
                if path in (SC0, SC1):
                    proofs[path]["revision"] = story_review(path, ids[0], clean.read_file(path), prior_files[path], current_files[path], review, refs[1])
                else:
                    assert len(IlnkContainer.parse(clean.read_file(HELP)).blocks) == 202 and len(after) == 217
                    for row in review["records"]:
                        if row["file_path"] == HELP and row["decision"] == "revision":
                            ref = row["registered_reference"]
                            assert ref["block"] in ids and after[ref["block"]].hex() == ref["exact_block_hex"]
            image.replace_file(path, prior_files[path])
        assert sha256(image.rom.save()).hexdigest() == prior["candidate_sha256"]
        results.append(dict(step=step, candidate_sha256=release["candidate_sha256"], changed_paths=sorted(scope),
                            review_counts=dict(Counter(row["decision"] for row in review["records"])), exact_work=proofs, evidence=refs))
        prior, prior_files = release, current_files

    assert contract.template.right_bound(prior_files[ARM], prior["right_bound_configuration"])["matched_repair_spans"] == 8
    for i in range(4):
        assert sha256(prior_files[f"/data/SC{i}.DK4"]).hexdigest() == prior[f"target_SC{i}_sha256"]
    assert sha256(prior_files[HELP]).hexdigest() == prior["target_HELP_sha256"]
    startup = read(prior["own_registered_startup"])
    assert startup["candidate_sha256"] == prior["candidate_sha256"] and startup["cold_boot"] and not startup["savestate"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(Path(prior["own_registered_startup"]).with_name("qa_passed.xml")).iter("testsuite")
    stats = {key: int(suite.get(key, "0")) for key in ("tests", "failures", "errors", "skipped")}
    assert stats == dict(tests=17, failures=0, errors=0, skipped=0)
    drive = read(DRIVE)
    assert drive["nds_files_in_folder"] == 1 and drive["streamed_readback_exact"]
    assert drive["downloaded_sha256"] == drive["candidate_sha256"] == prior["candidate_sha256"]
    round_trip_path = Path(prior["own_registered_startup"]).with_name("clean_patch_proof.json")
    round_trip = read(round_trip_path)
    assert round_trip["byte_exact"] and round_trip["clean_input_sha256"] == prior["clean_input_sha256"]
    assert round_trip["patch"]["sha256"] == prior["patch_sha256"]
    assert round_trip["candidate"]["sha256"] == round_trip["rebuilt"]["sha256"] == prior["candidate_sha256"]
    write(OUT, dict(candidate_sha256=prior["candidate_sha256"], prior_intact_audit=reference(ANCHOR),
                    exact_registered_deltas=results, manifest=latest_manifest(prior), ascii_right_bound_spans=8,
                    current_coverage=coverage(anchor, prior, review, prior_files),
                    focused_repository_tests=stats, candidate_startup=reference(prior["own_registered_startup"]),
                    exact_round_trip_receipt=reference(round_trip_path),
                    same_candidate_prior_drive_receipt=reference(DRIVE), ordinary_gameplay_added=False,
                    remaining="Unknown archived COMMON callers, alternate runtime Fleet Info producers, and practical additional town and random scenes stay open.",
                    ROM_changed=False, full_editorial_goal_complete=False, new_editorial_credit=0))
    print(f"Verified {len(results)} exact release inverses, the six latest startup holds, and 460 passing release checks.")


if __name__ == "__main__":
    main()
