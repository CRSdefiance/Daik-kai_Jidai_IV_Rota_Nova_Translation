"""Prepare B174 research references, reusing the exact registered parent loader."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_research_tools_v4481')
PARENT=Path('out/all_routes_combined_v4445_candidate.nds')
ROM=Path('out/lil_B174_reference_v4482_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B174_relocation_v4477/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4445'
    assert len(registry['accepted_layers'])==114 and 'all-routes-unified-v4445' in registry['profiles']
    tools=[derive('scripts/create_lil_B173_reference_v4431.py','scripts/create_lil_B174_reference_v4482.py',{
        'V4404':'V4445','lil_B173_research_v4431':'lil_B174_research_v4482',
        'all_routes_combined_v4404':'all_routes_combined_v4445','lil_B173_reference_v4431':'lil_B174_reference_v4482',
        'lil_B173_relocation_v4428':'lil_B174_relocation_v4477',
        'lil_B173_stored_v4429/all11_final_stored_targets44':'lil_B174_stored_v4478/all33_final_stored_targets132',
        'editorial_handoff_verification_v4427':'editorial_handoff_verification_v4480','all11_final_targets':'all33_final_targets',
        "current_final_stored_macro_alignment_cases']==44":"current_final_stored_macro_alignment_cases']==132",
        'current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=132',
        '[173]':'[174]','actual_selected_B173_IDs':'actual_selected_B174_IDs',
    })]
    # Replace the old reuse provenance with the B173 research proof, whose image is
    # byte-identical to registered V4445. It remains a reused, not rerun, parent.
    tools.append(derive('scripts/verify_lil_B173_loader_v4432.py','scripts/verify_lil_B174_loader_v4483.py',{
        'work/analysis/lil_B172_loader_v4385/whole_SC2_and_B172_initial_entry_proof.json':
            'work/analysis/lil_B173_loader_v4432/whole_SC2_and_B173_initial_entry_proof.json',
        'prepare_lil_B173_research_v4430':'prepare_lil_B174_research_v4481',
        'lil_B173_loader_v4432':'lil_B174_loader_v4483','lil_B173_research_v4431':'lil_B174_research_v4482',
        'whole_SC2_and_B173_initial_entry_proof':'whole_SC2_and_B174_initial_entry_proof','B173_fits':'B174_fits',
        'one B173 resized block':'one B174 resized block','registered V4404':'registered V4445','byte-identical V4404':'byte-identical V4445',
        'New B173 research':'New B174 research',
    }))
    common={'prepare_lil_B173_research_v4430':'prepare_lil_B174_research_v4481'}
    tools.append(derive('scripts/verify_lil_B173_references_v4433.py','scripts/verify_lil_B174_references_v4484.py',{
        **common,'lil_B173_reference_census_v4433':'lil_B174_reference_census_v4484',
        'lil_B173_loader_v4432':'lil_B174_loader_v4483','B173':'B174','[173]':'[174]',
        'for r in result)==23':'for r in result)==45','all23':'all45','native_commands_each=23':'native_commands_each=45',
        '23-command/four-span':'45-command/four-span',
    }))
    tools.append(derive('scripts/prove_lil_B173_ends_v4434.py','scripts/prove_lil_B174_ends_v4485.py',{
        **common,'B173':'B174','lil_B173_ends_v4434':'lil_B174_ends_v4485','n==173':'n==174',
    }))
    tools.append(derive('scripts/prove_lil_B173_relocated_controls_v4435.py','scripts/prove_lil_B174_relocated_controls_v4486.py',{
        **common,'B173':'B174','lil_B173_relocated_controls_v4435':'lil_B174_relocated_controls_v4486',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'blocks[173]':'blocks[174]','block=173':'block=174',
        'import probe\n':'import probe\nfrom scripts.prove_lil_B139_C200_v3461e import C200\n',
        'dispatches=[];leaves=[];predicates=[]':'dispatches=[];leaves=[];predicates=[];uis=[]',
        "            predicates.append(dict(source_offset=a,target_offset=b,cases=pair))":
            """            predicates.append(dict(source_offset=a,target_offset=b,cases=pair))
        if command['word']==0xC200:
            pair=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                pair.append(dict(version=label,**ctx.execute(C200,block,cmd)));ctx.machines.pop()
            assert pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes']
            uis.append(dict(source_offset=a,target_offset=b,cases=pair))""",
        'len(dispatches)==11':'len(dispatches)==33',
        'len(predicates)==1 and not ctx.machines':'len(predicates)==1 and len(uis)==1 and not ctx.machines',
        '[0x6000,0x6329,0x6340,0xA000,0x8000,0xA000,0x6240,0]':'[0x6000,0x6340,0x8000,0x6240,0xA000,0xA000,0xC200,0]',
        "len(control['two_resource_words20_boundary_cases'])==20":"len(control['one_resource_word10_boundary_cases'])==10",
        'all11':'all33','relocated_C200_pairs=[]':'relocated_C200_pairs=uis',
        'source_resource20_boundary_cases_reused':'source_resource10_boundary_cases_reused',
        'all11_speeches_before_conditional_effect_suffix':'source32_unconditional_speeches_and_optional_Emilio69_preserved',
        '11 relocated dispatches,eight exact leaves,predicate pair,four relative sites/20 native cases and both suffix paths pass.':
            '33 relocated dispatches,eight exact leaves,predicate/C200 pairs,four relative sites/20 native cases and both optional-speech paths pass.',
        'presentation_resource_and_two_A000_bodies_not_fully_executed_by_this_probe':
            'presentation_resource_and_two_A000_bodies_not_fully_executed_by_this_probe',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=174,structural_commands=45,
        relative_sites=4,target_cases=20,pause=0,C200=1,endwords=1,nonrelative_leaves=8,
        source_resources=[0x6340],source_A000_offsets=[2068,2076],source_predicate_offset=874,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4445',research_parent='all-routes-unified-v4445',
        whole_ROM_exact_parent_loader_reuse=True,no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Prepared B174 research, fresh loader with exact V4445 parent reuse,45-command census, guarded end and C200/optional-speech controls.')
