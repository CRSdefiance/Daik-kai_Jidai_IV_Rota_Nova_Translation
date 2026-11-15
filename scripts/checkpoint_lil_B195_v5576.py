"""Checkpoint actual-approved B195 without credit and with an exact historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.checkpoint_lil_B195_v5559 import gates as original_native_gates,COUNTERS
from scripts.lil_B195_checkpoint_text_v5576 import NEXT,SUMMARY

ROOT=Path('work/analysis/lil_B195_checkpoint_v5576')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5577')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B195_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B195_editorial_relocation_map_v1.json')
APPROVAL=Path('work/analysis/lil_B195_reference_approval_v5575/approval_receipt.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5560/verified_handoff.json')
KEY='Lil_B195_reference_actual_v5576'
PREVIOUS='previous_latest_checkpoint_before_Lil_B195_v5576'
SCOPE='unfinished_editorial_scope_v5576'

def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE)
    return result

def gates():
    original,native_evidence=original_native_gates();doc,mapping,approval=map(read,[DOC,MAP,APPROVAL])
    assert approval['manuscripts'][str(DOC)]==sha(DOC.read_bytes())
    assert approval['reference_map_sha256']==sha(MAP.read_bytes())
    assert approval['all20_source_native_reference_and_representative_rules_approved'] and approval['new_editorial_credit']==0
    assert approval['registered_release_and_current_startup_pending']
    assert [r['english'] for r in doc['records']]==[r['english'] for r in original['records']]
    assert [r['compiled_hex'] for r in doc['records']]==[r['compiled_hex'] for r in original['records']]
    assert (doc['revised'],doc['retained'])==(3,17) and doc['registered_integration_pending']
    assert len(mapping['blocks'])==1 and mapping['blocks'][0]['block']==195
    assert len(mapping['blocks'][0]['command_map'])==23 and len(mapping['blocks'][0]['text_records'])==20
    actual=read(doc['postscene_native_state_proof'])
    assert actual['all79_complete_native_holds_and115_paired_nontext_samples_pass']
    assert actual['no_open_translation_specific_display_or_control_finding'] and not actual['visual_review_pending']
    assert actual['fixture_return_frames']==[7655,7657] and actual['all_content_jobs_terminal']
    assert actual['exact_timing_difference_counts']==dict(total=15,speech=13,control_or_end=2)
    assert len(actual['sampled_postscene_whole_RGB_differences_unmasked'])==4 and not actual['PRNG_equality']
    assert actual['whole_RGB_final9001_equal'] and all(actual['postscene9001_native_component_equality'].values())
    assert len(actual['all_actual_consumer_sheets_viewed'])==4 and len(actual['paired_full_screen_views'])==5
    assert all(s['viewed_after_image_return'] for s in actual['all_actual_consumer_sheets_viewed']+actual['paired_full_screen_views'])
    evidence={**native_evidence,str(DOC):sha(DOC.read_bytes()),str(MAP):sha(MAP.read_bytes()),str(APPROVAL):sha(APPROVAL.read_bytes()),
        str(PRIOR):sha(PRIOR.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes()),
        'scripts/lil_B195_checkpoint_text_v5576.py':sha(Path('scripts/lil_B195_checkpoint_text_v5576.py').read_bytes())}
    for data in [doc,mapping,approval,actual]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
        for k,v in data.items():
            if k.endswith('_sha256') and isinstance(data.get(k[:-7]),str):
                p=Path(data[k[:-7]])
                if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    for s in actual['all_actual_consumer_sheets_viewed']+actual['paired_full_screen_views']:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];evidence[s['path']]=s['sha256']
    prior=read(PRIOR)
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return doc,actual,evidence

def audit(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete'];gates();return new

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);phase=parser.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and all(k not in old for k in [KEY,PREVIOUS,SCOPE])
        doc,actual,evidence=gates()
        known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        fresh={historical_key(r) for r in doc['records']};assert len(known)==6135 and len(fresh)==20 and not known&fresh
        fields=['id','file_path','block','source_record_index','source_reference','source_hex','source_Japanese','source_complete_preamble_hex',
            'current_record_index','current_reference','current_hex','english','compiled_hex','editorial_decision','localization_note',
            'fresh_retained_wording_justification','native_layout_retention_reason','review','native_display_consumer','actual_B22_display_fixture_observed']
        records=[{k:r[k] for k in fields if k in r} for r in doc['records']]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scope_path=Path(old['unfinished_editorial_scope_v5559']['path'])
        assert sha(scope_path.read_bytes())==old['unfinished_editorial_scope_v5559']['sha256']
        scope=deepcopy(read(scope_path));scope['next_focus']=NEXT
        scope['historical_Lil_B195_native_only_before_v5576']=scope.pop('next_Lil_B195_native_approved_uncredited_v5559')
        scope['next_Lil_B195_reference_actual_approved_uncredited_v5576']=dict(manuscript=str(DOC),sha256=sha(DOC.read_bytes()),
            objects=20,revisions=3,retentions=17,uncredited=True,actual_display_and_normal_return_verified=True,
            registered_release_and_startup_pending=True,original_three_row_R17_retained_under_native_guard=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=records,
            revised=3,retained=17,approved_uncredited_objects=20,source_prose_or_completion_credit_added=0,
            source_native_relocation_reference_and_representative_actual_complete=True,
            remaining_gates=['atomic-compiler-and-meaningful-negative-checks','registered-cumulative-release','appropriate-regressions','clean-input-patch','fresh-current-startup'],
            actual_B195_content_in_disclosed_B22_fixture_observed=True,actual_natural_source_event195_activation_claimed=False,
            fresh_complete_native_holds=79,paired_nontext_samples=115,actual_consumer_sheets_viewed=4,paired_fullscreens_viewed=20,
            actual_fixture_return_frames=actual['fixture_return_frames'],timing_difference_counts=actual['exact_timing_difference_counts'],
            later_original_lower_A_indicator_RGB_difference_frames=[8410,8590,8770,8950],
            unequal_PRNG_seeds=actual['postscene9001_PRNG_seeds'],full_RAM_or_future_world_equivalence_claimed=False,
            new_research_ROMs=3,new_cold_boot_emulator_runs=2,total_frames=18002,all_jobs_terminal_and_reaped=True,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B195_reference_actual_approved_uncredited_objects=20,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5576: Twenty B195 actual display reviews approved;registered integration pending\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5576\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six actual-approved checkpoint targets staged;twenty approvals remain uncredited.')
    elif phase=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();plan=read(ROOT/'staged_checkpoint.json');audit(plan)
        save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_planned_and_evidence_hashes_exact=True,
            full_nested_inverse_recovers_every_historical_value=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False))
        print('Six targets and complete historical inverse pass.')
    elif phase=='apply':
        assert not (ROOT/'application_receipt.json').exists();plan=read(ROOT/'staged_checkpoint.json')
        assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());audit(plan)
        workspace=Path.cwd().resolve()
        for item in plan['files']:assert Path(item['target']).is_relative_to(workspace) and Path(item['planned']).is_relative_to(ROOT.resolve())
        for item in plan['files']:
            with Path(item['target']).open('r+b') as stream:
                stream.write(Path(item['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
        save(ROOT/'application_receipt.json',dict(all6_targets_exact=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False))
        print('Six audited actual-approved checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6135,source_prose=6138,revised=3871,retained=2264,SC2=4250,SC3=96,reviewed_routes=4536,completed_routes=4536,
            approved_uncredited_Lil_B195_objects=20,Lil_proposed_revisions=3,Lil_justified_retentions=17,
            all20_source_prose_native_reference_representative_actual_reviews_verified=True,
            final_stored_alignment_cases=80,fresh_actual_complete_native_holds=79,paired_nontext_samples=115,
            actual_consumer_sheets_viewed=4,paired_fullscreens_viewed=20,actual_B195_display_pending=False,
            registered_integration_and_current_startup_pending=True,main_V4701_preserved=True,
            new_editorial_credit=0,new_research_ROMs=3,new_cold_boot_emulator_runs=2,total_frames=18002,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5576 verified;V5531 current. Twenty actual-approved objects uncredited;registered integration pending;full goal active.')
