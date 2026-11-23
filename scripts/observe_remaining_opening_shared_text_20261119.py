"""Trace pending COMMON requests on the remaining native New Game openings."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as observer
from scripts import observe_opening_scene_labels_20261115 as prior
from scripts import observe_setup_save_common_v1 as setup
from scripts import register_sea_event_dialogue_followup_20261118 as current
from scripts.source_locked_derivation_v5118 import checked_text

base = current.base
ROOT = Path("work/opening_shared_text_20261119")
MARIA = Path("work/analysis/maria_opening_v674")
ROUTES = prior.ROUTES
BINDING = current.stage.ROOT / "shared_text_current_binding.json"
RUNS = {
    "lil": [2429, 2500, 2640, 2790, 2860, 2950],
    "hodram": [2429, 2500, 2660, 2890, 3120, 3200],
    "maria": [3400, 3600, 4000, 4500, 5000],
}


def schedule(case):
    if case == "maria":
        inputs = MARIA / "dispatch_inputs.json"
        baseline, = [row for row in base.load(MARIA / "proof.json")["reports"] if row["tag"] == "baseline"]
        assert base.digest(baseline["path"]) == baseline["sha256"]
        assert base.load(inputs) == base.load(baseline["path"])["scripted_input_schedule"]
        manifest_path = current.verified.replay.STARTUP / "system_unlock_manifest.json"
        manifest = base.load(manifest_path)
        assert base.digest(manifest["fixture_save"]) == manifest["fixture_save_sha256"]
        assert manifest["production_ROM_sha256"] == base.digest(current.ROM)
        donor = dict(source=manifest["fixture_save"], source_sha256=manifest["fixture_save_sha256"],
            manifest=str(manifest_path))
        return base.load(inputs), RUNS[case], RUNS[case][-1], inputs, donor
    cfg = base.load(ROUTES)[case]
    inputs = Path(cfg["inputs"])
    assert base.digest(inputs) == cfg["inputs_sha256"] and cfg["frames"] == RUNS[case][-1]
    return base.load(inputs), RUNS[case], cfg["frames"], inputs, None


def main(case):
    binding = base.load(BINDING)
    assert binding["candidate_sha256"] == base.load(current.RELEASE)["candidate_sha256"]
    focus = {r["message_ID"] for r in binding["records"]}
    assert len(focus) == 276
    src = checked_text(getsource(observer.main), {
        "argv += ['--battery-save', donor['source'], '--touchscreen']":
        "argv += ['--battery-save', donor['source'], '--allow-gallery-fixtures',\n"
        "                 '--gallery-save-fixture-manifest', donor['manifest']]",
        "assert not any(value for key, value in report.items() if key.startswith('synthetic_'))":
        "assert not any(value for key, value in report.items() if key.startswith('synthetic_')\n"
        "                   and key != 'synthetic_gallery_fixtures')\n"
        "    assert len(report.get('synthetic_gallery_fixtures', [])) == int(bool(donor))",
    })
    env = vars(observer) | dict(ROOT=ROOT, parent=current, observer=setup.scoped_observer,
        get_schedule=schedule, FOCUS=focus, __file__=__file__)
    exec(compile(src, __file__ + "::new-game", "exec"), env)
    env["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=tuple(RUNS))
    main(parser.parse_args().case)
