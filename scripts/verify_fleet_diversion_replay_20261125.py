"""Check both Lure Fleet prompt pairs and the surrounding native transitions."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_fleet_diversion_questions_20261125 as replay
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_scheme_gameplay_v776 import ADVANCE, BODY
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


draft = replay.draft
OUT = draft.OUT.with_name("fleet_diversion_questions_paired_20261125.json")
SHEET = OUT.with_suffix(".png")
HOLD = 16400
COMPANIONS = (3200, 15200, 16000, 16800, 17200, 17600, 18000)


def captures(version, message):
    folder = replay.ROOT / f"{version}_{message}"
    terminal = read(folder / "terminal.json")
    report_path = Path(terminal["capture"]["path"])
    assert terminal["capture"] == reference(report_path)
    report = read(report_path)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert terminal["candidate"] == reference(report["ROM"])
    file = NdsImage.open(report["ROM"])
    arm = file.read_file(draft.current.ARM)
    tables = file.read_file(draft.current.COMMON)
    entries = draft.native.owned_entries(tables, arm, sha256(arm[draft.native.DIRECTORY_OFFSET:draft.native.TABLE_OFFSET]).hexdigest())
    frames, memory = {}, {}
    for frame in report["frames_captured"]:
        path = Path(frame["path"])
        assert digest(path) == frame["PNG_sha256"]
        if frame["frame"] in replay.CAPTURES and path.stem.endswith("_cold_boot"):
            frames[frame["frame"]] = Image.open(path).convert("RGB")
    for meta in report["read_only_capture_RAM_snapshots"] + report["read_only_pause_RAM_snapshots"]:
        raw = Path(meta["path"]).read_bytes()
        assert meta["read_only_export"] and meta["bytes"] == len(raw) == 0x400000
        assert sha256(raw).hexdigest() == meta["sha256"]
        assert meta["frame"] not in memory or memory[meta["frame"]] == raw
        memory[meta["frame"]] = raw
    assert set(frames) == set(memory) == {HOLD, *COMPANIONS}
    receipt, = report["synthetic_strategist_room_assignment_fixtures"]
    _, expected = replay.fixture(arm, memory[3200], True, message, sha256(arm).hexdigest())
    assert receipt == expected | {"frame": 3200}
    return terminal, report, file, arm, entries, frames, memory, receipt


def check_panel(raw, arm, rom, frame, body, layout):
    expanded, formatted, owner = (unpack_from("<I", arm, offset)[0] for offset in (0x5444C, 0x54450, 0x552A0))
    assert cstring(raw, owner + 0x2030) == cstring(raw, expanded) == body
    rendered = bytes.fromhex(layout["formatted_hex"])
    assert cstring(raw, formatted) == rendered
    mask = draft.schemes.native_portrait(arm, rom.read_file("/GRP/KANJI.FNT"), rendered, layout["lines"])
    assert sha256(mask).hexdigest() == layout["complete_glyph_mask_sha256"]
    expected = {(16 + i % 228, 296 + i // 228) for i, ink in enumerate(mask) if ink}
    actual = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
              if frame.getpixel((x, y)) == (0, 8, 0)}
    assert expected == actual, (len(expected - actual), len(actual - expected))
    return actual


def main():
    packet = read(draft.OUT)
    results, previews = [], []
    for row in packet["records"]:
        message = row["message_ID"]
        if message not in draft.DRAFTS:
            continue
        a, b = (captures(version, message) for version in ("current", "proposed"))
        assert a[3] == b[3] and a[1]["scripted_input_schedule"] == b[1]["scripted_input_schedule"]
        assert a[1]["core_options"] == b[1]["core_options"]
        assert a[7]["changes"] == b[7]["changes"]
        for number in COMPANIONS:
            difference = ImageChops.difference(a[5][number], b[5][number])
            assert difference.getbbox() is None, (message, number, difference.getbbox())
        paired_state = {number: state(a[3], a[6][number]) for number in (3200, 16400, 17200, 18000)}
        assert paired_state == {number: state(b[3], b[6][number]) for number in paired_state}
        assert paired_state[17200]["cash"] == paired_state[18000]["cash"]
        for frame in (17200, 17600):
            for run in (a, b):
                confirmation = cstring(run[6][frame], unpack_from("<I", run[3], 0x5444C)[0])
                assert b"Clifford" in confirmation and b"London" in confirmation
        masks = []
        for run, layout in zip((a, b), row["native_layouts"], strict=True):
            body = run[4][message].text
            assert body.decode("ascii").strip() == " ".join(layout["lines"])
            masks.append(check_panel(run[6][HOLD], run[3], run[2], run[5][HOLD], body, layout))
            previews.append((f'{message} {layout["version"]}', run[5][HOLD].crop((0, 192, 256, 384))))
        difference = ImageChops.difference(a[5][HOLD], b[5][HOLD])
        difference.paste((0, 0, 0), ADVANCE)
        text_pixels = masks[0] | masks[1]
        for x, y in text_pixels | {(x + 1, y + 1) for x, y in text_pixels}:
            difference.putpixel((x, y), (0, 0, 0))
        assert difference.getbbox() is None, (message, difference.getbbox())
        results.append(dict(message_ID=message, hold=HOLD, current=a[0], proposed=b[0],
                            entirely_matching_frames=list(COMPANIONS), paired_state=paired_state,
                            glyph_plane_matches_preflight=True, nameplate_identical=True,
                            confirmation_faction="Clifford", confirmation_destination="London",
                            cancelled_without_payment=True, prior_preview=row["native_layouts"]))
    img = Image.new("RGB", (1024, 816), (39, 50, 56))
    labels = ImageDraw.Draw(img)
    for index, (label, panel) in enumerate(previews):
        x, y = 512 * (index % 2), 408 * (index // 2)
        labels.text((x + 8, y + 5), label, fill="white")
        img.paste(panel.resize((512, 384), Image.Resampling.NEAREST), (x, y + 22))
    img.save(SHEET)
    write(OUT, dict(preflight=reference(draft.OUT), staged=read(replay.PROOF), results=results,
                    sheet=reference(SHEET), ordinary_gameplay=False, focused_fixture_gameplay=True,
                    editor_credit_added=0, registered=False))
    print("Verified two revised holds, 14 whole-screen comparisons and both cancellation returns.")


if __name__ == "__main__":
    main()
