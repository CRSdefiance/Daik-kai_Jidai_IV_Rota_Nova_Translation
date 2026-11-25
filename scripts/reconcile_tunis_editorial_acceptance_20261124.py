"""Bind the latest three releases and the inherited editorial inventory to Tunis."""

from collections import Counter
from itertools import pairwise
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from ndspy.code import MainCodeFile
from scripts import audit_current_name_aliases_20261123 as aliases
from scripts import reconcile_archived_message_reader_20261124 as reader
from scripts import reconcile_kurushima_acceptance_20261123 as kurushima
from scripts import reconcile_shared_reference_coverage_20261124 as callers
from scripts import reconcile_yard_editorial_acceptance_20261124 as yard
from scripts import verify_archived_message_storage_20261124 as storage
from scripts.seal_shared_text_source_v1 import reference as message_reference
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_yard_numerals_native_20261124 import call_number, get_machine
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_R2


ROOT = yard.ROOT
OUT = ROOT / "editorial_acceptance_after_tunis_20261124.json"
DRIVE = ROOT / "tunis_shop_advice_drive_20261124.json"
SHARED = ROOT / "shared_editorial_coverage_20261123.json"
ARM, COMMON, HELP = yard.ARM, yard.COMMON, yard.HELP
ROUTES = tuple(f"/data/SC{i}.DK4" for i in range(4))
STEPS = (
    ("20261124_yard_numerals", (), None),
    ("20261124_london_guild_display", (1073, 1084), "london_guild_display_preflight_20261124.json"),
    ("20261124_guild_trade_numerals", (1072, 1083, 1086, 1095), "guild_trade_numerals_preflight_20261124.json"),
    ("20261124_tunis_shop_advice", (654,), "stored_proof.json"),
)
YARD_PRICE_CALL = 0x020630FC
YARD_OWNER_SCOPE = (0x02063038, 0x02063140)


def refs(before, after, jp, review, expected):
    assert len(before) == len(after) == len(jp) == 3668
    assert {a.message_id for a, b in zip(before, after, strict=True) if a.text != b.text} == set(expected)
    changed = {row["message_ID"]: row for row in review["records"]
               if row["decision"] == "revision" and row["file_path"] == COMMON}
    assert changed.keys() == set(expected)
    results = []
    for key in expected:
        row = changed[key]
        exact = dict(message_ID=key)
        for kind, entry in zip(("source", "current", "registered"), (jp[key], before[key], after[key]), strict=True):
            ref = row[f"{kind}_reference"]
            assert all(ref[prop] == value for prop, value in message_reference(entry).items())
            recorded_hex = ref.get("exact_stored_hex", ref.get("exact_hex", row.get(f"{kind}_hex")))
            assert recorded_hex == entry.text.hex()
            exact[f"{kind}_reference"] = ref
        assert " ".join(after[key].text.decode("ascii").split()) == row["english"]
        exact["english"] = row["english"]
        results.append(exact)
    return results


def arm_delta(old, new, edits):
    restored = bytearray(new)
    changes = []
    for entry in edits:
        at = entry["offset"] if "offset" in entry else entry["address"] - 0x02000000
        a, b = (bytes.fromhex(entry[key]) for key in ("previous_hex", "installed_hex"))
        assert len(a) == len(b) and old[at:at + len(a)] == a and new[at:at + len(b)] == b
        restored[at:at + len(a)] = a
        changes.append(dict(offset=at, previous_hex=a.hex(), installed_hex=b.hex()))
    assert restored == old
    return changes


def exact_deltas(clean, history):
    jp = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    results = []
    for (_, previous), ((tag, numbers, stored_name), current) in pairwise(zip(STEPS, history, strict=True)):
        parent, _, _, old_image = previous
        release, review, files, image = current
        assert all(parent[k] == release["predecessor"][k] for k in
                   ("candidate", "candidate_sha256", "registry_sha256", "manifest_sha256"))
        assert release["passing_release_checks"] == parent["passing_release_checks"] + 1
        assert release["registered_manifest_entries"] == parent["registered_manifest_entries"] + 1
        assert release["clean_input_sha256"] == parent["clean_input_sha256"] == digest(CLEAN)
        assert release["canonical_sha256"] == parent["canonical_sha256"]
        before, after = map(yard.assets, (old_image, image))
        assert before.keys() == after.keys()
        stored_path = Path(files[1]["path"]).with_name(stored_name)
        assert digest(stored_path) == review["stored_proof"]["sha256"]
        stored = read(stored_path)
        changes = {path for path in before if before[path] != after[path]}
        edits = stored.get("exact_ARM9_edits", [])
        expected = {COMMON, ARM} if edits else {COMMON}
        assert changes == expected == set(release["changed_internal_files"])
        exact_arm = arm_delta(before[ARM], after[ARM], edits)
        get = lambda assets: yard.common_rows(assets[COMMON], assets[ARM])
        exact_prose = refs(get(before), get(after), jp, review, numbers)
        for path in changes:
            image.replace_file(path, before[path])
        try:
            assert sha256(image.rom.save()).hexdigest() == parent["candidate_sha256"]
        finally:
            for path in changes:
                image.replace_file(path, after[path])
        results.append(dict(step=tag, candidate_sha256=release["candidate_sha256"], changed_paths=sorted(changes),
            native_ARM9_edits=exact_arm, verified_COMMON_revisions=exact_prose, exact_predecessor_inverse=True,
            review_counts=dict(Counter(row["decision"] for row in review["records"])), evidence=files))
    return results


def package_state(release, last_package):
    assert digest(REGISTRY) == release["registry_sha256"]
    registry = read(REGISTRY)
    accepted = registry["accepted_layers"]
    assert len(accepted) == 114 and registry["profiles"][release["profile"]]["status"] == "experimental"
    manifest = read(release["manifest"])
    assert manifest["candidate_sha256"] == release["candidate_sha256"]
    assert manifest["release_stack_sha256"] == release["registry_sha256"] and manifest["profile"] == release["profile"]
    batches = {path.replace("\\", "/") for path in manifest["batches"]}
    checks = manifest["checks"]
    assert len(batches) == release["registered_manifest_entries"] == 1128
    assert len(checks) == release["passing_release_checks"] == 463 and all(checks.values())
    assert all(row["status"] == "accepted" and
               (row.get("baked_into_baseline") or row["batch"].replace("\\", "/") in batches) for row in accepted)
    startup_path = Path(release["own_registered_startup"])
    startup, drive = map(read, (startup_path, DRIVE))
    assert startup["candidate_sha256"] == drive["downloaded_sha256"] == drive["candidate_sha256"] == release["candidate_sha256"]
    assert startup["cold_boot"] and not startup["savestate"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(startup_path.with_name("qa_passed.xml")).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "errors", "failures", "skipped")] == [17, 0, 0, 0]
    assert drive["streamed_readback_exact"] and drive["nds_files_in_folder"] == 1
    patch_path = startup_path.with_name("clean_patch_proof.json")
    patch = read(patch_path)
    assert patch["byte_exact"] and patch["clean_input_sha256"] == release["clean_input_sha256"]
    assert patch["candidate"]["sha256"] == patch["rebuilt"]["sha256"] == release["candidate_sha256"]
    assert patch["patch"]["sha256"] == release["patch_sha256"]
    package_files = read(last_package / "checksums.json")
    assert all(digest(last_package / path) == expected for path, expected in package_files.items())
    return dict(manifest_batches=len(batches), passing_checks=len(checks), accepted_layers=len(accepted),
                candidate_startup=reference(startup_path), clean_patch_round_trip=reference(patch_path),
                drive_readback=reference(DRIVE), candidate_regressions=17, package_file_checks=len(package_files))


def recheck_yard_argument(arm, lock, release):
    original = NdsImage.open(CLEAN).read_file(ARM)
    lo, hi = YARD_OWNER_SCOPE
    assert (lo, hi) == (lock["start"], lock["end"])
    old, new = (callers.tape(data, lo, hi) for data in (original, arm))
    assert sha256(old).hexdigest() == lock["sha256"]
    i = YARD_PRICE_CALL - lo
    assert old[:i] == new[:i] and old[i + 4:] == new[i + 4:]
    yard_package = Path("releases/all_routes_editorial_20261124_yard_numerals_candidate")
    patch = yard_package / "verification/stored_proof.json"
    assert digest(patch) == read(yard_package / "checksums.json")["verification/stored_proof.json"]
    change, = [row for row in read(patch)["instruction_changes"] if row["address"] == YARD_PRICE_CALL]
    assert old[i:i + 4].hex() == change["before_hex"] and new[i:i + 4].hex() == change["after_hex"]
    literal = 0x02063210
    assert unpack_from("<I", arm, literal - reader.BASE) == unpack_from("<I", original, literal - reader.BASE) == (1245,)
    snapshot = read(release["own_registered_startup"])["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert sha256(raw).hexdigest() == snapshot["sha256"]
    assert callers.tape(raw, lo, hi) == new
    cpu, _ = get_machine(arm, raw)
    results = []
    for amount in (0, 1, 99, 100, 7500, 65535, 2147483647):
        pointer, text = call_number(cpu, YARD_PRICE_CALL, amount)
        assert text == str(amount).encode("ascii")
        # Stop at the real wrapper branch after loading the ID and the numeric argument.
        cpu.emu_start(YARD_PRICE_CALL + 4, 0x0206310C, count=8)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x0206310C and cpu.reg_read(UC_ARM_REG_R2) == pointer
        assert cpu.reg_read(UC_ARM_REG_R1) == 1245
        results.append(dict(amount=amount, rendered=text.decode("ascii"), message_ID=1245))
    return dict(scope=[lo, hi], previous_sha256=lock["sha256"], installed_sha256=sha256(new).hexdigest(),
                sole_edit=change, source_literal=literal, native_argument_cases=results, registered_Yard_edit=reference(patch))


def archived_arguments(clean, image, release):
    early, completed, reader_receipt = map(read, (callers.OUT, reader.bounded.OUT, reader.OUT))
    arm = image.read_file(ARM)
    sites = {(row["call_site"], row["entry"], row["instruction"], row["component"]): row for row in early["references"]}
    aligned = callers.forwarding.earlier.prior.census(release["candidate"])
    assert aligned == sites.keys() and len(aligned) == completed["fully_bounded_census_sites"] == 827
    resolved = {(row["call_site"], row["target"]): row for row in completed["completed_bindings"]}
    assert {key[:2] for key, row in sites.items() if row["possible_COMMON_ids"] is None} == resolved.keys()
    for key, row in sites.items():
        ids = row["possible_COMMON_ids"]
        if ids is None:
            ids = resolved[key[:2]]["ids"]
        assert set(ids).isdisjoint(storage.KEYS)
    indirect = reader.bounded.indirect(clean, image, clean.read_file(ARM), arm)
    assert len(indirect) == 5
    assert all({k: resolved[key][k] for k in item} == item for key, item in indirect.items())
    spans = [*early["supplementary_literal_and_table_locks"],
             *(row for records in early["earlier_native_locks"].values() for row in records),
             *(lock for key, row in resolved.items() if key not in indirect for lock in row["exact_locks"])]
    changed = [row for row in spans if sha256(callers.tape(arm, row["start"], row["end"])).hexdigest() != row["sha256"]]
    yard_span, = changed
    yard_recheck = recheck_yard_argument(arm, yard_span, release)
    sections = MainCodeFile(arm, reader.BASE).sections
    for row in early["exact_alias_code_spans"]:
        lo, hi = row["start"], row["end"]
        section, = [s for s in sections if s.ramAddress <= lo < hi <= s.ramAddress + len(s.data)]
        assert sha256(section.data[lo - section.ramAddress:hi - section.ramAddress]).hexdigest() == row["sha256"]
    found = reader.references(image, set(reader_receipt["checked_wrapper_entries"]), installed=True)
    assert found == [tuple(row) for row in reader_receipt["current_external_references"]]
    table = reader.reader.references(release["candidate"])
    prior_table = dict(reader_receipt["filename_directory_and_offset_literal_readers"])
    for key in ("aligned_archive_range_pointer_words", "archive_name_locations"):
        prior_table[key] = [tuple(row) for row in prior_table[key]]
    assert table == prior_table
    return dict(aligned_callers=827, completed_argument_bindings=len(resolved), exact_previous_code_locks=len(spans) - len(changed),
        exact_relocated_alias_spans=len(early["exact_alias_code_spans"]), reader_references=found,
        rechecked_changed_Yard_selector=yard_recheck,
        independent_computed_display_open=True, proof_sources=list(map(reference, (callers.OUT, reader.bounded.OUT, reader.OUT))))


def coverage(clean, current, release, review, prior_counts):
    ledger = read(yard.LEDGER)
    assert ledger["current_integrated_candidate"]["sha256"] == release["candidate_sha256"] and not ledger["full_goal_complete"]
    listed = ledger["contextual_story_natural_dialogue_pass_v1871"]["integrated_record_keys"]
    counts = Counter(row["file_path"] for row in listed)
    assert len(listed) == len({(row["file_path"], row["id"]) for row in listed}) == ledger["records_editorially_completed"] == 27700
    assert dict(counts) == dict(zip((*ROUTES, COMMON, HELP, ARM), (6887, 5356, 6720, 5129, 3392, 202, 14), strict=True))
    credited = {int(row["id"].split("_")[-1]) for row in listed if row["file_path"] == COMMON}
    del ledger, listed
    use = read(SHARED)
    arm = current.read_file(ARM)
    table, archived = storage.inventory(current, clean=False)
    originals = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    prior_archived = {int(key): row for key, row in read(yard.ARCHIVED)["installed"]["archived_records"].items()}
    assert archived["archived_records"] == prior_archived
    approved = review["shared_consumer_binding"]
    assert approved["candidate_sha256"] == release["candidate_sha256"]
    ids = {row["message_ID"] for row in approved["records"]}
    assert len(ids) == len(use["records"]) == 276 and not credited.intersection(ids)
    assert credited | ids == set(range(len(table)))
    assert ids == {row["message_ID"] for row in use["records"]}
    assert all(row["exact_body_retained"] and row["installed"] == message_reference(table[row["message_ID"]])
               for row in approved["records"])
    for row in use["records"]:
        key = row["message_ID"]
        assert row["source_hex"] == originals[key].text.hex() and row["installed_hex"] == table[key].text.hex()
    for row in use["subdivision_evidence"]:
        assert digest(row["path"]) == row["sha256"]

    paragraphs = {path: IlnkContainer.parse(current.read_file(path)).blocks for path in ROUTES}
    clean_story = {path: IlnkContainer.parse(clean.read_file(path)).blocks for path in ROUTES}
    assert sum(map(len, paragraphs.values())) == sum(map(len, clean_story.values())) == 1307
    for index, path in enumerate(ROUTES):
        assert sha256(current.read_file(path)).hexdigest() == release[f"target_SC{index}_sha256"]
        assert current.read_file(f"/data/EV{index}.DK4") == clean.read_file(f"/data/EV{index}.DK4")
    assert sum(counts[path] for path in ROUTES) == prior_counts["story_positions"] == 24092
    priority = kurushima.genoa.acceptance.priority_bindings(clean_story, paragraphs)
    assert priority["groups"] == prior_counts["priority_groups"] and priority["exact_source_and_approved_blocks"] == 416
    source_help, installed_help = (IlnkContainer.parse(image.read_file(HELP)).blocks for image in (clean, current))
    assert len(source_help) == 202 and len(installed_help) == 217
    assert sha256(current.read_file(HELP)).hexdigest() == release["target_HELP_sha256"]

    credit = kurushima.credit
    credit.runtime_scope["verify_runtime"](arm, release)
    release_path = Path(release["own_registered_startup"]).with_name("registered_release_verification.json")
    names_run = FunctionType(credit.names.name_bindings.__code__,
                             vars(credit.names) | {"current": SimpleNamespace(RELEASE=release_path)})
    names = names_run(release, clean.read_file(ARM))
    assert names["original_default_getter_cases"] == 414 and names["checked_clean_and_current_field_slots"] == 621
    assert all(not aliases.OLD.search(row[field].encode("ascii")) for row in names["outputs"]
               for field in ("progressive", "catalogue"))
    assert all(not aliases.OLD.search(block) for blocks in paragraphs.values() for block in blocks)
    assert all(not aliases.OLD.search(row.text) for row in table) and not aliases.OLD.search(current.read_file(HELP))
    configured = read(release["manifest"])["relocations"][ARM]["reviewed_name_integration"]["catalog"]
    visible_routes = [b"\xff".join(paragraphs[path]) for path in ROUTES]
    historical = [row for row in configured["records"] if aliases.OLD.search(bytes.fromhex(row["key_hex"]))]
    assert len(historical) == 197
    for row in historical:
        key = bytes.fromhex(row["key_hex"]) + b"\0"
        assert b"\xff" not in key
        assert not any(key in data for index, data in enumerate(visible_routes) if row["route_mask"] & (1 << index))
    spelling = dict(historical_catalogue_keys_absent_from_allowed_routes=len(historical),
        old_spelling_matches_in_production_story_COMMON_help_and_default_names=0,
        native_older_Hodram_middle_name=aliases.precedent.middle_cases(arm),
        Gallery_captions=aliases.gallery_descriptions(arm, clean.read_file(ARM), current),
        earlier_alias_review=reference(aliases.OUT))
    assert yard.contract.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    return dict(historical_credits_by_path=dict(counts), credited_story_positions=24092, priority_decisions=priority,
        native_COMMON_slots=len(table), credited_COMMON_records=len(credited), scoped_COMMON_records=len(ids),
        remaining_COMMON_without_scoped_disposition=[], retained_common_proof=reference(SHARED),
        archived_storage_owners=archived["archived_records"], still_open_archived_display_ids=sorted(storage.KEYS),
        original_help_topics=len(source_help), installed_help_pages=len(installed_help), ascii_right_bound_spans=8,
        default_names=names, aliases=spelling, user_reported_regressions=dict(Julio=credit.julio_dependency(current, arm),
            Deck=credit.deck_dependencies(current, arm), Trade_Goods_Info_redirect_and_both_data_pointers=True),
        deferred_artwork_ids=use["exact_archived_artwork_identities_open"])


def main():
    anchor = read(yard.OUT)
    history = [yard.load(tag) for tag, _, _ in STEPS]
    assert history[0][0]["candidate_sha256"] == anchor["candidate_sha256"]
    release, review, receipts, current = history[-1]
    clean = NdsImage.open(CLEAN)
    deltas = exact_deltas(clean, history)
    prior_story_reviews = [read(step["evidence"][1]["path"]) for step in anchor["exact_registered_deltas"]
                           if any(path in ROUTES for path in step["changed_paths"])]
    kurushima_package = yard.load("20261123_kurushima_confrontation_wraps")[1]
    wraps = kurushima.wrap_queue(current, [kurushima_package, *prior_story_reviews])
    evidence = coverage(clean, current, release, review, anchor["current_coverage"])
    package = package_state(release, Path(receipts[0]["path"]).parent.parent)
    archive = archived_arguments(clean, current, release)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], yard_acceptance=reference(yard.OUT),
        inherited_eight_deltas=len(anchor["exact_registered_deltas"]), exact_registered_deltas=deltas,
        current_coverage=evidence, current_progressive_wrap_scan=wraps, registered_candidate=package,
        archived_display_argument_continuity=archive,
        remaining=dict(archived_display_owners=sorted(storage.KEYS), Fleet_Info_unobserved_runtime_inputs=True,
                       practical_town_and_random_sampling=True, wider_alias_and_custom_name_paths_require_separate_evidence=True),
        ordinary_gameplay_added=False, ROM_changed=False, new_editorial_credit=0, full_editorial_goal_complete=False))
    print(f"Verified three exact release inverses, all 3,668 scoped COMMON slots, and "
          f"{len(wraps['reviewed_flags'])} retained story wrap dispositions with {len(wraps['open_flags'])} open.")


if __name__ == "__main__":
    main()
