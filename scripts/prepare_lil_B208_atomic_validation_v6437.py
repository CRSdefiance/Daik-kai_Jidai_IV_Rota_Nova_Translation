"""Prepare B208 semantic rejection cases with distinct FE/thought/phase/state risks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_atomic_validation_tools_v6437')
if __name__=='__main__':
    assert not ROOT.exists()
    extras='''    mutations.extend([
      ('FE-attributed-to-actor',PROOFS['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][-1].update(resolved_actor_ID=254)),
      ('FE-attributed-voice',PROOFS['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][-1].update(source_voice_class=3)),
      ('FE-invented-nameplate',PROOFS['actual_proof'],lambda v:v['actual_panels'][-1]['holds'][0].update(nameplate_expected=True)),
      ('FE-clipped-literal-name',PROOFS['actual_proof'],lambda v:v['actual_panels'][-1]['holds'][0].update(all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane=False)),
      ('thought-unparenthesized',DOC,lambda v:next(r for r in v['records'] if r['source_record_index']==86).update(english=next(r['english'] for r in v['records'] if r['source_record_index']==86).replace('(','',1))),
      ('FE-wrong-person',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Lil: Charm +1!')),
      ('FE-wrong-attribute',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Cristina: Charisma +1!')),
      ('FE-wrong-amount',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Cristina: Charm +2!')),
      ('phase-36-cell-guard-lost',doc['phase_capacity_proof'],lambda v:v.update(first36_cell_preLF_auto_wrap_rejected=False)),
      ('phase-missing-native-plane',doc['phase_capacity_proof'],lambda v:v['cases'].pop()),
      ('phase-codec-hash-lost',doc['phase_capacity_proof'],lambda v:v.update(unchanged_codec_sha256='0'*64)),
      ('target-tail-lost',MAP,lambda v:v['blocks'][0].update(target_alignment_tail_bytes=0)),
      ('erased-duration-difference',PROOFS['postscene_native_state_proof'],lambda v:v['command_duration_changes'].pop()),
      ('claimed-all-final-groups-equal',PROOFS['postscene_native_state_proof'],lambda v:v['five_native_component_equality'].update(models=True)),
      ('erased-actual-hold',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'].pop()),
      ('lost-FE-null-actor-native-proof',doc['native_font_proof'],lambda v:v['cases'][-1].update(original_null_actor_consumer_preserved=False)),
      ('wrong-FE-font-consumer',DOC,lambda v:v['records'][-1].update(native_display_consumer='original_progressive_54020')),
      ('lost-declared-end-extent',MAP,lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(extent=2)),
    ])
'''
    r=derive('scripts/validate_lil_B207_atomic_v6378d.py','scripts/validate_lil_B208_atomic_v6437.py',{
        'lil_B207_editorial_v4':'lil_B208_editorial_v3','seal_lil_B207_references_v6377b':'seal_lil_B208_references_v6434','B207':'B208','atomic_v6378d':'atomic_v6437','reference_approval_v6377b':'reference_approval_v6434','dk4-lil-B207-editorial-release-v4':'dk4-lil-B208-editorial-release-v3',
        "deps.update(mapping['evidence'])":"deps.update(mapping['evidence']);deps.add('dk4tool/patch/lil_B208_editorial_guards_v2.py')",
        "len(proof['changed_records'])==13":"len(proof['changed_records'])==24",'Positive13-record':'Positive24-record','positive_records=13':'positive_records=24','Atomic13-record':'Atomic24-record',
        "english='{SPEAKER:0E}{MACRO:FI}'":"english='{SPEAKER:AA}{MACRO:FI}'",
        'all216x64_ink_gray_pixels_equal_complete_native_plane':'all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane',
        'natural_event207_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed':'natural_event208_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed',
        "('claimed-following-scene-finished',PROOFS['representative_proof'],lambda v:v.update(final11001_both_following_B120_still_active_black_upper=False))":"('lost-following-scene-end',PROOFS['representative_proof'],lambda v:v.update(following_B120_end_frame=0))",
        'all2_source_current_target_nontext_leaves':'all5_source_current_target_nontext_leaves','all13_five_gates_approved':'all24_five_gates_approved','two_native_name_planes_four_getters32_macro_alignments51_actual_header_holds_approved':'two_native_name_planes_four_getters32_macro_alignments91_actual_header_holds_approved',
        "    for gate in doc['records'][0]['review']:":extras+"    for gate in doc['records'][0]['review']:",
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_semantic_validation.json',dict(tool=r,additional18_FE_thought_phase_tail_end_and_honest_state_cases=True,no_evidence_file_modified_by_semantic_injection=True,all_pre_mutation_invariants_and_whole_predecessor_inverse_required=True,full_goal_complete=False));print('B20824-record positive reconstruction and89 semantic rejection cases prepared;no archive mutation or registration.')
