"""Check the exact dialogue, counts, choice controls and return in two normal Tavern visits."""

from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_azores_return_20261123 as azores
from scripts import replay_recruitment_capacity_20261123 as playback
from scripts import stage_recruitment_capacity_wraps_20261123 as stage
from scripts.check_tavern_round_digits_20261120 import capture_ram, wallet
from scripts.reconcile_editorial_acceptance_20261123 import OUT
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, load_exact, text_at
from scripts.verify_plaque_release_v247 import find_mask


REPORT = OUT.with_name("recruitment_capacity_gameplay_20261123.json")
SHEET = REPORT.with_suffix(".png")
CASES = {
    "azores": (1048, 67, "Manuel Almeida", (18080,), 18360, (15900, 17800, 18080, 18360),
               (39333, 38633, 38633, 38633), "Assign Sailors", (50, 0, 205, 19)),
    "istanbul": (1042, 51, "Charles Rochefort", (6600, 7000), 8800, (3200, 5400, 8800),
                 (8371, 6798, 6798), "Tavern", (43, 233, 130, 268)),
}


def verify(case, candidate, arm, font, installed):
    folder = playback.PLAY / case
    report_path, terminal_path = folder / "capture/capture_report.json", folder / "terminal.json"
    report, terminal = map(read, (report_path, terminal_path))
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    for path, sha in terminal["evidence"].items():
        assert digest(path) == sha
    inputs, frames, end, _, donor = playback.schedule(case)
    assert report["scripted_input_schedule"] == inputs and report["exact_requested_capture_frames"] == list(frames)
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    calls = terminal["target_COMMON_calls"]
    key, count, speaker, holds, end_frame, cash_frames, funds, caption, bounds = CASES[case]
    matched = [row for row in calls if row["message_ID"] == key]
    assert [row["PC"] for row in matched] == [0x0205528C, 0x020534F4]
    assert all(row["caller_LR"] == 0x02053D10 and row["frame"] < holds[0] for row in matched)
    assert all(any(row["message_ID"] == number for row in calls) for number in (51, 904, 907))
    shot_map = shots(report, "cold_boot.png")
    view, evidence, results = [], {}, []
    paragraph = installed[key].text % str(count).encode("ascii")
    expected_lines = tuple((stage.DRAFTS[key][0] % str(count)).split(". ", 1))
    expected_lines = (expected_lines[0] + ".", expected_lines[1])
    for frame in holds:
        snap, raw = capture_ram(report, frame)
        plain, wrapped = (text_at(raw, unpack_from("<I", arm, at)[0]) for at in (0x5444C, 0x54450))
        assert plain.rstrip() == paragraph.rstrip() and wrapped.split() == paragraph.split()
        assert tuple(line.strip() for line in wrapped.decode("ascii").split("\n")) == expected_lines
        image = picture(shot_map[frame])
        glyphs = body_mask(font, image, expected_lines)
        complete_mask(font, speaker, image, 16, 277, (98, 97, 98))
        results.append(dict(frame=frame, formatted_hex=wrapped.hex(), lines=expected_lines, complete_body=glyphs,
                            capture=shot_map[frame], snapshot=snap, lowercase_and_final_punctuation_exact=True))
        view.append((f"{case.title()} / {speaker} / {frame}", image))
    balances = []
    for frame, amount in zip(cash_frames, funds, strict=True):
        snap, raw = capture_ram(report, frame)
        value = wallet(arm, raw)
        assert value == amount, (case, frame, value)
        balances.append(dict(frame=frame, gold=value, snapshot=snap))
    final = picture(shot_map[end_frame])
    # The selected menu captions are on light plaques or bright buttons.
    final_proof = dict(label=caption, frame=end_frame)
    if case == "istanbul":
        assign = picture(shot_map[7400])
        final_proof["assign_sailors"] = find_mask(font, "Assign Sailors", assign, (50, 0, 205, 19))
        view.append(("Istanbul / declined the next round, then assigned sailors", assign))
        final_proof["menu_glyphs"] = complete_mask(font, caption, final, 64, 245, (0, 8, 0))
    else:
        final_proof["assign_sailors"] = find_mask(font, caption, final, bounds)
        before_path = azores.ROOT / "revised/capture/capture_report.json"
        before = read(before_path)
        assert before["ROM_sha256"] == read(stage.parent.RELEASE)["candidate_sha256"]
        reference_frames = shots(before, "cold_boot.png")
        matches = tuple(n for n in frames if n != 18080)
        assert all(reference_frames[n]["framebuffer_sha256"] == shot_map[n]["framebuffer_sha256"] for n in matches)
        original = read(stage.VISIT)
        old_shot = shots(original, "navigation.png")[18080]
        earlier = picture(old_shot)
        difference = ImageChops.difference(earlier, view[0][1]).getbbox()
        assert difference and 16 <= difference[0] < difference[2] <= 244 and 295 <= difference[1] < difference[3] <= 360
        prior_state, = [row for row in original["read_only_pause_RAM_snapshots"] if row["frame"] == 18080]
        assert wallet(arm, load_exact(prior_state)) == funds[-1]
        evidence.update(full_matching_frames=list(matches), previous_prompt=old_shot, changed_body_bounds=difference)
        view.insert(0, ("Azores / previous prompt", earlier))
    view.append((f"{case.title()} / return", final))
    return dict(message_ID=key, count=count, voice=speaker, holds=results, call_pair=matched, gold_balances=balances,
                normal_continue_decline_return=final_proof, actual_gameplay=True, fixture=False,
                capture=reference(report_path), observer=reference(terminal_path), comparison=evidence), view


def main():
    staged = read(stage.PROOF)
    assert digest(stage.ROM) == staged["candidate_sha256"]
    rom = NdsImage.open(stage.ROM)
    arm, common = (rom.read_file(path) for path in (stage.ARM, stage.COMMON))
    installed = stage.recruitment.catalogue(arm, common)
    font = GameAsciiFont.from_arm9(arm)
    results, frames = {}, []
    for case in CASES:
        result, views = verify(case, staged["candidate_sha256"], arm, font, installed)
        results[case] = result
        frames.extend(views)
    sheet = Image.new("RGB", (3 * 268, 410 * ((len(frames) + 2) // 3)), "#28313b")
    draw = ImageDraw.Draw(sheet)
    for i, (label, image) in enumerate(frames):
        x, y = i % 3 * 268 + 6, i // 3 * 410
        draw.text((x, y + 4), label, fill="white")
        sheet.paste(image, (x, y + 22))
    sheet.save(SHEET)
    write(REPORT, dict(candidate_sha256=staged["candidate_sha256"], previous_sha256=staged["verified_predecessor_sha256"],
        ordinary_play=results, native_layout_only_IDs=list(range(1043, 1048)), hardware=False,
        screenshot=reference(SHEET), full_editorial_goal_complete=False))
    print("Verified Manuel and Charles, full choice controls, balances and two ordinary returns.")


if __name__ == "__main__":
    main()
