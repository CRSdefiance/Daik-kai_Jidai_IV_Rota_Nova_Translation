"""Bind source conditional paths,resource42,two C200 sites and exact nontext leaves."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B190_C200_v5318 import C200,adapter_source
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B194_controls_v5495')
SOURCE=Path('work/analysis/lil_B194_source_v5489/all11_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B194_branches_v5493/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,branch=map(read,[SOURCE,BRANCH]);group=packet['blocks'][0]
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[194] for im in images]
    commands=group['all_current_native_commands'];leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=194,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(c['offset'],c['source_current_hex']) for c in leaves]==[(8,'00a0ffff012536a1'),(312,'0080ffff06fe0030'),(406,'2a63'),(494,'00c2'),(534,'00c2'),(536,'00000000')]
    assert len(commands)==21 and len(blocks[0])==len(blocks[1])==540 and packet['source_macro_counts']==dict(FI=1,FA=0,FO=0)
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==40
    text=inspect.getsource(resource_base.control630A)
    replacements={'def control630A(':'def source632A(',"value=bytes.fromhex('0a63')":"value=bytes.fromhex('2a63')",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,42,2,1]',
        'cpu.mem_write(result,bytes(24))':"cpu.mem_write(result,struct.pack('<6I',0,previous,0,0,0,0))",
        'decoded==[3,0,0,0,0,0]':'decoded==[3,previous,0,0,0,0]'}
    for old,new in replacements.items():assert old in text; text=text.replace(old,new)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::source-resource42-prior-result','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicate=next(c for c in commands if c['word']==0x8000);predicates=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        r=ctx.execute(probe,block,predicate);ctx.machines.pop();assert not r['original_event_completion_calls']
        predicates.append(dict(version=label,**r))
    assert predicates[0]['native_result']==predicates[1]['native_result']
    uis=[]
    for c in [c for c in commands if c['word']==0xC200]:
        pair=[]
        for label,block in zip(['clean','current'],blocks,strict=True):pair.append(dict(version=label,**ctx.execute(C200,block,c)));ctx.machines.pop()
        assert pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,2,13,0,0,0,1]
        assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes']
        uis.append(dict(source_offset=c['offset'],cases=pair))
    resources=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for incidental in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['source632A'],previous,incidental));ctx.machines.pop()
    assert len(resources)==10 and not ctx.machines
    raw=bytes.fromhex(leaves[0]['source_current_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;effects=[]
    for label,image in zip(['clean','current'],images,strict=True):
        r=walk(image.read_file('/__arm9__.bin'),isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated)
        assert len(r['rows'])==1 and r['rows'][0]['word']==0xA000 and r['rows'][0]['native_extent']==8;effects.append(dict(version=label,**r))
    assert effects[0]['rows']==effects[1]['rows'] and effects[0]['opaque_effect_bridges']==effects[1]['opaque_effect_bridges']
    byat={c['offset']:c for c in commands};speech={r['source_reference']['header_offset']:r for r in packet['records']}
    def path(last):
        cursor=8;visited=[];spoken=[];controls=[]
        for _ in range(30):
            c=byat[cursor];word=c['word'];visited.append(cursor)
            if word==0:return dict(predicate_result=last,source_command_offsets=visited,speech_record_indices=spoken,non_speech_non_relative_offsets=controls+[cursor],source_end_offset=cursor,not_full_VM_or_actual_scene_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last];assert len(cases)==1
                cursor=cases[0]['original_next_command_offset'];continue
            if word==0x4000:spoken.append(speech[cursor]['source_record_index'])
            else:controls.append(cursor)
            cursor+=c['native_extent']
        raise AssertionError('source path did not terminate')
    paths=[path(v) for v in [0,1]]
    assert [len(p['speech_record_indices']) for p in paths]==[9,11] and all(p['source_end_offset']==536 for p in paths)
    assert [p['non_speech_non_relative_offsets'] for p in paths]==[[8,312,534,536],[8,312,406,494,534,536]]
    save(ROOT/'one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all6_source_current_nonrelative_nonspeech_leaves=leaves,source_predicate_cases=predicates,source_C200_pairs=uis,source_resource42_boundary_and_carried_result_cases=resources,
        source_A000_structural_cases=effects,source_structural_predicate0_1_paths=paths,source_relative_native_cases=40,
        resource632A_dispatches_original_resource42_boundary_and_preserves_five_prior_results=True,resource_body_explicitly_bridged_and_unexecuted=True,
        one_FI_in_conditional_Julio6_interjection_preserved_without_forced_actual_branch=True,
        C200494_is_conditional_C200534_is_common_and_both_original_fleet_descriptors_bound=True,
        source_A000_raw_bytes_preserved_packed_semantics_not_inferred=True,
        full_scene_eligibility_resource_body_C200_actual_UI_and_return_unexecuted=True,
        source_owned_adapters=dict(predicate=inspect.getsource(probe),C200=adapter_source(),resource42=text,isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(unforced_results=[p['native_result'] for p in predicates],resource_cases=10,C200_sites=[p['source_offset'] for p in uis],source_path_speech_counts=[len(p['speech_record_indices']) for p in paths],source_complete_paths_only_not_actual_gameplay=True,credit=0))
