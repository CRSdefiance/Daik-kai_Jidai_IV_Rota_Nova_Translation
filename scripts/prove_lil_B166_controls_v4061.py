"""Bind one Fernando predicate,two resources,eight branches,advice paths and eleven exact leaves."""
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
ROOT=Path('work/analysis/lil_B166_controls_v4061')
SOURCE=Path('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json')
BRANCH=Path('work/analysis/lil_B166_branches_v4058/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);branch=read(BRANCH);images=[NdsImage.open('work/clean.nds'),NdsImage.open(v['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[166] for im in images];g=v['blocks'][0];leaves=[];other=[];predcommands=[]
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
        assert a['whole_command_hex']==b['whole_command_hex'];r=dict(block=166,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']);leaves.append(r)
        if a['word']==0x8000:predcommands.append(b)
        elif a['word'] not in [0,0xA000] and a['word']&0xFF00!=0x6300:other.append(r)
    assert len(leaves)==11 and len(other)==6 and {r['word'] for r in other}=={0x45FF,0x4641,0x4620,0x050A,0x6005}
    assert [r['offset'] for r in leaves if r['word']==0]==[2948]
    assert [(r['offset'],r['word']) for r in leaves if r['word'] in [0xA000,0x632B,0x632C]]==[(954,0x632B),(1532,0x632C),(2940,0xA000)]
    assert len(predcommands)==1 and predcommands[0]['whole_command_hex']=='0080ffff14fe0030'
    text=inspect.getsource(resource_base.control630A)
    for a,b in [('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in [0x632B,0x632C];value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:assert a in text;text=text.replace(a,b)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::two-source-resources','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B166_voices_v4056/current_native_input.json',v['historical_snapshot_ROM'],ROOT/'current_context');resources=[];predicates=[]
    for c in predcommands:predicates.append(dict(block=166,**ctx.execute(probe,blocks[1],c)));ctx.machines.pop()
    for word in [0x632B,0x632C]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(dict(source_word=word,**ctx.execute(env['control630A'],previous,result,word)));ctx.machines.pop()
    assert not ctx.machines;structural=[]
    for r in other:
        raw=bytes.fromhex(r['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==r['word'] and result['rows'][0]['native_extent']==r['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(source_site=r,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==80
    commands={c['offset']:c for c in g['all_clean_native_commands']};byat={r['source_reference']['header_offset']:r for r in v['records']}
    def path(start,stop,last):
        cursor=start;visited=[];spoken=[]
        while cursor<stop:
            c=commands[cursor];visited.append(cursor)
            if c['word'] in [0x100,0x200,0x300,0x400]:
                cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last];assert len(cases)==1;cursor=cases[0]['original_next_command_offset']
            else:assert c['word']==0x4000;spoken.append(byat[cursor]['source_record_index']);cursor+=c['native_extent']
        assert cursor==stop
        return dict(last_result=last,native_command_offsets=visited,spoken_source_record_indices=spoken,resume_source_offset=stop,not_actual_UI_or_full_VM_execution=True)
    optional=[path(1168,1216,result) for result in [0,1]];assert [r['spoken_source_record_indices'] for r in optional]==[[],[87]]
    advice=[path(2180,2938,option) for option in [0,1]];assert [r['spoken_source_record_indices'] for r in advice]==[[149,153,157,161,165,169,172,175],[181]]
    save(ROOT/'Fernando_predicate_two_resources_advice_paths_and11_leaves.json',dict(candidate=v['current_ROM'],candidate_sha256=v['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,original_membership_word_selects_Fernando20=True,optional_Fernando_paths=optional,advice_choice_paths=advice,all11_source_current_nonrelative_nonspeech_nonchoice_leaves=leaves,source_six_presentation_structural_cases=structural,two_resource_words20_boundary_cases=resources,source_owned_resource_adapter=text,source_owned_membership_adapter=inspect.getsource(probe),source_single_declared_end_offset=2948,one_later_recruitment_A000_at2940_after_both_menu_paths_rejoin2938=True,spoken_acceptance_and_full_name_before_advice_menu_do_not_move_effect=True,no_C200_C283_2000_FE_4700_or4100_in_this_scope=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_resource_presentation_and_A000_bodies_full_VM_UI_and_actual_displays_unexecuted_by_these_probes=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(unforced_Fernando_result=[r['native_result'] for r in predicates],relative_cases=80,advice_paths=[r['spoken_source_record_indices'] for r in advice],resource_boundaries=20,leaves=11,presentation_sites=6,credit=0))
