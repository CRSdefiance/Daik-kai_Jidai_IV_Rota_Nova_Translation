"""Check complete starter-ship glyphs in the original Hangzhou Shipyard."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_maria_starter_ship_names_20261121 as stage
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_ship_class_names_20261115 import strip_owned_text


base, ROOT = stage.base, stage.ROOT
PROOF = ROOT / "shipyard_verification.json"
SHEET = ROOT / "maria_starter_names_shipyard.png"
TOP_NAME = (5, 0, 127, 24)
TOP_CLASS = (193, 0, 252, 24)
SELL_ROW = (30, 192, 145, 208)


def run(folder, candidate, frames):
    path = ROOT / folder / "capture_report.json"
    report = base.load(path)
    assert report["ROM_sha256"] == candidate and report["frames"] == frames
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    save = report["battery_save_preloaded"]
    assert save["copied_byte_exact_before_cold_boot"]
    assert base.digest(save["source"]) == save["source_sha256"]
    return report, {str(path): base.digest(path)}


def comparison(panels):
    evidence = Image.new("RGB", (1024, 2 * 534), "#22313a")
    draw = ImageDraw.Draw(evidence)
    for i, (label, image) in enumerate(panels):
        x, y = (i % 2) * 512, (i // 2) * 534
        draw.text((x + 9, y + 4), label, fill="white")
        crop = image.crop((0, 0, 256, 192))
        evidence.paste(crop.resize((512, 384), Image.Resampling.NEAREST), (x, y + 18))
        # Show the name header and the list in their original order.
        entries = image.crop((0, 192, 256, 256))
        evidence.paste(entries.resize((512, 128), Image.Resampling.NEAREST), (x, y + 402))
    evidence.save(SHEET)


def main():
    assert not PROOF.exists() and not SHEET.exists()
    staged = base.load(stage.PROOF)
    parent_sha, candidate = staged["parent_sha256"], staged["candidate_sha256"]
    current, old_proof = run("current_shipyard", parent_sha, 33700)
    revised, new_proof = run("staged_shipyard", candidate, 33700)
    remodel, remodel_proof = run("staged_remodel", candidate, 34300)
    assert current["scripted_input_schedule"] == revised["scripted_input_schedule"]
    assert remodel["scripted_input_schedule"] == base.load(ROOT / "remodel_controls.json")
    assert len({r["battery_save_preloaded"]["source_sha256"] for r in (current, revised, remodel)}) == 1
    assert len({r["core_DLL_sha256"] for r in (current, revised, remodel)}) == 1
    frame_sets = [shots(report) for report in (current, revised, remodel)]
    evidence = old_proof | new_proof | remodel_proof

    def screen(which, frame):
        item = frame_sets[which][frame]
        evidence[item["path"]] = item["PNG_sha256"]
        return captured(item)

    before, after = screen(0, 32800), screen(1, 32800)
    assert screen(0, 33400).tobytes() == screen(1, 33400).tobytes()
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    diff = ImageChops.difference(before, after)
    assert diff.getbbox()
    sale = [strip_owned_text(diff, font, label, image, bounds)
            for label, image in (("Hua", before), ("Huachang", after))
            for bounds in (TOP_NAME, SELL_ROW)]
    assert diff.getbbox() is None
    hull = find_mask(font, "Junk", after, TOP_CLASS)
    assert hull == find_mask(font, "Junk", before, TOP_CLASS)

    flagship = screen(2, 34000)
    header = find_mask(font, "Chunshen", flagship, TOP_NAME)
    kind = find_mask(font, "Junk", flagship, TOP_CLASS)
    first = find_mask(font, "Chunshen", flagship, (22, 192, 177, 218))
    second = find_mask(font, "Huachang", flagship, (22, 220, 177, 255))
    assert first["bounds"][3] <= second["bounds"][1]
    remodel_row = dict(selected="Chunshen", complete_name=header, hull=kind, visible_list=[first, second])
    exit_screen = screen(2, 34300)
    assert exit_screen.tobytes() != flagship.tobytes()
    comparison((("Sell before", before), ("Sell with full name", after),
                ("Remodel flagship and escort", flagship), ("Back to the shipyard", exit_screen)))
    base.save(PROOF, dict(
        candidate_sha256=candidate, parent_sha256=parent_sha, checked_model_IDs=[147, 148],
        ordinary_controls=True, prepared_system_unlock=True, hardware=False,
        sell_name_masks=sale, sell_surroundings_and_return_exact=True, unchanged_hull=hull,
        remodel_selected_and_list_masks=remodel_row, evidence=evidence,
        sheets={str(SHEET): base.digest(SHEET)},
    ))


if __name__ == "__main__":
    main()
