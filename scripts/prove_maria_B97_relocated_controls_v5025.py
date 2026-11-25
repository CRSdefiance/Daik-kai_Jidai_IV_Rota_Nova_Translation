"""Bind32 final stored dispatches,one FO and all relocated setup/resource/effect/item leaves."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.research_wedding_command_v676 import walk
from scripts.maria_B97_reference_paths_v5021 import PARENT,ROM,PLAN,DOC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_relocated_controls_v5025')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);source=read(doc['source_context']);dispatch=read(doc['source_dispatch_proof']);control=read(doc['control_contract']);images=[NdsImage.open(p) for p in [PARENT,ROM]];blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[97] for im in images]
    assert images[0].read_file('/__arm9__.bin')==images[1].read_file('/__arm9__.bin') and images[0].read_file('/COMMON/MESFILE.DK4')==images[1].read_file('/COMMON/MESFILE.DK4')
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatch['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](images[1]);assert binding['route']==3 and binding['route_mask']==8
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');calls=[]
    for r in plan['text_records']:
        raw=bytes.fromhex(r['stored_text_hex']);result=ctx.execute(env['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
        assert result['resolved_actor_ID']==(None if raw[0]==254 else raw[0]) and result['registered_catalog_match'] is None
        calls.append(dict(id=r['id'],new_command_offset=r['new_command_offset'],stored_hex=raw.hex(),**result))
    pe=dict(picture_base.__dict__);text=control['source_owned_adapters']['picture4820'];exec(compile(text,__file__+'::picture','exec'),pe);pictures=[]
    for c in plan['mapped_native_commands']:
        if c['word'] not in [0x4820,0x4700]:continue
        command=dict(word=c['word'],offset=c['new_offset'],native_extent=c['new_extent'],whole_command_hex=blocks[1][c['new_offset']:c['new_offset']+c['new_extent']].hex())
        result=ctx.execute(pe['picture'],blocks[1],command);ctx.machines.pop();old=next(r for r in control['picture4820_and_hide4700_four_source_current_cases'] if r['version']=='current' and r['source_offset']==c['old_offset'])
        assert result['original_picture_boundary_calls']==old['original_picture_boundary_calls'] and result['source_command_hex']==old['source_command_hex']
        pictures.append(dict(old_offset=c['old_offset'],new_offset=c['new_offset'],original_current_case_reused=old,target_case=result))
    leaves=[];structural=[]
    for c in plan['mapped_native_commands']:
        if c['word']==0x4000:continue
        a,b=c['old_offset'],c['new_offset'];old,new=blocks[0][a:a+c['old_extent']],blocks[1][b:b+c['new_extent']];assert old==new
        leaves.append(dict(old_offset=a,new_offset=b,word=c['word'],extent=c['old_extent'],hex=old.hex()))
        if c['word'] not in [0x6000,0x4620,0xA000]:continue
        isolated=b'CS\0\1'+struct.pack('<H',len(new))+bytes(2)+new;result=walk(images[1].read_file('/__arm9__.bin'),isolated)
        assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['native_extent']==c['new_extent']
        oldcase=next(r for r in control['setup_and_two_A000_eight_isolated_structural_cases'] if r['source_site']['offset']==a)['versions'][1]
        assert result['rows']==oldcase['rows'] and result['opaque_effect_bridges']==oldcase['opaque_effect_bridges']
        structural.append(dict(old_offset=a,new_offset=b,word=c['word'],result=result,source_current_result_reused=oldcase,nondecode_effect_bodies_unexecuted=True))
    assert len(calls)==32 and len(pictures)==2 and len(leaves)==8 and len(structural)==4 and not ctx.machines
    save(ROOT/'all32_final_dispatches_FO_and_eight_relocated_leaves.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),relocated_dispatch_cases=calls,all8_source_current_target_exact_leaves=leaves,target_item_hide_pairs=pictures,target_setup_and_two_effect_structural_pairs=structural,source633E_ten_cases_reused=control['resource633E_ten_guarded_boundary_cases'],source633E_remains_same_word_at14_and_original_boundary_args=True,one_FE_null_actor_and31_original_progressive_consumers_preserved=True,one_source_FO_default_Li_Clan_preserved=True,all_other_actor_models_PRNG_and4MiB_exact_for_isolated_native_contracts=True,whole_UI_resource_picture_effect_bodies_not_executed_offline=True,actual_source_controls_and_two_page_transition_proved_separately=doc['actual_proof'],current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(doc['source_dispatch_proof']),Path(doc['control_contract']),Path(__file__)]},new_review_credit=0,new_emulator_runs=0,full_goal_complete=False));print('32 final relocated dispatches pass,one FE/FO preserved;all8 leaves and original picture/hide descriptors exact.')
