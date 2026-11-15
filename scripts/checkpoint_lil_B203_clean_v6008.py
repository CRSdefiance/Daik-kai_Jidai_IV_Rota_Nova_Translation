"""Record22 uncredited clean glosses while preserving the verified cumulative build."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_clean_checkpoint_v6008')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6009')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6004/verified_handoff.json')
INV=Path('work/analysis/lil_B203_clean_inventory_v6006/all_clean_B203_speeches_before_predecessor_comparison.json')
GLOSS=Path('work/analysis/lil_B203_clean_context_v6007/all22_clean_cordyceps_book_offer_and1000_to100_negotiation_glosses.json')
KEY='Lil_B203_clean_source_v6008'
SCOPE='unfinished_editorial_scope_v6008'
NEXT='Continue B203 from complete clean inventory6006 and whole-exchange gloss6007 before reading older English. Bind source selectors2/76/170 and the separate FE notice to exact clean/current names,roles,voices and display consumers without borrowing B202 actors or aliases. Retrospectively review awkward anonymous labels against the Japanese and actual scene;preserve all207 names/roles/aliases in scope. Preserve the cordyceps/Chinese medicinal context as character dialogue,the unspecified offered reference work,hesitation about an expensive-looking gift,teasing about companion interest and1000-to100 spoken negotiation without inventing kinship,rank,profession,provenance,guaranteed efficacy or payment semantics. Bind actual source scene,item14 assumptions must not be inherited,picture/widget/native item identity,entry,all31 commands,nine nonspeech leaves,one FE/FI charm+1 and four-byte end810 in816 stored/814 logical bytes/two tailzeros. There is no explicit spoken book title. Preserve clean references,then compare old English as evidence and complete natural-dialogue-v2/native/reference/representative/release gates. Keep22 glosses uncredited until necessary gates pass and registered integration is verified. Reuse sealed B202/V5998 checks absent a concrete new risk. Keep every storyline,earlier translations,shared town/shop/random/Help/prose,premature wraps and207 names open. Preserve all artifacts and earlier leads including following B43 source-item/Local Product,Samwell and Alexandria. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
DETAILS='V6008 records a fresh clean-only B203 inventory and whole-exchange gloss:22 objects,21 progressive speeches plus one FE/FI charm+1 notice,31 commands,selectors76x6/2x8/170x7/254x1,zero FA/FO,choices or typed styles. Source816 stored/814 logical bytes has two alignment zeros and a complete four-byte end at810. Nine nonspeech leaves remain exact and uninterpreted beyond inventory:one4820,one4735,one6003,one632E,fourA000 and the end.4C reacts to an insect with apparent grass growing on it;AA identifies cordyceps and describes its Chinese medicinal use. AA then offers a reference work about medicinal materials.02 hesitates over its apparent value;AA says it is no longer needed,then teases4C interest.4C admits wanting to read the book.02 proposes paying1000 gold;AA accepts100 instead. No explicit book title is spoken. Preserve uncertain discovery,older colloquial/teasing voices,unfinished objection,embarrassed admission,generosity and exact amounts. Names/roles/voices,actual source scene,item/widget identity,payment/effects,current references,old-English comparison and all target gates remain pending. These22 clean glosses add no source-prose/completion credit,no ROM and no new emulator run. Registered cumulative experimental V5998 and its exact clean-input patch remain verified with590 batches/114 accepted/18 release checks. B20219 reviews were integrated once:six revisions/13 justified retentions. Coverage stays6327 completed/6330 source-prose/3959 integrated revisions/2368 justified retentions/SC24442/SC396/routes4728/4728,zero credited route drafts pending. Main V4701 remains promoted. All earlier root/nested history,ROMs,translations,failed producers and unresolved scope are preserved. Full editorial and207-entry name/role/alias review remain active.'
def inverse(new):
    d=deepcopy(new);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def immutable_checks():
    prior=read(PRIOR);release=read('work/analysis/lil_B202_release_v5999/registered_release_verification.json')
    for k in ['candidate','patch']:assert prior[k+'_sha256']==release[k+'_sha256']==sha(Path(release[k]).read_bytes())
    for p,h in read('releases/all_routes_unified_v5998/immutable_input_audit.json')['inputs'].items():assert sha(Path(p).read_bytes())==h
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==590 and all(manifest['checks'].values())
    return prior
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();prior=immutable_checks();before=LEDGER.read_bytes();assert sha(before)==prior['ledger_sha256'];old=json.loads(before);gloss=read(GLOSS);assert gloss['prior_English_speech_unread'] and len(gloss['records'])==22 and gloss['new_review_credit']==0
        new=deepcopy(old);assert KEY not in new and SCOPE not in new;summary=DETAILS+'\n\n'+NEXT
        inventory=deepcopy(read(old['unfinished_editorial_scope_v6003']['path']));inventory['next_focus']=NEXT;inventory['historical_B203_clean_pending_before_v6008']=inventory.pop('next_Lil_B203_clean_review_pending')
        inventory['Lil_B203_clean_only_uncredited_v6008']=dict(clean_inventory=str(INV),clean_inventory_sha256=sha(INV.read_bytes()),clean_gloss=str(GLOSS),clean_gloss_sha256=sha(GLOSS.read_bytes()),source_speech_objects=22,source_commands=31,prior_English_unread=True,reviewed_target_objects=0,new_source_prose_or_completion_credit=0,actual_names_voices_roles_title_widget_controls_source_paths_and_English_pending=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        evidence={str(p):sha(p.read_bytes()) for p in [INV,GLOSS,PRIOR,Path(__file__),Path('releases/all_routes_unified_v5998/verification.json')]}
        new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),B203_clean_only_uncredited_speech_and_notice_objects=22,retrospective207_names_and_all_wider_editorial_families_preserved=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],evidence=evidence,source_speech_objects=22,new_source_prose_reviews=0,new_completed_records=0,new_ROMs=0,new_emulator_runs=0,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
        new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V6008: B203 clean-only whole-exchange gloss;V5998 stays verified\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;text=target.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V6008\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[target]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;22 clean-only B203 glosses,no credit or candidate change.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior=immutable_checks()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6327 and new['records_with_source_and_prose_pass']==6330 and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'independent_audit.json').exists();save(ROOT/'independent_audit.json',dict(deep_inverse_preserves_all_history=True,all_six_targets_and_immutable_inputs_verified=True,staged_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False));print('Checkpoint deep inverse,six targets and immutable inputs audited.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'independent_audit.json')['staged_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());workspace=Path.cwd().resolve()
            for e in plan['files']:assert Path(e['target']).is_relative_to(workspace) and Path(e['planned']).is_relative_to(ROOT.resolve())
            for e in plan['files']:
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,full_goal_complete=False));print('Six audited checkpoint files applied.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            result={**prior,'previous_verified_handoff':str(PRIOR),'previous_verified_handoff_sha256':sha(PRIOR.read_bytes()),'ledger_sha256':sha(LEDGER.read_bytes()),'all_prior_history_and_current_candidate_exactly_preserved':True,'latest_checkpoint_key':KEY,'next_B203_clean_source_glosses':22,'B203_target_reviews_uncredited':True,'prior_English_B203_speech_unread':True,'new_source_prose_or_completion_credit':0,'goal_turn_classification':'progress','evidence':plan['evidence'],'producer_sha256':sha(Path(__file__).read_bytes())}
            save(VERIFY/'verified_handoff.json',result);print('Verified V6008 clean-only checkpoint:V5998/6327 completed unchanged,B20322 glosses uncredited;full goal active.')
