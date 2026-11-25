"""Compare the selected Square and Market pages before and after the revision."""

from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_square_and_market_reward_wraps_20261123 as stage
from scripts import verify_market_reward_dialogue_20261115 as market
from scripts.verify_giveaway_gameplay_v746 import cargo
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


base = stage.base
LIVE = stage.ROOT / "focused_dialogue.json"


def display_hold(key, frame, old, new, old_plane, new_plane, evidence):
    for shot in (old, new):
        evidence[shot["path"]] = shot["PNG_sha256"]
    a, b = map(market.captured, (old, new))
    pixels = [native_hold(image, plane) for image, plane in ((a, old_plane), (b, new_plane))]
    diff = ImageChops.difference(a, b).getbbox()
    if key in stage.EDITS:
        assert diff and 16 <= diff[0] < diff[2] <= 244 and 294 <= diff[1] < diff[3] <= 360
    else:
        assert diff is None
    return dict(message_ID=key, frame=frame, native_ink_pixels=pixels, changed_bounds=diff), (a, b)


def render_sheet(name, pairs):
    path = stage.ROOT / f"{name}_replay.png"
    sheet = Image.new("RGB", (1040, 228 * len(pairs)), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (label, images) in enumerate(pairs):
        for col, (version, photo) in enumerate(zip(("Previous", "Revised"), images, strict=True)):
            x, y = col * 520 + 4, index * 228
            draw.text((x, y + 4), f"{label} · {version}", fill="white")
            body = photo.crop((0, 280, 256, 384))
            sheet.paste(body.resize((512, 208), Image.Resampling.NEAREST), (x, y + 16))
    sheet.save(path)
    return {str(path): base.digest(path)}


def market_holds(stored, displays, evidence):
    runs = []
    for side, case, sha in (("old", "current", stored["predecessor_sha256"]),
                            ("new", "reviewed", stored["candidate_sha256"])):
        folder = stage.ROOT / f"{side}_market"
        read = FunctionType(market.read_run.__code__, vars(market) | {"ROOT": folder})
        runs.append(read(case, sha))
    (before, old_trace, older, prior_paths), (after, new_trace, newer, live_paths) = runs
    assert all(before[name] == after[name] for name in ("scripted_input_schedule", "core_DLL_sha256", "core_options"))
    assert older.keys() == newer.keys()
    evidence.update(prior_paths | live_paths)
    holds, panels = [], []
    for key, a, b in zip(market.CHAIN, old_trace, new_trace, strict=True):
        old_hex, new_hex, old_plane, new_plane = displays[key]
        assert a["source_request"] == b["source_request"]
        assert a["frame"] == b["frame"] and a["bounds"] == b["bounds"] == [0, 0, 228, 48]
        assert a["text_hex"] == old_hex and b["text_hex"] == new_hex
        for frame in sorted(n for n in older if n > b["frame"]):
            try:
                native_hold(market.captured(newer[frame]), new_plane)
            except AssertionError:
                continue
            row, pictures = display_hold(key, frame, older[frame], newer[frame], old_plane, new_plane, evidence)
            holds.append(row)
            panels.append((f"Market {key}", pictures))
            break
        else:
            raise AssertionError(("Market panel not held", key))
    for n in (12000, 12001):
        assert older[n]["PNG_sha256"] == newer[n]["PNG_sha256"]
        evidence[older[n]["path"]] = older[n]["PNG_sha256"]
        evidence[newer[n]["path"]] = newer[n]["PNG_sha256"]
    return holds, [12000, 12001], render_sheet("market_reward", panels)


def square_holds(stored, displays, evidence, arm):
    frames = []
    for side, sha in (("old", stored["predecessor_sha256"]), ("new", stored["candidate_sha256"])):
        folder = stage.ROOT / f"{side}_square/samples"
        terminal = folder / "terminal.json"
        summary = base.load(terminal)
        path = Path(summary["report"])
        report = base.load(path)
        assert base.digest(path) == summary["report_sha256"] and report["ROM_sha256"] == sha
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        save = report["battery_save_preloaded"]
        assert save["copied_byte_exact_before_cold_boot"] and summary["original_save_unchanged"]
        assert save["source_sha256"] == summary["source_save_sha256"]
        fixture, = report["synthetic_missionary_Chapel_assignment_fixtures"]
        assert fixture["frame"] == 3200 and fixture["supplied_voice_style"] == 5
        assert fixture["original_confirmation"] == 663 and fixture["original_announcement"] == 671
        assert len(fixture["changes"]) == 4 and fixture["only_four_declared_room_assignment_and_voice_bytes_changed"]
        ram = {}
        for record in report["read_only_pause_RAM_snapshots"]:
            raw = Path(record["path"]).read_bytes()
            assert record["read_only_export"] and base.digest(record["path"]) == record["sha256"]
            ram[record["frame"]] = raw
            evidence[record["path"]] = record["sha256"]
        assert [cargo(arm, ram[n]) for n in (3200, report["frames"])] == [2, 0]
        frames.append(market.shots(report))
        evidence.update({str(p): base.digest(p) for p in (terminal, path)})
    older, newer = frames
    holds, panels = [], []
    for frame, key in ((4800, 663), (5200, 663), (6800, 671), (7200, 674)):
        _, _, old_plane, new_plane = displays[key]
        result, pair = display_hold(key, frame, older[frame], newer[frame], old_plane, new_plane, evidence)
        holds.append(result)
        if frame != 5200:
            panels.append((f"Square {key}", pair))
    assert older[8000]["PNG_sha256"] == newer[8000]["PNG_sha256"]
    for shot in (older[8000], newer[8000]):
        evidence[shot["path"]] = shot["PNG_sha256"]
    return holds, [8000], render_sheet("square_sample", panels)


def main():
    assert not LIVE.exists()
    stored = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    previous = base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM) == previous["candidate_sha256"] == stored["predecessor_sha256"]
    ctx = stage.town.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    rom = base.NdsImage.open(stage.ROM)
    arm, kanji = (rom.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    assert arm == ctx.arm
    raster, _, _ = stage.town.font_tools(rom)
    displays = {}
    for row in stored["records"]:
        key = row["message_ID"]
        old, _ = stage.display(ctx, bytes.fromhex(row["current_hex"]), key, cpu)
        new = bytes.fromhex(row["display_hex"])
        old_plane, new_plane = (stage.town.render_portrait(raster, arm, kanji, data)[0] for data in (old, new))
        assert stage.native.digest(new_plane) == row["native_plane_sha256"]
        displays[key] = (old.hex(), new.hex(), old_plane, new_plane)
    evidence = {str(stage.PROOF): base.digest(stage.PROOF)}
    commerce, market_return, market_sheet = market_holds(stored, displays, evidence)
    square, square_return, square_sheet = square_holds(stored, displays, evidence, arm)
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        observed=dict(market=commerce, square=square), revised_holds=2, retained_holds=5, menu_transitions=3,
        revised_offline_only_records=[], ordinary_gameplay=False, focused_fixtures=True, hardware=False,
        returns=dict(market=market_return, square=square_return), evidence=evidence, sheets=market_sheet | square_sheet))
    print("Verified both revised holds, five retained holds and three transition frames in focused replays.")


if __name__ == "__main__":
    main()
