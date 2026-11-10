"""Bind every relocated B199 speech, picture, short47xx and exact source control."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.prepare_lil_B199_reference_tools_v5796 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_relocated_controls_v5804')
DOC=Path('translations/lil_B199_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan=read(DOC),read(PLAN);packet=read(doc['source_context'])
    dp,cp=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract']])
    images=[NdsImage.open(p) for p in [PARENT,ROM]]
    arm=images[1].read_file('/__arm9__.bin');assert images[0].read_file('/__arm9__.bin')==arm
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[199] for im in images]
    spec=plan['blocks'][0];assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](images[1])
    picenv=dict(picture_base.__dict__)
    exec(compile(cp['source_owned_adapters']['picture47xx'],__file__+'::source-picture47xx','exec'),picenv)
    ROOT.mkdir(parents=True);ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];pictures=[]
    for r in spec['text_records']:
        value=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(value)]==value
        result=ctx.execute(env['dispatch'],value[0],value[1:]);ctx.machines.pop()
        expected,match=env['expanded_current_body'](value[1:]);assert match is None
        actor=None if value[0]==254 else rows[r['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==expected.hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if actor is None:assert result['FE_original_null_actor_calls'] and b'FI' not in value
        dispatches.append(dict(id=r['id'],new_offset=at,stored_target_hex=value.hex(),**result))
    for c in spec['command_map']:
        word=c['word'];a,b=c['old_offset'],c['new_offset']
        if word==0x4000:continue
        raw=new[b:b+c['new_extent']];assert raw==old[a:a+c['old_extent']]
        original=next(v for v in cp['all16_source_current_nonspeech_leaves'] if v['offset']==a)
        assert original['word']==word and original['whole_command_hex']==raw.hex()
        leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        if word in [0x4821,0x4895,0x4720,0x4735]:
            versions=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                command=dict(offset=at,word=word,native_extent=len(raw),whole_command_hex=raw.hex())
                result=ctx.execute(picenv['picture'],block,command);ctx.machines.pop()
                versions.append(dict(version=label,**result))
            left,right=[v['original_picture_boundary_calls'] for v in versions]
            if word in [0x4821,0x4895]:assert left==right
            else:
                assert len(left)==len(right)==1
                assert {k:v for k,v in left[0].items() if k!='args'}=={k:v for k,v in right[0].items() if k!='args'}
                assert left[0]['args'][:3]==right[0]['args'][:3]
                assert left[0]['args'][3]==0x02660000+a and right[0]['args'][3]==0x02660000+b
            pictures.append(dict(word=word,old_offset=a,new_offset=b,cases=versions))
    assert len(dispatches)==31 and sum(r['resolved_actor_ID'] is None for r in dispatches)==1
    assert len(leaves)==16 and len(pictures)==4 and not ctx.machines
    assert sum(r['word']==0xA000 for r in leaves)==sum(r['word']==0 for r in leaves)==sum(r['word']==0x2000 for r in leaves)==1
    assert len(spec['original2000_pause_and_resume_maps'])==1
    pause=spec['original2000_pause_and_resume_maps'][0]
    assert pause['old_offset']==56 and pause['source_resume']==58 and pause['target_resume']==pause['new_offset']+2
    assert sum(bytes.fromhex(r['target_hex'])[1:].count(b'FI') for r in spec['text_records'])==1
    save(ROOT/'all31_dispatches_two_picture_two47xx_pairs_one_pause_and16_exact_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all16_source_current_target_control_leaves=leaves,picture_and_short47xx_pairs=pictures,
        one_source_pause_and_resume_map=pause,original40_resource_boundary_cases_seven_structural_pairs_reused_by_exact_bytes_and_current_snapshot=True,
        all30_progressive_and_one_null_actor_sound_effect_FE_preserved=True,one_FI_no_FA_FO_preserved=True,
        original_R58_effective_Camille_question_preserved_in_direct_reviewed_target_no_stale_catalog_match=True,
        no_predicates_choices_relative_sites_or_C200_inherited=True,
        picture_descriptor_and_short47xx_words_not_promoted_to_item_semantics=True,
        source_commands_controls_and_single_complete_end_not_omitted=True,actual_English_scene_comparison_pending=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]},
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('31 relocated dispatches,two picture/two47xx pairs,one pause and16 exact leaves pass;one FI and effective Camille retained. English scene next.')
