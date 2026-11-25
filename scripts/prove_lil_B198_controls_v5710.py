"""Bind every B198 control leaf without guessing its scene or item semantics."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B198_controls_v5710')
SOURCE=Path('work/analysis/lil_B198_source_v5702/all17_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B198_voices_v5703/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet=read(SOURCE)
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[198] for im in images]
    group=packet['blocks'][0]
    commands=group['all_current_native_commands']
    assert len(commands)==37 and sum(c['word']==0x4000 for c in commands)==17
    leaves=[]
    for source,current in zip(group['all_clean_native_commands'],commands,strict=True):
        assert source['offset']==current['offset'] and source['whole_command_hex']==current['whole_command_hex']
        if current['word'] not in [0x4000,0x100,0x200,0x300,0x400]:
            leaves.append(current)
    assert len(leaves)==12
    resource=checked_text(inspect.getsource(resource_base.control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word==0x633F;value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    env=dict(resource_base.__dict__)
    exec(compile(resource,__file__+'::source633F','exec'),env)
    pic=checked_text(inspect.getsource(picture),{
        'word in [0x4821,0x4822,0x4823,0x4700]':'word in [0x4821,0x4822,0x4823,0x4700,0x4835]'})
    picenv=dict(picture.__globals__)
    exec(compile(pic,__file__+'::source4835','exec'),picenv)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicates=[];resources=[];pictures=[];ends=[];structural=[]
    for c in leaves:
        if c['word']==0x8000:
            assert c['offset'] in [306,480] and c['whole_command_hex']=='0080ffff0ffe0030'
            result=ctx.execute(probe,blocks[1],c);ctx.machines.pop()
            assert not result['original_event_completion_calls']
            predicates.append(result)
        elif c['word']==0x633F:
            assert c['offset']==16
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:
                    resources.append(ctx.execute(env['control630A'],previous,returned,0x633F));ctx.machines.pop()
        elif c['word']==0x4835:
            assert c['offset']==364 and c['whole_command_hex']=='35482aa8'
            for label,block in zip(['clean','current'],blocks,strict=True):
                pictures.append(dict(version=label,**ctx.execute(picenv['picture'],block,c)));ctx.machines.pop()
            assert pictures[0]['original_picture_boundary_calls']==pictures[1]['original_picture_boundary_calls']
        elif c['word']==0:
            assert c['offset']==540
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                for previous in [0,1,2,3,0xFFFFFFFF]:
                    ends.append(dict(version=label,**end_case(image.read_file('/__arm9__.bin'),block,540,previous)))
        else:
            assert c['word'] in [0x6000,0x4500,0xA000,0x623F,0x4621,0x61FF]
            value=bytes.fromhex(c['whole_command_hex'])
            isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value
            versions=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==c['word']
                assert result['rows'][0]['native_extent']==c['native_extent']
                versions.append(dict(version=label,**result))
            assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=c['offset'],source_command_hex=value.hex(),word=c['word'],versions=versions,
                isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_semantic_or_display_execution=True))
    assert len(predicates)==2 and len(resources)==10 and len(pictures)==2 and len(ends)==10 and len(structural)==7
    assert not ctx.machines
    save(ROOT/'twelve_exact_leaves_two_predicates_resource_picture_seven_structural_pairs_and_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all12_source_current_nonrelative_nonspeech_leaves=leaves,source_two_unforced_predicates=predicates,
        source633F_ten_boundary_cases=resources,source4835_picture_clean_current_cases=pictures,
        source_seven_presentation_and_effect_structural_pairs=structural,source540_ten_guarded_end_cases=ends,
        source_owned_adapters=dict(predicate=inspect.getsource(probe),resource=resource,picture=pic,end=inspect.getsource(end_case)),
        source_predicate_semantics_not_inferred_from_Angelo_speech=True,
        picture_descriptor_not_assumed_item_identity_or_title=True,
        source_effect_and_resource_bodies_and_actual_scene_transitions_unexecuted=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B19812 exact leaves:two unforced predicates,10resource cases,one clean/current picture pair,seven structural pairs and10guarded end cases. Bodies/scene semantics pending;no credit.')
