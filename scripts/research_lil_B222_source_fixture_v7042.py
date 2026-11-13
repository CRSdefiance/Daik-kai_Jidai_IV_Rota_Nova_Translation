"""Preserve all eighteen original B222 commands in a disclosed initialized source fixture."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_source_fixture_v7042')
SOURCE=Path('work/analysis/lil_B222_source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references.json')
ENTRY=Path('work/analysis/lil_B222_entry_v7039/source_EV2_B222_action_dependency_and_native_getter_binding.json')
ROM=Path('out/lil_B222_source_v7042_clean_Japanese_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();packet=read(SOURCE);entry=read(ENTRY)
    assert [(e['event_ID'],e['script_block'],e['action_index'],e['must_be_completed'],e['must_not_be_completed']) for e in entry['selected_B222_source_events']]==[(222,222,223,[89],[])]
    parent=NdsImage.open(packet['current_ROM']);clean=NdsImage.open('work/clean.nds');assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;original=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks;jp=original[222]
    inventory,_,_=scoped_inventory();init,_=inventory(parent.read_file('/__arm9__.bin'),current[22]);first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9 and sum(c['word']==0xA000 for c in init[:9])==4
    prelude=current[22][8:first];assert prelude==original[22][8:first]
    end=8+struct.unpack_from('<H',jp,4)[0];assert len(jp)==end==1112 and jp[1108:]==bytes(4)
    logical=bytearray(current[22][:8]+prelude+jp[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
    assert len(commands)==27 and len(speeches)==16 and {c['word'] for c in commands if c['offset']>=56}=={0x4000,0xA000,0}
    assert sum(c['word']==0xA000 for c in commands)==5 and sum(c['word']==0 for c in commands)==1
    objects=[];texts=[]
    for command in packet['blocks'][0]['all_clean_native_commands']:
        at=command['offset']+48;mapped=next(c for c in commands if c['offset']==at)
        assert mapped['whole_command_hex']==command['whole_command_hex'] and mapped['native_extent']==command['native_extent'] and mapped['ancestor_0100_offsets']==[]
        row=next((r for r in packet['records'] if r['source_reference']['header_offset']==command['offset']),None)
        objects.append(dict(source_block=222,source_offset=command['offset'],source_word=command['word'],fixture_offset=at,native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex'],text_ID=None if row is None else row['id']))
        if row is not None:texts.append(dict(id=row['id'],source_block=222,source_record_index=row['source_record_index'],fixture_command_offset=at,source_selector=row['source_selector'],native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(packet['current_ROM']);image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM)
    saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    fixture=dict(case='clean_Japanese',source_block=222,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),
        original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,explicitly_excluded_original_commands=[],all27_stored_fixture_commands=commands)
    ROOT.mkdir(parents=True);save(ROOT/'complete_B222_source_B22_fixture.json',dict(parent=packet['current_ROM'],parent_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fixtures=[fixture],
        all18_source_commands_plus9_original_initializers_stored=True,original_clean_B22_initializers_byte_exact=True,original_event222_requires89_not_forced=True,
        source_controls_roster_funds_RNG_results_and_effects_not_forced=True,initialized_fixture_Amsterdam_not_natural_Japan_event222_activation_or_earned_progress=True,
        no_save_state_or_RAM_fixture=True,not_registered_candidate_or_release_parent=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ENTRY,Path(__file__)]},full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    added=dict(path=str(ROM.resolve()),reason='Complete B222 sixteen-speech sunset/Noritsune/armor clean-source fixture;all18 controls and original9 initializers. Event222 requires89;not forced or naturally selected. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    data=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before)
    assert pins.read_bytes()==before and json.loads(data)[:-1]==values
    with pins.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(new_pins=[added],all_prior_pins_preserved=True,before_sha256=sha(before),after_sha256=sha(data),ROMs_deleted=0,full_goal_complete=False))
    print('B222 whole source fixture pinned:18 original+9 original initializer commands,16 speeches. Requires89 remains unforced;initialized Amsterdam test is not natural Japan activation.',flush=True)
