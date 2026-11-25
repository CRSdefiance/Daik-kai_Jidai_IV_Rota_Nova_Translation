"""Reconcile the current cumulative editorial coverage and the remaining acceptance gaps."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import audit_current_editorial_coverage_20261123 as credit
from scripts import reconcile_archived_message_operands_20261123 as archived_operands
from scripts import reconcile_archived_message_selectors_20261123 as archived_selectors
from scripts import rebind_shared_forwarding_20261123 as forwarding
from scripts import reconcile_elegy_acceptance_20261123 as elegy
from scripts import reconcile_genoa_acceptance_20261123 as genoa
from scripts import register_kurushima_confrontation_wraps_20261123 as current
from scripts import scan_current_progressive_wrap_leads_20261111 as scanner
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = genoa.ROOT
OUT = ROOT / "editorial_acceptance_after_kurushima_20261123.json"
DRIVE = ROOT / "kurushima_confrontation_drive_20261123.json"
CLEANUP = ROOT / "kurushima_confrontation_cleanup_20261123.json"
PACKAGES = (genoa.PACKAGES[-1], *(current.PACKAGE.with_name(f"all_routes_editorial_20261123_{name}_candidate")
    for name in ("london_relic_tip", "missionary_destination", "nagasaki_dream", "kurushima_confrontation_wraps")))
ARCHIVES = genoa.WORLDS
ARM, COMMON, HELP = genoa.ARM, genoa.COMMON, genoa.HELP
SHARED, PRIORITY = genoa.acceptance.SHARED, genoa.acceptance.PRIORITY
ARCHIVED = (284, 318, 750, 751, 752)
VOYAGE = ROOT / "maria_post_nagasaki_voyage_20261123.json"


def checks(releases):
    inherited = genoa.registry
    ready = FunctionType(elegy.check_registered_release.__code__, vars(elegy) | dict(RELEASE=current.RELEASE,
        PACKAGE=current.PACKAGE, DRIVE=DRIVE, QA=current.VERIFY / "qa_passed.xml"))
    latest = ready()
    assert latest == releases[-1] and latest["repository_tests"] == 17
    assert [r["passing_release_checks"] for r in releases] == list(range(448, 453))
    assert [r["registered_manifest_entries"] for r in releases] == list(range(1113, 1118))
    assert all(r["accepted_layers"] == 114 and r["experimental_not_promoted"] for r in releases)
    assert all(r["clean_input_patch_byte_exact"] and r["whole_parent_inverse_exact"] for r in releases)
    assert {r["clean_input_sha256"] for r in releases} == {digest(CLEAN)}
    assert {r["canonical_sha256"] for r in releases} == {digest(latest["canonical_base"])}
    for previous, next_ in zip(releases, releases[1:]):
        assert all(previous[k] == next_["predecessor"][k] for k in ("candidate", "candidate_sha256", "registry_sha256", "manifest_sha256"))
        for key in ("candidate", "manifest", "patch", "own_registered_startup"):
            assert digest(previous[key]) == previous[f"{key}_sha256"]
    with inherited.mapped(REGISTRY) as data:
        profile = inherited.value(data, latest["profile"], 4)
        accepted = inherited.value(data, "accepted_layers", 2)
        assert profile["status"] == "experimental" and len(accepted) == 114
    with inherited.mapped(Path(latest["manifest"])) as data:
        read_field = lambda key: inherited.value(data, key, 2)
        assert read_field("candidate_sha256") == latest["candidate_sha256"]
        assert read_field("release_stack_sha256") == latest["registry_sha256"]
        assert read_field("profile") == latest["profile"]
        batches, release_checks = read_field("batches"), read_field("checks")
        assert len(batches) == 1117 and len(release_checks) == 452 and all(release_checks.values())
        keys = {p.replace("\\", "/") for p in batches}
        assert all(r["status"] == "accepted" and (r.get("baked_into_baseline") is True or r["batch"].replace("\\", "/") in keys)
                   for r in accepted)
    with inherited.mapped(inherited.base.LEDGER) as data:
        entry = inherited.value(data, "current_integrated_candidate", 1)
        assert entry["sha256"] == latest["candidate_sha256"] and entry["profile"] == latest["profile"]
        assert inherited.value(data, "records_editorially_completed", 1) == 27700
        assert inherited.value(data, "full_goal_complete", 1) is False
        _, lo, hi, _ = inherited.previous.scope["field"](data, inherited.base.CONTEXT, 1)
        rows = inherited.value(data, "integrated_record_keys", 2, lo, hi)
        identities = {(r["file_path"], r["id"]) for r in rows}
        assert len(identities) == len(rows) == 27700
    cleanup = read(CLEANUP)
    assert cleanup["candidate_sha256"] == latest["candidate_sha256"]
    for row in cleanup["removed_exact_duplicates"]:
        assert not Path(row["path"]).exists() and digest(row["retained"]) == row["sha256"]
    return identities


def exact_story(earlier, after, clean, stored, review, block, ids):
    a, b, source = (genoa.blocks(image, ARCHIVES[3]) for image in (earlier, after, clean))
    assert {i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y} == {block}
    assert sha256(a[block]).hexdigest() == stored["before_block_sha256"]
    assert sha256(b[block]).hexdigest() == stored["target_block_sha256"]
    commands = {ident: row for row in stored["commands"] for ident in row["record_ids"]}
    assert set(commands) == {row["id"] for row in review["records"]}
    assert {r["id"] for r in review["records"] if r["decision"] == "revision"} == ids
    for r in stored["commands"]:
        if not r["record_ids"]:
            continue  # Relative/layout command extents remain bound by the stored block proof.
        source_bytes, previous_bytes, installed_bytes = (bytes.fromhex(r[k]) for k in ("source", "current", "stored"))
        for raw, at, data in ((source[block], r["source_offset"], source_bytes),
                              (a[block], r["current_offset"], previous_bytes),
                              (b[block], r["stored_offset"], installed_bytes)):
            assert raw[at:at + len(data)] == data
        assert source_bytes[:6] == previous_bytes[:6] == installed_bytes[:6]
        assert (previous_bytes != installed_bytes) == bool(set(r["record_ids"]) & ids)
    assert stored["source25"]["total_exact_source_bound_relocated_leading25_count"] == 7
    return dict(file=ARCHIVES[3], block=block, exact_clean_parent_installed_speeches=len(commands), revised_ids=sorted(ids))


def exact_chain(images, clean, releases, reviews, proofs):
    deltas = []
    for earlier, after, receipt, review, stored in zip(images[:-1], images[1:], releases[1:], reviews, proofs, strict=True):
        validate_natural_dialogue_batch(review)
        assert review["candidate_sha256"] == receipt["candidate_sha256"] and review["source_credit_added"] == 0
        component, = receipt["changed_internal_files"]
        if component == ARM:
            offset = stored["rom_offset"]
            original, changed = (bytes.fromhex(stored[k]) for k in ("current_hex", "staged_hex"))
            a, b = (Path(r).read_bytes() for r in (receipt["predecessor"]["candidate"], receipt["candidate"]))
            assert len(original) == len(changed) == 4 and b[offset:offset + 4] == changed
            assert b[:offset] + original + b[offset + 4:] == a
            deltas.append(dict(file=ARM, rom_offset=offset, byte_extent=4, revised_label="Missionary"))
        else:
            genoa.inverse(earlier, after, receipt, component)
            revised = {r["id"] for r in review["records"] if r["decision"] == "revision"}
            if component == COMMON:
                a, b = (elegy.common_rows(image.read_file(COMMON), image.read_file(ARM)) for image in (earlier, after))
                changed = [row.message_id for prev, row in zip(a, b, strict=True)
                           if genoa.common_binding(prev) != genoa.common_binding(row)]
                assert changed == [843] and revised == {"COMMON_MESSAGE_843"}
                deltas.append(dict(file=COMMON, messages=changed))
            else:
                assert component == ARCHIVES[3]
                block = stored["changed_block"]
                expected = {3: {22, 26, 32}, 171: {29, 52, 83, 94}}[block]
                assert revised == {f"DK4_MES_B{block}_R{n:04d}" for n in expected}
                deltas.append(exact_story(earlier, after, clean, stored, review, block, revised))
        deltas[-1].update(candidate_sha256=receipt["candidate_sha256"], exact_complete_parent_inverse=True)
    return deltas


def wrap_queue(installed, reviewed):
    previous = read(credit.WRAPS)
    by_position = {(r["file_path"], r["block"], r["offset"], r["block_sha256"], r["stored_body_hex"]): r["reviewed"]
                   for r in previous["records"]}
    for evidence in reviewed:
        for row in evidence["records"]:
            ref = row.get("registered_reference", {})
            if row.get("file_path") not in ARCHIVES:
                continue
            exact = ref.get("exact_command_hex", ref.get("complete_command_hex"))
            if exact and ref.get("block_sha256"):
                data = bytes.fromhex(exact)
                body = data[6:data.index(0, 6)].hex()
                key = (row["file_path"], row["block"], ref["command_offset"] + 5, ref["block_sha256"], body)
                by_position[key] = dict(id=row["id"], finding=row["localization_note"], decision=row["decision"])
    scoped, remaining = [], []
    totals = {}
    for path in ARCHIVES:
        stats, flags = scanner.scan(path, installed.read_file(path))
        totals[path] = dict(stats) | dict(heuristic_hits=len(flags))
        for row in flags:
            key = (path, row["block"], row["offset"], row["block_sha256"], row["stored_body_hex"])
            finding = by_position.get(key)
            if finding:
                scoped.append(row | {"reviewed": finding})
            else:
                remaining.append(row)
    return dict(earlier=reference(credit.WRAPS), totals=totals, reviewed_flags=scoped, open_flags=remaining,
                scope="Byte-signature scan of ASCII progressive story bodies. Gameplay findings and other consumers use their own evidence.")


def archived_message_scope(installed):
    arm = installed.read_file(ARM)
    selector_proof, archive_proof = map(read, (archived_selectors.OUT, archived_operands.REPORT))
    assert selector_proof["candidate_sha256"] == digest(archived_selectors.current.ROM)
    selector_image = NdsImage.open(archived_selectors.current.ROM)
    assert all(selector_image.read_file(p) == installed.read_file(p) for p in (ARM, COMMON))
    references = selector_proof["earlier_matching_reference_scope"]["references"]
    assert len(references) == 42 and not selector_proof["earlier_matching_reference_scope"]["changed_dependencies"]
    assert all(not (set(r.get("possible_COMMON_ids", ())) & set(ARCHIVED)) for r in references)

    forwarded = read(forwarding.OUTPUT)
    price = read(forwarding.active.RELEASE)
    assert forwarded["candidate_sha256"] == price["candidate_sha256"] == digest(price["candidate"])
    price_arm = NdsImage.open(price["candidate"]).read_file(ARM)
    range_ledger = read(forwarding.earlier.OUTPUT)
    results = forwarding.static_results(price_arm, arm, range_ledger["reference_outcomes"])
    expected = {r["address"]: r["ids"] for r in forwarded["static_results"]}
    assert len(results) == len(expected) == 706
    assert all(r["status"] == "reused exact dependencies" and expected[r["address"]] == r["ids"] for r in results)
    assert all(not (set(r["ids"]) & set(ARCHIVED)) for r in results)
    reference_scope = read(forwarding.earlier.prior.OUTPUT)
    aligned = {tuple(row) for group in ("all_shared_reference_candidates", "current_only_reference_candidates")
               for row in reference_scope[group]}
    assert forwarding.earlier.prior.census(current.ROM) == aligned
    assert len(aligned) == forwarded["aligned_reference_candidates"] == 827

    shortfall_path = archived_operands.RELEASE
    shortfall_receipt = read(shortfall_path)
    assert archive_proof["candidate_sha256"] == shortfall_receipt["candidate_sha256"] == digest(shortfall_receipt["candidate"])
    older = NdsImage.open(shortfall_receipt["candidate"])
    assert all(sha256(arm[r["start"] - archived_operands.BASE:r["end"] - archived_operands.BASE]).hexdigest() == r["sha256"]
               for r in archive_proof["exact_code_spans"])
    changed = {}
    for path, prior in archive_proof["installed_story"].items():
        assert sha256(older.read_file(path)).hexdigest() == prior["archive_sha256"]
        before, after = (genoa.blocks(rom, path) for rom in (older, installed))
        delta = [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
        if delta:
            changed[path] = delta
            assert not set(delta) & {r["block"] for r in prior["hits"]}
            assert all(not archived_operands.matches(after[i]) for i in delta)
    assert changed == {ARCHIVES[1]: [170, 181], ARCHIVES[3]: [3, 171]}
    events = archive_proof["event_archives"]
    assert all(sha256(installed.read_file(path)).hexdigest() == row["archive_sha256"] for path, row in events.items())
    assert archive_proof["counts"]["installed_SC_hits"] == 43 and archive_proof["counts"]["exact_clean_and_installed_EV_hits"] == 23
    return dict(archived_COMMON_ids=ARCHIVED, retained_native_selector_references=len(references),
        exact_bounded_forwarding_arguments=len(results), aligned_forwarding_reference_count=827,
        exact_previously_classified_story_hits=43, exact_previously_classified_event_hits=23,
        changed_blocks_without_new_numeric_matches=changed,
        proof_sources=list(map(reference, (archived_selectors.OUT, archived_operands.REPORT, forwarding.OUTPUT))),
        computed_or_indirect_display_outside_these_scopes_open=True)


def main():
    receipts = [genoa.sealed(pkg, "verification/registered_release_verification.json") for pkg in PACKAGES]
    releases = list(map(read, receipts))
    latest = releases[-1]
    previous = read(genoa.OUT)
    assert previous["candidate_sha256"] == releases[0]["candidate_sha256"]
    ids = checks(releases)
    assert Counter(p for p, _ in ids) == dict(zip((*ARCHIVES, COMMON, HELP, ARM), (6887, 5356, 6720, 5129, 3392, 202, 14), strict=True))
    clean = NdsImage.open(CLEAN)
    images = [NdsImage.open(r["candidate"]) for r in releases]
    installed = images[-1]
    reviews = [read(genoa.sealed(pkg, "verification/registered_review.json")) for pkg in PACKAGES[1:]]
    proofs = [read(genoa.sealed(pkg, "verification/stored_proof.json")) for pkg in PACKAGES[1:]]
    deltas = exact_chain(images, clean, releases, reviews, proofs)
    source_story = {p: genoa.blocks(clean, p) for p in ARCHIVES}
    installed_story = {p: genoa.blocks(installed, p) for p in ARCHIVES}
    assert sum(map(len, source_story.values())) == 1307
    for i, path in enumerate(ARCHIVES):
        assert sha256(installed.read_file(path)).hexdigest() == latest[f"target_SC{i}_sha256"]
        assert len(installed_story[path]) == len(source_story[path])
        assert clean.read_file(f"/data/EV{i}.DK4") == installed.read_file(f"/data/EV{i}.DK4")
    priorities = genoa.acceptance.priority_bindings(source_story, installed_story)
    shared, help_proof = elegy.shared_and_help(clean, installed, images[0], latest)
    approved = read(SHARED)
    assert len(approved["records"]) == 276 and not approved["remaining_without_scoped_disposition"]
    assert {n for n in range(3668) if (COMMON, f"COMMON_MESSAGE_{n}") not in ids} == {r["message_ID"] for r in approved["records"]}
    current_common = elegy.common_rows(installed.read_file(COMMON), installed.read_file(ARM))
    clean_common = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    archived = [r for r in approved["records"] if r["message_ID"] in ARCHIVED]
    assert sorted(r["message_ID"] for r in archived) == list(ARCHIVED)
    assert all(r["other_direct_COMMON_display_unverified"] for r in archived)
    assert all(clean_common[n].text.count(b"%s") == current_common[n].text.count(b"%s") for n in ARCHIVED)
    arm = installed.read_file(ARM)
    credit.runtime_scope["verify_runtime"](arm, latest)
    regressions = dict(Julio=credit.julio_dependency(installed, arm), Deck=credit.deck_dependencies(installed, arm),
        Market_Goods_Info_and_right_bound="Original redirect payload, both pointers and eight repair spans verified.")
    names = FunctionType(credit.names.name_bindings.__code__, vars(credit.names) | {"current": current})(latest, clean.read_file(ARM))
    assert names["original_default_getter_cases"] == 414 and names["checked_clean_and_current_field_slots"] == 621
    wraps = wrap_queue(installed, [read(genoa.sealed(PACKAGES[0], "verification/registered_review.json")), *reviews])
    archived_paths = archived_message_scope(installed)
    voyage = read(VOYAGE)
    assert voyage["candidate_sha256"] == releases[-2]["candidate_sha256"] and voyage["ordinary_controller_gameplay"]
    assert len(voyage["shared"]) == 13 and len(voyage["story"]) == 8
    assert not (set(map(int, voyage["requests"])) & set(ARCHIVED))
    assert all(images[-2].read_file(p) == installed.read_file(p) for p in (ARM, COMMON))
    write(OUT, dict(candidate_sha256=latest["candidate_sha256"], release_chain=list(map(reference, receipts)),
        previous_acceptance=reference(genoa.OUT), registered_deltas=deltas, historical_credit_count=len(ids),
        previous_credited_story_positions=24092, native_story_event_blocks=1307, priority_decisions=priorities,
        shared_display=shared, approved_help=help_proof, default_name_review=names, user_reported_regressions=regressions,
        progressive_wrap_queue=wraps, voyage=reference(VOYAGE), drive=reference(DRIVE), cleanup=reference(CLEANUP),
        archived_message_scope=archived_paths, open_archived_message_callers=archived,
        remaining_artwork_assignments=approved["exact_archived_artwork_identities_open"],
        continued_review_required=True, full_editorial_goal_complete=False))
    print(f"Verified four current release deltas, 416 priority bindings, 414 default-name cases, and {len(ids):,} unique credits.")
    print(f"Current story scan: {len(wraps['reviewed_flags'])} reviewed and {len(wraps['open_flags'])} open heuristic hits.")


if __name__ == "__main__":
    main()
