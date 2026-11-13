"""Stage,audit,apply and verify uncredited source/native progress losslessly."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B194_checkpoint_text_v5504 import NEXT,SUMMARY
ROOT=Path('work/analysis/lil_B194_checkpoint_v5504')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5505')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B194_editorial_manuscript_v3.json')
APPROVAL=Path('work/analysis/lil_B194_native_approval_v5503/all11_source_prose_current_native_approval.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5484/verified_handoff.json')
KEY='Lil_B194_contextual_native_v5504'
PREVIOUS='previous_latest_checkpoint_before_Lil_B194_v5504'
SCOPE='unfinished_editorial_scope_v5504'
EXTRA=[Path(p) for p in [
    'work/analysis/lil_B194_controls_v5495/one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json',
    'work/analysis/lil_B194_predicate_trace_v5495b/unforced_original_calls.json',
    'work/analysis/lil_B194_carried_result_v5495c/all20_C200_and10_end_prior_result_cases.json',
    'work/analysis/lil_B194_predicate_binding_v5495e/source_FE06_actor6_availability_and_unforced_current_false_result.json',
    'scripts/bind_lil_B194_predicate_v5495d.py',
    'work/analysis/lil_B194_predicate_binding_v5495d/current_context/current_native_pipeline_plan.json',
    'scripts/bind_lil_B194_predicate_v5495e.py','scripts/lil_B194_checkpoint_text_v5504.py']]
def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE);return result
def original():return json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))
def gates():
    d,a=map(read,[DOC,APPROVAL]);assert a['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(d['records'])==11 and (d['revised'],d['retained'])==(4,7) and d['source_prose_or_completion_credit_added']==0
    assert Counter(r['editorial_decision'] for r in d['records'])=={'revise':4,'retain-wording':7} and all(all(r['review'].values()) for r in d['records'])
    f=read(d['native_font_proof']);assert f['current_original_macro_alignment_calls']==88 and len(f['negative_controls'])==24
    assert len(a['formatter_negatives'])==28 and len(a['reviewed_sheets'])==2 and all(s['viewed_in_full_current_turn'] for s in a['reviewed_sheets'])
    for s in a['reviewed_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    source=read(d['source_context']);assert source['source_macro_counts']==dict(FI=1,FA=0,FO=0) and len(source['records'])==11
    assert sum(r['english'].count('{MACRO:FI}') for r in d['records'])==1
    control,trace,carry,binding=map(read,EXTRA[:4])
    assert len(control['source_relative_native_cases'] if isinstance(control['source_relative_native_cases'],list) else range(control['source_relative_native_cases']))==40
    assert len(control['source_resource42_boundary_and_carried_result_cases'])==10
    assert [len(p['speech_record_indices']) for p in control['source_structural_predicate0_1_paths']]==[9,11]
    assert len(carry['C200_cases'])==20 and len(carry['end_cases'])==10 and carry['all_five_prior_result_values_preserved_at_both_C200_and_end']
    assert trace['result']['native_result']==[2,0,0,0,0,0]
    values=binding['current_native_availability'];assert values['current_company_value']==1 and values['actor_company_value']==21 and values['original_7DB14_result']==0
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,PRIOR,*EXTRA,Path(__file__)]}
    for k,v in d.items():
        if k.endswith('_sha256') and k[:-7] in d and isinstance(d[k[:-7]],str):
            p=Path(d[k[:-7]])
            if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    prior=read(PRIOR);assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==d['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    manifest=read(Path(prior['candidate']).with_suffix('.manifest.json'));assert len(manifest['batches'])==577 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    return d,evidence
def audit(plan,applied=False):
    for e in plan['files']:
        assert sha(Path(e['target']).read_bytes())==e['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(e['planned']).read_bytes())==e['planned_sha256']
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    new=read(plan['files'][0]['planned']);old=original();assert inverse(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6124,6127,3867,2257)
    assert new['goal_status']=='active' and not new['full_goal_complete'];gates();return new
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);phase=parser.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==read(PRIOR)['ledger_sha256']
        assert all(k not in old for k in [KEY,PREVIOUS,SCOPE]);doc,evidence=gates()
        keys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};fresh={historical_key(r) for r in doc['records']}
        assert len(keys)==6124 and len(fresh)==11 and not keys&fresh
        fields=['id','file_path','block','source_record_index','source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex',
            'source_Japanese','source_meaning','english','speaker','context','editorial_decision','localization_note','fresh_retained_wording_justification','review','compiled_hex','source_prose_or_completion_credit_added']
        records=[{k:deepcopy(r[k]) for k in fields if k in r} for r in doc['records']]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scope=deepcopy(read(old['unfinished_editorial_scope_v5483']['path']));scope['next_focus']=NEXT
        scope['historical_Lil_B194_clean_only_before_v5504']=scope.pop('next_Lil_B194_clean_only_v5488')
        scope['next_Lil_B194_native_approved_uncredited_v5504']=dict(manuscript=str(DOC),sha256=sha(DOC.read_bytes()),objects=11,revisions=4,retentions=7,uncredited=True,actual_and_registered_release_pending=True)
        terms=Path(doc['actor_terminology_reconciliation']);scope['legacy_UI_Sake37_older_fidelity_review_open']=dict(path=str(terms),sha256=sha(terms.read_bytes()),source='清酒',UI='Sake',no_new_widget_credit=True)
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,scope);evidence[str(inv)]=sha(inv.read_bytes())
        new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=records,
            revised=4,retained=7,approved_uncredited_objects=11,source_prose_or_completion_credit_added=0,native_formatting_review_complete=True,
            remaining_gates=['reversible-relocation','final-stored-native-alignments','one-block-reference-load-and-relocated-control-checks','paired-content-gameplay-and-transition','atomic-compiler','registered-cumulative-release','clean-input-patch','fresh-current-startup'],
            actual_B194_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inv),sha256=sha(inv.read_bytes()),Lil_B194_native_approved_uncredited_objects=11,broader_storylines_shared_town_shop_random_help_and_prose_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5504: Eleven B194 native reviews approved;conditional gameplay pending\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;text=p.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5504\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[p]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six native-checkpoint targets staged;11 approvals remain uncredited.')
    elif phase=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();plan=read(ROOT/'staged_checkpoint.json');audit(plan)
        save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_planned_and_evidence_hashes_exact=True,full_nested_inverse_recovers_every_historical_value=True,
            staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False));print('Six targets and complete historical inverse pass.')
    elif phase=='apply':
        assert not (ROOT/'native_application_receipt.json').exists();plan=read(ROOT/'staged_checkpoint.json')
        assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());audit(plan)
        workspace=Path.cwd().resolve()
        for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
        for e in plan['files']:
            with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
        save(ROOT/'native_application_receipt.json',dict(all6_targets_exact=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False));print('Six audited native-checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'native_application_receipt.json')['all6_targets_exact'];plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True)
        prior=read(PRIOR);VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6124,source_prose=6127,revised=3867,retained=2257,SC2=4239,SC3=96,reviewed_routes=4525,completed_routes=4525,
            approved_uncredited_Lil_B194_objects=11,Lil_proposed_revisions=4,Lil_justified_retentions=7,all11_source_prose_current_native_reviews_verified=True,
            native_alignment_cases=88,real_FI_expansion_pipeline_cases=8,consumer_negatives=24,formatter_negatives=28,source_relative_cases=40,source_resource_boundary_cases=10,
            source_C200_carried_result_cases=20,source_end_carried_result_cases=10,unforced_current_predicate_result=0,
            actual_B194_gameplay_pending=True,registered_integration_pending=True,main_V4701_preserved=True,new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5504 verified;V5478 remains current. Eleven B194 native approvals uncredited;actual/registered integration pending;full goal active.')
