"""Trace title and New Game text lookups on the registered ROM."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import observe_online_gallery_common_v1 as driver
from scripts import observe_opening_scene_labels_20261115 as title
from scripts import observe_remaining_opening_shared_text_20261119 as later
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_ending_credit_spacing_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/opening_dispositions")
COMPOSITION = title.TITLE
CASES = ("title", "rafael", "hodram", "lil", "maria")


def title_anchors():
    output = {}
    for row in base.load(COMPOSITION)["cases"]:
        if row["source_movie"] != "/FLS/M28.fls":
            continue
        assert row["whole49152_RGB_pixels_exact_without_exclusions"]
        frame = row["display_frame"]
        for layer in row["native_draws"]:
            if layer["alpha"] and layer["drawn_pixels"]:
                index = layer["texture"]
                best = output.get(index)
                weight = layer["alpha"], layer["drawn_pixels"]
                if best is None or weight > best["weight"]:
                    output[index] = dict(frame=frame, weight=weight)
    assert {74, 77, 149, 169} <= output.keys()
    return output


def schedule(case):
    if case == "title":
        # Use one clear reference frame per texture and the existing held title frames.
        frames = {ref["frame"] for ref in title_anchors().values()}
        frames.update(title.title_frames().values())
        return [], sorted(frames), 7400, COMPOSITION, None
    if case == "rafael":
        return title.schedule(case)
    if case != "maria":
        return later.schedule(case)
    path = later.ROOT / "maria/capture/capture_report.json"
    old = base.load(path)
    assert old["cold_boot"] and not old["savestate_loaded"] and not old["callback_errors"]
    fixture, = old["synthetic_gallery_fixtures"]
    manifest = Path(fixture["preloaded_save_manifest"])
    assert base.digest(manifest) == fixture["manifest_sha256"]
    donor = old["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"] == base.load(manifest)["fixture_save_sha256"]
    assert old["scripted_input_schedule"] == base.load(later.MARIA / "dispatch_inputs.json")
    return old["scripted_input_schedule"], later.RUNS[case], old["frames"], path, donor


def observe(case):
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    scope = vars(driver) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)),
        get_schedule=schedule, observer=trace.scoped_observer, __file__=__file__)
    FunctionType(driver.main.__code__, scope)(case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=CASES)
    observe(parser.parse_args().case)
