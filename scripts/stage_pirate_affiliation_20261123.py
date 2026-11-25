"""Stage the source-locked Pirate affiliation edit with the active release guards."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_online_card_copy_20261123 as parent
from scripts.probe_pirate_affiliation_20261123 import ENGLISH, JAPANESE, SLOT
from scripts.reconcile_editorial_acceptance_20261123 import right_bound
from scripts.verify_pirate_panel_emulator_20261123 import REPORT as DISPLAY


base, native, ARM = parent.base, parent.native, parent.ARM
ROOT = Path(".codex-release-work/pirate_affiliation_20261123/staged")
ROM = ROOT / "Translation_DS_Pirate_Affiliation_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release, visual = map(base.load, (parent.RELEASE, DISPLAY))
    assert release["candidate_sha256"] == visual["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    assert visual["tested_full_nameplate"] and visual["complete_English_pixels_per_hold"] == 70
    assert base.digest(visual["sheet"]["path"]) == visual["sheet"]["sha256"]
    validate_natural_dialogue_batch(visual)
    row, = visual["records"]
    assert row["proposed_reference"] == {"offset": SLOT, "bytes": ENGLISH.hex(), "exclusive_end": SLOT + len(ENGLISH)}
    clean, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    source_arm, old_arm = (obj.read_file(ARM) for obj in (clean, target))
    assert native.digest(old_arm) == release["target_ARM9_sha256"]
    end = SLOT + len(JAPANESE)
    assert source_arm[SLOT:end] == old_arm[SLOT:end] == JAPANESE
    assert source_arm[0xBBFC:0xBC7C] == old_arm[0xBBFC:0xBC7C]
    new_arm = old_arm[:SLOT] + ENGLISH + old_arm[end:]
    assert len(new_arm) == len(old_arm) and new_arm[SLOT:end].endswith(b"\0\0")
    assert right_bound(old_arm, release["right_bound_configuration"]) == right_bound(new_arm, release["right_bound_configuration"])
    source, before = map(native.files, (clean, target))
    target.replace_file(ARM, new_arm)
    after = native.files(target)
    assert before.keys() == after.keys() and {asset for asset in before if before[asset] != after[asset]} == {ARM}
    guard = parent.parent.bind_registered_story_percent_guard(parent.guard_spec())(source, after)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(target.rom.save())
    target.replace_file(ARM, old_arm)
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    candidate = base.digest(ROM)
    bound = row | {"installed_reference": row["proposed_reference"] | {"candidate_sha256": candidate,
                "ARM9_sha256": native.digest(new_arm)}}
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=release["candidate_sha256"],
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(new_arm), changed_files=[ARM],
        target_COMMON_sha256=release["target_COMMON_sha256"], exact_parent_inverse=True,
        source25=guard, records=[bound], evidence={str(DISPLAY): base.digest(DISPLAY)}, staged_only=True))
    print(f"Staged {candidate} with only the six Pirate text bytes changed.")


def patch():
    assert not PATCH.exists() and not REBUILT.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof["candidate_sha256"] and base.digest(native.CLEAN) == proof["clean_sha256"]
    make_xdelta(native.CLEAN, ROM, PATCH)
    apply_xdelta(native.CLEAN, PATCH, REBUILT)
    assert base.digest(REBUILT) == proof["candidate_sha256"]
    print(f"Exact clean-input patch {base.digest(PATCH)}")


def startup():
    step = parent.playback.release_tools.startup
    FunctionType(step.__code__, step.__globals__ | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup"))
    globals()[parser.parse_args().action]()
