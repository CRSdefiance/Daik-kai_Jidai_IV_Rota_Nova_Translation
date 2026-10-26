"""Protect cumulative/research/reconstruction ROMs; never prune generated artifacts."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    target = Path('translations/rom_retention_pins.json')
    pins = read(target)
    before = list(pins)
    known = {str(Path(pin['path']).resolve()) for pin in pins}
    paths = [Path('out/all_routes_combined_v4204_candidate.nds'),
        Path('out/lil_B168_reference_v4193_RESEARCH_ONLY.nds'),
        Path('out/lil_B168_display_v4198_clean_Japanese_RESEARCH_ONLY.nds'),
        Path('out/lil_B168_display_v4198_reviewed_English_RESEARCH_ONLY.nds'),
        Path('work/analysis/lil_B168_release_v4205/patch_reconstruction_RESEARCH_ONLY.nds')]
    added = []
    for path in paths:
        assert path.is_file()
        absolute = str(path.resolve())
        if absolute not in known:
            entry = dict(path=absolute, reason='B168 V4204 cumulative, exact reconstruction or disclosed research evidence; preserve all generated ROMs under active user goal. SHA-256 ' + sha(path.read_bytes()))
            pins.append(entry)
            added.append(entry)
            known.add(absolute)
    assert pins[:len(before)] == before
    save(target, pins)
    print(dict(new_pins=len(added), all_earlier_pins_preserved=True, ROMs_deleted=0))
