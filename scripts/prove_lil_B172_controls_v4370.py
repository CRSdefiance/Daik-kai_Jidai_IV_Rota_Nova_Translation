"""Bind B172's11 leaves,three resources,C200,five presentations,later A000 and one end."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_controls_v4370')
SOURCE=Path('work/analysis/lil_B172_source_v4364/all27_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B172_branches_v4367/original_relative_skip_operand_proof.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet,branch=map(read,[SOURCE,BRANCH]);group=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[172] for im in images]
    commands=group['all_current_native_commands']
    assert len(commands)==38 and sum(c['word']==0x4000 for c in commands)==27
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0x2000] for c in commands)
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=172,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['word'],r['source_current_hex']) for r in leaves]==[
        (8,0x6000,'0060'),(10,0x45FF,'ff45ffff0020'),(16,0x6329,'2963'),(18,0x4651,'5146f080'),(22,0x6340,'4063'),
        (1218,0x4620,'20467d80'),(1222,0x632A,'2a63'),(1868,0xC200,'00c2'),(1870,0xA000,'00a0ffff010cc960'),(1878,0x6240,'4062'),(1880,0,'00000000')]
    text=inspect.getsource(resource_base.control630A)
    for old,new in [('previous,boundary_return):','previous,boundary_return,word):'),
        ("value=bytes.fromhex('0a63')","assert word in [0x6329,0x6340,0x632A];value=struct.pack('<H',word)"),
        ('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:
        assert old in text;text=text.replace(old,new)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::three-source-resources','exec'),env)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B172_voices_v4365/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[]
    for word in [0x6329,0x6340,0x632A]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:
                resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)));ctx.machines.pop()
    ui_command=next(c for c in commands if c['word']==0xC200);uis=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        uis.append(dict(version=label,**ctx.execute(C200,block,ui_command)));ctx.machines.pop()
    assert len(resources)==30 and not ctx.machines
    assert uis[0]['source_owned_UI_request_words']==uis[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes']==uis[1]['source_owned_UI_writes']
    structural=[]
    for row in [r for r in leaves if r['word'] in [0x6000,0x45FF,0x4651,0x4620,0x6240,0xA000]]:
        raw=bytes.fromhex(row['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
            assert len(result['rows'])==1 and result['rows'][0]['word']==row['word'] and result['rows'][0]['native_extent']==row['native_extent']
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,
            nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert len(structural)==6
    save(ROOT/'three_resources_C200_five_presentations_later_A000_one_end_and11_source_leaves.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_predicate_cases=[],all11_source_current_nonrelative_nonspeech_leaves=leaves,three_resource_words30_boundary_cases=resources,
        source_C200_pairs=[dict(block=172,source_offset=1868,cases=uis)],
        five_presentation_structural_cases=[r for r in structural if r['source_site']['word']!=0xA000],
        one_later_A000_structural_case=[r for r in structural if r['source_site']['word']==0xA000],
        source_A000_hex='00a0ffff010cc960',source_A000_raw_hex_words=['0C01','60C9'],source_A000_packed_semantics_not_inferred=True,
        source_C2001868_then_A0001870_then6240_1878_then_end1880_preserved=True,
        source_pause_resume_pairs=[],source_declared_end_offsets=[1880],single_tail_end_terminates_linear_source_path=True,
        source_linear_path_command_offsets=[c['offset'] for c in commands],all27_speeches_on_linear_source_path=True,
        no_source_2000_pause_FE_2100_4100_membership_predicate_or_relative_sites=True,
        source_resources_presentations_A000_full_bodies_and_actual_displays_unexecuted_by_these_probes=True,
        source_owned_adapters=dict(three_source_resources=text,C200=inspect.getsource(C200),isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(leaves=11,resource_cases=30,C200_clean_current_pairs=1,presentation_sites=5,later_A000_structural_case=1,
        ends=[1880],actual_scene_unexecuted=True,credit=0))
