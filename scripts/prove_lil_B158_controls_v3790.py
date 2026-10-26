"""Bind all B158 source predicates, resource boundaries, two pauses and exact presentation leaves."""
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
ROOT=Path('work/analysis/lil_B158_controls_v3790')
SOURCE=Path('work/analysis/lil_B158_source_v3788/all19_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B158_B160_source_v3786/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[158] for im in images];g=packet['blocks'][0];words=sorted({c['word'] for c in g['all_current_native_commands'] if c['word']&0xFF00==0x6300});assert words==[0x6307,0x6308,0x633A,0x6340];text=inspect.getsource(resource_base.control630A)
    for a,b in [('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]:assert a in text,a;text=text.replace(a,b)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,str(Path(__file__))+'::four-source-resource-values','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[];resources=[];leaves=[];other=[]
    for c in g['all_current_native_commands']:
        if c['word']==0x8000:r=ctx.execute(probe,blocks[1],c);ctx.machines.pop();predicates.append(dict(block=158,**r))
        if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]:
            assert blocks[0][c['offset']:c['offset']+c['native_extent']]==blocks[1][c['offset']:c['offset']+c['native_extent']];leaves.append(dict(block=158,offset=c['offset'],word=c['word'],native_extent=c['native_extent'],source_current_hex=c['whole_command_hex'],preserved_by_exact_leaf_ownership_not_full_effect_execution=True))
            if c['word'] not in [0,0x8000] and c['word']&0xFF00!=0x6300:other.append(c)
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==6 and len(resources)==40 and len(leaves)==22 and len(other)==11 and not ctx.machines;assert sum(c['word']&0xFF00==0x6300 for c in leaves)==4 and not any(c['word'] in [0xA000,0xC200] for c in leaves) and sum(c['word']==0 for c in leaves)==1;unique={c['whole_command_hex']:c for c in other};structural=[];assert len(unique)==9
    for value,c in unique.items():
        raw=bytes.fromhex(value);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for version,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];versions.append(dict(version=version,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];structural.append(dict(word=c['word'],source_command_hex=value,source_offsets=[x['offset'] for x in other if x['whole_command_hex']==value],isolated_synthetic_offset8_not_original_in_block_cursor=True,versions=versions,all_nondecode_callees_explicitly_bridged_with_zero_return=True,not_current_context_body_effect_or_display_execution=True))
    pauses=[c for c in other if c['word']==0x2000];assert [(c['offset'],c['native_extent'],c['whole_command_hex']) for c in pauses]==[(402,2,'0020'),(506,2,'0020')];assert {c['word'] for c in other}>={0x4650,0x4660,0x4670,0x4621,0x050A,0x623A,0x6240}
    save(ROOT/'six_predicates_four_resource_sites_two_pauses_and22_source_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,source_C200_pairs=[],source630x_resource_words=words,source630x_boundary_cases=resources,all22_nonrelative_source_current_control_leaves=leaves,other11_presentation_sites_isolated_structural_boundaries=structural,source_owned_adapters=dict(predicate=inspect.getsource(probe),source630x=text,isolated_structural_walk=inspect.getsource(walk)),six_unforced_membership_sites_Camille5_Emilio1_not_actual_eligibility=True,one_declared_endword_must_survive_relocation=True,source_pause_resume_pairs=[dict(pause=402,resume=404,bytes=2),dict(pause=506,resume=508,bytes=2)],source_4650_4660_4670_picture_music_applause_pause_resource_bodies_or_actual_effects_not_claimed=True,source_four_FE_patron_and_applause_panels_need_distinct_complete_native_and_actual_geometry_proof=True,no_source_A000_C200_4700_dynamic_2100_or4100_objects=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B158_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(predicates=[r['native_result'] for r in predicates],resource_values=4,resource_sites=4,boundary_cases=40,leaves=22,other_presentation_sites=11,unique_structural_commands=9,pause_pairs=2,FE_native_actual_pending=True,credit=0))
