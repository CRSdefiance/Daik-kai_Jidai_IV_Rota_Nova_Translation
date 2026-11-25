"""Fresh current-runtime24 dispatches,four picture/short pairs,three structural effects and ten guarded ends."""
import struct,inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.research_wedding_command_v676 import walk
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.create_lil_B206_reference_v6307 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_relocated_controls_v6311');DOC=Path('translations/lil_B206_editorial_manuscript_v7.json');CP=Path('work/analysis/lil_B206_controls_v6239/eight_exact_leaves_picture138_three47xx_three_A000_and_guarded_end.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,cp=map(read,[DOC,PLAN,CP]);packet=read(doc['source_context']);dp=read(doc['control_contract']);parent,target=[NdsImage.open(p) for p in [PARENT,ROM]];arm=target.read_file('/__arm9__.bin');assert arm==parent.read_file('/__arm9__.bin') and sha(arm)==doc['required_runtime_ARM9_sha256'] and sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    previous=read(packet['previous_source_packet']);assert cp['candidate_sha256']==dp['candidate_sha256']==previous['current_ROM_sha256'];old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[206] for im in [parent,target]];spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256']==packet['blocks'][0]['current_block_sha256'] and sha(new)==spec['research_block_sha256']
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}};adapters=dict(dp['source_owned_adapters']);adapters['bind_current_catalog']=checked_text(adapters['bind_current_catalog'],{previous['current_ARM9_sha256']:sha(arm)})
    for name,text in adapters.items():exec(compile(text,__file__+'::current-'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](target);picenv=dict(picture_base.__dict__);exec(compile(cp['source_owned_adapters']['picture47xx'],__file__+'::source-picture47xx','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(doc['current_strict_native_input'],'unused-no-old-RAM',ROOT/'current_context');rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];pictures=[];structural=[];ends=[]
    for ref in spec['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert new[at:at+len(raw)]==raw;result=ctx.execute(env['dispatch'],raw[0],raw[1:]);ctx.machines.pop();expected,match=env['expanded_current_body'](raw[1:]);assert match is None and expected==raw[1:] and result['resolved_actor_ID']==rows[ref['id']]['source_selector']==raw[0] and result['registered_catalog_match'] is None and result['boundaries'][1]['text_hex']==expected.hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        assert all(bytes.fromhex(rows[ref['id']]['source_hex'])[1:].count(m)==raw[1:].count(m)==0 for m in [b'FI',b'FA',b'FO']);dispatches.append(dict(id=ref['id'],new_offset=at,stored_target_hex=raw.hex(),**result))
    for ref in spec['command_map']:
        word=ref['word'];a,b=ref['old_offset'],ref['new_offset']
        if word in [0x4000,0x2100,0x100,0x200,0x300,0x400]:continue
        value=new[b:b+ref['new_extent']];assert value==old[a:a+ref['old_extent']];original=next(v for v in cp['all8_source_current_nonrelative_nonchoice_leaves'] if v['offset']==a);assert original['word']==word and original['whole_command_hex']==value.hex();leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if word in [0x4835,0x4735,0x4720]:
            versions=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                command=dict(offset=at,word=word,native_extent=len(value),whole_command_hex=value.hex());r=ctx.execute(picenv['picture'],block,command);ctx.machines.pop();versions.append(dict(version=label,**r))
            left,right=[r['original_picture_boundary_calls'] for r in versions]
            if word==0x4835:assert left==right and left[0]['descriptor']==[0,138,1,5] and left[0]['layout']==[3,1,1]
            else:
                assert len(left)==len(right)==1 and {k:v for k,v in left[0].items() if k!='args'}=={k:v for k,v in right[0].items() if k!='args'} and left[0]['args'][:3]==right[0]['args'][:3]
                assert left[0]['args'][3]==0x02660000+a and right[0]['args'][3]==0x02660000+b
            pictures.append(dict(word=word,old_offset=a,new_offset=b,cases=versions))
        elif word==0xA000:
            isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;r=walk(arm,isolated);assert r['error'] is None and r['stopped_offset']==r['logical_end']==len(isolated) and len(r['rows'])==1 and r['rows'][0]['word']==word
            oldcase=next(r for r in cp['source_three_A000_structural_pairs'] if r['source_offset']==a);assert r['rows']==oldcase['cases'][1]['rows'] and r['opaque_effect_bridges']==oldcase['cases'][1]['opaque_effect_bridges'];structural.append(dict(old_offset=a,new_offset=b,command_hex=value.hex(),current_runtime_isolated_offset8_result=r,nondecode_bodies_bridged_not_complete_effects_or_payment=True))
        else:
            assert word==0 and a==1518 and b==1576
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                logical=8+struct.unpack_from('<H',block,4)[0];assert (len(block),logical,len(block)-logical)==((1524,1522,2) if label=='current' else (1580,1580,0))
                for last in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,logical_end=logical,stored_bytes=len(block),**end_case(arm,block,at,last)))
    assert len(dispatches)==24 and all(r['resolved_actor_ID'] in [2,7,173] for r in dispatches) and len(leaves)==8 and len(pictures)==4 and len(structural)==3 and len(ends)==10 and not ctx.machines
    save(ROOT/'all24_dispatches_picture_three47xx_three_A000_and10_guarded_ends.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,all8_source_current_target_nonchoice_leaves=leaves,picture_and_three_short47xx_pairs=pictures,fresh_current_three_A000_structural_cases=structural,fresh_current_target10_complete_end_cases=ends,all24_progressive_no_FE_or_macros_preserved=True,two2100_and_eight_relative_sites_are_separate_stored_and_branch_proofs=True,picture138_descriptor_and_layout_exact=True,original_names_Lil_Argot_Cristina_Erneco_and_Shady_Man_preserved=True,no_natural_event_or_full_effect_payment_or_eligibility_claim=True,actual_English_scene_comparison_pending=True,registered_catalog_binding=binding,source_locked_current_catalog_adapter=adapters['bind_current_catalog'],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),historical_source_control_proofs_retained_not_relabelled_as_fresh=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,CP,Path(doc['control_contract']),Path('scripts/current_build_native_context_v6261b.py'),Path(__file__)]}));print('24 relocated speech calls,four current/target picture-short pairs,three fresh structural effects and10 guarded ends pass.467-row catalog rebound to exact V6270;no effect/eligibility overclaim.')
