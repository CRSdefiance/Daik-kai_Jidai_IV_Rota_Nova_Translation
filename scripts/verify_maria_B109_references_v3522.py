"""Fresh executable censuses,full SC3 loader binding and relocated Maria consumers."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_maria_B109_controls_v3502 import C200
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B109_references_v3522')
APPROVAL=Path('work/analysis/maria_B109_native_approval_v3520/approval_and_production_scope_research_receipt.json')
LOAD=Path('work/analysis/maria_B109_loader_v3521/whole_SC3_and_B109_initial_entry_proof.json')
DISPATCH=Path('work/analysis/maria_B109_dispatches_v3500/all26_source_current_Maria_dispatches_and_catalog.json')
ENTRY=Path('work/analysis/maria_B109_entry_v3501/source_EV3_B109_action_dependency_and_native_getter_binding.json')

if __name__=='__main__':
    assert not ROOT.exists();approval,loader,dispatch,entry=map(read,[APPROVAL,LOAD,DISPATCH,ENTRY]);planpath=Path(approval['plan']);plan=read(planpath);docpath=Path(approval['manuscript']);doc=read(docpath);sourcepath=Path(doc['source_context']);packet=read(sourcepath)
    assert approval['manuscript_sha256']==sha(docpath.read_bytes()) and approval['plan_sha256']==sha(planpath.read_bytes())
    assert loader['all303_whole_blocks_and606_modes_each_pass'] and loader['original_parent_both_modes_start_at_loaded_payload_plus8'] and loader['original_EV3_actions_select_by_block_index_without_interior_byte_offset']
    for r in loader['versions']:
        assert r['whole_SC3_loads_and_cache_hits']==303 and r['original_parent_modes']==606
        for k in ['load','parent']:assert sha(Path(r[k+'_proof']).read_bytes())==r[k+'_sha256']
    paths=['work/clean.nds',approval['parent'],approval['research_ROM']];images=[NdsImage.open(p) for p in paths];clean,current,target=images
    assert sha(Path(paths[1]).read_bytes())==approval['parent_sha256'] and sha(Path(paths[2]).read_bytes())==approval['research_ROM_sha256']
    code={name:census(im) for name,im in zip(['clean','current','target'],images,strict=True)}
    assert code['current']==code['target'] and all(r['branches'][0]['address']==0x02024070 and not r['literal_aliases'] for r in code.values())
    assert current.read_file('/data/EV3.DK4')==target.read_file('/data/EV3.DK4')==clean.read_file('/data/EV3.DK4')
    blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in images];assert all(len(bs)==303 for bs in blocks)
    assert [n for n,(a,b) in enumerate(zip(blocks[1],blocks[2],strict=True)) if a!=b]==[109]
    assert sha(blocks[2][109])==plan['target_block_sha256'] and blocks[2][109][:4]==blocks[0][109][:4]==b'CS\1\1'
    control=read(plan['control_proof']);assert plan['all34_commands26_speech_preambles_and8_source_non_speech_commands_preserved'] and plan['exact_inverse_recovers_predecessor_bad_control_bytes_and_all_old_speech_bytes']
    assert len(plan['mapped_native_commands'])==34 and len(plan['text_records'])==26 and not plan['relative_sites']
    assert blocks[2][109][8:18]==blocks[0][109][8:18] and blocks[1][109][8:18]!=blocks[0][109][8:18]
    ROOT.mkdir(parents=True);namespace={**prior.__dict__,'SOURCE':sourcepath,'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():exec(compile(text,str(DISPATCH)+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](target);assert binding['route']==3 and binding['route_mask']==8
    ctx=CurrentContext(dispatch['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context');byid={r['id']:r for r in doc['records']};cases=[]
    for t in plan['text_records']:
        value=bytes.fromhex(t['stored_text_hex']);at=t['new_text_offset'];assert blocks[2][109][at:at+len(value)]==value and blocks[2][109][at+len(value)]==0
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        assert result['resolved_actor_ID']==value[0]==byid[t['id']]['source_selector'] and result['boundaries'][1]['text_hex']==value[1:].hex() and result['registered_catalog_match'] is None
        cases.append(dict(id=t['id'],new_text_offset=at,stored_target_hex=value.hex(),**result))
    c=next(c for c in plan['mapped_native_commands'] if c['word']==0xC200);at=c['new_offset'];command=dict(offset=at,native_extent=c['new_extent'],word=c['word'],whole_command_hex=blocks[2][109][at:at+c['new_extent']].hex())
    c200=ctx.execute(C200,blocks[2][109],command);ctx.machines.pop();before=control['source_current_C200_pair'][0]
    assert c200['native_result']==before['native_result'] and c200['source_owned_UI_writes']==before['source_owned_UI_writes'] and c200['source_owned_UI_request_words']==before['source_owned_UI_request_words']==[1,54,13,0,0,0,1]
    assert c200['all_other4MiB_actor_roster_event_RNG_and_models_exact'] and len(c200['source_owned_UI_writes'])==9 and c200['native_presentation_resource_bodies_not_executed']
    assert len(cases)==26 and not ctx.machines
    evidence={str(p):sha(p.read_bytes()) for p in [APPROVAL,LOAD,DISPATCH,ENTRY,planpath,docpath,sourcepath,Path(plan['control_proof']),Path(__file__)]}
    save(ROOT/'B109_source_entry34_commands26_relocated_dispatches_and_C200.json',dict(parent=approval['parent'],parent_sha256=approval['parent_sha256'],research_ROM=approval['research_ROM'],research_ROM_sha256=approval['research_ROM_sha256'],ARM9_sha256=sha(target.read_file('/__arm9__.bin')),native_call_census=code,all303_loader_cache_hits606_parent_modes_each_image=True,original_EV3_unchanged_and_event109_action110_selects_block109=True,source_event_entry_proof=str(ENTRY),source_event_entry_proof_sha256=sha(ENTRY.read_bytes()),current_source_event109_eligibility_not_executed=True,source_and_target34_command_maps=plan['mapped_native_commands'],current_bad_prefix35_commands_not_silently_equated_to_source34=True,source_owned_control_repair=plan['source_owned_prefix_span'],all302_other_SC3_blocks_every_other_file_component_exact=approval['all302_other_SC3_blocks_every_other_file_component_exact'],relocated_dispatch_cases=cases,all26_stored_targets_reach_expected_original_progressive_consumer=True,relocated_C200=c200,C200_source_owned9_writes_and_Maria_index54_preserved=True,C200_offline_resource_bodies_unexecuted_actual_fixture_transition_separate=True,registered_catalog_binding=binding,portable_source_owned_adapters=dispatch['source_owned_adapters'],portable_C200_adapter=control['portable_source_owned_adapters']['C200'],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence=evidence,no_ledger_registration_or_completion_change=True,full_goal_complete=False))
    print(dict(executable_censuses=3,source_commands=34,relocated_dispatches=26,Maria_C200_index=54,loader_blocks=303,parent_modes_per_ROM=606,credit=0))
