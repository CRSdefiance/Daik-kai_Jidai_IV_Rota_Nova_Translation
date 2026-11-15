"""Reversibly record the source-specific name retention without new dialogue credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Maria_B36_v7826b import COUNTERS,AFTER,INTRO,DETAILS,NEXT as PREVIOUS_NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/name_consumer_checkpoint_v7829')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7830')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7827/verified_handoff.json')
PROOF=Path('work/analysis/retainer_source_consumer_v7828/nine_roles_original_Sailor_nameplate_distinct_from_internal_subordinate_field.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='shared151_159_original_progressive_name_consumer_v7829'
SCOPE='unfinished_editorial_scope_v7829'
FINDING="""The original clean progressive name getter explicitly displays the literal 水夫 for inclusive actor IDs151-159. Current Sailor is therefore a source-supported retention for these direct dialogue nameplates. Its code is unchanged from clean Japanese; the separate full-name getter has no such special case and uses the table's 配下 field, currently Retainer. The previous varied subordinate contexts do not invalidate the explicit source nameplate. Preserve the earlier evidence and supersede only that inference; full-name wording, indirect/typed/COMMON/other UI consumers and all207 names remain under review.

This finding uses read-only original disassembly, exact branch/literal/table bytes and 18 existing native getters rebound through byte-identical ARM9/COMMON. No new actual Japanese/English nameplate captures or native getter executions are claimed. The nine context samples cover129 speeches; all3150 census speeches remain unreviewed as a full set. No global name asset, ROM, credit or promotion changes."""
NEXT=PREVIOUS_NEXT.replace('verified V7827','verified V7830').replace(
    "Check the original Japanese progressive-name consumer before inferring a global label from internal fields.",
    "The original progressive 水夫/Sailor branch is now proved for IDs151-159; retain those direct nameplates. Review the separate 配下/Retainer full-name wording and remaining indirect/typed/COMMON/UI consumers against their own source consumers.")
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
    assert len(proof['rows'])==9 and proof['original_getter_calls_reused']==18 and proof['new_native_getter_executions']==0
    assert all(r['decision']=='retain-progressive-nameplate-wording' for r in proof['rows'])
    assert proof['branch_literal']['clean']['text']=='水夫' and proof['branch_literal']['current']['text']=='Sailor'
    assert proof['no_global_asset_change_ornew_dialogue_credit'] and not proof['new_credit']
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
        oldscope=old['unfinished_editorial_scope_v7826'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(proof=str(PROOF),proof_sha256=sha(PROOF.read_bytes()),finding=FINDING,
            direct_progressive_nameplates_retained=9,all_prior_inventories_andfull_scope_preserved=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        put(['formatting_watchlist',KEY],dict(proof=str(PROOF),finding=FINDING,full_name_andother_consumers_open=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        index=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
        put(['coverage_units',index,'next'],NEXT)
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('scripts/review_retainer_source_name_consumer_v7828.py'),
            Path('scripts/review_retainer_source_name_consumer_v7828b.py'),
            Path('work/analysis/retainer_source_consumer_repair_v7828b/provenance.json'),
            Path('work/analysis/maria_B36_completion_repair_v7826b/provenance.json')]}
        new[KEY]=dict(summary=FINDING,next=NEXT,proof=str(PROOF),evidence=evidence,inverse_operations=ops,
            direct_progressive_nameplate_retentions=9,these_are_name_decisions_not_new_dialogue_completion_credit=True,
            new_credit=0,new_emulator_runs=0,new_native_getter_executions=0,
            earlier_broad_inference_superseded_only_for_explicit_source_progressive_branch=True,
            full_name_andremaining_consumers_open=True,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and new['completed_editorial_families']==old['completed_editorial_families']
        assert new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V7829: Original shared speaker-name consumer clarified; V7821 current\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V7829; V7821 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,zero_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six name-consumer checkpoint targets staged;all counts andcurrentROM unchanged.')
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
            print('Six audited name-consumer checkpoint targets applied;V7821/6938completed unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                shared151_159_original_progressive_Sailor_source_verified=True,
                shared151_159_internal_role_not_progressive_display_source=True,
                shared151_159_full_name_andother_consumers_remain_open=True,
                source_name_consumer_proof=str(PROOF),source_name_consumer_proof_sha256=sha(PROOF.read_bytes()),
                unfinished_scope=SCOPE,next_required=NEXT,latest_checkpoint=KEY,
                new_credit=0,new_emulator_runs=0,new_native_getter_executions=0,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('V7830 verified:original Sailor consumer clarified;V7821/6938complete remain.Fullobjective active.')
