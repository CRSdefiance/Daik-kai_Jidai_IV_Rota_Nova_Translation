"""Create paired complete B178 content fixtures with original B22 initialization."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_display_fixture_v4691')
PARENT=Path('out/all_routes_combined_v4655_candidate.nds')
PLAN=Path('work/analysis/lil_B178_relocation_v4681/nested_source_relocation_research.json')
DOC=Path('translations/lil_B178_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC);packet=read(doc['source_context'])
    parent,clean=NdsImage.open(PARENT),NdsImage.open('work/clean.nds');arm=parent.read_file('/__arm9__.bin')
    current=IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks
    jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    en=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    inventory,_,_=scoped_inventory();b22=current[22];init,_=inventory(arm,b22)
    first=next(c['offset'] for c in init if c['word']==0x4000)
    assert first==56 and len(init[:9])==9 and sum(c['word']==0xA000 for c in init[:9])==4
    prelude=b22[8:first];group=packet['blocks'][0]
    ROOT.mkdir(parents=True);fixtures=[]
    for case,bank in [('clean_Japanese',jp),('reviewed_English',en)]:
        commands,_=inventory(arm,bank[178]);assert len(commands)==16
        assert [c['word'] for c in commands if c['word']!=0x4000]==[0xA000,0xC200,0]
        end=8+struct.unpack_from('<H',bank[178],4)[0]
        logical=bytearray(b22[:8]+prelude+bank[178][8:end]);struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+bytes(-len(logical)%4);walk,speeches=inventory(arm,target)
        assert len(walk)==25 and len(speeches)==13
        assert sum(c['word']==0 for c in walk)==1 and sum(c['word']==0xC200 for c in walk)==1
        assert sum(c['word']==0xA000 for c in walk)==5
        assert not any(c['word'] in [0x8000,0x100,0x200,0x300,0x400,0x2100,0x4100,0x2000] for c in walk)
        objects=[];texts=[]
        for source,command in zip(group['all_clean_native_commands'],commands,strict=True):
            at=command['offset']+first-8;mapped=next(c for c in walk if c['offset']==at)
            assert mapped['word']==source['word'] and mapped['whole_command_hex']==command['whole_command_hex']
            row=next((r for r in group['records'] if r['source_reference']['header_offset']==source['offset']),None)
            objects.append(dict(source_block=178,source_offset=source['offset'],source_word=source['word'],fixture_offset=at,
                native_extent=command['native_extent'],whole_command_hex=command['whole_command_hex'],text_ID=None if row is None else row['id']))
            if row is not None:texts.append(dict(id=row['id'],source_block=178,source_record_index=row['source_record_index'],
                fixture_command_offset=at,source_selector=row['source_selector'],native_extent=command['native_extent'],
                complete_preamble_hex=bytes.fromhex(command['whole_command_hex'])[:6].hex(),whole_command_hex=command['whole_command_hex']))
        assert sum(r['source_selector']==254 for r in texts)==1
        path=Path(f'out/lil_B178_display_v4691_{case}_RESEARCH_ONLY.nds');assert not path.exists()
        image=NdsImage.open(PARENT);blocks=list(current);blocks[22]=target
        image.replace_file('/data/SC2.DK4',IlnkContainer(blocks).to_bytes());image.save(path);saved=NdsImage.open(path)
        assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4']
        assert all(saved.read_file(p)==v for p,v in parent.iter_components())
        after=IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
        assert [n for n,(a,b) in enumerate(zip(current,after,strict=True)) if a!=b]==[22]
        fixtures.append(dict(case=case,source_block=178,research_ROM=str(path),research_ROM_sha256=sha(path.read_bytes()),
            fixture_block=22,fixture_block_hex=target.hex(),fixture_block_sha256=sha(target),original_B22_prelude_hex=prelude.hex(),
            original_B22_prelude_commands=init[:9],selected_original_objects=objects,original_text_records=texts,
            explicitly_excluded_original_commands=[],all25_stored_fixture_commands=walk,
            all13_speeches12_progressive1_impersonal_FE_one_source_A000_C200_single_end_retained=True,
            all335_other_SC2_blocks_and_every_other_file_component_exact=True))
    save(ROOT/'complete_B178_B22_fixtures.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),
        fixtures=fixtures,closing_notice_names_Amsterdam_without_proving_earlier_scene_location_initialized_fixture_town_is_Amsterdam=True,
        source_event178_not_selected_or_eligibility_earned=True,original_B22_nine_init_commands_including_four_A000s_preserved=True,
        source_all16_commands_preserved_without_omission_or_flattening=True,no_source_predicate_relative_pause_resources_presentations_or_typed_objects=True,
        source_FE_notice_remains_impersonal_and_leading_A000_packed_operand_semantics_not_inferred=True,
        expected_conditional_speech_IDs=[],stored_speech_objects=13,actual_transition_A000_and_single_end_reachability_to_be_observed=True,
        no_savestate_or_RAM_or_funds_fixture=True,not_registered_candidate_or_new_release_parent=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B178 fixtures retain all16 commands+9 original init commands,twelve progressive/one impersonal FE,one source A000,C200 and single end.')
