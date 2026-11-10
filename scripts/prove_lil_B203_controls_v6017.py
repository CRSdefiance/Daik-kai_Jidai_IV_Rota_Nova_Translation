"""Bind B203's source controls without guessing rescue,item or stat effect bodies."""
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
ROOT=Path('work/analysis/lil_B203_controls_v6017')
SOURCE=Path('work/analysis/lil_B203_source_v6010/all22_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B203_voices_v6011/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[203] for im in images]
    group=packet['blocks'][0];commands=group['all_current_native_commands']
    assert len(commands)==31 and sum(c['word']==0x4000 for c in commands)==22
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[
        (334,'204812a8'),(738,'3547'),(740,'0360'),(742,'2e63'),
        (778,'00a0fffffaff0191'),(786,'00a0ffff01020260'),(794,'00a0ffff01001230'),(802,'00a0ffff1d000100'),(810,'00000000')]
    resource=checked_text(inspect.getsource(resource_base.control630A),{
        'previous,boundary_return):':'previous,boundary_return,word):',
        "value=bytes.fromhex('0a63')":"assert word in [0x632E];value=struct.pack('<H',word)",
        '[0x02386EFC,10,2,1]':'[0x02386EFC,word&255,2,1]'})
    env=dict(resource_base.__dict__);exec(compile(resource,__file__+'::two-source-resources','exec'),env)
    pic=checked_text(inspect.getsource(picture),{
        '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4820,0x4735]',
        'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
        'if word in [0x4700,0x4735]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None',
        '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4735] else 4)'})
    picenv=dict(picture.__globals__);exec(compile(pic,__file__+'::source-picture-and-short-call','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[];audio=[];pictures=[];short=[];ends=[];structural=[]
    for c in leaves:
        word=c['word'];at=c['offset']
        if word in [0x632E,0x6003]:
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:
                    f,args=(command6003,[previous,returned]) if word==0x6003 else (env['control630A'],[previous,returned,word])
                    (audio if word==0x6003 else resources).append(dict(source_offset=at,source_word=word,**ctx.execute(f,*args)));ctx.machines.pop()
        elif word in [0x4820,0x4735]:
            cases=[]
            for label,block in zip(['clean','current'],blocks,strict=True):
                cases.append(dict(version=label,**ctx.execute(picenv['picture'],block,c)));ctx.machines.pop()
            assert cases[0]['original_picture_boundary_calls']==cases[1]['original_picture_boundary_calls']
            (pictures if word==0x4820 else short).append(dict(source_offset=at,word=word,cases=cases))
        elif word==0:
            assert at==810 and len(blocks[0])==len(blocks[1])==816
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0];assert logical==814 and block[logical:]==bytes(2)
                for previous in [0,1,2,3,0xFFFFFFFF]:
                    ends.append(dict(version=label,stored_bytes=len(block),logical_end=logical,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word in [0xA000]
            value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;cases=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==word and result['rows'][0]['native_extent']==c['native_extent']
                cases.append(dict(version=label,**result))
            assert cases[0]['rows']==cases[1]['rows'] and cases[0]['opaque_effect_bridges']==cases[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=cases,
                isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(resources)==10 and len(audio)==10 and len(pictures)==len(short)==1 and len(ends)==10 and len(structural)==4 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0]
    assert call['descriptor']==[0,18,1,5] and call['layout']==[2,0,0]
    save(ROOT/'nine_exact_leaves_resource632E_6003_picture47xx_four_A000_pairs_and_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all9_source_current_nonspeech_leaves=leaves,one_resource632E_ten_boundary_cases=resources,source6003_ten_boundary_cases=audio,
        source_one_picture_pair=pictures,source_one_short47xx_pair=short,source_four_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,
        picture_descriptor18_layout2_0_0_not_assumed_item_name_or_powers=True,
        no_source4301_4600_4381_4640_transition_commands_invented=True,
        four_A000_operands_preserved_without_invented_payment_reward_or_stat_body_semantics=True,
        short47xx_original_boundary_return_entire_word_argument_bound=True,
        actual_resource_effect_picture_payment_stat_bodies_and_all22_objects_still_unobserved=True,
        one_source_FE_FI_notice_no_FA_FO_predicate_choice_relative_or2000_pause_invented=True,
        source_owned_adapters=dict(resource=resource,picture47xx=pic,command6003=inspect.getsource(command6003),end=inspect.getsource(end_case),structural=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B2039 leaves exact:10 resource/10 6003 boundary cases,one picture/one47xx pair,four A000 pairs,ten guarded ends. Descriptor18/layout2,0,0;actual semantics pending.')
