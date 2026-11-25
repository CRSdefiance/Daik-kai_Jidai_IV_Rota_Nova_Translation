"""Check the four revised story panels and every captured companion frame."""

from types import SimpleNamespace

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_amsterdam_hodram_wraps_20261125 as stage
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


panels = stage.panels
OUT = stage.OUT.with_name("amsterdam_hodram_wraps_paired_20261125.json")


def main():
    before_path = stage.review.play.ROOT / "capture/capture_report.json"
    replay_path = stage.CAPTURE / "capture_report.json"
    before, after, stored, proposal = map(read, (before_path, replay_path, stage.STORED, stage.OUT))
    assert before["ROM_sha256"] == stored["parent"]["sha256"]
    assert after["ROM_sha256"] == stored["candidate"]["sha256"] == digest(stage.ROM)
    assert stored["proposal"] == reference(stage.OUT) and stored["exact_parent_inverse"]
    assert [e for e in before["scripted_input_schedule"] if e["start"] <= stage.FINAL_REPLAY_FRAME] == after["scripted_input_schedule"]
    assert after["frames"] == stage.FINAL_REPLAY_FRAME
    for key in ("core_DLL_sha256", "core_options"):
        assert before[key] == after[key]
    for report in (before, after):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    a, b = (report["battery_save_preloaded"] for report in (before, after))
    assert a["source_sha256"] == b["source_sha256"] == digest(b["source"])
    frames = {n: s for n, s in panels.shots(before, "_navigation.png").items() if 10800 <= n <= stage.FINAL_REPLAY_FRAME}
    installed = panels.shots(after, "_cold_boot.png")
    assert set(frames) <= set(installed)
    changed = {row["capture"]["frame"]: row for row in proposal["records"]}
    assert set(changed) <= set(frames)
    image = NdsImage.open(stage.ROM)
    arm = image.read_file(stage.parent.ARM)
    assert arm == NdsImage.open(stage.parent.ROM).read_file(stage.parent.ARM)
    ctx = SimpleNamespace(arm=arm, image=image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    renderer, font = panels.town.clipped_renderer(ctx), GameAsciiFont.from_arm9(arm)
    companion, revised, figures = [], [], []
    for n, shot in frames.items():
        prior, new = panels.picture(shot), panels.picture(installed[n])
        difference = ImageChops.difference(prior, new)
        if n not in changed:
            assert difference.getbbox() is None, (n, difference.getbbox())
            companion.append(n)
            continue
        row = changed[n]
        assert shot["PNG_sha256"] == row["capture"]["PNG_sha256"]
        body = panels.bytes_for(bytes.fromhex(row["exact_proposed_command_hex"]))
        page, = panels.story_display.display.raster(ctx, kanji, renderer, body, row["formatter_plan"]["lines"], 1)
        plane = bytes.fromhex(page["native_plane_hex"])
        assert sha256(plane).hexdigest() == row["native_preview_sha256"] and panels.mask_check(plane, 216, new)
        assert panels.nameplate(font, row["speaker"], prior) == panels.nameplate(font, row["speaker"], new)
        difference.paste((0, 0, 0), (224, 360, 240, 376))
        bounds = difference.getbbox()
        assert bounds and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 360
        revised.append(dict(id=row["id"], frame=n, before=shot, after=installed[n], body_bounds=bounds,
                            native_mask_sha256=sha256(plane).hexdigest()))
        figures += [(f"{row['id']} before", prior), (f"{row['id']} revised", new)]
    sheets = panels.sheets_for("amsterdam_hodram_wraps_paired_20261125", figures)
    write(OUT, dict(candidate=stored["candidate"], parent=stored["parent"], ordinary_gameplay=True,
        baseline=reference(before_path), replay=reference(replay_path), revised_holds=revised,
        exact_companion_frames=companion, sheets=sheets, proposal=reference(stage.OUT)))
    print(f"Verified all four revised story holds and {len(companion)} pixel-exact companion frames.")


if __name__ == "__main__":
    main()
