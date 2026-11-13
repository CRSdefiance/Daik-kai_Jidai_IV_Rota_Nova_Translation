"""Bind original B197 control leaves without guessing effect or disappearance semantics."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prove_lil_B196_6003_ends_v5597 import command6003,end_case
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_controls_v5654')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
RESOURCE=Path('work/analysis/lil_B196_controls_v5596/seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[197] for im in images];commands=packet['blocks'][0]['all_current_native_commands']
    resource=read(RESOURCE)['source_owned_adapters']['resource'];env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':[0x632E]}
    exec(compile(resource,__file__+'::source632E','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B197_voices_v5648/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    leaves=[];structural=[];pictures=[];resources=[];special=[];ends=[]
    for c in commands:
        if c['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2200]:continue
        at=c['offset'];raw=bytes.fromhex(c['whole_command_hex'])
        assert all(b[at:at+c['native_extent']]==raw for b in blocks)
        leaves.append(dict(offset=at,word=c['word'],native_extent=c['native_extent'],source_current_hex=raw.hex()))
        if c['word'] in [0xA000,0x4720,0x4735]:
            isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
            for label,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent']
                versions.append(dict(version=label,**result))
            assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
            structural.append(dict(source_offset=at,word=c['word'],source_command_hex=raw.hex(),versions=versions,callee_bodies_bridged_not_full_effect_or_transition_execution=True))
        elif c['word']==0x4821:
            versions=[]
            for label,block in zip(['clean','current'],blocks,strict=True):
                versions.append(dict(version=label,**ctx.execute(picture,block,c)));ctx.machines.pop()
            assert versions[0]['original_picture_boundary_calls']==versions[1]['original_picture_boundary_calls']
            pictures.append(dict(source_offset=at,cases=versions))
        elif c['word']==0x632E:
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,returned,0x632E));ctx.machines.pop()
        elif c['word']==0x6003:
            assert at==832 and raw==bytes.fromhex('0360')
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for returned in [0,0xFFFFFFFF]:special.append(ctx.execute(command6003,previous,returned));ctx.machines.pop()
        elif c['word']==0:
            assert at==874
            for label,image,block in zip(['clean','current'],images,blocks,strict=True):
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**end_case(image.read_file('/__arm9__.bin'),block,at,previous)))
        else:raise AssertionError('Unclassified B197 control leaf')
    assert len(leaves)==11 and len(structural)==7 and len(pictures)==1 and len(resources)==len(special)==len(ends)==10 and not ctx.machines
    descriptor=pictures[0]['cases'][0]['original_picture_boundary_calls'][0]['descriptor'];assert descriptor==[0,140,1,5]
    save(ROOT/'eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all11_source_current_nonrelative_nonspeech_nonchoice_leaves=leaves,source_A000_and47xx_structural_pairs=structural,source_picture_pairs=pictures,source_picture_descriptor=descriptor,
        source632E_boundary_cases=resources,source6003_boundary_cases=special,source_declared_end_cases=ends,
        source_owned_adapters=dict(picture=inspect.getsource(picture),source632E=resource,command6003=inspect.getsource(command6003),end=inspect.getsource(end_case)),
        five_original_effects_and_both_short47xx_controls_preserved_without_body_semantic_claim=True,
        source_picture_descriptor140_not_assumed_book_title_or_item_identity=True,
        source_disappearance_is_dialogue_report_4720_4735_visual_behavior_needs_focused_native_or_actual_proof=True,
        original_money8500_affordability_debit_gift_and_Charm_effect_semantics_still_pending=True,
        source_all39_commands_and_three_option_menu_retained_not_flattened=True,
        current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,RESOURCE,Path(__file__)]},
        actual_B197_source_event_choice_paths_and_state_effects_unexecuted=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B19711 exact leaves;five A000/two47xx structural pairs,one source/current picture pair,10 resource/10 6003/10 end cases pass.Picture140 and short47xx/funds/gift/Charm bodies not semantically certified;no gameplay or credit.')
