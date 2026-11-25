"""Preserve the whole ledger inverse while crediting eleven integrated conditional/FI reviews once."""
import re
from collections import Counter
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B194_completion_tools_v5536')
GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all578_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V5478'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed']
    assert view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==93 and reg['all_negatives_reject_before_mutation']
    assert actual==transitions and actual['unique_actual_display_objects']==11 and actual['actual_panel_observations_across_setups']==20
    assert actual['actual_new_cold_boot_runs']==4 and actual['total_frames']==36004 and actual['all_content_jobs_terminal_and_reaped']
    assert [v['complete_native_holds'] for v in actual['versions']]==[35,44] and actual['sampled_nontext_pairs']==230
    assert actual['total_paired_fullscreen_views']==24 and actual['representative_actual_coverage_sufficient_for_this_distinct_display_scope']
    assert actual['no_open_translation_specific_display_or_control_finding'] and not actual['visual_review_pending']
    for index,v in enumerate(actual['versions']):
        assert v['return_frames']==[[5017,5017],[5737,5737]][index] and v['predicate_result']==index
        assert v['timing_differences']==dict(total=0,speech=0,control_or_end=0)
        assert v['sampled_postscene_and_final_RGB_equal'] and v['all_five_native_groups_and_whole1A04_actor_and_captain2_equal']
        assert v['final_PRNG_seeds']==[3723009301,3723009301]
        assert len(v['viewed_sheets'])==5 and all(s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in v['viewed_sheets'])
    tests=read('work/analysis/lil_B194_regressions_v5531/terminal.json')
    assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256']
    assert '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==578 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B194_retention_v5535/pin_receipt.json')['all_prior_pins_preserved']
    source=read(NEXT_SOURCE)
    assert len(source['records'])==20 and source['read_no_predecessor_English'] and source['new_review_credit']==0
    assert source['source_commands']==23 and source['source_stored_bytes']==712 and source['source_logical_end']==710
    return release

'''

if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B193_v5483.py');text=source.read_text(encoding='utf-8')
    a=text.index('def gates():');b=text.index('\ndef restore',a)
    c=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5442']['path']))")
    e=text.index("        for unit in inventory['broader_coverage_units']:",c)
    inventory="""        inventory=deepcopy(read(old['unfinished_editorial_scope_v5527']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B194_completed_v5536']=dict(final_review=str(FINAL),completed_objects=11,registered_candidate=release['candidate'],natural_event194_not_selected=True)
        inventory['historical_Lil_B194_reference_actual_before_completion_v5536']=inventory.pop('next_Lil_B194_reference_actual_approved_uncredited_v5527')
        inventory['next_Lil_B195_clean_only_v5540']=dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()),objects=20,uncredited=True,linear23_commands_no_macros_predicates_or_relatives=True)
"""
    changes={text[a:b]:GATES,text[c:e]:inventory,
        'B193':'B194','fifteen':'eleven','Fifteen':'Eleven','completion_v5483':'completion_v5536','verification_v5484':'verification_v5537',
        'release_v5479':'release_v5532','startup_v5481':'startup_v5534','registration_v5477':'registration_v5530',
        'work/analysis/lil_B193_actual_v5472/actual_all15_progressive_FE_A000_C200_and_single_end.json':
        'work/analysis/lil_B194_actual_views_v5525/both_unforced_paths_all11_panels24_fullscreens_and_normal_returns_viewed.json',
        'work/analysis/lil_B193_actual_review_v5473/all15_panels12_fullscreens_three_Ladies_return_and_measured_differences.json':
        'work/analysis/lil_B194_actual_views_v5525/both_unforced_paths_all11_panels24_fullscreens_and_normal_returns_viewed.json',
        'verification_v5443':'verification_v5528','B194_clean_context_v5488/all11':'B195_clean_context_v5540/all20',
        'Lil-B193-three-Ladies-cooking-reported-spice-price-concern-friendship-and-prospective-Seoul15':
        'Lil-B194-sake-rice-hearsay-causal-invitation-conditional-Julio-FI-personal-purchase-and-prospective-Hangzhou11',
        'editorial_scope_v5483':'editorial_scope_v5536','B193_v5483':'B194_v5536','completion_text_v5483':'completion_text_v5536',
        'all577':'all578','V5437':'V5478','regressions_v5478':'regressions_v5531','retention_v5482':'retention_v5535',
        "len(manifest['batches'])==577":"len(manifest['batches'])==578",'[-15:]':'[-11:]',
        "{'revise':8,'retain-wording':7}":"{'revise':4,'retain-wording':7}",'blocks[193]':'blocks[194]','block=193':'block=194','blocks=[193]':'blocks=[194]',
        '6109':'6124','6124':'6135','6127':'6138','3867':'3871','2257':'2264','4224':'4239','4239':'4250','4525':'4536',
        'revised=8':'revised=4','revised_count=8':'revised_count=4','fresh_revisions=8':'fresh_revisions=4','new_revisions=8':'new_revisions=4',
        'actual_matching_holds=59':'actual_matching_holds=79','all15':'all11','exactly15':'exactly11',
        '==15':'==11','=15':'=11','event193':'event194','source193':'source194',
        'batch_new_emulator_runs=4':'batch_new_emulator_runs=6','goal_turn_new_emulator_runs=4':'goal_turn_new_emulator_runs=2',
        'explicit_content_fixture_runs=2':'explicit_content_fixture_runs=4','batch_new_frames=39404':'batch_new_frames=57406','goal_turn_new_frames=39404':'goal_turn_new_frames=21402',
        "body=value[1:];assert not any(m in body for m in [b'FI',b'FA',b'FO'])":
        "body=value[1:];assert not any(m in body for m in [b'FA',b'FO'])\n            assert body.count(b'FI')==bytes.fromhex(row['source_hex']).count(b'FI')",
        "current_effective_runtime_English=body.decode('ascii')":"current_effective_runtime_English=body.replace(b'FI',b'Lil').decode('ascii')",
        "current_effective_paragraph=' '.join(body.decode('ascii').split())":"current_effective_paragraph=' '.join(body.decode('ascii').replace('FI','{MACRO:FI}').split())",
        'Lil_B194_clean_only_uncredited_objects=11':'Lil_B195_clean_only_uncredited_objects=20',
        '## V5483:':'## V5536:','cumulative V5478':'cumulative V5531','handoff - V5483':'handoff - V5536',
        'new_clean_only_Lil_B194_uncredited_objects=11':'new_clean_only_Lil_B195_uncredited_objects=20',
        'ten_speech_timings_and_measured_postscene_RGB_PRNG_scope_preserved':'two_unforced_paths_disclosed_original_setup_and_measured_timing_RGB_PRNG_scope_preserved',
        'V5478 integration verified;':'V5531 integration verified;','Eleven conditional B194 clean-only glosses pending':'Twenty B195 clean-only glosses pending',
        'previous_B193_objects_uncredited':'previous_B194_objects_uncredited',
    }
    assert all(k in text for k in changes)
    planned=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    compile(planned,'scripts/complete_lil_B194_v5536.py','exec')
    old,new=native_numbers(text),native_numbers(planned)
    assert old-new==Counter({463267532:2}) and new-old==Counter({3723009301:2})
    result=derive(source,'scripts/complete_lil_B194_v5536.py',changes)
    assert Path(result['successor']).read_text(encoding='utf-8')==planned
    ROOT.mkdir(parents=True);save(ROOT/'prepared_reversible_completion.json',dict(derivation=result,
        expected_completed=6135,expected_source_prose=6138,revisions=3871,retentions=2264,SC2=4250,routes=4536,
        new_disjoint_keys=11,next_clean_only=20,one_FI_raw_template_runtime_and_complete_paragraph_distinguished=True,
        all_partial_checkpoints_and_full_nested_ledger_inverse_preserved=True,full_goal_complete=False))
