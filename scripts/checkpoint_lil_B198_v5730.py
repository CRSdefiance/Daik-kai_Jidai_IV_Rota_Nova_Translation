"""Save B198's native-reviewed, uncredited whole exchange with a lossless historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B198_checkpoint_v5730')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5731')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5709/verified_handoff.json')
DOC=Path('translations/lil_B198_editorial_manuscript_v4.json')
KEY='Lil_B198_native_review_v5730'
PREVIOUS='previous_latest_checkpoint_before_Lil_B198_v5730'
SCOPE='unfinished_editorial_scope_v5730'
COUNTERS=dict(records_editorially_completed=6215,records_with_source_and_prose_pass=6218,
    records_revised_and_integrated=3905,retained_wordings_editorially_completed=2310)
SUMMARY=(
    'V5730 reviews all17 Lil SC2B198 speeches as one clean-Japanese Namahage encounter:12 revisions/'
    'five individually justified retentions. Restore both calls in each of two source refrain objects '
    '(four calls total),three repeated direct questions,Yukihisa\'s full identity challenge,questioning '
    'recognition of Namahage,qualified recollection of wrongdoing,acknowledgment,dream realization and '
    'prospective Admiral handover perhaps tomorrow morning. Keep Angelo\'s resumed present-tense '
    'question distinct from the dream. Retain his natural first outcry,Yukihisa\'s Huh?! and Strange '
    'things do happen.,and both complete CP932 silent pauses with individual reasons. Preserve '
    'Namahage cultural context without an explanatory lecture,Western monster substitution or invented '
    'ritual date,age,kinship,rank,room-sharing relationship,scene location,confirmed supernatural '
    'identity/cause or item powers. Spoken this remains unnamed despite the existing item card. '
    'Fresh clean name fields bind Yukihisa12 voice1 (progressive Yukihisa Shiraki/full Yukihisa Genjo '
    'Shiraki) and Angelo15 voice4 (Angelo Puccini). Six FE panels are an unattributed speaking voice, '
    'not an impersonal stat notice;retain the null-actor consumer. These name bindings are not new '
    'global name-localization completion credit. '
    'One complete Japanese-source cold boot13001 frames observes15 distinct speeches and source '
    'end540 returning at6697. Both original predicates return zero in this unforced initial-roster '
    'fixture,omitting Angelo65/95;those two clauses are reviewed offline with their full source '
    'nesting and are not claimed as actual captures. Five complete source sheets were viewed. '
    'The source scene changes from black upper screen to coastal/mountain backdrop before the '
    'dream realization. Existing UI shows Namahage Cleaver/Weapon/dash;this is contextual observation, '
    'not new item-title/widget fidelity approval or permission to add its title to speech. All37 '
    'source commands plus nine original B22 initializers are stored unchanged;conditions,roster, '
    'funds,RNG and effects are unforced. This is an initialized-Amsterdam B22 content fixture, '
    'not natural event198 activation,its original location,full route or hardware testing. '
    'Every reviewed English paragraph passes136 original processor alignment cases,11 complete '
    'progressive planes/six FE logical and physical planes,18 source-consumer negatives and28 '
    'formatter negatives. All three final native sheets were viewed. The first preview exposed '
    'a break after Any in the second repeated question;an exact B198 successor protects the '
    'any/naughty phrase. Each complete call now occupies its own row. Only those two compiled '
    'paragraphs change;all words,native metrics,widths,guards,pair phase,bounds and pagination '
    'remain unchanged. No authored break,fit-driven shortening or weak-boundary safety waiver. '
    'The handover uses two complete rows without losing perhaps or tomorrow morning. Both CP932 '
    'pauses pass exact native multibyte glyph/order/independent-plane checks. '
    'Offline relocation expands544 stored/logical bytes to644,retaining all37 commands,17 full '
    'preambles,eight relative spans/40 mapped native skip cases,two predicates,two A000 effects, '
    '6000/4500/633F/623F/4621/61FF/4835 and the sole source end540 mapped to640. Exact inverse '
    'recovers all544 predecessor bytes with zero source tailzeros;335 other SC2 blocks remain '
    'exact. All17 final stored targets pass68 alignments:28 fresh for seven parity tails and40 '
    'byte-identical reuse. Complete reviewed glyph planes remain exact with no blank page or lost '
    'character. Initial stopped control producers and the glyph event-schema failure are preserved; '
    'corrected source-locked successors passed. No English gameplay/reference seal/compiler/registered '
    'release approval is claimed. The17 objects remain uncredited until necessary gates pass. '
    'Coverage remains6215 completed/6218 source-prose/3905 integrated revisions/2310 retentions/ '
    'SC24330/SC396/routes4616/4616,zero pending credited route drafts. Registered cumulative '
    'experimental V5692 and its exact clean-input patch stay unchanged;main V4701 stays promoted. '
    'All earlier ROMs,translations,proofs,failures and historical values remain preserved. '
    'The full four-storyline,earlier-dialogue,town/shop/random,Help and remaining-prose objective, '
    'retrospective early wrapping and user-requested retrospective proper-name/role-label '
    'localization stay active. The207-entry name queue,paired164/165 Couple labels,Samwell full '
    'catalogue field and every earlier unresolved lead remain open. Graphics/all18 plaques and '
    'later older-record technical re-audit stay separate/open.'
)
NEXT=(
    'Continue B198 from native-approved manuscript v4,source-context5715,final native proof5723, '
    'approval5724,relocation5725 and stored-target proof5726. All17 objects remain uncredited. '
    'Next bind whole-image loading/external entries and relocated dispatches/original controls/end; '
    'use the retained complete Japanese source path as the focused English scene/transition comparison. '
    'Keep Angelo65/95 explicitly offline-only unless a practical source-faithful path is observed; '
    'do not force predicates,roster or results merely for exhaustive visitation. Resolve concrete '
    'changed-scene risks,then create the atomic source-locked compiler,registered cumulative '
    'candidate/exact clean-input patch and appropriate current startup checks;integrate once. '
    'Do not repeat sealed B197/previous-release checks without a concrete new risk. Continue the '
    'full editorial objective afterward,including the retrospective proper-name/role-label review '
    'and earlier premature wraps. Retain V5692 experimental/main V4701 and every prior artifact. '
    'No promotion,pruning,commit or push is part of this checkpoint.'
)


def inverse(value):
    result=deepcopy(value)
    result['latest_checkpoint']=result.pop(PREVIOUS)
    result.pop(KEY);result.pop(SCOPE)
    return result


def gates():
    doc=read(DOC);font=read(doc['native_font_proof'])
    approval_path=Path('work/analysis/lil_B198_native_approval_v5724/all17_source_prose_current_native_approval.json')
    approval=read(approval_path)
    planpath=Path('work/analysis/lil_B198_relocation_v5725/nested_source_relocation_research.json')
    storedpath=Path('work/analysis/lil_B198_stored_v5726/all17_final_stored_targets68_macro_cases_and_complete_planes.json')
    plan,stored=map(read,[planpath,storedpath])
    assert approval['manuscript_sha256']==plan['manuscript_sha256']==stored['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==17 and doc['revised']==12 and doc['retained']==5
    assert all(all(r['review'].values()) for r in doc['records'])
    assert font['current_original_macro_alignment_calls']==136
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(11,6)
    assert len(font['negative_controls'])==18 and len(approval['formatter_negatives'])==28
    assert len(approval['reviewed_sheets'])==3 and all(r['viewed_in_full_current_turn'] for r in approval['reviewed_sheets'])
    b=plan['blocks'][0]
    assert (b['source_bytes'],b['research_bytes'],b['source_logical_end'],b['research_logical_end'])==(544,644,544,644)
    assert len(b['command_map'])==37 and len(b['relative_skip_fixups'])==8 and len(b['target_native_skip_cases'])==40
    assert b['inverse_plus_original_zero_tailzeros_recovers_every_stored_source_byte']
    assert stored['current_final_stored_macro_alignment_cases']==68
    assert stored['new_parity_macro_alignment_cases']==28 and stored['exact_byte_identical_reused_macro_alignment_cases']==40
    context=read(doc['contextual_reconciliation'])
    assert context['actual_original_source_cold_boots']==1 and context['actual_source_frames']==13001
    assert context['actual_source_distinct_speeches']==15 and context['offline_only_conditional_source_indices']==[65,95]
    assert len(context['viewed_source_sheets'])==5 and all(r['viewed_in_full_current_turn'] for r in context['viewed_source_sheets'])
    paths={DOC,approval_path,planpath,storedpath,Path(__file__)}
    for key,value in doc.items():
        if key.endswith('_sha256') and isinstance(doc.get(key[:-7]),str) and Path(doc[key[:-7]]).is_file():
            p=Path(doc[key[:-7]]);assert sha(p.read_bytes())==value;paths.add(p)
    for r in approval['reviewed_sheets']+context['viewed_source_sheets']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['sha256'];paths.add(p)
    for data in [approval,plan,stored,context]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;paths.add(Path(p))
    for p in [Path('scripts/prove_lil_B198_controls_v5710.py'),Path('scripts/prove_lil_B198_controls_v5710b.py'),
        Path('scripts/verify_lil_B198_fonts_v5721.py')]:assert p.is_file();paths.add(p)
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
        old_scopepath=Path(old['unfinished_editorial_scope_v5708']['path'])
        assert sha(old_scopepath.read_bytes())==old['unfinished_editorial_scope_v5708']['sha256']
        scope=deepcopy(read(old_scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B198_clean_source_bound_before_v5730']=scope.pop('next_Lil_B198_clean_review_pending')
        scope['next_Lil_B198_native_approved_uncredited_v5730']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
            objects=17,revised=12,retained=5,source_context=doc['source_context'],actual_source_speeches=15,
            offline_only_conditional_source_indices=[65,95],native_alignments=136,final_stored_alignments=68,
            relocation_source_target_bytes=[544,644],all37_commands_and8_relative_spans_retained=True,
            external_references_relocated_controls_English_actual_atomic_compiler_registered_release_pending=True,
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
            native_approved_uncredited_objects=17,revised=12,retained=5,new_editorial_credit=0,new_ROMs=1,
            new_revised_English_ROMs=0,new_emulator_runs=1,actual_source_frames=13001,actual_source_speeches=15,
            offline_only_conditional_source_indices=[65,95],native_alignments=136,source_consumer_negatives=18,
            formatter_negatives=28,relocation_source_target_bytes=[544,644],source_commands=37,relative_sites=8,
            target_native_skip_cases=40,final_stored_alignments=68,
            remaining_gates=['whole-image-load-and-external-entry-reference-map','relocated-dispatch-controls-and-end',
                'focused-English-scene-transition-comparison','atomic-compiler-registered-release-clean-patch-current-startup'],
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            user_requested_names_scope_and_all_earlier_open_work_preserved=True,evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B198_native_approved_uncredited_objects=17,
            retrospective_names_and_role_labels_review_open=True,broader_full_editorial_goal_open=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5730: B198 whole-exchange native review;17 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V5730\n\n' if name=='editorial_handoff_current.md' else '')+section+NEXT+'\n\n'
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
                actual_source_cold_boots=1,actual_source_frames=13001,actual_source_speeches=15,
                offline_only_conditional_source_indices=[65,95],native_alignment_cases=136,final_stored_alignment_cases=68,
                all37_commands8_relative_spans40_target_skip_cases_and_exact544_byte_inverse=True,
                B198_reference_English_actual_compiler_registered_release_pending=True,
                retrospective207_name_queue_paired164_165_labels_and_full_broader_scope_preserved=True,
                all_sessions_terminal_and_reaped=True,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5731 verified:17 B198 native-reviewed/uncredited objects saved;V5692/main/counters unchanged. Full goal active.')
