"""Record36 uncredited source/current leads while preserving every earlier ledger value."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_SC0_SC1_checkpoint_v7622');VERIFY=Path('work/analysis/editorial_handoff_verification_v7623')
LEDGER=Path('translations/editorial_review_current_v1.json');PRIOR=Path('work/analysis/editorial_handoff_verification_v7618/verified_handoff.json')
CLEAN=Path('work/analysis/papal_trade_SC0_SC1_clean_v7619/two_complete_clean_exchanges36_refs_exact_Japanese_gloss_reuse_before_current_English.json')
CURRENT=Path('work/analysis/papal_trade_SC0_SC1_current_v7620/two_complete_current_exchanges36_source_current_refs_before_new_prose.json')
FINDINGS=Path('work/analysis/papal_trade_SC0_SC1_findings_v7621/all36_whole_exchange_raw_findings_andcandidate_retentions_native_consumers_pending.json')
KEY='papal_trade_SC0_SC1_source_current_lead_v7622';SCOPE='unfinished_editorial_scope_v7622'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed'];VALUES=(6801,6804,6804,4251,2550)
SUMMARY="""V7611 remains the current experimental registered cumulative image,with626 batches,114 accepted layers,18 passing release checks,110 release regressions,exact clean-input patch andown-current startup/native input. B234's18 integrated decisions remain credited once:14 revisions/four retentions. All completed counters stay6801 completed,6804 source-prose/drafts,4251 revisions,2550 retentions;SC2 4915 androutes5201/5201 are subsets,not full-goal completion. MainV4701 andall earlier ROMs,translations,producers,traces,proofs andfailures remain.

Both complete papal-trade source counterparts,SC0B246 andSC1B237,now have36 exact file-qualified clean/current references. Live6801-key comparison confirms all36 positions are uncredited. Their full clean1468-byte blocks,20 commands18 speeches each,complete0x68/0x13 preambles,A0001456/raw00a0ffff6a000110 andfour-byte end1464 match the prior B234 Japanese byte for byte. The earlier18 clean glosses are explicitly reused through exact whole-block/record equality before either other-route current English body is exposed;they are not relabeled as newly authored glosses ortranslated from English. Newsource orcompletion credit remains zero.

The current blocks also remain1468/logical1468/tail0. Complete current native command walks,source/current references,preambles,opaque operands andfull Japanese reconstruction bind every byte. The original EV0/EV1 files remain exact,buttheir route-specific event dependencies have not yet been interpreted. Raw storage isnot approved effective runtime text. Both full current exchanges havebeen read as exchanges only after all clean source/gloss bindings. Findings are stored in work/analysis/papal_trade_SC0_SC1_findings_v7621/all36_whole_exchange_raw_findings_andcandidate_retentions_native_consumers_pending.json. Both use This man in raw first-person speech;SC0 erases Filippo as friend,whileSC1 stores a full-width initial F in the name. These are raw wording/width leads,not proved parser causes orpermission to globally rename Trader. Other leads include excessive recovery certainty,lost aboard-ship fact,missing direct rule,shared-ancestry wording,invented lord-to-lord transfer,flattened great-grandfather envy,missing hearsay,possibly overstated relic wording,reported use changed to possessions,andmissing explicit if-found condition. Silence,warm recognition,short story question,cooperative decline andreflective religious response are only candidate retentions,with individual reasons andfinal decisions still pending.

No new English manuscript orformal localization/formatting approval exists for these36 records. Route-specific effective bodies,voice,getters,names/aliases,EV entry,display andregistered release remain pending. No other-route actual gameplay coverage,earned progress,natural activation,full effects orduplicate B234 credit is claimed. Preserve the complete four-storyline,earlier dialogue,shared shop/town,random,Help,remaining player prose,full207 name/role/alias andretrospective premature-wrap objective. All previous unresolved leads andcompleted-name history remain;graphics/all18 plaques andlater older-record technical re-audit stay separate. No separate unified test package,promotion,pruning,commit orpush. The full goal remains active."""
NEXT="""Continue from the two complete clean/current packets and36 raw findings above;do not repeat their source extraction orclaim fresh gloss authoring. Bind effective current bodies,voices,static19/104 name getters androute-specific EV0/EV1 entry against V7611's own strict input at work/analysis/current_V7611_native_v7616/current_native_input.json. Review whole exchanges andindividual retentions before authoring natural-dialogue-v2 American English. Preserve allsource facts,reported uncertainty,cultural religious context,Carlo/Filippo familiarity andthe explicit merchant great-grandfather;do not invent cause of recovery,kinship,rank,current city/date,trade route,authenticity,divine stat orguaranteed find. Use exact-input reuse of already validated native fonts/geometry where justified,andrepresentative gameplay/focused tests for distinct behavior orconcrete risks,with honest offline/actual scope. Integrate validated work through the full registered stack andexact clean-input patch;grant no duplicate credit. Preserve allfour storylines,remaining Lil blocks,earlier translations,shared town/shop,random,Help,remaining prose,all207 names/roles/aliases,retrospective early wraps,all unresolved inventory andlater graphics/technical work. MainV4701 andall existing artifacts remain;no automatic promotion,pruning,commit,push orseparate test package."""
def restore(value):
    out=deepcopy(value);entry=out.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def gates():
    prior,ledger,clean,current,findings=map(read,[PRIOR,LEDGER,CLEAN,CURRENT,FINDINGS])
    assert tuple(ledger[k] for k in COUNTERS)==VALUES and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    candidate=ledger['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert candidate['sha256']==prior['candidate_sha256']==sha(Path(candidate['path']).read_bytes()) and candidate['profile']=='all-routes-unified-v7611'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==626 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert clean['source_speech_references']==current['total_source_speeches']==findings['file_qualified_source_current_references']==len(findings['records'])==36 and clean['all36_source_positions_uncredited_in_live6801_ledger'] and current['source_packet_sha256']==sha(CLEAN.read_bytes()) and findings['current_source_packet_sha256']==sha(CURRENT.read_bytes())
    assert current['current_ROM_sha256']==findings['current_ROM_sha256']==candidate['sha256'] and all(not r['review']['formatting'] and not r['review']['localization'] and r['formal_editorial_decision'] is None for r in findings['records'])
    return prior,findings
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase;prior,findings=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256'];new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        scope=old['unfinished_editorial_scope_v7617'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'];inventory=deepcopy(read(scope['path']));inventory['next_focus']=NEXT
        inventory['papal_trade_SC0_SC1_source_current_findings_v7622']=dict(clean_packet=str(CLEAN),current_packet=str(CURRENT),findings=str(FINDINGS),file_qualified_positions=36,live6801_coverage_overlap=0,all_clean_gloss_bindings_precede_current_English=True,raw_findings_not_effective_runtime_orfinal_localization_approval=True,entry_names_native_actual_andrelease_pending=True,new_credit=0)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_broader_objective_andprior_leads_preserved=True,SC0B246_SC1B237_raw_source_current_leads36_uncredited=True,full_goal_complete=False))
        put(['formatting_watchlist','papal_trade_SC0_SC1_v7622'],dict(status='raw-source-current-findings-effective-consumers-andprose-pending',findings=str(FINDINGS),full_width_F_andfirst_person_raw_wording_leads_no_proved_runtime_cause=True,no_new_credit=True))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5201;put(['coverage_units',ri,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [CLEAN,CURRENT,FINDINGS,PRIOR,inv,Path('translations/release_stack.json'),Path(__file__)]}
        new[KEY]=dict(clean_packet=str(CLEAN),current_packet=str(CURRENT),findings=str(FINDINGS),records=deepcopy(findings['records']),file_qualified_source_current_refs=36,formal_approved_prose_decisions=0,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,current_ROM_all_families_andall_five_credit_counters_unchanged=True,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families'] and tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V7622: SC0B246/SC1B237 source-current findings pending native/prose review; V7611 current\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7622; V7611 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False));print('Six-target36-reference checkpoint staged;zero credits,current V7611/families/counters preserved.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,zero_credit=True,full_goal_complete=False));print('Deep inverse audit passes;all prior records,history,counters andROM refs recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False));print('Six audited36-reference pending targets applied;zero credit,V7611 unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,SC0B246_SC1B237_exact_source_current_refs36_uncredited=True,source_gloss_reuse_exact_Japanese_not_fresh_authoring=True,current_raw_wording_findings_effective_runtime_prose_entry_names_native_actual_release_pending=True,new_credit=0,next_SC0B246_SC1B237_clean_counterparts_current_English_context_native_entry_andrelease_unreviewed=False,historical_prior_next_flag_superseded_by_raw_storage_findings=True,pending_checkpoint=str(ROOT/'application_receipt.json'),full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified);print('V7622 verified:36 uncredited source/current leads;V7611/6801 completed unchanged.Full goal active.')
