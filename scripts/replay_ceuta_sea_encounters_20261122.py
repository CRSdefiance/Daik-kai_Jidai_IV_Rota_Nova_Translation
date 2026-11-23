"""Replay the historical Ceuta departure on the current retail dialogue candidate."""

from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_istanbul_tobacco_20261122 as release


base = release.base
ROOT = Path("work/analysis/ceuta_sea_encounters_20261122")
HISTORY = Path("work/emulation_v193/sea_foam_family_v514_final_actual/capture_report.json")
ROM = release.ROM
CAPTURES = (3200, 4300, 4600, 5200, 5500, 5800, 5980, 6440, 6740, 7060, 7500, 8000, 8310,
            8400, 8476, 8576, 8676, 8776, 8876, 8976, 9076, 9176, 9276, 9376, 9476, 9700, 10100)


def main():
    assert not ROOT.exists()
    registration, old = map(base.load, (release.RELEASE,HISTORY))
    candidate = base.digest(ROM)
    assert candidate == registration["candidate_sha256"] and base.digest(base.REGISTRY) == registration["registry_sha256"]
    assert base.digest(release.MANIFEST) == registration["manifest_sha256"]
    assert old["cold_boot"] and not old["savestate_loaded"] and not old["callback_errors"]
    assert not any(value for key,value in old.items() if key.startswith("synthetic_"))
    donor = old["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir(parents=True)
    inputs = ROOT/"inputs.json"
    base.save(inputs, old["scripted_input_schedule"])
    base.save(ROOT/"source_binding.json",dict(candidate_sha256=candidate,previous_run=str(HISTORY),
        previous_run_sha256=base.digest(HISTORY),input_sha256=base.digest(inputs),donor=donor["source"],
        donor_sha256=donor["source_sha256"],ordinary_inputs_only=True))
    argv = sys.argv
    try:
        sys.argv = [harness.__file__,"--rom",str(ROM),"--out",str(ROOT/"capture"),"--frames","10101",
            "--inputs-json",str(inputs),"--press-start","-1","--touchscreen","--battery-save",donor["source"],
            "--capture-every","999999","--dump-ram","--capture-at",*map(str,CAPTURES)]
        harness.main()
    finally:
        sys.argv = argv
    assert base.digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()

