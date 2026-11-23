"""Match the Ceuta wind-choice replay to the revised native pages."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import audit_rafael_sailing_modes_playback_20261119 as original
from scripts import replay_ceuta_lesson_20261119 as play
from scripts import stage_story_short_phrase_wraps_20261119 as build
from scripts import verify_setup_save_equipment_v1 as boot
from scripts import verify_story_short_phrase_wraps_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
PROOF = play.ROOT / "verified_wind_choice.json"
STARTUP = build.ROOT / "own_startup_verification.json"


def gameplay():
    assert not PROOF.exists()
    setup, checked = map(base.load, (play.FIXTURES, offline.PROOF))
    fixture, = setup["fixtures"]
    assert base.digest(build.ROM) == setup["candidate_sha256"] == checked["candidate_sha256"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"] and setup["exact_candidate_inverse"]
    revisions = {r["id"]: r["pages"][0] for r in checked["revisions"] if r["id"].startswith("DK4_MES_B127_")}
    assert len(revisions) == 6
    name_proof = base.load(original.NAMES)
    names = {r["actor_ID"]: r for r in name_proof["name_planes"]}
    expected = dict(menu_selection=1, source_speech_IDs=[
        r["id"] for r in fixture["original_text_records"] if r["id"] != "DK4_MES_B127_R0044"])
    assert len(expected["source_speech_IDs"]) == 16
    source = checked_text(getsource(original.path_result), {
        '{"Please do.", "No, thanks."}': '''{"I've got it!", "The wind might be against us..."}''',
        '    assert commands == expected["visited_source_command_offsets"]':
            '    assert commands and len(set(commands)) == len(commands) and commands == sorted(commands)',
        'f"{choice}: retained choices"': '"Ceuta tutorial choices"',
        'f"{choice}: after the original return"': '"After the tutorial returns"',
    })
    env = vars(original) | {"play": play}
    exec(compile(source, __file__ + "::ceuta-speech-and-choice", "exec"), env)
    result = env["path_result"]("decline", fixture, expected, revisions, names)
    assert result["result"] == [0, 1] and {r["id"] for r in result["checked_revisions"]} == revisions.keys()
    result["evidence"].update({str(p): base.digest(p) for p in (play.FIXTURES, play.FIXTURE, offline.PROOF, original.NAMES)})
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], paths=[result], revised_pages_verified=6,
        natural_activation=False, hardware=False, evidence=result["evidence"]))
    print("Verified all six revised Ceuta pages and the wind-question choice and return.")


def startup():
    capture = play.STARTUP / "capture/capture_report.json"
    previous = base.load(build.parent.RELEASE)
    basis = base.load(play.STARTUP / "basis.json")
    prior = Path(basis["previous_report"])
    assert base.digest(prior) == basis["previous_report_sha256"]
    assert base.digest(basis["manifest"]) == basis["manifest_sha256"]
    source = checked_text(getsource(boot.verify_startup), {
        "ROOT / 'own_startup/capture/capture_report.json'": "CAPTURE",
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR_CAPTURE",
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": "",
        "proof['registered_input']['candidate_sha256']": "proof['predecessor_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": "PRIOR_BOOT",
    })
    env = vars(boot) | dict(PROOF=build.PROOF, ROM=build.ROM, BOOT=STARTUP, CAPTURE=capture, PRIOR_CAPTURE=prior,
                           PRIOR_BOOT=Path(previous["own_registered_startup"]), __file__=__file__)
    exec(compile(source, __file__ + "::startup", "exec"), env)
    env["verify_startup"]()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
