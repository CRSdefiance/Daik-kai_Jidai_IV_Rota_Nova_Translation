"""Bind six exact B204 leaves without guessing transition or acquisition bodies."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_controls_v6139')
SOURCE=Path('work/analysis/lil_B204_current_v6118/all20_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B204_current_v6118/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[204] for im in images];group=packet['blocks'][0];commands=group['all_current_native_commands'];leaves=[]
    assert len(commands)==26 and sum(c['word']==0x4000 for c in commands)==20
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']==0x4000:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(256,'0143'),(258,'8143'),(342,'354874a8'),(694,'3547'),(696,'00a0ffff01007430'),(1308,'00000000')]
    pic=checked_text(inspect.getsource(picture),{
        '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4835,0x4735]',
        'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
        'if word in [0x4700,0x4735]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None',
        '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4735] else 4)'})
    env=dict(picture.__globals__);exec(compile(pic,__file__+'::source4835-and4735','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');pictures=[];short=[];structural=[];ends=[]
    for c in leaves:
        word,at=c['word'],c['offset']
        if word in [0x4835,0x4735]:
            pair=[]
            for label,block in zip(['clean','current'],blocks,strict=True):pair.append(dict(version=label,**ctx.execute(env['picture'],block,c)));ctx.machines.pop()
            assert pair[0]['original_picture_boundary_calls']==pair[1]['original_picture_boundary_calls'];(pictures if word==0x4835 else short).append(dict(source_offset=at,word=word,cases=pair))
        elif word==0:
            assert at==1308
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0];assert len(block)==logical==1312 and not block[logical:]
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,stored_bytes=1312,logical_end=1312,tailzeros=0,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word in [0x4301,0x4381,0xA000];value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1
                assert result['rows'][0]['word']==word and result['rows'][0]['native_extent']==c['native_extent'];pair.append(dict(version=label,**result))
            assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=pair,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(pictures)==len(short)==1 and len(structural)==3 and len(ends)==10 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0];assert call['descriptor']==[0,116,1,5] and call['layout']==[3,1,1]
    save(ROOT/'six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all6_source_current_nonspeech_leaves=leaves,
        source_one_picture_pair=pictures,source_one_short47xx_pair=short,source_two43xx_and_one_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,
        picture_descriptor116_layout3_1_1_not_assumed_item_name_or_powers=True,original4301_4381_and_A000_bytes_preserved_not_full_transition_or_acquisition_body_execution=True,
        short47xx_original_boundary_return_entire_word_argument_bound=True,source_owned_adapters=dict(picture47xx=pic,end=inspect.getsource(end_case),structural=inspect.getsource(walk)),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_source_transitions_item_widget_all20_objects_and_four_FE_letter_consumers_pending=True,no_resource6003_FE_stat_notice_FI_FA_FO_predicate_relative_or_pause_inherited=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B204 six leaves:one4835/one4735 pair,two43xx/one A000 structural pairs,ten guarded ends. Descriptor116/layout3,1,1;actual transitions/letter/widget pending.')
