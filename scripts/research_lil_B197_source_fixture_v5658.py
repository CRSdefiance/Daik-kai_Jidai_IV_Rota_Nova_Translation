"""Retain the entire clean B197 in one disclosed B22 source-behavior fixture."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_source_fixture_v5658')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
ROM=Path('out/lil_B197_source_v5658_clean_Japanese_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();packet=read(SOURCE)
    parent=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin')
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[197]
    inventory,_,_=scoped_inventory();init,_=inventory(arm,current[22]);first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9 and sum(c['word']==0xA000 for c in init[:9])==4
    end=8+struct.unpack_from('<H',jp,4)[0];assert len(jp)==880 and end==878 and jp[end:]==bytes(2)
    prelude=current[22][8:first];logical=bytearray(current[22][:8]+prelude+jp[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(arm,target)
    assert len(commands)==48 and len(speeches)==21 and sum(c['word']==0x2200 for c in commands)==1
    assert sum(c['word']==0xA000 for c in commands)==9 and sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==6
    objects=[];texts=[];group=packet['blocks'][0]
    for c in group['all_clean_native_commands']:
        at=c['offset']+first-8;new=next(v for v in commands if v['offset']==at)
        assert new['word']==c['word'] and new['whole_command_hex']==c['whole_command_hex']
        assert new['ancestor_0100_offsets']==[a+first-8 for a in c['ancestor_0100_offsets']]
        r=next((r for r in packet['records'] if r['source_reference']['header_offset']==c['offset']),None)
        objects.append(dict(source_block=197,source_offset=c['offset'],source_word=c['word'],fixture_offset=at,native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex'],text_ID=None if r is None else r['id']))
        if r is not None:texts.append(dict(id=r['id'],source_block=197,source_record_index=r['source_record_index'],fixture_command_offset=at,source_selector=r['source_selector'],native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(packet['current_ROM']);image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM)
    saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    fixture=dict(case='clean_Japanese',source_block=197,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,explicitly_excluded_original_commands=[],all48_stored_fixture_commands=commands)
    ROOT.mkdir(parents=True);save(ROOT/'complete_B197_source_B22_fixture.json',dict(parent=packet['current_ROM'],parent_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fixtures=[fixture],
        all39_source_commands_and9_original_init_commands_stored=True,source_all_speech_branches_menu_47xx_effects_and_end_retained_without_omission=True,
        source_conditions_RNG_funds_roster_and_effect_results_not_forced=True,source_event197_not_naturally_selected_or_eligibility_earned=True,
        initialized_fixture_town_is_Amsterdam_not_original_event_location=True,no_save_state_or_RAM_fixture=True,not_registered_candidate_or_new_release_parent=True,
        original_runtime_and_all335_other_blocks_and_files_components_preserved=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='B197 complete clean-source branch/menu/47xx behavior fixture;preserve every ROM.SHA256 '+sha(ROM.read_bytes())))
    data=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before)
    assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,before_sha256=sha(before),after_sha256=sha(data),ROMs_deleted=0,full_goal_complete=False))
    print('Pinned one B197 clean-source fixture:all39 original+9 init commands,three choices/six relative sites,all effects and short47xx controls retained.No source results forced;not a release.')
