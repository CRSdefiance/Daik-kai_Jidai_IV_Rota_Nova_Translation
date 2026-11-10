"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_wrap_checkpoint_v7834')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7835')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7830/verified_handoff.json')
PROOF=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='retrospective_B218_predicate_layout_pending_v7834'
SCOPE='unfinished_editorial_scope_v7834'
FINDING="The retrospective contraction/question-tag scan examined the 558 available recorded formatted_markup plans among6938 completed records. It found13 leads in11 native groups across all four storylines. Every lead binds exactly to one original source speech and one live V7821 speech with its complete preamble; all13 current raw bodies have no catalogue override. This is offline inventory and catalogue evidence, not new actual scene coverage. The other6380 records were not covered by this markup-only heuristic.\n\nLil B218 was reread as a complete13-speech clean/current exchange. All13 wordings are retained with individual reasons: practical Lil presses for a weapon's location while Ian explains his fascination with uncertain ancient legend. For R27, the automatic planner now proposes (Ian's interested? / That's a surprise.) instead of splitting That's / a surprise. No words, punctuation, macros, source controls, physical width or font change. Only this exact paragraph gains the ordinary that's/a boundary preference;12 compiled plans remain exact. All13 unmodified base-QA checks pass, without warning removal or waivers.\n\nThis is a pending retrospective layout proposal. New complete native characters/planes/bounds, storage/control/inverse, focused actual evidence, frozen policy and registered integration remain to be checked. No additional source/prose, completion or integrated-revision credit is added for revisiting already credited lines.\n\nThe original shared151-159 progressive nameplate finding remains: clean 水夫 supports Sailor, independently of the 配下/Retainer full-name field. Full-name and remaining indirect/typed/COMMON/UI consumers and all207 names remain open. Keep the full editorial objective and all other wrap/source/story/shop/town/random/Help/player-prose leads. MainV4701 stays unchanged; the separate unified test package remains canceled."
NEXT="Continue the full objective from verified V7835 and experimental current V7821. First advance the pending B218 R27 automatic-layout proposal in translations/lil_B218_retrospective_layout_manuscript_v1.json and work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json. The complete13 clean/current speeches were reviewed, all words retained, and only one automatic compiled plan changed. Obtain Lil's own current V7821 context when needed; do not substitute Maria's or historical RAM. Validate the changed native display and storage/controls/inverse, relevant actual behavior and policy, then integrate through the registered cumulative workflow and exact clean-input patch without duplicate editorial credit.\n\nKeep all13 retrospective leads in work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json. They are candidates, not automatic defects or global boundary rules. The heuristic covers558 existing markup plans, not all6938 records; extend coverage through exact source/current consumers. Evaluate each complete exchange and measure alternatives; retain ordinary wraps with reasons.\n\nContinue all four storylines and earlier translated exchanges, broad practical shared shop/town/random capture, Help and all remaining player-facing prose, all207 names/roles/aliases and earlier unfinished inventories/counterpart/item/display leads. Preserve the original151-159 水夫/Sailor progressive-name retention and review their separate full-name/other consumers. Preserve every generated ROM, translation, draft, executed producer, failure, trace and proof. Keep graphics/all18 plaques and the later older-record technical re-audit separate. No canceled separate test package, promotion, pruning, commit or push."
SUMMARY=INTRO+'\n\n'+FINDING+'\n\n'+DETAILS

def restore(value):
    new=deepcopy(value);entry=new.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(new,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return new

def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    plan=read('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json')
    leads=read('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
    assert plan['manuscript_sha256']==sha(PROOF.read_bytes()) and len(proof['records'])==13
    assert plan['changed_IDs']==['DK4_MES_B218_R0027'] and proof['wording_retentions']==13
    assert proof['proposed_automatic_layout_revisions']==1 and proof['unchanged_exact_compiled_plans']==12
    assert proof['all13_complete_clean_andcurrent_exchanges_read'] and proof['proposed_formatting_native_storage_actual_policy_release_pending']
    assert leads['lead_count']==13 and len(leads['source_current_native_groups'])==11 and not leads['binding_issues']
    assert proof['no_new_completion_orintegrated_revision_counter_credit'] and not proof['new_credit']
    assert proof['current_ROM_sha256']==prior['candidate_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return prior,proof

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,proof=gates()
    if mode=='stage':
        assert not ROOT.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old
        assert tuple(old[k] for k in COUNTERS)==AFTER and old['goal_status']=='active' and not old['full_goal_complete']
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        oldscope=old['unfinished_editorial_scope_v7829'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            wordings_retained=13,pending_layout_revisions=1,other_exact_compiled_reuses=12,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,native_storage_actual_policy_andrelease_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json'),
            Path('work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json'),
            Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json'),
            Path('scripts/plan_retrospective_B218_predicate_v7833.py')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            wording_retentions=13,pending_automatic_wrap_revisions=1,no_duplicate_dialogue_credit=True,
            new_credit=0,new_emulator_runs=0,new_native_getter_executions=0,
            only13_metadata_leads_andone_pending_changed_plan_not_broad_wrap_approval=True,
            full_scope_all13_other_wrap_leads_andnames_remain_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7834: Retrospective wrap scan and one pending automatic refinement; V7821 current\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7834; V7821 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six retrospective-wrap checkpoint targets staged;all counts andcurrentROM unchanged.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER
        assert new['goal_status']=='active' and not new['full_goal_complete']
        assert new['completed_editorial_families']==old['completed_editorial_families'] and new['current_integrated_candidate']==old['current_integrated_candidate']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                all_prior_roots_families_counters_currentROM_andhistory_recover_exactly=True,zero_credit=True,full_goal_complete=False))
            print('Deep inverse andall six before/planned hashes pass;zero credit.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,no_ROM_orcredit_change=True,full_goal_complete=False))
            print('Six audited retrospective-wrap checkpoint targets applied;V7821/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                retrospective_B218_R27_layout_pending=True,retrospective_wrap_leads=13,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_layout_manuscript=str(PROOF),pending_layout_manuscript_sha256=sha(PROOF.read_bytes()),
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=0,new_native_getter_executions=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7835 verified:13wrap leads/one pending automatic refinement recorded;V7821/6938complete remain.Fullobjective active.')
