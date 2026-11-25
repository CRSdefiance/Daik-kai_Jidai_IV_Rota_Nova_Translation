"""Verify the revised Stockholm panels in their original gameplay sequences."""
from pathlib import Path
from struct import unpack, unpack_from
from types import SimpleNamespace

from PIL import ImageChops

from scripts import replay_stockholm_dialogue_followup_20261121 as run
from scripts import verify_stockholm_dialogue_display_20261121 as display


base,town,native = display.base,display.town,display.native
PROOF = run.ROOT / "verified_stockholm.json"


def main():
    assert not PROOF.exists()
    staged,offline,before,old_report,report,review = map(base.load,(
        run.stage.PROOF,display.PROOF,run.original.OUTPUT,run.original.REPORT,run.REPORT,run.stage.REBOUND))
    sha = base.digest(run.stage.ROM)
    assert sha == staged["candidate_sha256"] == offline["candidate_sha256"] == report["ROM_sha256"]
    assert base.digest(run.original.REPORT) == before["evidence"][str(run.original.REPORT)]
    assert report["scripted_input_schedule"] == old_report["scripted_input_schedule"] == base.load(run.PLAN)
    assert report["core_options"] == old_report["core_options"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert report["frames"] == old_report["frames"] == run.original.RETURN
    for key in ("source","source_sha256","copied_byte_exact_before_cold_boot"):
        assert report["battery_save_preloaded"][key] == old_report["battery_save_preloaded"][key]

    image = base.NdsImage.open(run.stage.ROM)
    arm,font,archive = (image.read_file(p) for p in (native.ARM,"/GRP/KANJI.FNT",run.original.EVENT_PATH))
    current = SimpleNamespace(image=image,arm=arm)
    painter,system = town.clipped_renderer(current),town.current_fe_painter(current)
    source = report["read_only_RAM_snapshot"]
    raw = Path(source["path"]).read_bytes()
    assert len(raw) == 0x400000 and source["read_only_export"] and base.digest(source["path"]) == source["sha256"]
    at = raw.index(archive[:96])
    assert raw.find(archive[:96],at+1) == -1
    cpu,get = town.get_machine(arm,raw)
    owner = town.B+at-0x34
    assert get(0x7F244)==1 and get(0xB65E4)==7 and get(0x23840,owner+4,189)==1
    get(0x23888,town.SCRATCH,owner+4,189)
    location = town.B+at+before["source"]["event_record_offset"]
    assert unpack("<I",bytes(cpu.mem_read(town.SCRATCH,4))) == (location,)
    proof_hex = bytes.fromhex(before["exact_loaded_event_hex"])
    assert bytes(cpu.mem_read(location,len(proof_hex))) == proof_hex
    get(0xCC9A8,town.SCRATCH,get(0xCB1B4))
    _,y,m,d,_ = unpack("<5I",bytes(cpu.mem_read(town.SCRATCH,20)))
    assert [y,m+1,d+1] == [0,12,19]
    assert bytes(cpu.mem_read(town.B,0x400000)) == raw

    checks = {row["id"]:row for row in offline["records"] if row["decision"]=="revision"}
    frames = {row["frame"]:row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    final, = (row for row in report["frames_captured"] if row["path"].endswith("_final.png"))
    assert final["frame"] == run.original.RETURN
    frames.setdefault(final["frame"],final)
    ready = {row["observed"]["frame"]:row["observed"] for row in before["complete_fur_exchange"]}
    ready.update({row["frame"]:row for row in before["separate_Tavern_tutorial_frames"]})
    control = set(run.CONTROL_FRAMES)-ready.keys()
    ready.update({row["frame"]:row for row in before["calendar_and_voyage_holds"] if row["frame"] in control})
    ready[run.original.RETURN] = before["Square_return"]
    edits = {row["previous_capture"]["frame"]:row for row in review["records"] if row["decision"]=="revision"}
    assert len(edits)==3 and set(edits)<=ready.keys()
    confirmed,unchanged,previews = [],[],[]
    for number, old_shot in sorted(ready.items()):
        shot,panel = town.read_frame(frames,number)
        if number not in edits:
            assert old_shot["framebuffer_sha256"] == shot["framebuffer_sha256"],number
            unchanged.append(shot)
            continue
        row = edits[number]
        ident = row["id"]
        result = checks[ident]
        cmd = bytes.fromhex(result["stored_command_hex"])
        at = result["stored_offset"]
        data = native.IlnkContainer.parse(image.read_file(row["file_path"])).blocks[row["block"]]
        assert data[at:at+len(cmd)]==cmd
        body = cmd[6:cmd.index(0,6)]
        if row["source_selector"]==254:
            rendered = system(body)
            plane,width = rendered["physical"],228
        else:
            rendered = painter(arm,font,body)
            page, = rendered["pages"]
            assert page["native_independent_plane_equal"]
            plane,width = bytes.fromhex(page["native_plane_hex"]),216
        assert rendered["complete_consumed_bytes"]==len(body) and native.digest(plane)==result["plane_sha256"]
        assert run.original.proof.mask_check(plane,width,panel),ident
        _,old = town.read_frame({number:old_shot},number)
        delta = ImageChops.difference(old,panel)
        delta.paste((0,0,0),(16,296,244,360))
        assert delta.getbbox() is None,ident
        confirmed.append(dict(id=ident,file_path=row["file_path"],frame=number,
            prior=old_shot,revised=shot,all_glyphs_and_external_pixels_match=True))
        previews.extend(((ident+" before",old),(ident+" revised",panel)))
    assert len(confirmed)==3 and len(unchanged)==16
    sheet=run.ROOT/"stockholm_before_after_gameplay.png"
    town.sheet(previews,sheet)
    base.save(PROOF,dict(candidate_sha256=sha,holds=confirmed,unchanged_controls=unchanged,
        natural_activation=True,exact_native_glyph_matches=True,original_notice_dismissal_and_Square_return=True,
        date=[12,19],original_completion_flag=1,exercised_Tavern_choice=0,hardware_verified=False,
        snapshot=source,sheets=[dict(path=str(sheet),sha256=base.digest(sheet))],
        evidence={str(p):base.digest(p) for p in (run.PLAN,run.REPORT,run.original.OUTPUT,display.PROOF)}))
    print("Three changed panels and sixteen exact control holds passed. The December event completes normally.")


if __name__ == "__main__":
    main()
