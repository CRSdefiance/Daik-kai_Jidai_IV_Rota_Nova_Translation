"""Stage,audit,apply and verify uncredited twenty-object progress with a complete historical inverse."""
import argparse
import gzip
import json
import os
import struct
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save
from scripts.lil_B195_checkpoint_text_v5559 import NEXT, SUMMARY

ROOT=Path('work/analysis/lil_B195_checkpoint_v5559')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5560')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/lil_B195_editorial_manuscript_v3.json')
APPROVAL=Path('work/analysis/lil_B195_native_approval_v5557/all20_source_prose_current_native_approval.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5537/verified_handoff.json')
RETENTION=Path('work/analysis/lil_B195_R17_guarded_rows_v5558/all11_two_row_splits_rejected_original_three_rows_retained.json')
KEY='Lil_B195_contextual_native_v5559'
PREVIOUS='previous_latest_checkpoint_before_Lil_B195_v5559'
SCOPE='unfinished_editorial_scope_v5559'
COUNTERS=dict(records_editorially_completed=6135,records_with_source_and_prose_pass=6138,
              records_revised_and_integrated=3871,retained_wordings_editorially_completed=2264)


def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE)
    return result


def gates():
    doc,approval,retention=map(read,[DOC,APPROVAL,RETENTION])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==20 and (doc['revised'],doc['retained'])==(3,17) and doc['source_prose_or_completion_credit_added']==0
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':3,'retain-wording':17}
    assert all(all(r['review'].values()) for r in doc['records']) and not doc['formatting_review_pending']
    font=read(doc['native_font_proof'])
    assert font['current_original_macro_alignment_calls']==160 and len(font['cases'])==20 and len(font['negative_controls'])==20
    assert len(approval['formatter_negatives'])==28 and len(approval['reviewed_sheets'])==3
    assert all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['reviewed_sheets'])
    source=read(doc['source_context'])
    assert len(source['records'])==20 and source['source_macro_counts']==dict(FI=0,FA=0,FO=0)
    assert source['source_static_actor_selectors']==[92,103,119] and len(source['blocks'][0]['all_current_native_commands'])==23
    assert [(c['offset'],c['whole_command_hex']) for c in source['blocks'][0]['all_current_native_commands'] if c['word']!=0x4000]==[
        (8,'00a0ffff010841a1'),(704,'00c2'),(706,'00000000')]
    assert retention['all11_two_row_splits_fail_unchanged_native_lint'] and retention['no_ordinary_boundary_exception_adopted']
    assert retention['paragraph_ASCII_characters']==68 and retention['selected_formatter_unchanged']
    assert retention['all20_paragraphs_compiled_bytes_and_current_native_planes_unchanged']
    assert len(retention['all_complete_word_two_row_splits'])==11
    row=next(r for r in doc['records'] if r['source_record_index']==17)
    assert row['native_layout_retention_reason']==retention['retention_reason'] and row['compiled_hex']==retention['retained_compiled_hex']
    assert row['english']==retention['exact_logical_prose'] and not row.get('reviewed_ordinary_boundaries')
    assert Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B195_layout_v1.py')
    terms=read(doc['actor_terminology_reconciliation'])
    assert terms['approved_prose_names']=={'92':'Barkeep','103':'Patron','119':'Port Worker'}
    assert terms['commodity_index']==8 and terms['commodity']=='Cheese' and terms['city']=='Veracruz'
    assert len(terms['two_source_current_city_aliases'])==2 and terms['Cheese8_older_UI_fidelity_review_stays_open_separate_from_dialogue']
    paths=[DOC,APPROVAL,RETENTION,PRIOR,Path('scripts/lil_B195_checkpoint_text_v5559.py'),Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    for data in [doc,retention]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
        for k,v in data.items():
            if k.endswith('_sha256') and isinstance(data.get(k[:-7]),str):
                p=Path(data[k[:-7]])
                if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    prior=read(PRIOR)
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    manifest=read(Path(prior['candidate']).with_suffix('.manifest.json'))
    assert len(manifest['batches'])==578 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json')
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return doc,evidence


def audit(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))
    new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete']
    gates();return new


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);phase=parser.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and all(k not in old for k in [KEY,PREVIOUS,SCOPE])
        doc,evidence=gates()
        known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        fresh={historical_key(r) for r in doc['records']};assert len(known)==6135 and len(fresh)==20 and not known&fresh
        fields=['id','file_path','block','source_record_index','source_reference','source_hex','source_Japanese','source_complete_preamble_hex',
                'current_record_index','current_reference','current_hex','english','compiled_hex','editorial_decision','localization_note',
                'fresh_retained_wording_justification','native_layout_retention_reason','review']
        records=[{k:r[k] for k in fields if k in r} for r in doc['records']]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scope_path=Path(old['unfinished_editorial_scope_v5536']['path'])
        assert sha(scope_path.read_bytes())==old['unfinished_editorial_scope_v5536']['sha256']
        scope=deepcopy(read(scope_path));scope['next_focus']=NEXT
        scope['historical_Lil_B195_clean_only_before_v5559']=scope.pop('next_Lil_B195_clean_only_v5540')
        scope['next_Lil_B195_native_approved_uncredited_v5559']=dict(manuscript=str(DOC),sha256=sha(DOC.read_bytes()),
            objects=20,revisions=3,retentions=17,uncredited=True,actual_and_registered_release_pending=True,
            original_three_row_R17_retained_under_native_guard=True,stopped_two_row_exploration_not_approved=True)
        terms=Path(doc['actor_terminology_reconciliation'])
        scope['legacy_UI_Cheese8_older_fidelity_review_open']=dict(path=str(terms),sha256=sha(terms.read_bytes()),source='チーズ',UI='Cheese',no_new_widget_credit=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=records,
            revised=3,retained=17,approved_uncredited_objects=20,source_prose_or_completion_credit_added=0,
            native_formatting_review_complete=True,original_formatter_retained=True,
            source_bound_R17_layout_retention_proof=str(RETENTION),source_bound_R17_layout_retention_proof_sha256=sha(RETENTION.read_bytes()),
            remaining_gates=['reversible-relocation','final-stored-native-alignments','one-block-reference-load-and-relocated-control-checks',
                             'paired-content-gameplay-and-transition','atomic-compiler','registered-cumulative-release','clean-input-patch','fresh-current-startup'],
            actual_B195_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B195_native_approved_uncredited_objects=20,
            broader_storylines_shared_town_shop_random_help_and_prose_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5559: Twenty B195 native reviews approved;three-row guard retained;gameplay pending\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5559\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six native-checkpoint targets staged;twenty approvals remain uncredited.')
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
        print('Six audited native-checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6135,source_prose=6138,revised=3871,retained=2264,SC2=4250,SC3=96,reviewed_routes=4536,completed_routes=4536,
            approved_uncredited_Lil_B195_objects=20,Lil_proposed_revisions=3,Lil_justified_retentions=17,
            all20_source_prose_current_native_reviews_verified=True,native_alignment_processor_cases=160,source_name_macro_occurrences=0,
            consumer_negatives=20,formatter_negatives=28,all11_R17_two_row_splits_rejected_unchanged_native_guards=True,
            original_v1_formatter_and_all_words_compiled_bytes_planes_retained=True,ordinary_boundary_exception_adopted=False,
            actual_B195_gameplay_pending=True,registered_integration_pending=True,main_V4701_preserved=True,
            new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5559 verified;V5531 remains current. Twenty native approvals uncredited;actual/registered integration pending;full goal active.')
