"""Separate original typed menu, four branch controls and nine opaque leaves."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B164_controls_v3968')
SOURCE=Path('work/analysis/lil_B164_source_v3960/all49_clean_current_complete_context_with_typed_choice.json')
BRANCH=Path('work/analysis/lil_B164_branches_v3965/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);branch=read(BRANCH);images=[NdsImage.open('work/clean.nds'),NdsImage.open(v['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[164] for im in images];g=v['blocks'][0];leaves=[];other=[]
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
        assert a['whole_command_hex']==b['whole_command_hex'];r=dict(block=164,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']);leaves.append(r)
        if a['word'] not in [0,0xA000] and a['word']&0xFF00!=0x6300:other.append(r)
    assert len(leaves)==9 and len(other)==5 and {r['word'] for r in other}=={0x45FF,0x4694,0x4620,0x6005,0x610B};assert [r['offset'] for r in leaves if r['word']==0]==[1854,3454];assert [(r['offset'],r['word']) for r in leaves if r['word'] in [0xA000,0x632B]]==[(1554,0xA000),(3452,0x632B)]
    text=inspect.getsource(resource_base.control630A)
    for a,b in [('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word==0x632B;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:assert a in text;text=text.replace(a,b)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::source-resource632B','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B164_voices_v3963/current_native_input.json',v['historical_snapshot_ROM'],ROOT/'current_context');resources=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,0x632B));ctx.machines.pop()
    assert not ctx.machines;structural=[]
    for r in other:
        raw=bytes.fromhex(r['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==r['word'] and result['rows'][0]['native_extent']==r['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(source_site=r,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==40;choice_paths=[]
    for option in [0,1]:
        cursor=1676;visited=[]
        while cursor<1862:
            visited.append(cursor)
            if cursor==1688:break
            cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==option];assert len(cases)==1;cursor=cases[0]['original_next_command_offset']
        assert cursor==[1862,1688][option];choice_paths.append(dict(option_index=option,source_Japanese=['聞く','聞かない'][option],native_relative_cursor_trace=visited,destination=cursor,spoken_source_records=([136,140,143,147,150,153,156,159,163,166,169,173,177,180,183,186] if option==0 else [121,125]),separated_end_offset=[3454,1854][option],recruitment_precedes_both_options=True,not_actual_UI_selection_or_full_VM_execution=True))
    save(ROOT/'four_branches_typed_advice_outcomes_resource_and9_leaves.json',dict(candidate=v['current_ROM'],candidate_sha256=v['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_current_opaque_nonrelative_nonchoice_leaves=leaves,source_presentation_structural_cases=structural,resource632B_boundary_cases=resources,source_owned_resource_adapter=text,source_choice_outcome_paths=choice_paths,original_choice_getters_reused_from_source_packet=True,two_separated_declared_endwords=[1854,3454],one_A000_at1554_before_advice_choice1654=True,no_predicates_C200_C283_2000_FE_4700_or4100_in_this_scope=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_resource_body_A000_effects_full_VM_UI_choices_and_actual_displays_unexecuted=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,source_prose_orcompletion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False));print('9 opaque leaves,5 presentation commands,10 resource boundaries and both native advice-choice paths pass;actual UI pending.')
