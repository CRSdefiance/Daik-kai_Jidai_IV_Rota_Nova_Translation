"""Stage the in-place bargaining revision and replay the ordinary controls."""

from argparse import ArgumentParser
import sys

from dk4tool.formats.ilnk import IlnkContainer
from scripts import headless_desmume_v193 as harness
from scripts import preflight_lisbon_guild_bargaining_20261125 as draft
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


play, current = draft.review.play, draft.current
ROOT = play.ROOT.with_name("editorial_20261125_guild_bargaining_revision")
ROM = ROOT / "Guild_Bargaining_STAGED.nds"
STAGED = ROOT / "unregistered_replay_manifest.json"
CAPTURE = ROOT / "paired"
FRAMES = (37300, 37540, 37780, 38020, 38260, 38500, 38740, 38980, 39220, 39460, 39700, 39940,
          40180, 40420, 40660, 40900, 41140, 41380, 41620, 41860, 42100, 42340, 42580, 42820, 43060)
REVISED_HOLDS = {39700: 1080, 41860: 1092}


def stage():
    base, proposed = map(read, (current.RELEASE, draft.OUT))
    assert proposed["candidate_sha256"] == base["candidate_sha256"] == digest(current.ROM)
    image = NdsImage.open(current.ROM)
    common = image.read_file(current.COMMON)
    assert sha256(common).hexdigest() == base["target_COMMON_sha256"]
    blocks = list(IlnkContainer.parse(common).blocks)
    assert set(map(int, proposed["allocations"])) == draft.DRAFTS.keys()
    for slot in proposed["allocations"].values():
        block, lo, hi = (slot[k] for k in ("block", "start", "end"))
        a, b = (bytes.fromhex(slot[k]) for k in ("before", "after"))
        assert len(a) == len(b) == hi - lo and blocks[block][lo:hi] == a
        blocks[block] = blocks[block][:lo] + b + blocks[block][hi:]
    archive = IlnkContainer(blocks).to_bytes()
    assert sha256(archive).hexdigest() == proposed["proposed_COMMON_sha256"]
    image.replace_file(current.COMMON, archive)
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(current.COMMON, common)
    assert sha256(image.rom.save()).hexdigest() == base["candidate_sha256"]
    write(STAGED, dict(candidate=reference(ROM), parent=reference(current.ROM),
                       target_COMMON_sha256=proposed["proposed_COMMON_sha256"], proposal=reference(draft.OUT),
                       exact_parent_inverse=True, unregistered_staged_replay=True))


def capture():
    stored, terminal = map(read, (STAGED, play.ROOT / "terminal.json"))
    assert terminal["candidate_sha256"] == stored["parent"]["sha256"]
    assert reference(ROM) == stored["candidate"] and stored["proposal"] == reference(draft.OUT)
    source = play.ROOT / "capture/capture_report.json"
    assert terminal["evidence"][str(source)] == digest(source)
    baseline = read(source)
    assert baseline["frames"] == terminal["total_frames"] == FRAMES[-1]
    assert baseline["cold_boot"] and not baseline["savestate_loaded"] and not baseline["callback_errors"]
    assert not any(value for key, value in baseline.items() if key.startswith("synthetic_"))
    donor = baseline["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    inputs = ROOT / "inputs.json"
    write(inputs, baseline["scripted_input_schedule"])
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(CAPTURE), "--frames", str(FRAMES[-1]),
                    "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                    "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, FRAMES)]
        harness.main()
    finally:
        sys.argv = argv
    report = read(CAPTURE / "capture_report.json")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["ROM_sha256"] == stored["candidate"]["sha256"] and report["frames"] == FRAMES[-1]
    assert report["scripted_input_schedule"] == baseline["scripted_input_schedule"]
    assert digest(donor["source"]) == donor["source_sha256"]
    print("Completed the proposed Guild replay with the same ordinary controls.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "capture"))
    globals()[parser.parse_args().action]()
