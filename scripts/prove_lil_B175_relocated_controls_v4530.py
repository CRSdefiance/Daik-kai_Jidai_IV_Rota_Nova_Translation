"""Bind32 relocated progressive/FE dispatches, seven leaves and paired C200 ownership."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B175_research_v4525 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_relocated_controls_v4530')
DOC=Path('translations/lil_B175_editorial_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN);packet=read(doc['source_context'])
    dispatch,control=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[175] for p in [PARENT,ROM]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==control['candidate_sha256']
    assert NdsImage.open(PARENT).read_file('/__arm9__.bin')==NdsImage.open(ROM).read_file('/__arm9__.bin')
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM))
    ROOT.mkdir(parents=True);ctx=CurrentContext(dispatch['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};spec=plan['blocks'][0]
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    dispatches=[];leaves=[];uis=[]
    for record in spec['text_records']:
        value,at=bytes.fromhex(record['target_hex']),record['new_offset']
        assert new[at:at+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        actor=None if value[0]==254 else rows[record['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        expected=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert result['boundaries'][1]['text_hex']==expected.hex()
        assert result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if value[0]==254:assert result['FE_original_null_actor_calls']
        dispatches.append(dict(id=record['id'],block=175,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in control['all7_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word']==0x4000:continue
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=175,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xC200:
            pair=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                pair.append(dict(version=label,**ctx.execute(C200,block,cmd)));ctx.machines.pop()
            assert pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes']
            uis.append(dict(source_offset=a,target_offset=b,cases=pair))
    assert len(dispatches)==32 and sum(d['resolved_actor_ID'] is None for d in dispatches)==9
    assert len(leaves)==7 and len(uis)==1 and not ctx.machines
    assert [r['word'] for r in leaves]==[0x6000,0x6344,0x4696,0x4635,0xC200,0,0]
    assert len(control['one_resource_word10_boundary_cases'])==10 and len(control['three_presentation_structural_cases'])==3
    assert not spec['relative_skip_fixups'] and not spec['target_native_skip_cases'] and not spec['original2000_pause_and_resume_maps']
    before_first_end=[]
    for c in spec['command_map']:
        before_first_end.append(c)
        if c['word']==0:break
    assert len(before_first_end)==38 and sum(c['word']==0x4000 for c in before_first_end)==32
    assert before_first_end[-2]['word']==0xC200 and before_first_end[-1]['new_offset']==1690
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all32_progressive_FE_dispatches_C200_pair_and7_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all7_source_current_target_nonrelative_nonspeech_leaves=leaves,relocated_C200_pairs=uis,
        all23_progressive_actors9_null_actor_FE_and_FI4_FA1_macro_expansions_exact=True,
        source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime=True,
        source_three_presentation_structures_reused_only_by_exact_whole_commands_and_runtime=True,
        original_no_relative_predicate_A000_pause_or_typed_objects_preserved=True,
        first_end_linear_structural_command_map=before_first_end,second_end_preserved_but_actual_reachability_pending=True,
        source_presentation_operand_semantics_not_inferred=True,presentation_resource_full_bodies_and_actual_scene_unexecuted_by_this_probe=True,
        later_older_record0D_reaudit_stays_open=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B175_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('32 relocated dispatches:23 progressive/nine null-actor FE,FI4/FA1;seven exact leaves,C200 pair and both ends pass. Actual reachability pending.')
