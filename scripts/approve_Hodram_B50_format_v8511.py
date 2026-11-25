"""Approve three B50 formatting decisions after complete native and paired actual evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_format_v8511')
OLD=Path('translations/hodram_B50_editorial_manuscript_v3.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v4.json')
OLD_NAMES=Path('translations/hodram_B50_speaker_name_review_v1.json')
NAMES=Path('translations/hodram_B50_speaker_name_review_v2.json')
PROOFS={
 'native_view':'work/analysis/Hodram_B50_native_review_v8493/native_body_review.json',
 'relocation':'work/analysis/Hodram_B50_relocation_v8495/reconstruction.json',
 'stored':'work/analysis/Hodram_B50_stored_v8496/stored_bodies.json',
 'controls':'work/analysis/Hodram_B50_controls_v8497/stored_controls.json',
 'independent':'work/analysis/Hodram_B50_independent_v8501/independent_reconstruction.json',
 'reference':'work/analysis/Hodram_B50_reference_v8502/research_image_receipt.json',
 'loaders':'work/analysis/Hodram_B50_loaders_v8503/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'references':'work/analysis/Hodram_B50_references_v8503/references.json',
 'fixtures':'work/analysis/Hodram_B50_fixtures_v8504/two_whole_scripts.json',
 'whole_actual':'work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json',
 'whole_view':'work/analysis/Hodram_B50_actual_review_v8510b/whole_exchange_review.json',
 'FE_binding':'work/analysis/Hodram_B50_FE_binding_v8508/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
 'comparison':'work/analysis/Hodram_B50_comparison_v8509/paired_selected_path_comparison.json',
 'differences':'work/analysis/Hodram_B50_difference_view_v8510/sheet.json',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old,names=map(read,[OLD,OLD_NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert old['translation_policy']=='natural-dialogue-v2' and old['target_locale']=='en-US' and old['encoder']=='dialogue-relocatable-v1'
    assert len(old['records'])==3 and old['physical_speech_objects']==3 and old['typed_choice_objects']==0
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in old['records'])
    assert data['native_view']['all_three_complete_bodies_visually_read'] and data['native_view']['no_qa_waivers']
    assert data['stored']['all3_ink_planes_exact_to_already_viewed'] and data['stored']['compiler_tails_create_no_blank_oradditional_page']
    assert data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert data['controls']['all3_source_actors_voices_full_preambles_stored_bodies_andoriginal_null_FE_exact']
    assert data['controls']['original_item148_layout0_andhide_boundaries_exact'] and data['controls']['no_relative_orquery_sites_and25_normal_value_carries_pass']
    assert not data['whole_actual']['unresolved'] and data['whole_actual']['all_observed_complete_body_name_holds_andnative_flow_pass']
    assert data['whole_view']['all_three_sheets_directly_viewed'] and data['whole_view']['FE_before6302_original_order_andabsent_header_portrait_preserved_inboth_languages']
    assert data['whole_view']['actual_complete_source_andEnglish_body_name_orabsent_FE_header_holds']==50
    assert data['FE_binding']['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model']
    assert [len(g['complete_actual_holds']) for g in data['FE_binding']['groups']]==[3,3]
    observed={s['id'] for g in data['whole_actual']['groups'] for s in g['speeches']};assert observed=={r['id'] for r in old['records']}
    mapping=data['relocation']['groups'][0];refs={r['id']:r for r in mapping['text_records']}
    doc=deepcopy(old);ng=deepcopy(names)
    for row in doc['records']:
        ref=refs[row['id']];assert row['final_hex']==row['stored_hex']==ref['target_hex'] and row['compiled_hex']==ref['compiled_hex']
        assert row['final_reference']['offset']==ref['new_offset'] and row['final_reference']['bytes']==ref['new_length']
        actual=[]
        for g in data['whole_actual']['groups']:
            s=next(s for s in g['speeches'] if s['id']==row['id']);assert s['complete_holds'] and s['selected_capture']
            actual.append(dict(version=g['version'],source_selector=s['source_selector'],name=s['name'],selected_capture=s['selected_capture'],complete_holds=len(s['complete_holds'])))
        reason=row['native_body_review_reason']+' Complete stored bodies,compiler-owned parity,all original commands/preambles andsource/current inverses remain exact. Both initialized source/English exchanges showcomplete first/internal/final glyphs andsinglepages,original names/portraits orabsent FEheader,andnormal full-end returns. No authored breaks,padding,shortening,viewport/font changes,extra pages orQA waivers.'
        if row['source_selector']==254:reason+=' Original FE-before6302 order ispreserved. Two live paint snapshots andsix same-run holds bind228x48/288stride/6x12/physical16pitch,source-qualified vtables,palette,full bank-D bitmap andRGB;the outgoing wristband notice remains distinct fromthe following Ullr bow acquisition UI.'
        row.update(actual_display_evidence=actual,formatting_approval_reason=reason,formatting_approval_pending_actual_transition_policy_andrelease=False,formatting_registered_release_pending=True,current_review_status='all-five-individual-gates-reviewed-frozen-policy-atomic-registered-release-pending')
        row['review']['formatting']=True
    assert len(ng['records'])==1 and ng['records'][0]['actor_ID']==2 and ng['records'][0]['decision']=='retention'
    name=ng['records'][0];assert all(name['review'].values())
    name.update(actual_body_name_proof=PROOFS['whole_actual'],actual_body_name_proof_sha256=sha(Path(PROOFS['whole_actual']).read_bytes()),actual_complete_Lil_Argot_nameplates_in_both_source_andEnglish=True,actual_final_t_andleading_L_complete=True,registered_name_asset_change=False)
    ng.update(predecessor=str(OLD_NAMES),predecessor_sha256=sha(OLD_NAMES.read_bytes()),scoped_Lil_name_actual_header_binding_complete=True,all207_names_roles_aliases_andcustom_names_still_open=True,new_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(NAMES,ng)
    doc['review_gates']['formatting']=True
    doc['all_three_four_prose_gates_true_formatting_false']=False;doc['all_three_formatting_gates_still_false']=False
    doc['distinct_actual_transition_risk']['actual_source_andEnglish_FE_header_portrait_typed_view_palette_VRAM_anditem_transition_need_representative_capture']=False
    doc['distinct_actual_transition_risk'].update(actual_source_andEnglish_behavior_verified=True,evidence=[PROOFS['whole_actual'],PROOFS['FE_binding'],PROOFS['whole_view']])
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),status='all-five-individual-gates-reviewed-frozen-policy-atomic-registered-release-pending',all_three_individual_five_gates_true=True,
        reference_ROM=data['reference']['research_ROM'],reference_ROM_sha256=data['reference']['research_ROM_sha256'],actual_source_andEnglish_all_three_speeches_observed_in_complete_initialized_fixtures=True,actual_emulator_runs=2,total_actual_frames=20002,actual_complete_body_name_orabsent_FE_header_holds=50,
        remaining_required_work='Frozen natural-dialogue-v2 policy,meaningful semantic rejection tests,independent production validation/one-complete-ROM atomic commit,registered cumulative release/exact clean-input patch andown startup beforeonce-only3credit.',
        formatting_evidence={k:dict(path=p,sha256=sha(Path(p).read_bytes())) for k,p in PROOFS.items()},measured_limits=data['whole_view'],natural_optional_activation_original_location_earned_inventory_future_PRNG_outcomes_broad_simulation_fullroute_hardware_andcustomnames_not_claimed=True,
        no_new_ROM_orregistered_stage_orcompletion_credit=True,new_credit=0,full_goal_complete=False)
    for before,after in zip(old['records'],doc['records'],strict=True):
        for key in ['id','english','source_hex','source_reference','current_hex','current_reference','compiled_hex','final_hex','stored_hex','final_reference','decision','finding','retention_reason']:
            assert before[key]==after[key]
        assert all(after['review'].values())
    save(DOC,doc)
    save(ROOT/'formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),individual_speech_approvals=3,typed_choices=0,scoped_name_retentions=1,all3_five_gates_true=True,all_source_current_final_references_bound=True,all_approved_words_andcompiled_bytes_unchanged=True,actual_frames=20002,actual_emulator_runs=2,complete_holds=50,FE_original_paint_two_snapshots_six_VRAM_palette_RGB_holds=True,measured_limits=data['whole_view'],registered_policy_atomic_build_patch_startup_andonceonly_credit_still_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,*map(Path,PROOFS.values()),Path(__file__)]}))
    print('B50 three individual formatting gates approved;allwords/source/current/finalrefs unchanged. Actual20002frames/2runs/50holds,twoFEpaint/sixVRAMholds;alllimits retained.Policy/atomic/registeredrelease pending;zero credit.')
