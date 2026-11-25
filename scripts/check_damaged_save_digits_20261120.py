"""Check the full checksum warning, regular digits and original menu transitions."""

from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import checkpoint_damaged_save_20261115 as prior
from scripts import replay_damaged_save_digits_20261120 as replay
from scripts import stage_damaged_save_digits_20261120 as stage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.plan_literal_static_layout_v1 import render
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_forces_relationships_20261115 import font_points


base, ROOT = stage.base, stage.ROOT
PROOF, NATIVE_SHEET, GAMEPLAY_SHEET = (ROOT / n for n in ("verification.json", "native_digits.png", "continue_comparison.png"))
HOLD = (3700, 3800)
RASTER_SAMPLES = (*range(1, 11), 99, 100, 256)


def execute_preparation(arm):
    machine = machine_for(arm)
    machine.mem_map(0x01FF8000, 0x8000)
    for section in stage.runtime.MainCodeFile(arm, BASE).sections:
        if section.ramAddress in (0x01FF8000, stage.runtime.ITCM):
            machine.mem_write(section.ramAddress, bytes(section.data))
    frame = STACK - 36 - 0x74
    pool, = unpack_from("<I", arm, 0xABFC0)
    suffix = arm[stage.OFFSET:stage.OFFSET + stage.CAPACITY]
    cases = []
    # The game reads an unsigned byte. Exercise each value at the preparation
    # boundary, without treating them all as valid retail save slots.
    for slot in range(256):
        machine.mem_write(STACK - 0x200, b"\xA5" * 0x200)
        machine.mem_write(pool + 8, pack("<I", 31) + b"\xA5" * (32 * 128))
        machine.reg_write(UC_ARM_REG_SP, STACK)
        machine.reg_write(UC_ARM_REG_R0, slot)
        machine.emu_start(BASE + 0xEE67C, BASE + 0xEE6BC, count=1000)
        assert machine.reg_read(UC_ARM_REG_PC) == BASE + 0xEE6BC
        assert machine.reg_read(UC_ARM_REG_SP) == frame
        assert bytes(machine.mem_read(frame + 0x3C, stage.CAPACITY)) == suffix
        machine.emu_start(BASE + 0xEE75C, BASE + 0xEE780, count=10000)
        text = str(slot + 1) + stage.formatted_suffix()
        expected = text.encode("ascii") + b"\0"
        assert machine.reg_read(UC_ARM_REG_PC) == BASE + 0xEE780
        assert machine.reg_read(UC_ARM_REG_SP) == machine.reg_read(UC_ARM_REG_R0) == frame
        assert bytes(machine.mem_read(frame, 0x3C)) == expected.ljust(0x3C, b"\xA5")
        assert bytes(machine.mem_read(frame + 0x3C, stage.CAPACITY)) == suffix
        cases.append(dict(incoming_slot_byte=slot, display_number=slot + 1, complete_text=text,
            bytes_including_nul=len(expected), destination_capacity=0x3C, original_buffer_guards=True))
    return cases


def offline(arm, image):
    cases = execute_preparation(arm)
    raster, _, calibration = font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    sheet = Image.new("RGB", (936, 7 * 85), "#273034")
    captions = ImageDraw.Draw(sheet)
    renders = []
    for index, number in enumerate(RASTER_SAMPLES):
        text = cases[number - 1]["complete_text"]
        assert text == str(number) + stage.formatted_suffix()
        assert cases[number - 1]["bytes_including_nul"] <= 0x3C
        pixels, rows, origins, visible = render(raster, font, arm, text.encode("ascii"))
        assert rows == [line.strip() for line in text.splitlines()]
        assert origins == [6, 6] and {e["y"] for e in visible} == {0, 16}
        renders.append(dict(display_number=number, rows=rows, one_page=True,
            full_pixels_sha256=stage.batch.digest(pixels), complete_glyphs_bounds_and_words=True))
        panel = Image.frombytes("L", (228, 48), bytes(22 if ink else 248 for ink in pixels))
        x, y = 468 * (index % 2), 85 * (index // 2)
        captions.text((x + 8, y + 4), f"Slot {number}", fill="white")
        sheet.paste(panel.crop((0, 0, 228, 32)).resize((456, 64), Image.Resampling.NEAREST), (x + 6, y + 18))
    sheet.save(NATIVE_SHEET)
    return cases, renders, calibration


def gameplay(digests, before_arm, target_arm, kanji):
    paths = [ROOT / side / "capture/capture_report.json" for side in ("parent", "revised")]
    report = [base.load(path) for path in paths]
    fixture_path = replay.HISTORY / "checksum_fixture.json"
    history_path = replay.HISTORY / "corrupt_slot/capture/capture_report.json"
    fixture, history = map(base.load, (fixture_path, history_path))
    for index, r in enumerate(report):
        assert r["ROM_sha256"] == digests[index] and r["frames"] == history["frames"]
        assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
        assert not any(v for k, v in r.items() if k.startswith("synthetic_"))
        assert r["scripted_input_schedule"] == history["scripted_input_schedule"]
        donor = r["battery_save_preloaded"]
        assert donor["source_sha256"] == fixture["copy_sha256"] == base.digest(donor["source"])
        assert donor["copied_byte_exact_before_cold_boot"]
    assert report[0]["core_DLL_sha256"] == report[1]["core_DLL_sha256"]
    assert report[0]["core_options"] == report[1]["core_options"]
    previous, revised = map(shots, report)
    font = GameAsciiFont.from_arm9(target_arm)
    first, second = ("1" + stage.formatted_suffix()).splitlines()
    wanted_before = prior.complete_mask(before_arm, kanji, "１" + stage.formatted_suffix())
    wanted_after = font_points(font, first, 22, 297) | font_points(font, second.lstrip(), 22, 313)
    evidence = {str(p): base.digest(p) for p in (*paths, fixture_path, history_path)}
    screen = []
    for frame in history["exact_requested_capture_frames"]:
        before, after = [captured(row[frame]) for row in (previous, revised)]
        evidence.update({row[frame]["path"]: row[frame]["PNG_sha256"] for row in (previous, revised)})
        diff = ImageChops.difference(before, after).getbbox()
        if frame not in HOLD:
            assert diff is None, (frame, diff)
            continue
        assert diff and 10 <= diff[0] < diff[2] < 246 and 294 <= diff[1] < diff[3] < 355
        for image, expected in ((before, wanted_before), (after, wanted_after)):
            actual = {(x, y) for x in range(10, 246) for y in range(294, 355)
                      if image.getpixel((x, y)) == prior.INK}
            assert actual == expected, (frame, len(actual), len(expected))
        screen.append(dict(frame=frame, full_previous_ink=len(wanted_before), full_revised_ink=len(wanted_after)))

    assert len(screen) == 2
    sheet = Image.new("RGB", (1032, 216), "#273034")
    labels = ImageDraw.Draw(sheet)
    for index, frames in enumerate((previous, revised)):
        x = index * 516 + 2
        labels.text((x + 4, 2), ("Previous", "Revised")[index], fill="white")
        panel = captured(frames[HOLD[0]]).crop((0, 286, 256, 384))
        sheet.paste(panel.resize((512, 196), Image.Resampling.NEAREST), (x, 16))
    sheet.save(GAMEPLAY_SHEET)
    return screen, evidence


def main():
    assert not any(path.exists() for path in (PROOF, NATIVE_SHEET, GAMEPLAY_SHEET))
    staged = base.load(stage.PROOF)
    before, target = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    before_arm, arm = [image.read_file(stage.ARM) for image in (before, target)]
    kanji = target.read_file("/GRP/KANJI.FNT")
    assert kanji == before.read_file("/GRP/KANJI.FNT")
    assert stage.batch.digest(arm) == staged["target_ARM9_sha256"]
    cases, raster, calibration = offline(arm, target)
    game, evidence = gameplay([staged["parent_sha256"], staged["candidate_sha256"]], before_arm, arm, kanji)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], parent_sha256=staged["parent_sha256"],
        preparations=cases, modal_raster_cases=raster, emulator_holds=game,
        raster_calibration=calibration, offline_wrapper_execution=False,
        original_return_frames=[4200, 4400, 4700, 5100], one_checksum_bit_changed_in_copied_save=True,
        earlier_common_117_trace_reused=str(stage.PRIOR), fresh_live_lookup_trace=False,
        hardware=False, sheets={str(p): base.digest(p) for p in (NATIVE_SHEET, GAMEPLAY_SHEET)}, evidence=evidence))
    print(f"{len(cases)} native preparations, {len(raster)} full raster cases and {len(game)} paired emulator holds passed.")


if __name__ == "__main__":
    main()
