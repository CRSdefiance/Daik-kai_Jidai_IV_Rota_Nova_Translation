"""Preserve all B177 cumulative, exact-reconstruction and content-evidence ROMs."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_retention_v4659')
if __name__=='__main__':
    assert not ROOT.exists()
    target=Path('translations/rom_retention_pins.json');before=target.read_bytes();pins=read(target)
    original=list(pins);known={str(Path(p['path']).resolve()) for p in pins}
    release=read('work/analysis/lil_B177_release_v4656/registered_release_verification.json')
    paths=[Path(release['candidate']),Path('out/lil_B177_reference_v4630_RESEARCH_ONLY.nds'),
        Path('out/lil_B177_display_v4635_clean_Japanese_RESEARCH_ONLY.nds'),
        Path('out/lil_B177_display_v4635_reviewed_English_RESEARCH_ONLY.nds'),Path(release['exact_patch_reconstruction'])]
    assert paths[0].read_bytes()==paths[1].read_bytes()==paths[-1].read_bytes()
    added=[]
    for p in paths:
        assert p.is_file();absolute=str(p.resolve())
        if absolute not in known:
            item=dict(path=absolute,reason='B177 V4655 cumulative,exact reconstruction or disclosed research evidence;preserve every generated ROM under active user goal. SHA-256 '+sha(p.read_bytes()))
            pins.append(item);added.append(item);known.add(absolute)
    assert len(added)==2 and pins[:len(original)]==original
    data=(json.dumps(pins,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert target.read_bytes()==before
    with target.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    assert target.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(new_pins=2,all_prior_pins_preserved=True,ROMs_deleted=0,
        before_sha256=sha(before),after_sha256=sha(data),all5_B177_ROM_paths=[str(p) for p in paths],
        candidate_sha256=release['candidate_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Two cumulative/reconstruction pins added;all three previous B177 research pins and every earlier ROM preserved.')
