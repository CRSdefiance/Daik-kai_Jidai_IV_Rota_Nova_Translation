"""Preserve the cumulative candidate and exact reconstruction alongside every old ROM."""
import json,os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_retention_v5896')
if __name__=='__main__':
    assert not ROOT.exists();release=read('work/analysis/generic_speaker_labels_release_v5895/registered_release_verification.json')
    target=Path('translations/rom_retention_pins.json');before=target.read_bytes();pins=read(target);added=[]
    for key in ['candidate','exact_patch_reconstruction']:
        p=Path(release[key]);assert sha(p.read_bytes())==release['candidate_sha256']
        if not any(Path(r['path']).resolve()==p.resolve() for r in pins):added.append(dict(path=str(p.resolve()),reason='Verified three-label cumulative V5891 or exact clean-input reconstruction;preserve every generated ROM. SHA256 '+sha(p.read_bytes())))
    assert len(added)==2;data=(json.dumps(pins+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert target.read_bytes()==before and json.loads(data)[:-len(added)]==pins
    with target.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert target.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(new_pins=added,all_prior_pins_preserved=True,ROMs_deleted=0,all_prior_ROMs_translations_proofs_and_failures_preserved=True,
        before_sha256=sha(before),after_sha256=sha(data),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned V5891 and exact clean-input reconstruction;all prior pins preserved.No ROMs deleted.')
