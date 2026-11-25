"""Preserve the cumulative candidate,reconstruction and already pinned native reference."""
from pathlib import Path
import json,os
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier775_retention_v4991')
if __name__=='__main__':
    assert not ROOT.exists();release=read('work/analysis/earlier775_release_v4988/registered_release_verification.json')
    paths=[Path(release['candidate']),Path(release['exact_patch_reconstruction']),Path('out/recommendation775_reference_v4983_RESEARCH_ONLY.nds')]
    assert paths[0].read_bytes()==paths[1].read_bytes()==paths[2].read_bytes()
    target=Path('translations/rom_retention_pins.json');before=target.read_bytes();old=read(target);known={Path(r['path']).resolve() for r in old};added=[]
    for p in paths:
        if p.resolve() not in known:added.append(dict(path=str(p.resolve()),reason='V4987 cumulative775 reflow or exact reconstruction;preserve every generated ROM. SHA256 '+sha(p.read_bytes())));known.add(p.resolve())
    assert len(added)==2;data=(json.dumps(old+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert target.read_bytes()==before
    with target.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert read(target)[:-2]==old and target.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(new_pins=2,all_prior_pins_preserved=True,ROMs_deleted=0,paths=[str(p) for p in paths],
        before_sha256=sha(before),after_sha256=sha(data),candidate_sha256=release['candidate_sha256'],full_goal_complete=False))
