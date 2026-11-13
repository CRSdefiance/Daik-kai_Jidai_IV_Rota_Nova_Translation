"""Add the B175 reference pin while preserving every previous pin and ROM."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_reference_pin_v4526')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt_path=Path('work/analysis/lil_B175_research_v4526/research_image_receipt.json')
    receipt=read(receipt_path);rom=Path(receipt['research_ROM'])
    assert sha(rom.read_bytes())==receipt['research_ROM_sha256']
    path=Path('translations/rom_retention_pins.json');before=path.read_bytes();pins=read(path)
    resolved=str(rom.resolve())
    assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    after=pins+[dict(path=resolved,reason='B175 V4526 one-block reference;preserve for active contextual/native/actual/release work. No pruning. SHA-256 '+receipt['research_ROM_sha256'])]
    data=(json.dumps(after,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert sha(path.read_bytes())==sha(before) and json.loads(data)[:-1]==pins
    with path.open('r+b') as stream:
        stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    assert path.read_bytes()==data
    save(ROOT/'pin_receipt.json',dict(new_pins=1,all_prior_pins_preserved=True,ROMs_deleted=0,rom=resolved,
        rom_sha256=receipt['research_ROM_sha256'],receipt_sha256=sha(receipt_path.read_bytes()),
        before_sha256=sha(before),after_sha256=sha(data),full_goal_complete=False))
    print('Pinned B175 reference;all prior pins/ROMs preserved.')
