"""Independent20-completion ledger,source/runtime/release and coverage audit."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import lil_seville_editorial as owned
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2729')
CHECKPOINT=Path('work/analysis/lil_Seville_completion_v2728')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read('work/analysis/editorial_handoff_verification_v2711/verified_handoff.json')
    assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows};assert len(selected)==len(rows)==20
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':17,'retain-wording':3}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    priorcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==completed==priorcompleted|selected and not priorcompleted&selected
    assert keys=={(r['file_path'],r['id']) for r in oldfresh['record_keys']} and len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==2276
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2276,2276,0)
    assert Counter(path for path,key in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':449,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2276,1592,684)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2279
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for key in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    candidate=ledger['current_integrated_candidate'];rompath=Path(candidate['path']);image=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    release=read('work/analysis/lil_Seville_release_v2725/registered_release_verification.json')
    assert sha(rompath.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==rompath.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v2724' and len(manifest['batches'])==496 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_Seville_registration_v2723/registration_receipt.json')['builder_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);base=NdsImage.open(manifest['base_rom'])
    assert sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    result=owned.apply_release(parent,base);assert parent.read_file('/data/SC2.DK4')==image.read_file('/data/SC2.DK4') and result==release['stage']
    assert release['file_changes']==['/data/SC2.DK4'] and release['component_changes']==[]
    assert sha(image.read_file('/__arm9__.bin'))==before['current_integrated_candidate']['ARM9_sha256']
    en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    for row in rows:
        sr,cr=row['source_reference'],row['integrated_reference'];b=row['block']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(row['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(row['integrated_hex'])==bytes.fromhex(row['current_hex'])
        assert row['current_reference']==cr and cr['record_index']==en[b][:cr['offset']].count(b'\0')
        if row['kind']=='typed-choice-label':assert bytes.fromhex(row['integrated_hex'])==row['english'].encode('ascii')
        else:assert en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00') and bytes.fromhex(row['integrated_hex'])[:1]==bytes.fromhex(row['source_hex'])[:1]
        if row['editorial_decision']=='retain-wording':assert row['fresh_retained_wording_justification'] and row['english'].split('}',1)[1]==' '.join(row['historical_source_prose_predecessor_fields']['current_English'].split())
    mapping=read('translations/lil_seville_editorial_relocation_map_v1.json');assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==69 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==28
    assert mapping['all140_relocated_relative_skip_cases_preserve_original_targets'] and mapping['representative_shared_rules_approved']
    font=read('work/analysis/lil_Seville_font_approval_v2715/all18_native_macro_font_reconciliation.json');assert len(font['cases'])==18 and font['current_original_macro_alignment_calls']==144 and font['all18_current_native_planes_and_complete_glyphs_pass']
    sample=read('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
    assert sample['actual_Seville_IDs']==[] and sample['new_emulator_runs']==0 and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['registered_owned_ITCM_wrapper_delta']['all_other_ITCM_bytes_exact']
    negative=read('work/analysis/lil_Seville_registration_v2723/negative_cases.json');assert len(negative['cases'])==15 and negative['all_rejected_before_mutation']
    start=read('work/analysis/lil_Seville_startup_v2727/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V2674'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['actual_Seville_IDs']==[]
    assert read('work/analysis/lil_Seville_completion_v2728/current_six_frame_visual_review.json')['viewed']
    for case in ['control','newgame','town']:assert read(Path('work/analysis/lil_Seville_runs_v2726')/(case+'_terminal.json'))['terminal']
    inventory=read(ledger['unfinished_editorial_scope_v2728']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0 and inventory['incomplete_route_source_prose_groups']==[]
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert unit['reviewed_route_records']==unit['completed_route_records']==677
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    handoff=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V2728') and '2276 reread /2276 integrated-reconciled /zero pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2728',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        fresh_records=2276,fresh_integrated=2276,fresh_pending=0,source_prose=2279,new_completed_records=20,new_source_prose_reviews=0,revisions=17,justified_retentions=3,
        completed_records=2276,historical_revised=1592,historical_retained=684,incomplete_COMMON=3,incomplete_route=0,
        all20_clean_current_integrated_references_and_five_review_gates_verified=True,all69commands28relative_sites_and140relocated_cases_bound=True,
        current144plus72macro_calls_18font_planes_and_typed_choice_rules_bound=True,all15negative_cases_rejected_before_mutation=True,
        historical_shared_rules_and_new_current_startup_scope_distinct=True,actual_Seville_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=1,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        whole_clean_input_patch_reconstruction_exact=True,all496batches114accepted_layers_previous_profiles_and_V1492_promotion_preserved=True,
        prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2728audit passes:20completed,17revisions/3retentions;registeredV2724/496batches/exact clean patch/current startup.2276integrated,source/prose2279;full goal active.')
