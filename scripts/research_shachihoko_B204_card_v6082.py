"""Copy the complete source fixture with only the provisional item-name data change."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_B204_card_fixture_v6082')
SOURCE=Path('work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json')
ITEM=Path('work/analysis/shachihoko_item_name_research_v6079/research_image_receipt.json')
ROM=Path('out/shachihoko_B204_card_v6082_clean_Japanese_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();source,item=map(read,[SOURCE,ITEM]);original=source['fixtures'][0];assert sha(Path(original['research_ROM']).read_bytes())==original['research_ROM_sha256']
    parent=NdsImage.open(original['research_ROM']);image=NdsImage.open(original['research_ROM']);arm=NdsImage.open(item['research_ROM']).read_file('/__arm9__.bin');assert sha(arm)==item['target_ARM9_sha256']
    image.replace_file('/__arm9__.bin',arm);image.save(ROM);after=NdsImage.open(ROM)
    assert not [p for _,p,v in parent.iter_files() if after.read_file(p)!=v] and [p for p,v in parent.iter_components() if after.read_file(p)!=v]==['/__arm9__.bin']
    revised=deepcopy(source);revised['fixtures'][0].update(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()))
    revised.update(previous_source_fixture=str(SOURCE),previous_source_fixture_sha256=sha(SOURCE.read_bytes()),item_name_research=str(ITEM),item_name_research_sha256=sha(ITEM.read_bytes()),
        original_complete_B204_Japanese_and_nine_initializers_byte_exact=True,only_owned_item116_title_prefix_changes=True,
        not_registered_candidate_or_release_parent=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    ROOT.mkdir(parents=True);save(ROOT/'complete_B204_source_B22_fixture_with_provisional_item_name.json',revised)
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Complete clean B204 content fixture with provisional Shachihoko item116 label;display research only. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw);assert pins.read_bytes()==raw
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),ROMs_deleted=0,full_goal_complete=False))
    print('Complete Japanese B204 data-only name successor pinned;source fixture bytes and all other components preserved.')
