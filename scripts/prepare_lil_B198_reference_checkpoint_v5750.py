"""Prepare a lossless successor checkpoint after the B198 style-reference risk is resolved."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_reference_checkpoint_tools_v5750')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/checkpoint_lil_B198_v5730.py').read_text(encoding='utf-8')
    a=source.index('SUMMARY=(');b=source.index('\n\ndef inverse',a)
    c=source.index('def gates():');d=source.index('\n\ndef audit(',c)
    gates='''def gates():
    doc=read(DOC)
    sealpath=Path('work/analysis/lil_B198_reference_approval_v5746/reference_approval.json')
    seal=read(sealpath)
    assert seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['all17_source_native_reference_and_representative_rules_approved']
    assert seal['source_prose_English_and_compiled_targets_unchanged']
    assert len(doc['records'])==17 and doc['revised']==12 and doc['retained']==5 and all(all(r['review'].values()) for r in doc['records'])
    font=read(doc['native_font_proof']);stored=read(doc['final_padding_proof']);control=read(doc['relocated_control_proof'])
    sample=read(doc['representative_proof']);visual=read(doc['postscene_native_state_proof']);style=read(doc['source_original_progressive_style_proof'])
    actualpath=Path(visual['actual_proof']);actual=read(actualpath)
    assert font['current_original_macro_alignment_calls']==136 and font['source_original_progressive_caller_style']==11
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(11,6) and len(font['negative_controls'])==18
    assert stored['current_final_stored_macro_alignment_cases']==68 and stored['source_original_progressive_caller_style']==11
    assert stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
    assert style['source_explicit_style']==11 and all(r['exact_actual_ink'] and r['exact_actual_gray'] for r in style['cases'])
    assert len(control['relocated_dispatch_cases'])==17 and len(control['original_unforced_predicate_pairs'])==2 and len(control['all12_source_current_target_control_leaves'])==12
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['actual_timing_differences'] and not actual['later_whole_RGB_differences']
    assert sample['source_and_English_return_frames']==[6697,6697] and sample['sampled_nontext_frames']==182
    assert len(sample['actual_sampled_display_IDs'])==15 and sample['offline_only_display_IDs']==['DK4_MES_B198_R0065','DK4_MES_B198_R0095']
    assert visual['final_13001_PRNG_seeds']==sample['final_13001_PRNG_seeds'] and len(set(visual['final_13001_PRNG_seeds']))==1
    assert visual['no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim']
    mapping=read(doc['reference_map']);block=mapping['blocks'][0]
    assert (block['source_bytes'],block['research_bytes'])==(544,644) and len(block['mapped_native_commands'])==37
    assert len(block['relative_skip_fixups'])==8 and len(block['target_native_skip_cases'])==40 and mapping['external_references_complete']
    paths={DOC,sealpath,actualpath,Path(__file__),Path('scripts/lil_B198_reference_checkpoint_text_v5750.py')}
    for key,value in doc.items():
        if key.endswith('_sha256') and isinstance(doc.get(key[:-7]),str) and Path(doc[key[:-7]]).is_file():
            p=Path(doc[key[:-7]]);assert sha(p.read_bytes())==value;paths.add(p)
    for key in ['all_current_native_sheets_viewed','all_actual_consumer_sheets_viewed','paired_full_screen_views']:
        assert len(visual[key])==3
        for r in visual[key]:
            assert r['viewed_in_full_current_turn'] and r['original_detail']
            p=Path(r['path']);assert sha(p.read_bytes())==r['sha256'];paths.add(p)
    for data in [seal,sample,visual,actual]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;paths.add(Path(p))
    for p in [Path('scripts/audit_lil_B198_actual_v5740.py'),Path('scripts/probe_lil_B198_ellipsis_context_v5740b.py')]:
        assert p.is_file();paths.add(p)
    return doc,{str(p):sha(p.read_bytes()) for p in paths}
'''
    tool=derive('scripts/checkpoint_lil_B198_v5730.py','scripts/checkpoint_lil_B198_reference_v5750.py',{
        source[a:b]:'from scripts.lil_B198_reference_checkpoint_text_v5750 import SUMMARY,NEXT\n',source[c:d]:gates,
        'checkpoint_v5730':'reference_checkpoint_v5750','verification_v5731':'verification_v5751',
        'verification_v5709':'verification_v5731','editorial_manuscript_v4.json':'editorial_manuscript_v6.json',
        'Lil_B198_native_review_v5730':'Lil_B198_reference_review_v5750',
        'previous_latest_checkpoint_before_Lil_B198_v5730':'previous_latest_checkpoint_before_Lil_B198_reference_v5750',
        "SCOPE='unfinished_editorial_scope_v5730'":"SCOPE='unfinished_editorial_scope_v5750'",
        "old['unfinished_editorial_scope_v5708']":"old['unfinished_editorial_scope_v5730']",
        "scope['historical_Lil_B198_clean_source_bound_before_v5730']=scope.pop('next_Lil_B198_clean_review_pending')":
        "scope['historical_Lil_B198_native_approved_before_v5750']=scope.pop('next_Lil_B198_native_approved_uncredited_v5730')",
        "scope['next_Lil_B198_native_approved_uncredited_v5730']":"scope['next_Lil_B198_reference_approved_uncredited_v5750']",
        'external_references_relocated_controls_English_actual_atomic_compiler_registered_release_pending=True':
        'atomic_compiler_registered_release_clean_patch_and_current_startup_pending=True',
        'new_editorial_credit=0,new_ROMs=1':'new_editorial_credit=0,new_ROMs=2',
        'new_revised_English_ROMs=0':'new_revised_English_ROMs=1',
        'actual_source_frames=13001,actual_source_speeches=15':'actual_source_frames=13001,actual_source_speeches=15,actual_English_frames=13001,actual_English_speeches=15,actual_native_holds=56,total_source_English_frames=26002',
        "remaining_gates=['whole-image-load-and-external-entry-reference-map','relocated-dispatch-controls-and-end',\n                'focused-English-scene-transition-comparison','atomic-compiler-registered-release-clean-patch-current-startup']":
        "remaining_gates=['atomic-compiler-semantic-negatives-before-mutation','registered-release-clean-patch-current-startup']",
        '## V5730: B198 whole-exchange native review;17 uncredited objects':'## V5750: B198 reference and English scene approved;17 uncredited objects',
        '# Current editorial handoff - V5730':'# Current editorial handoff - V5750',
        'B198_reference_English_actual_compiler_registered_release_pending=True':'B198_references_and_English_actual_approved=True,B198_atomic_compiler_registered_release_and_startup_pending=True',
        'V5731 verified:17 B198 native-reviewed/uncredited objects saved;V5692/main/counters unchanged. Full goal active.':
        'V5751 verified:17 B198 reference/gameplay-approved objects saved uncredited;V5692/main/counters unchanged. Full goal active.'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reference_checkpoint.json',dict(tool=tool,
        all_current_and_historical_ledger_values_recoverable=True,all17_objects_remain_uncredited=True,
        all_source_correct_style11_native_references_and15_actual56_holds_bound=True,
        whole_image_references_and_English_actual_not_repeated=True,atomic_compiler_registered_release_and_current_startup_next=True,
        full_broader_editorial_name_review_and_separate_graphics_later_reaudit_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared lossless B198 reference/gameplay checkpoint;atomic compiler/registered release next. Full objective preserved.')
