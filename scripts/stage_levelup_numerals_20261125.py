"""Route only the COMMON 336 stat-gain amount through the installed ASCII helper."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
import sys

from ndspy.code import MainCodeFile

from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, ITCM, NUMBER, compact_helper
from scripts import headless_desmume_v193 as harness
from scripts import register_lisbon_guild_bargaining_20261125 as current
from scripts import review_common_336_levelup_v1 as growth
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


ROOT = current.ROM.parent.with_name("editorial_20261125_levelup_numerals")
ROM = ROOT / "Levelup_Numerals_STAGED.nds"
PROOF = ROOT / "unregistered_replay_manifest.json"
CAPTURE = ROOT / "paired"
CALL = 0x0207E524
HOLD = 42580


def proposed_arm9(source, current_arm):
    start, end = growth.TEXT_SPAN
    assert source[start:end] == current_arm[start:end]
    helper = compact_helper()
    itcm = MainCodeFile(current_arm, BASE).sections[4]
    assert itcm.ramAddress == ITCM and len(itcm.data) == 4096
    assert bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    assert current_arm[NUMBER - BASE:NUMBER - BASE + 0x7C] == source[NUMBER - BASE:NUMBER - BASE + 0x7C]
    for row in read(growth.CONFIG)["owned_patches"]:
        raw = bytes.fromhex(row["after_hex"])
        offset = row["address"] - BASE
        assert current_arm[offset:offset + len(raw)] == raw
    offset = CALL - BASE
    before, after = (assemble(f"bl {target}", CALL) for target in (NUMBER, HELPER))
    assert len(before) == len(after) == 4 and current_arm[offset:offset + 4] == before
    revised = current_arm[:offset] + after + current_arm[offset + 4:]
    assert cache_plan(revised) == cache_plan(current_arm)
    return revised, dict(address=CALL, offset=offset, before_hex=before.hex(), after_hex=after.hex(),
        original_number_formatter=NUMBER, installed_ascii_helper=HELPER, ascii_helper_sha256=sha256(helper).hexdigest())


def stage():
    parent = read(current.RELEASE)
    assert digest(current.ROM) == parent["candidate_sha256"] and digest(REGISTRY) == parent["registry_sha256"]
    assert digest(CLEAN) == parent["clean_input_sha256"]
    source, image = map(NdsImage.open, (CLEAN, current.ROM))
    original, arm = (item.read_file(current.ARM) for item in (source, image))
    assert sha256(arm).hexdigest() == parent["target_ARM9_sha256"]
    commons = image.read_file(current.COMMON)
    assert sha256(commons).hexdigest() == parent["target_COMMON_sha256"]
    revised, edit = proposed_arm9(original, arm)
    image.replace_file(current.ARM, revised)
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(current.ARM, arm)
    assert sha256(image.rom.save()).hexdigest() == parent["candidate_sha256"]
    write(PROOF, dict(parent=reference(current.ROM), parent_release=reference(current.RELEASE), candidate=reference(ROM),
        target_ARM9_sha256=sha256(revised).hexdigest(), target_COMMON_sha256=parent["target_COMMON_sha256"],
        exact_parent_inverse=True, unregistered_staged_replay=True, edit=edit))
    print("Staged one ARM9 call and verified the whole-parent inverse.")


def capture():
    stored, earlier = map(read, (PROOF, current.gameplay.OUT))
    assert stored["parent"] == earlier["candidate"] == reference(current.ROM)
    assert stored["candidate"] == reference(ROM)
    inherited = earlier["replay"]
    assert inherited == reference(inherited["path"])
    baseline = read(inherited["path"])
    frames = current.replay.FRAMES
    assert baseline["ROM_sha256"] == stored["parent"]["sha256"] and baseline["frames"] == frames[-1]
    assert baseline["cold_boot"] and not baseline["savestate_loaded"] and not baseline["callback_errors"]
    assert not any(value for key, value in baseline.items() if key.startswith("synthetic_"))
    donor = baseline["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    inputs = ROOT / "inputs.json"
    write(inputs, baseline["scripted_input_schedule"])
    argv, stdin = sys.argv, sys.stdin
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(CAPTURE), "--frames", str(frames[-1]),
                    "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                    "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, frames),
                    "--pause-at", str(HOLD), "--dump-pause-ram"]
        sys.stdin = StringIO(dumps(dict(until=frames[-1], buttons=[])) + "\n" + dumps(dict(stop=True)) + "\n")
        harness.main()
    finally:
        sys.argv, sys.stdin = argv, stdin
    report = read(CAPTURE / "capture_report.json")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["ROM_sha256"] == stored["candidate"]["sha256"] and report["frames"] == frames[-1]
    assert report["scripted_input_schedule"] == baseline["scripted_input_schedule"]
    assert digest(donor["source"]) == donor["source_sha256"]
    print("Completed the stat-gain replay with the same ordinary Lisbon controls.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "capture"))
    globals()[parser.parse_args().action]()
