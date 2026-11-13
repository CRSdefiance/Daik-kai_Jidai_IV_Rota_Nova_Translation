"""Bind all37 relocated dispatches, original C200 queue and all eight leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B171_research_v4334 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B171_relocated_controls_v4339')
DOC=Path('translations/lil_B171_editorial_manuscript_v4.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN)
    packet=read(doc['source_context'])
    dp,cp=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[171] for p in [PARENT,ROM]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']
    assert NdsImage.open(PARENT).read_file('/__arm9__.bin')==NdsImage.open(ROM).read_file('/__arm9__.bin')
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
        assert result['boundaries'][1]['text_hex']==value[1:].replace(b'FI',b'Lil').hex()
        dispatches.append(dict(id=record['id'],block=171,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in cp['all8_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word']==0x4000:continue
        assert command['word'] not in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0xA000,0x2000]
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=171,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xC200:
            paired=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                paired.append(dict(version=label,**ctx.execute(C200,block,cmd)))
                ctx.machines.pop()
            assert paired[0]['source_owned_UI_request_words']==paired[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert paired[0]['source_owned_UI_writes']==paired[1]['source_owned_UI_writes']==cp['source_C200_pairs'][0]['cases'][0]['source_owned_UI_writes']
            c200.append(dict(source_offset=a,target_offset=b,cases=paired))
    assert len(dispatches)==37 and len(leaves)==8 and len(c200)==1 and not ctx.machines
    assert [r['word'] for r in leaves]==[0x6000,0x4500,0x4621,0x61FF,0x6325,0xC200,0,0]
    assert len(cp['one_resource_word10_boundary_cases'])==10
    assert len(cp['four_presentation_structural_cases'])==4
    assert not spec['original2000_pause_and_resume_maps'] and not spec['relative_skip_fixups']
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all37_progressive_dispatches_C200_and8_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,relocated_predicate_pairs=[],all8_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=c200,all37_progressive_consumers_FI1_FO0_exact=True,
        original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor=True,
        source_resource10_boundary_cases_reused_only_by_exact_word_and_runtime=True,
        source_four_presentation_structural_results_reused_only_by_exact_whole_commands_and_runtime=True,
        presentation_resource_bodies_not_fully_executed_by_this_probe=True,
        both_consecutive_endwords_and_no_source_pause_or_A000_preserved=True,
        no_source_relative_sites_or_membership_predicates=True,later_older_record0D_reaudit_stays_open=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B171_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('37 relocated dispatches,8 exact leaves,C200 queue pair and both ends pass. Actual presentations and transitions remain pending.')
