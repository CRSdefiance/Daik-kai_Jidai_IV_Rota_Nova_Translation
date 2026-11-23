"""Check revised Square labels in ordinary Lisbon gameplay and the cumulative boot."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_deck_comments_20261119 as boot
from scripts import replay_lisbon_shopkeeper_20261119 as lisbon
from scripts import stage_square_label_wording_20261119 as stage
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.verify_captain_biographies_v1 import captured, shots

base = stage.base
STARTUP = stage.ROOT / "own_startup"
STARTUP_PROOF = stage.ROOT / "own_startup_verification.json"
GAME = stage.ROOT / "lisbon"
GAME_PROOF = stage.ROOT / "verified_lisbon_captions.json"
GAME_SHEET = stage.ROOT / "lisbon_caption_comparison.png"


def startup():
    FunctionType(boot.startup.__code__, vars(boot) | globals())()


def capture():
    assert not GAME.exists()
    context = {"ROM": stage.ROM, "RELEASE": stage.PROOF}
    pending = {r["message_ID"] for r in base.load(stage.parent.stage.PENDING)["records"]}
    scope = vars(playback) | dict(ROOT=stage.ROOT, parent=type("Staged", (), context), observer=scoped_observer,
        get_schedule=lisbon.schedule, FOCUS=pending, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::lisbon", "exec"), scope)
    scope["main"]("lisbon")


def verify():
    assert not GAME_PROOF.exists()
    staged = base.load(stage.PROOF)
    previous_proof = base.load(lisbon.PROOF)
    assert previous_proof["candidate_sha256"] == staged["parent_sha256"] == base.digest(stage.parent.ROM)
    candidate = staged["candidate_sha256"]
    assert base.digest(stage.ROM) == candidate
    inputs, frames, end, _, donor = lisbon.schedule("lisbon")
    report_path, trace_path, end_path = ("capture/capture_report.json", "requests.json", "terminal.json")
    paths = tuple(folder / p for folder in (lisbon.FOLDER, GAME) for p in (report_path, trace_path, end_path))
    old, old_trace, prior, new, new_trace, after = map(base.load, paths)
    assert old["ROM_sha256"] == prior["ROM_sha256"] == staged["parent_sha256"]
    assert new["ROM_sha256"] == after["ROM_sha256"] == candidate
    assert prior["completed_frames"] == after["completed_frames"] == old["frames"] == new["frames"] == end
    assert old["scripted_input_schedule"] == new["scripted_input_schedule"] == inputs
    assert old["core_options"] == new["core_options"] and old["core_DLL_sha256"] == new["core_DLL_sha256"]
    assert old_trace["source_requests"] == new_trace["source_requests"] and len(new_trace["source_requests"]) == 10
    assert after["target_COMMON_calls"] == []
    for report, trace in ((old, old_trace), (new, new_trace)):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
        battery = report["battery_save_preloaded"]
        assert battery["source_sha256"] == base.digest(donor["source"]) == donor["source_sha256"]
        assert battery["copied_byte_exact_before_cold_boot"]
        assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    old_shots, new_shots = map(shots,(old,new))
    assert set(old_shots) == set(new_shots) == set(frames) | {1, 60, 180, end}
    evidence = {str(p): base.digest(p) for p in (*paths, lisbon.PROOF)}
    revised, exact = [], []
    regions = [stage.prior.caption_box(i) for i in (0,2)]
    for frame in sorted(new_shots):
        a,b = (captured(r[frame]) for r in (old_shots,new_shots))
        diff = ImageChops.difference(a,b)
        bounds = diff.getbbox()
        if bounds:
            for box in regions:
                diff.paste((0,0,0),box)
            assert diff.getbbox() is None, (frame,diff.getbbox())
            revised.append(dict(frame=frame, differences_in_caption_regions_only=True, bounds=bounds))
        else:
            exact.append(frame)
        evidence.update({row[frame]["path"]: row[frame]["PNG_sha256"] for row in (old_shots,new_shots)})
    assert revised and {3200,3720,9550,end} <= set(exact)

    font = stage.prior.GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    sheet = Image.new("RGB",(1024,384),"#263238")
    draw = ImageDraw.Draw(sheet)
    masks = []
    for j,(side,data,names) in enumerate((
        ("Previous",old_shots,("Cond. Shop","Treats Shop","Fiber Shop","Crafts Shop")),
        ("Revised",new_shots,("Seasonings","Treats Shop","Textile Shop","Crafts Shop")),
    )):
        frame = captured(data[4750])
        for i,name in enumerate(names):
            masks.append(dict(side=side, frame=4750, **stage.prior.live_caption(font,frame,i,name)))
        draw.text((512*j+6,3),f"{side} / Lisbon Square",fill="white")
        crop = frame.crop((0,194,256,375))
        sheet.paste(crop.resize((512,362),Image.Resampling.NEAREST),(512*j,19))
    sheet.save(GAME_SHEET)
    sha = base.digest(GAME_SHEET)
    evidence[str(GAME_SHEET)] = sha
    base.save(GAME_PROOF,dict(candidate_sha256=candidate, prior_sha256=staged["parent_sha256"],
        ordinary_lisbon_existing_save=True, native_full_caption_masks=masks,
        revised_pixel_frames=revised, unchanged_frames=exact, returned_to_lisbon_frame=9550,
        all_dialogue_requests_exact=True, no_pending_shared_requests=True, hardware=False,
        sheets=[dict(path=str(GAME_SHEET),sha256=sha)], evidence=evidence))
    print(f"Verified both complete Lisbon captions and {len(revised)} frame differences confined to the two label fields.")


def patch():
    delta, rebuilt = stage.ROOT / "clean_input.xdelta", stage.ROOT / "clean_rebuilt.nds"
    assert not delta.exists() and not rebuilt.exists()
    make_xdelta(stage.CLEAN,stage.ROM,delta)
    apply_xdelta(stage.CLEAN,delta,rebuilt)
    assert rebuilt.read_bytes() == stage.ROM.read_bytes()
    print("Clean-input round trip is byte-exact.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("startup","capture","verify","patch"))
    globals()[parser.parse_args().action]()
