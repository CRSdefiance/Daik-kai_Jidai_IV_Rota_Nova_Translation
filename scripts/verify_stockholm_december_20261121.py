"""Verify the full Stockholm Square exchange opened during ordinary December play."""
from pathlib import Path
from struct import unpack, unpack_from
from types import SimpleNamespace

from scripts import replay_stockholm_december_20261121 as replay
from scripts import register_seville_stockholm_trends_20261121 as prior
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as proof


base, native, town = proof.base, proof.native, proof.town
ROOT = replay.ROOT / "riga"
REPORT = ROOT / "capture/capture_report.json"
OUTPUT = town.events.BOOK / "stockholm_december_gameplay_20261121_v1.json"
FIRST, STEP, RETURN = 47790, 310, 50270
PATH, EVENT_PATH, BLOCK = "/data/SC1.DK4", "/data/EV1.DK4", 189


def main():
    assert not OUTPUT.exists()
    release = base.load(replay.active.RELEASE)
    candidate = base.digest(replay.active.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    report = base.load(REPORT)
    assert report["ROM_sha256"] == candidate and report["frames"] == RETURN
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    journal = ROOT / "capture/navigation_command_journal.json"
    commands = base.load(journal)["commands_received"]
    assert all(row["validation_passed"] for row in commands)
    image, clean = map(base.NdsImage.open,(replay.active.ROM,native.CLEAN))
    arm, font, events = (image.read_file(path) for path in (native.ARM,"/GRP/KANJI.FNT",EVENT_PATH))
    assert events == clean.read_file(EVENT_PATH)
    event, = [e for e in base.load(town.events.OUTPUT)["routes"][1]["entries"] if e["town"] == 7]
    assert event["event_ID"] == event["script_block"] == BLOCK
    snap = report["read_only_RAM_snapshot"]
    raw = Path(snap["path"]).read_bytes()
    assert snap["read_only_export"] and len(raw)==0x400000 and base.digest(snap["path"])==snap["sha256"]
    at = raw.index(events[:96])
    assert raw.find(events[:96], at + 1) == -1
    owner = town.B + at - 0x34
    cpu, get = town.get_machine(arm,raw)
    assert get(0x7F244) == 1 and get(0xB65E4) == 7
    descriptor = list(unpack("<3I",bytes(cpu.mem_read(owner+0x2454,12))))
    assert descriptor == [event[k] for k in ("category","town","facility")] == [7,7,0]
    get(0xCC9A8,town.SCRATCH,get(0xCB1B4))
    _,year,month,day,_ = unpack("<5I",bytes(cpu.mem_read(town.SCRATCH,20)))
    assert (year,month,day)==(0,11,18)
    assert get(0x23840,owner+4,BLOCK)==1
    get(0x23888,town.SCRATCH,owner+4,BLOCK)
    pointer = town.B + at + event["event_record_offset"]
    assert unpack("<I",bytes(cpu.mem_read(town.SCRATCH,4))) == (pointer,)
    source_event = bytes.fromhex(event["record_hex"])
    runtime_event = bytes(cpu.mem_read(pointer,len(source_event)))
    assert runtime_event[4:]==source_event[4:]
    assert unpack_from("<I",runtime_event)[0]^unpack_from("<I",source_event)[0]==0xC0008000
    assert bytes(cpu.mem_read(town.B,0x400000)) == raw

    japanese,english = [native.IlnkContainer.parse(rom.read_file(PATH)).blocks[BLOCK] for rom in (clean,image)]
    assert native.digest(japanese) == event["prior_review"]["clean_block_sha256"]
    assert native.digest(english) == event["prior_review"]["current_block_sha256"]
    rows = [row for row in base.load(prior.REVIEW)["records"] if row["file_path"]==PATH and row["block"]==BLOCK]
    assert len(rows) == event["prior_review"]["records"] == 8
    context = SimpleNamespace(image=image,arm=arm)
    render, system = town.clipped_renderer(context), town.current_fe_painter(context)
    names = proof.GameAsciiFont.from_arm9(arm)
    frames = {row["frame"]:row for row in report["frames_captured"] if row["path"].endswith("_navigation.png")}
    held, previews = [], []
    for i,row in enumerate(rows):
        source, installed = row["source_reference"], row["registered_reference"]
        orig, current = bytes.fromhex(row["source_hex"]), bytes.fromhex(installed["exact_stored_hex"])
        for bank, ref, body in ((japanese,source,orig),(english,installed,current)):
            start, offset = ref["command_offset"], ref["offset"]
            assert offset == start + 5 and bank[start:start+5] == b"\0\x40\xff\xff\0"
            assert bank[offset:offset+len(body)+1] == body + b"\0"
        selector = row["source_selector"]
        assert current[0] == orig[0] == selector and current[1:].isascii() and all(row["review"].values())
        shot,panel = town.read_frame(frames,FIRST+i*STEP)
        nameplate = None
        if selector == 254:
            draw = system(current[1:])
            plane,width = draw["physical"],228
        else:
            draw = render(arm,font,current[1:])
            page, = draw["pages"]
            assert page["native_independent_plane_equal"]
            plane,width = bytes.fromhex(page["native_plane_hex"]),216
            count,bounds = proof.complete_mask(names,row["speaker"],panel,16,277,town.INKS[1])
            nameplate = dict(text=row["speaker"],ink_pixels=count,bounds=bounds)
        assert draw["complete_consumed_bytes"] == len(current) - 1
        assert proof.mask_check(plane,width,panel),row["id"]
        held.append(dict(id=row["id"],Japanese=row["Japanese"],english=row["english"],source_reference=source,
            current_reference=installed | {"archive_sha256":native.digest(image.read_file(PATH)),
                                            "current_ROM_sha256":candidate},five_gates=row["review"],
            observed=shot,native_mask_sha256=native.digest(plane),nameplate=nameplate))
        previews.append((row["id"],panel))
    return_frame,panel = town.read_frame(frames,RETURN)
    previews.append(("Return to the Stockholm Square",panel))
    sheets = []
    for i in range(0,len(previews),6):
        sheet = ROOT / f"fur_exchange_{i//6+1}.png"
        town.sheet(previews[i:i+6],sheet)
        sheets.append(dict(path=str(sheet),sha256=base.digest(sheet)))
    # Includes the complete recorded recruitment choice, lesson and Tavern return.
    tutorial_frames = (8640,8950,9260,9570,9880,10190,10500)
    tutorial = [town.read_frame(frames,n)[0] for n in tutorial_frames]
    rests = [15650,*range(18880,44721,3230),46860]
    holds = [town.read_frame(frames,n)[0] for n in (8000,*rests,47160,47460)]
    base.save(OUTPUT, dict(candidate_sha256=candidate, ordinary_gameplay=True, hardware_verified=False,
        complete_fur_exchange=held, Square_return=return_frame, route=1, source=event, completion_getter=1,
        observed_game_date=[12,19], exact_loaded_event_hex=runtime_event.hex(), calendar_and_voyage_holds=holds,
        Inn_nights=310, snapshot=snap, separate_Tavern_tutorial_frames=tutorial, sheets=sheets,
        evidence={str(p):base.digest(p) for p in (REPORT,journal,prior.REVIEW,town.events.OUTPUT)},
        prior_editorial_coverage_retained=True,new_editorial_credit=0))
    print("All eight fur panels, Man/Woman nameplates, December 19 availability and the Square return matched.")


if __name__ == "__main__":
    main()
