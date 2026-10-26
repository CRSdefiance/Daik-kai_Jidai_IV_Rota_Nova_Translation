"""Independent32-record/ledger/source/native/release and retention audit."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_reaction_native_plan_v1484 import compiled,IDS
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2700')
CHECKPOINT=Path('work/analysis/battle_reactions_completion_v2699')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    beforepath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(beforepath)
    prior=read('work/analysis/editorial_handoff_verification_v2694/verified_handoff.json');assert sha(beforepath.read_bytes())==prior['ledger_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        backup=CHECKPOINT/(Path(p).name+'.before');assert sha((backup if backup.exists() else Path(p)).read_bytes())==digest,p
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    oldcompleted={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==completed and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2256
    assert completed-oldcompleted=={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS} and oldcompleted<=completed
    assert {(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}==keys
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2256,2256,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert Counter(p for p,n in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':429,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2256,1575,681)
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file'] and sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==3 and set(ledger['reviewed_but_incomplete_COMMON_IDs'])==set(before['reviewed_but_incomplete_COMMON_IDs'])-set(IDS)
    assert set(ledger['active_source_prose_drafts']['native_message_IDs'])==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert all(not set(IDS)&set(ns) for ns in ledger['active_source_prose_drafts']['manuscript_record_subsets_pending'].values())
    assert ledger['current_integrated_candidate']==before['current_integrated_candidate']
    dp=Path(fresh['latest_contextual_manuscript']);doc=read(dp);validate_natural_dialogue_batch(doc)
    final=read('translations/battle_reactions_contextual_final_review_v1.json');assert final['records']==doc['records']
    assert (final['new_completed_records'],final['revised_count'],final['retained_count'])==(32,0,32) and final['historical_decisions_newly_completed']=={'revised':16,'retained':16}
    assert final['actual_selected_reaction_IDs']==[] and final['new_emulator_runs']==0 and final['all_review_sheets_viewed']
    assert doc['all_three_review_sheets_viewed'] and not doc['formatting_review_pending'] and not doc['current_native_and_representative_reconciliation_pending']
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    rompath=Path(doc['current_ROM']);rom=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds')
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');en=current_entries(common,arm)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n=row['message_id'];assert n in IDS and all(row['review'].values()) and row['editorial_decision']=='retain-wording'
        assert row['source_meaning'] and row['localization_note']==row['fresh_retained_wording_justification']
        assert row['source_hex']==jp[n].text.hex() and row['source_reference']==ref(jp[n]) and row['source_Japanese']==jp[n].text.decode('cp932')
        assert row['current_reference']==row['integrated_reference']==ref(en[n])
        assert row['current_hex']==row['current_text_hex']==row['integrated_hex']==en[n].text.hex()==compiled(row).hex()
        assert row['current_English']==en[n].text.decode('ascii') and not en[n].text.startswith(b' ') and row['actual_selected_reaction_holds']==[] and row['individual_actual_activation_not_claimed']
    assert {en[n].block for n in IDS}=={23}
    manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);stage=manifest['relocations']['/COMMON/MESFILE.DK4']['battle_reaction_editorial']
    cp=Path(stage['release_config']);config=read(cp);mp=Path(config['manuscript'])
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and sha(mp.read_bytes())==config['dependencies'][config['manuscript']] and set(IDS)<=set(stage['proof']['native_IDs'])
    original={r['message_id']:r for r in read(mp)['records']};assert Counter(original[n]['editorial_decision'] for n in IDS)=={'revise':16,'retain':16}
    assert all(original[r['message_id']]['english']==r['english'] for r in doc['records'])
    font=read(doc['current_native_font_proof']);source=read(doc['native_context_proof'])
    assert len(source['voice_tables'])==4 and sum(len(t['all207_original_actor_choices']) for t in source['voice_tables'])==828
    assert len(font['cases'])==32 and font['findings']==[] and len(font['all64_current_cold_warm_copies'])==64
    assert len(font['invalid_compiler_inputs'])==14 and all(c['rejected'] for c in font['invalid_compiler_inputs'])
    assert {c['message_ID'] for c in font['cases']}==set(IDS)
    for c in font['cases']:
        n=c['message_ID'];assert c['compiled_hex']==c['loaded_template_hex']==c['native_pipeline']['input_hex']==en[n].text.hex()
        assert c['complete_native_and_independent_plane_equal'] and c['complete_ordered_glyphs_margins_blank_paper_and_bounds_pass'] and c['all_prior_formatted_bytes_lines_and_full_palette_plane_equal']
        assert c['weak_line_end_indices']==[] and not c['single_word_final_row'] and ' '.join(c['lines'])==en[n].text.decode('ascii')
        assert c['existing_actor_object_passed_directly_no_roster_fixture'] and c['original_actor_choice']['message_ID']==n
    assert all(row['native_argument_count']==0 and row['source_native_macros']==[] for row in doc['records'])
    assert font['all_executed_pipeline_instructions_current_exact_and_actor_models_unchanged'] and font['all_source_native_arguments_remain_zero']
    sample=read(doc['representative_reconciliation']);assert len(sample['reused_historical_holds'])==4 and len(sample['reused_negative_controls'])==9
    assert sample['actual_selected_reaction_IDs']==[] and sample['new_emulator_runs']==sample['new_RGB_execution']==0 and sample['historical_actual_IDs']==[2082,2138]
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['current_candidate_identical_to_completed_representative_proof']
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    release=read('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');registry=read('translations/release_stack.json')
    assert sha(rompath.read_bytes())==release['candidate_sha256']==receipt['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256'] and sha(manifestpath.read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']==receipt['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256'] and sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256'] and sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    assert len(manifest['batches'])==494 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/surrender_advice_registration_v2673/registration_receipt.json')['builder_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v2699']['path']);assert inventory['incomplete_COMMON_count']==3
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==3 and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    handoff=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V2699') and '2256 reread /2256 integrated-reconciled /zero pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2699',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),fresh_records=2256,fresh_integrated=2256,fresh_pending=0,new_completed_records=32,new_current_prose_revisions=0,fresh_retentions=32,historical_revised=1575,historical_retained=681,source_prose=2259,incomplete_COMMON=3,
        all32_exact_clean_current_registered_source_native_and_representative_scope_verified=True,native_original_pipeline_and_full_font_cases=32,old_full_palette_case_matches=32,native_copies=64,compiler_rejections=14,no_roster_fixtures=True,
        reused_historical_representative_RGB_holds=4,reused_negative_controls=9,actual_selected_reaction_IDs=[],new_emulator_runs=0,prior_ledger_and_updated_file_chains_verified=True,handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),candidate=str(rompath),candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],no_ROM_registry_builder_profile_manifest_or_patch_change=True,whole_clean_input_reconstruction_proof_still_bound=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2699audit passes:32new retentions/completions,2256fresh reconciled;32current native cases/64copies/14compiler controls;4historical RGBholds reused.2674ROM/patch unchanged;3incompleteCOMMON andwider objective remain.')
