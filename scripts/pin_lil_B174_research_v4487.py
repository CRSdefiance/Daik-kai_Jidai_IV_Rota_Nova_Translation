"""Append explicit B174 research pins; preserve every earlier pin and ROM."""
from pathlib import Path
import os
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_research_pins_v4487')
if __name__=='__main__':
    assert not ROOT.exists()
    path=Path('translations/rom_retention_pins.json');before=path.read_bytes();pins=read(path)
    previous=list(pins);fixture=read('work/analysis/lil_B174_display_fixture_v4487/complete_effect_preserving_B22_fixtures.json')
    source=read('work/analysis/lil_B174_research_v4482/research_image_receipt.json')
    files=[Path(source['research_ROM']),*[Path(row['research_ROM']) for row in fixture['fixtures']]]
    assert len(files)==3
    known={str(Path(row['path']).resolve()).casefold() for row in pins};added=[]
    for file in files:
        absolute=str(file.resolve());assert file.is_file()
        if absolute.casefold() in known:continue
        row=dict(path=absolute,reason='B174 full-command source/current research evidence, not a release parent. Preserve every ROM; no pruning. SHA-256 '+sha(file.read_bytes()))
        pins.append(row);added.append(row);known.add(absolute.casefold())
    assert pins[:len(previous)]==previous and len(added)==3
    import json
    data=(json.dumps(pins,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert path.read_bytes()==before
    with path.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    assert path.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(pins_added=added,all_previous_pins_preserved=True,ROMs_deleted=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned all3 B174 reference/content ROMs; every previous pin preserved, zero deletions.')
