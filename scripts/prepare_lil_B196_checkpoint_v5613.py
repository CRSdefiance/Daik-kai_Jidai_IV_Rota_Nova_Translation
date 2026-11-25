"""Prepare a lossless native-review checkpoint;all36 approvals stay uncredited."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_checkpoint_tools_v5613')
GATES='''def gates():
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
'''
SCOPE_BLOCK="""        scope['historical_Lil_B196_source_only_before_v5613']=scope.pop('next_Lil_B196_source_bound_uncredited_v5599')
        scope['next_Lil_B196_native_approved_uncredited_v5613']=dict(
            speech_manuscript='translations/lil_B196_editorial_manuscript_v3.json',
            speech_manuscript_sha256=sha(Path('translations/lil_B196_editorial_manuscript_v3.json').read_bytes()),
            choice_manuscript='translations/lil_B196_choice_manuscript_v2.json',
            choice_manuscript_sha256=sha(Path('translations/lil_B196_choice_manuscript_v2.json').read_bytes()),
            objects=36,speeches=24,choice_labels=12,typed_choice_objects=6,revisions=15,retentions=21,
            uncredited=True,all_five_editorial_and_native_format_gates_true=True,
            actual_relocation_final_stored_reference_and_registered_release_pending=True,
            exact_R74_three_ordinary_wraps_with_all_words_native_guards_retained=True)
"""
ENTRY="""        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
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
"""
VERIFY_BLOCK="""        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
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
"""
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/checkpoint_lil_B196_v5599.py');s=source.read_text(encoding='utf-8')
    a=s.index('def gates():');b=s.index('\ndef audit(',a)
    c=s.index("        scope['historical_Lil_B196_unread_lead");e=s.index("        inventory=ROOT/",c)
    f=s.index('        new[KEY]=dict(');g=s.index("        new[PREVIOUS]=",f)
    h=s.index("        save(VERIFY/'verified_handoff.json'")
    rows=derive(source,'scripts/checkpoint_lil_B196_v5613.py',{
        s[a:b]:GATES,s[c:e]:SCOPE_BLOCK,s[f:g]:ENTRY,s[h:]:VERIFY_BLOCK,
        'from scripts.lil_B196_checkpoint_text_v5599 import NEXT,SUMMARY':
        'from scripts.lil_B196_checkpoint_text_v5613 import NEXT,SUMMARY\nfrom scripts.checkpoint_lil_B196_v5599 import gates as original_source_gates',
        'checkpoint_v5599':'checkpoint_v5613','verification_v5600':'verification_v5614','verification_v5586':'verification_v5600',
        "KEY='Lil_B196_source_contracts_v5599'":"KEY='Lil_B196_native_review_v5613'",
        'before_Lil_B196_v5599':'before_Lil_B196_v5613',"SCOPE='unfinished_editorial_scope_v5599'":"SCOPE='unfinished_editorial_scope_v5613'",
        "old['unfinished_editorial_scope_v5585']":"old['unfinished_editorial_scope_v5599']",
        "'source_selector']":"'source_selector','english','compiled_hex','editorial_decision','localization_note','fresh_retained_wording_justification','review','reviewed_ordinary_boundaries','native_layout_retention_reason']",
        '## V5599: B196 clean exchange and native source contracts;36 uncredited objects':'## V5613: B196 contextual native reviews approved;36 uncredited objects',
        'handoff - V5599':'handoff - V5613',
        'Six source-contract checkpoint targets staged;36 objects remain unapproved/uncredited.':'Six native-review checkpoint targets staged;36 approvals remain uncredited.',
        'Six audited source-contract checkpoint files applied exactly.':'Six audited native-review checkpoint files applied exactly.'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_lossless_native_checkpoint.json',dict(derivation=rows,
        all_prior_root_and_nested_history_preserved_by_inverse=True,new_native_approved_objects=36,proposed_revisions=15,justified_retentions=21,
        no_editorial_or_completion_credit_added_by_preparation=True,no_ROM_or_emulator_change=True,full_goal_complete=False))
