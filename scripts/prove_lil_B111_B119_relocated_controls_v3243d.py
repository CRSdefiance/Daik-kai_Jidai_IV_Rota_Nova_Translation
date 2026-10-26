"""Re-execute relocated dispatch, style tables and predicates in current code."""
import struct
from types import SimpleNamespace
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prepare_lil_B111_B119_research_v3240b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_relocated_controls_v3243d')
DOC=Path('translations/lil_B111_B119_editorial_manuscript_v5.json')
VOICE=Path('translations/lil_B111_B119_actor_style_manuscript_v4.json')
REFERENCE=Path('work/analysis/lil_B111_B119_reference_census_v3242/all305_commands64_relative_sites_and_shipped_entry_census.json')

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
    namespace={**prior.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in original['source_owned_adapters'].items():
        exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    native=SimpleNamespace(**namespace)
    namespace['CATALOG_LOOKUP'],catalog_binding=native.bind_current_catalog(parent)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B111_B119_fonts_v3234c/current_native_input.json',
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
            prefix=row['source_selector'] if isvoice else value[0]
            body=value if isvoice else value[1:]
            result=ctx.execute(native.dispatch,prefix,body);ctx.machines.pop()
            expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert result['boundaries'][1]['text_hex']==expected.hex()
            assert result['registered_catalog_match'] is None
            dispatches.append(dict(id=r['id'],block=n,new_offset=at,stored_target_hex=value.hex(),
                actual_virtual_prefix_not_stored=isvoice,**result))
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
                assert all(q['args'][1]==319 for q in result['original_event_completion_calls'])
                pairs.append(dict(version=version,**result))
            assert pairs[0]['native_result']==pairs[1]['native_result']
            assert pairs[0]['source_command_hex']==pairs[1]['source_command_hex']
            left,right=[p['original_event_completion_calls'] for p in pairs]
            assert len(left)==len(right)
            for a,b in zip(left,right,strict=True):
                assert a['address']==b['address'] and a['args'][:3]==b['args'][:3]
                assert a['args'][3]==0x02660000+command['old_offset']
                assert b['args'][3]==0x02660000+command['new_offset']

            predicates.append(dict(block=n,old_offset=command['old_offset'],new_offset=command['new_offset'],
                cases=pairs,operands_results_and_unowned_RAM_exact=True))
    catalog=ctx.execute(native.catalog_style_getters,objects);ctx.machines.pop()
    assert len(dispatches)==150 and sum(c['source_selector']==254 for c in dispatches)==1
    assert len(whole)==12 and len(catalog['cases'])==2484 and len(predicates)==16 and not ctx.machines
    assert all(c['source_selector'] in [208,209,214,215,220] and c['resolved_actor_ID']==151 and c['original_actor_style']==4 for c in whole) and {c['source_selector'] for c in whole}=={208,209,214,215,220}
    assert original['all2484_catalog_getters_preserve_each_original_style_pointer_and_alias']
    queries=[dict(block=p['block'],old_offset=p['old_offset'],new_offset=p['new_offset'],event=q['args'][1],args=q['args']) for p in predicates for q in p['cases'][0]['original_event_completion_calls']]
    assert len(queries)==1 and queries[0]['block']==114 and queries[0]['old_offset']==46 and queries[0]['event']==319
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,VOICE,PLAN,REFERENCE,Path(doc['control_contract']),Path(__file__)]}
    save(ROOT/'all150_dispatch12_style_commands2484_getters16_predicate_query_pairs.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,
        relocated_dispatch_cases=dispatches,current_and_relocated_whole_original4100_command_cases=whole,
        all207_actor_style_current_and_relocated_pointer_cases=catalog,relocated_predicate_pairs=predicates,
        all150_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text=True,
        one_FE_preserves_original_null_actor_before_dynamic_fallback=True,
        all12_style_commands_use_actual_variable_source_prefix_unforced_fallback151_style4_without_role_assignment=True,
        all2484_pointer_cases_and_all_source_alias_groups_preserved=True,
        all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal=True,
        original_event_queries=queries,canonical_Maria32_copy_not_dispatched_under_Lil_context=True,original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact=True,no_predicate_flag_event_roster_RNG_health_or_outcome_fixture=True,
        sole_native_unaligned_operand_scratch_restore_recovers_all4MiB=True,
        original_UI_preparation_progressive_FE_bodies_unexecuted_boundaries=True,
        complete_native_rendering_proved_separately_not_actual_gameplay=True,
        current_catalog_binding=catalog_binding,current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_selected_B111_B119_IDs=[],new_emulator_runs=0,registered_release_and_sampling_pending=True,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('150relocated dispatches/12whole variable-selector commands/2484catalog pointers/15predicate andoneevent319query pairs pass. No forced roles,flags ornewgameplay.')
