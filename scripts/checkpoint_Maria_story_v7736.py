"""Reversible full-scope pending checkpoint; no ROM, registration or credit changes."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_checkpoint_v7736')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7737')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7723/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v2.json')
NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v1.json')
SOURCE=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
GLOSS=Path('work/analysis/maria_story_chain_gloss_v7726/all67_clean_whole_exchange_glosses_before_current_English.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
CONSUMERS=Path('work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json')
NATIVE_NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
ENTRY=Path('work/analysis/maria_story_entries_predicates_v7731/three_original_EV3_getters_ten_source_current_predicates.json')
LOGICAL=Path('work/analysis/maria_story_logical_v7732/67_logical_paragraphs268_original_native_macro_literal_alignments.json')
PLANS=Path('work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json')
KEY='Maria_SC3B34_B108_B35_contextual_pending_v7736'
SCOPE='unfinished_editorial_scope_v7736'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6855,6858,6858,4290,2565)
NEXT="""Continue the full four-storyline contextual goal from the unintegrated Maria B34/B108/B35 v2 draft and V7717 own-ROM captain3 context. Do not repeat unchanged clean inventories/glosses,67 source/current mappings,134 dispatches,16 getters,80 source/default macro alignments,three event getters,ten predicates or268 final logical alignments. Final logical coverage is256 exact own-current reused alignments plus12 fresh changed-paragraph alignments;the original v1's268 remain. Next bind every compiled paragraph through four native alignments and original font/page renderers,complete first/internal/final glyphs,bounds andpagination,including B108 R111's five-row/two-page plan. Review actual full-width output rather than shortening meaning or silently waiving layout findings. Preserve scoped216x64/four-row geometry,FA2/FI5/FO7 andall source selectors/macros. Resolve the shared actor155 Sailor/Retainer mismatch through broader151–159 consumers before choosing orchanging a label;the seven other names arecontextual retentions,not full catalogueUI approval. Complete exact nested0100 andrelative0200/0300 branch/relocation proofs,original UI setup/waits/A000/C200 controls,source header/loader/caller bindings andrepresentative source/English actual scene transitions andfocused concrete risks. Original event dependency chain34->108->35 doesnot prove immediate chronology,natural eligibility,all branch playback,earned unlock orfull effects. Then freeze policy,stored/reference/inverse,atomic production/challenges andregistered cumulative integration/exactclean patch workflow;credit only after necessarychecks pass. Keep every prior family,all other storylines/earlier translated exchanges,shared town/shop/random practical broad capture,Help/player prose,all207 names/roles/aliases andretrospective earlywrap leads active. Graphics/all18 plaques andlater older-record technical re-audit stayseparate. Preserve every ROM,translation,draft,executed producer,failure,proof andtrace. MainV4701 remains;no separate unified test package,automatic promotion,pruning,commit orpush."""
SUMMARY="""V7717 remains the registered experimental cumulative ROM:629 batches,114 accepted layers,18 release checks,110 regressions andthe exactly reconstructable clean-input patch. Counts stay6855 completed/6858 source-prose anddrafts/4290 integrated revisions/2565 retentions;SC0 135,SC1 91,SC2 4915,SC3 114 andCOMMON1600 completed/1603 source-prose remain. Route5255/5255 is a subset,not full-goal completion. This checkpoint adds67 uncredited Maria draft positions andchanges no ROM,registry,completed family orcredit counter. MainV4701 andthe full editorial objective remain.

The complete clean Japanese ofSC3B34(8 speeches),B108(31) andB35(28) wasread andfreshly glossed before anycurrent English. Exact originalEV3 prerequisites bind34->108->35;additional predicates,scheduling,elapsed time,intervening events andnatural activation areseparate. Preserve local exploitation/foreign expansion,EastAsia versusSoutheastAsia versusNorthSea,the informant's moral discomfort/former Kuhn service/false trading allegation/reported young leader's justice andanger/conditional lethal risk,andMaria's explicit personal safety promise. Preserve Camille's Argot membership andexplicit nonmembership inHodram's fleet,unspecified closeness toLil,temporary separate travels,tentative whereabouts nearBatavia andunexplained present reluctance tosee her. No invented romance,kinship,rank,commodity,assassin technique,current city,date,completed travel,battle,reward orguaranteed mechanic.

The v2 manuscript has48 proposed revisions and19 individually justified retentions,with exact file-qualified clean/current/effective references andsource glosses. All67 formatting gates remainfalse. Actual current route3 catalogue lookup replaces eight rawstorage lines;those effective paragraphs were reviewed ratherthan mistaking old rawKamil/Kuen fordisplayed English. The initial v1's47 revisions/20 retentions andall findings remain. Three measured wrap risks prompted faithful natural rephrasing;the previously justified B35R68 retention ispreserved withwhy a later display-driven revision wasneeded.

OwnV7717 strictMaria captain3/mask8 context binds134 original clean/current dispatches,eight static selectors1/3/9/10/26/74/116/155,eight voices and16 progressive/full name getters. Native source fields supportHodramBergstrom/fullJoakim,MariaLi/fullHuamei,CamilleOverijssel/fullMarinus,XienYan,JulianLopes,RichardTownsend andPortWorker. Region metadata isnot asurname andport-worker brother wording isnot kinship. Actor155 isclean配下/subordinate withSoutheastAsia metadata;progressive saysSailor whilecatalogue saysRetainer. A consistent replacement remainspending broader151–159 consumers,no global name change. Full207-name/role/alias review andactual headers/fullcatalogueUI remainopen.

Eighty default/source paragraph macro alignments bindFI5/Maria,FA2/Li,FO7/LiClan andall12 real substitutions(FI1/FA4/FO7). The generic Maria profile stillhas historicalFA3/Lee metadata;this batch uses measured scopedvalues without changing global profiles orapproving older consumers. Three original event getters andten current/source predicate executions preserveABI/canaries/unowned4MiB;their snapshot results donot prove natural eligibility orfullbranch execution. Existing exact system-only Maria unlock remainsdisclosed,earned=false;no historicalRAM overlay orruntime/roster/roles/funds/RNG/condition forcing.

All67 v1 complete logical paragraphs passed268 original native macro/literalI/F alignments. Three revised paragraphs passed12 fresh alignments;64 exact unchanged bodies/selectors reuse256 own-current cases,for268 final logical coverage. These areoffline CPU byte checks,not native font pixels oractual gameplay. The initial automatic67 plans/five weak-boundary warnings across three records arepreserved. Cost-only successor7734 leftthose warnings andexited1;itisnot aROM failure orcounted rejection. Faithful v2 rephrasing yieldszero QA warnings/errors and22 individually justified row-count infos. The current plan has66 one-page speeches andB108R111 five rows/two pages,68 pages total;native font/bounds/pagination,compiled/stored,source controls,actual scenes,production andrelease remainpending. No warning waswaived,global font/profile/weak-boundary rule changed ormanual break/padding authored.

No new emulator runs orgameplay coverage wereadded. Retain all completedV7717 checks,earlier actual/timing/RNG/state/calendar/actor/RGB limits andall broad unfinished inventories. The full four-storyline,earlier translations,shared town/shop/random/Help/player prose,all207 names andretrospective earlywrap objective remainsactive. Graphics/all18 plaques andlater older-record technical work stayseparate."""
def restore(new):
    out=deepcopy(new);change=out.pop(KEY)
    for op in reversed(change['inverse_operations']):
        parent,key=parent_at(out,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return out
def evidence_paths():
    return [PRIOR,MANUSCRIPT,NAMES,SOURCE,GLOSS,CURRENT,CONSUMERS,NATIVE_NAMES,ENTRY,LOGICAL,PLANS,
        Path('translations/maria_B34_B108_B35_editorial_manuscript_v1.json'),
        Path('work/analysis/maria_story_layout_v7733/67_automatic_full_width_plans_all_base_QA_preserved.json'),
        Path('work/analysis/maria_story_wrap_v7734/67_refined_full_width_plans_no_prose_changes_all_QA_preserved.json'),
        Path('translations/release_stack.json'),Path(__file__)]
def gates():
    prior,doc,plans,names=map(read,[PRIOR,MANUSCRIPT,PLANS,NATIVE_NAMES])
    assert prior['candidate_sha256']==doc['current_ROM_sha256']==plans.get('candidate_sha256',doc['current_ROM_sha256'])==sha(Path(doc['current_ROM']).read_bytes())
    assert plans['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and len(doc['records'])==67 and not plans['unresolved']
    assert sum(r['decision']=='revision' for r in doc['records'])==48 and sum(r['decision']=='retention' for r in doc['records'])==19
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(read(CONSUMERS)['source_current_dispatches'])==134 and len(read(ENTRY)['native_predicate_cases'])==10
    assert names['actual_original_captain_ID']==3 and len(names['native_sixteen_progressive_and_full_name_consumers']['rows'])==16
    assert sum(r['expected_native_pages'] for r in plans['records'])==68 and len([r for r in plans['records'] if r['expected_native_pages']==2])==1
    assert plans['fresh_logical_alignment_cases']==12 and plans['exact_own_current_logical_alignment_cases_reused']==256
    assert not any(i['severity'] in ['warning','error'] for r in plans['records'] for i in r['base_QA']['issues'])
    return prior,doc,plans
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,doc,plans=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
        assert tuple(old[k] for k in COUNTERS)==VALUES and old['goal_status']=='active' and not old['full_goal_complete']
        candidate=old['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
        assert candidate['profile']=='all-routes-unified-v7717' and len(manifest['batches'])==629 and len(manifest['checks'])==18 and all(manifest['checks'].values())
        assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
        assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
        completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        keys={historical_key(r) for r in doc['records']};assert len(completed)==6855 and len(keys)==67 and not completed&keys
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old['unfinished_editorial_scope_v7722'];assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(manuscript=str(MANUSCRIPT),file_qualified_positions=67,proposed_revisions=48,proposed_retentions=19,names=str(NAMES),plans=str(PLANS),
            source_dependency_chain=[34,108,35],all67_formatting_false=True,native_font_compiled_stored_controls_actual_production_release_pending=True,new_credit=0)
        inventory['Maria_story_shared_actor155_label_v7736']=dict(native_proof=str(NATIVE_NAMES),progressive='Sailor',catalogue='Retainer',clean='配下',
            regional_metadata='東南アジア',replacement_not_selected_orchanged=True,broader151_159_andother_consumers_pending=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        ROOT.mkdir(parents=True);inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),all_prior_leads_full_scope_andhistory_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(plans=str(PLANS),one_two_page_risk='SC3B108R111',all67_unapproved=True,all_old_warnings_preserved=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes');put(['coverage_units',ri,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [*evidence_paths(),inv]}
        new[KEY]=dict(records=deepcopy(doc['records']),proposed_revisions=48,proposed_retentions=19,native_names=str(NAMES),plan=str(PLANS),
            summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,new_source_prose_reviews=0,new_completed_records=0,new_revisions=0,new_retentions=0,
            no_ROM_registry_completed_family_orcounter_changes=True,new_emulator_runs=0,new_gameplay_coverage=0,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==candidate
        assert tuple(new[k] for k in COUNTERS)==VALUES
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7736: Maria linked story arc67 contextual drafts; native display andintegration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            p=Path('docs')/name;prefix=('# Current editorial handoff - V7736; V7717 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
        files=[]
        for i,(p,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
            files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,zero_credit=True,full_goal_complete=False))
        print('Six pending checkpoint targets staged;67 uncredited drafts,all counts andV7717 unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES
        assert new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:
            assert sha(Path(e['planned']).read_bytes())==e['planned_sha256']
            assert sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse audit passes;all prior roots,completed records,counts andROM references recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,no_ROM_orcredit_counter_change=True,full_goal_complete=False))
            print('Six audited pending checkpoint targets applied;67 uncredited drafts;V7717 unchanged.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                Maria_story67_uncredited=True,proposed_revisions=48,proposed_retentions=19,manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
                source_chain=[34,108,35],native_names_eight_speakers16getters=True,current_source_dispatches=134,
                final_logical_alignment_coverage=268,fresh_changed_alignments=12,exact_own_current_alignments_reused=256,
                final_automatic_plans=67,planned_pages=68,focused_two_page_risk='SC3B108R111',all_formatting_gates_false=True,
                shared_actor155_Sailor_Retainer_conflict_open=True,new_credit=0,new_emulator_runs=0,new_gameplay_coverage=0,
                all_prior_roots_records_families_counters_andROM_refs_recover_exactly=True,pending_checkpoint=str(ROOT/'application_receipt.json'),
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('V7736 verified:67 uncredited contextual drafts;V7717/6855completed unchanged.Full objective active;next compiled/native font,controls,actual andrelease checks.')
