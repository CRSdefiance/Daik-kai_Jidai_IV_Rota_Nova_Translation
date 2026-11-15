"""Protect the new cumulative build and all B167 research inputs; prune nothing."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__ == '__main__':
    target = Path('translations/rom_retention_pins.json')
    pins = read(target)
    paths = [Path('out/all_routes_combined_v4160_candidate.nds'),
        Path('out/lil_B167_reference_v4142_RESEARCH_ONLY.nds'),
        Path('out/lil_B167_display_v4147_clean_Japanese_RESEARCH_ONLY.nds'),
        Path('out/lil_B167_display_v4147_reviewed_English_RESEARCH_ONLY.nds'),
        Path('work/analysis/lil_B167_release_v4161/patch_reconstruction_RESEARCH_ONLY.nds')]
    old = list(pins)
    known = {str(Path(p['path']).resolve()) for p in pins}
    added = []
    for path in paths:
        assert path.exists()
        absolute = str(path.resolve())
        if absolute not in known:
            entry = dict(path=absolute,reason='B167 V4160 cumulative/reconstruction or disclosed research evidence; required for continued editorial work. Preserve all generated ROMs under the active user goal. SHA-256 '+sha(path.read_bytes()))
            pins.append(entry)
            added.append(entry)
            known.add(absolute)
    assert pins[:len(old)] == old
    save(target,pins)
    print(dict(new_pins=len(added),all_earlier_pins_preserved=True,ROMs_deleted=0))
