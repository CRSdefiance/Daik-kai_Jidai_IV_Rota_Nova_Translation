"""Bind nine final speech consumers,three opaque controls,end value andboth target tail bytes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.create_lil_B227_reference_v7307 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B227_relocated_controls_v7310');SOURCE=Path('work/analysis/lil_B227_source_v7287/nine_clean_current_sword_practice_cloth_rumor_source_references.json');CURRENT=Path('work/analysis/lil_B227_consumers_v7288/nine_effective_bodies18_dispatches_two_actors_four_name_consumers.json');CONTROL=Path('work/analysis/lil_B227_controls_v7290/six_source_A000_structural50_normal_end_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current,control,plan=map(read,[SOURCE,CURRENT,CONTROL,PLAN]);image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[227];spec=plan['blocks'][0]
    assert sha(PARENT.read_bytes())==source['current_ROM_sha256']==plan['candidate_sha256'] and sha(block)==spec['research_block_sha256'] and len(block)==708 and spec['research_logical_end']==706 and spec['research_tail_bytes']==2 and len(spec['command_map'])==13 and not spec['original_630B_map'] and not spec['original_C200_map']
    ns={**inherited.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}}
    for name,text in current['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext(source['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');rows={r['id']:r for r in source['records']};cases=[]
    for ref in spec['text_records']:
        row=rows[ref['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);prefix=row['source_selector'];assert block[at:at+len(value)+1]==value+b'\0' and value[0]==prefix and block[at-5:at+1].hex()==row['source_complete_preamble_hex'];body=value[1:];assert not any(k in body for k in [b'FI',b'FA',b'FO']);result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop();assert result['resolved_actor_ID']==prefix and result['source_voice_class']=={2:3,25:3}[prefix] and result['registered_catalog_match'] is None
        boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');assert boundary['text_hex']==body.hex();cases.append(dict(id=row['id'],new_offset=at,target_hex=value.hex(),**result))
    effects=[];expected=[(638,678,'00a0ffff37000110'),(646,686,'00a0ffff010d1960'),(654,694,'00a0ffff010e1960')]
    assert len(spec['original_A000_map'])==3
    for ref,(old,at,value) in zip(spec['original_A000_map'],expected,strict=True):
        assert ref['source_offset']==old and ref['target_offset']==at;raw=block[at:at+ref['extent']];prior=next(r for r in control['source_A000_structural_cases'] if r['version']=='current-English' and r['original_offset']==old);assert raw.hex()==prior['source_command_hex']==value
        isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw;relocated=walk(ctx.arm,isolated);assert relocated['error'] is None and relocated['rows']==prior['rows'] and relocated['opaque_effect_bridges']==prior['opaque_effect_bridges'];effects.append(dict(source_offset=old,target_offset=at,source_hex=value,source=prior,relocated=relocated))
    env=dict(end_case.__globals__);exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::seeded-normal-end','exec'),env);end=spec['complete_end_map'][0]['target_offset'];assert end==702 and block[end:]==bytes(6)
    ends=[env['end_case'](ctx.arm,block,end,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]];assert len(cases)==9 and len(ends)==25 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends) and not ctx.machines
    save(ROOT/'all9_final_dispatches_three_A00025_normal_seeded_ends.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),target_block_sha256=sha(block),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),dispatch_cases=cases,all9_complete_preambles_voices_andzero_macro_bodies_bound=True,zero_original_orinvented_FI_FA_FO=True,three_source_andrelocated_A000_cases=effects,normal_terminal_seed_cases=ends,normal_state0_retains_existing_value_word_in_all25_cases=True,original_normal_end702_four_bytes_andtarget_tail2_preserved=True,all13_commands_no_predicate_relative_typed_style_orpicture_assumptions=True,opaque_A000_effects_bridged_not_fully_explained=True,source_control=str(CONTROL),source_control_sha256=sha(CONTROL.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,CONTROL,PLAN,Path(__file__)]},full_goal_complete=False))
    print('B227:9 final dispatches,voice3,zero macros,allthree A000,normal702end andtail2 pass25 seeds;no forced state ornew credit.')
