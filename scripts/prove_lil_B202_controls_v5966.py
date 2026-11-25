"""Bind B202's seven exact leaves and original boundaries without effect guesses."""
import inspect,struct
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
ROOT=Path('work/analysis/lil_B202_controls_v5966')
SOURCE=Path('work/analysis/lil_B202_source_v5959/all19_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B202_voices_v5960/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[202] for im in images];group=packet['blocks'][0];commands=group['all_current_native_commands'];leaves=[]
    assert len(commands)==26 and sum(c['word']==0x4000 for c in commands)==19
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(162,'2a63'),(182,'2a63'),(322,'35480ea8'),(564,'00a0ffff01000e30'),(572,'2147'),(574,'00a0ffff1d000100'),(582,'00000000')]
    resource=checked_text(inspect.getsource(resource_base.control630A),{"value=bytes.fromhex('0a63')":"value=bytes.fromhex('2a63')",'[0x02386EFC,10,2,1]':'[0x02386EFC,42,2,1]'})
    env=dict(resource_base.__dict__);exec(compile(resource,__file__+'::original632A-boundary','exec'),env)
    pic=checked_text(inspect.getsource(picture),{
      '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4835,0x4721]',
      'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
      'if word in [0x4700,0x4721]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None',
      '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4721] else 4)'})
    picenv=dict(picture.__globals__);exec(compile(pic,__file__+'::source4835-and4721','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');resources=[];pictures=[];short=[];structural=[];ends=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for returned in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,returned));ctx.machines.pop()
    for c in leaves:
        word,at=c['word'],c['offset']
        if word==0x632A:continue
        if word in [0x4835,0x4721]:
            cases=[]
            for label,block in zip(['clean','current'],blocks,strict=True):cases.append(dict(version=label,**ctx.execute(picenv['picture'],block,c)));ctx.machines.pop()
            assert cases[0]['original_picture_boundary_calls']==cases[1]['original_picture_boundary_calls'];(pictures if word==0x4835 else short).append(dict(source_offset=at,word=word,cases=cases))
        elif word==0:
            assert at==582
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0];assert logical==586 and len(block)==588 and block[logical:]==bytes(2)
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,stored_bytes=588,logical_end=586,tailzeros=2,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word==0xA000;value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;cases=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==word and result['rows'][0]['native_extent']==8;cases.append(dict(version=label,**result))
            assert cases[0]['rows']==cases[1]['rows'] and cases[0]['opaque_effect_bridges']==cases[1]['opaque_effect_bridges'];structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=cases,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(resources)==10 and len(pictures)==len(short)==1 and len(structural)==2 and len(ends)==10 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0];assert call['descriptor']==[0,14,1,5] and call['layout']==[3,1,1]
    save(ROOT/'seven_exact_leaves632A_picture47xx_two_A000_pairs_and_guarded_end.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all7_source_current_nonspeech_leaves=leaves,
        original632A_word_two_exact_source_sites=[162,182],ten_distinct_632A_decoder_boundary_cases=resources,second_site_reuses_identical_word_and_current_context_not_an_extra_execution_claim=True,
        source_one_picture_pair=pictures,source_one_short47xx_pair=short,source_two_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,
        picture_descriptor14_layout3_1_1_not_assumed_item_name_or_powers=True,two_A000_operands_preserved_without_invented_acquisition_or_event_state_semantics=True,
        short47xx_original_boundary_return_entire_word_argument_bound=True,
        source_owned_adapters=dict(resource632A=resource,picture47xx=pic,end=inspect.getsource(end_case),structural=inspect.getsource(walk)),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_source_scene_effect_bodies_picture_title_and_all19_speeches_pending=True,no_predicate_choice_relative_FE_FI_or2000_pause_inherited=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Seven leaves:10 unique632A boundary cases for two exact-word sites,one4835/one4721 pair,two A000 structural pairs and10 guarded ends. Descriptor14/layout3,1,1;actual semantics pending.')
