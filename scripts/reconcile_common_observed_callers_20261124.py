"""Reconcile recorded COMMON fetches with the current finite caller census."""

from collections import Counter, defaultdict
from pathlib import Path
from struct import unpack

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.checkpoint_pending_shared_native_20261115 import branch_hits, components
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_genoa_copenhagen_town_20261123 import find_line
from scripts.verify_plaque_release_v247 import find_mask


ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
WORK = Path(".codex-release-work")
CENSUS = ROOT / "shared_reference_coverage_20261124.json"
BOUNDS = ROOT / "archived_message_argument_ranges_20261124.json"
ACCEPTANCE = ROOT / "editorial_acceptance_after_tunis_20261124.json"
OUT = ROOT / "archived_common_observed_callers_20261124.json"
RELEASES = Path("releases")
PREVIOUS = RELEASES / "all_routes_editorial_20261124_tunis_shop_advice_candidate/release_manifest.json"
RELEASE = RELEASES / "all_routes_editorial_20261124_maria_captured_ship_candidate/release_manifest.json"
LATEST_RUN = WORK / "shared_display_20261123/maria_system_quit_20261124/trace/requests.json"
CLEANUP = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_maria_captured_ship/common_request_audit_cache_cleanup.json")
GETTER, COPIER = 0x0205528C, 0x020534F4
ARCHIVED = {284, 318, 750, 751, 752}
REQUIRED = {"frame", "PC", "caller_LR", "message_ID"}


def caller_domains():
    census, bounds, proof = map(read, (CENSUS, BOUNDS, ACCEPTANCE))
    assert bounds["inherited_dispositions"] == reference(CENSUS)
    assert set(bounds["archived_ids"]) == set(census["separate_open_keys"]) == ARCHIVED
    rows = {(r["call_site"], r["entry"]): r.copy() for r in census["references"]}
    assert len(rows) == bounds["fully_bounded_census_sites"] == 827
    for bound in bounds["completed_bindings"]:
        row = rows[bound["call_site"], bound["target"]]
        assert row["possible_COMMON_ids"] is None
        row["possible_COMMON_ids"] = bound["ids"]
    assert all(ids is not None and ARCHIVED.isdisjoint(ids) for ids in
               (row["possible_COMMON_ids"] for row in rows.values()))
    active, before = map(read, (RELEASE, PREVIOUS))
    assert digest(REGISTRY) == active["registry_sha256"] and digest(active["candidate"]) == active["candidate_sha256"]
    assert proof["candidate_sha256"] == before["candidate_sha256"]
    image = NdsImage.open(active["candidate"])
    arm = image.read_file("/__arm9__.bin")
    assert sha256(arm).hexdigest() == active["target_ARM9_sha256"] == before["target_ARM9_sha256"]
    tail = arm[GETTER - 0x02000000:GETTER - 0x02000000 + 24]
    assert tail.hex() == "08c09fe50010a0e104009fe51cff2fe1f4340502dce62802"
    assert unpack("<I", tail[16:20])[0] == COPIER
    return active, image, rows, tail.hex()


def capture_for(trace):
    for folder in trace.parents:
        if folder == WORK:
            break
        choices = [path for path in (folder / "capture_report.json", folder / "capture/capture_report.json") if path.is_file()]
        if choices:
            capture, = choices
            return capture
    raise ValueError(f"No capture report for {trace}")


def observe(rows, active_sha):
    observations, trace_rows, retired = defaultdict(Counter), [], []
    for path in sorted(WORK.rglob("requests.json")):
        run = read(path)
        if not isinstance(run, dict) or not run.get("source_requests"):
            continue
        if not run.get("all_host_slots_restored_and_core_file_exact") or run.get("errors") or run.get("mismatches"):
            continue
        requests = run["source_requests"]
        if any(not REQUIRED <= set(row) for row in requests):
            retired.append(reference(path))
            continue

        capture = capture_for(path)
        report = read(capture)
        assert report["cold_boot"] and not report["callback_errors"]
        assert not any(v for key, v in report.items() if key.startswith("synthetic_"))
        contract = path.with_name("source_contract.json")
        assert contract.exists() and digest(contract) == run["source_contract_sha256"]
        limited = Counter()
        for opened, copied in zip(requests[::2], requests[1::2], strict=True):
            assert opened["PC"] == GETTER and copied == opened | {"PC": COPIER}
            lr, key = opened["caller_LR"], opened["message_ID"]
            site = (lr & ~1) - 4
            assert 0 <= opened["frame"] <= report["frames"]
            row = rows[site, GETTER]
            assert row["instruction"] == ("thumb_blx_immediate" if lr & 1 else "arm_bl")
            assert key in row["possible_COMMON_ids"] and key not in ARCHIVED
            observations[site][key] += 1
            limited[site] += 1
        sha = report["ROM_sha256"]
        trace_rows.append(dict(trace=reference(path), capture=reference(capture), instrument_contract=reference(contract),
            candidate_sha256=sha, is_current_registered_ROM=sha == active_sha, paired_requests=len(requests) // 2,
            original_call_counts=dict(sorted(limited.items())),
            runtime_overrides_declared_in_capture=False))
    current, = [row for row in trace_rows if row["trace"]["path"] == LATEST_RUN.as_posix()]
    assert current["is_current_registered_ROM"] and current["paired_requests"] == 2
    assert current["original_call_counts"] == {0x0205467C: 2}
    return trace_rows, observations, retired


def review_quit(active, image):
    report_path = capture_for(LATEST_RUN)
    report, trace = map(read, (report_path, LATEST_RUN))
    assert report["frames"] == 8200 and report["ROM_sha256"] == active["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert [row["message_ID"] for row in trace["source_requests"]] == [319] * 4
    assert {row["caller_LR"] for row in trace["source_requests"]} == {0x02054680}
    schedule = {row["start"]: row["buttons"] for row in report["scripted_input_schedule"]}
    assert schedule[6001] == ["B"] and schedule[7601] == ["A"]

    arm = image.read_file("/__arm9__.bin")
    archive = image.read_file("/COMMON/MESFILE.DK4")
    assert sha256(archive).hexdigest() == active["target_COMMON_sha256"]
    assert digest(CLEAN) == active["clean_input_sha256"]
    clean = NdsImage.open(CLEAN)
    source = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"), clean.read_file("/__arm9__.bin"))[319]
    del clean
    current = owned_entries(archive, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())[319]
    text = current.text.decode("ascii").strip()
    assert text == "Quit the game?"
    font = GameAsciiFont.from_arm9(arm)
    frames = shots(report, "_navigation.png")
    panels = []
    for frame in (6000, 7600):
        screen = picture(frames[frame])
        ink = font_mask(screen, font, text, 16, 297, (16, 296, 245, 330), (0, 8, 0))
        options = [find_mask(font, name, screen, box) for name, box in
                   (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
        panels.append(dict(frame=frame, visible_body_pixels=ink, labels=options, capture=frames[frame]))
    reopened, ended = picture(frames[6400]), picture(frames[8200])
    returned_menu = find_line(font, "Quit Game", reopened, range(95, 114), range(285, 315), (8, 8, 8))
    title_menu = find_line(font, "New Game", ended, range(95, 114), range(246, 269), (8, 8, 8))
    return dict(source=dict(Japanese=source.text.decode("cp932"), block=source.block,
                            block_offset=source.block_offset, exact_hex=source.text.hex()),
        installed=dict(english=text, block=current.block, block_offset=current.block_offset, exact_hex=current.text.hex()),
        message_ID=319, decision="retention", reason="The direct question names the action and leaves the choice to the player.",
        review=dict.fromkeys(GATES, True), actual_prompts=panels, save_source=reference(donor["source"]),
        capture=reference(report_path), no=dict(menu=returned_menu, capture=frames[6400]),
        yes=dict(menu=title_menu, capture=frames[8200]), exact_requests=trace["source_requests"])


def main():
    active, image, rows, getter_code = caller_domains()
    captured, counts, retired = observe(rows, active["candidate_sha256"])
    current = {address: (which, mode) for which, start, data in components(image.rom)
               for address, target, mode in branch_hits(data, start, {GETTER}) if address in counts}
    assert set(current) == set(counts)
    sites = []
    for site, keys in sorted(counts.items()):
        row = rows[site, GETTER]
        assert current[site] == (row["component"], row["instruction"])
        sites.append(dict(call_site=site, component=row["component"], instruction=row["instruction"],
                          inherited_argument_domain_size=len(row["possible_COMMON_ids"]),
                          observed_ids=dict(sorted(keys.items()))))
    num_pairs = sum(row["paired_requests"] for row in captured)
    assert num_pairs == sum(sum(keys.values()) for keys in counts.values())
    quit_record = review_quit(active, image)
    write(OUT, dict(candidate_sha256=active["candidate_sha256"], release=reference(RELEASE),
        earlier_reference_census=reference(CENSUS), finite_bounds_supplement=reference(BOUNDS),
        current_ARM9_matches_Tunis_audit=reference(ACCEPTANCE), preparer=reference(Path(__file__)),
        getter_tail=dict(address=GETTER, forwards_original_LR_to_copier=True, copier=COPIER, exact_hex=getter_code),
        matched_traces=len(captured), unique_capture_reports=len({row["capture"]["sha256"] for row in captured}),
        known_rom_hashes=len({row["candidate_sha256"] for row in captured}), matched_getter_copy_pairs=num_pairs,
        observed_call_sites=sites, trace_evidence=captured, older_traces_without_PC=retired,
        archived_ids=sorted(ARCHIVED), archived_requests_observed=[], new_gameplay_runs=1, ROM_changed=False,
        current_quit_review=quit_record,
        cache_cleanup=reference(CLEANUP),
        scope="Previously recorded emulator replays with explicit PC, return address and message ID. Includes older and staged ROMs and inherited saves."))
    print(f"Verified {num_pairs} getter and copier pairs from {len(captured)} traces across {len(counts)} original call sites.")


if __name__ == "__main__":
    main()
