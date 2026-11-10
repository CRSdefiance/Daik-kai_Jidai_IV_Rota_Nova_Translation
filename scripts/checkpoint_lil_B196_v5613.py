"""Save36 uncredited B196 source objects with a complete historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B196_checkpoint_text_v5613 import NEXT,SUMMARY
from scripts.checkpoint_lil_B196_v5599 import gates as original_source_gates
ROOT=Path('work/analysis/lil_B196_checkpoint_v5613')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5614')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
GLOSS=Path('work/analysis/lil_B196_clean_context_v5589/all24_clean_exchange_six_choices_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5600/verified_handoff.json')
KEY='Lil_B196_native_review_v5613'
PREVIOUS='previous_latest_checkpoint_before_Lil_B196_v5613'
SCOPE='unfinished_editorial_scope_v5613'
COUNTERS=dict(records_editorially_completed=6155,records_with_source_and_prose_pass=6158,
    records_with_source_prose_drafts=6158,records_revised_and_integrated=3874,retained_wordings_editorially_completed=2281)
PROOFS={
 'voices':'work/analysis/lil_B196_voices_v5591/current207_catalog_eight_voices_and_six_source_selectors.json',
 'dispatch':'work/analysis/lil_B196_dispatches_v5592/all24_source_current_dispatches_FI1_and37_control_leaves.json',
 'entry':'work/analysis/lil_B196_entry_v5593/source_EV2_B196_action_dependency_and_native_getter_binding.json',
 'names':'work/analysis/lil_B196_names_v5594/twelve_original_progressive_and_catalogue_name_consumers.json',
 'branches':'work/analysis/lil_B196_branches_v5595/original_relative_skip_operand_proof.json',
 'controls':'work/analysis/lil_B196_controls_v5596/seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json',
 'special':'work/analysis/lil_B196_6003_ends_v5597/source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json',
 'source_names':'work/analysis/lil_B196_source_names_v5598/six_source_name_fields_twelve_current_consumers_and_literal_scope.json'}

def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE);return result

def gates():
    packet,evidence=original_source_gates()
    docpath=Path('translations/lil_B196_editorial_manuscript_v3.json');choicepath=Path('translations/lil_B196_choice_manuscript_v2.json')
    approvalpath=Path('work/analysis/lil_B196_native_approval_v5612/all36_source_prose_current_native_speech_choice_approval.json')
    doc,choice,approval=map(read,[docpath,choicepath,approvalpath])
    assert approval['manuscripts']=={str(p):sha(p.read_bytes()) for p in [docpath,choicepath]}
    assert approval['all36_five_source_context_localization_naturalness_formatting_gates_true']
    assert (approval['revised'],approval['retained'])==(15,21) and len(doc['records'])==24 and len(choice['records'])==12
    rows=doc['records']+choice['records']
    assert all(all(r['review'].values()) for r in rows) and not doc['formatting_review_pending'] and not choice['formatting_review_pending']
    assert sum(r['editorial_decision']=='revise' for r in rows)==15
    assert sum(r['editorial_decision']=='retain-wording' for r in rows)==21
    assert all(r['fresh_retained_wording_justification'] for r in rows if r['editorial_decision']=='retain-wording')
    assert len(approval['formatter_negatives'])==28 and len(approval['source_consumer_negative_controls'])==30
    assert approval['speech_processor_alignment_cases']==192 and approval['choice_selection_cancel_cases']==36 and approval['choice_current_and_reviewed_style_label_planes']==48
    assert Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B196_layout_v3.py')
    assert Path(doc['scoped_profile_module'])==Path('dk4tool/dialogue/lil_B196_profile_v2.py')
    wrap=read(doc['source_bound_wrap_retention_proof']);r74=next(r for r in doc['records'] if r['source_record_index']==74)
    assert r74['english']==wrap['exact_target'] and r74['compiled_hex']==wrap['retained_compiled_hex']
    assert len(r74['reviewed_ordinary_boundaries'])==3 and r74['reviewed_ordinary_boundaries']==wrap['exact_source_prose_boundaries']
    assert wrap['all24_words_source_controls_compiled_bytes_and_native_planes_unchanged'] and len(wrap['six_source_or_prose_changes_do_not_inherit_review'])==6
    assert (wrap['paragraph_ASCII_characters'],wrap['paragraph_words'])==(129,23)
    funds=read(doc['source_financial_context']);assert len(funds['cases'])==36 and funds['six_source_prices_match_six_exact_native_payment_amounts']
    terms=read(doc['actor_terminology_reconciliation']);assert terms['money_term']=='gold' and terms['stat_term']['English']=='Charm'
    assert terms['current_source_FI_expansion']=='Lil' and sum(len(p['cases']) for p in terms['native_FE_macro_pipelines'])==8
    assert len(approval['reviewed_sheets'])==3 and len(approval['reviewed_menu_sheets'])==6
    for s in approval['reviewed_sheets']+approval['reviewed_menu_sheets']:
        assert s['viewed_in_full_current_turn'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256']
        evidence[s['path']]=s['sha256']
    for data in [doc,choice,approval,wrap,funds,terms]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
        for k,v in data.items():
            if k.endswith('_sha256') and isinstance(data.get(k[:-7]),str):
                p=Path(data[k[:-7]])
                if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    extra=[docpath,choicepath,approvalpath,PRIOR,Path(__file__),Path('scripts/lil_B196_checkpoint_text_v5613.py'),
        Path('scripts/prove_lil_B196_funds_v5601.py'),Path('scripts/prepare_lil_B196_funds_v5601b.py'),
        Path('scripts/prove_lil_B196_funds_v5601b.py'),Path('scripts/prepare_lil_B196_layout_v5606.py'),
        Path('scripts/plan_lil_B196_layout_v5607.py'),Path('scripts/plan_lil_B196_layout_v5607b.py'),
        Path('scripts/verify_lil_B196_fonts_v5609.py'),Path('scripts/verify_lil_B196_fonts_v5609b.py'),
        Path('scripts/prove_lil_B196_choices_v5610.py'),Path('scripts/prove_lil_B196_choices_v5610b.py')]
    evidence.update({str(p):sha(p.read_bytes()) for p in extra})
    prior=read(PRIOR);assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    approved=deepcopy(packet);approved['records']=doc['records'];approved['typed_choice_records']=choice['records']
    return approved,evidence

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
        packet,evidence=gates();rows=packet['records']+packet['typed_choice_records']
        known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};fresh={historical_key(r) for r in rows}
        assert len(known)==6155 and len(fresh)==36 and not known&fresh
        fields=['id','file_path','block','kind','source_record_index','source_reference','source_hex','source_Japanese','source_complete_preamble_hex',
            'current_record_index','current_reference','current_hex','fresh_source_gloss','whole_exchange_note','command_offset','option_index','source_selector','english','compiled_hex','editorial_decision','localization_note','fresh_retained_wording_justification','review','reviewed_ordinary_boundaries','native_layout_retention_reason']
        records=[{k:r[k] for k in fields if k in r} for r in rows]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scopepath=Path(old['unfinished_editorial_scope_v5599']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5599']['sha256']
        scope=deepcopy(read(scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B196_source_only_before_v5613']=scope.pop('next_Lil_B196_source_bound_uncredited_v5599')
        scope['next_Lil_B196_native_approved_uncredited_v5613']=dict(
            speech_manuscript='translations/lil_B196_editorial_manuscript_v3.json',
            speech_manuscript_sha256=sha(Path('translations/lil_B196_editorial_manuscript_v3.json').read_bytes()),
            choice_manuscript='translations/lil_B196_choice_manuscript_v2.json',
            choice_manuscript_sha256=sha(Path('translations/lil_B196_choice_manuscript_v2.json').read_bytes()),
            objects=36,speeches=24,choice_labels=12,typed_choice_objects=6,revisions=15,retentions=21,
            uncredited=True,all_five_editorial_and_native_format_gates_true=True,
            actual_relocation_final_stored_reference_and_registered_release_pending=True,
            exact_R74_three_ordinary_wraps_with_all_words_native_guards_retained=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            native_approved_uncredited_objects=36,speech_objects=24,typed_choice_labels=12,typed_choice_objects=6,
            proposed_revisions=15,individually_justified_retentions=21,source_prose_or_completion_credit_added=0,
            all36_source_context_localization_naturalness_native_format_reviews_complete=True,
            speech_processor_alignments=192,choice_selection_cancel_cases=36,choice_style_label_planes=48,
            source_consumer_negatives=30,formatter_negatives=28,viewed_speech_sheets=3,viewed_menu_sheets=6,
            R74_exact_ordinary_boundaries_after_words=['the','must','can'],R74_paragraph_characters=129,R74_words=23,
            all24_words_compiled_bytes_and_native_planes_unchanged_by_ordinary_wrap_review=True,
            remaining_gates=['reversible119-command-relocation-including-six-menus-and52-relative-operands',
                'final-stored-speech-and-choice-native-checks','whole-native-load-entry-control-and-end-references',
                'representative-actual-display-menus-and-transitions','atomic-compiler-and-registered-cumulative-build',
                'clean-input-patch-and-current-startup'],
            actual_B196_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B196_native_approved_uncredited_objects=36,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5613: B196 contextual native reviews approved;36 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5613\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six native-review checkpoint targets staged;36 approvals remain uncredited.')
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
        print('Six audited native-review checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6155,source_prose=6158,revised=3874,retained=2281,SC2=4270,SC3=96,reviewed_routes=4556,completed_routes=4556,
            native_approved_uncredited_Lil_B196_objects=36,B196_speeches=24,B196_choice_labels=12,B196_menus=6,
            proposed_revisions=15,individually_justified_retentions=21,all36_five_gates_true=True,
            speech_processor_alignments=192,choice_selection_cancel_cases=36,choice_current_reviewed_style_label_planes=48,
            consumer_negatives=30,formatter_negatives=28,viewed_speech_sheets=3,viewed_menu_sheets=6,
            exact_R74_three_source_prose_bound_ordinary_wraps_all129_characters23_words_and_native_guards_retained=True,
            relocation_final_stored_references_actual_and_registered_release_pending=True,
            new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5613 verified;V5580 remains current.36 B196 native approvals uncredited;full editorial objective active.')
