"""Pin the verified cumulative image and its exact clean-input reconstruction."""
import json,os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_retention_v6112')
if __name__=='__main__':
    assert not ROOT.exists()
    release=read('work/analysis/shachihoko_release_v6111/registered_release_verification.json')
    target=Path('translations/rom_retention_pins.json');before=target.read_bytes();old=json.loads(before);added=[]
    for key in ['candidate','exact_patch_reconstruction']:
        p=Path(release[key]);assert sha(p.read_bytes())==release['candidate_sha256']
        assert not any(Path(r['path']).resolve()==p.resolve() for r in old)
        added.append(dict(path=str(p.resolve()),reason='Verified cumulative V6110 or exact clean-input reconstruction. Preserve every ROM. SHA256 '+release['candidate_sha256']))
    data=(json.dumps(old+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    assert json.loads(data)[:-2]==old
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert target.read_bytes()==before
    with target.open('r+b') as f:f.write(data);f.truncate();f.flush();os.fsync(f.fileno())
    assert target.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(new_pins=added,all_prior_pins_preserved=True,ROMs_deleted=0,before_sha256=sha(before),after_sha256=sha(data),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V6110 and exact reconstruction pinned;all prior ROMs and pins preserved.')
