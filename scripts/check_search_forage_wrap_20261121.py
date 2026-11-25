"""Replay Charles's original foraging report with the revised line breaks."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from scripts import check_search_forage_digits_20261121 as prior_capture
from scripts import replay_search_supply_and_fatigue_digits_20261121 as replay
from scripts import stage_search_forage_wrap_20261121 as stage
from scripts.verify_crew_and_shore_reports_v1 import fleet_state


base, shared, ROOT = stage.base, stage.shared, stage.ROOT
PROOF, SHEET = ROOT / "verified_forage_wrap.json", ROOT / "search_forage_wrap_live.png"
HOLD, RETURN = prior_capture.HOLD, prior_capture.RETURN
ID, AMOUNTS = prior_capture.EXPECTED_ID, list(prior_capture.QUANTITIES)


def run():
    env = vars(replay) | {"stage": stage, "ROOT": ROOT, "HOLDS": {HOLD: (ID, AMOUNTS)}, "__file__": __file__}
    FunctionType(replay.replay.__code__, env)("after", extend=True)


def verify():
    assert not PROOF.exists()
    prior = base.load(prior_capture.PROOF)
    draft = base.load(stage.PROOF)
    assert prior["candidate_sha256"] == draft["parent_sha256"] and base.digest(stage.ROM) == draft["candidate_sha256"]
    folders = [folder / "after_extra" / "capture" for folder in (replay.ROOT, ROOT)]
    paths = [folder / "capture_report.json" for folder in folders]
    reports = list(map(base.load, paths))
    assert [r["ROM_sha256"] for r in reports] == [draft["parent_sha256"], draft["candidate_sha256"]]
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] for r in reports)
    for key in ("frames", "core_options", "core_DLL_sha256", "scripted_input_schedule"):
        assert reports[0][key] == reports[1][key]
    journals = [folder / "navigation_command_journal.json" for folder in folders]
    assert base.load(journals[0])["commands_received"] == base.load(journals[1])["commands_received"]
    fixtures = [[(r["frame"], r["owned_bytes"], r["changes"]) for r in report["synthetic_battle_recovery_proximity_fixtures"]]
                for report in reports]
    assert fixtures[0] == fixtures[1] and len(fixtures[0]) == 8
    views = [{r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
             for report in reports]
    assert views[0].keys() == views[1].keys()
    changed, exact = [], []
    for frame, old in views[0].items():
        new = views[1][frame]
        assert all(base.digest(r["path"]) == r["PNG_sha256"] for r in (old, new)), frame
        (exact if old["framebuffer_sha256"] == new["framebuffer_sha256"] else changed).append(frame)
    assert changed == [11173, HOLD] and RETURN in exact

    images = [base.NdsImage.open(p) for p in (stage.parent.ROM, stage.ROM)]
    arms = [img.read_file(shared.ARM) for img in images]
    ram, = (r for r in reports[1]["read_only_capture_RAM_snapshots"] if r["frame"] == HOLD)
    assert ram["read_only_export"] and base.digest(ram["path"]) == ram["sha256"]
    memory = Path(ram["path"]).read_bytes()
    at = unpack_from("<I", arms[1], 0x54450)[0] - stage.previous.number.BASE
    resident = memory[at:at + 512].split(b"\0", 1)[0]
    sample, = (r for r in draft["native_display_cases"] if r["message_ID"] == ID and r["water_and_food"] == AMOUNTS)
    assert resident.hex() == sample["after_hex"]
    panels = [Image.open(rows[HOLD]["path"]).convert("RGB") for rows in views]
    font, _, _ = stage.previous.common.discovery.mixed.font_tools(images[1])
    kanji = images[1].read_file("/GRP/KANJI.FNT")
    ink, _ = stage.previous.render_portrait(font, arms[1], kanji, resident)
    box = (16, 296, 244, 360)
    assert bytes(pixel == (0, 8, 0) for pixel in panels[1].crop(box).get_flattened_data()) == ink
    for frame in changed:
        before, after = [Image.open(rows[frame]["path"]).convert("RGB") for rows in views]
        rect = ImageChops.difference(before, after).getbbox()
        assert rect and box[0] <= rect[0] < rect[2] <= box[2] and box[1] <= rect[1] < rect[3] <= box[3]
    states = []
    for arm, report in zip(arms, reports, strict=True):
        last = report["read_only_RAM_snapshot"]
        assert base.digest(last["path"]) == last["sha256"]
        states.append(fleet_state(arm, Path(last["path"]).read_bytes()))
    assert states[0] == states[1] == prior["final_fleet_state"]
    sheet = Image.new("RGB", (1024, 338), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, panel in enumerate(panels):
        left = i * 512
        labels.text((left + 6, 6), ("Previous wrap", "Complete resource phrases")[i], fill="white")
        sheet.paste(panel.crop((0, 226, 256, 384)).resize((512, 316), Image.Resampling.NEAREST), (left, 22))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=draft["candidate_sha256"], parent_sha256=draft["parent_sha256"],
        water_and_food=AMOUNTS, message_ID=ID, speaker="Charles Rochefort", lines=sample["lines"],
        exact_live_glyphs=True, original_Search_outcome=True, actual_return_frame=RETURN, same_fleet_state=states[1],
        unchanged_frames=exact, changed_dialogue_frames=changed, hardware_verified=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)), evidence={str(p): base.digest(p) for p in (*paths, *journals)}))
    print(f"Charles’s complete resource phrases match gameplay ink. The other {len(exact)} views and sailing state match.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("replay", "verify"))
    (run if parser.parse_args().action == "replay" else verify)()
