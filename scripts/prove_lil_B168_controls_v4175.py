"""Bind three source predicates, four resources, six presentation sites and twelve spans."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_controls_v4175')
SOURCE=Path('work/analysis/lil_B168_source_v4168/all54_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B168_branches_v4172/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,branch=map(read,[SOURCE,BRANCH]);g=packet['blocks'][0]
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[168] for im in images]
    leaves,other,predcommands=[],[],[]
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex']
        r=dict(block=168,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']);leaves.append(r)
        if a['word']==0x8000:predcommands.append(b)
        elif a['word'] not in [0,0xA000] and a['word']&0xFF00!=0x6300:other.append(r)
    assert len(leaves)==16 and len(other)==6 and {r['word'] for r in other}=={0x4301,0x050F,0x4381,0x6005,0x6242,0x0503}
    assert [r['offset'] for r in leaves if r['word']==0]==[2906,2910]
    assert [(r['offset'],r['whole_command_hex']) for r in predcommands]==[(96,'0080ffff06fe0030'),(394,'0080ffff06fe0030'),(1494,'0080ffff14fe0030')]
    assert [r['offset'] for r in leaves if r['word']==0xA000]==[2582]
    words=sorted({r['word'] for r in leaves if r['word']&0xFF00==0x6300});assert words==[0x6300,0x6301,0x630B,0x6342]
    text=inspect.getsource(resource_base.control630A)
    for old,new in [('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:
        assert old in text;text=text.replace(old,new)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,__file__+'::four-source-resources','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B168_voices_v4170/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicates,resources=[],[]
    for c in predcommands:predicates.append(dict(block=168,**ctx.execute(probe,blocks[1],c)));ctx.machines.pop()
    assert predicates[0]['native_result']==predicates[1]['native_result']
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)));ctx.machines.pop()
    assert len(resources)==40 and not ctx.machines
    structural=[]
    for r in other:
        raw=bytes.fromhex(r['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1
            assert result['rows'][0]['word']==r['word'] and result['rows'][0]['native_extent']==r['native_extent']
            versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=r,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==120
    commands={c['offset']:c for c in g['all_clean_native_commands']};byat={r['source_reference']['header_offset']:r for r in packet['records']}
    def path(julio,fernando):
        cursor,last=8,0;visited,spoken,queries=[],[],[]
        while True:
            c=commands[cursor];word=c['word'];visited.append(cursor)
            if word==0:return dict(Julio6_membership_result=julio,Fernando20_membership_result=fernando,native_command_offsets=visited,spoken_source_record_indices=spoken,membership_query_offsets=queries,source_end_offset=cursor,not_actual_UI_or_full_VM_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last]
                assert len(cases)==1;cursor=cases[0]['original_next_command_offset'];continue
            if word==0x8000:queries.append(cursor);last=julio if cursor in [96,394] else fernando
            elif word==0x4000:spoken.append(byat[cursor]['source_record_index'])
            cursor+=c['native_extent']
    paths=[path(j,f) for j in [0,1] for f in [0,1]]
    assert [(p['Julio6_membership_result'],p['Fernando20_membership_result'],len(p['spoken_source_record_indices'])) for p in paths]==[(0,0,51),(0,1,52),(1,0,53),(1,1,54)]
    assert all(p['source_end_offset']==2906 and p['membership_query_offsets']==[96,394,1494] for p in paths)
    save(ROOT/'three_predicates_four_resources_six_presentations_and16_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,two_original_Julio6_queries_one_Fernando20_query=True,complete_source_membership_paths=paths,all16_source_current_nonrelative_nonspeech_nonchoice_leaves=leaves,source_six_presentation_structural_cases=structural,four_resource_words40_boundary_cases=resources,source_owned_resource_adapter=text,source_owned_membership_adapter=inspect.getsource(probe),source_declared_end_offsets=[2906,2910],first_end_terminates_structural_path_second_end_still_owned_and_preserved=True,one_later_A000_at2582_after_touch_protest_yelp_and_sigh_before_FE_help=True,source_three_FE_panels_and_final_Mikhail_work_limitation_follow_effect=True,no_source_C200_C283_2000_4700_2100_or4100_commands=True,source_resource_presentation_and_A000_bodies_full_VM_UI_natural_eligibility_and_actual_displays_unexecuted_by_these_probes=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(predicates=[r['native_result'] for r in predicates],source_relative_cases=120,resources=40,presentation_sites=6,leaves=16,path_speech_counts=[len(p['spoken_source_record_indices']) for p in paths],source_effect_and_actual_display_not_executed=True,credit=0))
