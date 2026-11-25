"""Bind ordinary New Game display coverage to the pending opening labels."""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw

from scripts import checkpoint_opening_scene_labels_20261115 as prior
from scripts import observe_remaining_opening_shared_text_20261119 as replay

base, current = replay.base, replay.current
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/opening_scene_display_scope_20261119_v1.json")
SHEET = replay.ROOT / "opening_display_samples.png"
PREVIEW = {"lil": (2429, 2640, 2860), "hodram": (2660, 2890, 3120), "maria": (3600, 4000, 5000)}


def pixels(shot, upper=False):
    assert base.digest(shot["path"]) == shot["PNG_sha256"]
    with Image.open(shot["path"]) as image:
        rgb = image.convert("RGB")
    return rgb.crop((0, 0, 256, 192)) if upper else rgb


def checked_run(case, baseline, release, focus):
    folder = replay.ROOT / case
    report_path = folder / "capture/capture_report.json"
    trace_path = folder / "requests.json"
    contract_path = folder / "source_contract.json"
    events, frames, end, inputs, donor = replay.schedule(case)
    terminal_path = folder / "terminal.json"
    report, trace, contract = map(base.load, (report_path, trace_path, contract_path))
    assert report["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == end and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["scripted_input_schedule"] == events
    assert report["core_options"]["desmume_cpu_mode"] == "interpreter"
    assert report["exact_requested_capture_frames"] == frames and base.load(folder / "inputs.json") == events
    assert not any(value for key, value in report.items() if key.startswith("synthetic_")
                   and key != "synthetic_gallery_fixtures")
    gallery = report.get("synthetic_gallery_fixtures", [])
    assert len(gallery) == int(bool(donor))
    assert bool(report.get("battery_save_preloaded")) == bool(donor)
    if donor:
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
        assert gallery[0]["manifest_sha256"] == base.digest(donor["manifest"])
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    assert base.digest(contract_path) == trace["source_contract_sha256"]
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {r["PC"] for r in contract["targets"]} == set(replay.setup.REQUESTS)
    requests = trace["source_requests"]
    assert len(requests) == trace["callbacks"] == 2
    assert {r["PC"] for r in requests} == set(replay.setup.REQUESTS)
    assert {r["message_ID"] for r in requests} == {120} and not focus.intersection(r["message_ID"] for r in requests)
    assert requests[0]["frame"] == requests[1]["frame"]

    assert base.digest(baseline["path"]) == baseline["sha256"]
    earlier = base.load(baseline["path"])
    assert earlier["scripted_input_schedule"] == events
    before = {r["frame"]: r for r in earlier["frames_captured"]}
    after = {r["frame"]: r for r in report["frames_captured"]}
    exact_upper = []
    for n in frames:
        shot = pixels(after[n], upper=True)
        if n in before and shot.tobytes() == pixels(before[n], upper=True).tobytes():
            exact_upper.append(n)
    assert exact_upper == {"lil": frames, "hodram": [3120, 3200], "maria": [3400, 3600, 4000]}[case]
    if terminal_path.exists():
        terminal = base.load(terminal_path)
        assert terminal["ROM_sha256"] == release["candidate_sha256"] and not terminal["target_COMMON_calls"]
    findings = dict(actual_gameplay=True, capture_frames=frames, frame_count=end,
        exact_prior_upper_frames=exact_upper, requests=requests, pending_requests=0,
        system_unlock_only=bool(donor), no_savestate=True, hardware=False,
        evidence={str(p): base.digest(p) for p in (report_path, trace_path, contract_path, inputs)},
        historical_capture=baseline)
    if donor:
        findings["evidence"][donor["manifest"]] = base.digest(donor["manifest"])
    return findings, after


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.load(base.LEDGER)["current_integrated_candidate"]["sha256"] == release["candidate_sha256"]
    binding = base.load(replay.BINDING)
    assert binding["candidate_sha256"] == release["candidate_sha256"]
    rows = {r["message_ID"]: r for r in binding["records"]}
    assert len(rows) == 276
    older = base.load(prior.OUTPUT)
    old_route = replay.ROUTES.with_name("route_opening_movie_proof.json")
    old_assets = replay.ROUTES.with_name("preflight.json")
    maria_proof = replay.MARIA / "proof.json"
    old_movie, preflight, maria = map(base.load, (old_route, old_assets, maria_proof))
    assert old_movie["candidate_sha256"] == preflight["candidate_sha256"]
    assert old_movie["all5_English_captions_complete8559_ink_shadow_texels_and10_visible_boundary_controls"]
    assert maria["initial_Maria_M26_mapping_retracted_not_used_as_evidence"]
    rom = base.NdsImage.open(current.ROM)
    assets = older["alternate_visible_assets"] | preflight["movies"]
    for r in maria["Maria_actual_two_source_bound_court_backgrounds"]:
        assets[r["source"]] = r["source_sha256"]
    assert all(sha256(rom.read_file(p)).hexdigest() == digest for p, digest in assets.items())

    carried = older["ordinary_emulator_runs"]
    assert {k for k in carried} == {"title", "rafael"}
    for scope in carried.values():
        assert scope["control_only"] and scope["target_requests"] == 0
        assert all(base.digest(p) == v for p, v in scope["evidence"].items())
    cases = {}
    sheet = Image.new("RGB", (768, 1224), "#1f2830")
    text = ImageDraw.Draw(sheet)
    for y, case in enumerate(replay.RUNS):
        baseline = old_movie["reports"][case]["baseline"] if case != "maria" else next(
            r for r in maria["reports"] if r["tag"] == "baseline")
        cases[case], shots = checked_run(case, baseline, release, set(rows))
        for x, frame in enumerate(PREVIEW[case]):
            text.text((x * 256 + 6, y * 408 + 4), f"{case.title()} · frame {frame}", fill="white")
            sheet.paste(pixels(shots[frame]), (x * 256, y * 408 + 22))
    sheet.save(SHEET)

    records = []
    for prior_row in older["records"]:
        n = prior_row["message_ID"]
        current_row = rows[n]
        assert current_row["source_reference"] == prior_row["source_reference"]
        assert current_row["current_hex"] == prior_row["current_hex"]
        assert current_row["draft"]["english"] == prior_row["English_draft"]
        records.append(dict(message_ID=n, source_reference=current_row["source_reference"],
            current_reference=current_row["current_reference"], source_hex=current_row["source_hex"],
            current_hex=current_row["current_hex"], Japanese=prior_row["source_Japanese"],
            reviewed_English=prior_row["English_draft"], reason=prior_row["reason"],
            artwork_association=prior_row["artwork_association"], review=prior_row["review"],
            tested_title_and_opening_requests={k: 0 for k in (*carried, *cases)},
            separate_display_path_verified_for_tested_openings=True,
            other_consumers_open=True))
    assert {r["message_ID"] for r in records} == set(range(3570, 3607))
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"],
        existing_title_and_Rafael_evidence=dict(path=str(prior.OUTPUT), sha256=base.digest(prior.OUTPUT)),
        original_visible_asset_sha256=assets, current_replays=cases, records=records,
        historically_unbound_artwork_labels=older["unbound_label_ids"], pending_keys_in_focus=len(rows),
        changes_to_installed_text=False, new_editorial_credit=0, other_consumers_open=True, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in (replay.BINDING, prior.OUTPUT, old_route, old_assets, maria_proof, SHEET)}))
    print("Verified three current opening replays, six setup requests, zero pending requests, and 37 scoped label decisions.")


if __name__ == "__main__":
    main()

