"""Bind every final speech and relocated630B/A000/end while leaving all gameplay state unforced."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.create_lil_B225_reference_v7199 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_relocated_controls_v7202');SOURCE=Path('work/analysis/lil_B225_source_v7178/thirteen_clean_current_children_heroes_exchange_source_references.json');CURRENT=Path('work/analysis/lil_B225_consumers_v7179/thirteen_effective_bodies26_dispatches_four_actors_eight_name_consumers.json');CONTROL=Path('work/analysis/lil_B225_controls_v7181/four_source630B_A000_structural10_resource50_normal_end_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current,control,plan=map(read,[SOURCE,CURRENT,CONTROL,PLAN]);image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[225];spec=plan['blocks'][0]
    assert sha(PARENT.read_bytes())==source['current_ROM_sha256']==plan['candidate_sha256'] and sha(block)==spec['research_block_sha256'] and len(block)==1076 and spec['research_logical_end']==1074 and spec['research_tail_bytes']==2 and len(spec['command_map'])==16
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext(source['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');rows={r['id']:r for r in source['records']};cases=[]
    for ref in spec['text_records']:
        row=rows[ref['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);prefix=row['source_selector'];assert block[at:at+len(value)+1]==value+b'\0' and value[0]==prefix and block[at-5:at+1].hex()==row['source_complete_preamble_hex'];body=value[1:];assert not any(k in body for k in [b'FI',b'FA',b'FO']);result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop();assert result['resolved_actor_ID']==prefix and result['source_voice_class']=={2:3,16:1,151:4,162:0}[prefix] and result['registered_catalog_match'] is None;boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');assert boundary['text_hex']==body.hex();cases.append(dict(id=row['id'],new_offset=at,target_hex=value.hex(),**result))
    structural=[]
    for key,word,offset,expected in [('original_630B_map',0x630B,88,'0b63'),('original_A000_map',0xA000,1062,'00a0ffff48000110')]:
        ref=spec[key][0];at=ref['target_offset'];raw=block[at:at+ref['extent']];prior=next(r for r in control['source630B_A000_structural_cases'] if r['version']=='current-English' and r['word']==word);assert at==offset and raw.hex()==prior['source_command_hex']==expected
        isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw;r=walk(ctx.arm,isolated);assert r['error'] is None and r['rows']==prior['rows'] and r['opaque_effect_bridges']==prior['opaque_effect_bridges'];structural.append(dict(word=word,source_offset=ref['source_offset'],target_offset=at,source_command_hex=expected,source=prior,relocated=r))
    env=dict(resource_base.__dict__);exec(compile(control['source_owned_adapters']['source630B'],__file__+'::source630B','exec'),env);resources=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result));ctx.machines.pop()
    assert resources==control['source630B_boundary_cases'] and all(r['all4MiB_owner_input_ABI_output_and_length_guards_exact'] for r in resources)
    env=dict(end_case.__globals__);exec(compile(control['source_owned_adapters']['seeded_end'],__file__+'::seeded-normal-end','exec'),env);end=spec['complete_end_map'][0]['target_offset'];assert end==1070 and block[end:]==bytes(6);ends=[env['end_case'](ctx.arm,block,end,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]];assert len(cases)==13 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    save(ROOT/'all13_final_dispatches_630B_A00010_resource25_normal_seeded_ends.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),target_block_sha256=sha(block),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),dispatch_cases=cases,all13_complete_preambles_voices_andzero_macro_bodies_bound=True,zero_original_orinvented_FI_FA_FO=True,source_andrelocated630B_A000_structural_cases=structural,source630B_boundary_cases=resources,source630B_target88_original_request_owner11_2_1_andunowned4MiB_exact=True,resource_body_unexecuted_at_isolated_boundary_no_inferred_role_assignment=True,normal_terminal_seed_cases=ends,normal_state0_retains_existing_value_word_in_all25_cases=True,original_normal_end1070_four_bytes_andtwo_byte_tail_preserved=True,all16_commands_no_predicate_relative_typed_style_orpicture_assumptions=True,opaque_A000_effects_bridged_not_fully_explained=True,source_control=str(CONTROL),source_control_sha256=sha(CONTROL.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_credit=0,full_goal_complete=False));print('B22513 final dispatches,630B78->88,A000962->1062,end970->1070/tail2,10 unchanged-memory resource cases and25 normal residual ends pass. Actual English pending;zero credit.')
