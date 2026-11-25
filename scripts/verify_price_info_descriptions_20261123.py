"""Verify the revised Beef description and its return to the ordinary Price Info list."""

from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_price_info_descriptions_20261123 as replay
from scripts.checkpoint_price_info_wraps_20261115 import PAPER, screen_pixels
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.verify_azores_return_20261123 import picture, shots
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact
from scripts.verify_trade_good_descriptions_v1 import exact_title


REPORT = replay.ROOT / "price_info_gameplay.json"
SHEET = replay.ROOT / "price_info_gameplay.png"
HOLD, CLOSED = 16200, 16600


def main():
    stage = replay.stage
    proof, review = map(read, (stage.STORED, stage.MANUSCRIPT))
    controls, donor = replay.inputs()
    frame_sets, evidence = {}, []
    row, = [item for item in review["records"] if item["message_id"] == 143]
    arm = NdsImage.open(stage.ROM).read_file("/__arm9__.bin")
    font = GameAsciiFont.from_arm9(arm)
    for case, sha_key, text_key in (("current", "previous_sha256", "exact_current_hex"),
                                  ("revised", "candidate_sha256", "staged_hex")):
        folder = replay.ROOT / case
        report_path = folder / "capture/capture_report.json"
        capture = read(report_path)
        assert capture["ROM_sha256"] == proof[sha_key] and capture["frames"] == replay.FRAMES[-1]
        assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
        assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
        assert capture["scripted_input_schedule"] == controls == read(folder / "inputs.json")
        assert capture["exact_requested_capture_frames"] == list(replay.FRAMES)
        assert capture["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
        assert capture["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        snapshot, = [snap for snap in capture["read_only_capture_RAM_snapshots"] if snap["frame"] == HOLD]
        raw = load_exact(snapshot)
        stored = bytes.fromhex(row[text_key]) + b"\0"
        for addr in unpack_from("<2I", arm, 0x54890):
            offset = addr - 0x02000000
            assert raw[offset:offset + len(stored)] == stored
        frames = shots(capture, "_cold_boot.png")
        frame_sets[case] = {f: picture(frames[f]) for f in replay.FRAMES}
        evidence.extend(reference(path) for path in (report_path, folder / "inputs.json", snapshot["path"], frames[HOLD]["path"], frames[CLOSED]["path"]))

    before, after = (frame_sets[case][HOLD] for case in ("current", "revised"))
    complete_page, = row["pages"]
    assert screen_pixels(after) == complete_page["pixel_sha256"] != screen_pixels(before)
    changed = ImageChops.difference(before, after).getbbox()
    assert changed and PAPER[0] <= changed[0] < changed[2] <= PAPER[2] and PAPER[1] <= changed[1] < changed[3] <= PAPER[3]
    exact_frames = [f for f in replay.FRAMES if ImageChops.difference(frame_sets["current"][f], frame_sets["revised"][f]).getbbox() is None]
    assert exact_frames == [f for f in replay.FRAMES if f != HOLD]
    assert exact_title(font, "Beef", frame_sets["revised"][15800]) == exact_title(font, "Beef", frame_sets["revised"][CLOSED])
    sheet = Image.new("RGB", (804, 218), "#24303c")
    draw = ImageDraw.Draw(sheet)
    closed = frame_sets["revised"][CLOSED]
    for i, (label, frame) in enumerate((("Previous Beef description", before), ("Revised Beef description", after), ("Back at the list", closed))):
        draw.text((268 * i + 6, 4), label, fill="white")
        sheet.paste(frame.crop((0, 192, 256, 384)), (268 * i + 6, 22))
    sheet.save(SHEET)
    write(REPORT, dict(candidate_sha256=proof["candidate_sha256"], previous_sha256=proof["previous_sha256"],
        ordinary_gameplay=True, fixture=False, live_message_ID=143, page=complete_page, full_frame_control_matches=exact_frames,
        original_choice_or_page_advance=True, returned_to_list_frame=CLOSED, changed_body_bounds=changed,
        screenshot=reference(SHEET), hardware=False, evidence=evidence))
    print("Verified the complete Beef page, original exit and ten exact control frames.")


if __name__ == "__main__":
    main()
