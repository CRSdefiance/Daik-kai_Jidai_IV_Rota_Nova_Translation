"""Focused original constructor fixture for the full19-character high-price label;no story credit."""
import inspect,struct,json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_long_menu_fixture_v6283');ROM=Path('out/lil_B206_long_menu_v6283_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();doc=read('translations/lil_B206_choice_manuscript_v1.json');parent=NdsImage.open(doc['current_ROM']);arm=parent.read_file('/__arm9__.bin')
    vm=checked_text(inspect.getsource(original.choice_vm),{'pointer, 32':'pointer, len(object_bytes)','96':'VM_GUARD_BYTES'});env={**original.__dict__,'VM_GUARD_BYTES':256};exec(compile(vm,__file__+'::source-original-VM','exec'),env)
    menu_cases=[]
    for offset in [852,1020]:
        labels=[r['english'].encode('ascii') for r in doc['records'] if r['command_offset']==offset];assert len(labels)==2
        chunks=[];offsets=[];cursor=0
        for label in labels:
            assert label.strip()==label and b'\n' not in label;offsets.append(cursor);chunk=label+b'\0';chunk+=b'\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
        value=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks);result=env['choice_vm'](arm,value);menu_cases.append(dict(source_offset=offset,object_hex=value.hex(),labels=[x.decode() for x in labels],native_VM=result,width_px=result['minimum_width_units']*6))
    assert [r['width_px'] for r in menu_cases]==[48,114]
    bank=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;inventory,_,_=scoped_inventory();commands,_=inventory(arm,bank[22]);first=next(c['offset'] for c in commands if c['word']==0x4000);assert first==56 and len(commands[:9])==9 and sum(c['word']==0xA000 for c in commands[:9])==4
    selected=menu_cases[1];value=bytes.fromhex(selected['object_hex']);raw=bytearray(bank[22][:8]+bank[22][8:first]+value+bytes(4));struct.pack_into('<H',raw,4,len(raw)-8);raw=bytes(raw)+bytes(-len(raw)%4);walk,speech=inventory(arm,raw);assert len(walk)==11 and not speech and walk[-2]['word']==0x2100 and walk[-1]['word']==0
    image=NdsImage.open(doc['current_ROM']);blocks=list(bank);blocks[22]=raw;image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM);saved=NdsImage.open(ROM);assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    ROOT.mkdir(parents=True);save(ROOT/'focused_typed_menu_constructor_fixture.json',dict(parent=doc['current_ROM'],parent_sha256=doc['current_ROM_sha256'],all_two_reviewed_menu_VM_and_width_cases=menu_cases,fixtures=[dict(case='reviewed',research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block_hex=raw.hex(),all11_fixture_commands=walk,typed_menu_offset=56,typed_menu_object_hex=value.hex(),logical_menu_width_px=114,source_B206_menu_offset=1020)],original_B22_initializers_preserved=True,no_B206_story_or_branch_or_effect_or_natural_event_coverage=True,no_savestate_funds_roster_RNG_or_RAM_fixture=True,source_owned_VM_adapter=vm,new_review_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    base=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json');assert sha(base.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541';save(ROOT/'inputs.json',read(base)+[dict(start=3200,duration=5,buttons=['DOWN'])])
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values);values.append(dict(path=str(ROM.resolve()),reason='B206 original long-menu constructor/backing/complete-glyph risk research;preserve every ROM. SHA256 '+sha(ROM.read_bytes())));data=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as f:f.write(data);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,ROMs_deleted=0,full_goal_complete=False));print('Full second-menu constructor fixture pinned:114px native logical width,11 commands,no story/effect coverage or wording change.')
