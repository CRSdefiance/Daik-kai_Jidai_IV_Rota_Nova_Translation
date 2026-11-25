"""Verify all thirteen naturally activated Amsterdam bread panels."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack, unpack_from
from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import checkpoint_town_trend_event_entries_20261121 as events
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts.verify_all_routes_next_phrase_wraps_20261118 import clipped_renderer
from scripts.verify_personal_gameplay_v841 import get_machine


base, native, replay = events.base, events.native, events.replay
ROOT = Path("out/amsterdam_bread_gameplay_20261121_v2")
REVIEW = Path("releases/all_routes_editorial_20261115_town_trend_exchanges_candidate/verification/registered_review.json")
PRIOR_PLANES = Path("work/analysis/lil_B178_native_approval_v4678/all13_native_progressive_FE_and_source_reconciliation.json")
RECEIPT = events.BOOK / "amsterdam_bread_gameplay_20261121_v1.json"
FILE = "/data/SC2.DK4"
B = 0x02000000
SCRATCH = 0x02640000
FIRST, STEP, RETURN = 12980, 260, 16360
INKS = ((0, 8, 0), (98, 97, 98))


def verify_event(arm, report, archive, selector_row):
    snapshot = report["read_only_RAM_snapshot"]
    path = Path(snapshot["path"])
    raw = path.read_bytes()
    assert snapshot["read_only_export"] and base.digest(path) == snapshot["sha256"]
    assert len(raw) == 0x400000
    at = raw.index(archive[:96])
    assert raw.find(archive[:96], at + 1) == -1
    owner = B + at - 0x34
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == 2
    actor = get(0xCB184) + 0x19E4
    get(0xCC9A8, SCRATCH, get(0xCB1B4))
    date = list(unpack("<5I", bytes(cpu.mem_read(SCRATCH, 20))))[1:]
    birthday = [get(0x82F88, actor), get(0x82F80, actor)]
    assert date[2] == birthday[1] == 0 and birthday[0] == 7 and date[1] == 0
    descriptor = list(unpack("<3I", bytes(cpu.mem_read(owner + 0x2454, 12))))
    assert descriptor == [selector_row[k] for k in ("category", "town", "facility")] == [7, 2, 0]
    index = selector_row["event_ID"]
    assert index == 178 and get(0x23840, owner + 4, index) == 1
    pointer = B + at + selector_row["event_record_offset"]
    get(0x23888, SCRATCH, owner + 4, index)
    assert unpack("<I", bytes(cpu.mem_read(SCRATCH, 4))) == (pointer,)
    source = bytes.fromhex(selector_row["record_hex"])
    state = bytes(cpu.mem_read(pointer, len(source)))
    assert state[4:] == source[4:] and (unpack_from("<I", state)[0] ^ unpack_from("<I", source)[0]) == 0xC0008000
    assert bytes(cpu.mem_read(B, 0x400000)) == raw
    return dict(read_only_snapshot=snapshot, calendar_date_fields=date, captain_birthday_fields=birthday,
                observed_facility_descriptor=descriptor, runtime_event_address=pointer, loaded_event_hex=state.hex(),
                native_event_completion=1, source_event=selector_row)


def read_frame(frames, number):
    row = frames[number]
    assert base.digest(row["path"]) == row["PNG_sha256"]
    return row, Image.open(row["path"]).convert("RGB")


def sheet(examples, target):
    canvas = Image.new("RGB", (1024, 410 * ((len(examples) + 1) // 2)), "#263238")
    draw = ImageDraw.Draw(canvas)
    for i, (label, panel) in enumerate(examples):
        x, y = (i % 2) * 512, (i // 2) * 410
        draw.text((x + 8, y + 4), label, fill="white")
        canvas.paste(panel.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x, y + 20))
    canvas.save(target)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, default=ROOT)
    arg = parser.parse_args()
    assert not RECEIPT.exists()
    folder = arg.folder
    log = folder / "capture/capture_report.json"
    report, index, release = map(base.load, (log, events.OUTPUT, replay.active.RELEASE))
    assert report["ROM_sha256"] == index["candidate_sha256"] == release["candidate_sha256"] == base.digest(replay.active.ROM)
    assert report["frames"] == 16870 and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    commands = folder / "capture/navigation_command_journal.json"
    journal = base.load(commands)["commands_received"]
    assert all(row["validation_passed"] for row in journal)
    assert journal[2]["frame"] == 12620 and journal[2]["command"]["buttons"] == ["A"]
    images = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
    roman = base.NdsImage.open(replay.active.ROM)
    arm = roman.read_file(native.ARM)
    context = SimpleNamespace(arm=arm, image=roman)
    font = roman.read_file("/GRP/KANJI.FNT")
    paint = clipped_renderer(context)
    paint_system = current_fe_painter(context)
    route = index["routes"][2]
    source_event, = [r for r in route["entries"] if r["script_block"] == 178]
    event = verify_event(arm, report, roman.read_file(route["event_archive"]), source_event)
    raw = native.IlnkContainer.parse(roman.read_file(FILE)).blocks[178]
    assert native.digest(raw) == source_event["prior_review"]["current_block_sha256"]
    rows = [r for r in base.load(REVIEW)["records"] if r["file_path"] == FILE and r["block"] == 178]
    references = base.load(PRIOR_PLANES)["cases"]
    assert len(rows) == len(references) == 13
    holds, scans, portraits, titles = [], [], {}, set()
    for i, (row, prior) in enumerate(zip(rows, references, strict=True)):
        assert row["id"] == prior["id"] and all(row["review"].values())
        ref = row["registered_reference"]
        stored = bytes.fromhex(ref["complete_command_hex"])
        at = ref["command_offset"]
        assert raw[at:at + len(stored)] == stored
        assert stored[5:].rstrip(b"\0 ") == bytes.fromhex(prior["encoded_hex"]).rstrip(b" ")
        actor = row["source_selector"]
        body = bytes.fromhex(ref["raw_hex"])[1:]
        if actor == 254:
            surface = paint_system(body)
            expected = surface["physical"]
            width = 228
        else:
            surface = paint(arm, font, body)
            page, = surface["pages"]
            assert page["native_independent_plane_equal"]
            expected = bytes.fromhex(page["native_plane_hex"])
            width = 216
        assert surface["complete_consumed_bytes"] == len(body) and len(expected) == width * 64
        captured, image = read_frame(images, FIRST + i * STEP)
        pixels = image.crop((16, 296, 16 + width, 360)).get_flattened_data()
        assert bytes(bool(v) for v in expected) == bytes(p == INKS[0] for p in pixels), (row["id"], captured["frame"])
        assert INKS[1] not in pixels
        if actor != 254:
            portraits.setdefault(actor, set()).add(native.digest(image.crop((4, 199, 67, 268)).tobytes()))
            titles.add(native.digest(image.crop((5, 274, 50, 288)).tobytes()))
        holds.append(dict(id=row["id"], selector=actor, registered_reference=ref,
            source_reference=row["source_reference"], source_hex=row["source_hex"], english_record=row["english"],
            decision=row["decision"], localization_note=row["localization_note"], five_gates=row["review"],
            complete_body_ink_mask_matches_current_renderer=True, current_native_plane_sha256=native.digest(expected),
            observed=captured))
        scans.append((row["id"], image))
    assert set(portraits) == {166, 167, 168} and all(len(p) == 1 for p in portraits.values()) and len(titles) == 1
    assert len({next(iter(p)) for p in portraits.values()}) == 3
    exit_frame, exit_image = read_frame(images, RETURN)
    entry, _ = read_frame(images, 12620)
    assert exit_image.size == (256, 384)
    target = folder / "verified_bread_exchange_1.png"
    sheet(scans[:6], target)
    second = folder / "verified_bread_exchange_2.png"
    sheet(scans[6:12], second)
    closing = folder / "verified_bread_forecast_and_return.png"
    sheet([scans[12], ("Return to Amsterdam's Square", exit_image)], closing)
    results = (target, second, closing)
    base.save(RECEIPT, dict(candidate_sha256=report["ROM_sha256"], ROM=report["ROM"], frames=report["frames"],
        fresh_masks_from_current_registered_font_and_native_painters=True, natural_activation=True, ordinary_new_game_and_square_inputs=True,
        test_setup="Lil's birthday set to August 1 in the normal New Game editor to match the opening calendar day.",
        hardware_verified=False, scene=FILE, block=178, event=event, panels=holds, return_to_square=exit_frame,
        Square_selected_before_confirm=entry, separate_nameplate_artwork_for_each_actor=True,
        three_distinct_portraits_and_identical_Lady_header_crop=True, new_editorial_credit=0,
        screenshots=[dict(path=str(path), sha256=base.digest(path)) for path in results],
        evidence={str(path):base.digest(path) for path in (REVIEW, PRIOR_PLANES, events.OUTPUT, log, commands)}))
    print("All 13 complete native mask matches, the original event completion bit and three separate portraits verified.")


if __name__ == "__main__":
    main()

