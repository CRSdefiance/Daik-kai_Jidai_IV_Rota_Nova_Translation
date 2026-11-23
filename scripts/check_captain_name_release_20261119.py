"""Qualify the staged captain names against the registered startup and live Gallery."""

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run
from sys import executable

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.stage_captain_name_latin_20261119 import ARM, PROOF_NAME, ROM_NAME, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_rafael_custom_name_20261119 import ROM_HASH, digest, read

PARENT = Path("out/deck_view_guidance_registered_20261119_v1/Translation_DS_Deck_View_Guidance_20261119_candidate.nds")
PARENT_RELEASE = Path("releases/all_routes_editorial_20261119_deck_view_guidance_candidate/verification")
PARENT_STARTUP = Path("work/deck_view_guidance_20261119/staged_v2/own_startup/capture/capture_report.json")
GALLERY = Path("work/emulation_v193/gallery_all_v523/capture_report.json")
START_FRAMES = (1600, 2200, 3340, 4000, 16000, 31000)
GALLERY_FRAMES = (2400, 2800, 3200, 3400, 3800, 4100, 4400)


def replay(output, name, rom, events, frames, battery=None):
    folder = output / name
    folder.mkdir()
    inputs = folder / "inputs.json"
    write(inputs, events)
    args = [executable, "-m", "scripts.headless_desmume_v193", "--rom", str(rom), "--out", str(folder / "capture"),
            "--frames", str(frames[-1]), "--press-start", "-1", "--touchscreen", "--capture-every", "999999",
            "--capture-at", *map(str, frames), "--inputs-json", str(inputs), "--dump-native-state"]
    if battery:
        assert digest(Path(battery["source"]).read_bytes()) == battery["source_sha256"]
        args.extend(["--battery-save", battery["source"], "--capture-native-state-at", "3200", "3400"])
    run(args, check=True)


def capture(output):
    candidate = output / ROM_NAME
    assert digest(candidate.read_bytes()) == read(output / PROOF_NAME)["candidate_sha256"]
    assert digest(PARENT.read_bytes()) == ROM_HASH
    prior = read(PARENT_STARTUP)
    assert prior["ROM_sha256"] == ROM_HASH
    original = read(GALLERY)
    events = [*original["scripted_input_schedule"][:7],
              {"start": 3201, "duration": 8, "buttons": ["LEFT"]},
              *({"start": n, "duration": 8, "buttons": ["B"]} for n in (3401, 3801, 4101))]
    donor = original["battery_save_preloaded"]
    jobs = [("release_startup", candidate, prior["scripted_input_schedule"], START_FRAMES,
             prior["battery_save_preloaded"]),
            ("gallery_parent", PARENT, events, GALLERY_FRAMES, donor),
            ("gallery_candidate", candidate, events, GALLERY_FRAMES, donor)]
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = [pool.submit(replay, output, *args) for args in jobs]
        for result in results:
            result.result()


def screens(report, frames):
    pictures = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    assert all(digest(Path(pictures[n]["path"]).read_bytes()) == pictures[n]["PNG_sha256"] for n in frames)
    return [pictures[n] for n in frames]


def equal_screens(before, after, frames):
    old, new = [screens(report, frames) for report in (before, after)]
    assert [row["framebuffer_sha256"] for row in old] == [row["framebuffer_sha256"] for row in new]
    return new


def tcm(snapshot):
    export = Path(snapshot["path"])
    assert digest(export.read_bytes()) == snapshot["sha256"]
    region = read(export)["regions"]["ITCM"]
    data = Path(region["path"]).read_bytes()
    assert len(data) == region["bytes"] == 0x8000 and digest(data) == region["sha256"]
    return data


def compare(output):
    plan = read(output / PROOF_NAME)
    rom = output / ROM_NAME
    assert digest(rom.read_bytes()) == plan["candidate_sha256"]
    image = NdsImage.open(rom)
    arm = image.read_file(ARM)
    sections = MainCodeFile(arm, BASE).sections
    start, end = plan["autoload_span"]
    assert sections[-1].ramAddress == start and len(sections[-1].data) == end - start
    overlay, = loadOverlayTable(image.rom.arm9OverlayTable, lambda _, ident: image.rom.files[ident]).values()
    assert overlay.ramAddress + overlay.ramSize + overlay.bssSize == start
    overlay_rom = bytes(overlay.data)

    startup_path = output / "release_startup/capture/capture_report.json"
    current, raw = checked_report(startup_path, plan["candidate_sha256"], START_FRAMES[-1])
    previous, _ = checked_report(PARENT_STARTUP, ROM_HASH, START_FRAMES[-1])
    old_options, new_options = [dict(report["core_options"]) for report in (previous, current)]
    pointer_modes = [options.pop("desmume_pointer_type") for options in (old_options, new_options)]
    assert old_options == new_options
    assert current["scripted_input_schedule"] == previous["scripted_input_schedule"]
    assert not any("touch" in event for event in current["scripted_input_schedule"])
    holds = equal_screens(previous, current, START_FRAMES)
    payload = bytes(sections[3].data[:-48])
    assert len(payload) == cache_plan(arm)["payload_bytes"] == 123264
    assert raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    assert raw[DIRECTORY_OFFSET:TABLE_END] == arm[DIRECTORY_OFFSET:TABLE_END]
    original = read(PARENT_RELEASE / "own_startup_verification.json")
    rows = read(Path("work/ship_command_label_release_v1/own_registered_name_getters_v1.json"))["own_name_consumers"]["rows"]
    names = []
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == 3
    for row in rows:
        value = bytes.fromhex(row["text_hex"])
        ptr = get(row["getter"] - BASE, row["actor_object"])
        assert bytes(cpu.mem_read(ptr, len(value) + 1)) == value + b"\0"
        names.append({key: row[key] for key in ("actor_ID", "consumer", "getter", "text", "text_hex")})
    assert names == original["original_protected_name_getters"] and len(names) == 24

    gallery_paths = [output / f"gallery_{side}/capture/capture_report.json" for side in ("parent", "candidate")]
    pair = [checked_report(path, sha, GALLERY_FRAMES[-1])[0]
            for path, sha in zip(gallery_paths, (ROM_HASH, plan["candidate_sha256"]), strict=True)]
    assert pair[0]["scripted_input_schedule"] == pair[1]["scripted_input_schedule"]
    gallery = equal_screens(*pair, GALLERY_FRAMES)
    for case in pair:
        donor = case["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"]
        assert digest(Path(donor["source"]).read_bytes()) == digest(Path(donor["destination"]).read_bytes()) == donor["source_sha256"]
    for case in pair:
        native = case["read_only_capture_native_states"]
        assert [row["frame"] for row in native] == [3200, 3400]
        for row in native:
            data = tcm(row)
            at = overlay.ramAddress - 0x01FF8000
            assert data[at:at + len(overlay_rom)] == overlay_rom
            if case is pair[1]:
                assert data[start - 0x01FF8000:end - 0x01FF8000] == sections[-1].data

    proof = {"candidate_sha256": plan["candidate_sha256"], "cold_boot": True, "savestate": False,
             "exact_matching_frames": holds, "original_protected_name_getters": names,
             "complete_deployed_payload_exact": True, "read_only_snapshot": current["read_only_RAM_snapshot"],
             "non_pointer_core_options_equal": True, "unused_pointer_modes": pointer_modes,
             "gallery_exact_matching_frames": gallery, "gallery_overlay_and_adjacent_autoload_exact_in_live_itcm": True,
             "hardware": False, "evidence": {str(p): digest(p.read_bytes()) for p in [startup_path, PARENT_STARTUP,
                                                                                    *gallery_paths]}}
    write(output / "own_startup_verification.json", proof)
    print("Six startup holds, 24 protected getters and seven matching Gallery frames verified.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("capture", "compare"))
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    (capture if args.action == "capture" else compare)(args.output)
