"""Keep the whole clean B204 content fixture while testing coordinated item data and ordinary menus."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_item_menu_fixture_v6103')
SOURCE=Path('work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json')
COORD=Path('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json')
ROM=Path('out/shachihoko_item116_menu_v6103_clean_Japanese_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();source,coord=map(read,[SOURCE,COORD]);original=source['fixtures'][0];assert sha(Path(original['research_ROM']).read_bytes())==original['research_ROM_sha256']
    parent=NdsImage.open(coord['research_ROM']);jp=NdsImage.open(original['research_ROM']);image=NdsImage.open(coord['research_ROM']);image.replace_file('/data/SC2.DK4',jp.read_file('/data/SC2.DK4'));image.save(ROM);after=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if after.read_file(p)!=v]==['/data/SC2.DK4'] and all(after.read_file(p)==v for p,v in parent.iter_components())
    old,new=[IlnkContainer.parse(r.read_file('/data/SC2.DK4')).blocks for r in [parent,after]];assert [i for i,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[22]
    result=deepcopy(source);result.update(parent=coord['research_ROM'],parent_sha256=coord['research_ROM_sha256'],original_source_fixture=str(SOURCE),original_source_fixture_sha256=sha(SOURCE.read_bytes()),coordinated_item_receipt=str(COORD),coordinated_item_receipt_sha256=sha(COORD.read_bytes()),
        ordinary_menu_input_after_source_scene_planned=True,no_inventory_roster_money_RNG_or_other_RAM_fixture=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False)
    result['fixtures'][0].update(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()))
    ROOT.mkdir(parents=True);save(ROOT/'complete_B204_source_B22_fixture_with_coordinated_item_data.json',result)
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Whole clean B204 content fixture with coordinated item116 name/description;ordinary item menu gameplay research. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw);assert pins.read_bytes()==raw
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),ROMs_deleted=0,full_goal_complete=False))
    print('Pinned complete Japanese B204+original initializers/coordinated item data fixture;only B22 differs from6094 research. Ordinary menu navigation pending;no RAM inventory fixture.')
