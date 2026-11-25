"""Bind all relocated B174 speech,predicate,relative paths and eight numeric leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B174_research_v4481 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_relocated_controls_v4486')
DOC=Path('translations/lil_B174_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN);packet=read(doc['source_context'])
    dispatch,control=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[174] for p in [PARENT,ROM]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==control['candidate_sha256']
    assert NdsImage.open(PARENT).read_file('/__arm9__.bin')==NdsImage.open(ROM).read_file('/__arm9__.bin')
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(dispatch['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};spec=plan['blocks'][0]
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    dispatches=[];leaves=[];predicates=[];uis=[]
    for record in spec['text_records']:
        value,at=bytes.fromhex(record['target_hex']),record['new_offset']
        assert new[at:at+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        assert result['resolved_actor_ID']==rows[record['id']]['source_selector'] and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==value[1:].hex()
        dispatches.append(dict(id=record['id'],block=174,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in control['all8_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=174,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0x8000:
            pair=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0x8000,native_extent=8,whole_command_hex=value.hex())
                pair.append(dict(version=label,**ctx.execute(probe,block,cmd)));ctx.machines.pop()
            assert pair[0]['native_result']==pair[1]['native_result']==control['source_predicate_cases'][1]['native_result']==[2,1,0,0,0,0]
            predicates.append(dict(source_offset=a,target_offset=b,cases=pair))
        if command['word']==0xC200:
            pair=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                pair.append(dict(version=label,**ctx.execute(C200,block,cmd)));ctx.machines.pop()
            assert pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes']
            uis.append(dict(source_offset=a,target_offset=b,cases=pair))
    assert len(dispatches)==33 and len(leaves)==8 and len(predicates)==1 and len(uis)==1 and not ctx.machines
    assert [r['word'] for r in leaves]==[0x6000,0x6340,0x8000,0x6240,0xA000,0xA000,0xC200,0]
    assert len(control['one_resource_word10_boundary_cases'])==10
    assert len(control['two_presentation_structural_cases'])==len(control['two_A000_structural_cases'])==2
    assert not spec['original2000_pause_and_resume_maps'] and len(spec['relative_skip_fixups'])==4 and len(spec['target_native_skip_cases'])==20
    mapping={c['old_offset']:c for c in spec['command_map']};target_commands={c['new_offset']:c for c in spec['command_map']}
    paths=[]
    for original in control['complete_two_boolean_suffix_paths']:
        last=original['predicate_result'];cursor=8;visited=[];effects=[]
        while True:
            command=target_commands[cursor];word=command['word'];visited.append(cursor)
            if word==0:break
            if word in [0x100,0x200,0x300,0x400]:
                cases=[c for c in spec['target_native_skip_cases'] if c['new_offset']==cursor and c['last_result']==last]
                assert len(cases)==1;cursor+=cases[0]['native_extent'];continue
            if word==0xA000:effects.append(cursor)
            cursor+=command['new_extent']
        assert visited==[mapping[a]['new_offset'] for a in original['native_command_offsets']]
        assert effects==[mapping[a]['new_offset'] for a in original['original_A000_offsets']]
        paths.append(dict(predicate_result=last,original_command_offsets=original['native_command_offsets'],relocated_command_offsets=visited,
            original_A000_offsets=original['original_A000_offsets'],relocated_A000_offsets=effects,source_end=original['source_end_offset'],target_end=cursor,
            original_native_skip_cases_used_not_full_VM_or_effect_execution=True))
    paths_to_hash=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all33_dispatches_predicate_pair_four_relative_sites_two_A000s_and8_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,all8_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=uis,all33_progressive_consumers_no_macros_exact=True,
        original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor=True,
        source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime=True,
        source_two_presentation_and_two_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime=True,
        source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths=paths,
        source_A000_hex_by_offset=control['source_A000_hex_by_offset'],source_A000_raw_hex_words_by_offset=control['source_A000_raw_hex_words_by_offset'],
        source_predicate_hex=control['source_predicate_hex'],source_predicate_raw_hex_words=control['source_predicate_raw_hex_words'],
        source_packed_effect_and_predicate_semantics_not_inferred=True,single_tail_end_and_no_source_pause_preserved=True,
        source32_unconditional_speeches_and_optional_Emilio69_preserved=True,presentation_resource_and_two_A000_bodies_not_fully_executed_by_this_probe=True,
        later_older_record0D_reaudit_stays_open=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths_to_hash},actual_selected_B174_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('33 relocated dispatches,eight exact leaves,predicate/C200 pairs,four relative sites/20 native cases and both optional-speech paths pass. Actual scene/effect bodies pending.')
