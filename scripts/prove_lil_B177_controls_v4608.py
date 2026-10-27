"""Bind B177's opaque leading A000,C200 ownership and one source endword."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_controls_v4608')
SOURCE=Path('work/analysis/lil_B177_source_v4602/all10_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B177_branches_v4605/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists()
    packet,branch=read(SOURCE),read(BRANCH);group=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[177] for im in images]
    commands=group['all_current_native_commands'];assert len(commands)==13 and sum(c['word']==0x4000 for c in commands)==10
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100,0x4100,0x2000] for c in commands)
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=177,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['source_current_hex']) for r in leaves]==[(8,'00a0ffff01090fa1'),(480,'00c2'),(482,'00000000')]
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B177_voices_v4603/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    ui=next(c for c in commands if c['word']==0xC200);uis=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        uis.append(dict(version=label,**ctx.execute(C200,block,ui)));ctx.machines.pop()
    assert not ctx.machines and uis[0]['source_owned_UI_request_words']==uis[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes']==uis[1]['source_owned_UI_writes']
    raw=bytes.fromhex(leaves[0]['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
    for label,image in zip(['clean','current'],images,strict=True):
        result=walk(image.read_file('/__arm9__.bin'),synthetic)
        assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
        assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
        versions.append(dict(version=label,**result))
    assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
    save(ROOT/'one_A000_C200_single_end_and3_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=[],
        all3_source_current_nonrelative_nonspeech_leaves=leaves,source_C200_pairs=[dict(block=177,source_offset=480,cases=uis)],
        one_A000_structural_cases=[dict(source_site=leaves[0],versions=versions,isolated_offset8_matches_original_cursor=True,
            nondecode_effect_callee_bridged_zero_return_not_body_or_game_state_execution=True)],
        source_A000_hex_by_offset={'8':'00a0ffff01090fa1'},source_A000_packed_operand_semantics_not_inferred=True,
        source_declared_end_offsets=[482],source_pause_resume_pairs=[],source_linear_path_command_offsets=[c['offset'] for c in commands],
        all10_speeches_on_complete_linear_structural_path=True,FE1_impersonal_notice_and_progressive9_dispatches_bound_separately=True,
        no_source_relative_predicate_2000_pause_2100_4100_resources_or_presentation_sites=True,
        source_A000_and_C200_full_bodies_actual_displays_and_earned_fashion_state_unexecuted_by_these_probes=True,
        source_owned_adapters=dict(C200=inspect.getsource(C200),isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(nonrelative_leaves=3,A000_structural_pairs=1,C200_clean_current_pairs=1,FE=1,progressive=9,end=482,actual_scene_unexecuted=True,credit=0))
