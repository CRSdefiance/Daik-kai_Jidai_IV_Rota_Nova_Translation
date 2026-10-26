"""Protect cumulative/research/reconstruction ROMs; never prune generated artifacts."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    target = Path('translations/rom_retention_pins.json')
    pins = read(target)
    before = list(pins)
    known = {str(Path(pin['path']).resolve()) for pin in pins}
    paths = [Path('out/all_routes_combined_v4353_candidate.nds'),
        Path('out/lil_B171_reference_v4335_RESEARCH_ONLY.nds'),
        Path('out/lil_B171_display_v4340_clean_Japanese_RESEARCH_ONLY.nds'),
        Path('out/lil_B171_display_v4340_reviewed_English_RESEARCH_ONLY.nds'),
        Path('work/analysis/lil_B171_release_v4354/patch_reconstruction_RESEARCH_ONLY.nds')]
    added = []
    for path in paths:
        assert path.is_file()
        absolute = str(path.resolve())
        if absolute not in known:
            entry = dict(path=absolute, reason='B171 V4353 cumulative, exact reconstruction or disclosed research evidence; preserve all generated ROMs under active user goal. SHA-256 ' + sha(path.read_bytes()))
            pins.append(entry)
            added.append(entry)
            known.add(absolute)
    assert pins[:len(before)] == before
    import json,os
    data=(json.dumps(pins,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    assert len(data)>=target.stat().st_size
    with target.open('r+b') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    print(dict(new_pins=len(added), all_earlier_pins_preserved=True, ROMs_deleted=0))
