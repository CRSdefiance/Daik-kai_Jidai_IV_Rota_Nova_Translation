"""155 relocated dispatches and14 original predicate pairs,without fixtures."""
from pathlib import Path
from types import SimpleNamespace
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prepare_lil_B131_B133_research_v3330b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_relocated_controls_v3333b')
DOC=Path('translations/lil_B131_B133_editorial_manuscript_v4.json')
REFERENCE=Path('work/analysis/lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,reference=map(read,[DOC,PLAN,REFERENCE]);source=read(doc['source_context']);original=read(doc['control_contract'])
    parent,image=NdsImage.open(PARENT),NdsImage.open(ROM);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256'] and sha(ROM.read_bytes())==reference['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and image.read_file('/COMMON/MESFILE.DK4')==parent.read_file('/COMMON/MESFILE.DK4')
    oldblocks,newblocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,image]]
    namespace={**prior.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in original['source_owned_adapters'].items():exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    native=SimpleNamespace(**namespace);namespace['CATALOG_LOOKUP'],catalog_binding=native.bind_current_catalog(parent)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B131_B133_fonts_v3324b/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    dispatches=[];predicates=[];byid={r['id']:r for r in doc['records']}
    for spec in plan['blocks']:
        n=spec['block'];old,new=oldblocks[n],newblocks[n];assert sha(new)==spec['research_block_sha256'] and sha(old)==spec['source_block_sha256'] and not spec['actor_style_commands']
        for r in spec['text_records']:
            row=byid[r['id']];value=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(value)]==value and new[at+len(value)]==0 and value[0]==row['source_selector']
            result=ctx.execute(native.dispatch,value[0],value[1:]);ctx.machines.pop()
            expected=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert result['boundaries'][1]['text_hex']==expected.hex() and result['registered_catalog_match'] is None
            dispatches.append(dict(id=r['id'],block=n,new_offset=at,stored_target_hex=value.hex(),**result))
        for c in spec['command_map']:
            if c['word'] not in [0x8000,0x8100]:continue
            pair=[]
            for version,block,at,extent in [('current',old,c['old_offset'],c['old_extent']),('relocated',new,c['new_offset'],c['new_extent'])]:
                command=dict(offset=at,native_extent=extent,word=c['word'],whole_command_hex=block[at:at+extent].hex());result=ctx.execute(native.predicate,block,command);ctx.machines.pop()
                assert not result['original_event_completion_calls'];pair.append(dict(version=version,**result))
            assert pair[0]['native_result']==pair[1]['native_result'] and pair[0]['source_command_hex']==pair[1]['source_command_hex']
            predicates.append(dict(block=n,old_offset=c['old_offset'],new_offset=c['new_offset'],cases=pair,source_operands_results_and_unowned_RAM_exact=True))
    assert len(dispatches)==61 and sum(r['source_selector']==254 for r in dispatches)==1 and len(predicates)==5 and not ctx.machines
    assert sum(r['source_selector']==0 and r['resolved_actor_ID']==0 for r in dispatches)==18
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,REFERENCE,Path(doc['control_contract']),Path(__file__)]}
    save(ROOT/'all61_relocated_dispatches_source00_and5_predicate_pairs.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,all61_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text=True,all1_FE_preserves_original_null_actor_before_dynamic_fallback=True,all5_predicate_current_relocated_results_and_source_operands_equal=True,original_event_queries=[],no_dynamic_selectors_or4100_objects=True,all18_final_source00_speeches_are_static_Rafael0_without_role_assignment=True,current_registered_catalog_binding=catalog_binding,no_predicate_flag_event_roster_RNG_health_or_outcome_fixture=True,sole_native_unaligned_operand_scratch_restore_recovers_all4MiB=True,original_UI_preparation_progressive_FE_bodies_unexecuted_boundaries=True,complete_native_rendering_proved_separately_not_actual_gameplay=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B131_B133_IDs=[],new_emulator_runs=0,no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('61 relocated dispatches,including18source00Rafael,oneFE null actor andfive predicate pairs pass. Original source operands/results andunowned RAM preserved;no selected gameplay orrelease claim.')
