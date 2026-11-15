"""Bind final B196 dispatches, seven unforced predicates, pictures and six menus."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.prepare_lil_B196_research_v5618 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_relocated_controls_v5623')
DOC=Path('translations/lil_B196_editorial_manuscript_v3.json')
MENU=Path('translations/lil_B196_choice_manuscript_v2.json')
FUNDS=Path('work/analysis/lil_B196_funds_v5601b/six_exact_source_prices_six_unforced_and_thirty_offline_payment_boundaries.json')
OTHER=Path('work/analysis/lil_B196_6003_ends_v5597/source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,menu,plan=map(read,[DOC,MENU,PLAN]);packet=read(doc['source_context'])
    dp,cp=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract']])
    images=[NdsImage.open(p) for p in [PARENT,ROM]]
    arm=images[1].read_file('/__arm9__.bin')
    assert images[0].read_file('/__arm9__.bin')==arm
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[196] for im in images]
    spec=plan['blocks'][0];assert len(plan['blocks'])==1
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](images[1])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];predicates=[];pictures=[];menus=[]
    source_leaves={r['offset']:r for r in dp['source_current_opaque_nonrelative_control_leaves']}
    source_predicates={r['offset']:r for r in cp['source_predicate_cases']}
    source_pictures={r['source_offset']:r for r in cp['source_picture_pairs']}
    for r in spec['text_records']:
        value=bytes.fromhex(r['target_hex']);at=r['new_offset']
        assert new[at:at+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        expected,match=namespace['expanded_current_body'](value[1:]);assert match is None
        actor=None if value[0]==254 else rows[r['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==expected.hex()
        assert result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if actor is None:assert result['FE_original_null_actor_calls'] and b'FI' in value[1:] and b'Lil' in expected
        dispatches.append(dict(id=r['id'],new_offset=at,stored_target_hex=value.hex(),**result))
    for c in spec['command_map']:
        word=c['word'];a,b=c['old_offset'],c['new_offset']
        if word in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
        raw=new[b:b+c['new_extent']];assert raw==old[a:a+c['old_extent']]
        ref=source_leaves[a];assert ref['word']==word and ref['native_extent']==len(raw) and ref['clean_current_hex']==raw.hex()
        leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        command=dict(offset=b,word=word,native_extent=len(raw),whole_command_hex=raw.hex())
        if word==0x8000:
            result=ctx.execute(probe,new,command);ctx.machines.pop();prior=source_predicates[a]
            assert result['native_result']==prior['native_result'] and not result['original_event_completion_calls']
            assert result['no_predicate_or_event_flag_forced'] and result['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact']
            predicates.append(dict(old_offset=a,new_offset=b,**result))
        elif word==0x4821:
            result=ctx.execute(picture,new,command);ctx.machines.pop();prior=source_pictures[a]['cases'][1]
            assert result['original_picture_boundary_calls']==prior['original_picture_boundary_calls']
            pictures.append(dict(old_offset=a,new_offset=b,**result))
    for c in spec['choice_commands']:
        at=c['new_offset'];raw=new[at:at+c['new_length']]
        rs=sorted([r for r in menu['records'] if r['command_offset']==c['old_offset']],key=lambda r:r['option_index'])
        assert len(rs)==2 and [r['english'] for r in rs]==['Buy','Pass']
        assert all(r['typed_target_object_hex']==raw.hex() for r in rs)
        command=dict(offset=at,word=0x2100,native_extent=len(raw),whole_command_hex=raw.hex())
        getters=choice_getters(arm,command)
        assert len(getters)==2 and all(p['count']==2 and [r['text'] for r in p['labels']]==['Buy','Pass'] for p in getters)
        menus.append(dict(old_offset=c['old_offset'],new_offset=at,command=command,native_getter_phases=getters,record_IDs=c['record_IDs']))
    assert len(dispatches)==24 and sum(r['resolved_actor_ID'] is None for r in dispatches)==1
    assert len(leaves)==37 and len(predicates)==7 and len(pictures)==6 and len(menus)==6 and not ctx.machines
    assert sum(r['word']==0xA000 for r in leaves)==14 and sum(r['word']==0 for r in leaves)==7
    assert sum(r['word']==0x6003 for r in leaves)==1
    assert sorted({r['word'] for r in leaves if r['word']&0xFF00==0x6300})==[0x6302,0x632E]
    funds,other=map(read,[FUNDS,OTHER])
    assert funds['candidate_sha256']==other['candidate_sha256']==doc['current_ROM_sha256']
    assert funds['six_source_prices_match_six_exact_native_payment_amounts'] and len(funds['cases'])==36
    paths=[DOC,MENU,PLAN,FUNDS,OTHER,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]
    save(ROOT/'all24_dispatches_seven_predicates_six_pictures_menus_and37_exact_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(arm),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves=leaves,
        relocated_unforced_predicates=predicates,relocated_picture_boundaries=pictures,relocated_menu_getters=menus,
        all23_progressive_actors_and_one_null_actor_FE_FI_exact=True,all_six_typed_menus_and_seven_source_endings_preserved=True,
        all36_payment_boundaries20_resource_boundaries10_6003_boundaries_and14_opaque_structural_pairs_reused=True,
        reuse_requires_identical_whole_ARM9_original_snapshot_and_complete_command_bytes=True,
        picture_resource_6003_and_item_Charm_bodies_not_executed_by_this_probe=True,
        menu_input_loops_actual_association_and_branch_reachability_pending=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B196_IDs=[],new_emulator_runs=0,
        no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False))
    print('24 relocated speech/FE-FI calls,7 unforced predicates,6 pictures,6 menus and37 exact leaves pass. Unchanged payment/resource/6003/opaque contracts reused;actual selection and effects remain separate.')
