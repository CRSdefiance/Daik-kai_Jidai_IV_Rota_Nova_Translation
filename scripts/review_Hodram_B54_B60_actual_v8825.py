"""Qualify existing captures,resource views,scope andall measured limitations."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_actual_review_v8825')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v1.json')
PROOFS={
 'relocation':'work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json',
 'independent':'work/analysis/Hodram_B54_B60_independent_v8810/independent_reconstruction.json',
 'stored':'work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json',
 'reference':'work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json',
 'loaders':'work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json',
 'references':'work/analysis/Hodram_B54_B60_references_v8814/references.json',
 'fixtures':'work/analysis/Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
 'models':'work/analysis/Hodram_B54_B60_models_v8817/native_models.json',
 'B56_actual':'work/analysis/Hodram_B56_actual_v8818/B56/paired_actual_dialogue_headers_flow_returns.json',
 'B56_FE':'work/analysis/Hodram_B56_FE_binding_v8819b/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
 'comparison':'work/analysis/Hodram_B54_B60_comparison_v8821/paired_selected_path_comparison.json',
 'focus_actual':'work/analysis/Hodram_B60_focus_actual_v8823/B60/paired_actual_dialogue_headers_flow_returns.json',
 'focus_comparison':'work/analysis/Hodram_B60_focus_comparison_v8824/paired_selected_path_comparison.json',
}
for _block in [54,57,58,59,60]:PROOFS['B'+str(_block)+'_actual']=f'work/analysis/Hodram_B54_B60_actual_v8820/B{_block}/paired_actual_dialogue_headers_flow_returns.json'

if __name__=='__main__':
    assert not ROOT.exists();doc,names=map(read,[DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()};deps={p:sha(Path(p).read_bytes()) for p in PROOFS.values()}
    actual_ids=set();actors=set();runs=[];records=[];sheets=[];total_frames=0;holds=0;pages=0
    for number in [54,56,57,58,59,60]:
        proof=data['B'+str(number)+'_actual'];assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass']
        schedules=[]
        for g in proof['groups']:
            folder=Path('work/analysis/Hodram_B54_B60_scene_runs_v8816')/f'route1_B{number}_{g["version"]}'
            terminal,plan=read(folder/'terminal.json'),read(folder/'run_plan.json');report=read(terminal['report']);trace=read(terminal['observer'])
            assert terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored'] and report['frames']==g['actual_frames']
            assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
            assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
            for p,h in [(terminal['report'],terminal['report_sha256']),(terminal['observer'],terminal['observer_sha256']),(terminal['run_plan'],terminal['run_plan_sha256']),(plan['inputs'],plan['inputs_sha256'])]:assert sha(Path(p).read_bytes())==h;deps[p]=h
            for p in [folder/'terminal.json',folder/'run_plan.json']:deps[str(p)]=sha(p.read_bytes())
            schedules.append(report['scripted_input_schedule']);assert schedules[-1]==read(plan['inputs'])
            assert g['normal_return']['complete_four_byte_end'] and g['normal_return']['native_result']==[0,1 if number==58 else 0]
            for speech in g['speeches']:
                actual_ids.add(speech['id'])
                if speech['source_selector']!=254:actors.add(speech['source_selector'])
                expected_pages=set(range(1,speech['pages']+1));observed={h['native_page'] for h in speech['complete_holds']};assert expected_pages==observed
                for h in speech['complete_holds']:
                    assert sha(Path(h['capture']).read_bytes())==h['sha256'] and h['complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal']
                    assert h['original_FE_absent_nameplate_preserved'] if speech['source_selector']==254 else h['complete_name_mask_equal']
                holds+=len(speech['complete_holds']);pages+=speech['pages'];records.append(dict(block=number,version=g['version'],**speech))
            total_frames+=report['frames'];runs.append(dict(block=number,version=g['version'],frames=report['frames'],terminal=str(folder/'terminal.json'),terminal_sha256=sha((folder/'terminal.json').read_bytes()),
                observed_ids=[s['id'] for s in g['speeches']],unvisited_ids=g['unvisited_conditional_text_IDs'],normal_return=g['normal_return']))
        assert schedules[0]==schedules[1];sheets.extend(proof['review_sheets'])
    assert total_frames==116012 and holds==580 and pages==129 and len(actual_ids)==63 and actors=={1,23,24,36,84,114,119,141}
    all_ids={r['id'] for r in doc['records']};offline=sorted(all_ids-actual_ids)
    assert len(offline)==19 and 'DK4_MES_B55_R0006' in offline and all('B58_' in x for x in offline if x!='DK4_MES_B55_R0006')
    comparison=data['comparison'];assert comparison['total_actual_frames']==116012
    expected_diffs={54:(3,22),56:(0,43),57:(0,56),58:(3,77),59:(65,65),60:(61,61)}
    for g in comparison['groups']:
        assert (g['later_RGB_difference_count'],len(g['later_RGB_comparisons']))==expected_diffs[g['block']] and not g['UI_request_differences']
        assert all(n['captain_ID']==1 for n in g['final_native_values'])
    long60=next(g for g in comparison['groups'] if g['block']==60)
    assert not long60['whole_actors_equal'] and not long60['five_native_component_equality']['persistent_objects']
    focus=data['focus_actual'];fc=data['focus_comparison'];assert not focus['unresolved'] and fc['total_actual_frames']==14002
    assert all(fc['groups'][0]['five_native_component_equality'].values()) and fc['groups'][0]['whole_actors_equal']
    assert fc['groups'][0]['later_RGB_difference_count']==len(fc['groups'][0]['later_RGB_comparisons'])==11
    assert fc['groups'][0]['final_PRNG_seeds']==[3736791874,459828772]
    prefix=[]
    for version in ['clean_Japanese','revised_English']:
        a=read(f'work/analysis/Hodram_B54_B60_scene_runs_v8816/route1_B60_{version}/terminal.json');b=read(f'work/analysis/Hodram_B60_boundary_focus_runs_v8822/route1_B60_{version}/terminal.json')
        ar,br=read(a['report']),read(b['report']);at,bt=read(a['observer']),read(b['observer'])
        assert br['scripted_input_schedule']==[v for v in ar['scripted_input_schedule'] if v['start']<6640] and br['scripted_input_schedule'][-1]['start']==6400
        x=[r for r in at['rows'] if r['frame']<=6640];y=[r for r in bt['rows'] if r['frame']<=6640]
        assert len(x)==len(y)==(41 if version=='clean_Japanese' else 40)
        keys=['frame','kind','WRAM_sha256','DTCM_sha256','ITCM_sha256','CPU128_hex']
        assert all(all(i[k]==j[k] for k in keys) for i,j in zip(x,y,strict=True))
        prefix.append(dict(version=version,matching_callback_rows=len(x),exact_full_memory_CPU_TCM_prefix_through_before_next_A6640=True))
        for t in [b]:
            for key in ['report','observer','run_plan']:assert sha(Path(t[key]).read_bytes())==t[key+'_sha256'];deps[t[key]]=t[key+'_sha256']
    for old,new in zip(data['B60_actual']['review_sheets'],focus['review_sheets'],strict=True):
        assert old['sha256']==new['sha256']==sha(Path(new['path']).read_bytes())
    resource=[]
    for a,b in zip(data['B59_actual']['groups'][0]['speeches'],data['B59_actual']['groups'][1]['speeches'],strict=True):
        assert a['id']==b['id'];pa,pb=[s['selected_capture'] for s in [a,b]]
        ia,ib=[Image.open(p['capture']).convert('RGB') for p in [pa,pb]]
        assert ia.crop((0,0,256,272)).tobytes()==ib.crop((0,0,256,272)).tobytes()
        resource.append(dict(id=a['id'],source_capture=pa,revised_capture=pb,upper_scene_portrait_andresource_RGB_equal_at_corresponding_dialogue_stage=True))
    resource_calls=[]
    for g in data['B59_actual']['groups']:
        calls=[c for c in g['command_pairs'] if c['word'] in [0x4700,0x4800,0x4810]]
        assert [(c['word'],c['canonical_source_offset']) for c in calls]==[(0x4810,44),(0x4700,104),(0x4800,154),(0x4700,458)]
        resource_calls.append(dict(version=g['version'],calls=calls))
    assert data['B56_FE']['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model']
    sheets.extend(comparison['review_sheets']);sheets.extend(fc['review_sheets'])
    assert len(sheets)==27
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'qualified_actual_review.json',dict(manuscript=dict(path=str(DOC),sha256=sha(DOC.read_bytes())),names=dict(path=str(NAMES),sha256=sha(NAMES.read_bytes())),
        total_main_runs=12,total_main_frames=116012,total_main_holds=580,total_main_observed_page_occurrences=129,
        focused_runs=2,focused_frames=14002,total_runs=14,total_frames=130014,total_holds=676,
        actual_unique_text_IDs=sorted(actual_ids),offline_only_text_IDs=offline,actual_progressive_actor_IDs=sorted(actors),records=records,runs=runs,
        all27_main_dialogue_transition_andfocused_transition_sheets_directly_viewed=True,viewed_sheets=sheets,focused_four_dialogue_sheets_identical_to_viewed_long_sheets=True,
        all_selected_complete_pages_names_FEabsence_sourcecontrols_native_returns_andunforced_paths_pass=True,
        source_andEnglish_bodies_use_current_registered_UI_andnames_not_all_Japanese_UI=True,
        B59_whole_original_resource_show_hide_calls=resource_calls,B59_allseven_corresponding_upper_scene_resource_views=resource,
        current_Wepar_Halberd_andLower_Stone_Tablet_labels_are_UI_observations_not_new_source_identity_oritem_editorial_approval=True,
        B56_two_actual_FEcontexts_andsix_bitmap_palette_VRAM_RGB_holds=str(PROOFS['B56_FE']),
        all_measured_long_timing_RGB_RNG_calendar_actor_andfollowing_command_differences=deepcopy_data if False else comparison,
        focused_B60_bounded_comparison=fc,focused_common_input_prefix_exact_rows=prefix,
        focused_final7001_matches_all_five_components_wholeactors_captain_andrawcalendar=True,
        focused_PRNG_and11later_RGB_pairs_still_differ_andlong_actor_divergence_not_erased=True,
        main_WRAM_not_saved_by_boundary_native_exports_no_immediate_return_actor_snapshot_claim=True,
        no_everyframe_causality_broad_future_simulation_original_location_natural_eligibility_fullroute_orhardware_claim=True,
        no_input_retiming_savestate_RAM_code_eventflag_roster_RNG_funds_orresults_forced=True,
        full_names_shared_de_ownership_all207_catalogue_UI_customnames_wider_contexts_still_open=True,
        all_prior_outputs_andstopped8819_fourhold_assumption_preserved_8819b_uses_actual_threeholds=True,
        sourcequalified_production_atomic_registered_cumulative_cleanpatch_startup_andonceonly_credit_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={**deps,str(DOC):sha(DOC.read_bytes()),str(NAMES):sha(NAMES.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}))
    print('Qualified14runs/130014frames;main63uniqueutterances/129pages/580holds;19offline.27sheets viewed. B60focus boundedstatepass;alllong/RNG/RGBlimits retained.No credit.',flush=True)
