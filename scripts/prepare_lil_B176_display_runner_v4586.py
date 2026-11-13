"""Prepare paired 9001-frame B176 cold boots and retain both content ROMs."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_display_tools_v4586')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/run_lil_B175_display_fixture_v4533.py','scripts/run_lil_B176_display_fixture_v4587.py',{
        'B175':'B176','lil_B175':'lil_B176','display_fixture_v4531':'display_fixture_v4585',
        'display_run_v4533':'display_run_v4587','display_v4533':'display_v4587',
        'source_event175_not_selected':'source_event176_not_selected',
        "'displayed_original_source_block':175":"'displayed_original_source_block':176",
        'all_source39_commands_23_progressive9_FE_resource_three_presentations_C200_and_two_ends_retained':
            'all_source13_commands_9_progressive1_impersonal_FE_A000_C200_and_single_end_retained',
        'range(2600,15501,240)':'range(2600,8501,240)',
        "'requested_frames':16001":"'requested_frames':9001",
        "'--frames','16001'":"'--frames','9001'",
        'range(2350,16001,60)':'range(2350,9001,60)',
    })
    fixture_path=Path('work/analysis/lil_B176_display_fixture_v4585/complete_B176_B22_fixtures.json')
    fixture=read(fixture_path)
    pinpath=Path('translations/rom_retention_pins.json')
    before=pinpath.read_bytes();pins=read(pinpath);added=[]
    for f in fixture['fixtures']:
        rom=Path(f['research_ROM'])
        assert sha(rom.read_bytes())==f['research_ROM_sha256']
        assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
        added.append(dict(path=str(rom.resolve()),reason='B176 complete-content paired fixture;preserve all ROMs. No pruning. SHA-256 '+f['research_ROM_sha256']))
    assert len(added)==2
    data=(json.dumps(pins+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True)
    (ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert sha(pinpath.read_bytes())==sha(before) and json.loads(data)[:-2]==pins
    with pinpath.open('r+b') as stream:
        stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    assert pinpath.read_bytes()==data
    save(ROOT/'runner_and_pin_receipt.json',dict(tool=tool,fixture_manifest=str(fixture_path),fixture_manifest_sha256=sha(fixture_path.read_bytes()),
        source_speeches=10,progressive=9,FE=1,source_commands=13,stored_fixture_commands=22,
        source_A000=1,prelude_A000=4,frames=9001,new_pins=2,all_prior_pins_preserved=True,
        ROMs_deleted=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared B176 ordinary-input paired9001-frame runner and pinned both fixtures;all earlier pins/ROMs preserved.')
