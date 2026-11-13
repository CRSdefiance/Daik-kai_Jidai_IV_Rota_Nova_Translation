"""Bind B173's predicate,relative suffix,resources and opaque effect bytes."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B173_controls_v4417')
SOURCE=Path('work/analysis/lil_B173_source_v4411/all11_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B173_branches_v4414/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists()
    packet,branch=map(read,[SOURCE,BRANCH]);group=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[173] for im in images]
    commands=group['all_current_native_commands']
    assert len(commands)==23 and sum(c['word']==0x4000 for c in commands)==11
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes())
    assert len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=173,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['source_current_hex']) for r in leaves]==[
        (8,'0060'),(10,'2963'),(12,'4063'),(720,'00a0ffff010b39a2'),(728,'0080ffff000cca70'),
        (748,'00a0ffff010cca60'),(760,'4062'),(762,'00000000')]
    text=inspect.getsource(resource_base.control630A)
    for old,new in [('previous,boundary_return):','previous,boundary_return,word):'),
        ("value=bytes.fromhex('0a63')","assert word in [0x6329,0x6340];value=struct.pack('<H',word)"),
        ('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:
        assert old in text;text=text.replace(old,new)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::two-source-resources','exec'),env)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B173_voices_v4412/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    resources=[]
    for word in [0x6329,0x6340]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:
                resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)));ctx.machines.pop()
    predicate=next(c for c in commands if c['word']==0x8000)
    assert predicate['offset']==728 and predicate['whole_command_hex']=='0080ffff000cca70'
    predicates=[]
    for version,block in zip(['clean','current'],blocks,strict=True):
        predicates.append(dict(version=version,block=173,**ctx.execute(probe,block,predicate)));ctx.machines.pop()
    assert predicates[0]['native_result']==predicates[1]['native_result']
    assert predicates[0]['native_result'][0]==2 and predicates[0]['native_result'][1] in [0,1]
    assert len(resources)==20 and not ctx.machines
    structural=[]
    for row in [r for r in leaves if r['word'] in [0x6000,0x6240,0xA000]]:
        raw=bytes.fromhex(row['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic)
            assert len(result['rows'])==1 and result['rows'][0]['word']==row['word'] and result['rows'][0]['native_extent']==row['native_extent']
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,
            nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert len(structural)==4
    by_at={c['offset']:c for c in commands};speech={r['source_reference']['header_offset']:r for r in packet['records']}
    def path(result):
        cursor,last=8,0;visited=[];spoken=[];effects=[]
        while True:
            command=by_at[cursor];word=command['word'];visited.append(cursor)
            if word==0:return dict(predicate_result=result,native_command_offsets=visited,spoken_source_record_indices=spoken,
                original_A000_offsets=effects,source_end_offset=cursor,not_actual_full_VM_or_effect_body_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                cases=[c for c in branch['cases'] if c['version']=='current' and c['offset']==cursor and c['last_choice_or_result']==last]
                assert len(cases)==1;cursor=cases[0]['original_next_command_offset'];continue
            if word==0x8000:last=result
            elif word==0x4000:spoken.append(speech[cursor]['source_record_index'])
            elif word==0xA000:effects.append(cursor)
            cursor+=command['native_extent']
    paths=[path(value) for value in [0,1]]
    expected=[r['source_record_index'] for r in packet['records']]
    assert all(p['spoken_source_record_indices']==expected and p['source_end_offset']==762 for p in paths)
    assert [p['original_A000_offsets'] for p in paths]==[[720],[720,748]]
    save(ROOT/'two_resources_one_predicate_four_spans_two_A000s_and_single_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_predicate_cases=predicates,source_predicate_hex='0080ffff000cca70',source_predicate_raw_hex_words=['0C00','70CA'],
        no_predicate_or_event_state_forced=True,unforced_historical_predicate_result=predicates[0]['native_result'][1],
        source_predicate_semantics_not_assumed_from_packed_words=True,
        all8_source_current_nonrelative_nonspeech_leaves=leaves,two_resource_words20_boundary_cases=resources,
        two_presentation_structural_cases=[r for r in structural if r['source_site']['word']!=0xA000],
        two_A000_structural_cases=[r for r in structural if r['source_site']['word']==0xA000],
        source_A000_hex_by_offset={'720':'00a0ffff010b39a2','748':'00a0ffff010cca60'},
        source_A000_raw_hex_words_by_offset={'720':['0B01','A239'],'748':['0C01','60CA']},
        source_A000_packed_semantics_not_inferred=True,source_C200_pairs=[],source_pause_resume_pairs=[],
        source_declared_end_offsets=[762],four_source_relative_sites40_clean_current_cases=branch['cases'],complete_two_boolean_suffix_paths=paths,
        all11_speeches_precede_first_A000_and_predicate=True,second_A000_only_on_predicate1_structural_path=True,
        no_source_2000_pause_FE_2100_4100_or_C200=True,
        source_resources_presentations_A000_full_bodies_and_actual_displays_unexecuted_by_these_probes=True,
        source_owned_adapters=dict(two_source_resources=text,predicate=inspect.getsource(probe),isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(nonrelative_leaves=8,resource_cases=20,predicate_clean_current_results=[p['native_result'] for p in predicates],
        relative_sites=4,relative_cases=40,structural_paths=2,presentation_sites=2,A000_structural_cases=2,end=762,actual_scene_unexecuted=True,credit=0))
