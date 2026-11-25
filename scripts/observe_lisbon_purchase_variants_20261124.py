"""Continue the ordinary Lisbon Market replay with an earned Purser assignment."""

import json
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_claudio_opening_wrap_20261124 as current
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, write

ROOT = current.ROM.parent.with_name("editorial_20261124_lisbon_purchase_variants")
BOOK = Path("translations/editorial_checkpoints/shared_display_20261123/lisbon_ordinary_purser_20261124.json")
CONTROLLER = ROOT / "controller.jsonl"
PAUSE = 37300
ACTIONS = (
    dict(until=37700, duration=8, buttons=['A']),
    dict(until=38100, duration=8, touch=[94, 105]),
    dict(until=38500, duration=8, buttons=['A']),
    dict(until=38700, duration=8, buttons=['A']),
    dict(until=38900, duration=8, buttons=['A']),
    dict(until=39100, duration=8, buttons=['A']),
    dict(until=39300, duration=8, buttons=['A']),
    dict(until=39500, duration=8, buttons=['A']),
    dict(until=39900, duration=8, touch=[160, 105]),
    dict(until=40300, duration=8, buttons=['A']),
    dict(until=40700, duration=8, buttons=['X']),
    dict(until=41100, duration=8, buttons=['B']),
    dict(until=41500, duration=8, buttons=['X']),
    dict(until=41900, duration=8, buttons=['A']),
    dict(until=42300, duration=8, buttons=['A']),
    dict(until=42700, duration=8, buttons=['A']),
    dict(until=43100, duration=8, buttons=['SELECT']),
    dict(until=43500, duration=8, buttons=['DOWN']),
    dict(until=43900, duration=8, buttons=['DOWN']),
    dict(until=44300, duration=8, buttons=['DOWN']),
    dict(until=44700, duration=8, touch=[50, 158]),
    dict(until=45100, duration=8, buttons=['A']),
    dict(until=45500, duration=8, buttons=['L']),
    dict(until=45900, duration=8, buttons=['R']),
    dict(until=46300, duration=8, buttons=['L']),
    dict(until=46700, duration=8, buttons=['B']),
    dict(stop=True),
)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    source = read(BOOK)
    assert source["original_cold_boot_and_ordinary_controller_inputs"]
    capture = source["evidence"]["capture"]
    previous = read(capture["path"])
    assert digest(capture["path"]) == capture["sha256"]
    assert previous["frames"] == PAUSE and previous["cold_boot"] and not previous["savestate_loaded"]
    assert not previous["callback_errors"] and not any(v for k, v in previous.items() if k.startswith("synthetic_"))
    donor = previous["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == source["evidence"]["donor"]["sha256"]
    ROOT.mkdir()
    inputs = ROOT / "inputs.json"
    write(inputs, previous["scripted_input_schedule"])
    CONTROLLER.write_text("".join(json.dumps(action) + "\n" for action in ACTIONS), encoding="utf-8")
    stream = GrowingCommands(CONTROLLER)
    args, stdin = sys.argv, sys.stdin
    try:
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "60000", "--inputs-json", str(inputs), "--battery-save", donor["source"],
            "--touchscreen", "--press-start", "-1", "--capture-every", "999999",
            "--pause-at", str(PAUSE)]
        sys.stdin = stream
        harness.main()
    finally:
        sys.argv, sys.stdin = args, stdin
        stream.close()
    assert digest(donor["source"]) == donor["source_sha256"]


if __name__ == "__main__":
    main()
