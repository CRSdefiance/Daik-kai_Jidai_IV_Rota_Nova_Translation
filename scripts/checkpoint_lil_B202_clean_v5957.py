"""Record19 uncredited clean glosses while preserving the verified cumulative build."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_clean_checkpoint_v5957')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5958')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5953/verified_handoff.json')
INV=Path('work/analysis/lil_B202_clean_inventory_v5955/all_clean_B202_speeches_before_predecessor_comparison.json')
GLOSS=Path('work/analysis/lil_B202_clean_context_v5956/all19_clean_unsolicited_book_handoff_pursuit_and_self_interested_request_glosses.json')
KEY='Lil_B202_clean_source_v5957'
SCOPE='unfinished_editorial_scope_v5957'
NEXT='Continue B202 from the sealed complete clean inventory5955 and whole-exchange gloss5956 before reading older English. Bind all four source selectors2/18/157/147 to exact clean/current fields,approved names and voices without borrowing B201 identities. Review anonymous speaker labels contextually,retaining source primary/secondary/middle fields and distinct name consumers;do not invent theft,police,kinship,rank or ownership provenance from a chase alone. Map clean/current complete preambles and all26 commands/seven opaque leaves,including two632A,one4835,twoA000,one4721 and the four-byte end582 in588 stored/586 logical bytes/two tailzeros. The source explicitly names ガラスの製法辞典;bind the spoken title to clean item data/current widget separately rather than reusing the unnamed-rope policy. The literal Dictionary of Glassmaking gloss is not an approved target title. Bind actual source/context,entry,dispatch,macro absence,display and effect scope before target prose. Then compare old English as evidence and complete natural-dialogue-v2/native/reference/representative/release checks. Keep19 glosses uncredited until all necessary gates pass and registered integration is verified. Reuse B201/V5947 checks absent a concrete new risk. Preserve the full four-storyline/earlier dialogue/shared town/shop/random/Help/prose,retrospective premature wrapping and207-entry proper-name/role/alias review. Preserve every artifact and prior lead. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
DETAILS='V5957 records a fresh clean-only B202 inventory and whole-exchange gloss:19 progressive speeches,26 commands,selectors2x8/18x6/157x3/147x2,zero FE/FI/FA/FO,choices or typed styles. Source588 stored/586 logical bytes has two alignment zeros and a complete four-byte end at582. Seven opaque nonspeech leaves remain uninterpreted beyond their exact inventory. A stranger abruptly gives02 an object,another speaker pursues them,and02 remains bewildered.18 asks what happened,examines the book and explicitly reads ガラスの製法辞典,advises keeping freely given things,then asks to see it later;02 recognizes the motive. Preserve the sudden handoff,confusion,unfinished objection and dry payoff. Do not infer criminality,police,rank,kinship or legitimate ownership from the chase alone. Names/voices/roles,item-title data/widget,effects,source gameplay,current references,English comparison and all target gates remain pending. Older English was not read. These19 clean glosses add no source-prose or completion credit,no ROM and no emulator run. Registered experimental V5947 and its exact clean-input patch remain unchanged and verified with589 batches/114 accepted/18 release checks. Coverage stays6308 completed/6311 source-prose/3953 integrated revisions/2355 justified retentions/SC24423/SC396/routes4709/4709,zero pending credited route drafts. B201 is integrated once;main V4701 remains promoted. All earlier values,ROMs,translations,failed producers and unresolved scope remain preserved. The full editorial/name-review goal remains active.'
def inverse(new):
    d=deepcopy(new);entry=d.pop(KEY);d.pop(SCOPE);d['latest_checkpoint']=entry['previous_latest_checkpoint'];return d
def immutable_checks():
    prior=read(PRIOR);release=read('work/analysis/lil_B201_release_v5948/registered_release_verification.json')
    for k in ['candidate','patch']:assert prior[k+'_sha256']==release[k+'_sha256']==sha(Path(release[k]).read_bytes())
    for p,h in read('releases/all_routes_unified_v5947/immutable_input_audit.json')['inputs'].items():assert sha(Path(p).read_bytes())==h
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(manifest['batches'])==589 and all(manifest['checks'].values())
    return prior
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);mode=p.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();prior=immutable_checks();before=LEDGER.read_bytes();assert sha(before)==prior['ledger_sha256'];old=json.loads(before);gloss=read(GLOSS);assert gloss['prior_English_speech_unread'] and len(gloss['records'])==19 and gloss['new_review_credit']==0
        new=deepcopy(old);assert KEY not in new and SCOPE not in new;summary=DETAILS+'\n\n'+NEXT
        inventory=deepcopy(read(old['unfinished_editorial_scope_v5952']['path']));inventory['next_focus']=NEXT;inventory['historical_B202_clean_pending_before_v5957']=inventory.pop('next_Lil_B202_clean_review_pending')
        inventory['Lil_B202_clean_only_uncredited_v5957']=dict(clean_inventory=str(INV),clean_inventory_sha256=sha(INV.read_bytes()),clean_gloss=str(GLOSS),clean_gloss_sha256=sha(GLOSS.read_bytes()),source_speech_objects=19,source_commands=26,prior_English_unread=True,reviewed_target_objects=0,new_source_prose_or_completion_credit=0,actual_names_voices_roles_title_widget_controls_source_paths_and_English_pending=True)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        evidence={str(p):sha(p.read_bytes()) for p in [INV,GLOSS,PRIOR,Path(__file__),Path('releases/all_routes_unified_v5947/verification.json')]}
        new[SCOPE]=dict(path=str(scope),sha256=sha(scope.read_bytes()),B202_clean_only_uncredited_speeches=19,retrospective207_names_and_all_wider_editorial_families_preserved=True,full_goal_complete=False)
        new[KEY]=dict(summary=summary,next=NEXT,previous_latest_checkpoint=old['latest_checkpoint'],evidence=evidence,source_speech_objects=19,new_source_prose_reviews=0,new_completed_records=0,new_ROMs=0,new_emulator_runs=0,goal_turn_classification='progress',previous_goal_turn_classification='progress',full_goal_complete=False)
        new['latest_checkpoint']=summary;assert inverse(new)==old
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)};section='## V5957: B202 clean-only whole-exchange gloss;V5947 stays verified\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            target=Path('docs')/name;text=target.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5957\n\n'+section+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[target]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for i,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{i:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False));print('Six targets staged;19 clean-only B202 glosses,no credit or candidate change.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned']);assert inverse(new)==old;prior=immutable_checks()
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['records_editorially_completed']==6308 and new['records_with_source_and_prose_pass']==6311 and new['goal_status']=='active' and not new['full_goal_complete']
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
            result={**prior,'previous_verified_handoff':str(PRIOR),'previous_verified_handoff_sha256':sha(PRIOR.read_bytes()),'ledger_sha256':sha(LEDGER.read_bytes()),'all_prior_history_and_current_candidate_exactly_preserved':True,'latest_checkpoint_key':KEY,'next_B202_clean_source_glosses':19,'B202_target_reviews_uncredited':True,'prior_English_B202_speech_unread':True,'new_source_prose_or_completion_credit':0,'goal_turn_classification':'progress','evidence':plan['evidence'],'producer_sha256':sha(Path(__file__).read_bytes())}
            save(VERIFY/'verified_handoff.json',result);print('Verified V5957 clean-only checkpoint:V5947/6308 completed unchanged,B20219 glosses uncredited;full goal active.')
