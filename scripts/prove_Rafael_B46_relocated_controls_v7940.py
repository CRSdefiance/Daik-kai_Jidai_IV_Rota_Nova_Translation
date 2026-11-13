"""Final stored dispatches, original typed-menu association and normal-end carry; actual paths pending."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_relocated_controls_v7940')
MAP=Path('work/analysis/Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json')
SOURCE=Path('work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json')
STORED=Path('work/analysis/Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json')
MENU=Path('work/analysis/Rafael_B46_stored_v7939/two_stored_menu_labels_exact8_viewed_planes_two_header_alignments.json')
INPUT=Path('work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,effective,source,stored,menu=map(read,[MAP,CURRENT,EFFECTIVE,SOURCE,STORED,MENU])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    image=NdsImage.open(current['current_ROM'])
    assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']==source['candidate_sha256']
    g=mapping['groups'][0];block=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks[46]
    assert sha(block)==g['target_block_sha256']==menu['research_block_sha256']
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':0,'route_mask':1,'CATALOG_LOOKUP':{}}
    for name,text in effective['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::original-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');dispatches=[]
    for ref in g['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0'
        result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop();is_FE=raw[0]==254
        expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
        boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
        assert boundary['text_hex']==expected and result['resolved_actor_ID']==(None if is_FE else raw[0])
        assert result['source_voice_class']==(None if is_FE else {0:2,5:4,6:5}[raw[0]])
        if is_FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
        dispatches.append(dict(id=ref['id'],final_offset=at,final_stored_hex=raw.hex(),**result))
    controls=[]
    for a,b,m in zip(current['groups'][0]['all_source_commands'],g['all_target_commands'],g['command_map'],strict=True):
        assert a['word']==b['word']==m['word']
        if a['word'] in [0x4000,0x2100,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex']
        controls.append(dict(source_offset=a['offset'],target_offset=b['offset'],word=a['word'],source_command_hex=a['whole_command_hex']))
    assert len(dispatches)==24 and sum(r['resolved_actor_ID'] is None for r in dispatches)==12
    assert len(controls)==8 and sum(r['word']==0xA000 for r in controls)==5 and not ctx.machines
    assert len(g['relative_fixups'])==4 and sum(len(c['cases']) for c in g['relocated_skip_cases'])==20
    terminal=g['all_target_commands'][-1];assert terminal['word']==0 and terminal['offset']+4==g['target_logical_end']==1526
    adapter=source['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::relocated-normal-end-carry','exec'),env)
    arm=image.read_file('/__arm9__.bin')
    ends=[env['end_case'](arm,block,terminal['offset'],p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    save(ROOT/'24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),
        stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),final_dispatches=dispatches,
        original_nontext_control_maps=controls,relocated_relative_cases=g['relocated_skip_cases'],normal_seeded_ends=ends,
        stored_typed_menu_proof=str(MENU),stored_typed_menu_proof_sha256=sha(MENU.read_bytes()),
        all_five_A000630061FF_andcomplete_normal_end_exact=True,
        original_source_structural_effect_cases_reused_by_exact_command_andruntime_bytes=True,
        full_A000_resource_effects_not_explained_orclaimed_executed=True,
        registered_current_catalogue_binding=catalogue,all24_final_body_actor_voice_and12_FE_null_actor_dispatches_exact=True,
        exact_two_choices_andboth_even_header_alignments_bound=True,
        no_gameplay_result_orbranch_condition_orseed_forced=True,
        actual_normal_end_value_carry_must_be_measured_for_both_choices_not_forced_zero=True,
        actual_body_names_FE_menu_backing_highlights_transitions_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,CURRENT,EFFECTIVE,SOURCE,STORED,MENU,INPUT,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('24 final dispatches/12 FE paths,two stored choices/four sites20 cases/25 seeded carry ends pass. Actual effects/selection/display pending.')
