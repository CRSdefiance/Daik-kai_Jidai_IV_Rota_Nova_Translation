"""Bind B200's source controls without guessing rescue,item or stat effect bodies."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import command6003,end_case
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_controls_v5833')
SOURCE=Path('work/analysis/lil_B200_source_v5826/all19_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B200_voices_v5827/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[200] for im in images]
    group=packet['blocks'][0];commands=group['all_current_native_commands']
    assert len(commands)==31 and sum(c['word']==0x4000 for c in commands)==19
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[
        (8,'2d63'),(94,'0143'),(96,'00460b80'),(100,'8143'),(618,'304865a8'),(718,'3547'),
        (864,'0360'),(866,'2e63'),(906,'00a0ffff01021360'),(914,'00a0ffff01006530'),(922,'4046081d'),(926,'00000000')]
    resource=checked_text(inspect.getsource(resource_base.control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word in [0x632D,0x632E];value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    env=dict(resource_base.__dict__);exec(compile(resource,__file__+'::two-source-resources','exec'),env)
    pic=checked_text(inspect.getsource(picture),{
        '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4830,0x4735]',
        'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
        'if word in [0x4700,0x4735]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None',
        '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4735] else 4)'})
    picenv=dict(picture.__globals__);exec(compile(pic,__file__+'::source-picture-and-short-call','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[];audio=[];pictures=[];short=[];ends=[];structural=[]
    for c in leaves:
        word=c['word'];at=c['offset']
        if word in [0x632D,0x632E,0x6003]:
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:
                    f,args=(command6003,[previous,returned]) if word==0x6003 else (env['control630A'],[previous,returned,word])
                    (audio if word==0x6003 else resources).append(dict(source_offset=at,source_word=word,**ctx.execute(f,*args)));ctx.machines.pop()
        elif word in [0x4830,0x4735]:
            cases=[]
            for label,block in zip(['clean','current'],blocks,strict=True):
                cases.append(dict(version=label,**ctx.execute(picenv['picture'],block,c)));ctx.machines.pop()
            assert cases[0]['original_picture_boundary_calls']==cases[1]['original_picture_boundary_calls']
            (pictures if word==0x4830 else short).append(dict(source_offset=at,word=word,cases=cases))
        elif word==0:
            assert at==926 and len(blocks[0])==len(blocks[1])==932
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0];assert logical==930 and block[logical:]==bytes(2)
                for previous in [0,1,2,3,0xFFFFFFFF]:
                    ends.append(dict(version=label,stored_bytes=len(block),logical_end=logical,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word in [0x4301,0x4600,0x4381,0xA000,0x4640]
            value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;cases=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==word and result['rows'][0]['native_extent']==c['native_extent']
                cases.append(dict(version=label,**result))
            assert cases[0]['rows']==cases[1]['rows'] and cases[0]['opaque_effect_bridges']==cases[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=cases,
                isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(resources)==20 and len(audio)==10 and len(pictures)==len(short)==1 and len(ends)==10 and len(structural)==6 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0]
    assert call['descriptor']==[0,101,1,5] and call['layout']==[3,0,0]
    save(ROOT/'twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all12_source_current_nonspeech_leaves=leaves,two_resource_words20_boundary_cases=resources,source6003_ten_boundary_cases=audio,
        source_one_picture_pair=pictures,source_one_short47xx_pair=short,source_six_structural_pairs=structural,ten_guarded_complete_end_cases=ends,
        picture_descriptor101_layout3_0_0_not_assumed_item_name_or_powers=True,
        source4301_4600_4381_and_final4640_preserved_without_forced_transition_or_location=True,
        two_A000_operands_preserved_without_invented_reward_or_stat_body_semantics=True,
        short47xx_original_boundary_return_entire_word_argument_bound=True,
        actual_scene_transition_resource_effect_picture_stat_bodies_and_all19_speeches_still_unobserved=True,
        no_predicate_choice_relative_FI_or2000_pause_inherited=True,
        source_owned_adapters=dict(resource=resource,picture47xx=pic,command6003=inspect.getsource(command6003),end=inspect.getsource(end_case),structural=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20012 leaves exact:20 resource/10 6003 boundary cases,one picture/one47xx pair,six structural pairs,ten guarded ends. Actual semantics pending.')
