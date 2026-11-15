"""Require cumulative release, exact patch, own-ROM startup andnative contexts before credit."""
from pathlib import Path
from dk4tool.patch import papal_trade_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_final_paths_v7655 import SEALED,MAP,SEAL,ACTUAL,LATER,VIEW
from scripts.verify_village_wrap_v608 import read
RELEASE=Path('work/analysis/papal_trade_release_v7661/registered_release_verification.json')
START=Path('work/analysis/papal_trade_startup_verification_v7664c/own_ROM_three_NewGames_town_exact_prior_comparisons.json')
START_VIEW=Path('work/analysis/papal_trade_startup_view_v7665b/two_own_ROM_startup_sheets_viewed_scope_corrected.json')
REG=Path('work/analysis/papal_trade_registration_v7659/registration_receipt.json')
PIN=Path('work/analysis/papal_trade_release_pins_v7662/pin_receipt.json')
NATIVE=Path('work/analysis/current_V7660_native_v7665/registered_current_three_native_input_bindings.json')
LEAD=Path('work/analysis/maria_B207_metadata_lead_v7665c/17_uncredited_SC3B207_metadata_refs_clean_complete_exchange_review_pending.json')
def gates():
    r,s,v,reg,pin,native=map(read,[RELEASE,START,START_VIEW,REG,PIN,NATIVE])
    conf=read(story.CONFIG);seal=read(SEAL);actual=read(ACTUAL);later=read(LATER)
    assert r['all628_manifest_batches_and114_accepted_layers_present'] and r['all18_registered_release_checks_pass'] and r['all110_release_dialogue_regressions_pass'] and r['whole_clean_input_ROM_reconstruction_byte_exact'] and r['whole_ROM_equals_pinned_approved_reference']
    assert s['whole_RGB_frame_pairs']==40 and s['all_current_requested_andfinal_frames_equal_V7611'] and s['all_native_actor_andcaptain_controls_equal'] and s['source_anddisposable_town_donors_unchanged']
    assert v['viewed'] and v['startup_proof_sha256']==sha(START.read_bytes()) and v['actual_inherited_town_captain']==1 and v['town_frame3200_displays_Copenhagen']
    for sheet in v['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert reg['profile']=='all-routes-unified-v7660' and reg['negative_count']==148 and reg['all_negatives_reject_before_commit'] and pin['all_prior_pins_andROMs_preserved']
    tests=read('work/analysis/papal_trade_regressions_v7660/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==r[k+'_sha256']
    assert r['candidate_sha256']==s['candidate_sha256']==native['candidate_sha256']==sha(Path(r['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    assert native['actual_original_captain_IDs']==[0,1,2] and len(native['contexts'])==3
    for c in native['contexts']:assert c['all_strict2b6_COMMON_directory123264_payload_andactual_captain_guards_pass'] and sha(Path(c['input']).read_bytes())==c['input_sha256']
    registry=read('translations/release_stack.json');manifest=read(r['manifest'])
    assert len(manifest['batches'])==628 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    assert seal['all36_five_gates_andexact_references_approved'] and actual['total_actual_speech_occurrences']==72 and read(VIEW)['all72_complete_source_English_speech_panes_individually_viewed']
    assert [len(g['later_RGB_differences']) for g in later['groups']]==[3,53] and later['no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim']
    for path in SEALED.values():assert all(all(row['review'].values()) for row in read(path)['records'])
    assert read(LEAD)['source_current_coverage_overlap']==0 and read(LEAD)['old_English_bodies_not_exposed_orused_for_gloss_orlocalization']
    r['stage']=read('work/analysis/papal_trade_atomic_v7657/positive_reconstruction.json')
    assert len(r['stage']['changed_records'])==36 and r['stage']['one_files_list_commit_after_all_gates']
    return r
