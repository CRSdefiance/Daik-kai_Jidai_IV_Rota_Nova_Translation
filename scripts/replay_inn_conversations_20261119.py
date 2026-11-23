"""Verify the revised Inn price and normal stay and choice transitions in Istanbul."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_hostess_conversations_20261119 as boot
from scripts import replay_square_label_wording_20261119 as patch_workflow
from scripts import stage_inn_conversations_20261119 as stage
from scripts.observe_setup_save_common_v1 import scoped_observer

base = stage.base
PLAN = Path("work/analysis/inn_actual_v2253/run_plan.json")
CAPTURE = stage.ROOT/"istanbul"
PLAYBACK = stage.ROOT/"verified_istanbul_inn.json"
STARTUP = stage.ROOT/"own_startup"
STARTUP_PROOF = stage.ROOT/"own_startup_verification.json"
HOLDS = {4800:1177,5200:1178,6200:1179,7000:1180,7400:1181}


def schedule(case):
    assert case=="istanbul"
    plan = base.load(PLAN)
    inputs = Path(plan["inputs"])
    assert base.digest(inputs)==plan["inputs_sha256"]
    source = Path(plan["prior_report"])
    assert base.digest(source)==plan["prior_report_sha256"]
    history = base.load(source)
    donor = history["battery_save_preloaded"]
    assert Path(donor["source"])==Path(plan["original_genuine_save"])
    assert base.digest(donor["source"])==donor["source_sha256"]==plan["donor_sha256"]
    inputs = base.load(inputs)
    assert inputs==history["scripted_input_schedule"]
    return inputs,plan["captures"][3:],plan["configured_maximum_frames"],source,donor


def capture():
    assert not CAPTURE.exists()
    scope = vars(playback)|dict(ROOT=stage.ROOT,parent=SimpleNamespace(ROM=stage.ROM,RELEASE=stage.PROOF),
        observer=scoped_observer,get_schedule=schedule,FOCUS=set(range(1177,1200)),__file__=__file__)
    exec(compile(getsource(playback.main),__file__+"::ordinary_Istanbul", "exec"),scope)
    scope["main"]("istanbul")


def startup():
    run = boot.boot.boot_replay.previous.startup
    FunctionType(run.__code__,run.__globals__|{"stage":stage,"STARTUP":STARTUP})()
    verify_startup()


def verify_startup():
    scope = vars(boot)|globals()|{"boot":boot.boot}
    FunctionType(boot.verify_startup.__code__,scope)()


def patch():
    FunctionType(patch_workflow.patch.__code__,vars(patch_workflow)|globals())()


def verify():
    assert not PLAYBACK.exists()
    paths = [CAPTURE/p for p in ("capture/capture_report.json","requests.json","terminal.json","inputs.json")]
    report,trace,terminal,inputs = map(base.load,paths)
    events,frames,end,source,donor = schedule("istanbul")
    candidate = base.digest(stage.ROM)
    assert report["ROM_sha256"]==terminal["ROM_sha256"]==candidate
    assert report["frames"]==terminal["completed_frames"]==end
    assert report["scripted_input_schedule"]==events==inputs
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"] and battery["source"]==donor["source"]
    assert base.digest(donor["source"])==battery["source_sha256"]==donor["source_sha256"]
    history = base.load(source)
    assert history["core_options"]==report["core_options"]
    shots = {r["frame"]:r for r in report["frames_captured"]}
    old = {r["frame"]:r for r in history["frames_captured"]}
    assert set(shots)==set(frames)|{1,60,180,end}
    requests = [r for r in trace["source_requests"] if r["PC"]==0x0205528C]
    assert [r["message_ID"] for r in requests if r["message_ID"] in HOLDS.values()]==list(HOLDS.values())
    reviewed = {r["message_ID"]:r for r in base.load(stage.PROOF)["records"]}
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    raster,independent,_ = stage.physical_renderers(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    evidence = {str(p):base.digest(p) for p in (*paths,source,PLAN)}
    canvas = Image.new("RGB",(768,210*2),"#263238")
    draw = ImageDraw.Draw(canvas)
    holds = []
    for i,(frame,n) in enumerate((*HOLDS.items(),(8600,None))):
        path = shots[frame]["path"]
        assert base.digest(path)==shots[frame]["PNG_sha256"]
        evidence[path] = shots[frame]["PNG_sha256"]
        with Image.open(path) as opened:
            img = opened.convert("RGB")
        x,y = i%3*256,i//3*210
        canvas.paste(img.crop((0,192,256,384)),(x,y+16))
        draw.text((x+3,y+2),f"{frame}  {'town return' if n is None else n}",fill="white")
        if n is None:
            continue
        request = max((r for r in requests if r["frame"]<frame),key=lambda r:r["frame"])
        assert 0<frame-request["frame"]<400 and request["message_ID"]==n
        args = ["３".encode("cp932").hex()] if n==1180 else []
        case, = (c for c in reviewed[n]["layout_cases"] if c["source_values_hex"]==args)
        raw = bytes.fromhex(case["formatted_hex"])
        plane,used = raster(arm,raw,0x01FFCE40-0x02000000,size=(228,64),complete=False,instruction_limit=2000000)
        assert used==len(raw) and plane==independent(arm,kanji,case["lines"])
        actual = {(x,y) for y in range(294,360) for x in range(16,244) if img.getpixel((x,y))==(0,8,0)}
        expected = {(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
        assert actual==expected,(n,len(actual),len(expected))
        holds.append(dict(frame=frame,message_ID=n,source_request=request,lines=case["lines"],complete_visible_ink=len(actual)))
    # The original and new runs arrive at the same town screen after both stays.
    for f in (3200,4000,4400,5600,5800,6600,7800,8200,8600):
        assert shots[f]["framebuffer_sha256"]==old[f]["framebuffer_sha256"], f
    sheet = stage.ROOT/"verified_istanbul_inn.png"
    canvas.save(sheet)
    evidence[str(sheet)] = base.digest(sheet)
    base.save(PLAYBACK,dict(candidate_sha256=candidate,ordinary_inputs=True,used_existing_battery_save=True,
        savestate=False,hardware=False,normal_town_return=True,holds=holds,observed_revised_IDs=[1179],
        exact_previous_transition_frames=[3200,4000,4400,5600,5800,6600,7800,8200,8600],
        sheets=[dict(path=str(sheet),sha256=base.digest(sheet))],evidence=evidence))
    print("Verified five Inn holds, the revised price, and the return to Istanbul.")


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","startup","verify_startup","patch","verify"))
    globals()[parser.parse_args().action]()
