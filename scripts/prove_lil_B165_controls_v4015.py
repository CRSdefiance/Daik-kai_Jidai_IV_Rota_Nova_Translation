"""Bind five Camille membership queries,solo/present alternatives,resource6329 and12 exact leaves."""
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
ROOT=Path('work/analysis/lil_B165_controls_v4015')
SOURCE=Path('work/analysis/lil_B165_source_v4008/all24_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B165_branches_v4013/original_relative_skip_operand_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);branch=read(BRANCH);images=[NdsImage.open('work/clean.nds'),NdsImage.open(v['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[165] for im in images];g=v['blocks'][0];leaves=[];other=[];predcommands=[]
    for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex'];r=dict(block=165,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']);leaves.append(r)
        if a['word']==0x8000:predcommands.append(b)
        elif a['word'] not in [0,0xA000] and a['word']&0xFF00!=0x6300:other.append(r)
    assert len(leaves)==12 and len(other)==4 and {r['word'] for r in other}=={0x45FF,0x4631,0x4620,0x6005};assert [r['offset'] for r in leaves if r['word']==0]==[1540] and [(r['offset'],r['word']) for r in leaves if r['word'] in [0xA000,0x6329]]==[(150,0x6329),(1532,0xA000)];assert len(predcommands)==5 and all(c['whole_command_hex']=='0080ffff09fe0030' for c in predcommands);text=inspect.getsource(resource_base.control630A)
    for a,b in [('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word==0x6329;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:assert a in text;text=text.replace(a,b)
    env=dict(resource_base.__dict__);exec(compile(text,__file__+'::source-resource6329','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B165_voices_v4011/current_native_input.json',v['historical_snapshot_ROM'],ROOT/'current_context');resources=[];predicates=[]
    for c in predcommands:predicates.append(dict(block=165,**ctx.execute(probe,blocks[1],c)));ctx.machines.pop()
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,0x6329));ctx.machines.pop()
    assert not ctx.machines;structural=[]
    for r in other:
        raw=bytes.fromhex(r['source_current_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==r['word'] and result['rows'][0]['native_extent']==r['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(source_site=r,versions=versions,isolated_synthetic_offset8_not_original_cursor=True,nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==200;commands={c['offset']:c for c in g['all_clean_native_commands']};byat={r['source_reference']['header_offset']:r for r in v['records']};alternatives=[]
    for membership in [0,1]:
        cursor=160;visited=[];spoken=[]
        while cursor<450:
            c=commands[cursor];visited.append(cursor)
            if c['word'] in [0x100,0x200,0x300,0x400]:cases=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==membership];assert len(cases)==1;cursor=cases[0]['original_next_command_offset']
            else:assert c['word']==0x4000;spoken.append(byat[cursor]['source_record_index']);cursor+=c['native_extent']
        assert cursor==450 and spoken==([20] if membership==0 else [25,29,33]);alternatives.append(dict(Camille_membership_result=membership,native_command_offsets=visited,spoken_source_record_indices=spoken,resume_source_offset=450,not_actual_source_eligibility_or_full_VM_execution=True))
    save(ROOT/'five_Camille_queries_solo_present_alternatives_resource_and12_leaves.json',dict(candidate=v['current_ROM'],candidate_sha256=v['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,all_five_original_membership_words_select_Camille9=True,first_solo_vs_Camille_exchange_alternatives=alternatives,all12_source_current_nonrelative_nonspeech_leaves=leaves,source_four_presentation_structural_cases=structural,resource6329_boundary_cases=resources,source_owned_resource_adapter=text,source_owned_membership_adapter=inspect.getsource(probe),source_single_declared_end_offset=1540,one_later_recruitment_A000_at1532_preserved=True,no_C200_C283_2000_FE_4700_2100_or4100_in_this_scope=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_resource_body_A000_effects_full_VM_and_actual_displays_unexecuted_by_these_probes=True,source_claims_and_character_opinions_do_not_establish_kinship_rank_retirement_or_medical_condition=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,source_prose_orcompletion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False));print(dict(five_unforced_Camille_results=[r['native_result'] for r in predicates],relative_cases=200,first_alternatives=[[20],[25,29,33]],resource_boundaries=10,leaves=12,presentation_commands=4,credit=0))
