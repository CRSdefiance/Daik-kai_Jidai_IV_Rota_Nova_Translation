"""Read the full native credit plane and return prompt for each staged movie."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_ending_credit_spacing_20261123 as replay
from scripts import stage_ending_credit_spacing_20261123 as stage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_ending_credits_v578 import source_caption


base, native = stage.base, stage.native
OUT = stage.ROOT / "verified_playback.json"
SHEET = stage.ROOT / "ending_credits_before_after.png"


def image(shot):
    assert base.digest(shot["path"]) == shot["PNG_sha256"]
    with Image.open(shot["path"]) as original:
        return original.convert("RGB")


def verify():
    preflight = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == preflight["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == preflight["predecessor_sha256"]
    original, revised = map(base.NdsImage.open, (stage.parent.ROM, stage.ROM))
    font = GameAsciiFont.from_arm9(revised.read_file(stage.parent.ARM))
    evidence = {str(stage.PROOF): base.digest(stage.PROOF), str(Path(__file__)): base.digest(Path(__file__))}
    sheet = Image.new("RGB", (1056, 408), "#263238")
    captions = ImageDraw.Draw(sheet)
    rows, record_ids = [], []
    for sequence, row in enumerate(preflight["records"]):
        captain, path, index = (row[key] for key in ("captain", "file_path", "texture_index"))
        archive, active = (rom.read_file(path) for rom in (original, revised))
        assert native.digest(archive) == row["source_reference"]["archive_sha256"]
        assert native.digest(active) == row["installed_reference"]["archive_sha256"]
        previous, original_points, _, rejected = source_caption(archive, index)
        texture, white, dark, accepted = source_caption(active, index)
        assert previous.palette == texture.palette
        assert layout_points(original_points) == set(map(tuple, white))
        assert set(accepted).isdisjoint(rejected)
        terminal_path = stage.ROOT / captain.lower() / "terminal.json"
        terminal = base.load(terminal_path)
        assert terminal["candidate_sha256"] == preflight["candidate_sha256"]
        assert all(base.digest(path) == digest for path, digest in terminal["evidence"].items())
        evidence.update(terminal["evidence"])
        evidence[str(terminal_path)] = base.digest(terminal_path)
        report = base.load(terminal["capture_report"])
        old = base.load(terminal["original_report"])
        fixture = terminal["ending_state_fixture"]
        assert fixture["native_dispatch_arguments"] == [sequence + 29, 0, 0, 0]
        assert fixture["changes"] == [{"address": 0x022796BC, "before": 1, "after": 4}]
        assert report["ROM_sha256"] == preflight["candidate_sha256"]
        headings = {shot["frame"]: shot for shot in report["frames_captured"]}
        historical = {shot["frame"]: shot for shot in old["frames_captured"]}
        holds = []
        for frame, shot in headings.items():
            if frame <= fixture["frame"]:
                continue
            pixels = image(shot).crop((0, 0, 256, 192)).point(lambda value: value >> 3).tobytes()
            if pixels in rejected:
                raise AssertionError(f"{captain} displays the earlier credit arrangement at frame {frame}")
            if (level := accepted.get(pixels)) is None:
                continue
            if frame in historical:
                comparison = image(historical[frame]).crop((0, 0, 256, 192)).point(lambda value: value >> 3)
                assert rejected.get(comparison.tobytes()) == level, (captain, frame, level)
            holds.append(dict(frame=frame, capture=shot, original_gray_level=level))
        opaque = next(hold for hold in holds if hold["original_gray_level"] == 31)
        assert len(holds) > 4 and len({hold["original_gray_level"] for hold in holds}) > 2
        end = image(headings[report["frames"]])
        prompt = dark_text(font, "Save the ending data?", end, (12, 292, 248, 324))
        assert prompt["ink_pixels"] > 0, (captain, prompt)
        for n, (title, art) in enumerate(((stage.ORIGINAL, previous.render()),
                (stage.ENGLISH, image(opaque["capture"]).crop((0, 90, 256, 106))))):
            x, y = 8 + 528 * n, 12 + sequence * 102
            captions.text((x, y), f"{captain} / {title}", fill="white")
            sheet.paste(art.convert("RGB").resize((512, 32), Image.Resampling.NEAREST), (x, y + 28))
        record_ids.append(row["id"])
        rows.append(dict(id=row["id"], captain=captain, texture_index=index, fixture=fixture,
            exact_full_upper_credit_holds=holds, first_opaque=opaque, white_pixels=len(white), dark_pixels=len(dark),
            original_credit_shape_rejected=True, complete_ending_save_prompt=prompt,
            prompt_capture=headings[report["frames"]]))
    sheet.save(SHEET)
    base.save(OUT, dict(candidate_sha256=preflight["candidate_sha256"], records=rows, stage_record_ids=record_ids,
        actual_focused_playback=True, earned_route_completion=False, hardware=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)), evidence=evidence))
    print("All four native credits and the ending-save prompts passed.")


def layout_points(points):
    left, right = stage.THANKS
    return {(x + stage.SPACE if left <= x < right else x, y) for x, y in points}


if __name__ == "__main__":
    verify()
