"""Reuse the already-proven complete Japanese B206 fixture with only its source-owned label changed."""
from pathlib import Path
from copy import deepcopy
import json,os
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_source_fixture_v6260');ROM=Path('out/shady_man_B206_source_v6260_RESEARCH_ONLY.nds')
OLD=Path('work/analysis/lil_B206_source_fixture_v6242/complete_B206_source_B22_fixture.json')
DATA=Path('work/analysis/shady_man_label_research_v6260/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();previous=read(OLD);data=read(DATA);old=previous['fixtures'][0];before=NdsImage.open(old['research_ROM'])
    assert sha(Path(old['research_ROM']).read_bytes())==old['research_ROM_sha256'];target=NdsImage.open(data['research_ROM']).read_file('/__arm9__.bin')
    image=NdsImage.open(old['research_ROM']);image.replace_file('/__arm9__.bin',target);image.save(ROM);after=NdsImage.open(ROM)
    assert all(after.read_file(p)==v for _,p,v in before.iter_files()) and [p for p,v in before.iter_components() if after.read_file(p)!=v]==['/__arm9__.bin']
    value=deepcopy(previous);fixture=value['fixtures'][0];fixture.update(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()))
    value.update(prior_source_fixture=str(OLD),prior_source_fixture_sha256=sha(OLD.read_bytes()),data_only_name_research=str(DATA),data_only_name_research_sha256=sha(DATA.read_bytes()),
      only_exact173_primary_string_prefix_differs_from_prior_source_fixture=True,source_scene_all51_commands_choices_item_effects_and_paragraphs_exact=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()))
    ROOT.mkdir(parents=True);save(ROOT/'complete_B206_source_B22_fixture.json',value)
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    values.append(dict(path=str(ROM.resolve()),reason='Shady Man source-bound complete Japanese B206 representative nameplate research;preserve all artifacts. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw)
    assert pins.read_bytes()==raw
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),all_prior_pins_and_ROMs_preserved=True,full_goal_complete=False))
    print('Complete Japanese B206 fixture pinned with Shady Man data only;all51 commands and earlier source prose remain exact.')
