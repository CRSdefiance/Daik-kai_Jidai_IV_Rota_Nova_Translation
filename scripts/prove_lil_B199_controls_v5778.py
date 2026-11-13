"""Bind B199's exact controls, pictures, short47xx, pause extent and complete end."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B199_controls_v5778')
SOURCE=Path('work/analysis/lil_B199_source_v5767/all31_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B199_voices_v5768/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[199] for im in images]
    group=packet['blocks'][0];commands=group['all_current_native_commands']
    assert len(commands)==47 and sum(c['word']==0x4000 for c in commands)==31
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[
        (50,'31468480'),(54,'0505'),(56,'0020'),(370,'2d63'),(372,'2146c280'),
        (420,'0b63'),(504,'2a63'),(532,'0305'),(602,'214853a8'),(674,'3547'),
        (704,'2b63'),(806,'30467e80'),(914,'954853a8'),(1152,'00a0ffff01005330'),
        (1160,'2047'),(1162,'00000000')]
    words=[0x632D,0x630B,0x632A,0x632B]
    resource=checked_text(inspect.getsource(resource_base.control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word in [0x632D,0x630B,0x632A,0x632B];value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    env=dict(resource_base.__dict__);exec(compile(resource,__file__+'::four-source-resources','exec'),env)
    pic=checked_text(inspect.getsource(picture),{
        '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4895,0x4720,0x4735]',
        'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
        'if word in [0x4700,0x4720,0x4735]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None',
        '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4720,0x4735] else 4)'})
    picenv=dict(picture.__globals__);exec(compile(pic,__file__+'::source-picture47xx','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[];pictures=[];short=[];ends=[];structural=[]
    for c in leaves:
        word=c['word'];at=c['offset']
        if word in words:
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:
                    resources.append(dict(source_offset=at,source_word=word,
                        **ctx.execute(env['control630A'],previous,returned,word)));ctx.machines.pop()
        elif word in [0x4821,0x4895,0x4720,0x4735]:
            cases=[]
            for label,block in zip(['clean','current'],blocks,strict=True):
                cases.append(dict(version=label,**ctx.execute(picenv['picture'],block,c)));ctx.machines.pop()
            assert cases[0]['original_picture_boundary_calls']==cases[1]['original_picture_boundary_calls']
            entry=dict(source_offset=at,word=word,cases=cases)
            (pictures if word in [0x4821,0x4895] else short).append(entry)
        elif word==0:
            assert at==1162 and len(blocks[0])==len(blocks[1])==1168
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0]
                assert logical==1166 and block[logical:]==bytes(2)
                for previous in [0,1,2,3,0xFFFFFFFF]:
                    ends.append(dict(version=label,stored_bytes=len(block),logical_end=logical,tailzeros=2,
                        **end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word in [0x4631,0x0505,0x2000,0x4621,0x0503,0x4630,0xA000]
            value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value
            cases=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==word and result['rows'][0]['native_extent']==c['native_extent']
                cases.append(dict(version=label,**result))
            assert cases[0]['rows']==cases[1]['rows'] and cases[0]['opaque_effect_bridges']==cases[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=cases,
                isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(resources)==40 and len(pictures)==len(short)==2 and len(ends)==10 and len(structural)==7 and not ctx.machines
    descriptors=[r['cases'][0]['original_picture_boundary_calls'][0]['descriptor'] for r in pictures]
    layouts=[r['cases'][0]['original_picture_boundary_calls'][0]['layout'] for r in pictures]
    assert descriptors==[[0,83,1,5],[0,83,1,5]] and layouts==[[2,0,1],[9,1,1]]
    pause=next(r for r in structural if r['word']==0x2000)
    following=next(c for c in commands if c['offset']==58)
    assert pause['source_offset']==56 and following['word']==0x4000
    save(ROOT/'sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all16_source_current_nonspeech_leaves=leaves,four_resource_words40_boundary_cases=resources,
        source_two_picture_pairs=pictures,source_two_short47xx_pairs=short,source_seven_structural_pairs=structural,
        ten_guarded_complete_end_cases=ends,source_pause_resume_pair=dict(pause=56,resume=58,native_extent=2,
            next_word=0x4000,pause_duration_units_or_actual_wait_behavior_not_inferred=True),
        both_pictures_share_descriptor_but_have_distinct_source_layouts=True,
        descriptor83_not_assumed_item_title_or_powers=True,
        short47xx_original_boundary_and_return_and_entire_word_argument_bound=True,
        actual_scene_transition_resource_effect_and_picture_bodies_unexecuted=True,
        no_predicate_choice_relative_or_C200_inherited=True,
        source_owned_adapters=dict(resource=resource,picture47xx=pic,end=inspect.getsource(end_case),structural=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('16 leaves exact:40 resource cases,two picture/two47xx pairs,seven structural pairs,ten guarded ends;pause56 resumes58. Actual semantics pending.')
