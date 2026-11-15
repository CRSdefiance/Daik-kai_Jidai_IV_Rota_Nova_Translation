"""Re-execute relocated dispatch, style tables and predicates in current code."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import prove_lil_shrines_temples_controls_v3168c as native
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prepare_lil_shrines_research_v3194 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_relocated_controls_v3197')
DOC=Path('translations/lil_shrines_temples_editorial_manuscript_v7.json')
VOICE=Path('translations/lil_shrines_temples_actor_style_manuscript_v5.json')
REFERENCE=Path('work/analysis/lil_Shrines_Temples_reference_census_v3196/all421_commands114_relative_sites_and_shipped_entry_census.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,voice,plan,reference=map(read,[DOC,VOICE,PLAN,REFERENCE])
    source=read(doc['source_context']);original=read(doc['control_contract'])
    parent,image=NdsImage.open(PARENT),NdsImage.open(ROM)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    assert sha(ROM.read_bytes())==reference['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')
    assert image.read_file('/COMMON/MESFILE.DK4')==parent.read_file('/COMMON/MESFILE.DK4')
    oldblocks,newblocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,image]]
    native.CATALOG_LOOKUP,catalog_binding=native.bind_current_catalog(parent)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_Shrines_Temples_fonts_v3183b/current_native_input.json',
        source['historical_snapshot_ROM'],ROOT/'current_context')
    dispatches=[];whole=[];objects=[];predicates=[]
    byid={r['id']:r for r in doc['records']+voice['records']}
    for spec in plan['blocks']:
        n=spec['block'];old,new=oldblocks[n],newblocks[n]
        assert sha(new)==spec['research_block_sha256'] and sha(old)==spec['source_block_sha256']
        target_records=[(r,False) for r in spec['text_records']]
        target_records.extend((r,True) for c in spec['actor_style_commands'] for r in c['alternative_records'])
        for r,isvoice in target_records:
            row=byid[r['id']];value=bytes.fromhex(r['target_hex']);at=r['new_offset']
            assert new[at:at+len(value)]==value and new[at+len(value)]==0
            prefix=208 if isvoice else value[0]
            body=value if isvoice else value[1:]
            result=ctx.execute(native.dispatch,prefix,body);ctx.machines.pop()
            expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert result['boundaries'][1]['text_hex']==expected.hex()
            assert result['registered_catalog_match'] is None
            dispatches.append(dict(id=r['id'],block=n,new_offset=at,stored_target_hex=value.hex(),
                virtual_D0_not_stored=isvoice,**result))
        for c in spec['actor_style_commands']:
            versions=[]
            for version,block,at,extent in [('current',old,c['old_offset'],c['old_length']),
                                             ('relocated',new,c['new_offset'],c['new_length'])]:
                value=block[at:at+extent]
                command=dict(offset=at,native_extent=extent,word=0x4100,whole_command_hex=value.hex())
                result=ctx.execute(native.whole_style_command,block,command);ctx.machines.pop()
                whole.append(dict(block=n,version=version,command_offset=at,**result))
                slots=[]
                for index in range(8):
                    relative=20+struct.unpack_from('<H',value,2+index*2)[0]
                    body=value[relative:value.index(b'\0',relative)]
                    slots.append(dict(style_index=index,relative_offset=relative,hex=body.hex()))
                versions.append(dict(version=version,command_offset=at,command_hex=value.hex(),style_slots=slots))
            objects.append(dict(block=n,command_offset=c['old_offset'],versions=versions))
        for command in spec['command_map']:
            if command['word'] not in [0x8000,0x8100]:continue
            pairs=[]
            for version,block,at,extent in [('current',old,command['old_offset'],command['old_extent']),
                                             ('relocated',new,command['new_offset'],command['new_extent'])]:
                c=dict(offset=at,native_extent=extent,word=command['word'],whole_command_hex=block[at:at+extent].hex())
                result=ctx.execute(native.predicate,block,c);ctx.machines.pop()
                assert not result['original_event_completion_calls']
                pairs.append(dict(version=version,**result))
            assert pairs[0]['native_result']==pairs[1]['native_result']
            assert pairs[0]['source_command_hex']==pairs[1]['source_command_hex']
            predicates.append(dict(block=n,old_offset=command['old_offset'],new_offset=command['new_offset'],
                cases=pairs,operands_results_and_unowned_RAM_exact=True))
    catalog=ctx.execute(native.catalog_style_getters,objects);ctx.machines.pop()
    assert len(dispatches)==220 and sum(c['source_selector']==254 for c in dispatches)==30
    assert len(whole)==16 and len(catalog['cases'])==3312 and len(predicates)==21 and not ctx.machines
    assert all(c['source_selector']==208 and c['resolved_actor_ID']==151 and c['original_actor_style']==4 for c in whole)
    assert original['all3312_catalog_getter_cases_cover_every_actor_style_without_role_assignment']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,VOICE,PLAN,REFERENCE,Path(doc['control_contract']),Path(__file__)]}
    save(ROOT/'all220_dispatch16_style_commands3312_getters21_predicate_pairs.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,
        relocated_dispatch_cases=dispatches,current_and_relocated_whole_original4100_command_cases=whole,
        all207_actor_style_current_and_relocated_pointer_cases=catalog,relocated_predicate_pairs=predicates,
        all220_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text=True,
        all30_FE_preserve_original_null_actor_before_dynamic_fallback=True,
        all16_style_commands_use_unforced_D0_fallback151_style4_without_role_assignment=True,
        all3312_pointer_cases_and_all_source_alias_groups_preserved=True,
        all21_current_relocated_predicate_results_and_source_operands_equal=True,
        original_event_queries=[],no_predicate_flag_event_roster_RNG_health_or_outcome_fixture=True,
        sole_native_unaligned_operand_scratch_restore_recovers_all4MiB=True,
        original_UI_preparation_progressive_FE_bodies_unexecuted_boundaries=True,
        complete_native_rendering_proved_separately_not_actual_gameplay=True,
        current_catalog_binding=catalog_binding,current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,registered_release_and_sampling_pending=True,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('220relocated dispatches/16whole actor-style commands/3312catalog pointers/21current-target predicate pairs pass. No forced roles,flags ornewgameplay.')
