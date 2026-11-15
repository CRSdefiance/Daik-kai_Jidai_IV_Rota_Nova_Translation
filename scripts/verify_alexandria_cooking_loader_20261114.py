"""Exercise the original event loader on the four proposed Alexandria archives."""

from pathlib import Path

from scripts import verify_alexandria_cooking_assets_20261114 as assets
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.trace_event_script_sources_v727 import run as load_story
from scripts.verify_release_baseline import files
from scripts.verify_script_handoff_v732 import run as handoff


base, parent, stage = assets.base, assets.parent, assets.stage
ROOT = assets.WORK / "whole_image_loader"
ROM = ROOT / "Alexandria_all_routes_RESEARCH_ONLY.nds"
RECEIPT = ROOT / "whole_image_loader_receipt.json"


def main():
    assert not ROOT.exists()
    release, receipt = map(base.load, (parent.RELEASE, assets.RECEIPT))
    assert base.digest(parent.ROM) == release["candidate_sha256"] == receipt["candidate_sha256"]
    image, clean = map(base.NdsImage.open, (parent.ROM, stage.CLEAN))
    original = files(image)
    owned = set()
    for item in receipt["routes"]:
        name = item["file_path"]
        target = Path(item["proposed_archive"]).read_bytes()
        assert assets.edit.digest(original[name]) == item["source_archive_sha256"]
        assert assets.edit.digest(target) == item["proposed_archive_sha256"]
        image.replace_file(name, target)
        owned.add(name)
    target_files = files(image)
    assert original.keys() == target_files.keys()
    assert {path for path in original if original[path] != target_files[path]} == owned
    ROOT.mkdir()
    image.save(ROM)
    for path in owned:
        image.replace_file(path, original[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()

    image = base.NdsImage.open(ROM)
    arm, clean_arm = [im.read_file(stage.ARM) for im in (image, clean)]
    for a,b in ((0x23E94, 0x23F84), (0x23F4C, 0x24134), (0x24134, 0x24230), (0x2A510, 0x2A530)):
        assert arm[a:b] == clean_arm[a:b]
    entry_census = census(image)
    assert entry_census == census(base.NdsImage.open(parent.ROM))
    loaded = load_story(image, "Alexandria all four proposed archives")
    assert loaded["native_selected_action_cases"] == 1312 and loaded["complete_SC_loads_and_cache_hits"] == 1307
    load_path = ROOT / "whole_loads.json"
    base.save(load_path, loaded)
    parents = handoff(image, "Alexandria all four proposed archives", loaded)
    parent_path = ROOT / "original_parent_modes.json"
    base.save(parent_path, parents)
    base.save(RECEIPT, dict(candidate_sha256=release["candidate_sha256"], proposed_ROM=str(ROM),
        proposed_ROM_sha256=base.digest(ROM), exact_parent_ROM_inverse=True, verified_archives=sorted(owned),
        entry_census=entry_census, complete_native_loads=1307, parent_modes=2614,
        evidence={str(path):base.digest(path) for path in (load_path, parent_path, assets.RECEIPT, assets.REVIEW, Path(__file__))}))
    print("All 1,307 whole-block loads, 2,614 interpreter-entry cases, and the complete parent inverse passed.")


if __name__ == "__main__":
    main()

