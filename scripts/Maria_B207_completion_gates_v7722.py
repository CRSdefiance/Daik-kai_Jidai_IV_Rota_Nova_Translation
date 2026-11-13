"""Require complete registered release, exact patch andown-ROM controls before credit."""
from pathlib import Path
from dk4tool.patch import maria_B207_editorial_v2 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B207_final_paths_v7712 import SEALED,MAP,SEAL,ACTUAL,LATER,VIEW
from scripts.verify_village_wrap_v608 import read
RELEASE=Path('work/analysis/maria_B207_release_v7718/registered_release_verification.json')
START=Path('work/analysis/maria_B207_startup_verification_v7720/own_ROM_four_NewGames_town_exact_V7660_controls_andfour_strict_inputs.json')
START_VIEW=Path('work/analysis/maria_B207_startup_view_v7721/three_own_ROM_startup_sheets_viewed.json')
REG=Path('work/analysis/maria_B207_registration_v7716/registration_receipt.json')
PIN=Path('work/analysis/maria_B207_release_pins_v7718/pin_receipt.json')
NATIVE=START
def gates():
    r,s,v,reg,pin=map(read,[RELEASE,START,START_VIEW,REG,PIN]);conf=read(story.CONFIG);seal,actual,later=map(read,[SEAL,ACTUAL,LATER])
    assert r['all629_manifest_batches_and114_accepted_layers_present'] and r['all18_registered_release_checks_pass'] and r['all110_release_dialogue_regressions_pass'] and r['whole_clean_input_ROM_reconstruction_byte_exact'] and r['whole_ROM_equals_pinned_approved_reference']
    assert s['whole_RGB_frame_pairs']==47 and s['actual_frames']==33405 and s['all_current_requested_andfinal_frames_equal_V7660'] and s['all_native_actor_andcaptain_controls_equal'] and s['source_anddisposable_town_donors_unchanged']
    assert v['viewed'] and v['startup_proof_sha256']==sha(START.read_bytes()) and v['actual_inherited_town_captain']==1 and v['town_frame3200_displays_Copenhagen'] and v['all_five_jobs_terminal_andreaped']
    for sheet in v['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert reg['profile']=='all-routes-unified-v7717' and reg['negative_count']==163 and reg['all_negatives_reject_before_commit'] and pin['all_prior_pins_andROMs_preserved']
    tests=read('work/analysis/maria_B207_regressions_v7717/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(r[k]).read_bytes())==r[k+'_sha256']
    assert r['candidate_sha256']==s['candidate_sha256']==sha(Path(r['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    assert s['actual_NewGame_captains']==[0,1,2,3] and len(s['all_four_own_current_strict_native_contexts'])==4
    for c in s['all_four_own_current_strict_native_contexts']:assert c['strict2b6_COMMON_directory123264_payload_andownership_guards_pass'] and sha(Path(c['input']).read_bytes())==c['input_sha256']
    registry,manifest=read('translations/release_stack.json'),read(r['manifest'])
    assert len(manifest['batches'])==629 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    assert seal['all18_five_gates_andexact_references_approved'] and actual['total_actual_speech_occurrences']==36 and read(VIEW)['all36_complete_source_English_speech_panes_individually_viewed']
    assert len(later['groups'])==1 and len(later['groups'][0]['later_RGB_differences'])==104 and later['groups'][0]['later_sample_count']==123 and later['no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim']
    for path in SEALED.values():assert all(all(row['review'].values()) for row in read(path)['records'])
    r['stage']=read('work/analysis/maria_B207_atomic_v7714b/positive_reconstruction.json');assert len(r['stage']['changed_records'])==18 and r['stage']['one_files_list_commit_after_all_gates']
    return r
