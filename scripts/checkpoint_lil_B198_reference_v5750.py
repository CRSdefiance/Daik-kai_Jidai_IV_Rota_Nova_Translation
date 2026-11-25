"""Save B198's native-reviewed, uncredited whole exchange with a lossless historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B198_reference_checkpoint_v5750')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5751')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5731/verified_handoff.json')
DOC=Path('translations/lil_B198_editorial_manuscript_v6.json')
KEY='Lil_B198_reference_review_v5750'
PREVIOUS='previous_latest_checkpoint_before_Lil_B198_reference_v5750'
SCOPE='unfinished_editorial_scope_v5750'
COUNTERS=dict(records_editorially_completed=6215,records_with_source_and_prose_pass=6218,
    records_revised_and_integrated=3905,retained_wordings_editorially_completed=2310)
from scripts.lil_B198_reference_checkpoint_text_v5750 import SUMMARY,NEXT


def inverse(value):
    result=deepcopy(value)
    result['latest_checkpoint']=result.pop(PREVIOUS)
    result.pop(KEY);result.pop(SCOPE)
    return result


def gates():
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


def audit(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
        assert sha(gzip.decompress(Path(item['before']).read_bytes()))==item['before_sha256']
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()))
    new=read(plan['files'][0]['planned']);assert inverse(new)==old
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete']
    prior=read(PRIOR)
    assert prior['ledger_sha256']==plan['files'][0]['before_sha256']
    for key in ['candidate','patch']:assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    gates();return new


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);phase=parser.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and all(k not in old for k in [KEY,PREVIOUS,SCOPE])
        doc,evidence=gates()
        known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        fresh={historical_key(r) for r in doc['records']}
        assert len(known)==6215 and len(fresh)==17 and not known&fresh
        old_scopepath=Path(old['unfinished_editorial_scope_v5730']['path'])
        assert sha(old_scopepath.read_bytes())==old['unfinished_editorial_scope_v5730']['sha256']
        scope=deepcopy(read(old_scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B198_native_approved_before_v5750']=scope.pop('next_Lil_B198_native_approved_uncredited_v5730')
        scope['next_Lil_B198_reference_approved_uncredited_v5750']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
            objects=17,revised=12,retained=5,source_context=doc['source_context'],actual_source_speeches=15,
            offline_only_conditional_source_indices=[65,95],native_alignments=136,final_stored_alignments=68,
            relocation_source_target_bytes=[544,644],all37_commands_and8_relative_spans_retained=True,
            atomic_compiler_registered_release_clean_patch_and_current_startup_pending=True,
            uncredited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
        ROOT.mkdir(parents=True);inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope)
        evidence[str(inventory)]=sha(inventory.read_bytes());evidence[str(old_scopepath)]=sha(old_scopepath.read_bytes())
        fields=['id','file_path','block','kind','source_record_index','source_reference','source_hex','source_Japanese',
            'source_complete_preamble_hex','current_record_index','current_reference','current_hex','fresh_source_gloss',
            'whole_exchange_note','source_selector','english','compiled_hex','editorial_decision','localization_note',
            'fresh_retained_wording_justification','review','native_layout_retention_reason','qa_waivers','qa_waiver_reason',
            'actual_source_paths','actual_source_fixture_observed']
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
            records=[{k:r[k] for k in fields if k in r} for r in doc['records']],
            native_approved_uncredited_objects=17,revised=12,retained=5,new_editorial_credit=0,new_ROMs=2,
            new_revised_English_ROMs=1,new_emulator_runs=1,actual_source_frames=13001,actual_source_speeches=15,actual_English_frames=13001,actual_English_speeches=15,actual_native_holds=56,total_source_English_frames=26002,
            offline_only_conditional_source_indices=[65,95],native_alignments=136,source_consumer_negatives=18,
            formatter_negatives=28,relocation_source_target_bytes=[544,644],source_commands=37,relative_sites=8,
            target_native_skip_cases=40,final_stored_alignments=68,
            remaining_gates=['atomic-compiler-semantic-negatives-before-mutation','registered-release-clean-patch-current-startup'],
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            user_requested_names_scope_and_all_earlier_open_work_preserved=True,evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B198_native_approved_uncredited_objects=17,
            retrospective_names_and_role_labels_review_open=True,broader_full_editorial_goal_open=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5750: B198 reference and English scene approved;17 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V5750\n\n' if name=='editorial_handoff_current.md' else '')+section+NEXT+'\n\n'
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz'
            planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
            files.append(dict(target=str(target.resolve()),before=str(backup.resolve()),before_sha256=sha(target.read_bytes()),
                planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six files staged:all17 native-reviewed source/current decisions;no credit. Full names scope and historical inverse preserved.')
    else:
        planpath=ROOT/'staged_checkpoint.json';plan=read(planpath)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();audit(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(planpath.read_bytes()),
                all_before_planned_and_evidence_hashes_exact=True,full_nested_historical_inverse_exact=True,full_goal_complete=False))
            print('Six-file preapplication audit passes;all historical root/nested values recover exactly.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(planpath.read_bytes());audit(plan)
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(Path.cwd().resolve()) and Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as stream:
                    stream.write(Path(item['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all6_targets_exact=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False))
            print('Six audited B198 checkpoint files applied;17 reviewed objects remain uncredited.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
            audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],
                candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],
                all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,**COUNTERS,
                completed=6215,source_prose=6218,revised=3905,retained=2310,SC2=4330,SC3=96,reviewed_routes=4616,completed_routes=4616,
                native_approved_uncredited_Lil_B198_objects=17,pending_B198_revisions=12,pending_B198_retentions=5,
                actual_source_cold_boots=1,actual_source_frames=13001,actual_source_speeches=15,actual_English_frames=13001,actual_English_speeches=15,actual_native_holds=56,total_source_English_frames=26002,
                offline_only_conditional_source_indices=[65,95],native_alignment_cases=136,final_stored_alignment_cases=68,
                all37_commands8_relative_spans40_target_skip_cases_and_exact544_byte_inverse=True,
                B198_references_and_English_actual_approved=True,B198_atomic_compiler_registered_release_and_startup_pending=True,
                retrospective207_name_queue_paired164_165_labels_and_full_broader_scope_preserved=True,
                all_sessions_terminal_and_reaped=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5751 verified:17 B198 reference/gameplay-approved objects saved uncredited;V5692/main/counters unchanged. Full goal active.')
