"""Verify London's and Athens's ordinary town trends and Stockholm's calendar gate."""
from pathlib import Path
from struct import pack, unpack, unpack_from
from types import SimpleNamespace

from scripts import replay_european_trends_20261121 as runs
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as previous


town, base, native = previous.town, previous.base, previous.native
OUTPUT = town.events.BOOK / "european_trend_gameplay_20261121_v1.json"
CASES = {
    "london": dict(route=1, town=0, block=186, first=14710, step=310, returned=17190,
                   opening=3760, ready=13720, entry=14380, opening_calendar=[10, 27],
                   final_calendar=[11, 12], birthday=[7, 12], days=16),
    "athens": dict(route=1, town=19, block=185, first=14490, step=310, returned=17590,
                   opening=5810, ready=13500, entry=14160, opening_calendar=[9, 22],
                   final_calendar=[10, 12], birthday=[7, 12], days=20),
}


def capture_receipt(city, sha):
    folder = runs.ROOT / city
    path = folder / "capture/capture_report.json"
    plan_path = folder / "source_save.json"
    journal_path = folder / "capture/navigation_command_journal.json"
    report, donor, journal = map(base.load, (path, plan_path, journal_path))
    assert report["ROM_sha256"] == donor["working_ROM_sha256"] == sha and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert all(row["validation_passed"] for row in journal["commands_received"])
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"] and battery["source"] == donor["donor"]
    assert battery["source_sha256"] == donor["sha256"] == base.digest(donor["donor"])
    captures = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
    refs = (path, plan_path, journal_path, folder / "navigation.jsonl", folder / "inputs.json")
    return folder, report, captures, {str(p): base.digest(p) for p in refs}


def stockholm(sha, arm, archive, event):
    _, report, captures, evidence = capture_receipt("stockholm", sha)
    assert report["frames"] == 9300
    s = report["read_only_RAM_snapshot"]
    raw = Path(s["path"]).read_bytes()
    assert len(raw) == 0x400000 and s["read_only_export"] and base.digest(s["path"]) == s["sha256"]
    owner_at = raw.index(archive[:96])
    assert raw.find(archive[:96], owner_at+1) == -1
    owner = town.B + owner_at - 0x34
    cpu, get = town.get_machine(arm, raw)
    assert get(0x7F244) == 1 and get(0xB65E4) == 7
    assert event["event_ID"] == 189 and get(0x23840, owner+4, 189) == 0
    pointer = town.B + owner_at + event["event_record_offset"]
    get(0x23888, town.SCRATCH, owner+4, 189)
    assert unpack("<I", bytes(cpu.mem_read(town.SCRATCH, 4))) == (pointer,)
    loaded = bytes(cpu.mem_read(pointer, 12))
    orig = bytes.fromhex(event["record_hex"])
    assert loaded[4:] == orig[4:] and (unpack_from("<I", loaded)[0] ^ unpack_from("<I", orig)[0]) & ~0xC0008000 == 0
    date_object = town.SCRATCH + 0x80
    get(0xCC9A8, date_object, get(0xCB1B4))
    _, year, month, day, _ = unpack("<5I", bytes(cpu.mem_read(date_object,20)))
    assert [month+1,day+1] == [2,12]
    cpu.mem_write(owner+0x2454, pack("<3I",7,7,0))
    baseline = bytes(cpu.mem_read(town.B, 0x400000))
    cases = []
    for y, m, d, expected in ((year,2,12,0),(year,11,19,0),(year,12,18,0),
                               (year,12,19,1),(year,12,20,1),(year+1,1,19,0),
                               (year+1,12,19,1),(year,12,12,0)):
        cpu.mem_write(date_object+4, pack("<3I",y,m-1,d-1))
        actual = get(0x220D8, owner, pointer, date_object, 0)
        assert actual == expected and bytes(cpu.mem_read(town.B, 0x400000)) == baseline
        cases.append(dict(calendar_year_index=y, month=m, day=d, eligible=bool(actual)))
    selected = [town.read_frame(captures,n)[0] for n in (8000,8300,8640,8980,9300)]
    return dict(city="stockholm", arrival_via_ordinary_navigation=True, Square_opened_on_february_12=True,
                displayed_fur_exchange=False, source_event=event, completion_getter=0, observed=selected,
                offline_cases=cases, offline_only_owner_context_and_date_inputs=True,
                source_snapshot=s, evidence=evidence)


def main():
    assert not OUTPUT.exists()
    active = runs.active
    release = base.load(active.RELEASE)
    sha = base.digest(active.ROM)
    assert sha == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    arm, font = (current.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT"))
    archive = current.read_file("/data/EV1.DK4")
    assert archive == clean.read_file("/data/EV1.DK4")
    event_archive = base.load(town.events.OUTPUT)
    assert native.digest(archive) == event_archive["routes"][1]["archive_sha256"]
    clean_arm = clean.read_file(native.ARM)
    for ref in event_archive["clean_identical_native_dependencies"]:
        a, b = ref["address"] - town.B, ref["end_exclusive"] - town.B
        assert arm[a:b] == clean_arm[a:b] and native.digest(arm[a:b]) == ref["sha256"]
    events = {row["town"]: row for row in event_archive["routes"][1]["entries"]}
    ctx = SimpleNamespace(image=current, arm=arm)
    render, render_fe = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    names = previous.GameAsciiFont.from_arm9(arm)
    path = "/data/SC1.DK4"
    clean_bank, current_bank = [native.IlnkContainer.parse(image.read_file(path)).blocks for image in (clean,current)]
    reviews = base.load(town.REVIEW)["records"]
    results = []
    for city, plan in CASES.items():
        folder, report, captures, evidence = capture_receipt(city, sha)
        assert report["frames"] == plan["returned"]
        block = plan["block"]
        event = events[plan["town"]]
        assert event["script_block"] == block
        control = previous.event_completion(arm, report, archive, event, plan)
        a, b = clean_bank[block], current_bank[block]
        assert native.digest(a) == event["prior_review"]["clean_block_sha256"]
        assert native.digest(b) == event["prior_review"]["current_block_sha256"]
        rows = [r for r in reviews if r["file_path"] == path and r["block"] == block]
        assert len(rows) == event["prior_review"]["records"]
        found, previews = [], []
        for i, row in enumerate(rows):
            source, stored = row["source_reference"], row["registered_reference"]
            for data, ref in ((a,source),(b,stored)):
                offset = ref["command_offset"]
                cmd = bytes.fromhex(ref["complete_command_hex"])
                assert data[offset:offset+len(cmd)] == cmd
            assert all(row["review"].values())
            body = bytes.fromhex(stored["raw_hex"])[1:]
            assert body.isascii()
            selector = row["source_selector"]
            if selector == 254:
                surface = render_fe(body)
                plane, width = surface["physical"],228
            else:
                surface = render(arm,font,body)
                page, = surface["pages"]
                assert page["native_independent_plane_equal"]
                plane,width = bytes.fromhex(page["native_plane_hex"]),216
            assert surface["complete_consumed_bytes"] == len(body)
            frame,image = town.read_frame(captures,plan["first"]+i*plan["step"])
            assert previous.mask_check(plane,width,image),(city,row["id"])
            name = None
            if selector != 254:
                assert selector in (166,167,168)
                count,bounds = previous.complete_mask(names,"Lady",image,16,277,town.INKS[1])
                name=dict(text="Lady", ink_pixels=count,bounds=bounds)
            found.append(dict(id=row["id"], clean_Japanese=row["Japanese"], source_hex=row["source_hex"],
                source_reference=source, registered_reference=stored, english=row["english"],
                original_localization_note=row["localization_note"], five_gates=row["review"], observed=frame,
                observed_native_plane_sha256=native.digest(plane), nameplate=name))
            previews.append((row["id"],image))
        controls={}
        for k in ("opening","ready","entry","returned"):
            controls[k], image = town.read_frame(captures,plan[k])
        previews.append(("Return to the Square",image))
        sheets=[]
        for i in range(0,len(previews),6):
            target=folder/f"complete_exchange_{i//6+1}.png"
            town.sheet(previews[i:i+6],target)
            sheets.append(dict(path=str(target),sha256=base.digest(target)))
        results.append(dict(city=city, natural_activation=True, panels=found, original_event_completion=control,
            calendar_controls=controls, opening_calendar=plan["opening_calendar"], Inn_days=plan["days"],
            sheets=sheets,evidence=evidence))
        print(city,len(found),"complete panels matched",flush=True)
    bound_stockholm=stockholm(sha,arm,archive,events[7])
    base.save(OUTPUT, dict(candidate_sha256=sha, game_activated_original_events=True, new_editorial_credit=0,
        played_with_verified_copies_of_existing_saves=True, hardware_verified=False,
        scene_runs=results, stockholm=bound_stockholm, source_review_sha256=base.digest(town.REVIEW),
        event_map_sha256=base.digest(town.events.OUTPUT)))
    print("Stockholm boundary verified offline after the ordinary February visit.",flush=True)


if __name__ == "__main__":
    main()

