"""Check the localized Gallery option and both original collection paths."""

from argparse import ArgumentParser

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_gallery_historic_sites_menu_20261121 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, root = stage.base, stage.ROOT
SHEET = root / "gallery_menu_comparison.png"
FULL = root / "full_popup_verified.json"


def menu_mask(font, image, text):
    center = 128 - len(text) * 3
    matches = []
    for y in range(230, 340):
        for x in range(center - 4, center + 5):
            try:
                matches.append(complete_mask(font, text, image, x, y, (8, 8, 8)))
            except ValueError:
                pass
    (ink, bounds), = matches
    assert 67 <= bounds[0] < bounds[2] <= 189 and 228 <= bounds[1] < bounds[3] <= 342
    return dict(text=text, complete_ink_pixels=ink, bounds=bounds)


def main():
    assert not stage.LIVE.exists()
    manifest = base.load(stage.PROOF)
    digest = manifest["candidate_sha256"]
    assert base.digest(stage.ROM) == digest
    directories = [root / key / "capture" for key in ("empty_before", "empty_after", "populated")]
    old, new = (base.load(folder / "capture_report.json") for folder in directories[:2])
    populated = report(directories[2], digest)
    assert old["ROM_sha256"] == manifest["parent_sha256"] and new["ROM_sha256"] == digest
    for data in (old, new):
        assert data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
        assert not data.get("synthetic_gallery_fixtures") and data["frames"] == 6400
        assert data["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    for field in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "exact_requested_capture_frames"):
        assert old[field] == new[field]
    assert old["battery_save_preloaded"]["source_sha256"] == new["battery_save_preloaded"]["source_sha256"]
    a, b, c = map(shots, (old, new, populated))
    assert a.keys() == b.keys()
    all_frames = [3900, 4300, 4700, 5100, 5500, 5900, 6300]
    before, after = ({n: captured(images[n]) for n in all_frames} for images in (a, b))
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    menus = {n: [
        menu_mask(font, before[n], "Ruins"), menu_mask(font, after[n], stage.ENGLISH),
        menu_mask(font, after[n], "Items"),
    ] for n in (3900, 4700, 5100, 5900)}
    notices = {}
    for key, image, text in (
        ("items_before", before[4300], "You haven't acquired any items."),
        ("items_after", after[4300], "You haven't acquired any items."),
        ("sites_before", before[5500], "You haven't discovered any ruins."),
        ("sites_after", after[5500], stage.EMPTY),
    ):
        notices[key] = font_mask(image, font, text, 16, 297, (16, 296, 237, 349), (0, 8, 0))
    assert before[6300].tobytes() == after[6300].tobytes()
    assert all(before[n].crop((0, 0, 256, 192)).tobytes() == after[n].crop((0, 0, 256, 192)).tobytes()
               for n in all_frames)
    preceding = base.load(stage.parent.stage.ROOT / "after/capture/capture_report.json")
    assert preceding["ROM_sha256"] == manifest["parent_sha256"]
    assert preceding["scripted_input_schedule"] == populated["scripted_input_schedule"]
    p = shots(preceding)
    stable = (2800, 3200, 7000, 7200, 7400)
    for n in stable:
        assert captured(p[n]).tobytes() == captured(c[n]).tobytes(), n
    keep = (("Before menu", before[5100]), ("After menu", after[5100]),
            ("After empty notice", after[5500]), ("Populated Historic Sites", captured(c[3200])))
    sheet = Image.new("RGB", (1024, 216), "#23313a")
    text = ImageDraw.Draw(sheet)
    for i, (label, picture) in enumerate(keep):
        x = 256 * i
        text.text((x + 4, 4), label, fill="white")
        sheet.paste(picture.crop((0, 192, 256, 384)), (x, 24))
    sheet.save(SHEET)
    evidence = {str(path): base.digest(path) for path in (
        *(d / "capture_report.json" for d in directories),
        stage.parent.stage.ROOT / "after/capture/capture_report.json",
        SHEET,
    )}
    for frames, ids in ((a, all_frames), (b, all_frames), (p, stable), (c, stable)):
        evidence.update({frames[n]["path"]: frames[n]["PNG_sha256"] for n in ids})
    base.save(stage.LIVE, dict(candidate_sha256=digest, complete_popup_masks=menus, complete_notice_masks=notices,
         populated_viewer_unchanged_frames=list(stable), modal_dismissal_and_title_return=True,
         ordinary_empty_collection=True, populated_with_initialized_save=True, hardware=False,
         sheets={str(SHEET): base.digest(SHEET)}, evidence=evidence))
    print("The menu, empty notice, populated gallery and return controls all passed.")


def full_popup():
    assert not FULL.exists()
    folder = root / "full_popup/capture"
    digest = base.digest(stage.ROM)
    replay = report(folder, digest)
    assert replay["frames"] == 2400 and not replay["earned_unlock_verified"]
    frame = shots(replay)[2400]
    picture = captured(frame)
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    labels = [menu_mask(font, picture, name) for name in ("Items", stage.ENGLISH, "Characters", "Event Scenes")]
    assert [row["bounds"][1] for row in labels] == sorted({row["bounds"][1] for row in labels})
    base.save(FULL, dict(candidate_sha256=digest, frame=frame, ordered_glyph_masks=labels,
                         capture_report=str(folder / "capture_report.json"),
                         capture_sha256=base.digest(folder / "capture_report.json")))
    print("Verified all four Gallery labels in the initialized popup.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--full-popup", action="store_true")
    full_popup() if parser.parse_args().full_popup else main()
