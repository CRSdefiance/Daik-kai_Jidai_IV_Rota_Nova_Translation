"""Prepare focused ordinary-input B175 paired cold boots and pin both fixture ROMs."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_display_tools_v4532')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/run_lil_B174_display_fixture_v4488.py','scripts/run_lil_B175_display_fixture_v4533.py',{
        'B174':'B175','lil_B174':'lil_B175','display_fixture_v4487':'display_fixture_v4531',
        'complete_effect_preserving_B22_fixtures':'complete_B175_B22_fixtures',
        'display_run_v4488':'display_run_v4533','display_v4488':'display_v4533',
        "'displayed_original_source_block':174":"'displayed_original_source_block':175",
        'source_event174_not_selected':'source_event175_not_selected',
        'all_source_commands_presentations_resource_predicate_optional_Emilio_four_spans_two_A000s_and_C200_retained':
            'all_source39_commands_23_progressive9_FE_resource_three_presentations_C200_and_two_ends_retained',
    })
    fixture_path=Path('work/analysis/lil_B175_display_fixture_v4531/complete_B175_B22_fixtures.json');fixture=read(fixture_path)
    pinpath=Path('translations/rom_retention_pins.json');before=pinpath.read_bytes();pins=read(pinpath);added=[]
    for f in fixture['fixtures']:
        rom=Path(f['research_ROM']);assert sha(rom.read_bytes())==f['research_ROM_sha256']
        assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
        added.append(dict(path=str(rom.resolve()),reason='B175 paired complete-content fixture;preserve for ongoing actual/reference/release work. No pruning. SHA-256 '+f['research_ROM_sha256']))
    data=(json.dumps(pins+added,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);(ROOT/'pins.before.json').write_bytes(before);(ROOT/'pins.planned.json').write_bytes(data)
    assert sha(pinpath.read_bytes())==sha(before) and json.loads(data)[:-2]==pins
    with pinpath.open('r+b') as stream:
        stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    assert pinpath.read_bytes()==data
    save(ROOT/'runner_and_pin_receipt.json',dict(tool=tool,fixture_manifest=str(fixture_path),fixture_manifest_sha256=sha(fixture_path.read_bytes()),
        source_speeches=32,progressive=23,FE=9,source_commands=39,stored_fixture_commands=48,frames=16001,new_pins=2,
        all_prior_pins_preserved=True,ROMs_deleted=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared B175 ordinary-input paired16001-frame runner and pinned both fixtures;all earlier pins/ROMs preserved.')
