"""Independent16retention/current-source/palette/sampling and unchanged release audit."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.ship_sinking_native_plan_v1330 import compiled
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2687')
CHECKPOINT=Path('work/analysis/ship_sinking_completion_v2686');IDS=set(range(2058,2074))

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    beforepath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(beforepath)
    prior=read('work/analysis/editorial_handoff_verification_v2680/verified_handoff.json');assert sha(beforepath.read_bytes())==prior['ledger_sha256']
    previousreceipt=read(prior['handoff_receipt'])
    for p,digest in previousreceipt['updated_files'].items():
        backup=CHECKPOINT/(Path(p).name+'.before');assert sha((backup if backup.exists() else Path(p)).read_bytes())==digest,p
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    oldcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==completed and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2200
    assert completed-oldcompleted=={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS} and oldcompleted<=completed
    assert {(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}==keys
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2200,2200,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert Counter(p for p,n in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1543,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2200,1535,665)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file'] and sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==59 and set(ledger['reviewed_but_incomplete_COMMON_IDs'])==set(before['reviewed_but_incomplete_COMMON_IDs'])-IDS
    assert set(ledger['active_source_prose_drafts']['native_message_IDs'])==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert all(not IDS&set(ns) for ns in ledger['active_source_prose_drafts']['manuscript_record_subsets_pending'].values())
    assert ledger['current_integrated_candidate']==before['current_integrated_candidate']
    dp=Path(fresh['latest_contextual_manuscript']);doc=read(dp);validate_natural_dialogue_batch(doc)
    fp=Path('translations/ship_sinking_contextual_final_review_v1.json');final=read(fp)
    assert final['records']==doc['records'] and final['new_completed_records']==16 and final['revised_count']==0 and final['retained_count']==16
    assert final['historical_decisions_newly_completed']=={'revised':8,'retained':8}
    assert final['actual_sinking_IDs']==[] and final['new_emulator_runs']==0 and final['all_review_sheets_viewed']
    assert doc['all_five_review_sheets_viewed'] and not doc['formatting_review_pending'] and not doc['current_native_and_representative_reconciliation_pending']
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    rompath=Path(doc['current_ROM']);rom=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');en=current_entries(common,arm)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n=row['message_id'];assert n in IDS and all(row['review'].values()) and row['editorial_decision']=='retain-wording'
        assert row['source_meaning'] and row['localization_note'] and row['fresh_retained_wording_justification']
        assert row['source_hex']==jp[n].text.hex() and row['source_reference']==ref(jp[n]) and row['source_Japanese']==jp[n].text.decode('cp932')
        assert row['current_reference']==row['integrated_reference']==ref(en[n])
        assert row['current_hex']==row['current_text_hex']==row['integrated_hex']==en[n].text.hex()==compiled(row).hex()
        assert row['current_English']==en[n].text[1:].decode('ascii') and row['actual_sinking_holds']==[] and row['individual_actual_activation_not_claimed']
    manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);stage=manifest['relocations']['/COMMON/MESFILE.DK4']['ship_sinking_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript'])
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['dependencies'][config['manuscript']]
    assert IDS<=set(stage['proof']['native_IDs'])
    original={r['message_id']:r for r in read(mp)['records']};assert Counter(original[n]['editorial_decision'] for n in IDS)=={'revise':8,'retain':8}
    assert all(original[r['message_id']]['english']==r['english'] for r in doc['records'])
    font=read(doc['current_native_font_proof']);source=read(doc['native_context_proof'])
    assert len(source['voice_tables'])==2 and sum(len(t['all207_original_actor_choices']) for t in source['voice_tables'])==414
    assert len(source['original_live_name_getters'])==5 and len({n['name_hex'] for n in source['original_live_name_getters']})==4
    assert len(source['original_actor_getter_argument_cases'])==12
    assert len(font['cases'])==496 and font['full_native_font_and_original_pipeline_cases']==496 and len(font['names'])==31
    assert len(font['all32_current_cold_warm_copies'])==32 and font['findings']==[]
    assert sum(c['matches_prior_full_native_case'] for c in font['cases'])==416 and font['additional_current_names_or_percent_cases']==80
    for c in font['cases']:
        n=c['message_ID'];argument=bytes.fromhex(c['name_case']['hex']);assert 0<len(argument)<=18
        assert c['compiled_hex']==c['loaded_template_hex']==en[n].text.hex()
        assert c['native_pipeline']['input_hex']==en[n].text.replace(b'%s',argument,1).hex()
        assert c['complete_native_and_independent_plane_equal'] and c['complete_ordered_glyphs_margins_blank_paper_and_bounds_pass']
        assert c['single_word_final_row'] is False and c['weak_line_end_indices']==[]
    assert len(font['original_speaker_fixtures'])==16
    for f in font['original_speaker_fixtures']:
        if f['message_ID']<2066:assert len(f['CPU_only_fixture']['one_roster_byte_changed'])==1 and f['CPU_only_fixture']['all_actor_objects_skills_RNG_and_other4MiB_bytes_exact']
        else:assert f['CPU_only_fixture']['existing_actor_object_passed_directly'] and f['CPU_only_fixture']['not_an_earned_gunner_assignment']
    palette=read(doc['palette_review']);assert len(palette['samples'])==4 and palette['binary_previews_are_coverage_masks_not_actual_ink_color']
    assert palette['colors']=={'0':[255,255,255],'1':[0,8,0],'15':[197,198,197]}
    assert all(s['whole_palette_plane_equals_previously_executed_native_SHA'] for s in palette['samples'])
    sample=read(doc['representative_reconciliation']);assert len(sample['historical_holds'])==4 and len(sample['negative_controls'])==9
    assert all(h['current_complete_native_ink_gray_shadow_and_blank_masks_equal'] and h['historical_other_family_not_a_sinking_or_current_visit'] for h in sample['historical_holds'])
    assert all(c['rejected'] for c in sample['negative_controls']) and sample['actual_sinking_IDs']==[] and sample['new_emulator_runs']==0
    assert sample['historical_actual_IDs']==[2082,2138] and sample['no_open_translation_specific_display_or_control_finding']
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    release=read('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');registry=read('translations/release_stack.json')
    assert sha(rompath.read_bytes())==release['candidate_sha256']==receipt['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256'] and sha(manifestpath.read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']==receipt['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256'] and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256'] and len(manifest['batches'])==494 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/surrender_advice_registration_v2673/registration_receipt.json')['builder_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v2686']['path']);assert inventory['incomplete_COMMON_count']==59
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs']) and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==59
    assert ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0 and ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    handoff=Path('docs/editorial_handoff_current.md').read_text();assert handoff.startswith('# Current editorial handoff - V2686')
    assert '2200 reread /2200 integrated-reconciled /zero pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2686',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        fresh_records=2200,fresh_integrated=2200,fresh_pending=0,new_completed_records=16,new_current_prose_revisions=0,fresh_retentions=16,
        historical_revised=1535,historical_retained=665,source_prose=2259,incomplete_COMMON=59,
        all16_exact_clean_current_registered_source_native_palette_and_representative_scope_verified=True,
        native_original_pipeline_and_full_font_cases=496,old_full_palette_case_matches=416,native_copies=32,
        historical_representative_RGB_holds=4,negative_controls=9,actual_sinking_IDs=[],new_emulator_runs=0,
        getter_argument_inputs_are_copied_CPU_values_not_all_earned_or_reachable_gun_positions=True,
        prior_ledger_and_updated_file_chains_verified=True,handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_ROM_registry_builder_profile_manifest_or_patch_change=True,whole_clean_input_reconstruction_proof_still_bound=True,
        all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V2686 audit passes:16new retentions,2200fresh reconciled;496current native cases,4fullRGB representative holds,9corruptions;2674ROM/patch unchanged.59incompleteCOMMON andwider objective remain open.')
