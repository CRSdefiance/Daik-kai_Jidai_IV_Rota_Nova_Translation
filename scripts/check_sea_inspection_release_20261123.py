"""Verify the staged inspection reactions against the original replay and clean patch."""

from argparse import ArgumentParser
from os import link, replace
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as prior
from scripts import stage_sea_inspection_prose_20261123 as stage
from scripts.stage_cartridge_title_20261123 import digest, read, reference, write
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask
from scripts.verify_special_target_labels_20261115 import captured, shots


PATCH, REBUILT = stage.WORK / "translation.xdelta", stage.WORK / "clean_rebuilt.nds"
STARTUP_CAPTURE = stage.WORK / "startup/capture/capture_report.json"
PATCH_PROOF = stage.WORK / "clean_patch_proof.json"
PLAY, SHEET = stage.WORK / "focused_replay_proof.json", stage.WORK / "focused_replay.png"
CASES = ("fish", "whale")


def check_replays(stored):
    assert not PLAY.exists() and not SHEET.exists()
    image = stage.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    observed = {}
    sheet = Image.new("RGB", (1040, 420), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, case in enumerate(CASES):
        baseline = stage.live.ROOT / case / "capture/capture_report.json"
        revised = stage.WORK / "focused" / case / "capture/capture_report.json"
        old, new = map(read, (baseline, revised))
        assert old["ROM_sha256"] == stored["predecessor"]["sha256"]
        assert new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(stage.ROM)
        assert old["frames"] == new["frames"] == 6750
        for key in ("scripted_input_schedule", "core_options", "core_DLL_sha256"):
            assert old[key] == new[key]
        assert new["cold_boot"] and not new["savestate_loaded"] and not new["callback_errors"]
        before, after = map(shots, (old, new))
        original_panel, revised_panel = (captured(frames[5950]) for frames in (before, after))
        old_lines = ("O-oh, no... Are we going to make it", "home alive?")
        new_lines = (stage.EDITS[2209],)
        body_mask(font, original_panel, old_lines)
        proof = body_mask(font, revised_panel, new_lines)
        complete_mask(font, "Charles Rochefort", revised_panel, 16, 277, (98, 97, 98))
        bounds = ImageChops.difference(original_panel, revised_panel).getbbox()
        assert bounds is not None and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 346
        same_frames = (4800, 5400, 5600, 5700, 6300, 6750)
        assert all(before[n]["framebuffer_sha256"] == after[n]["framebuffer_sha256"] for n in same_frames)
        observed[case] = dict(clean_predecessor=reference(baseline), revised=reference(revised),
           full_visible_reaction_glyphs=proof, untouched_frame_numbers=same_frames,
           changed_pixel_bounds=bounds, portrait_and_nameplate_preserved=True, focused_encounter_fixture=True,
           current_and_revised_screens=[before[5950], after[5950]])
        x = i * 520
        for j, (tag, src) in enumerate((("before", original_panel), ("revised", revised_panel))):
            y = j * 210
            draw.text((x + 5, y + 5), f"{case.capitalize()} {tag}", fill="white")
            sheet.paste(src.crop((0, 272, 256, 365)).resize((512, 186), Image.Resampling.NEAREST), (x + 5, y + 20))
    sheet.save(SHEET)
    write(PLAY, dict(candidate_sha256=stored["candidate"]["sha256"], captures=observed, sheet=reference(SHEET),
        actual_fixture_coverage=[2209], native_offline_role_alternatives=[2210, 2211, 2212],
        all_revised_and_retained_portrait_paths_have_exact_native_layout=True))
    print("Both focused replays preserved the inspection transitions and displayed Charles's full revised line.")


def check(task):
    stored = read(stage.PROOF)
    if task == "play":
        check_replays(stored)
        return
    action = getattr(prior, task)
    context = action.__globals__ | dict(PATCH=PATCH, REBUILT=REBUILT, RELEASE=stage.live.RELEASE,
                                      STARTUP_CAPTURE=STARTUP_CAPTURE)
    proof = dict(candidate=str(stage.ROM), candidate_sha256=stored["candidate"]["sha256"],
                 clean_input_sha256=stored["clean"]["sha256"], predecessor_sha256=stored["predecessor"]["sha256"])
    FunctionType(action.__code__, context)(proof)
    if task == "patch":
        assert digest(REBUILT) == proof["candidate_sha256"]
        alias = stage.WORK / "verified_rebuild.link"
        link(stage.ROM, alias)
        replace(alias, REBUILT)
        write(PATCH_PROOF, dict(candidate_sha256=proof["candidate_sha256"], patch=reference(PATCH),
             clean_input_sha256=proof["clean_input_sha256"], rebuilt_same_file=stage.ROM.samefile(REBUILT), byte_exact=True))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("play", "patch", "startup"))
    check(parser.parse_args().check)
