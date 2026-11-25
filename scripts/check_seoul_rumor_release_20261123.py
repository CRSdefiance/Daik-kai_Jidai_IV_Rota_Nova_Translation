"""Check the exact patch, startup, and paired ordinary Seoul Food Shop replay."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_supply_ratio_release_inputs_20261123 as prior
from scripts.prepare_riga_seoul_review_20261123 import ARM, NEW_LINES, OLD_LINES, RELEASE, ROM, ROOT, STAGE
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask


PATCH, REBUILT = STAGE / "translation.xdelta", STAGE / "clean_rebuilt.nds"
STARTUP_CAPTURE = STAGE / "startup/capture/capture_report.json"
PATCH_PROOF = STAGE / "clean_patch_proof.json"
PLAY, SHEET = STAGE / "ordinary_Seoul_comparison.json", STAGE / "ordinary_Seoul_comparison.png"


def play(stored):
    paths = [ROOT / name / "capture/capture_report.json" for name in ("seoul", "seoul_staged")]
    original, staged = map(read, paths)
    assert original["ROM_sha256"] == stored["predecessor"]["sha256"]
    assert staged["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert original["frames"] == 15130 and staged["frames"] == 10650
    cases, frames = [], []
    for path, run in zip(paths, (original, staged), strict=True):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(v for k, v in run.items() if k.startswith("synthetic_"))
        terminal_path = path.parent.parent / "terminal.json"
        terminal = read(terminal_path)
        donor = run["battery_save_preloaded"]
        assert terminal["candidate_sha256"] == run["ROM_sha256"] and terminal["ordinary_controller_inputs"]
        assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == terminal["copied_save_sha256"]
        frames.append({row["frame"]: row for row in run["frames_captured"] if row["path"].endswith("_navigation.png")})
        cases.append(dict(emulator=reference(path), terminal=reference(terminal_path), donor=reference(donor["source"])))
    assert cases[0]["donor"] == cases[1]["donor"]
    assert original["scripted_input_schedule"][:len(staged["scripted_input_schedule"])] == staged["scripted_input_schedule"]
    for key in ("core_options", "core_DLL_sha256"):
        assert original[key] == staged[key]
    journals = [read(path.parent / "navigation_command_journal.json")["commands_received"] for path in paths]
    assert journals[0][:len(journals[1])-1] == journals[1][:-1]
    assert journals[1][-1]["command"] == {"stop": True}
    controls = (3200, 3830, 5480, 9230, 9530, 9850, 10010, 10330, 10650)
    assert all(frames[0][n]["PNG_sha256"] == frames[1][n]["PNG_sha256"] for n in controls)
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))
    sheet = Image.new("RGB", (1040, 456), "#263238")
    draw = ImageDraw.Draw(sheet)
    changes = []
    for i, n in enumerate((10170, 10490)):
        old, new = [captured(group[n]) for group in frames]
        body_mask(font, old, OLD_LINES)
        glyphs = body_mask(font, new, NEW_LINES)
        ink, name = complete_mask(font, "Shopkeeper", new, 16, 277, (98, 97, 98))
        assert not any(pixel == (0, 8, 0) for pixel in new.crop((16, 345, 245, 360)).get_flattened_data())
        bounds = ImageChops.difference(old, new).getbbox()
        assert bounds is not None and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 346
        for j, picture in enumerate((old, new)):
            x, y = 5 + j * 520, i * 228
            draw.text((x, y + 5), f"Food Shop visit {i + 1} / {'before' if j == 0 else 'revised'}", fill="white")
            sheet.paste(picture.crop((0, 271, 256, 372)).resize((512, 202), Image.Resampling.NEAREST), (x, y + 21))
        changes.append(dict(frame=n, revised_glyphs=glyphs, nameplate=dict(pixels=ink, bounds=name),
                            changed_pixel_bounds=bounds, original=frames[0][n], revised=frames[1][n]))
    sheet.save(SHEET)
    write(PLAY, dict(candidate_sha256=stored["candidate"]["sha256"], cases=cases, matching_control_frames=controls,
                    ordinary_food_shop_repetitions=changes, sheet=reference(SHEET), hardware=False))


def check(task):
    stored = read(STAGE / "stored_proof.json")
    if task == "play":
        play(stored)
        return
    action = getattr(prior, task)
    scope = action.__globals__ | dict(PATCH=PATCH, REBUILT=REBUILT, RELEASE=RELEASE, STARTUP_CAPTURE=STARTUP_CAPTURE)
    proof = dict(candidate=str(ROM), candidate_sha256=stored["candidate"]["sha256"],
                 clean_input_sha256=stored["clean"]["sha256"], predecessor_sha256=stored["predecessor"]["sha256"])
    FunctionType(action.__code__, scope)(proof)
    if task == "patch":
        assert digest(REBUILT) == proof["candidate_sha256"]
        write(PATCH_PROOF, dict(candidate_sha256=proof["candidate_sha256"], patch=reference(PATCH),
                               clean_input_sha256=proof["clean_input_sha256"], rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("play", "patch", "startup"))
    check(parser.parse_args().action)
