"""Bind33 relocated dispatches,original C200 queue behavior,pause andall12 leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B170_research_v4283 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_relocated_controls_v4288')
DOC=Path('translations/lil_B170_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN)
    packet=read(doc['source_context'])
    dp,cp=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[170] for p in [PARENT,ROM]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():
        exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']}
    spec=plan['blocks'][0]
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    dispatches,leaves,c200=[],[],[]
    for record in spec['text_records']:
        value,at=bytes.fromhex(record['target_hex']),record['new_offset']
        assert new[at:at+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:])
        ctx.machines.pop()
        assert result['resolved_actor_ID']==rows[record['id']]['source_selector']
        assert result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==value[1:].replace(b'FI',b'Lil').replace(b'FO',b'Argot Co.').hex()
        dispatches.append(dict(id=record['id'],block=170,new_offset=at,stored_target_hex=value.hex(),**result))
    for command in spec['command_map']:
        if command['word']==0x4000:continue
        assert command['word'] not in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100]
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value
        leaves.append(dict(block=170,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xC200:
            source_command=dict(offset=a,word=0xC200,native_extent=2,whole_command_hex=value.hex())
            target_command=dict(offset=b,word=0xC200,native_extent=2,whole_command_hex=value.hex())
            paired=[]
            for label,block,cmd in [('current',old,source_command),('relocated',new,target_command)]:
                paired.append(dict(version=label,**ctx.execute(C200,block,cmd)))
                ctx.machines.pop()
            assert paired[0]['source_owned_UI_request_words']==paired[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert paired[0]['source_owned_UI_writes']==paired[1]['source_owned_UI_writes']==cp['source_C200_pairs'][0]['cases'][0]['source_owned_UI_writes']
            c200.append(dict(source_offset=a,target_offset=b,cases=paired))
    assert len(dispatches)==33 and len(leaves)==12 and len(c200)==1 and not ctx.machines
    assert sum(r['word']==0 for r in leaves)==2 and sum(r['word']==0xA000 for r in leaves)==1
    assert [r['word'] for r in leaves if r['word']&0xFF00==0x6300]==[0x6342,0x632D]
    assert len(cp['two_resource_words20_boundary_cases'])==20
    assert len(spec['original2000_pause_and_resume_maps'])==1
    pause=spec['original2000_pause_and_resume_maps'][0]
    assert pause['old_offset']==36 and pause['source_resume']==38 and pause['target_resume']==pause['new_offset']+2
    assert old[36:38]==new[pause['new_offset']:pause['new_offset']+2]==b'\0\x20'
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all33_progressive_dispatches_C200_pause_and12_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,relocated_predicate_pairs=[],all12_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=c200,source_pause_and_mapped_resume=pause,all33_progressive_consumers_FI1_FO1_exact=True,
        original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor=True,
        source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime=True,
        source_other_presentation_structural_results_reused_only_by_exact_whole_commands_and_runtime=True,
        source_A000_and_presentation_resource_bodies_not_fully_executed_by_this_probe=True,
        source_A000_hex='00a0ffff19100120',source_A000_after_final_encouragement_before_C200_and_both_ends_preserved=True,
        both_consecutive_endwords_and_one_pause_preserved=True,no_source_relative_sites_or_membership_predicates=True,
        later_older_record0D_reaudit_stays_open=True,registered_catalog_binding=binding,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B170_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('33 relocated dispatches,12 exact leaves,C200 source/target queue pair,pause/resume and both ends pass. Actual effects/transitions remain pending.')
