"""Bind two Cesare queries,two resources and complete original lecture/refusal paths."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_controls_v4125')
SOURCE = Path('work/analysis/lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json')
BRANCH = Path('work/analysis/lil_B167_branches_v4122/original_relative_skip_operand_proof.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    packet,branch=read(SOURCE),read(BRANCH)
    group=packet['blocks'][0]
    image=NdsImage.open(packet['current_ROM'])
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[167]
    leaves=[]
    for source,current in zip(group['all_clean_native_commands'],group['all_current_native_commands'],strict=True):
        if source['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2100]:
            continue
        assert source['whole_command_hex']==current['whole_command_hex']
        leaves.append(dict(block=167,offset=source['offset'],word=source['word'],native_extent=source['native_extent'],
            source_current_hex=source['whole_command_hex']))
    assert [(r['offset'],r['word']) for r in leaves]==[(62,0x6327),(264,0x8000),(430,0),(2008,0x8000),(2170,0x632B),(2172,0)]
    predicate_commands=[c for c in group['all_current_native_commands'] if c['word']==0x8000]
    assert len(predicate_commands)==2 and all(c['whole_command_hex']=='0080ffff0dfe0030' for c in predicate_commands)
    text=inspect.getsource(resource_base.control630A)
    for old,new in [('previous,boundary_return):','previous,boundary_return,word):'),
                    ("value=bytes.fromhex('0a63')","assert word in [0x6327,0x632B];value=struct.pack('<H',word)"),
                    ('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:
        assert old in text
        text=text.replace(old,new)
    env=dict(resource_base.__dict__)
    exec(compile(text,__file__+'::two-original-resources','exec'),env)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B167_voices_v4120/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicates,resources=[],[]
    for command in predicate_commands:
        predicates.append(dict(block=167,**ctx.execute(probe,block,command)))
        ctx.machines.pop()
    assert predicates[0]['native_result']==predicates[1]['native_result']
    for word in [0x6327,0x632B]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:
                resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)))
                ctx.machines.pop()
    assert not ctx.machines
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==120
    commands={c['offset']:c for c in group['all_clean_native_commands']}
    texts={r['source_reference']['header_offset']:r for r in group['records']}
    def path(option,membership):
        cursor,last=8,0
        visited,spoken,queried=[],[],[]
        while True:
            command=commands[cursor]
            word=command['word']
            visited.append(cursor)
            if word==0:
                return dict(option_index=option,Cesare_membership_result=membership,native_command_offsets=visited,
                    spoken_source_record_indices=spoken,membership_query_offsets=queried,source_end_offset=cursor,
                    final_last_result=last,original_selected_resource_words=[commands[a]['word'] for a in visited if commands[a]['word']&0xFF00==0x6300],
                    not_actual_UI_or_full_VM_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last]
                assert len(cases)==1
                cursor=cases[0]['original_next_command_offset']
                continue
            if word==0x4000:
                spoken.append(texts[cursor]['source_record_index'])
            elif word==0x2100:
                assert cursor==152
                last=option
            elif word==0x8000:
                queried.append(cursor)
                last=membership
            else:
                assert word in [0x6327,0x632B]
            cursor+=command['native_extent']
    paths=[path(option,membership) for option in [0,1] for membership in [0,1]]
    assert [(p['option_index'],p['Cesare_membership_result'],p['source_end_offset'],len(p['spoken_source_record_indices'])) for p in paths]==[(0,0,2172,22),(0,1,2172,23),(1,0,430,6),(1,1,430,7)]
    assert all(p['membership_query_offsets']==([2008] if p['option_index']==0 else [264]) for p in paths)
    assert all(p['final_last_result']==p['Cesare_membership_result'] for p in paths)
    assert all((131 in p['spoken_source_record_indices'])==(p['option_index']==0 and p['Cesare_membership_result']==1) for p in paths)
    assert all((45 in p['spoken_source_record_indices'])==(p['option_index']==1 and p['Cesare_membership_result']==1) for p in paths)
    save(ROOT/'two_Cesare_queries_two_resources_four_paths_and6_leaves.json',dict(candidate=packet['current_ROM'],
        candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_predicate_cases=predicates,source_membership_word_selects_Cesare13=True,complete_choice_and_membership_paths=paths,
        option0_accepts_lecture_option1_declines=True,refusal_and_lecture_ends_are_separate=True,
        both_queries_occur_after_menu_and_final_last_result_is_query_result_not_assumed_option=True,
        optional_Cesare_boast_and_realization_belong_to_alternative_paths=True,
        all6_source_current_nonrelative_nonspeech_nonchoice_leaves=leaves,two_resource_words20_boundary_cases=resources,
        source_owned_resource_adapter=text,source_owned_membership_adapter=inspect.getsource(probe),
        source_two_declared_end_offsets=[430,2172],no_source_A000_or_other_presentation_or_C200_C283_2000_FE_4700_4100_commands=True,
        source_resource_bodies_full_VM_UI_natural_source_eligibility_and_actual_displays_unexecuted_by_these_probes=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(unforced_Cesare_results=[p['native_result'] for p in predicates],relative_cases=120,
        paths=[(p['option_index'],p['Cesare_membership_result'],len(p['spoken_source_record_indices']),p['source_end_offset'],p['final_last_result']) for p in paths],credit=0))
