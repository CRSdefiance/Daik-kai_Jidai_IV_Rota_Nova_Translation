"""Bind the sea-event editorial batch to its emulator startup and focused replay."""

from inspect import getsource
from pathlib import Path

from PIL import Image, ImageDraw

from scripts import replay_sea_event_dialogue_followup_20261118 as replay
from scripts import verify_sea_event_bubbles_focused_v2 as history
from scripts import verify_setup_save_equipment_v1 as startup_check
from scripts.source_locked_derivation_v5118 import checked_text

stage, base = replay.stage, replay.base
STARTUP = stage.ROOT / "own_startup_verification.json"
GAME = stage.ROOT / "verified_bubbles.json"
SHEET = stage.ROOT / "bubbles_gameplay.png"


def startup():
    capture = replay.STARTUP / "capture/capture_report.json"
    previous = base.load(stage.parent.RELEASE)
    basis = base.load(replay.STARTUP / "basis.json")
    prior_report = Path(basis["previous_report"])
    assert base.digest(prior_report) == basis["previous_report_sha256"]
    assert base.digest(basis["manifest"]) == basis["manifest_sha256"]
    original = getsource(startup_check.verify_startup)
    source = checked_text(original, {
        "ROOT / 'own_startup/capture/capture_report.json'": "CAPTURE",
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR_CAPTURE",
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": "",
        "proof['registered_input']['candidate_sha256']": "proof['parent_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": "PRIOR_BOOT",
    })
    env = vars(startup_check) | dict(PROOF=stage.PROOF, ROM=stage.ROM, BOOT=STARTUP,
        CAPTURE=capture, PRIOR_CAPTURE=prior_report, PRIOR_BOOT=Path(previous["own_registered_startup"]),
        __file__=__file__)
    exec(compile(source, __file__ + "::startup", "exec"), env)
    env["verify_startup"]()


def gameplay():
    source = checked_text(getsource(history.main), {
        "storage['research_ROM_sha256']": "storage['candidate_sha256']",
        "storage['cases']": "storage['records']",
        "    assert rows[478]['native_formatter_addresses'] == [0x01FF9FAC]\n":
        "    assert BASELINE['native_formatter_addresses'] == [0x01FF9FAC]\n"
        "    assert all(rows[478][k] == BASELINE[k] for k in ('staged_hex', 'display_hex'))\n",
        "PROOF, dict(candidate_sha256=sha": "GAME, dict(candidate_sha256=sha",
    })
    earlier = Path("releases/all_routes_editorial_20261110_sea_events_candidate/verification/stored_balanced_verification.json")
    baseline, = [row for row in base.load(earlier)["cases"] if row["message_ID"] == 478]
    env = vars(history) | dict(PROOF=GAME, GAME=GAME, ROM=stage.ROM, EVIDENCE=stage.PROOF,
        OUT=replay.LIVE, set_condition=replay.set_condition, BASELINE=baseline, __file__=__file__)
    exec(compile(source, __file__ + "::gameplay", "exec"), env)
    env["main"]()
    game = base.load(GAME)
    sheet = Image.new("RGB", (1024, 645), "#202930")
    label = ImageDraw.Draw(sheet)
    frames = [(f"COMMON {r['message_ID']}", r["capture"]) for r in game["observed"]]
    frames.append(("Returned to sailing", game["return_to_sailing_capture"]))
    for i, (caption, capture) in enumerate(frames):
        x, y = i % 2 * 512, i // 2 * 215
        assert base.digest(capture["path"]) == capture["PNG_sha256"]
        with Image.open(capture["path"]) as picture:
            screen = picture.convert("RGB").crop((0, 288, 256, 384))
        label.text((x + 8, y + 4), caption, fill="white")
        sheet.paste(screen.resize((512, 192), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    game["evidence"].update({str(p): base.digest(p) for p in (SHEET, earlier)})
    game["observed_revised_records"] = [457]
    game["offline_only_revised_records"] = sorted(set(stage.REVISIONS) - {457})
    game["compiled_captain_wrap_observed"] = True
    base.save(GAME, game)


if __name__ == "__main__":
    gameplay()
    startup()
