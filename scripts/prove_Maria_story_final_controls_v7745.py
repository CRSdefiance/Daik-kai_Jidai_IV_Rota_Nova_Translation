"""Final67 native dispatches, exact numeric leaves and focused original control contracts."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B196_6003_ends_v5597 import command6003,end_case
from scripts.prove_maria_B109_controls_v3502 import pause
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_controls_v7745')
MAP=Path('work/analysis/maria_story_relocation_v7742/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
SOURCE=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
CONSUMERS=Path('work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json')
STORED=Path('work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,source,consumers,stored=map(read,[MAP,CURRENT,SOURCE,CONSUMERS,STORED])
    im=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']
    bank=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':3,'route_mask':8,'CATALOG_LOOKUP':{}}
    for name,text in consumers['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(consumers['source_owned_measured_macro_body_adapter'],__file__+'::measured-Maria-body','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](im)
    resource_adapter=checked_text(inspect.getsource(resource_base.control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word in [0x633F,0x632D,0x633C,0x632A];value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    re=dict(resource_base.__dict__);exec(compile(resource_adapter,__file__+'::four-original-63xx-controls','exec'),re)
    setup_adapter=checked_text(inspect.getsource(command6003),{
        "value=bytes.fromhex('0360')":"value=bytes.fromhex('0060')",
        '[0x02386EFC,3]':'[0x02386EFC,0]'})
    se=dict(command6003.__globals__);exec(compile(setup_adapter,__file__+'::original-6000-control','exec'),se)
    end_adapter=checked_text(inspect.getsource(end_case),{
        'def end_case(arm,block,offset,previous):':'def end_case(arm,common,raw,plan,block,offset,previous):',
        'cpu=machine(arm);':'cpu,get,provider=machine(arm,common,raw,plan);'})
    ee=dict(end_case.__globals__);exec(compile(end_adapter,__file__+'::own-current-complete-end','exec'),ee)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    dispatches=[]
    for group in mapping['groups']:
        block=bank[group['block']];assert sha(block)==group['target_block_sha256']
        for ref in group['text_records']:
            value=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(value)+1]==value+b'\0'
            result=ctx.execute(ns['dispatch'],value[0],value[1:]);ctx.machines.pop()
            original=next(r for r in stored['records'] if r['id']==ref['id'])
            assert result['resolved_actor_ID']==value[0] and result['registered_catalog_match'] is None
            assert next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body')['text_hex']==original['final_expanded_hex']
            dispatches.append(dict(id=ref['id'],file_path=group['file_path'],final_offset=at,final_stored_hex=value.hex(),**result))
    numeric=[];opaque={}
    for sg,cg,tg in zip(source['groups'],current['groups'],mapping['groups'],strict=True):
        assert sg['block']==cg['block']==tg['block']
        triples=zip(sg['commands'],cg['all_current_commands'],tg['all_target_commands'],strict=True)
        for a,b,c in triples:
            assert a['word']==b['word']==c['word']
            if a['word'] in [0x4000,0x100,0x200,0x300,0x400,0x8000,0x8100]:continue
            assert a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex']
            numeric.append(dict(block=sg['block'],word=a['word'],source_offset=a['offset'],current_offset=b['offset'],target_offset=c['offset'],
                source_hex=a['whole_command_hex'],source_extent=a['native_extent'],target_extent=c['native_extent']))
            if a['word'] in [0xA000,0x4631,0x0514,0x4630,0x050A,0x623C]:
                value=bytes.fromhex(a['whole_command_hex'])
                if value.hex() not in opaque:
                    isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value
                    structural=walk(ctx.arm,isolated)
                    assert structural['error'] is None and structural['logical_end']==structural['stopped_offset']==len(value)+8
                    opaque[value.hex()]=dict(source_hex=value.hex(),**structural,isolated_structural_decoder_not_full_effects_orwhole_VM=True)
    resources=[];setups=[];pauses=[];c200=[];ends=[]
    for word in [0x633F,0x632D,0x633C,0x632A]:
        assert any(r['word']==word for r in numeric)
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for returned in [0,0xFFFFFFFF]:
                resources.append(ctx.execute(re['control630A'],previous,returned,word));ctx.machines.pop()
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for returned in [0,0xFFFFFFFF]:
            setups.append(ctx.execute(se['command6003'],previous,returned));ctx.machines.pop()
            pauses.append(ctx.execute(pause,previous,returned));ctx.machines.pop()
    for sg,cg,tg in zip(source['groups'],current['groups'],mapping['groups'],strict=True):
        versions=[('clean-Japanese',bytes.fromhex(sg['clean_block_hex']),sg['commands']),
                  ('current-English',bytes.fromhex(cg['current_block_hex']),cg['all_current_commands']),
                  ('relocated-English',bank[tg['block']],tg['all_target_commands'])]
        for label,block,commands in versions:
            for command in commands:
                if command['word']==0xC200:
                    result=ctx.execute(C200,block,command);ctx.machines.pop();c200.append(dict(block=tg['block'],version=label,**result))
            terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4
            for previous in [0,1,2,3,0xFFFFFFFF]:
                result=ctx.execute(ee['end_case'],block,terminal['offset'],previous);ctx.machines.pop()
                ends.append(dict(block=tg['block'],version=label,**result))
    assert len(dispatches)==67 and len(resources)==40 and len(setups)==len(pauses)==10 and len(c200)==3 and len(ends)==45 and not ctx.machines
    assert all(r['source_owned_UI_request_words']==c200[0]['source_owned_UI_request_words'] for r in c200)
    save(ROOT/'67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json',dict(
        candidate=mapping['candidate'],candidate_sha256=mapping['candidate_sha256'],final_archive=mapping['target_archive'],final_archive_sha256=mapping['target_archive_sha256'],
        final_dispatches=dispatches,current_registered_catalogue_binding=catalogue,all67_final_stored_dispatches_have_no_catalogue_override=True,
        exact_source_current_target_numeric_leaves=numeric,isolated_opaque_structural_cases=list(opaque.values()),
        native_63xx_resource_boundary_cases=resources,original6000_setup_boundary_cases=setups,original2000_pause_boundary_cases=pauses,
        source_current_target_C200_cases=c200,source_current_target_complete_normal_end_cases=ends,
        source_owned_adapters=dict(resource63xx=resource_adapter,setup6000=setup_adapter,pause2000=inspect.getsource(pause),C200=inspect.getsource(C200),normal_end=end_adapter),
        all_original_ABI_guards_owned_UI_spans_andunowned4MiB_preserved=True,
        unused_resource_andpause_return_values_not_source_story_conditions=True,
        resource_callee_UI_audio_bodies_andopaque_A000_effects_not_executed_to_completion=True,
        exact_46xx_05xx_623C_andA000_bytes_andstructural_widths_not_full_scene_semantics=True,
        no_actual_button_pagination_natural_activation_orfull_gameplay_effect_claim=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,CURRENT,SOURCE,CONSUMERS,STORED,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('67final dispatches;numeric leaves',len(numeric),';unique opaque structural cases',len(opaque),';40resources/10setup/10pause/3C200/45complete-end native cases.All guards pass.Actual fullscene/effects remainpending.')
