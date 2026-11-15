"""Final stored dispatches and relocated predicate/end probes; exact source control reuse is explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_relocated_controls_v7886')
MAP=Path('work/analysis/Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json')
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B45_effective_v7872/all12_effective_English_templates24_original_dispatches_distinct_FE.json')
SOURCE=Path('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json')
STORED=Path('work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json')
INPUT=Path('work/analysis/current_V7857_Rafael_native_v7868/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,effective,source,stored=map(read,[MAP,CURRENT,EFFECTIVE,SOURCE,STORED])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']==source['candidate_sha256']
    bank=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks;group=mapping['groups'][0];block=bank[45]
    assert sha(block)==group['target_block_sha256']
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':0,'route_mask':1,'CATALOG_LOOKUP':{}}
    for name,text in effective['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::measured-Rafael-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');dispatches=[]
    for ref in group['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0'
        result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop();is_FE=raw[0]==254
        expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
        boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
        assert boundary['text_hex']==expected and result['resolved_actor_ID']==(None if is_FE else raw[0])
        assert result['source_voice_class']==(None if is_FE else {0:2,6:5}[raw[0]])
        if is_FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
        dispatches.append(dict(id=ref['id'],final_offset=at,final_stored_hex=raw.hex(),**result))
    controls=[]
    for a,b,m in zip(current['groups'][0]['all_source_commands'],group['all_target_commands'],group['command_map'],strict=True):
        assert a['word']==b['word']==m['word'] and b['offset']==m['new_offset']
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex']
        controls.append(dict(word=a['word'],source_offset=a['offset'],target_offset=b['offset'],source_hex=a['whole_command_hex'],native_extent=a['native_extent']))
    condition=next(c for c in group['all_target_commands'] if c['word']==0x8000)
    predicate=ctx.execute(probe,block,condition);ctx.machines.pop()
    assert predicate['source_command_hex']==source['source_predicate_exact_operand_hex']
    assert predicate['native_result']==source['source_predicate']['native_result']==[2,1,0,0,0,0]
    end=group['all_target_commands'][-1]
    assert end['word']==0 and end['native_extent']==4 and end['offset']+4==group['target_logical_end']==len(block)
    env=dict(end_case.__globals__);exec(compile(source['source_owned_seeded_end_adapter'],__file__+'::original-cold-seeded-end','exec'),env)
    ends=[env['end_case'](ctx.arm,block,end['offset'],last,seed) for last in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    assert len(dispatches)==12 and len(controls)==7 and not ctx.machines
    assert len(group['relative_fixups'])==5 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==25
    save(ROOT/'12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],
        relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),
        final_dispatches=dispatches,current_catalogue_binding=catalogue,all7_numeric_leaves_source_target_byte_equal=controls,
        relocated_relative_cases=group['relocated_skip_cases'],relocated_relative_fixups=group['relative_fixups'],
        relocated_predicate=predicate,normal_seeded_ends=ends,
        source_control_proof=str(SOURCE),source_control_proof_sha256=sha(SOURCE.read_bytes()),
        exact_reused_original_resources=deepcopy(source['original_resource_boundary_cases']),
        exact_reused_original61FF_C281_structural_pairs=deepcopy(source['isolated_source_61FF_C281_structural_cases']),
        resource_boundaries_not_executed_effects_orcontract_payment=True,
        seeded_ends_use_original_cold_isolated_decoder_not_gameplay_snapshot=True,
        actual_FE_conditional_selection_control_UI_effects_andcomplete_trade_mechanics_unproved=True,
        current_opening_predicate_result_not_natural_Ceuta_eligibility=True,
        no_ROM_RAM_save_roles_roster_funds_RNG_condition_orresult_gameplay_forcing=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_scene_caller_loader_policy_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('12 final stored dispatches,one relocated original predicate,25 seeded normal carry ends pass;five relative sites25cases andsource resource/structural contracts bound. No actual B45 activation/effects claim.')
