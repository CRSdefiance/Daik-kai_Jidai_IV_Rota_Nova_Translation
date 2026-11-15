"""Bind all12 source leaves,two resources,C200,one pause and both consecutive ends."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_controls_v4267')
SOURCE=Path('work/analysis/lil_B170_source_v4260/all33_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B170_branches_v4264/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists()
    packet,branch=read(SOURCE),read(BRANCH)
    group=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[170] for im in images]
    commands=group['all_current_native_commands']
    assert len(commands)==45 and sum(c['word']==0x4000 for c in commands)==33
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100] for c in commands)
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=170,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert len(leaves)==12
    assert [(r['offset'],r['word']) for r in leaves]==[(8,0x6000),(10,0x6342),(12,0x632D),(30,0x4621),(34,0x0505),(36,0x2000),
        (1838,0x050A),(1840,0x6242),(1842,0xA000),(1850,0xC200),(1852,0),(1856,0)]
    assert next(r for r in leaves if r['word']==0xA000)['source_current_hex']=='00a0ffff19100120'
    text=inspect.getsource(resource_base.control630A)
    changes=[('previous,boundary_return):','previous,boundary_return,word):'),
             ("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),
             ('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for old,new in changes:
        assert old in text
        text=text.replace(old,new)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':[0x632D,0x6342]}
    exec(compile(text,__file__+'::two-source-resources','exec'),env)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B170_voices_v4262/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[]
    for word in [0x632D,0x6342]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:
                resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)))
                ctx.machines.pop()
    ui_command=next(c for c in commands if c['word']==0xC200)
    uis=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        uis.append(dict(version=label,**ctx.execute(C200,block,ui_command)))
        ctx.machines.pop()
    assert len(resources)==20 and not ctx.machines
    assert uis[0]['source_owned_UI_request_words']==uis[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes']==uis[1]['source_owned_UI_writes']
    other=[r for r in leaves if r['word'] not in [0,0xA000,0xC200] and r['word']&0xFF00!=0x6300]
    assert len(other)==6
    structural=[]
    for row in other:
        raw=bytes.fromhex(row['source_current_hex'])
        synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
        versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
            assert len(result['rows'])==1 and result['rows'][0]['word']==row['word'] and result['rows'][0]['native_extent']==row['native_extent']
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,
            nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    pause=next(c for c in commands if c['word']==0x2000)
    assert pause['offset']==36 and pause['native_extent']==2 and pause['whole_command_hex']=='0020'
    assert next(c for c in commands if c['offset']==38)['word']==0x4000
    save(ROOT/'two_resources_C200_pause_two_ends_and12_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=[],
        all12_source_current_nonrelative_nonspeech_leaves=leaves,two_resource_words20_boundary_cases=resources,
        source_C200_pairs=[dict(block=170,source_offset=1850,cases=uis)],six_presentation_pause_structural_cases=structural,
        source_pause_resume_pairs=[dict(block=170,source_offset=36,source_resume=38,native_extent=2,source_hex='0020',next_command_word=0x4000,no_duration_unit_inferred=True)],
        source_declared_end_offsets=[1852,1856],first_end_terminates_linear_path_second_end_preserved=True,
        source_linear_path_command_offsets=[c['offset'] for c in commands if c['offset']<=1852],all33_speeches_on_linear_source_path=True,
        A000_source_offset=1842,A000_source_command_hex='00a0ffff19100120',A000_raw_u16_words_hex=['1019','2001'],
        packed_A000_semantics_and_natural_recruitment_not_inferred_from_numeric_words=True,
        no_source_FE_2100_4100_or_membership_predicate_and_no_relative_sites=True,
        source_resources_presentation_pause_A000_full_VM_and_actual_displays_unexecuted_by_these_probes=True,
        source_owned_adapters=dict(source630x=text,C200=inspect.getsource(C200),isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,
        no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(leaves=12,resource_cases=20,C200_clean_current_pairs=1,presentation_pause_sites=6,pause=[36,38],ends=[1852,1856],actual_scene_unexecuted=True,credit=0))
