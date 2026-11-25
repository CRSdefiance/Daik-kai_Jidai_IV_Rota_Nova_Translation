"""Verify the save dialog path and the exact candidate's startup."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_save_dialogue_followup_20261119 as replay
from scripts import verify_sea_event_dialogue_followup_20261118 as startup_workflow
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.plan_literal_static_layout_v1 import HEIGHT, WIDTH, render
from scripts.primary_town_native_font_v2102 import font_tools

stage, base = replay.stage, replay.base
STARTUP = stage.ROOT / "own_startup_verification.json"
GAME = stage.ROOT / "verified_save_dialogue.json"
SHEET = stage.ROOT / "save_gameplay.png"
CALL_SITES = {0xED6F4: 0, 0xED72C: 0, 0xED79C: "r5", 0xEE740: 0, 0xEE85C: 0,
              0xEEB50: 1, 0xEEC10: 1, 0xEECD8: "r7", 0xEED44: "r7", 0xEEEE0: "r7"}


def startup():
    check = FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | dict(
        stage=stage, replay=replay, STARTUP=STARTUP, __file__=__file__))
    check()


def mask_at(plane, pixels):
    points = [(i % WIDTH, i // WIDTH) for i, value in enumerate(plane) if value]
    sample = points[::max(1, len(points) // 12)]
    white = {(i % 256, i // 256) for i, color in enumerate(pixels.get_flattened_data()) if color == (0, 8, 0)}
    matched = []
    for x, y in white:
        ox, oy = x - points[0][0], y - points[0][1]
        if not (0 <= ox <= 256-WIDTH and 0 <= oy <= 192-HEIGHT):
            continue
        if not all((ox + a, oy + b) in white for a,b in sample):
            continue
        full = {(x,y) for x,y in white if ox <= x < ox+WIDTH and oy <= y < oy+HEIGHT}
        if full == {(ox+a, oy+b) for a,b in points}:
            matched.append([ox, oy+192, ox+WIDTH, oy+192+HEIGHT])
    bounds, = matched
    return bounds


def site_census(clean, arm):
    def calls(raw):
        result = []
        for at in range(0, len(raw)-3, 4):
            w, = unpack_from("<I", raw, at)
            if w & 0x0E000000 != 0x0A000000:
                continue
            delta = ((w & 0xFFFFFF) ^ 0x800000) - 0x800000
            if at + 8 + 4*delta == 0xEEF24:
                result.append(at)
        return result
    expected_words = {0: 0xE3A00000, 1: 0xE3A00001, "r5": 0xE1A00005, "r7": 0xE1A00007}
    assert calls(clean) == calls(arm) == list(CALL_SITES)
    rows = []
    for at, mode in CALL_SITES.items():
        exact = clean[at-4:at+4]
        assert arm[at-4:at+4] == exact
        assert unpack_from("<I", exact)[0] == expected_words[mode]
        rows.append(dict(ARM9_call_PC=stage.BASE+at, mode_initializer=mode, exact_instructions_hex=exact.hex()))
    return rows


def gameplay():
    assert not GAME.exists() and not SHEET.exists()
    staged, terminal = map(base.load,(stage.PROOF,replay.OUT/"terminal.json"))
    sha = base.digest(stage.ROM)
    assert sha == staged["candidate_sha256"] == terminal["candidate_sha256"]
    assert terminal["donor_unchanged"] and base.digest(terminal["report"]) == terminal["report_sha256"]
    assert base.digest(terminal["commands"]) == terminal["commands_sha256"]
    report, raw = checked_report(terminal["report"], sha, 7200)
    assert not any(report[k] for k in report if k.startswith("synthetic_") and k != "synthetic_condition_fixtures")
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    snapshots = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    frames = {r["frame"]: r for r in report["frames_captured"]}

    def snapshot(n):
        shot = snapshots[n]
        assert shot["read_only_export"] and base.digest(shot["path"]) == shot["sha256"]
        return Path(shot["path"]).read_bytes()

    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    raster, _, _ = font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    fixture = []
    for n, mode in ((replay.PAUSE, "write-return-zero"), (replay.RENDER_FRAME, "restore-write")):
        _, note = replay.set_condition(arm, snapshot(n), {"mode": mode})
        fixture.append(note | {"frame": n})
    assert report["synthetic_condition_fixtures"] == fixture
    off = replay.FIELD - stage.BASE
    assert raw[off:off+4] == arm[off:off+4]
    rows = {row["id"]:row for row in staged["records"]}
    after_format = unpack_from("<I", arm, 0x54894)[0] - stage.BASE
    observed = []
    sheet = Image.new("RGB", (1024, 410), "#273642")
    draw = ImageDraw.Draw(sheet)
    for i, (n, label, key) in enumerate((
            (replay.PAUSE, "Ordinary occupied-slot confirmation", "DK4_SAVE_OVERWRITE_CONFIRM"),
            (replay.RENDER_FRAME, "Focused write-error response", "DK4_SAVE_WRITE_ERROR"))):
        row = rows[key]
        frozen = snapshot(n)
        display = frozen[after_format:after_format+256].split(b"\0", 1)[0]
        assert display.hex() == row["display_hex"]
        plane, _, _, _ = render(raster,font,arm,display)
        assert stage.digest(plane) == row["native_ink_sha256"]
        with Image.open(frames[n]["path"]) as photo:
            lower = photo.convert("RGB").crop((0,192,256,384))
        crop = mask_at(plane,lower)
        draw.text((i*512+8, 3),label,fill="white")
        sheet.paste(lower.resize((512,384),Image.Resampling.NEAREST),(i*512,21))
        observed.append(dict(id=key, frame=n, capture=frames[n], crop=crop, complete_native_glyph_mask=True,
            supplied_write_failure=i>0))
    sheet.save(SHEET)
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    calls = site_census(clean, arm)
    base.save(GAME, dict(candidate_sha256=sha, observed=observed, actual_emulator=True, hardware=False,
        untouched_donor_verified=True, fixture=fixture, native_write_instruction_restored=True,
        original_failure_selector_direct_ARM_sites=calls,
        offline_only_revision_ids=sorted(set(rows)-{r["id"] for r in observed}),
        evidence={str(p):base.digest(p) for p in (
            stage.PROOF,replay.OUT/"terminal.json",terminal["report"],terminal["commands"],SHEET,Path(__file__))}))
    print("Verified both complete live dialog masks and the ten original card-error call sites.")


if __name__ == "__main__":
    gameplay()
    startup()

