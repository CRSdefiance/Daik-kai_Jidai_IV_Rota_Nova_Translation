"""Play the established startup route on the Athens and London candidate."""
import sys

from scripts.replay_athens_london_trends_20261121 import base, original, stage


def main():
    folder = stage.ROOT / "startup"
    plan = base.load(folder / "replay_parameters.json")
    harness = original.runs.previous.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(folder / "capture"),
        "--frames", str(plan["frames"]), "--inputs-json", str(folder / "identical_startup_inputs.json"),
        "--battery-save", plan["source"], "--press-start", "-1", "--touchscreen", "--dump-ram",
        "--capture-every", "999999", "--capture-at", *map(str, plan["captures"])]
    harness.main()


if __name__ == "__main__":
    main()
