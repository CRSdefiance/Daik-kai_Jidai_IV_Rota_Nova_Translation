"""Check the two revised Online cards, an unchanged neighbor, and the title return."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from scripts import stage_online_card_copy_20261123 as stage
from scripts import stage_rafael_deck_tutorial_followup_20261122 as release_tools


base, native, parent, proof = stage.base, stage.native, stage.parent, stage.review
ROOT = stage.ROOT
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
OUT, SHEET = ROOT / "verified_playback.json", ROOT / "checked_card_playback.png"


def schedule(case):
    assert case in ("highlights", "highlights_parent")
    original, _, _, source, donor = proof.live.schedule("online")
    events = original[:6] + [dict(start=t, duration=8, buttons=[key]) for t, key in (
        (2100,"DOWN"), (2300,"DOWN"), (2500,"DOWN"), (2700,"A"), (3700,"R"),
        (4700,"R"), (5700,"B"), (6000,"B"), (6300,"B"))]
    return events, [2890, 3890, 4075, 4890, 5075, 5260, 6499], 6600, source, donor


def replay(case="highlights"):
    doc = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == doc["candidate_sha256"] and doc["exact_parent_inverse"]
    assert all(base.digest(p) == digest for p, digest in doc["evidence"].items())
    driver = proof.live.driver
    rom = parent if case == "highlights_parent" else SimpleNamespace(ROM=stage.ROM, RELEASE=stage.PROOF)
    settings = vars(driver) | dict(ROOT=ROOT, parent=rom,
        FOCUS=set(range(3668)), get_schedule=schedule, __file__=__file__)
    FunctionType(driver.main.__code__, settings)(case)


def compare_panels(before, after, previous, revised):
    assert after.size == before.size == (256, 384)
    assert after.crop((0, 0, 256, 192)).tobytes() == before.crop((0, 0, 256, 192)).tobytes()
    old_body = proof.art_ink(previous, before)
    new_body = proof.art_ink(revised, after)
    old_pixels = before.crop((0, 192, 256, 384)).get_flattened_data()
    new_pixels = after.crop((0, 192, 256, 384)).get_flattened_data()
    change = 0
    for a, b, old, new in zip(old_pixels, new_pixels, previous.indices, revised.indices, strict=True):
        if a != b:
            assert old != new
            change += 1
    assert change > 0
    return dict(old_mask=old_body, new_mask=new_body, exact_RGB_outside_changed_text_art=True,
        changed_lower_pixels=change, two_pages=False)


def verify():
    root = ROOT / "highlights"
    report_path, trace_path, terminal_path = (root / p for p in (
        "capture/capture_report.json", "requests.json", "terminal.json"))
    record, trace, terminal, stage_proof = map(base.load, (report_path, trace_path, terminal_path, stage.PROOF))
    assert record["ROM_sha256"] == terminal["ROM_sha256"] == stage_proof["candidate_sha256"] == base.digest(stage.ROM)
    producer = ROOT / "original_replay_producer.py"
    assert all(base.digest(producer if Path(p).resolve() == Path(__file__).resolve() else p) == digest
               for p, digest in terminal["evidence"].items())
    assert record["cold_boot"] and not record["savestate_loaded"] and not record["callback_errors"]
    assert not record.get("battery_save_preloaded") and not any(v for k, v in record.items() if k.startswith("synthetic_"))
    assert not trace["source_requests"] and trace["all_host_slots_restored_and_core_file_exact"]
    assert not trace["errors"] and not trace["mismatches"] and len(trace["rows"]) == 3
    original, revised = map(base.NdsImage.open, (parent.ROM, stage.ROM))
    captured = {r["frame"]: r for r in record["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    prior = base.load(proof.OUT)["online_cards"]
    holds, examples = {}, []
    text_calls = {r["pointer"]:r for r in trace["rows"]}
    for n, key, frame in ((60,"DK4_EXTRAS_NEW_ALLIES",2890), (61,"DK4_EXTRAS_OWN_SHIP",3890), (62,"DK4_EXTRAS_VAST_WORLD",4890)):
        spec = prior[key]
        caption = spec["caption_review"]
        assert text_calls[caption["installed_reference"]["pointer"]]["text"] == caption["english"]
        before, after = map(proof.picture, (caption["screenshot"], captured[frame]))
        if n == 60:
            assert before.tobytes() == after.tobytes()
            continue
        path = spec["card_path"]
        source, target = (PxlImage.from_bytes(image.read_file(path)) for image in (original, revised))
        result = compare_panels(before, after, source, target)
        adjacent = (4075,) if n == 61 else (5075, 5260)
        result["same_revised_text_with_other_slides"] = [proof.art_ink(target, proof.picture(captured[f])) | dict(frame=f)
            for f in adjacent]
        holds[path] = result | dict(screenshot=captured[frame], caption=caption["english"])
        examples.append((n,before,after))
    assert set(holds) == set(stage_proof["changed_files"])
    earlier_title_path = ROOT / "highlights_parent/capture/capture_report.json"
    earlier_report = base.load(earlier_title_path)
    assert earlier_report["ROM_sha256"] == stage_proof["predecessor_sha256"] == base.digest(parent.ROM)
    assert earlier_report["scripted_input_schedule"] == record["scripted_input_schedule"]
    assert earlier_report["core_options"] == record["core_options"]
    earlier_title, = [shot for shot in earlier_report["frames_captured"] if shot["frame"] == 6499]
    assert proof.picture(earlier_title).tobytes() == proof.picture(captured[6499]).tobytes()
    sheet = Image.new("RGB", (512, 2 * 214), "#1f2830")
    draw = ImageDraw.Draw(sheet)
    for n, before, after in examples:
        y = (n - 61) * 214
        draw.text((4,y+2), f"Online {n} / previous wording", fill="white")
        draw.text((260,y+2), f"Online {n} / revised wording", fill="white")
        sheet.paste(before.crop((0,192,256,384)), (0,y+20))
        sheet.paste(after.crop((0,192,256,384)), (256,y+20))
    sheet.save(SHEET)
    base.save(OUT, dict(candidate_sha256=stage_proof["candidate_sha256"], records=holds,
        exact_unchanged_neighbor=True, exact_title_return=captured[6499], COMMON_requests=0,
        ordinary_controller_replay=True, hardware=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(p): base.digest(p) for p in (report_path, trace_path, terminal_path, stage.PROOF,
            earlier_title_path, producer)}))
    print("Both revised cards matched all ink and outline pixels, and the original title return matched exactly.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "replay-parent", "verify", "patch", "startup"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        step = getattr(release_tools, action)
        settings = dict(base=base, native=native, parent=parent, PROOF=stage.PROOF, ROM=stage.ROM,
            PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
        FunctionType(step.__code__, step.__globals__ | settings)()
    elif action == "replay-parent":
        replay("highlights_parent")
    else:
        globals()[action]()
