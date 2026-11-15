"""Bind20 relocated B204 dispatches and all six source-owned control leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.prepare_lil_B204_references_v6135 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_relocated_controls_v6143')
DOC=Path('translations/lil_B204_editorial_manuscript_v7.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=read(DOC),read(PLAN);packet=read(doc['source_context'])
    cp_path=Path('work/analysis/lil_B204_controls_v6139/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json');dp,cp=map(read,[doc['control_contract'],cp_path]);images=[NdsImage.open(p) for p in [PARENT,ROM]]
    arm=images[1].read_file('/__arm9__.bin');assert images[0].read_file('/__arm9__.bin')==arm
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[204] for im in images]
    spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](images[1]);picenv=dict(picture_base.__dict__)
    exec(compile(cp['source_owned_adapters']['picture47xx'],__file__+'::source-picture47xx','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];pictures=[]
    for r in spec['text_records']:
        value=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(value)]==value
        result=ctx.execute(env['dispatch'],value[0],value[1:]);ctx.machines.pop();expected,match=env['expanded_current_body'](value[1:]);assert match is None;expected=expected.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        actor=None if value[0]==254 else rows[r['id']]['source_selector'];assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==expected.hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        assert all(bytes.fromhex(rows[r['id']]['source_hex'])[1:].count(m)==value[1:].count(m) for m in [b'FI',b'FA',b'FO'])
        if actor is None:assert result['FE_original_null_actor_calls']
        dispatches.append(dict(id=r['id'],new_offset=at,stored_target_hex=value.hex(),**result))
    for c in spec['command_map']:
        word=c['word'];a,b=c['old_offset'],c['new_offset']
        if word==0x4000:continue
        raw=new[b:b+c['new_extent']];assert raw==old[a:a+c['old_extent']]
        original=next(v for v in cp['all6_source_current_nonspeech_leaves'] if v['offset']==a);assert original['word']==word and original['whole_command_hex']==raw.hex()
        leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        if word in [0x4835,0x4735]:
            versions=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                command=dict(offset=at,word=word,native_extent=len(raw),whole_command_hex=raw.hex());result=ctx.execute(picenv['picture'],block,command);ctx.machines.pop()
                versions.append(dict(version=label,**result))
            left,right=[v['original_picture_boundary_calls'] for v in versions]
            if word==0x4835:assert left==right
            else:
                assert len(left)==len(right)==1
                assert {k:v for k,v in left[0].items() if k!='args'}=={k:v for k,v in right[0].items() if k!='args'}
                assert left[0]['args'][:3]==right[0]['args'][:3]
                assert left[0]['args'][3]==0x02660000+a and right[0]['args'][3]==0x02660000+b
            pictures.append(dict(word=word,old_offset=a,new_offset=b,cases=versions))
    assert len(dispatches)==20 and sum(r['resolved_actor_ID'] is None for r in dispatches)==4
    assert len(leaves)==6 and len(pictures)==2 and not ctx.machines
    assert sum(r['word']==0xA000 for r in leaves)==1 and sum(r['word']==0 for r in leaves)==1 and not spec['original2000_pause_and_resume_maps']
    assert not any(r['word']==0x2000 for r in leaves)
    assert len(cp['source_one_picture_pair'])==len(cp['source_one_short47xx_pair'])==1 and len(cp['source_two43xx_and_one_A000_structural_pairs'])==3 and len(cp['ten_guarded_complete_end_cases'])==10
    save(ROOT/'all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all6_source_current_target_control_leaves=leaves,picture_and_short47xx_pairs=pictures,
        original_two43xx_one_A000_structural_pairs_and_ten_guarded_ends_reused_by_exact_bytes_and_current_snapshot=True,
        all16_progressive_and_four_FE_objects_preserved=True,no_FI_FA_FO_source_macros=True,
        no_predicates_choices_relative_sites2000_or_C200_inherited=True,picture_descriptor_and_A000_operands_not_promoted_to_complete_effect_semantics=True,
        source_commands_controls_and_single_complete_end_not_omitted=True,actual_English_scene_comparison_pending=True,original_names_and_Jam_progressive_full_signature_distinction_preserved=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(doc['control_contract']),cp_path,Path(__file__)]},
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('20 relocated dispatches,one picture/one47xx pair and6 exact leaves pass;four FE letters,no macros or2000 pause. English scene next.')
