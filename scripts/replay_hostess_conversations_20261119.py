"""Replay Lisbon's Tavern with ordinary inputs and check the staged candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts import observe_lisbon_voyage_and_osaka_20261115 as lisbon
from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_deck_comments_20261119 as boot
from scripts import replay_square_label_wording_20261119 as patch_workflow
from scripts import stage_hostess_conversations_20261119 as stage
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

base = stage.base
STARTUP = stage.ROOT / "own_startup"
STARTUP_PROOF = stage.ROOT / "own_startup_verification_v2.json"
CAPTURE = stage.ROOT / "lisbon"
FOLLOWUP = stage.ROOT / "lisbon_followup"
PLAYBACK = stage.ROOT / "verified_lisbon_hostess.json"


def schedule(case):
    events, _, _, source, donor = lisbon.schedule("lisbon")
    events = [r for r in events if r["start"] <= 2801]
    events.append(dict(start=3201, duration=8, buttons=[], touch=[80, 29]))
    keys = ("A", "A", "A", "B", "A", "B", "A", "A", "A", "B", "A", "B", "B", "B", "B")
    events.extend(dict(start=3601 + 400*i, duration=8, buttons=[key]) for i, key in enumerate(keys))
    if case == "lisbon_followup":
        followup = ("A",)*29 + ("B",)*10
        events.extend(dict(start=9601 + 240*i, duration=8, buttons=[key]) for i, key in enumerate(followup))
    end = events[-1]["start"] + 400
    frames = [3200, *(r["start"] + 199 for r in events[4:]), end-51]
    return events, frames, end, source, donor


def capture(case="lisbon"):
    assert not (stage.ROOT / case).exists()
    scope = vars(playback) | dict(ROOT=stage.ROOT, parent=SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF),
        observer=scoped_observer, get_schedule=schedule, FOCUS=set(range(989, 1020)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary_tavern", "exec"), scope)
    scope["main"](case)


def followup():
    capture("lisbon_followup")


def startup():
    run = boot.boot_replay.previous.startup
    FunctionType(run.__code__, run.__globals__ | {"stage":stage,"STARTUP":STARTUP})()
    verify_startup()


def verify_startup():
    assert not STARTUP_PROOF.exists()
    previous = base.load(stage.parent.RELEASE)
    basis = base.load(STARTUP / "basis.json")
    assert base.digest(basis["previous_report"]) == basis["previous_report_sha256"]
    assert base.digest(basis["manifest"]) == basis["manifest_sha256"]
    proof = checked_text(getsource(boot.boot_audit.verify_startup), {
        "ROOT / 'own_startup/capture/capture_report.json'": "REPORT",
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR_REPORT",
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": "",
        "proof['registered_input']['candidate_sha256']": "proof['parent_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": "PRIOR_BOOT",
    })
    scope = vars(boot.boot_audit) | dict(ROM=stage.ROM, PROOF=stage.PROOF, BOOT=STARTUP_PROOF,
        REPORT=STARTUP/"capture/capture_report.json", PRIOR_REPORT=Path(basis["previous_report"]),
        PRIOR_BOOT=Path(previous["own_registered_startup"]), __file__=__file__)
    exec(compile(proof, __file__ + "::startup", "exec"), scope)
    scope["verify_startup"]()


def patch():
    FunctionType(patch_workflow.patch.__code__, vars(patch_workflow) | globals())()


def verify():
    assert not PLAYBACK.exists()
    paths = [FOLLOWUP / p for p in ("capture/capture_report.json", "requests.json", "terminal.json", "inputs.json")]
    report, trace, terminal, inputs = map(base.load, paths)
    events, frames, end, source, donor = schedule("lisbon_followup")
    candidate = base.digest(stage.ROM)
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == candidate
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["scripted_input_schedule"] == events == inputs
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"] and battery["source"] == donor["source"]
    assert base.digest(donor["source"]) == battery["source_sha256"] == donor["source_sha256"]
    proof = base.load(stage.PROOF)
    reviewed = {r["message_ID"]: r for r in proof["records"]}
    expected = {827: ["Ah, Hodram? Here's to meeting you!"]}
    expected.update({n: reviewed[n]["layout_cases"][0]["lines"] for n in stage.EDITS})
    original = {n for n in range(989,1020) if n not in stage.EDITS} | {827}
    eligible = set(expected) | original
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    shots = {r["frame"]:r for r in report["frames_captured"]}
    assert set(shots) == set(frames) | {1,60,180,end}
    rows = [r for r in trace["source_requests"] if r["PC"] == 0x0205528C]
    evidence = {str(path):base.digest(path) for path in (*paths,source)}

    def screen(frame):
        p = shots[frame]["path"]
        assert base.digest(p) == shots[frame]["PNG_sha256"]
        evidence[p] = shots[frame]["PNG_sha256"]
        with Image.open(p) as opened:
            return opened.convert("RGB")

    holds, captures = [], []
    for frame in frames[1:]:
        recent = [r for r in rows if 0 < frame-r["frame"] <= 210]
        if not recent or recent[-1]["message_ID"] not in eligible:
            continue
        request = recent[-1]
        n = request["message_ID"]
        img = screen(frame)
        if n in expected:
            options = [expected[n]]
        else:
            options = [c["lines"] for c in reviewed[n]["layout_cases"] if all(line.isascii() for line in c["lines"])]
        for lines in options:
            try:
                ink, bounds = complete_mask(font, "Julia", img, 16, 277, (98,97,98))
                body = body_mask(img,font,lines)
            except (ValueError, AssertionError):
                continue
            holds.append(dict(frame=frame, message_ID=n, source_request=request, complete_nameplate="Julia",
                name_pixels=ink, name_bounds=bounds, body=body, revised=n in stage.EDITS))
            captures.append((frame,img))
            break
    assert [(r["frame"],r["message_ID"]) for r in holds] == [(7000,827),(10040,992),(11960,992),(15800,992)]
    restored, original_town = screen(end), screen(3200)
    assert restored.crop((0,0,256,192)).tobytes() == original_town.crop((0,0,256,192)).tobytes()
    town_after_dismissal = screen(17960)
    footer = (154,368,256,384)
    assert restored.crop(footer).tobytes() == town_after_dismissal.crop(footer).tobytes()
    assert restored.tobytes() == screen(18200).tobytes() == screen(19070).tobytes()
    captures.append((end,restored))
    sheet = stage.ROOT / "verified_lisbon_tavern.png"
    canvas = Image.new("RGB",(512,211*((len(captures)+1)//2)),"#263238")
    draw = ImageDraw.Draw(canvas)
    for i,(frame,img) in enumerate(captures):
        x,y = i%2*256,i//2*211
        draw.text((x+4,y+2), f"Frame {frame}", fill="white")
        canvas.paste(img.crop((0,192,256,384)),(x,y+17))
    canvas.save(sheet)
    evidence[str(sheet)] = base.digest(sheet)
    pending = {r["message_ID"] for r in base.load(stage.PENDING)["records"]}
    pending_calls = [r for r in rows if r["message_ID"] in pending]
    base.save(PLAYBACK,dict(candidate_sha256=candidate,ordinary_inputs=True,used_existing_battery_save=True,
        savestate=False,hardware=False,normal_town_return=True,return_frame=end,hostess_holds=holds,
        observed_revised_IDs=sorted({r["message_ID"] for r in holds if r["revised"]}),
        unvisited_reviewed_IDs=sorted(set(reviewed)-{r["message_ID"] for r in holds}),
        pending_shared_requests=pending_calls,sheets=[dict(path=str(sheet),sha256=base.digest(sheet))],evidence=evidence))
    print([(r["frame"],r["message_ID"]) for r in holds], "and return to Lisbon verified.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "followup", "startup", "verify_startup", "patch", "verify"))
    globals()[parser.parse_args().action]()
