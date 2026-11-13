"""Bind all27 relocated dispatches,original C200 queue then A000 and all eleven leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B172_research_v4383 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_relocated_controls_v4388')
DOC=Path('translations/lil_B172_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN)
    packet=read(doc['source_context'])
    dp,cp=read(doc['control_contract']),read(doc['source_effect_and_predicate_contract'])
    old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[172] for p in [PARENT,ROM]]
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
        assert result['boundaries'][1]['text_hex']==value[1:].hex()
        dispatches.append(dict(id=record['id'],block=172,new_offset=at,stored_target_hex=value.hex(),**result))
    old_leaves={r['offset']:r for r in cp['all11_source_current_nonrelative_nonspeech_leaves']}
    for command in spec['command_map']:
        if command['word']==0x4000:continue
        assert command['word'] not in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0x2000]
        a,b=command['old_offset'],command['new_offset']
        previous,value=old[a:a+command['old_extent']],new[b:b+command['new_extent']]
        assert previous==value and old_leaves[a]['source_current_hex']==value.hex()
        assert old_leaves[a]['word']==command['word'] and old_leaves[a]['native_extent']==len(value)
        leaves.append(dict(block=172,word=command['word'],old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if command['word']==0xC200:
            paired=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                cmd=dict(offset=at,word=0xC200,native_extent=2,whole_command_hex=value.hex())
                paired.append(dict(version=label,**ctx.execute(C200,block,cmd)))
                ctx.machines.pop()
            assert paired[0]['source_owned_UI_request_words']==paired[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
            assert paired[0]['source_owned_UI_writes']==paired[1]['source_owned_UI_writes']==cp['source_C200_pairs'][0]['cases'][0]['source_owned_UI_writes']
            c200.append(dict(source_offset=a,target_offset=b,cases=paired))
    assert len(dispatches)==27 and len(leaves)==11 and len(c200)==1 and not ctx.machines
    assert [r['word'] for r in leaves]==[0x6000,0x45FF,0x6329,0x4651,0x6340,0x4620,0x632A,0xC200,0xA000,0x6240,0]
    assert len(cp['three_resource_words30_boundary_cases'])==30
    assert len(cp['five_presentation_structural_cases'])==5 and len(cp['one_later_A000_structural_case'])==1
    assert cp['source_A000_hex']=='00a0ffff010cc960' and cp['source_A000_raw_hex_words']==['0C01','60C9']
    assert cp['source_C2001868_then_A0001870_then6240_1878_then_end1880_preserved']
    assert not spec['original2000_pause_and_resume_maps'] and not spec['relative_skip_fixups']
    assert [r['old_offset'] for r in leaves[-4:]]==[1868,1870,1878,1880]
    assert leaves[-3]['source_current_target_hex']=='00a0ffff010cc960'
    paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all27_progressive_dispatches_C200_then_A000_and11_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,relocated_predicate_pairs=[],all11_source_current_target_nonrelative_nonspeech_leaves=leaves,
        relocated_C200_pairs=c200,all27_progressive_consumers_no_macros_exact=True,
        original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor=True,
        source_resource30_boundary_cases_reused_only_by_exact_words_and_runtime=True,
        source_five_presentation_and_one_A000_structural_results_reused_only_by_exact_whole_commands_and_runtime=True,
        presentation_resource_later_A000_bodies_not_fully_executed_by_this_probe=True,
        single_tail_end_and_no_source_pause_preserved=True,source_A000_hex=cp['source_A000_hex'],source_A000_raw_hex_words=cp['source_A000_raw_hex_words'],source_C200_then_A000_then6240_and_end_preserved=True,
        no_source_relative_sites_or_membership_predicates=True,later_older_record0D_reaudit_stays_open=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B172_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('27 relocated dispatches,11 exact leaves,C200 queue pair then A000/6240 and one tail end pass. Actual presentations and transitions remain pending.')
