"""Verify all stored speaker/voice dispatches andrelocated raw predicates without game-state forcing."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_relocated_controls_v7991')
MAP=Path('work/analysis/Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B47_effective_v7981/all15_effective_English_templates30_original_progressive_dispatches.json')
SOURCE=Path('work/analysis/Rafael_B47_source_controls_v7977/source_EV0_24_relative_sites120_cases6_raw_predicates25_seeded_ends.json')
STORED=Path('work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json')
INPUT=Path('work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,effective,source,stored=map(read,[MAP,CURRENT,EFFECTIVE,SOURCE,STORED])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    image=NdsImage.open(current['current_ROM'])
    assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']==source['candidate_sha256']
    g=mapping['groups'][0];block=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks[47]
    assert sha(block)==g['target_block_sha256']==stored['research_block_sha256'] and len(block)==1344
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':0,'route_mask':1,'CATALOG_LOOKUP':{}}
    for name,text in effective['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::original-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    dispatches=[];predicates=[];controls=[]
    for ref in g['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0'
        result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
        expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
        boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body')
        assert boundary['text_hex']==expected and result['resolved_actor_ID']==raw[0] and result['source_voice_class']=={0:2,4:0,5:4,6:5}[raw[0]]
        assert not result['FE_original_null_actor_calls']
        dispatches.append(dict(id=ref['id'],final_offset=at,final_stored_hex=raw.hex(),**result))
    for a,b,m in zip(current['groups'][0]['all_source_commands'],g['all_target_commands'],g['command_map'],strict=True):
        assert a['word']==b['word']==m['word']
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex']
        controls.append(dict(source_offset=a['offset'],target_offset=b['offset'],word=a['word'],source_command_hex=a['whole_command_hex']))
        if a['word']==0x8000:
            result=ctx.execute(probe,block,b);ctx.machines.pop()
            original=next(r for r in source['source_raw_predicates'] if r['offset']==a['offset'])
            assert result['native_result']==original['native_result'] and result['source_command_hex']==original['source_command_hex']
            predicates.append(dict(source_offset=a['offset'],target_offset=b['offset'],original=original,relocated=result))
    assert len(dispatches)==15 and len(predicates)==6 and len(controls)==9 and not ctx.machines
    assert len(g['relative_fixups'])==24 and sum(len(r['cases']) for r in g['relocated_skip_cases'])==120
    terminal=g['all_target_commands'][-1]
    assert terminal['word']==0 and terminal['offset']==1340 and terminal['offset']+4==g['target_logical_end']==1344
    adapter=source['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__)
    exec(compile(adapter,__file__+'::relocated-normal-end-carry','exec'),env);arm=image.read_file('/__arm9__.bin')
    ends=[env['end_case'](arm,block,1340,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    save(ROOT/'15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),
        stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),final_dispatches=dispatches,
        original_nontext_control_maps=controls,relocated_relative_cases=g['relocated_skip_cases'],relocated_predicates=predicates,
        normal_seeded_ends=ends,all15_final_actors_voices_andcomplete_stored_bodies_exact=True,
        all_six_raw_predicates_current_unforced_values_preserved_including_unaligned_scratch_restore=True,
        original61FF_A000_andcomplete_normal_end_bytes_exact=True,
        original_source_structural_pairs_reused_by_exact_command_andruntime_bytes=True,
        full_A000_effect_body_not_explained_orclaimed_as_actual_execution=True,
        registered_current_catalogue_binding=catalogue,no_source_FE_typed_menu_orinvented_printf_conversion=True,
        no_gameplay_condition_roster_role_seed_orresult_forced=True,
        actual_B47_selected_paths_nameplates_normal_value_carry_andR53_page_turn_still_pending=True,
        fullreference_loaders_callers_frozen_policy_atomic_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,CURRENT,EFFECTIVE,SOURCE,STORED,INPUT,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('15 final stored dispatches,6 original raw predicates,24sites120cases and25 normal carry ends pass.Actual paths/R53 page turn/reference/release pending.')
