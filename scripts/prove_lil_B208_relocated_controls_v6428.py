"""Bind all24 stored dispatches,four unchanged opaque effects and complete original/target ends."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.research_wedding_command_v676 import walk
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.create_lil_B208_reference_v6424 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_relocated_controls_v6428');DOC=Path('translations/lil_B208_editorial_manuscript_v6.json');CP=Path('work/analysis/lil_B208_controls_v6396/four_source_current_structural_pairs_and_ten_guarded_complete_end_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,cp=map(read,[DOC,PLAN,CP]);packet=read(doc['source_context']);dp=read(doc['control_contract']);parent,target=[NdsImage.open(p) for p in [PARENT,ROM]];arm=target.read_file('/__arm9__.bin');assert arm==parent.read_file('/__arm9__.bin') and sha(arm)==doc['required_runtime_ARM9_sha256'] and sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']==dp['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[208] for im in [parent,target]];spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256']==packet['blocks'][0]['current_block_sha256'] and sha(new)==spec['research_block_sha256']
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}};adapters=dp['source_owned_adapters'];assert sha(arm) in adapters['bind_current_catalog'] and '123264' in adapters['bind_current_catalog']
    for name,text in adapters.items():exec(compile(text,__file__+'::current-'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](target);ROOT.mkdir(parents=True);ctx=CurrentContext(doc['current_strict_native_input'],'unused-no-historical-RAM',ROOT/'current_context');rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];structural=[];ends=[]
    for ref in spec['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];row=rows[ref['id']];fe=raw[0]==254;assert new[at:at+len(raw)+1]==raw+b'\0';result=ctx.execute(env['dispatch'],raw[0],raw[1:]);ctx.machines.pop();expected,match=env['expanded_current_body'](raw[1:]);assert match is None and expected==raw[1:] and row['source_selector']==raw[0] and result['resolved_actor_ID']==(None if fe else raw[0]) and result['source_voice_class']==(None if fe else {7:3,170:0}[raw[0]]) and result['registered_catalog_match'] is None and result['boundaries'][1]['text_hex']==raw[1:].hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        assert result['boundaries'][1]['kind']==('unexecuted-FE-modal-body' if fe else 'unexecuted-progressive-body') and bool(result['FE_original_null_actor_calls'])==fe
        assert all(bytes.fromhex(row['source_hex'])[1:].count(m)==raw[1:].count(m)==0 for m in [b'FI',b'FA',b'FO']);dispatches.append(dict(id=ref['id'],new_offset=at,stored_target_hex=raw.hex(),**result))
    originals={c['offset']:c for c in cp['all5_source_current_nontext_leaves']};oldcases={c['source_offset']:c for c in cp['source6005_632E_two_A000_structural_pairs']}
    exact=[(1118,'0560'),(1120,'2e63'),(1166,'00a0ffff01020760'),(1174,'00a0ffff28000110'),(1182,'00000000')]
    for ref in spec['command_map']:
        word,a,b=ref['word'],ref['old_offset'],ref['new_offset']
        if word==0x4000:continue
        value=new[b:b+ref['new_extent']];assert value==old[a:a+ref['old_extent']];original=originals[a];assert original['word']==word and original['whole_command_hex']==value.hex();leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=value.hex()))
        if word:
            assert word in [0x6005,0x632E,0xA000];isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;result=walk(arm,isolated);prior=next(c for c in oldcases[a]['cases'] if c['version']=='current');assert result['error'] is None and result['rows']==prior['rows'] and result['opaque_effect_bridges']==prior['opaque_effect_bridges'];structural.append(dict(old_offset=a,new_offset=b,command_hex=value.hex(),current_runtime_isolated_offset8_result=result,nondecode_body_bridged_not_complete_stat_inventory_quest_or_eligibility_effect=True))
        else:
            assert a==1182 and b==1190 and value==bytes(4)
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                logical=8+struct.unpack_from('<H',block,4)[0];assert (len(block),logical,len(block)-logical)==((1188,1186,2) if label=='current' else (1196,1194,2))
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,logical_end=logical,stored_bytes=len(block),**end_case(arm,block,at,previous)))
    assert [(r['old_offset'],r['source_current_target_hex']) for r in leaves]==exact and len(dispatches)==24 and sum(r['source_selector']==254 for r in dispatches)==1 and len(structural)==4 and len(ends)==10 and not ctx.machines
    save(ROOT/'all24_dispatches_four_structural_effects_and10_guarded_ends.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,all5_source_current_target_nontext_leaves=leaves,fresh_current_four_structural_effect_cases=structural,fresh_current_target10_complete_end_cases=ends,all23_progressive_one_FE_private_thought_literal_named_notice_no_macros_menus_or_branches_preserved=True,original_Cristina_Erneco_Mysterious_Old_Man_names_and_unknown_metadata_preserved=True,no_natural_event_or_full_stat_inventory_quest_or_eligibility_claim=True,actual_English_scene_comparison_pending=True,registered_catalog_binding=binding,source_owned_current_catalog_adapter=adapters['bind_current_catalog'],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),historical_source_control_proofs_retained_not_relabelled_as_fresh=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,CP,Path(doc['control_contract']),Path('scripts/current_build_native_context_v6261b.py'),Path(__file__)]}));print('B20824 stored dispatches(23 progressive/one FE),four original structural effects and10 guarded ends pass;English scene next. Full effects/eligibility unclaimed.')
