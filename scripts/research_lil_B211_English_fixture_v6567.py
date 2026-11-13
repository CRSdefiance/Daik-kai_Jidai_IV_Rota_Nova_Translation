"""Research complete B211 English page behavior in the same B22 context with original branches."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.create_lil_B211_reference_v6566 import PARENT,PLAN,STORED
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_English_fixture_v6567')
SOURCE_FIXTURE=Path('work/analysis/lil_B211_source_fixture_v6555/complete_B211_source_B22_fixture.json')
ROM=Path('out/lil_B211_English_v6567_reviewed_English_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();source_fixture=read(SOURCE_FIXTURE)['fixtures'][0];plan,stored=read(PLAN),read(STORED);packet=read(plan['source_context']);reference=read('work/analysis/lil_B211_reference_v6566/research_image_receipt.json')
    assert stored['relocation_plan_sha256']==reference['source_relocation_plan_sha256']==sha(PLAN.read_bytes()) and stored['all_final_stored_targets_equal_reviewed_complete_native_ink']
    parent=NdsImage.open(PARENT);assert sha(PARENT.read_bytes())==plan['candidate_sha256'];current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks;bank=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks
    inventory,_,_=scoped_inventory();init,_=inventory(parent.read_file('/__arm9__.bin'),current[22]);first=next(c['offset'] for c in init if c['word']==0x4000);assert first==56 and len(init[:9])==9
    prelude=current[22][8:first];assert prelude.hex()==source_fixture['original_B22_prelude_hex'];end=8+struct.unpack_from('<H',bank[211],4)[0];assert end==726 and len(bank[211])==728
    logical=bytearray(current[22][:8]+prelude+bank[211][8:end]);struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target);native,_=inventory(parent.read_file('/__arm9__.bin'),bank[211]);assert len(native)==14 and len(commands)==23 and len(speeches)==12
    assert sum(c['word']==0x4100 for c in commands)==0 and sum(c['word']==0x8000 for c in commands)==0 and sum(c['word']==0xA000 for c in commands)==5
    objects=[];texts=[]
    for original,c,mapping in zip(packet['blocks'][0]['all_clean_native_commands'],native,plan['blocks'][0]['command_map'],strict=True):
        assert original['word']==c['word']==mapping['word'] and original['offset']==mapping['old_offset'] and c['offset']==mapping['new_offset'];at=c['offset']+first-8;mapped=next(v for v in commands if v['offset']==at)
        assert mapped['whole_command_hex']==c['whole_command_hex'] and mapped['ancestor_0100_offsets']==[a+first-8 for a in c['ancestor_0100_offsets']]
        row=next((r for r in packet['records'] if r['source_reference']['header_offset']==original['offset']),None)
        objects.append(dict(source_block=211,source_offset=original['offset'],source_word=original['word'],fixture_offset=at,native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex'],text_ID=None if row is None else row['id']))
        if row is not None:texts.append(dict(id=row['id'],source_block=211,source_record_index=row['source_record_index'],fixture_command_offset=at,source_selector=row['source_selector'],native_extent=c['native_extent'],whole_command_hex=c['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(PARENT);image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM);saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22] and [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    # Both source and English fixtures use V6541 as parent. Only B22 differs between them.
    sourceim=NdsImage.open(source_fixture['research_ROM']);sourceblocks=IlnkContainer.parse(sourceim.read_file('/data/SC2.DK4')).blocks;assert [i for i,(a,b) in enumerate(zip(sourceblocks,after,strict=True)) if a!=b]==[22]
    ROOT.mkdir(parents=True);fixture=dict(case='reviewed_English',source_block=211,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,source_typed_actor_style_records=packet['typed_actor_style_records'],relocated_actor_style_commands=plan['blocks'][0]['actor_style_commands'],explicitly_excluded_original_commands=[],all23_stored_fixture_commands=commands)
    save(ROOT/'complete_B211_English_B22_fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),source_fixture=str(SOURCE_FIXTURE),source_fixture_sha256=sha(SOURCE_FIXTURE.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),fixtures=[fixture],all14_source_commands_plus9_initializers_retained_without_omission=True,all12_original_speeches_nine_progressive_three_FE_one_FI_A000_and_end_unforced=True,all12_original_single_page_native_progressive_and_FE_bodies_under_test=True,only_B22_differs_from_source_fixture_and_all335_other_blocks_exact=True,source_conditions_roster_roles_funds_RNG_results_RAM_battery_savestate_unforced=True,initialized_Amsterdam_B22_not_natural_event211_original_location_or_earned_progress=True,not_registered_candidate_or_release_parent=True,all_manuscript_formatting_gates_still_false=True,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old);assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values);values.append(dict(path=str(ROM.resolve()),reason='Complete B211 English swan-pair twelve-speech original-command scene with threeFE andoneFI research;name asset unchanged. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    runner=derive('scripts/run_lil_B211_source_v6556.py','scripts/run_lil_B211_English_v6568.py',{
        'source_fixture_v6555':'English_fixture_v6567','complete_B211_source_B22_fixture':'complete_B211_English_B22_fixture',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",'source_run_v6556':'English_run_v6568','source_v6556':'English_v6568','B211 Japanese content':'B211 reviewed English content',
    })
    save(ROOT/'pin_and_runner_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,before_sha256=sha(old),after_sha256=sha(encoded),ROMs_deleted=0,prepared_runner=runner,full_goal_complete=False))
    print('Pinned complete English B211 fixture:14source+9initializers,9progressive/3FE objects/oneFI,one original A000/complete end,no typed objects/relative paths/predicates. Same ordinary input;no forced state or natural activation claim.')
