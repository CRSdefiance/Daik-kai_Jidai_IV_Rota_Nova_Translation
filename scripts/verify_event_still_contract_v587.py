"""Bind the actual B7158 preallocated-canvas loader and matched native captures."""

import json
import shutil
import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_raw_direct_color_v587 import FILE, PARENT, ROOT, contents
from scripts.probe_button_prompt_native import BASE, call, machine

CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V587 Raw format controls")
HEADER, NAME, SCRATCH = 0x02276D74, 0x02134BC8, 0x02233040
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def loader_case(fixture, snapshot):
    rom = NdsImage.open(fixture["research_ROM"])
    raw, arm = snapshot.read_bytes(), rom.read_file("/__arm9__.bin")
    original = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0xB7158:0xB7260] == original[0xB7158:0xB7260]
    u = machine(arm)
    u.mem_write(BASE, raw)
    header = struct.unpack_from("<5I", raw, HEADER - BASE)
    assert header[0] & 255 == 8 and header[1:3] == (128, 192)
    palette, pixels = HEADER + header[3], HEADER + header[4]
    assert (palette, pixels) == (0x02276D88, 0x022BD850)
    data = rom.read_file(FILE)
    source = struct.unpack_from("<5I", data)
    accepted = (source[0] & 255, *source[1:3]) == (8, 128, 192)
    handles, events = {}, []

    def bridge(uc, address, size, user):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 96)).split(b"\0")[0].decode("ascii")
            assert name == FILE and obj not in handles
            handles[obj] = 0
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(data)))
            events.append({"operation": "open", "path": name})
            result = 1
        elif address == SEEK:
            assert uc.reg_read(UC_ARM_REG_R2) == 0
            handles[obj] = uc.reg_read(UC_ARM_REG_R1)
            result = 1
        elif address == READ:
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert target == SCRATCH and handles[obj] == 0 and count == len(data)
            uc.mem_write(target, data)
            handles[obj] += count
            events.append({"operation": "read", "target": target, "bytes": count})
            result = count
        else:
            handles.pop(obj)
            events.append({"operation": "close"})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    try:
        executed = call(u, 0xB7158, (HEADER, NAME), instruction_limit=500000)
    finally:
        u.hook_del(hook)
    assert not handles and bytes(u.mem_read(SCRATCH, len(data))) == data
    after = bytes(u.mem_read(BASE, len(raw)))
    allowed = set(range(SCRATCH - BASE, SCRATCH - BASE + len(data)))
    if accepted:
        assert 0x020E2910 in executed
        expected_header = (header[0] & ~0x100) | (source[0] & 0x100)
        assert int.from_bytes(u.mem_read(HEADER, 4), "little") == expected_header
        assert bytes(u.mem_read(palette, 512)) == data[source[3]:source[3] + 512]
        assert bytes(u.mem_read(pixels, 49152)) == data[source[4]:source[4] + 49152]
        allowed.update(range(HEADER - BASE, HEADER - BASE + 4))
        allowed.update(range(palette - BASE, palette - BASE + 512))
        allowed.update(range(pixels - BASE, pixels - BASE + 49152))
    else:
        assert 0x020E2910 not in executed and 0x020B71E8 not in executed
        assert bytes(u.mem_read(HEADER, 20)) == raw[HEADER - BASE:HEADER - BASE + 20]
        assert bytes(u.mem_read(palette, 512)) == raw[palette - BASE:palette - BASE + 512]
        assert bytes(u.mem_read(pixels, 49152)) == raw[pixels - BASE:pixels - BASE + 49152]
    assert all(a == b for i, (a, b) in enumerate(zip(raw, after, strict=True)) if i not in allowed)
    reason = "accepted" if accepted else "format_mismatch" if source[0] & 255 != 8 else "width_or_height_mismatch"
    return {"mode": fixture["mode"], "source_header": list(source), "destination_header": list(header),
            "actual_native_header": HEADER, "actual_palette": palette, "actual_indices": pixels,
            "SDK_file_events": events, "file_fully_read_to_scratch_before_validation": True,
            "disposition": reason, "all_destination_bytes_unchanged_when_rejected": not accepted,
            "positive_complete_palette_and_indices_exact": accepted,
            "all_other_main_RAM_exact_and_call_ABI_pass": True,
            "code_sha256": sha(arm[0xB7158:0xB7260])}


def main():
    parent = NdsImage.open(PARENT)
    baseline = contents(parent)
    fixtures = read(ROOT / "fixture_manifest.json")
    inputs = read(ROOT / "opening_inputs.json")
    reports, shots, snapshots, loaders = {}, {}, {}, []
    for f in fixtures:
        rom = NdsImage.open(f["research_ROM"])
        assert sha(rom.source.read_bytes()) == f["research_ROM_sha256"]
        current = contents(rom)
        expected = ["/__arm9__.bin"] if f["mode"] == "indexed8_positive" else sorted(["/__arm9__.bin", FILE])
        assert sorted(p for p in baseline if baseline[p] != current[p]) == expected
        assert current["/GRP/SLACKIMG.DK4"] == baseline["/GRP/SLACKIMG.DK4"]
        folder = CAPTURE / ("raw_direct_color_v587_" + f["mode"])
        report_path = folder / "capture_report.json"
        r = read(report_path)
        assert r["ROM_sha256"] == f["research_ROM_sha256"] and r["cold_boot"] and not r["savestate_loaded"]
        assert not r.get("battery_save_preloaded") and not r["callback_errors"] and r["frames"] == 4200
        assert r["scripted_input_schedule"] == inputs
        reports[f["mode"]] = {"path": str(report_path), "sha256": sha(report_path.read_bytes())}
        shots[f["mode"]] = {s["frame"]: s for s in r["frames_captured"]}
        snapshots[f["mode"]] = {s["frame"]: s for s in r["read_only_capture_RAM_snapshots"]}
        for s in r["frames_captured"]:
            assert sha(Path(s["path"]).read_bytes()) == s["PNG_sha256"]
        for s in r["read_only_capture_RAM_snapshots"]:
            assert sha(Path(s["path"]).read_bytes()) == s["sha256"]
        # Use one shared rejected baseline to prove what each full native call
        # actually does, instead of relying on a potentially already copied logo.
        base_snapshot = CAPTURE / "raw_direct_color_v587_source_highbits/frame_004000_arm9_ram.bin"
        loaders.append(loader_case(f, base_snapshot))
    assert len(loaders) == 8 and sum(r["disposition"] == "accepted" for r in loaders) == 1
    source = PxlImage.from_bytes(baseline[FILE])
    palette_words = struct.unpack_from("<256H", source.source, 20)
    assert [i for i, v in enumerate(palette_words) if not v & 0x8000] == [255]
    composite = []
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    archives = []
    for frame in (3600, 4000, 4200):
        background = Image.open(shots["source_highbits"][frame]["path"]).convert("RGB")
        for mode in shots:
            image = Image.open(shots[mode][frame]["path"]).convert("RGB")
            if mode != "indexed8_positive":
                assert image.tobytes() == background.tobytes(), (mode, frame)
            else:
                assert image.crop((0, 192, 256, 384)).tobytes() == background.crop((0, 192, 256, 384)).tobytes()
                for index, value in enumerate(source.indices):
                    x, y = index % 256, index // 256
                    word = palette_words[value]
                    actual = tuple(c >> 3 for c in image.getpixel((x, y)))
                    expected = (word & 31, word >> 5 & 31, word >> 10 & 31) if word & 0x8000 else tuple(c >> 3 for c in background.getpixel((x, y)))
                    assert actual == expected, (frame, x, y)
                snapshot = Path(snapshots[mode][frame]["path"]).read_bytes()
                words = struct.unpack_from("<5I", snapshot, HEADER - BASE)
                assert snapshot[HEADER - BASE + words[3]:HEADER - BASE + words[3] + 512] == source.source[20:532]
                assert snapshot[HEADER - BASE + words[4]:HEADER - BASE + words[4] + 49152] == bytes(source.indices)
            destination = ARCHIVE / f"{mode}_{frame}.png"
            shutil.copyfile(shots[mode][frame]["path"], destination)
            assert sha(destination.read_bytes()) == shots[mode][frame]["PNG_sha256"]
            archives.append({"path": str(destination), "sha256": sha(destination.read_bytes()),
                             "research_control_not_ordinary_comic_context": True})
        composite.append({"frame": frame, "all_seven_rejected_control_fullscreens_exact": True,
                          "positive_logo_whole_upper_composite_and_lower_exact": True})
    assert sha(PARENT.read_bytes()) == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    result = {"candidate_sha256": sha(PARENT.read_bytes()), "reports": reports,
              "actual_original_event_still_loader": 0x020B7158,
              "source_filename_formatter_caller": 0x02028B74,
              "actual_captured_canvas_header": HEADER, "native_loader_cases": loaders,
              "frame_compositing_cases": composite,
              "test_screen_requires_matching8_128word_192row_header": True,
              "all_six_direct16_and_one_wrong_geometry_indexed_controls_rejected": True,
              "read_to_scratch_is_not_cache_residency_or_display": True,
              "opacity_as_failure_cause_not_established": True,
              "isolated_PXL_resource_cache_probe_is_a_separate_API_from_live_canvas_loader": True,
              "ordinary_raw_comic_consumer_palette_or_GPU_readability_not_proven": True,
              "no_original_high_bit_or_artwork_fix_inferred": True,
              "archive": str(ARCHIVE), "screenshots": archives,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "production_ROM_and_patch_changed": False, "full_goal_complete": False}
    (ROOT / "event_still_contract_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("V587: actual fixed-canvas loader bound;8 complete calls/24 native controls;7 header rejections and complete positive logo composite pass. No raw-opacity defect inferred.")


if __name__ == "__main__":
    main()
