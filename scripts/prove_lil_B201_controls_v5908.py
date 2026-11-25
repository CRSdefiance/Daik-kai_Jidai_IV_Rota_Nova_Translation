"""B201 exact nonrelative leaves; preserve opaque effect/short-control semantics."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B196_6003_ends_v5597 import command6003,end_case
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_controls_v5908')
SOURCE=Path('work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json')
INPUT=Path('work/analysis/lil_B201_voices_v5903/current_native_input.json')
ADAPTER=Path('work/analysis/lil_B200_controls_v5833/twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[201] for im in images]
    adapters=read(ADAPTER)['source_owned_adapters'];resource=adapters['resource'];pic=adapters['picture47xx']
    env=dict(resource_base.__dict__);exec(compile(resource,__file__+'::exact-resource-adapter','exec'),env)
    pe=dict(picture.__globals__);exec(compile(pic,__file__+'::exact-picture-adapter','exec'),pe)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    leaves=[];resources=[];audio=[];pictures=[];structural=[];ends=[]
    group=packet['blocks'][0]
    for a,b in zip(group['all_clean_native_commands'],group['all_current_native_commands'],strict=True):
        assert (a['offset'],a['word'],a['native_extent'])==(b['offset'],b['word'],b['native_extent'])
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
        assert a['whole_command_hex']==b['whole_command_hex'];leaves.append(a);word=a['word'];at=a['offset']
        assert all(block[at:at+a['native_extent']].hex()==a['whole_command_hex'] for block in blocks)
        if word in [0x632E,0x6003]:
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:
                    fn,args=(command6003,[previous,returned]) if word==0x6003 else (env['control630A'],[previous,returned,word])
                    (audio if word==0x6003 else resources).append(dict(source_offset=at,**ctx.execute(fn,*args)));ctx.machines.pop()
        elif word==0x4830:
            cases=[]
            for label,block in zip(['clean','current'],blocks,strict=True):
                cases.append(dict(version=label,**ctx.execute(pe['picture'],block,a)));ctx.machines.pop()
            assert cases[0]['original_picture_boundary_calls']==cases[1]['original_picture_boundary_calls'];pictures.append(dict(source_offset=at,cases=cases))
        elif word==0:
            assert at==1448
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                logical=8+struct.unpack_from('<H',block,4)[0];assert len(block)==logical==1452
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,stored_bytes=len(block),logical_end=logical,tailzeros=0,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:
            assert word in [0xA000,0x4720,0x4721]
            value=bytes.fromhex(a['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;cases=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==word and result['rows'][0]['native_extent']==a['native_extent']
                cases.append(dict(version=label,**result))
            assert cases[0]['rows']==cases[1]['rows'] and cases[0]['opaque_effect_bridges']==cases[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=word,source_hex=value.hex(),cases=cases,
                isolated_offset8_not_original_cursor=True,nondecode_bodies_bridged_not_full_effect_or_transition_execution=True))
    assert len(leaves)==15 and len(resources)==30 and len(audio)==20 and len(pictures)==1 and len(structural)==8 and len(ends)==10 and not ctx.machines
    descriptor=pictures[0]['cases'][0]['original_picture_boundary_calls'][0]['descriptor']
    assert descriptor==[0,75,1,5]
    save(ROOT/'fifteen_exact_leaves_three_resources_two6003_picture_eight_structural_pairs_and_complete_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all15_source_current_nonrelative_nonspeech_nonchoice_leaves=leaves,source632E_thirty_boundary_cases=resources,
        two_source6003_twenty_boundary_cases=audio,source4830_picture_pair=pictures,source_picture_descriptor=descriptor,
        six_A000_and_two_short47xx_structural_pairs=structural,ten_guarded_complete_end_cases=ends,
        source_picture_descriptor75_not_assumed_item_name_or_power=True,
        all_six_A000_original_operands_and_two47xx_words_preserved_without_full_payment_item_stat_or_transition_semantic_claim=True,
        original_2100_four_relative_sites_two_FI_and_three_distinct_FE_not_flattened=True,
        actual_source_scene_both_choices_complete_stat_notices_and_control_transition_observation_pending=True,
        native_adapters=adapters,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,ADAPTER,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20115leaves exact:30resource/20audio boundaries,onepicture pair,eight structuralpairs,ten guardedends. Descriptor75 is not item lore;actual choices/effectsemantics pending.')
