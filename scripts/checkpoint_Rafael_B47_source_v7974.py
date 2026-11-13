"""Reversibly checkpoint fresh clean B47 glosses without credit or current-English exposure."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B46_v7969 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_source_checkpoint_v7974')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7975')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7970/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B47_clean_context_v7972/complete_clean_SC0_B37_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json')
KEY='Rafael_SC0B47_clean_source_gloss_pending_native_current_v7974'
SCOPE='unfinished_editorial_scope_v7974'
SUMMARY="""Rafael B46 is complete in current registered experimental cumulative V7964. Its 24 speeches and two menu labels were credited once: seven wording revisions and nineteen justified retentions. The ledger remains at 6,976 completed records, 6,979 source/prose records and drafts, 4,361 integrated wording revisions and 2,615 retentions. Completed SC0 is 173; the reviewed/completed route subset is 5,376. All 635 manifest batches and 114 accepted layers remain, with 18 passing release checks, 110 passing regressions, exact approved-reference equality and a byte-exact clean-input patch reconstruction. Fresh ordinary Rafael startup runs 4,001 frames; six whole-frame, captain 0 and whole-actor controls match V7911. The sheet was directly viewed. Main V4701 remains unchanged.

Verified B46 completion is work/analysis/editorial_handoff_verification_v7970/verified_handoff.json; the exact final coverage ledger is translations/rafael_B46_contextual_final_review_v1.json. Its frozen formatting policy passes all 24 speech plans and two labels, with 300 actual-changing expected-guard rejections and all 14 original row-count infos retained without waivers. Atomic production passes whole-ROM reconstruction and 187 independent precommit rejections with dependency checks bypassed. The first V7960 precommit metadata failure and its source-locked correction remain preserved. Preserve all earlier B46 source/native/stored/actual proofs, including the four 16,001-frame scene jobs, 214 complete holds, 14 viewed sheets, source accept4930 highlight-off sample, real timing/RNG/component/calendar/RGB differences and disclosed initialized-entry scope. No new full-route, natural B46 activation, hardware, future-state or complete causal equivalence claim is added.

The next source-only lead is SC0 B47: 15 complete clean Japanese speech objects, 48 commands, 1,284 stored/logical bytes, no tail and zero completed-coverage overlap. Its original EV0 event47/category5/action48 requires event37. The complete clean B37 prerequisite context contains 72 stored speech objects and 120 commands and itself requires event36. Fresh B47 glosses followed reading that whole source context; B47 current English remains unread. B37 was read for context only and receives no editorial or gameplay credit.

B47 moves from guarded relief about Mediterranean passage to advice about stronger powers, delaying Mediterranean trade, avoiding forced contracts or provocation, and still visiting large cities because they may have skilled navigators. Ship improvements and personal training follow. Rafael feels the amount of work, then resolves to do his best. Two stored Rafael alternatives mention the Ottoman Pasha forces alone or both the Spanish Valdes and Ottoman forces. Their exact predicates, relative spans, exclusivity and selected gameplay path remain unproved. Do not treat both variants as one spoken exchange. Do not invent kinship, rank, alliance, guaranteed protection or recruitment, a ban on all visits, an immediate destination or a completed ambition. Actor04's localized identity has not yet been approved for this batch.

Exact source packet: work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json. Complete prerequisite context: work/analysis/Rafael_B47_clean_context_v7972/complete_clean_SC0_B37_EV0_andcoverage_before_current_English.json. Fresh 15-record glosses: work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json. This is a source/context preparation checkpoint, with zero source/prose completion credit, zero new emulator runs and no ROM, registry, pin, patch or manuscript mutation."""
NEXT="""Continue from verified V7975/current registered V7964. B46 is complete; reuse its finished checks unless a new change or concrete unresolved risk warrants more testing. Current Rafael native input is work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json. Other routes' earlier contexts remain historical until properly rebound or recaptured.

For B47, begin with the recorded clean Japanese and whole B37 prerequisite glosses. Before opening B47 current English, bind all original source actors/names and display consumers, especially actor04, and execute/interpret its original 8000 predicate, relative branches, 48 complete commands and source-owned entry dependencies. Determine how the two Rafael alternatives compose without assuming chronology or activation from block numbers. Keep the source-only order explicit. Then compare all current records in complete context and make natural American English revisions or justified retentions, preserving every fact, qualification, voice, runtime substitution and speaker/layout control. Native wrapping, complete leading/trailing characters, bounds, pagination, representative actual scene coverage, frozen policy, atomic production and registered integration remain pending. Do not count the 72 contextual B37 objects as a new completed family.

The full editorial goal remains active across all four storylines and earlier translations, broad practical shared shop/town/random capture, Help and remaining prose, all 207 names/roles/aliases and premature wrapping. Preserve all previous unfinished inventories, twelve remaining contraction/question-tag wrap leads and the unscanned records beyond 558 recorded plans. Incidental B127/Sailor captures are previously exposed leads without editorial credit. Retain the Sailor151-159 versus Retainer consumer distinction and every older item, counterpart and display lead. Graphics/all 18 plaques and the later older-record technical re-audit remain separate, including normal-end value carry, B35R65's source-only nineteenth cell and all measured timing, highlight, RNG, component, calendar and RGB limits. Preserve every ROM, translation, draft, failed/executed producer and proof. No separate unified test package, promotion, pruning, commit or push."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    prior,source,context,gloss=map(read,[PRIOR,SOURCE,CONTEXT,GLOSS])
    assert prior['completed']==6976 and prior['manifest_batches']==635 and prior['Rafael_B46_completed_once']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(gloss['records'])==15 and gloss['all15_glosses_fresh_before_current_English_exposure']
    assert all(r['current_English_body_unread'] and r['source_gloss_not_current_English_derived'] for r in gloss['records'])
    assert len(source['groups'][0]['commands'])==48 and source['groups'][0]['completed_coverage_overlap']==0
    assert len(context['groups'][0]['records'])==72 and context['groups'][0]['block']==37
    assert gloss['source_packet_sha256']==sha(SOURCE.read_bytes()) and gloss['prerequisite_context_sha256']==sha(CONTEXT.read_bytes())
    return prior

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,CONTEXT,GLOSS,Path(__file__)]}
        pending=dict(status='clean-source-whole-context-glossed-native-names-branches-current-English-prose-format-actual-release-pending',
            file_path='/data/SC0.DK4',block=47,source_objects=15,source_commands=48,
            source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),prerequisite_context=str(CONTEXT),prerequisite_context_sha256=sha(CONTEXT.read_bytes()),
            fresh_gloss=str(GLOSS),fresh_gloss_sha256=sha(GLOSS.read_bytes()),current_English_unread=True,
            actor04_identity_andtwo_alternative_native_composition_pending=True,B37_context_only_not_completed=True,
            new_credit=0,new_emulator_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending);ROOT.mkdir(parents=True)
        scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,
            goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7974: B46 integrated; B47 clean source/context glossed before current English\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7974; V7964 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B47 source-only checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_restores_all_prior_values=True,all_counters_candidate_andfull_scope_unchanged=True,new_credit=0,full_goal_complete=False))
            print('B47 checkpoint deep inverse passes;all prior records,counts,candidate andscope preserved.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,new_credit=0,full_goal_complete=False))
            print('B47 source-only checkpoint applied;counts andcurrentV7964 unchanged.Full objective active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,
                pending_source_batch=KEY,B47_clean_gloss_records=15,B47_current_English_unread=True,new_credit=0,new_emulator_runs=0,new_actual_frames=0,
                all_sessions_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7975/currentV7964:6976completed;15 B47 clean glosses,currentEnglish unread,native/name/branch/prose/display/release pending.Full goal active.')
