"""Display the complete reviewed block with the same original initializer as the source fixture."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import derive
from scripts.prepare_lil_B197_research_v5676 import PARENT,ROM as REFERENCE,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_English_fixture_v5682')
ROM=Path('out/lil_B197_English_v5682_reviewed_English_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists()
    plan=read(PLAN);spec=plan['blocks'][0];doc=read(plan['manuscript']);packet=read(doc['source_context'])
    japanese=read('work/analysis/lil_B197_source_fixture_v5658/complete_B197_source_B22_fixture.json')
    parent,reference=[NdsImage.open(p) for p in [PARENT,REFERENCE]];arm=parent.read_file('/__arm9__.bin')
    assert sha(PARENT.read_bytes())==packet['current_ROM_sha256']==plan['candidate_sha256']==japanese['parent_sha256']
    assert arm==reference.read_file('/__arm9__.bin')
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks
    reviewed=IlnkContainer.parse(reference.read_file('/data/SC2.DK4')).blocks[197]
    assert reviewed==Path(spec['research_block']).read_bytes() and sha(reviewed)==spec['research_block_sha256']
    inventory,_,_=scoped_inventory();init,_=inventory(arm,current[22]);first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9 and sum(c['word']==0xA000 for c in init[:9])==4
    prelude=current[22][8:first];assert prelude.hex()==japanese['fixtures'][0]['original_B22_prelude_hex']
    end=8+struct.unpack_from('<H',reviewed,4)[0];assert len(reviewed)==1004 and end==1002 and reviewed[end:]==bytes(2)
    logical=bytearray(current[22][:8]+prelude+reviewed[8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4);commands,speeches=inventory(arm,target)
    assert len(commands)==48 and len(speeches)==21 and sum(c['word']==0x2200 for c in commands)==1
    assert sum(c['word']==0xA000 for c in commands)==9 and sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==6
    originals=packet['blocks'][0]['all_current_native_commands'];objects=[];texts=[]
    final_commands,_=inventory(arm,reviewed)
    for mapping,c in zip(spec['command_map'],final_commands,strict=True):
        assert mapping['word']==c['word'] and mapping['new_offset']==c['offset']
        at=c['offset']+first-8;new=next(v for v in commands if v['offset']==at)
        assert new['word']==c['word'] and new['whole_command_hex']==c['whole_command_hex']
        assert new['ancestor_0100_offsets']==[a+first-8 for a in c['ancestor_0100_offsets']]
        source_offset=mapping['old_offset'];r=next((r for r in packet['records'] if r['source_reference']['header_offset']==source_offset),None)
        objects.append(dict(source_block=197,source_offset=source_offset,reviewed_offset=c['offset'],source_word=c['word'],fixture_offset=at,native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex'],text_ID=None if r is None else r['id']))
        if r is not None:texts.append(dict(id=r['id'],source_block=197,source_record_index=r['source_record_index'],fixture_command_offset=at,source_selector=r['source_selector'],native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(PARENT);image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM)
    saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    fixture=dict(case='reviewed_English',source_block=197,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,explicitly_excluded_original_commands=[],all48_stored_fixture_commands=commands)
    ROOT.mkdir(parents=True);save(ROOT/'complete_B197_reviewed_English_B22_fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),source_context=doc['source_context'],source_context_sha256=sha(Path(doc['source_context']).read_bytes()),
        reference_ROM=str(REFERENCE),reference_ROM_sha256=sha(REFERENCE.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),fixtures=[fixture],
        all39_original_commands_with_reviewed_prose_and9_identical_original_init_commands_stored=True,
        all_original_branches_menu_47xx_effects_and_end_retained_without_omission=True,
        no_funds_roster_RNG_predicate_or_effect_result_forcing=True,
        same_B22_content_fixture_as_Japanese_not_natural_event197_activation_or_original_location=True,
        no_savestate_or_RAM_fixture=True,not_registered_candidate_or_new_release_parent=True,
        original_runtime_and_all335_other_blocks_and_files_components_preserved=True,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='B197 complete reviewed-English content fixture;all commands and prior ROMs preserved.SHA256 '+sha(ROM.read_bytes())))
    data=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(before)
    assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,before_sha256=sha(before),after_sha256=sha(data),ROMs_deleted=0))
    tool=derive('scripts/run_lil_B197_source_fixture_v5659.py','scripts/run_lil_B197_English_fixture_v5683.py',{
        'clean_Japanese':'reviewed_English','source_fixture_v5658':'English_fixture_v5682','complete_B197_source_B22_fixture':'complete_B197_reviewed_English_B22_fixture',
        'source_run_v5659':'English_run_v5683','source_v5659':'English_v5683'})
    save(ROOT/'source_locked_ordinary_input_English_runner.json',dict(tool=tool,all_frontend_input_frames_and_buttons_unchanged=True))
    print('Pinned complete English B22 fixture:39 reviewed source commands+9 identical initializers.Only B22 changes;ordinary input runner ready.No source conditions forced.')
