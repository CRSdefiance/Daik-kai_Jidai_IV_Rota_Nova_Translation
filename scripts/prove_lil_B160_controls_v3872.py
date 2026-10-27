"""Bind B160 predicates,C283/C200 requests,resource boundaries andall exact control leaves."""
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
ROOT=Path('work/analysis/lil_B160_controls_v3872')
SOURCE=Path('work/analysis/lil_B160_source_v3870/all22_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B160_source_v3868/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[160] for im in images];g=packet['blocks'][0];words=sorted({c['word'] for c in g['all_current_native_commands'] if c['word']&0xFF00==0x6300});assert words==[0x632A,0x632B,0x632C];text=inspect.getsource(resource_base.control630A);changes=[('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,str(Path(__file__))+'::three-source-resource-values','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[];uis=[];resources=[];leaves=[];other=[]
    for c in g['all_current_native_commands']:
        if c['word']==0x8000:r=ctx.execute(probe,blocks[1],c);ctx.machines.pop();predicates.append(dict(block=160,**r))
        elif c['word']==0xC200:
            values=[]
            for version,block in zip(['clean','current'],blocks,strict=True):r=ctx.execute(C200,block,c);ctx.machines.pop();values.append(dict(version=version,**r))
            assert values[0]['source_owned_UI_writes']==values[1]['source_owned_UI_writes'] and values[0]['source_owned_UI_request_words']==values[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=160,source_offset=c['offset'],cases=values))
        if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]:
            assert blocks[0][c['offset']:c['offset']+c['native_extent']]==blocks[1][c['offset']:c['offset']+c['native_extent']];leaves.append(dict(block=160,offset=c['offset'],word=c['word'],native_extent=c['native_extent'],source_current_hex=c['whole_command_hex'],preserved_by_exact_leaf_ownership_not_full_effect_execution=True))
            if c['word'] not in [0,0x8000,0xC200,0xA000] and c['word']&0xFF00!=0x6300:other.append(c)
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==5 and len(uis)==1 and len(resources)==30 and len(leaves)==12 and len(other)==1 and not ctx.machines;assert sum(c['word']&0xFF00==0x6300 for c in leaves)==3 and sum(c['word']==0xA000 for c in leaves)==0 and sum(c['word']==0 for c in leaves)==2;unique={c['whole_command_hex']:c for c in other};structural=[];assert len(unique)==1
    for value,c in unique.items():
        raw=bytes.fromhex(value);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(word=c['word'],source_command_hex=value,source_offsets=[x['offset'] for x in other if x['whole_command_hex']==value],isolated_synthetic_offset8_not_original_in_block_cursor=True,versions=versions,all_nondecode_callees_explicitly_bridged_with_zero_return=True,not_current_context_body_effect_or_display_execution=True))
    assert not any(c['word']==0x2000 for c in other);assert len(other)==1 and other[0]['word']==0xC283 and other[0]['offset']==278 and other[0]['native_extent']==2 and other[0]['whole_command_hex']=='83c2'
    save(ROOT/'five_predicates_C283_C200_three_resource_sites_and12_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,source_C200_pairs=uis,source630x_resource_words=words,source630x_boundary_cases=resources,all12_nonrelative_source_current_control_leaves=leaves,one_C283_presentation_site_isolated_structural_boundary=structural,source_owned_adapters=dict(predicate=inspect.getsource(probe),C200=inspect.getsource(C200),source630x=text,isolated_structural_walk=inspect.getsource(walk)),five_unforced_Angelo4_Emilio1_membership_sites_not_actual_eligibility=True,two_declared_endwords_must_survive_relocation=True,no_source2000_pause_object=True,source_C283_C200_and_resource_bodies_or_actual_transitions_not_claimed=True,source_C283_needs_focused_actual_port_transition_checks=True,source_all22_progressive_six_actors_need_complete_native_and_actual_display_proof=True,no_source_A000_FE_2000_4700_dynamic_2100_or4100_objects=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B160_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(predicates=[r['native_result'] for r in predicates],C200_pairs=1,resource_values=3,resource_sites=3,boundary_cases=30,leaves=12,other_presentation_sites=1,unique_structural_commands=1,pause_bytes=0,C283_body_actual_pending=True,credit=0))
