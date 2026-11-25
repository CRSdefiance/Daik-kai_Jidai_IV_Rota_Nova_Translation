"""Complete reviewed B204 in the same initialized B22 context,with unforced inputs/state."""
import json,os,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prepare_lil_B204_references_v6135 import PARENT,PLAN
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_English_fixture_v6144')
SOURCE_FIXTURE=Path('work/analysis/shachihoko_item_menu_fixture_v6103/complete_B204_source_B22_fixture_with_coordinated_item_data.json')
ROM=Path('out/lil_B204_English_v6144_reviewed_English_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();source_fixture=read(SOURCE_FIXTURE)['fixtures'][0];plan=read(PLAN);packet=read(plan['source_context'])
    loader=read('work/analysis/lil_B204_loader_v6140/whole_SC2_and_B204_initial_entry_proof.json');census=read('work/analysis/lil_B204_reference_census_v6141/all26_commands_no_relative_sites_and_shipped_entry_census.json');controls=read('work/analysis/lil_B204_relocated_controls_v6143/all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves.json')
    assert loader['all336_whole_blocks_and672_modes_each_pass'] and census['all26_clean_current_target_commands_and_no_relative_sites_reexecuted'] and len(controls['relocated_dispatch_cases'])==20
    parent=NdsImage.open(PARENT);assert sha(PARENT.read_bytes())==plan['candidate_sha256']
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;bank=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks
    inventory,_,_=scoped_inventory();init,_=inventory(parent.read_file('/__arm9__.bin'),current[22]);first=next(c['offset'] for c in init if c['word']==0x4000);assert first==56
    prelude=current[22][8:first];assert prelude.hex()==source_fixture['original_B22_prelude_hex'] and len(init[:9])==9
    end=8+struct.unpack_from('<H',bank[204],4)[0];assert len(bank[204])==plan['blocks'][0]['research_bytes'] and end==plan['blocks'][0]['research_logical_end']
    logical=bytearray(current[22][:8]+prelude+bank[204][8:end]);struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target);native,_=inventory(parent.read_file('/__arm9__.bin'),bank[204])
    assert len(native)==26 and len(commands)==35 and len(speeches)==20 and sum(c['word']==0xA000 for c in commands)==5 and not any(c['word']==0x8000 for c in commands)
    objects=[];texts=[]
    for original,c,mapping in zip(packet['blocks'][0]['all_clean_native_commands'],native,plan['blocks'][0]['command_map'],strict=True):
        assert original['word']==c['word']==mapping['word'] and original['offset']==mapping['old_offset'] and c['offset']==mapping['new_offset']
        at=c['offset']+first-8;mapped=next(v for v in commands if v['offset']==at);assert mapped['whole_command_hex']==c['whole_command_hex'] and mapped['ancestor_0100_offsets']==[a+first-8 for a in c['ancestor_0100_offsets']]
        r=next((r for r in packet['records'] if r['source_reference']['header_offset']==original['offset']),None)
        objects.append(dict(source_block=204,source_offset=original['offset'],source_word=original['word'],fixture_offset=at,native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex'],text_ID=None if r is None else r['id']))
        if r is not None:texts.append(dict(id=r['id'],source_block=204,source_record_index=r['source_record_index'],fixture_command_offset=at,source_selector=r['source_selector'],native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(PARENT);image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM)
    saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks;assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    fixture=dict(case='reviewed_English',source_block=204,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,explicitly_excluded_original_commands=[],all35_stored_fixture_commands=commands)
    ROOT.mkdir(parents=True);save(ROOT/'complete_B204_English_B22_fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),source_fixture=str(SOURCE_FIXTURE),source_fixture_sha256=sha(SOURCE_FIXTURE.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),fixtures=[fixture],all26_source_commands_plus9_initializers_retained_without_omission=True,source_conditions_roster_funds_RNG_and_results_unforced=True,initialized_Amsterdam_B22_content_fixture_not_natural_event204_activation_or_original_location=True,not_registered_candidate_or_release_parent=True,producer_sha256=sha(Path(__file__).read_bytes()),new_review_credit=0,full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='Complete B204 reviewed-English castle/four-letter/transition fixture. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    data=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as f:f.write(data);f.truncate();f.flush();os.fsync(f.fileno())
    runner=derive('scripts/run_lil_B204_source_fixture_v6071.py','scripts/run_lil_B204_English_fixture_v6145.py',{
        'source_fixture_v6070':'English_fixture_v6144','complete_B204_source_B22_fixture':'complete_B204_English_B22_fixture',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",'source_run_v6071_clean_Japanese':'English_run_v6145_reviewed_English','source_v6071_clean_Japanese':'English_v6145_reviewed_English','B204 Japanese content':'B204 reviewed English content',
    })
    save(ROOT/'pin_and_runner_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,before_sha256=sha(before),after_sha256=sha(data),ROMs_deleted=0,prepared_runner=runner,full_goal_complete=False));print('Complete English B204 fixture pinned:26 source+9 initializer commands,20 objects,four FE letters,current coordinated item data. Ordinary source input;no forced state.')
