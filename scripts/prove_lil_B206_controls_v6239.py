"""Bind B206's picture,three short controls,three opaque effects and guarded complete end."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_controls_v6239');SOURCE=Path('work/analysis/lil_B206_source_v6232/all28_clean_current_complete_context_with_four_choice_labels.json');INPUT=Path('work/analysis/current_V6220_native_v6228/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[206] for im in images];g=packet['blocks'][0];leaves=[]
    assert len(g['all_current_native_commands'])==42
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word'] not in [0x4000,0x100,0x200,0x300,0x400,0x2100]:assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(88,'35488aa8'),(1106,'3547'),(1108,'00a0ffff01008a30'),(1120,'2047'),(1348,'00a0ffff8a002fa3'),(1364,'2047'),(1506,'00a0ffff8a002aa3'),(1518,'00000000')]
    adapted=checked_text(inspect.getsource(picture),{'[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4835,0x4735,0x4720]','if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':'if word in [0x4700,0x4735,0x4720]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None','(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4735,0x4720] else 4)'})
    env=dict(picture.__globals__);exec(compile(adapted,__file__+'::source4835-4735-4720','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');pictures=[];short=[];structural=[];ends=[]
    for c in leaves:
        word,at=c['word'],c['offset']
        if word in [0x4835,0x4735,0x4720]:
            pair=[]
            for label,b in zip(['clean','current'],blocks,strict=True):pair.append(dict(version=label,**ctx.execute(env['picture'],b,c)));ctx.machines.pop()
            assert pair[0]['original_picture_boundary_calls']==pair[1]['original_picture_boundary_calls'];(pictures if word==0x4835 else short).append(dict(source_offset=at,word=word,cases=pair))
        elif word==0:
            assert at==1518
            for label,im,b in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',b,4)[0];assert len(b)==1524 and logical==1522 and b[logical:]==bytes(2)
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,stored_bytes=1524,logical_end=1522,tailzeros=2,**end_case(im.read_file('/__arm9__.bin'),b,at,previous)))
        else:
            assert word==0xA000;value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
            for label,im in zip(['clean','current'],images,strict=True):
                r=walk(im.read_file('/__arm9__.bin'),isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated) and len(r['rows'])==1 and r['rows'][0]['word']==word and r['rows'][0]['native_extent']==c['native_extent'];pair.append(dict(version=label,**r))
            assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges'];structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=pair,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_full_payment_item_or_transition_execution=True))
    assert len(pictures)==1 and len(short)==3 and len(structural)==3 and len(ends)==10 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0];assert call['descriptor']==[0,138,1,5] and call['layout']==[3,1,1]
    save(ROOT/'eight_exact_leaves_picture138_three47xx_three_A000_and_guarded_end.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all8_source_current_nonrelative_nonchoice_leaves=leaves,source_one_picture_pair=pictures,source_three_short47xx_pairs=short,source_three_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,source_picture_descriptor138_layout3_1_1_independently_bound=True,no_assumed_magic_dance_boost_payment_or_affordability_semantics=True,all_three_short_control_entire_words_original_boundary_and_returns_bound=True,source_owned_adapters=dict(picture47xx=adapted,end=inspect.getsource(end_case),structural=inspect.getsource(walk)),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_source_choices_labels_purchase_refusals_and_effects_pending=True,no_inherited_parrot_letters_resources_or_FE_contracts=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},full_goal_complete=False));print('B206 eight leaves:picture138/layout3,1,1,three47xx pairs,three A000 structural pairs and ten guarded ends. Choice routing and complete effects remain unclaimed.')
