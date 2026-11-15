"""Pin both complete B178 content fixtures and correct an unexecuted audit summary label."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_display_tools_v4692')
assert not ROOT.exists()
tool=derive('scripts/audit_lil_B178_actual_v4694.py','scripts/audit_lil_B178_actual_v4694b.py',{
    'actual_panels=10':'actual_panels=13',
})
fixture_path=Path('work/analysis/lil_B178_display_fixture_v4691/complete_B178_B22_fixtures.json');fixture=read(fixture_path)
target=Path('translations/rom_retention_pins.json');before=target.read_bytes();pins=read(target);added=[]
for f in fixture['fixtures']:
    rom=Path(f['research_ROM']);assert sha(rom.read_bytes())==f['research_ROM_sha256']
    assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    added.append(dict(path=str(rom.resolve()),reason='B178 complete-content paired fixture;preserve every ROM. No pruning. SHA-256 '+f['research_ROM_sha256']))
assert len(added)==2
data=(json.dumps(pins+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
assert target.read_bytes()==before and json.loads(data)[:-2]==pins
with target.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
assert target.read_bytes()==data
save(ROOT/'runner_and_pin_receipt.json',dict(corrected_audit_tool=tool,fixture_manifest=str(fixture_path),fixture_manifest_sha256=sha(fixture_path.read_bytes()),
    source_speeches=13,progressive=12,FE=1,source_commands=16,stored_fixture_commands=25,source_A000=1,prelude_A000=4,
    frames=9001,new_pins=2,all_prior_pins_preserved=True,ROMs_deleted=0,new_emulator_runs=0,full_goal_complete=False))
print('Pinned both B178 fixtures;all earlier pins/ROMs preserved. Corrected13-panel audit summary before execution.')
