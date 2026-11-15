"""Independent audit of B171 reference/gameplay checkpoint and preserved main build."""
from collections import Counter
import gzip
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4348')
CHECKPOINT=Path('work/analysis/lil_B171_reference_checkpoint_v4347')
DOC=Path('translations/lil_B171_editorial_manuscript_v5.json')
FAMILY='Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37'

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==receipt['ledger_sha256']
    before=json.loads(gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes()))
    allowed={'contextual_story_natural_dialogue_pass_v1871','active_source_prose_drafts','coverage_units',
        'unfinished_editorial_scope_v4347','lil_B171_reference_reconciliation_v4347','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    mutable={'latest_contextual_manuscript','latest_pending_contextual_family','pending_contextual_families','coverage_note'}
    assert {k:v for k,v in old.items() if k not in mutable}=={k:v for k,v in fresh.items() if k not in mutable}
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5762,5725,37)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5725,5765,3635,2090)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert receipt['new_source_prose_reviews']==receipt['new_completed_records']==0
    doc,prior=read(DOC),read('translations/lil_B171_editorial_manuscript_v4.json')
    validate_natural_dialogue_batch(doc)
    assert len(doc['records'])==37
    assert [(r['id'],r['source_hex'],r['current_hex'],r['english'],r['editorial_decision']) for r in doc['records']]==[(r['id'],r['source_hex'],r['current_hex'],r['english'],r['editorial_decision']) for r in prior['records']]
    assert Counter(r['editorial_decision'] for r in doc['records'])==Counter({'revise':24,'retain-wording':13})
    assert all(r['fresh_retained_wording_justification'] for r in doc['records'] if r['editorial_decision']=='retain-wording')
    assert len(fresh['pending_contextual_families'])==1
    pending=fresh['pending_contextual_families'][0]
    assert pending['id']==FAMILY and pending['manuscript']==str(DOC) and pending['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(pending['actual_sampled_display_IDs'])==37 and not pending['offline_only_display_IDs']
    units={r['id']:r for r in ledger['coverage_units']}
    assert all(units[r['id']]==r for r in before['coverage_units'] if r['id'] not in [FAMILY,'all-route-scenes'])
    assert units[FAMILY]['registered_release_pending'] and units[FAMILY]['actual_complete_native_panels']==37
    active=ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(DOC)]==[r['id'] for r in doc['records']]
    assert active['route_record_subsets_pending'][str(Path('translations/lil_B171_editorial_manuscript_v4.json'))]==[]
    for kind in ['evidence','preserved_release_files','updated_files']:
        for path,digest in receipt[kind].items():assert sha(Path(path).read_bytes())==digest,(kind,path)
    approval=read(pending['reference_approval'])
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())} and approval['new_emulator_runs']==4
    for path,digest in approval['evidence'].items():assert sha(Path(path).read_bytes())==digest,path
    mapping=read(doc['reference_map']);b=mapping['blocks'][0]
    assert b['block']==171 and len(b['command_map'])==45 and len(b['text_records'])==37
    assert not b['relative_skip_fixups'] and not b['target_native_skip_cases'] and not b['original2000_pause_and_resume_maps']
    assert [e['source_offset'] for e in b['original_declared_end_word_maps']]==[2112,2116]
    assert [e['target_offset'] for e in b['original_declared_end_word_maps']]==[2302,2306]
    actual=read('work/analysis/lil_B171_actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end.json')
    assert actual['fresh_actual_unique_speech_panels']==actual['complete_matching_observations']==37
    assert not actual['failures'] and not actual['paired_region_differences']
    visual=read('work/analysis/lil_B171_transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review.json')
    assert len(visual['all7_actual_sheets_viewed'])==7 and len(visual['later59_sailing_region_differences'])==59
    assert visual['paired_source_English_whole_RGB_town_returns'][0]['whole_RGB_equal']
    for row in visual['all7_actual_sheets_viewed']:assert sha(Path(row['path']).read_bytes())==row['sha256']
    repeat=read(doc['focused_repeat_proof'])
    assert repeat['paired_town11770_whole1A04_actor_models_and_captain2_equal']
    assert len(repeat['cross_language_command_timing_differences'])==22
    assert sum(r['source']['word']==0x4000 for r in repeat['cross_language_command_timing_differences'])==16
    assert repeat['all_requested_same_ROM_repeat_frames_whole_RGB_equal']
    assert all(all(r['component_equality'].values()) for r in repeat['paired_native_persistent_state_and_PRNG_samples'] if r['frame']<=16450)
    assert repeat['paired_native_persistent_state_and_PRNG_samples'][0]['source_seed']==repeat['paired_native_persistent_state_and_PRNG_samples'][0]['English_seed']
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[11737,11735]
    assert all(len(v['selected_B22_command_pairs'])==53 for v in actual['versions'])
    for case in ['clean_Japanese','reviewed_English']:
        for prefix,number in [('display',4341),('repeat',4343)]:
            terminal=read(Path(f'work/analysis/lil_B171_{prefix}_run_v{number}_{case}')/'terminal.json')
            assert terminal['terminal'] and terminal['observer_host_slots_restored']
    promotion=read('translations/promoted_build.json')
    assert promotion['profile']=='all-routes-unified-v4303'
    assert sha(Path(promotion['rom']).read_bytes())==promotion['rom_sha256']=='6e861308863c5e655aea9927364b2ad3e3bd6200e5cbe52c5bb7d789f4069abe'
    scope=ledger['unfinished_editorial_scope_v4347']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4347')
    assert len(lp.read_bytes())<100*1024*1024
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4347',ledger_sha256=sha(lp.read_bytes()),
        fresh_reread=5762,integrated=5725,pending=37,source_prose=5765,revised=3635,retained=2090,
        new_source_prose_reviews=0,new_completed_records=0,
        all37_source_English_decisions_prior_completions_pending_credit_and_wider_scope_preserved=True,
        all37_native_reference_and_actual_display_approved=True,actual_panels=37,actual_new_cold_boot_runs=4,
        dream_morning_and_whole_RGB_town_control_pass=True,first_end2112_actual_second2116_offline_only=True,
        later59_sailing_differences_and22_command_timing_differences_retained_with_state_PRNG_scope=True,
        all_prior_producers_proofs_and_ROMs_preserved=True,
        promoted_main_V4303_registry_builder_canonical_inputs_and_all_ROMs_preserved=True,
        current_candidate=promotion['rom'],candidate_sha256=promotion['rom_sha256'],remaining_B172_B180_physical_speeches=161,
        registered_B171_compiler_integration_patch_and_startup_pending=True,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V4348 audit passes:5762 rereads/5725 integrated/37 reference-approved pending;37 actual panels,four boots;V4303 main preserved. Full goal active.')
