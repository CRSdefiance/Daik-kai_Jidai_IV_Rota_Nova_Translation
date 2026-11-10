"""Bind eight exact B205 leaves without inventing capture,resource or stat-effect semantics."""
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
ROOT=Path('work/analysis/lil_B205_controls_v6179');SOURCE=Path('work/analysis/lil_B205_source_v6172/all17_clean_current_complete_context.json');INPUT=Path('work/analysis/current_V6160_native_v6168/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[205] for im in images];g=packet['blocks'][0];leaves=[]
    assert len(g['all_current_native_commands'])==25
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if b['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(b)
    assert [(c['offset'],c['whole_command_hex']) for c in leaves]==[(32,'414893a8'),(346,'0c63'),(348,'2d63'),(590,'00a0ffff010d0260'),(598,'2147'),(600,'00a0ffff010d0f60'),(608,'00a0ffff01009330'),(616,'00000000')]
    adapted=checked_text(inspect.getsource(picture),{'[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4841,0x4721]','if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':'if word in [0x4700,0x4721]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;assert word==0x4700 or args[1]==word;desc=None;layout=None','(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4721] else 4)'})
    env=dict(picture.__globals__);exec(compile(adapted,__file__+'::source4841-4721','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');pictures=[];short=[];structural=[];ends=[]
    for c in leaves:
        word,at=c['word'],c['offset']
        if word in [0x4841,0x4721]:
            pair=[]
            for label,b in zip(['clean','current'],blocks,strict=True):pair.append(dict(version=label,**ctx.execute(env['picture'],b,c)));ctx.machines.pop()
            assert pair[0]['original_picture_boundary_calls']==pair[1]['original_picture_boundary_calls'];(pictures if word==0x4841 else short).append(dict(source_offset=at,word=word,cases=pair))
        elif word==0:
            assert at==616
            for label,im,b in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',b,4)[0];assert len(b)==logical==620 and not b[logical:]
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,stored_bytes=620,logical_end=620,tailzeros=0,**end_case(im.read_file('/__arm9__.bin'),b,at,previous)))
        else:
            assert word in [0x630C,0x632D,0xA000];value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
            for label,im in zip(['clean','current'],images,strict=True):
                r=walk(im.read_file('/__arm9__.bin'),isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated) and len(r['rows'])==1 and r['rows'][0]['word']==word and r['rows'][0]['native_extent']==c['native_extent'];pair.append(dict(version=label,**r))
            assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges'];structural.append(dict(source_offset=at,word=word,source_command_hex=value.hex(),cases=pair,isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_scene_execution=True))
    assert len(pictures)==len(short)==1 and len(structural)==5 and len(ends)==10 and not ctx.machines
    call=pictures[0]['cases'][0]['original_picture_boundary_calls'][0];assert call['descriptor']==[0,147,1,5] and call['layout']==[4,0,1]
    save(ROOT/'eight_exact_leaves_picture147_47xx_two63xx_three_A000_and_guarded_end.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all8_source_current_nonspeech_leaves=leaves,source_one_picture_pair=pictures,source_one_short47xx_pair=short,source_two63xx_three_A000_structural_pairs=structural,ten_guarded_complete_end_cases=ends,picture_descriptor147_layout4_0_1_not_assumed_item_title_or_species=True,original630C_632D_three_A000_bytes_preserved_not_full_resource_or_effect_body_execution=True,short47xx_original_boundary_return_entire_word_argument_bound=True,source_owned_adapters=dict(picture47xx=adapted,end=inspect.getsource(end_case),structural=inspect.getsource(walk)),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_source_staging_all17_objects_parrot_capture_item_and_effects_pending=True,no_B204_castle_letter_43xx_or_one_A000_contract_inherited=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},full_goal_complete=False));print('B205 eight leaves:picture147/layout4,0,1,4721,two63xx/three A000 structural pairs,ten guarded ends. Actual staging and complete effects unclaimed.')
