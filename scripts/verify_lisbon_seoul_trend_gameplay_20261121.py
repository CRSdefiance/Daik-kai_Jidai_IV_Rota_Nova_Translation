"""Bind the first ordinary Lisbon and Seoul trend replays to the current ROM."""

from pathlib import Path
from struct import unpack, unpack_from
from types import SimpleNamespace

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_town_trends_saved_game_20261121 as runs
from scripts import verify_amsterdam_bread_gameplay_20261121 as town
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, native = town.base, town.native
OUTPUT = town.events.BOOK / "lisbon_seoul_trend_gameplay_20261121_v1.json"
ROUTES = {
    "lisbon": dict(route=1, block=184, duration_days=27, first=18250, step=310, returned=21660,
                   opening_calendar=[1, 16], final_calendar=[2, 12], birthday=[7, 12], last_rest=17350, entry=17950),
    "seoul": dict(route=3, block=166, duration_days=11, first=20640, step=340, returned=25740,
                  opening_calendar=[2, 24], final_calendar=[3, 7], birthday=[6, 7], last_rest=7860, entry=20320),
}
RECRUITMENT = Path("releases/all_routes_editorial_20261115_seoul_recruitment_candidate/verification/registered_review.json")


def event_completion(arm, report, archive, event, plan):
    proof = report["read_only_RAM_snapshot"]
    assert proof["read_only_export"] and base.digest(proof["path"]) == proof["sha256"]
    raw = Path(proof["path"]).read_bytes()
    assert len(raw) == 0x400000
    at = raw.index(archive[:96])
    assert raw.find(archive[:96], at + 1) == -1
    owner = town.B + at - 0x34
    cpu, get = town.get_machine(arm, raw)
    assert get(0x7F244) == plan["route"]
    get(0xCC9A8, town.SCRATCH, get(0xCB1B4))
    _, _, month, day, _ = unpack("<5I", bytes(cpu.mem_read(town.SCRATCH, 20)))
    assert [month + 1, day + 1] == plan["final_calendar"]
    actor = get(0xCB184) + 0x19E4
    birthday = [get(0x82F88, actor) + 1, get(0x82F80, actor) + 1]
    assert birthday == plan["birthday"] and birthday[1] == day + 1
    descriptor = list(unpack("<3I", bytes(cpu.mem_read(owner + 0x2454, 12))))
    assert descriptor == [event[k] for k in ("category", "town", "facility")]
    assert get(0x23840, owner + 4, event["event_ID"]) == 1
    if plan["route"] == 3:
        assert get(0x23840, owner + 4, 140) == 1
    get(0x23888, town.SCRATCH, owner + 4, event["event_ID"])
    at = town.B + at + event["event_record_offset"]
    assert unpack("<I", bytes(cpu.mem_read(town.SCRATCH, 4))) == (at,)
    clean = bytes.fromhex(event["record_hex"])
    completed = bytes(cpu.mem_read(at, len(clean)))
    assert completed[4:] == clean[4:]
    assert unpack_from("<I", completed)[0] ^ unpack_from("<I", clean)[0] == 0xC0008000
    assert bytes(cpu.mem_read(town.B, 0x400000)) == raw
    return dict(original_event=event, matched_town_facility_and_date=True, completion_getter=1,
                runtime_event_hex=completed.hex(), final_calendar=plan["final_calendar"],
                birthday=birthday, read_only_snapshot=proof)


def mask_check(render, width, image):
    actual = image.crop((16, 296, 16 + width, 360)).get_flattened_data()
    assert len(render) == len(actual) == width * 64 and town.INKS[1] not in actual
    return bytes(bool(pixel) for pixel in render) == bytes(pixel == town.INKS[0] for pixel in actual)


def main():
    assert not OUTPUT.exists()
    active = runs.active
    candidate = base.digest(active.ROM)
    release, event_map = map(base.load, (active.RELEASE, town.events.OUTPUT))
    assert candidate == release["candidate_sha256"] == event_map["candidate_sha256"]
    original, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    arm, font = (current.read_file(name) for name in (native.ARM, "/GRP/KANJI.FNT"))
    ctx = SimpleNamespace(image=current, arm=arm)
    painter, system_painter = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    name_font = GameAsciiFont.from_arm9(arm)
    review = base.load(town.REVIEW)["records"]
    results = []
    for city, plan in ROUTES.items():
        folder = runs.ROOT / city
        report_path = folder / "capture/capture_report.json"
        plan_path = folder / "source_save.json"
        journal_path = folder / "capture/navigation_command_journal.json"
        report, donor, journal = map(base.load, (report_path, plan_path, journal_path))
        stored_save = report["battery_save_preloaded"]
        assert stored_save["copied_byte_exact_before_cold_boot"]
        assert stored_save["source_sha256"] == donor["sha256"] == base.digest(donor["donor"])
        assert stored_save["source"] == donor["donor"]
        assert report["ROM_sha256"] == donor["working_ROM_sha256"] == candidate and report["cold_boot"]
        assert not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        assert report["frames"] == plan["returned"]
        assert all(record["validation_passed"] for record in journal["commands_received"])
        route = event_map["routes"][plan["route"]]
        path = route["scene_archive"]
        event, = [item for item in route["entries"] if item["script_block"] == plan["block"]]
        control = event_completion(arm, report, current.read_file(route["event_archive"]), event, plan)
        jpn, eng = [native.IlnkContainer.parse(image.read_file(path)).blocks[plan["block"]]
                    for image in (original, current)]
        assert native.digest(jpn) == event["prior_review"]["clean_block_sha256"]
        assert native.digest(eng) == event["prior_review"]["current_block_sha256"]
        rows = [row for row in review if row["file_path"] == path and row["block"] == plan["block"]]
        assert len(rows) == event["prior_review"]["records"]
        captures = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
        matched, pics = [], []
        for index, row in enumerate(rows):
            source, stored = row["source_reference"], row["registered_reference"]
            before, after = [bytes.fromhex(ref["complete_command_hex"]) for ref in (source, stored)]
            for bank, ref, cmd in ((jpn, source, before), (eng, stored, after)):
                at = ref["command_offset"]
                assert bank[at:at + len(cmd)] == cmd
            assert before[:6] == after[:6] and all(row["review"].values())
            body = bytes.fromhex(stored["raw_hex"])[1:]
            assert body.isascii()
            if row["source_selector"] == 254:
                native_result = system_painter(body)
                plane, width = native_result["physical"], 228
            else:
                native_result = painter(arm, font, body)
                page, = native_result["pages"]
                assert page["native_independent_plane_equal"]
                plane, width = bytes.fromhex(page["native_plane_hex"]), 216
            assert native_result["complete_consumed_bytes"] == len(body)
            frame, image = town.read_frame(captures, plan["first"] + plan["step"] * index)
            assert mask_check(plane, width, image), (city, row["id"], frame["frame"])
            name = None
            if row["source_selector"] in (166, 167, 168):
                count, name_bounds = complete_mask(name_font, "Lady", image, 16, 277, town.INKS[1])
                name = dict(label="Lady", full_mask_ink=count, bounds=name_bounds)
            matched.append(dict(id=row["id"], english=row["english"], source_hex=row["source_hex"], source_reference=source,
                registered_reference=stored, previous_decision=row["decision"], decision="retention",
                localization_note=row["localization_note"], five_gates=row["review"], native_width=width,
                complete_native_body_sha256=native.digest(plane), nameplate=name, observed=frame))
            pics.append((row["id"], image))
        return_frame, returned = town.read_frame(captures, plan["returned"])
        start, _ = town.read_frame(captures, 3760)
        rest, _ = town.read_frame(captures, plan["last_rest"])
        entry, _ = town.read_frame(captures, plan["entry"])
        pics.append(("Return to the Square", returned))
        sheets = []
        for i in range(0, len(pics), 6):
            target = folder / f"reviewed_pages_{i // 6 + 1}.png"
            town.sheet(pics[i:i+6], target)
            sheets.append(dict(path=str(target), sha256=base.digest(target)))
        competing_event = []
        if city == "seoul":
            for no, detail in ((9100, "Yukihisa stops Yifa"), (11500, "Yifa asks Li Clan to take her aboard"),
                               (19980, "Yifa Sol joined!"), (20320, "Square return before new selection")):
                frame, _ = town.read_frame(captures, no)
                competing_event.append(dict(detail=detail, observed=frame))
        results.append(dict(city=city, previous_review_path=str(town.REVIEW), event=control,
            original_stay_durations_total=plan["duration_days"], opened_existing_save=start, after_rest=rest,
            Square_before_confirm=entry, Square_after_notice=return_frame, finished_recruitment_before_trend=competing_event,
            records=matched, sheets=sheets, evidence={str(p):base.digest(p)
                for p in (report_path, plan_path, journal_path, folder / "navigation.jsonl")}))
        print(city, len(matched), "complete dialogue and notice planes with original event completion.")
    base.save(OUTPUT, dict(candidate_sha256=candidate, natural_activation=True, played_on_registered_ROM=True,
        preexisting_battery_saves_copied_by_hash=True, all_changes_from_ordinary_play=True, hardware_verified=False,
        new_editorial_credit=0, town_runs=results,
        dependencies={str(p):base.digest(p) for p in (town.REVIEW, RECRUITMENT, town.events.OUTPUT, active.RELEASE)}))


if __name__ == "__main__":
    main()

