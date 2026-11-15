"""Bind eight predicates,two C200s,source resources,pause andall29 exact leaves."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B161_B163_controls_v3918')
SOURCE=Path('work/analysis/lil_B161_B163_source_v3912/all45_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B161_B163_voices_v3914/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])];banks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in images];words=sorted({c['word'] for g in packet['blocks'] for c in g['all_current_native_commands'] if c['word']&0xFF00==0x6300});assert words==[0x6314,0x632C];text=inspect.getsource(resource_base.control630A);changes=[('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,__file__+'::two-source-resource-values','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[];uis=[];resources=[];leaves=[];other=[];pauses=[]
    for g in packet['blocks']:
        n=g['block'];blocks=[bank[n] for bank in banks]
        for c in g['all_current_native_commands']:
            if c['word']==0x8000:r=ctx.execute(probe,blocks[1],c);ctx.machines.pop();predicates.append(dict(block=n,**r))
            elif c['word']==0xC200:
                values=[]
                for version,block in zip(['clean','current'],blocks,strict=True):r=ctx.execute(C200,block,c);ctx.machines.pop();values.append(dict(version=version,**r))
                assert values[0]['source_owned_UI_writes']==values[1]['source_owned_UI_writes'] and values[0]['source_owned_UI_request_words']==values[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=n,source_offset=c['offset'],cases=values))
            if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]:
                assert blocks[0][c['offset']:c['offset']+c['native_extent']]==blocks[1][c['offset']:c['offset']+c['native_extent']];leaf=dict(block=n,offset=c['offset'],word=c['word'],native_extent=c['native_extent'],source_current_hex=c['whole_command_hex'],preserved_by_exact_leaf_ownership_not_full_effect_execution=True);leaves.append(leaf)
                if c['word'] not in [0,0x8000,0xC200,0xA000] and c['word']&0xFF00!=0x6300:other.append(leaf)
                if c['word']==0x2000:
                    following=next(x for x in g['all_current_native_commands'] if x['offset']==c['offset']+c['native_extent']);assert n==163 and c['offset']==198 and c['native_extent']==2 and c['whole_command_hex']=='0020' and following['offset']==200 and following['word']==0x4000;pauses.append(dict(block=n,source_offset=198,source_resume=200,native_extent=2,source_hex='0020',next_command_word=0x4000,no_pause_duration_unit_inferred=True))
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==8 and len(uis)==2 and len(resources)==20 and len(leaves)==29 and len(other)==11 and len(pauses)==1 and not ctx.machines;assert sum(c['word']&0xFF00==0x6300 for c in leaves)==3 and sum(c['word']==0xA000 for c in leaves)==1 and sum(c['word']==0 for c in leaves)==4;unique={c['source_current_hex']:c for c in other};assert len(unique)==9;structural=[]
    for value,c in unique.items():
        raw=bytes.fromhex(value);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(word=c['word'],source_command_hex=value,source_sites=[dict(block=x['block'],offset=x['offset']) for x in other if x['source_current_hex']==value],isolated_synthetic_offset8_not_original_in_block_cursor=True,versions=versions,all_nondecode_callees_explicitly_bridged_with_zero_return=True,not_current_context_body_effect_or_display_execution=True))
    save(ROOT/'eight_predicates_two_C200_two_resource_values_one_pause_and29_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,source_C200_pairs=uis,source630x_resource_words=words,source630x_boundary_cases=resources,all29_nonrelative_source_current_control_leaves=leaves,other11_presentation_sites_nine_isolated_structural_commands=structural,source_pause_resume_pairs=pauses,source_owned_adapters=dict(predicate=inspect.getsource(probe),C200=inspect.getsource(C200),source630x=text,isolated_structural_walk=inspect.getsource(walk)),eight_unforced_Angelo6_Fernando2_membership_sites_not_actual_eligibility=True,four_declared_endwords_across_three_blocks_require_relocation=True,one_later_A000_source_effect_preserved_not_naturally_earned=True,source_C283_4679_4622_4695_45FF_0514_4634_6005_pause_and_normal_returns_need_actual_display_checks=True,no_source_FE_4700_dynamic_2100_or4100_objects=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B161_B163_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(predicates=[r['native_result'] for r in predicates],C200_pairs=2,resource_values=2,resource_sites=3,boundary_cases=20,leaves=29,other_presentation_sites=11,unique_structural_commands=9,pause_bytes=2,actual_display_pending=True,credit=0))
