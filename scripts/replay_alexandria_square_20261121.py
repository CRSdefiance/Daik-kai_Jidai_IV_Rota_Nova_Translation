"""Cold-boot a verified Athens save for ordinary Alexandria Square testing."""
from inspect import getsource
from pathlib import Path

from scripts import register_rafael_mediterranean_dialogue_20261121 as active
from scripts import replay_stockholm_december_20261121 as prior
from scripts.source_locked_derivation_v5118 import checked_text


FIRST_ATTEMPT = Path("out/alexandria_square_gameplay_20261121")
ROOT = FIRST_ATTEMPT.with_name(FIRST_ATTEMPT.name + "_v2")
DEPARTURES = {"alexandria": (prior.HISTORY / "environment_voyage_v510_leg/capture_report.json", 7090, 2801)}


if __name__ == "__main__":
    source = checked_text(getsource(prior.main), {
        '"145000"': '"59000"',
        '"--dump-ram"]': '"--dump-ram", "--dump-pause-ram"]',
        "    root.mkdir(parents=True)": '''    prior_report = base.load(FIRST_ATTEMPT / "capture/capture_report.json")
    assert prior_report["ROM_sha256"] == release["candidate_sha256"] and prior_report["frames"] == 15100
    assert prior_report["scripted_input_schedule"][:4] == inputs
    inputs += [x for x in prior_report["scripted_input_schedule"] if 3760 < x["start"] < 6410]
    inputs += [dict(start=frame,duration=8,buttons=["A"]) for frame in (6411,6711,7011)]
    root.mkdir(parents=True)''',
    })
    scope = vars(prior) | globals()
    exec(compile(source, __file__, "exec"), scope)
    scope["main"](ROOT, "alexandria")
