"""Revisit the Hangzhou briefing through ordinary controls on the staged cumulative ROM."""

from argparse import ArgumentParser
from inspect import getsource
from types import SimpleNamespace

from scripts import observe_hangzhou_early_actual_20261122 as prior
from scripts import verify_hangzhou_early_actual_20261122 as prior_check
from scripts import verify_maria_hangzhou_followup_20261122 as display
from scripts import stage_maria_hangzhou_followup_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base=stage.base
ROOT=stage.ROOT/"ordinary_hangzhou"
REPORT=ROOT/"hangzhou/capture/capture_report.json"
PROOF=ROOT/"hangzhou_briefing_gameplay.json"


def capture():
    playback=prior.playback
    program=checked_text(getsource(playback.main),{
        "    release = base.load(parent.RELEASE)":"    release = base.load(stage.PROOF)",
    })
    scope=vars(playback)|globals()|dict(parent=SimpleNamespace(ROM=stage.ROM),observer=prior.scoped_observer,
        get_schedule=prior.schedule,FOCUS={704})
    exec(compile(program,__file__+"::Hangzhou-ordinary-inputs","exec"),scope)
    scope["main"]("hangzhou")


def verify():
    from PIL import Image, ImageDraw

    assert not PROOF.exists()
    terminal_path, requests_path = REPORT.parent.parent/"terminal.json", REPORT.parent.parent/"requests.json"
    report, term, requests, shown, staged = map(base.load,(REPORT,terminal_path,requests_path,display.PROOF,stage.PROOF))
    expected, _, end, _, donor=prior.schedule("hangzhou")
    assert report["ROM_sha256"] == shown["candidate_sha256"] == staged["candidate_sha256"] == base.digest(stage.ROM)
    assert term["ROM_sha256"] == report["ROM_sha256"] and report["frames"] == term["completed_frames"] == end
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == expected and report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert requests["all_host_slots_restored_and_core_file_exact"] and not requests["errors"] and not requests["mismatches"]
    assert all(base.digest(path)==digest for path,digest in term["evidence"].items())
    scopes = [call for call in requests["source_requests"] if call["frame"]>31000]
    assert len(scopes)==len(prior_check.SAMPLES)*2
    current=base.NdsImage.open(stage.ROM)
    arm=current.read_file(stage.native.ARM)
    font=prior_check.GameAsciiFont.from_arm9(arm)
    payload=prior_check.shared.entries(current)
    snapshots=prior_check.shots(report)
    old=prior_check.shots(base.load(prior_check.ROOT/"capture/capture_report.json"))
    code=checked_text(getsource(prior_check.body_mask),{"range(297, 345, 16)":"range(297, 361, 16)"})
    scope=prior_check.body_mask.__globals__.copy()
    exec(compile(code,__file__+"::all-four-visible-lines","exec"),scope)
    complete=scope["body_mask"]
    panels=[]
    for (frame,key,facility),lookup,copy in zip(prior_check.SAMPLES,scopes[::2],scopes[1::2],strict=True):
        assert [lookup["PC"],copy["PC"]] == [0x0205528C,0x020534F4]
        assert lookup["message_ID"] == copy["message_ID"] == key
        assert lookup["frame"] == copy["frame"] < frame
        lines,role,_ = prior_check.WORDING[key]
        image=prior_check.captured(snapshots[frame])
        if key==stage.shared.KEY:
            lines=shown["briefing"]["lines"]
        else:
            assert snapshots[frame]["framebuffer_sha256"] == old[frame]["framebuffer_sha256"]
        assert " ".join(payload[key].text.decode("ascii").split())==" ".join(lines)
        mask=complete(image,font,lines)
        assert len(mask)==len(lines)
        pixels,bounds=prior_check.complete_mask(font,role,image,16,277,(98,97,98))
        panels.append(dict(frame=frame,message_ID=key,facility=facility,observed_lines=lines,
            exact_body=mask,nameplate=dict(text=role,pixels=pixels,bounds=bounds),
            request=lookup,capture=snapshots[frame]))
    returns=[snapshots[n] for n in (36350,36750,37150)]
    for end_state in returns:
        assert end_state["framebuffer_sha256"]==old[end_state["frame"]]["framebuffer_sha256"]
    key,= [r for r in panels if r["message_ID"]==stage.shared.KEY]
    sheet=Image.new("RGB",(1024,410),"#243139")
    label=ImageDraw.Draw(sheet)
    for n,(caption,frame) in enumerate((("Hangzhou Luxury Shop briefing",key["capture"]),("Return to shop",returns[0]))):
        image=prior_check.captured(frame).crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
        sheet.paste(image,(n*512,20))
        label.text((n*512+4,3),caption,fill="white")
    shot=ROOT/"hangzhou_briefing_and_return.png"
    sheet.save(shot)
    base.save(PROOF,dict(candidate_sha256=report["ROM_sha256"],native_report_sha256=base.digest(display.PROOF),
        report_sha256=base.digest(REPORT),panels=panels,observed_unchanged_menu_returns=returns,
        changed_record=key,ordinary_facility_navigation=True,prepared_existing_unlock_only=True,
        sheets=[dict(path=str(shot),sha256=base.digest(shot))],hardware=False))
    print("Verified all four Hangzhou briefing rows, five exact neighboring holds, and three menu returns.")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","verify"),default="capture",nargs="?")
    globals()[parser.parse_args().action]()

