"""Preserve the whole final B221 exchange in an initialized fixture for both ordinary choices."""
import json,os,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.create_lil_B221_reference_v6997 import PARENT,PLAN,STORED
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_English_fixture_v7001')
SOURCE_FIXTURE=Path('work/analysis/lil_B221_source_fixture_v6978/complete_B221_source_B22_fixture.json')
ROM=Path('out/lil_B221_English_v7001_reviewed_English_RESEARCH_ONLY.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists()
    runners=[]
    for suffix,number in [('',7002),('c',7003)]:
        runners.append((f'scripts/run_lil_B221_source_v6979{suffix}.py',f'scripts/run_lil_B221_English_v{number}.py',{
            'source_fixture_v6978':'English_fixture_v7001',
            'complete_B221_source_B22_fixture':'complete_B221_English_B22_fixture',
            "selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",
            f'source_run_v6979{suffix}':f'English_run_v{number}',
            f'source_v6979{suffix}':f'English_v{number}',
            'B221 Japanese content':'B221 reviewed English content'}))
    for source,target,changes in runners:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf-8'),changes)
    source_fixture=read(SOURCE_FIXTURE)['fixtures'][0];plan,stored=read(PLAN),read(STORED)
    packet=read(plan['source_context']);reference=read('work/analysis/lil_B221_reference_v6997/research_image_receipt.json')
    loader=read('work/analysis/lil_B221_loader_v6998/whole_SC2_and_B221_initial_entry_proof.json')
    census=read('work/analysis/lil_B221_reference_census_v6999/all21_commands_four_relatives_one_menu_and_shipped_census.json')
    controls=read('work/analysis/lil_B221_relocated_controls_v7000b/all14_final_dispatches_A00025_normal_seeded_ends_four_relatives_one_menu.json')
    assert stored['relocation_plan_sha256']==reference['source_relocation_plan_sha256']==sha(PLAN.read_bytes())
    assert stored['all_final_stored_targets_equal_reviewed_complete_native_ink'] and stored['complete_native_pages']==16
    assert loader['all336_whole_blocks_and672_modes_each_pass'] and census['all21_clean_current_target_commands_bound']
    assert controls['target_block_sha256']==plan['blocks'][0]['research_block_sha256']
    parent=NdsImage.open(PARENT);assert sha(PARENT.read_bytes())==plan['candidate_sha256']
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks
    bank=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks
    inventory,_,_=scoped_inventory();init,_=inventory(parent.read_file('/__arm9__.bin'),current[22])
    first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9
    prelude=current[22][8:first];assert prelude.hex()==source_fixture['original_B22_prelude_hex']
    end=8+struct.unpack_from('<H',bank[221],4)[0];assert end==len(bank[221])==1224
    logical=bytearray(current[22][:8]+prelude+bank[221][8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4)
    commands,speeches=inventory(parent.read_file('/__arm9__.bin'),target)
    native,_=inventory(parent.read_file('/__arm9__.bin'),bank[221])
    assert len(native)==21 and len(commands)==30 and len(speeches)==14
    assert sum(c['word']==0xA000 for c in commands)==5 and sum(c['word']==0 for c in commands)==1
    assert sum(c['word']==0x2100 for c in commands)==1
    assert sum(c['word'] in [0x100,0x200,0x300] for c in commands)==4
    assert not any(c['word'] in [0x8000,0xC200,0x2200,0x4100] for c in commands)
    objects=[];texts=[]
    for original,command,mapping in zip(packet['blocks'][0]['all_clean_native_commands'],native,plan['blocks'][0]['command_map'],strict=True):
        assert original['word']==command['word']==mapping['word']
        assert original['offset']==mapping['old_offset'] and command['offset']==mapping['new_offset']
        at=command['offset']+first-8;mapped=next(c for c in commands if c['offset']==at)
        assert mapped['whole_command_hex']==command['whole_command_hex']
        assert mapped['ancestor_0100_offsets']==[a+first-8 for a in command['ancestor_0100_offsets']]
        row=next((r for r in packet['records'] if r['source_reference']['header_offset']==original['offset']),None)
        objects.append(dict(source_block=221,source_offset=original['offset'],source_word=original['word'],
            relocated_block_offset=command['offset'],fixture_offset=at,native_extent=command['native_extent'],
            whole_command_hex=command['whole_command_hex'],text_ID=None if row is None else row['id']))
        if row is not None:
            texts.append(dict(id=row['id'],source_block=221,source_record_index=row['source_record_index'],
                fixture_command_offset=at,source_selector=row['source_selector'],native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex']))
    blocks=list(current);blocks[22]=target;image=NdsImage.open(PARENT)
    image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(ROM)
    saved=NdsImage.open(ROM);after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(saved.read_file(p)==v for p,v in parent.iter_components())
    source_image=NdsImage.open(source_fixture['research_ROM'])
    source_blocks=IlnkContainer.parse(source_image.read_file('/data/SC2.DK4')).blocks
    assert [i for i,(a,b) in enumerate(zip(source_blocks,after,strict=True)) if a!=b]==[22]
    ROOT.mkdir(parents=True)
    fixture=dict(case='reviewed_English',source_block=221,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),
        original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,
        explicitly_excluded_original_commands=[],all30_stored_fixture_commands=commands)
    save(ROOT/'complete_B221_English_B22_fixture.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        source_fixture=str(SOURCE_FIXTURE),source_fixture_sha256=sha(SOURCE_FIXTURE.read_bytes()),
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),fixtures=[fixture],
        all21_source_commands_plus9_original_initializers_stored_without_omission=True,
        fourteen_speeches_two_choices_four_relatives_A000_normal_end_and_two_continuations_preserved=True,
        only_B22_differs_from_source_fixture_all335_other_blocks_files_fonts_names_and_runtime_exact=True,
        conditions_roster_roles_funds_RNG_results_RAM_battery_and_savestate_unforced=True,
        initialized_Amsterdam_B22_not_natural_event221_location_or_earned_progress=True,
        not_registered_candidate_or_release_parent=True,all16_dialogue_formatting_gates_still_false=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='Complete B221 English14-speech/two-choice scene with all21 original commands,four relatives,A000,complete normal end and two native continuations. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    (ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as stream:
        stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    proofs=[derive(*row) for row in runners]
    save(ROOT/'pin_and_two_runners_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),
        all_prior_pins_preserved=True,before_sha256=sha(old),after_sha256=sha(encoded),ROMs_deleted=0,
        prepared_runners=proofs,same_source_schedules_A_only_and_ordinary_DOWN3700_A3800=True,full_goal_complete=False))
    print('Pinned B221 English fixture:21 original+9 initializers,14 speeches/two choices/two continuations. Two unchanged-source-schedule runners prepared.')
